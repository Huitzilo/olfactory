#!/usr/bin/env python
# encoding: utf-8
"""

"""
import numpy as np
from scipy.spatial import distance


def findBestValue(distanceMatrix):
    return np.min(distanceMatrix)


def compute_distance_matrix(matrix, metric='euclidean', noise_threshold=None):
    if metric == 'noisy':
        s = matrix.shape
        m, n = s
        dm = np.zeros(m * (m - 1) / 2, )
        if noise_threshold == None:
            print "Provide a noise threshold"

        counter = 0
        for i, vectorX in enumerate(matrix):
            for j, vectorY in enumerate(matrix):
                if j > i:
                    v = vectorX - vectorY
                    v[np.where(abs(v) < noise_threshold)] = 0.
                    dm[counter] = float(np.sqrt((v ** 2).sum()))
                    counter = counter + 1
        return dm
    else:
        return distance.pdist(matrix, metric)