#!/usr/bin/env python
# encoding: utf-8
'''
Backward Elimination on dorsal subset of DoOR data.
'''
from door.data import DoOR
import featureselection
import toolbox

door = DoOR()

data, ors, odorants = door.get_dorsal_data()

features = 15
feature_list, backward_result = featureselection.backward_elimination(data)
sub_list = feature_list[:-features - 1:-1]

print "Top", str(features), "features"
print "Score:", backward_result[-features - 1]
print sub_list
print odorants[sub_list]

title = 'Backward Elimination of DoOr with %i features' % (features)
path = "../figures/door/be/door_be_progress.png"
toolbox.plot_progress_results(backward_result, features, path)
path = "../figures/door/be/door_be_min_" + str(features) + ".png"
toolbox.plot_fingerprints(title, odorants[sub_list], data[:, sub_list], ors, path, "door units")
