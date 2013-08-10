#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with forward selection method.
"""
import numpy as np

import toolbox
import featureselection
from hallem.data import Hallem

hallem = Hallem()

data = np.transpose(hallem.response) # Glomeruli x Odorants instead of Odorants x Glomeruli

distance_measure = 'euclidean'
features = 5

f_list, forward_result = featureselection.forward_selection(data, distance_measure)

feature_names = hallem.odorant_list
data_names = hallem.or_list
sub_list = f_list[:features]

print "Top", str(features), "features"
print "Score:", forward_result[features]
print sub_list
print feature_names[sub_list]

title = 'Forward Selection of Hallem'
path = "figures/hallem/fs/hallem_fs_" + str(features) + "_performance.png"
toolbox.plot_progress_results(forward_result[::-1], features, path)

path = "figures/hallem/fs/hallem_fs_" + str(features) + ".png"
toolbox.plot_fingerprints(title, feature_names[sub_list], data[:, sub_list], data_names, path)