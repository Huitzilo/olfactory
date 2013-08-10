#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with backward elimination method.
"""
import numpy as np
import featureselection
from hallem.data import Hallem
import toolbox

hallem = Hallem()
data = np.transpose(hallem.response) # Glomeruli x Odorants instead of Odorants x Glomeruli

feature_names = hallem.odorant_list
data_names = hallem.or_list
features = 6

feature_list, backward_result = featureselection.backward_elimination(data)
sub_list = feature_list[:-features - 1:-1]

print "Top", str(features), "features"
print "Score:", backward_result[-features - 1]
print sub_list
print feature_names[sub_list]

title = 'Backward Elimination on Hallem with ' + str(features) + " features"

path = "figures/hallem/be/hallem_be_" + str(features) + "_performance.png"
toolbox.plot_progress_results(backward_result, features, path)

path = "figures/hallem/be/hallem_be_" + str(features) + ".png"
toolbox.plot_fingerprints(title, feature_names[sub_list], data[:, sub_list], data_names, path)