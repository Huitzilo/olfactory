#!/usr/bin/env python
# encoding: utf-8
"""

Naive implementation of forward selection.
Progress of optimization criteria is plotted.
Based on that a dendrogram and a fingerprint is plotted.

Distance measure can be changed.

Created by  on 2012-01-27.
Copyright (c) 2012. All rights reserved.
"""
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
forward_result = []
distance_measure = 'euclidean'
features = 5


# find initial best tuple
max_value = -1
index = -1

# iterate over all glomeruli
for i in range(0, columns):
    for j in range(i, columns):
        f = list([i])
        f.append(j)
        # take just the columns f from the whole data and compute the distance matrix
        dm = distance.pdist(data[:, f], distance_measure)
        min_value = findBestValue(dm)

        if min_value > max_value:
            max_value = min_value
            index = (i, j)

f_list.append(index[0])
f_list.append(index[1])
forward_result.append(max_value)

print "Starting tuple: ", f_list, "aka", hallem.odorant_list[f_list]



## forward selection

# repeat until every column is taken into account
while len(f_list) < columns:
    max_value = -1
    index = -1
    for i in range(0, columns):
        if i not in f_list:
            f = list(f_list)
            f.append(i)
            dm = distance.pdist(data[:, f], distance_measure)
            min_value = findBestValue(dm)

            if min_value > max_value:
                max_value = min_value
                index = i
    f_list.append(index)
    forward_result.append(max_value)

print "Odorant list in sorted order"
for i in np.arange(features):
    print i, ":", hallem.odorant_list[f_list[i]]

fig = pl.figure(figsize=(23, 8), facecolor='w', edgecolor='k')
pl.title("Forward Selection")
pl.subplot(141)
pl.plot(range(0, len(forward_result)), forward_result)
pl.xlabel("#features")
pl.ylabel("max-min euclidean distance")
pl.title("progressing Euclidean Distance")

pl.subplot(142)
p = data[:, f_list[0:features]]
pl.xlabel("Euclidean Distance between \nglomeruli with " + str(features) + " features")
pl.ylabel("Glomerulus")

link = linkage(distance.pdist(p, distance_measure), method="single")
dend = dendrogram(link, labels=hallem.or_list, orientation="right")
sorted_list = p[dend["leaves"]]

pl.subplot(143)
pl.pcolor(sorted_list)
pl.ylim((0, 23))
pl.xlabel("Odorant")
pl.title("Heat Map of \nGlomeruli Activity")
pl.colorbar()

pl.subplot(144)
pl.title("Fingerprint")
for i in range(0, len(sorted_list)):
    x = range(0, len(sorted_list[i]))
    y = [i] * len(sorted_list[i])
    pl.scatter(x, y, s=sorted_list[i], c="grey", alpha=.75)
    pl.ylim((-.5, 22.5))
    pl.xlim((-.5, features))

#pl.show()
pl.savefig("figures/forward_" + distance_measure + "_" + str(features) + ".png")