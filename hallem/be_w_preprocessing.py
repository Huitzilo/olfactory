#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of Hallem data with backward elimination method.
"""
import numpy as np
import featureselection
from hallem.data import Hallem
import toolbox
import scipy as sp
from scipy import stats

hallem = Hallem()
data = hallem.response

feature_names = hallem.odorant_list
data_names = hallem.or_list
features = 25

removables = []
for i, rowA in enumerate(data):
    for j, rowB in enumerate(data):
        if j > i:
            c = sp.stats.pearsonr(rowA, rowB)[0]
            if c > 0.92:

                if np.std(rowA) > np.std(rowB):
                    removables.append(j)
                else:
                    removables.append(i)

print "removed (", len(removables), "):", removables
data = np.delete(data, removables, axis=0)
feature_names = np.delete(feature_names, removables)

data = np.transpose(data)

feature_list, backward_result = featureselection.backward_elimination(data)
sub_list = feature_list[:-features - 1:-1]

print str(np.sum(backward_result[-features - 1:])).replace(".", ",")
for i in backward_result[-features - 1:-2][::-1]:
    print str(i).replace(".", ",")

print "Top", str(features), "features"
print "Score:", backward_result[-features - 1]
print sub_list
print feature_names[sub_list]

title = 'Backward Elimination with preprocessing of Hallem with' + str(features) + " features"
path = "../figures/hallem/be/hallem_be_" + str(features) + "_performance_preprocessing.png"
toolbox.plot_progress_results(backward_result, features, path=path)
path = "../figures/hallem/be/hallem_be_" + str(features) + "_preprocessing.png"
toolbox.plot_fingerprints(title, feature_names[sub_list], data[:, sub_list], data_names, path)