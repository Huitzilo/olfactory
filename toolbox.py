#!/usr/bin/env python
# encoding: utf-8
"""

"""
from __future__ import division
import numpy as np
from scipy.spatial import distance


def findBestValue(distanceMatrix, k=0, n=0):
    return np.min(distanceMatrix)


def compute_distance_matrix(matrix, metric='euclidean', noise_threshold=None):
    if metric == 'noisy':
        s = matrix.shape
        m, n = s
        dm = np.zeros(m * (m - 1) / 2, )
        if noise_threshold == None:
            print "Provide a noise threshold"

        counter = 0

        for i in range(0, m - 1):
            for j in range(i + 1, m):
                v = matrix[i] - matrix[j]
                v[abs(v) < noise_threshold] = 0.
                dm[counter] = float(np.sqrt((v ** 2).sum()))
                counter += 1

        return dm
    else:
        return distance.pdist(matrix, metric)