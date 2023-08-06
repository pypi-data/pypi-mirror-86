import unittest
import os

test_rootpath = os.path.dirname(os.path.abspath(__file__))

from r3d3.experiment_launcher import main


class TestExperimentLauncher(unittest.TestCase):
    def test_main(self):
        launcher = main(
            f"{test_rootpath}/samples/sample_experiment.py",
            debug=False,
            forward_nb_processes=False,
        )
        self.assertEqual(launcher.db.get_nb_experiments(), 4)

    def test_multiple_plans(self):
        launcher = main(
            f"{test_rootpath}/samples/sample_experiment_2.py",
            debug=False,
            forward_nb_processes=False,
        )
        self.assertEqual(launcher.db.get_nb_experiments(), 8)

    def test_failure(self):
        launcher = main(
            f"{test_rootpath}/samples/sample_experiment_failing.py",
            debug=False,
            forward_nb_processes=False,
        )
        self.assertEqual(launcher.db.get_nb_experiments(), 1)
