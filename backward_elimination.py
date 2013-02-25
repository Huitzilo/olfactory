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
from sklearn.decomposition import PCA

from data import Hallem
import toolbox


hallem = Hallem()

#data = hallem.get_activation_matrix()
data = np.transpose(hallem.get_activation_matrix()) # Glomeruli x Odorants instead of Odorants x Glomeruli
x = PCA()
x.fit(data)

data = np.dot(x.components_[0:5], np.transpose(data)) # PCA reduction

columns = len(data[0])

pl.close()

f_list = []
b_list = range(columns)

backward_result = []
distance_measure = 'euclidean'
# distance_measure = 'noisy'
noise_threshold = 20
features = 5

dm = toolbox.compute_distance_matrix(data, distance_measure, noise_threshold)
local_min = toolbox.findBestValue(dm, len(data[0]), len(data[0]))
backward_result.append(local_min)

additional = ''
if distance_measure == 'noisy':
    additional = "_" + str(noise_threshold)

## backward elimination
# repeat until every column is taken into account
while len(b_list) > 0:
    maximum = -100
    index = -1

    # iterate over all odorants
    for odor in range(0, columns):
        if odor in b_list:
            f = list(b_list)
            f.remove(odor)

            # take just the columns f from the whole data and compute the distance matrix
            dm = toolbox.compute_distance_matrix(data[:, f], distance_measure, noise_threshold)
            local_min = toolbox.findBestValue(dm, len(f), len(data[0]))

            if local_min > maximum:
                maximum = local_min
                index = odor

    f_list.append(index)
    b_list.remove(index)
    backward_result.append(maximum)

print "Odorant list in sorted order in which they were removed from the dataset"
print hallem.odorant_list[f_list[-features:]]


#max_at = np.where(backward_result, np.max(backward_result))
fig = pl.figure(figsize=(23, 8), facecolor='w', edgecolor='k')
fig.autofmt_xdate()
pl.suptitle('Backward elimination with ' + str(features) + " features")
pl.title("Backward Elimination")
pl.subplot(141)
pl.plot(range(0, len(backward_result)), backward_result[::-1])
#pl.plot(max_at, backward_result[max_at],'rs')
pl.xlabel("#features")
pl.ylabel("max-min euclidean distance")
title = "progressing Euclidean Distance " + additional
pl.title(title)

pl.subplot(142)
data = np.transpose(hallem.get_activation_matrix()) # Glomeruli x Odorants instead of Odorants x Glomeruli
sub_list = f_list[:-features - 1:-1]
p = data[:, sub_list]
pl.xlabel("Euclidean Distance between \nglomeruli with " + str(features) + " features")
pl.ylabel("Glomerulus")
link = linkage(distance.pdist(p, 'euclidean'), method="single")
dend = dendrogram(link, labels=hallem.or_list, orientation="right")
sorted_list = p[dend["leaves"]]

print link
print "min", np.min(link[:, 2]), "max", np.max(link[:, 2])
print "mean", np.mean(link[:, 2]), "std", np.std(link[:, 2])

#print dend

pl.subplot(143)
pl.pcolor(sorted_list)
pl.ylim((0, 23))
pl.xticks(arange(.5, .5 + features), hallem.odorant_list[sub_list], rotation="vertical")
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
    pl.xticks(arange(features), hallem.odorant_list[sub_list], rotation="vertical")

#pl.show()

pl.savefig("figures/backward_pca_" + distance_measure + "_" + str(features) + additional + ".png")
