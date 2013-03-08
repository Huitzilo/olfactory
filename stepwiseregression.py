#!/usr/bin/env python
# encoding: utf-8

"""
Implementation of stepwise regression methods like backward elimination or forward selection.
"""
import toolbox


def backward_elimination(data, distance_measure='euclidean'):
    """
    Performs a backward elimination based on the given data.


    Parameters
    ----------
    data:  must be a matrix consisting solely of digits

    Returns
    -------
    f : list
        A list of the indices in the order they where removed from the feature set.
    b : list
        A list of the optimal values after a feature was removed.
    """
    columns = len(data[0])

    f = []
    b = range(columns)
    br = []

    # find the first feature to remove
    dm = toolbox.compute_distance_matrix(data, distance_measure)
    local_min = toolbox.findBestValue(dm, len(data[0]), len(data[0]))
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
                dm = toolbox.compute_distance_matrix(data[:, ff], distance_measure)
                local_min = toolbox.findBestValue(dm, len(ff), len(data[0]))

                if local_min > maximum:
                    maximum = local_min
                    index = odor

        f.append(index)
        b.remove(index)
        br.append(maximum)
    return f, br