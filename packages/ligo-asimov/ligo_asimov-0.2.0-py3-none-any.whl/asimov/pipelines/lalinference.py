"""LALInference Pipeline specification."""


import os
import glob
import subprocess
from ..pipeline import Pipeline, PipelineException, PipelineLogger
from ..ini import RunConfiguration
from asimov import config

class LALInference(Pipeline):
    """
    The LALInference Pipeline.

    Parameters
    ----------
    production : :class:`asimov.Production`
       The production object.
    category : str, optional
        The category of the job.
        Defaults to "C01_offline".
    """

    STATUS = {"wait", "stuck", "stopped", "running", "finished"}

    def __init__(self, production, category=None):
        super(LALInference, self).__init__(production, category)

        if not production.pipeline.lower() == "lalinference":
            raise PipelineException

    def detect_completion(self):
        """
        Check for the production of the posterior file to signal that the job has completed.
        """
        results_dir = glob.glob(f"{self.production.rundir}/posterior_samples")
        if len(results_dir)>0:
            if len(glob.glob(os.path.join(results_dir[0], f"posterior_*.hdf5"))) > 0:
                return True
            else:
                return False
        else:
            return False
                
    def build_dag(self, psds=None, user=None, clobber_psd=False):
        """
        Construct a DAG file in order to submit a production to the
        condor scheduler using LALInferencePipe.

        Parameters
        ----------
        production : str
           The production name.
        psds : dict, optional
           The PSDs which should be used for this DAG. If no PSDs are
           provided the PSD files specified in the ini file will be used
           instead.
        user : str
           The user accounting tag which should be used to run the job.

        Raises
        ------
        PipelineException
           Raised if the construction of the DAG fails.
        """
        os.chdir(os.path.join(self.production.event.repository.directory,
                              self.category))
        gps_file = self.production.get_timefile()
        ini = self.production.get_configuration()

        if not user:
            if self.production.get_meta("user"):
                user = self.production.get_meta("user")
        else:
            user = ini._get_user()
            self.production.set_meta("user", user)

        ini.update_accounting(user)

        if 'queue' in self.production.meta:
            queue = self.production.meta['queue']
        else:
            queue = 'Priority_PE'

        ini.set_queue(queue)

        ini.save()

        if self.production.rundir:
            rundir = self.production.rundir
        else:
            rundir = os.path.join(os.path.expanduser("~"),
                                  self.production.event.name,
                                  self.production.name)
            self.production.rundir = rundir

        #os.mkdir(self.production.rundir, exist_ok=True)
            
        command = [
            os.path.join(config.get("pipelines", "environment"),
            "bin",
            "lalinference_pipe"),
                   "-g", f"{gps_file}",
                   "-r", self.production.rundir,
                   ini.ini_loc
        ]
            
        pipe = subprocess.Popen(command, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, err = pipe.communicate()
        if err or "Successfully created DAG file." not in str(out):
            self.production.status = "stuck"
            if hasattr(self.production.event, "issue_object"):
                raise PipelineException(f"DAG file could not be created.\n{command}\n{out}\n\n{err}",
                                            issue=self.production.event.issue_object,
                                            production=self.production.name)
            else:
                raise PipelineException(f"DAG file could not be created.\n{command}\n{out}\n\n{err}",
                                        production=self.production.name)
        else:
            if hasattr(self.production.event, "issue_object"):
                return PipelineLogger(message=out,
                                      issue=self.production.event.issue_object,
                                      production=self.production.name)
            else:
                return PipelineLogger(message=out,
                                      production=self.production.name)

    def samples(self):
        """
        Collect the combined samples file for PESummary.
        """
        return glob.glob(os.path.join(self.production.rundir, "posterior_samples", "posterior*.hdf5"))
    def collect_logs(self):
        """
        Collect all of the log files which have been produced by this production and 
        return their contents as a dictionary.
        """
        logs = glob.glob(f"{self.production.rundir}/log/*.err") + glob.glob(f"{self.production.rundir}/*.err")
        messages = {}
        for log in logs:
            with open(log, "r") as log_f:
                message = log_f.read()
                messages[log.split("/")[-1]] = message
        return messages

    def submit_dag(self):
        """
        Submit a DAG file to the condor cluster.

        Parameters
        ----------
        category : str, optional
           The category of the job.
           Defaults to "C01_offline".
        production : str
           The production name.

        Returns
        -------
        int
           The cluster ID assigned to the running DAG file.
        PipelineLogger
           The pipeline logger message.

        Raises
        ------
        PipelineException
           This will be raised if the pipeline fails to submit the job.
        """

        os.chdir(self.production.rundir)

        self.before_submit()
        
        try:
            command = ["condor_submit_dag",
                                   os.path.join(self.production.rundir, f"multidag.dag")]
            dagman = subprocess.Popen(command,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        except FileNotFoundError as error:
            raise PipelineException("It looks like condor isn't installed on this system.\n"
                                    f"""I wanted to run {" ".join(command)}.""")

        stdout, stderr = dagman.communicate()

        if "submitted to cluster" in str(stdout):
            cluster = re.search("submitted to cluster ([\d]+)", str(stdout)).groups()[0]
            self.production.status = "running"
            self.production.job_id = cluster
            return cluster, PipelineLogger(stdout)
        else:
            raise PipelineException(f"The DAG file could not be submitted.\n\n{stdout}\n\n{stderr}",
                                    issue=self.production.event.issue_object,
                                    production=self.production.name)

    def after_completion(self):
        cluster = self.run_pesummary()
        self.production.meta['job id'] = int(cluster)
        self.production.status = "processing"
