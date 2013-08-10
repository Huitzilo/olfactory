#!/usr/bin/env python
# encoding: utf-8
"""
Implementation of feature selection methods backward elimination or forward selection.
"""
import numpy as np
from scipy.spatial import distance


def findBestValue(distanceMatrix, k=0):
    '''
        Returns the k-th minimal value of a given distance matrix.

        Parameters
        ----------
        distanceMatrix: numpy.array
                        Distance

        k:              int
                        specifies, which minimum should be returned.
                        if k=0, then its the real minimum.
                        if k=1, its, the second smallest value
                        etc.

    '''
    return np.sort(distanceMatrix)[k]


def compute_distance_matrix(matrix, metric='euclidean', noise_threshold=None):
    '''
        Computes the pairwise distance matrix between each row of the input matrix.

        Parameters
        ----------
        matrix: numpy.array
                input matrix

        metric: string
                possible values 'euclidean', 'noisy'
                'noisy': computes the pairwise euclidean distance but whenever a elemental value is below the threshold,
                 it is set to zero
    '''
    if metric == 'noisy':

        m, n = matrix.shape

        distance_matrix = np.zeros(m * (m - 1) / 2, )
        if noise_threshold == None:
            print "Error: Provide a noise threshold"

        counter = 0

        #for each pairwise combination, e.g. row-wise)
        for i in range(0, m - 1):
            for j in range(i + 1, m):
                # substract row j from row i
                v = matrix[i] - matrix[j]

                # set all values below the threshold to zero
                v[abs(v) < noise_threshold] = 0.

                # compute euclidean distance of v
                distance_matrix[counter] = float(np.sqrt((v ** 2).sum()))
                counter += 1

        return distance_matrix
    else:
        return distance.pdist(matrix, metric)


def backward_elimination(data, distance_measure='euclidean'):
    """
    Performs a backward elimination on the given data.


    Parameters
    ----------
    data:               numpy.array
                        a matrix consisting solely of digits
    distance_measure:   string
                        possible values 'euclidean', 'manhattan', 'noisy'

    Returns
    -------
    f : list
        A list of the indices in the order they where removed from the feature set.
    br : list
        A list of the optimal values after a feature was removed.
    """
    columns = len(data[0])

    f = []
    b = range(columns)
    br = []

    # find the first feature to remove
    dm = compute_distance_matrix(data, distance_measure)
    local_min = findBestValue(dm)
    br.append(local_min)

    # repeat until every column is taken into account
    while len(b) > 0:
        maximum = -100
        index = -1


        # iterate over all odorants
        for odor in range(0, columns):
            if odor in b:
                ff = list(b)
                ff.remove(odor)

                # take just the columns f from the whole data and compute the distance matrix
                dm = compute_distance_matrix(data[:, ff], distance_measure)
                local_min = findBestValue(dm)

                if local_min > maximum:
                    maximum = local_min
                    index = odor

        f.append(index)
        b.remove(index)

        br.append(maximum)
    return f, br


def forward_selection(data, distance_measure='euclidean'):
    """
    Performs a forward selection on the given data.

    Parameters
    ----------
    data:               numpy.array
                        a matrix consisting solely of digits
    distance_measure:   str
                        possible values 'euclidean', 'manhattan',

    Returns
    -------
    f : list
        A list of the indices in the order they where added to the feature set.
    fr : list
        A list of the optimal values after a feature was included.
    """
    f = []
    fr = [0, 0] #because no features or one feature will have no distance ;)
    columns = len(data[0])

    #
    # find initial best tuple
    #
    max_value = -1
    index = -1

    # iterate over all glomeruli
    for i in range(0, columns):
        for j in range(i, columns):
            ff = list([i])
            ff.append(j)
            # take just the columns ff from the whole data and compute the distance matrix
            dm = compute_distance_matrix(data[:, ff], distance_measure)
            min_value = findBestValue(dm)

            if min_value > max_value:
                max_value = min_value
                index = (i, j)

    f.append(index[0])
    f.append(index[1])
    fr.append(max_value)

    # repeat until every column is taken into account
    while len(f) < columns:
        max_value = -1
        index = -1
        for i in range(0, columns):
            if i not in f:
                ff = list(f)
                ff.append(i)

                dm = compute_distance_matrix(data[:, ff], distance_measure)
                min_value = findBestValue(dm)

                if min_value > max_value:
                    max_value = min_value
                    index = i
        f.append(index)
        fr.append(max_value)

    return f, fr