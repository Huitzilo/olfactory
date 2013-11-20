"""
Created on Mar 28, 2012

@author: jan
"""
import numpy as np
from scipy.stats import norm, gamma
from scipy.spatial.distance import squareform
from hallem.data import Hallem
from numpy.random import normal


def correlated_samples(cov, num_sampl, marginal_dist):
    """ create correlated samples with a gaussian copula """

    # Create Gaussian Copula
    dependence = np.random.multivariate_normal([0] * cov.shape[0], cov, num_sampl)
    dependence_dist = norm()
    uniform_dependence = dependence_dist.cdf(dependence)

    #Transform marginals 
    dependend_samples = marginal_dist.ppf(uniform_dependence)
    return dependend_samples


def group_covmtx(rho_intra, rho_inter, num_groups, num_objects):
    """ create a covarince matrix with groups
    
    in each group are num_objects with a covariance of rho_intra. 
    objects between groups have a covariance of rho_intra 
    """

    intra_mtx_size = (num_objects ** 2 - num_objects) / 2
    intra_cov = 1 - squareform([1 - rho_intra] * intra_mtx_size)

    cov = rho_inter * np.ones((num_groups * num_objects, num_groups * num_objects))
    for group_num in range(num_groups):
        #print group_num * num_objects, (group_num + 1) * num_objects
        cov[group_num * num_objects:(group_num + 1) * num_objects,
        group_num * num_objects:(group_num + 1) * num_objects] = intra_cov
    return cov, locals()


def adjusted_gamma(mean, var):
    scale = var / mean
    shape = mean / scale
    if shape > 1:
        print '!!! Warning !!! - shape parameter: ', str(shape)
    return gamma(shape, scale=scale)


def generate_noise_samples(data, samples=100, noise=10):
    """
    Generates a given number of labeled samples. Samples are based on data to which noise is added.

    Parameters
    ----------
    data:       numpy.array
                Data matrix.
    samples:    int
                (default=100) Number of samples to generate.
    noise:      float
                (default = 10) Noise level that will be added to real data. Noise is generated with normal distribution.
                Normally one should use the standard deviation as a level for noise.

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
            if noise != 0:
                v = normal(0, noise, size)
            else:
                v = 0
            big_matrix.append(v + glomeruli)
            labels.append(i)

    big_matrix = np.asarray(big_matrix)
    return big_matrix, labels


def generate_random_data(data, features):
    return np.random.randint(0, 200, (data, features))