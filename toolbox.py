#!/usr/bin/env python
# encoding: utf-8
"""

"""
from __future__ import division
import numpy as np
import pylab as pl
from scipy.spatial import distance
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram


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


def plot_stepwise_regression_results(title, feature_names, feature_list, result, data, data_names, path, features=5):
    # plotting the progress of the euclidean distance
    fig = pl.figure(figsize=(23, 8), facecolor='w', edgecolor='k')
    fig.autofmt_xdate()
    pl.suptitle(title + ' with ' + str(features) + " features")
    pl.title(title)
    pl.subplot(141)
    pl.plot(range(0, len(result)), result[::-1])
    pl.xlabel("#features")
    pl.ylabel("max-min euclidean distance")
    title = "progressing Euclidean Distance"
    pl.title(title)

    # plotting dendrogram of eucledean distance between glomeruli
    pl.subplot(142)
    sub_list = feature_list[:-features - 1:-1]
    p = data[:, sub_list]
    pl.xlabel("Euclidean Distance between \nglomeruli with " + str(features) + " features")
    pl.ylabel("Glomerulus")
    link = linkage(distance.pdist(p, 'euclidean'), method="single")
    dend = dendrogram(link, labels=data_names, orientation="right")
    sorted_list = p[dend["leaves"]]

    #print dendrogram
    pl.subplot(143)
    pl.pcolor(sorted_list)
    pl.ylim((0, 23))
    feature_list = np.asarray(feature_list)
    pl.xticks(np.arange(.5, .5 + features), feature_names[sub_list], rotation="vertical")
    pl.title("Heat Map of \nGlomeruli Activity")
    pl.colorbar()

    pl.subplot(144)
    pl.title("Fingerprint")
    for odor in range(0, len(sorted_list)):
        x = range(0, len(sorted_list[odor]))
        y = [odor] * len(sorted_list[odor])
        values = sorted_list[odor]
        pl.scatter(x, y, s=values, c="green", alpha=.75)
        pl.scatter(x, y, s=values * -1, c="red", alpha=1)

        pl.ylim((-.5, 22.5))
        pl.xlim((-.5, features))
        pl.xticks(np.arange(features), feature_list[sub_list], rotation="vertical")

    print '....', path
    pl.savefig(path)

