#!/usr/bin/env python
# encoding: utf-8
"""
Analysis of stability backward elimination method.
What happens when one of the features is removed before the feature selection.
"""
import numpy as np
import featureselection
from hallem.data import Hallem
import toolbox

hallem = Hallem()

rr = []

top = np.asarray([6, 44, 0, 7, 91])
top_features = np.sort(hallem.odorant_list[top])
for i in np.delete(range(0, 110), top):

    print i

    data = np.transpose(hallem.response) # Glomeruli x Odorants instead of Odorants x Glomeruli

    feature_names = hallem.odorant_list
    data_names = hallem.or_list

    x = feature_names[i]
    f = np.delete(range(0, len(feature_names)), i)
    data = data[:, f]
    feature_names = feature_names[f]

    features = len(top)

    feature_list, backward_result = featureselection.backward_elimination(data)

    current_features = np.sort(feature_names[feature_list[-features:]])

    # if the predicted set is different from the reference set...
    if not np.all(current_features == top_features):
        print x
        rr.append(i)

        title = 'Removed ' + x

        path = "figures/distorted/hallem_be_distorted_" + str(backward_result[-features - 1]) + "_" + x + "_" + str(
            features) + ".png"
        toolbox.plot_fingerprints(title, feature_names, data, data_names, path)

print rr
print hallem.odorant_list[rr]