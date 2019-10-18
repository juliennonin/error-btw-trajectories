"""
Module Docstring
"""

import unittest
import os
from unittest.mock import patch  # prevent ploting figures
import trajectories_error.estimator as estimator

def fetch_test_data(dirname, contains_solution=True, criterion='.txt',
                    sep=',', samples=slice(0, None)):
    """
    >>> fetch_test_data("shared-oracles/Oracles/CorrectInputTrajectories/")[0][1:]
    [Trajectory([Point(1.0, 1.0), Point(3.0, 1.0)]), \
Trajectory([Point(1.0, 2.0), Point(3.0, 2.0)]), 1.0, 0.001]
    >>> fetch_test_data("shared-oracles/Oracles/IncorrectInputTrajectories/", False)[2][1:]
    [Trajectory([Point(0.0, 0.0), Point(1.0, 0.0)]), Trajectory([])]
    >>> fetch_test_data("shared-oracles/Oracles/IncorrectInputTrajectories/", False)[1][1:]
    [Trajectory([Point(0.0, 1.0)]), Trajectory([])]
    """
    current_dir = os.path.dirname(__file__)
    dirname = filename = os.path.join(current_dir, dirname)
    test_file_names = [filename for filename in os.listdir(
        dirname) if criterion in filename]
    tests_sample = []
    for filename in sorted(test_file_names)[samples]:
        tests_sample.append(estimator.fetch_data(
            dirname + filename, contains_solution=contains_solution, sep=sep))
    return tests_sample


class TestEstimator(unittest.TestCase):
    """[TODO] : Docstring"""

    @patch('matplotlib.pyplot.figure')
    def test_incorrect_input(self, mock_show):
        """ Docstring """
        dirname = "shared-oracles/Oracles/IncorrectInputTrajectories/"
        for _, reference, acquired in fetch_test_data(dirname, contains_solution=False):
            with self.assertRaises(AssertionError):
                reference.error_with(acquired)

    @patch('matplotlib.pyplot.figure')
    def test_correct_input(self, mock_show):
        """ Docstring """
        dirname = "shared-oracles/Oracles/CorrectInputTrajectories/"
        for filename, reference, acquired, expected_output, epsilon \
                in fetch_test_data(dirname):
            output = reference.error_with(acquired)

            with self.subTest(test=filename, output=output, expected_output=expected_output):
                self.assertLessEqual(abs(expected_output - output), epsilon)

    @patch('matplotlib.pyplot.figure')
    def test_samples(self, mock_show):
        """ Docstring """
        dirname = "shared-oracles/Oracles/SampleTrajectories/"
        for filename, reference, acquired, expected_output, epsilon \
                in fetch_test_data(dirname):
            output = reference.error_with(acquired)

            with self.subTest(test=filename, output=output, expected_output=expected_output):
                self.assertLessEqual(abs(expected_output - output), epsilon)

    @patch('matplotlib.pyplot.figure')
    def test_perso_samples(self, mock_show):
        """ Docstring """
        dirname = "perso-tests/"
        for filename, reference, acquired, expected_output, epsilon \
                in fetch_test_data(dirname):
            output = reference.error_with(acquired)

            with self.subTest(test=filename, output=output, expected_output=expected_output):
                self.assertLessEqual(abs(expected_output - output), epsilon)
