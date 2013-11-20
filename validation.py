#!/usr/bin/env python
# encoding: utf-8
"""
    This script should allow you to cross check the results you get from gurobi, be or whatsoever.
    Since we have no test set, like in many machine learning tasks, we generate one from the original data.
    For each glomerulus spectrum we create 100 noisy samples and try to reverse classify them according to the glomerulus they are based on.
    For different levels of noise, the accuracy of prediction is measured, e.g. how many labels could be predicted correctly.
"""
import toydata
import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.colors

cdict = {'red': ((0.0, 1.0, 1.0),
                 (0.97, .5, .5),
                 (1.0, .0, .3)),
         'green': ((0.0, 1.0, 1.0),
                   (0.97, .5, .5),
                   (1.0, .5, .3)),
         'blue': ((0.0, 1.0, 1.0),
                  (0.97, .5, .5),
                  (1.0, .0, .3))}
cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap', cdict, 256)


def validate(data, features, noise=range(0, 50, 10), sample_size=100):
    """
    Parameters
    ----------
    features:   numpy.ndarray
                A list of feature lists. Normally with increasing size
    noise:      numpy.ndarray
                Different levels of noise which should be added.

    Returns
    -------
    results:    numpy.ndarray
                Matrix of the
    """

    results = []

    for sub in features:

        a = []

        for sd in noise:
            output = []

            # generate the samples and their classes
            samples, labels = toydata.generate_noise_samples(data, samples=sample_size, noise=sd)

            for sample in samples:
                label = -1

                sd = np.vstack([sample[:, sub], data[:, sub]])
                mm = pdist(sd)
                output.append(np.argmin(mm[:len(data)]))

            output = np.asarray(output)
            accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
            a.append(accuracy)
        results.append(a)

    results = np.asarray(results)

    return results