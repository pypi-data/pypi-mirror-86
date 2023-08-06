"""Tests for the Bilby interface."""

import unittest
import shutil
import os
import git

from asimov.pipelines.bilby import Bilby
from asimov.event import Event
from asimov.pipeline import PipelineException

TEST_YAML = """
name: S000000xx
repository: {0}/tests/test_data/s000000xx/
working_directory: {0}/tests/tmp/s000000xx/
webdir: ''
productions:
- Prod3:
    rundir: {0}/tests/tmp/s000000xx/C01_offline/Prod3
    pipeline: bilby
    comment: PSD production
    status: wait

"""


class BilbyTests(unittest.TestCase):
    """Test bilby interface"""

    @classmethod
    def setUpClass(cls):
        cls.cwd = os.getcwd()
        repo = git.Repo.init(cls.cwd+"/tests/test_data/s000000xx/")
        os.chdir(cls.cwd+"/tests/test_data/s000000xx/")
        os.system("git add C01_offline/Prod3_test.ini C01_offline/s000000xx_gpsTime.txt")
        os.system("git commit -m 'test'")


    @classmethod
    def tearDownClass(cls):
        """Destroy all the products of this test."""
        os.system(f"{cls.cwd}/tests/tmp/-rf")
        os.system(f"{cls.cwd}/tests/test_data/s000000xx/.git -rf")
        try:
            shutil.rmtree("/tmp/S000000xx")
        except:
            pass

    def tearDown(self):
        os.system(f"{self.cwd}/tests/tmp/-rf")
        
    def setUp(self):
        """Create a pipeline."""
        self.event = Event.from_yaml(TEST_YAML.format(self.cwd))
        self.pipeline = Bilby(self.event.productions[0])
        out = self.pipeline.build_dag()

    def test_dag(self):
        """Check that a DAG is actually produced."""
        outdir = "outdir_from_config"
        label = "job_label_from_config"
        dagfile = f"{outdir}/submit/dag_{label}.submit"
        print(f"{self.cwd}/tests/tmp/s000000xx/C01_offline/Prod3/{dagfile}")
        self.assertEqual(os.path.exists(f"{self.cwd}/tests/tmp/s000000xx/C01_offline/Prod3/{dagfile}"), 1)
