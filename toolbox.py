#!/usr/bin/env python
# encoding: utf-8
"""
    Plotting the results of subset predictions.
"""
from __future__ import division
import numpy as np
import pylab as pl
from scipy.spatial import distance
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from pylab import *


def create_cmap(minimum, maximum):
    zero = abs(float(minimum) / (maximum - minimum))

    if minimum < 0:
        cdict = {'red': ((0.0, 1.0, 1.0),
                         (zero, 1.0, 1.0),
                         (1.0, .0, 1.0)),
                 'green': ((.0, .0, .0),
                           (zero, 1.0, 1.0),
                           (1.0, .0, .0)),
                 'blue': ((0.0, 0.0, 0.0),
                          (zero, 1.0, 1.0),
                          (1.0, 1.0, 1.0))}
    else:
        cdict = {'red': ((0.0, 1.0, 1.0),
                         (minimum, 1.0, 1.0),
                         (1.0, .0, 1.0)),
                 'green': ((.0, 1.0, 1.0),
                           (minimum, 1.0, 1.0),
                           (1.0, .0, .0)),
                 'blue': ((0.0, 1.0, 1.0),
                          (minimum, 1.0, 1.0),
                          (1.0, 1.0, 1.0))}
    return matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)


def plot_progress_results(result, features, path, plot_hline=True):
    fig = pl.figure(figsize=(9, 6), dpi=300, facecolor='w', edgecolor='k')
    fig.autofmt_xdate()
    x_coord = features

    pl.plot(range(0, len(result)), result[::-1])
    if plot_hline:
        pl.axvline(x_coord, color='r')
    pl.xlabel("#features")
    pl.xticks([0, features, len(result)])
    pl.ylabel("max-min euclidean distance")
    pl.savefig(path)


def plot_fingerprints(title, feature_names, data, data_names, path, xlabel="spikes/s"):
    features = len(feature_names)

    fig = pl.figure(figsize=(18, 12), dpi=300, facecolor='w', edgecolor='k')
    fig.autofmt_xdate()

    # plotting dendrogram of eucledean distance between glomeruli
    pl.suptitle(title)
    pl.subplot(121)
    p = data
    pl.xlabel("Distance in " + xlabel)
    pl.ylabel("OR")
    link = linkage(distance.pdist(p, 'euclidean'), method="single")
    dend = dendrogram(link, labels=data_names, orientation="right", color_threshold=1)
    sorted_list = p[dend["leaves"]]
    pl.grid()

    pl.subplot(122)
    cmap = create_cmap(np.min(sorted_list), np.max(sorted_list))
    pl.imshow(sorted_list[::-1], cmap=cmap, vmin=np.min(sorted_list), vmax=np.max(sorted_list), interpolation="None",
              aspect="auto")

    pl.xticks(np.arange(0.5, .5 + features), feature_names, rotation="30", ha='right', fontsize=10)
    pl.yticks([])
    cb = pl.colorbar()
    cb.set_label(xlabel)
    pl.grid(which="major")
    pl.savefig(path)
