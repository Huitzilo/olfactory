#!/usr/bin/env python
# encoding: utf-8
"""

"""
import unittest

import numpy as np

import toolbox



#test compute distance matrix 'noisy'


class TestSequenceFunction(unittest.TestCase):
    def setUp(self):
        self.seq = range(10)

    def test_computation_noisy_distance(self):
        # 2 x 2 matrix
        matrix = np.asarray([[0., 4.],
                             [1., 0.]])

        dm = toolbox.compute_distance_matrix(matrix, 'noisy', 4)
        real = np.asarray([4.])
        self.assertTrue((dm == real).all())

        # 3 x 2 matrix
        matrix = np.asarray([[0., 4.],
                             [4., 4.],
                             [4., 0.]])

        dm = toolbox.compute_distance_matrix(matrix, 'noisy', 4)
        real = np.asarray([4., np.sqrt(32), 4])
        self.assertTrue((dm == real).all())


if __name__ == '__main__':
    unittest.main()
