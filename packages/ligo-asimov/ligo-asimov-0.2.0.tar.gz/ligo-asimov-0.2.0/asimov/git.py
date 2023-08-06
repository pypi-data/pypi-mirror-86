import os
import shutil
import glob
import subprocess
import pathlib
import getpass

import git

from .ini import RunConfiguration
from asimov import config
# from asimov import logging

class AsimovFileNotFound(FileNotFoundError):
    pass

class MetaRepository():

    def __init__(self, directory):
        self.directory = directory
        os.chdir(directory)
        repos_list = glob.glob("*")
        self.repos = {event: os.path.join(directory, event) for event in repos_list}

    def get_repo(self, event):
        return EventRepo(self.repos[event])


class EventRepo():
    """
    Read a git repository containing event PE information.

    Parameters
    ----------
    directory : str 
       The path to the git repository on the filesystem.
    url : str
       The URL of the git repository
    """

    def __init__(self, directory, url=None):
        self.event = directory.split("/")[-1]
        self.directory = directory
        self.repo = git.Repo(directory)
        self.url = url

    def __repr__(self):
        return self.directory
        
    @classmethod
    def from_url(cls, url, name, directory=None):
        """
        Clone a git repository into a working directory,
        then create an EventRepo object for it.

        Parameters
        ----------
        url : str
           The URL of the git repository
        name : str
           The name for the git repository (probably the event name)
        directory : str, optional
           The location to store the cloned repository.
           If this value isn't provided the repository is
           cloned into the /tmp directory.
        """
        if not directory:
            tmp = config.get("general", "git_default")
            directory = f"{tmp}/{name}"
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


        # Replace an https address with an ssh address
        if "https" in url:
            url = url.replace("https://", "git@")
            final = "/".join(url.split("/")[1:])
            start = url.split("/")[0]

            url = f"{start}:{final}"
            
        try:
            repo = git.Repo.clone_from(url, directory)
            repo.git.execute(["git", "lfs", "install"])
            repo.git.execute(["git", "lfs", "fetch"])
            repo.git.execute(["git", "lfs", "pull"])
        except git.exc.GitCommandError:
            repo = git.Repo(directory)
            repo.git.stash()
            repo.remotes[0].pull()
        return cls(directory, url)

    def add_file(self, source, destination, commit_message=None):
        """
        Add a new file to the repository.
        
        Parameters
        ----------
        source : str, file path
           The path to the file to be added.
        destination : str
           The location to which the file should be copied in
           the repository, relative to the root of the repository.
           Any directories which do not exist already will be created.
        commit_message : str, optional
           The commit message for the git commit.
           Defaults to a description of the file addition.
        """

        destination_dir = os.path.dirname(destination)
        destination_dir = os.path.join(self.directory, destination_dir)
        pathlib.Path(destination_dir).mkdir(parents=True, exist_ok=True)

        destination = os.path.join(self.directory, destination)

        try:
            shutil.copyfile(source, destination)
        except shutil.SameFileError:
            pass

        if not commit_message:
            commit_message = f"Added {destination}"
        
        self.repo.git.add(destination)
        self.repo.git.commit("-m", commit_message)
        self.repo.git.push()
    
    def find_timefile(self, category="C01_offline"):
        """
        Find the time file in this repository.
        """
        os.chdir(os.path.join(self.directory, category))
        try:
            gps_file = glob.glob("*gps*.txt")[0]
            return gps_file
        except IndexError:
            raise AsimovFileNotFound

    def find_coincfile(self, category="C01_offline"):
        """
        Find the coinc file for this calibration category in this repository.
        """
        #os.chdir(os.path.join(self.directory, category))
        coinc_file = glob.glob(os.path.join(self.directory, category, "*coinc*.xml"))
        
        if len(coinc_file)>0:
            return coinc_file[0]
        else:
            raise AsimovFileNotFound

    def find_prods(self, name=None, category="C01_offline"):
        """
        Find all of the productions for a relevant category of runs
        in the event repository.

        Parameters
        ----------
        name : str, optional
           The name of the production. 
           If omitted then all production ini files are returned.
        category : str, optional
           The category of run. Defaults to "C01_offline".
        """

        self.update()
        os.chdir(os.path.join(self.directory, category))
        prods = glob.glob(f"{name}.ini")
        return prods

    def upload_prod(self, production, rundir, preferred=False, category="C01_offline", rootdir="public_html/LVC/projects/O3/C01/", rename = False):
        """
        Upload the results of a PE job to the event repostory.

        Parameters
        ----------
        category : str, optional
           The category of the job.
           Defaults to "C01_offline".
        production : str
           The production name.
        rundir : str 
           The run directory of the PE job.
        """
        
        preferred_list = ["--preferred", "--append_preferred"]
        web_path = os.path.join(os.path.expanduser("~"),
                                *rootdir.split("/"),
                                self.event,
                                production) # TODO Make this generic
        if rename:
            prod_name = rename
        else:
            prod_name = production

        command = [config.get("pesummary", "location"),
                   "--event", self.event,
                   "--exp", prod_name,
                   "--rundir", rundir,
                   "--webdir", web_path,
                   "--edit_homepage_table"]
        if preferred:
            command += preferred_list
        dagman = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = dagman.communicate()

        if err or  not "master -> master" in str(out):
            raise ValueError(f"Sample upload failed.\n{out}\n{err}")
        else:
            return out

    def upload_preferred(self, event, prods):
        """
        Prepare the preferred PESummary file by combining all of the
        productions for an event which are marked as `Preferred`
        or `Finalised`.

        Parameters
        ----------
        event : `asimov.gitlab.EventIssue`
           The event which the preferred upload is being prepared for.
        prods : list
           A list of all of the productions which should be included in the preferred file.
        """

        samples = []
        labels = []
        configs = []

        for prod in prods:
            samples.append(glob.glob(str(os.path.join(event.data[f"{prod}_rundir"], "posterior_samples"),)+"/*.hdf5")[0])
            run_ini = os.path.join(event.data[f"{prod}_rundir"], "config.ini")
            actual_config = RunConfiguration(run_ini)
            engine_data = actual_config.get_engine()
            labels.append(f"C01:{engine_data['approx']}")
            configs.append(str(os.path.join(event.data[f"{prod}_rundir"], "config.ini")))


        os.chdir(os.path.join(self.directory, "Preferred", "PESummary_metafile"))

        command = ["summarycombine",
                   "--webdir", f"/home/daniel.williams/public_html/LVC/projects/O3/preferred/{event.title}",
                   "--samples", ]
        command += samples
        command += ["--labels"]
        command += labels
        command += ["--config"]
        command += configs
        command += ["--gw"]

        dagman = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = dagman.communicate()

        print(out)
        print(err)

        copy(f"/home/daniel.williams/public_html/LVC/projects/O3/preferred/{event.title}/samples/posterior_samples.h5", os.path.join(self.directory, "Preferred", "PESummary_metafile"))
        self.repo.git.add("Preferred/PESummary_metafile/posterior_samples.h5")
        self.repo.git.commit("-m", "Updated the preferred sample metafile.")
        self.repo.git.push()

        event.labels += ["Preferred cleaned"]
        event.issue_object.save()

        return True

    def update(self, stash=False, branch="master"):
        """
        Pull the latest updates to the repository.

        Parameters
        ----------
        stash : bool, optional
           If true any changes which are in the local version
           of the repository are first stashed.
           Default is False.
        branch : str, optional
           The branch which should be checked-out.
           Default is master.
        """
        if stash:
            self.repo.git.stash()

        print("Running a git pull")
            
        self.repo.git.checkout(branch)
        self.repo.git.pull()
        self.repo.git.execute(["git", "lfs", "fetch"])
