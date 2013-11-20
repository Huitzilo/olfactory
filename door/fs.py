#!/usr/bin/env python
# encoding: utf-8
"""
Forward Selection on dorsal subset of DoOR data.
"""
from door.data import DoOR
import featureselection
import toolbox

door = DoOR()

data, ors, odorants = door.get_dorsal_data()

features = 10
feature_list, forward_results = featureselection.forward_selection(data)
sub_list = feature_list[:features]

print forward_results
for i in range(20):
    print forward_results[i]

print "Top", str(features), "features"
print "Score:", forward_results[-features - 1]
print feature_list
print sub_list
print odorants[sub_list]

xxx = forward_results[-features - 1:]
for i in xxx[::-1]:
    print str(i).replace(".", ",")



# title = 'Backward Elimination of DoOr with %i features' % (features)
# path = "../figures/door/be/door_be_progress.png"
# toolbox.plot_progress_results(forward_results, features, path)
# path = "../figures/door/be/door_be_min_" + str(features) + ".png"
# toolbox.plot_fingerprints(title, odorants[sub_list], data[:, sub_list], ors, path, "DoOR units")
