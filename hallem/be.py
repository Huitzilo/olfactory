#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with backward elimination method.
"""
import pylab as pl
import numpy as np
import stepwiseregression
from hallem.data import Hallem
import toolbox

hallem = Hallem()

data = np.transpose(hallem.get_activation_matrix()) # Glomeruli x Odorants instead of Odorants x Glomeruli

distance_measure = 'euclidean'
features = 5

feature_list, backward_result = stepwiseregression.backward_elimination(data, distance_measure)

pl.close()
print "Odorant list in sorted order in which they were removed from the dataset"
print hallem.odorant_list[feature_list[-features:]]

features = 4
path = "figures/hallem_be_min_" + str(features) + ".png"
title = 'Backward Elimination of Hallem'
feature_names = hallem.odorant_list
data_names = hallem.or_list
toolbox.plot_stepwise_regression_results(title, feature_names, feature_list, backward_result, data, data_names, path,
                                         features)