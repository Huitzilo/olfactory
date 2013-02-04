#!/usr/bin/env python
# encoding: utf-8
"""

Naive implementation of backward elimination.
Progress of optimization criteria is plotted.
Based on that a dendrogram and a fingerprint is plotted.

Distance measure can be changed.
"""
from numpy.core.multiarray import arange
import pylab as pl
import numpy as np
from scipy.spatial import distance
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram

from data import Hallem


hallem = Hallem()

data = np.transpose(hallem.get_activation_matrix()) # Glomeruli x Odorants instead of Odorants x Glomeruli
columns = len(data[0])

pl.close()


def findBestValue(distanceMatrix):
    return np.min(distanceMatrix)


f_list = []
b_list = range(columns)

backward_result = []
distance_measure = 'euclidean'

dm = distance.pdist(data, distance_measure)
min_value = findBestValue(dm)
backward_result.append(min_value)

features = 3


## backward elimination



# repeat until every column is taken into account
while len(b_list) > 0:
    minimum = -1
    index = -1

    # iterate over all odorant
    for odor in range(0, columns):
        if odor in b_list:
            f = list(b_list)
            f.remove(odor)

            # take just the columns f from the whole data and compute the distance matrix
            dm = distance.pdist(data[:, f], distance_measure)
            min_value = findBestValue(dm)

            if min_value > minimum:
                minimum = min_value
                index = odor
    f_list.append(index)
    b_list.remove(index)
    backward_result.append(minimum)

print "Odorant list in sorted order in which they were removed from the dataset"
print hallem.odorant_list[f_list[-features:]]

fig = pl.figure(figsize=(23, 8), facecolor='w', edgecolor='k')
fig.autofmt_xdate()
pl.title("Backward Elimination")
pl.subplot(141)
pl.plot(range(0, len(backward_result)), backward_result[::-1])
pl.xlabel("#features")
pl.ylabel("min-min euclidean distance")
pl.title("progressing Euclidean Distance")

pl.subplot(142)
p = data[:, f_list[-features:]]
pl.xlabel("Euclidean Distance between \nglomeruli with " + str(features) + " features")
pl.ylabel("Glomerulus")
link = linkage(distance.pdist(p, distance_measure), method="single")
dend = dendrogram(link, labels=hallem.or_list, orientation="right")
sorted_list = p[dend["leaves"]]

pl.subplot(143)
pl.pcolor(sorted_list)
pl.ylim((0, 23))
pl.xticks(arange(.5, .5 + features), hallem.odorant_list[f_list[-features:]], rotation="vertical")
pl.title("Heat Map of \nGlomeruli Activity")
pl.colorbar()

pl.subplot(144)
pl.title("Fingerprint")
for odor in range(0, len(sorted_list)):
    x = range(0, len(sorted_list[odor]))
    y = [odor] * len(sorted_list[odor])
    pl.scatter(x, y, s=sorted_list[odor], c="grey", alpha=.75)
    pl.ylim((-.5, 22.5))
    pl.xlim((-.5, features))
    pl.xticks(arange(features), hallem.odorant_list[f_list[-features:]], rotation="vertical")

#pl.show()
pl.savefig("figures/backward_" + distance_measure + "_" + str(features) + ".png")