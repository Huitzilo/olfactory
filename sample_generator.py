#!/usr/bin/env python
# encoding: utf-8


import numpy as np
from numpy.random import normal
from hallem.data import Hallem

hallem = Hallem()
data = np.transpose(hallem.get_activation_matrix())


def generate_samples(samples=100, noise=10):
    """
    Generates a number of labeled samples. Samples are based on Hallem data to which noise is added.

    Parameters
    ----------
    samples:    int
                Number of samples to generate. default=100
    noise:      float
                Noise level that will be added to real data. Noise is generated with normal distribution.
                Normally one should use the standard deviation as a level for noise. default=10.

    Returns
    -------
    big_matrix: numpy.array
                A matrix containing the generated data.
    labels:     list
                A list containing the labels for the generated data. Can be used for training in machine learning algorithms.

    """
    big_matrix = []

    size = data.shape[1]

    labels = []

    for i, glomeruli in enumerate(data):
        for j in range(samples):
            v = normal(0, noise, size)
            big_matrix.append(v + glomeruli)
            labels.append(i)

    big_matrix = np.asarray(big_matrix)
    return big_matrix, labels