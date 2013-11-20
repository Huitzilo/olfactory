#!/usr/bin/env python
# encoding: utf-8
"""
Backward Elimination on dorsal subset of DoOR data.
"""
from door.data import DoOR
import featureselection
import toolbox
import numpy as np

door = DoOR()

data, ors, odorants = door.get_dorsal_data()


#print door.response.shape
#
#or1 = np.where(ors == "Or46a")[0][0]
#test = data[or1]
#sorting = np.argsort(data[or1])
#for i,v in enumerate((data[or1])[sorting]):
#    print (odorants[sorting])[i], "  -  ", v



## Reference
#or2 = np.where(door.or_names == "Or46a")[0][0]
#ref = door.response[or2]
#
#print ref - test
#sorting = np.argsort(door.response[or1])
#for i, v in enumerate((door.response[or1])[sorting]):
#    print (door.odorant_names[sorting])[i], "  -  ", v


#print odorants
#or1 = np.where(door.odorant_names == "Ethyl (R)-3-hydroxybutyrate")[0][0]
#
#sorting = np.argsort(door.or_names)
#print len(sorting)
#for i,v in enumerate((door.response[:, or1])[sorting]):
#    print (door.or_names[sorting])[i], "  -  ", v


features = 6
feature_list, backward_result = featureselection.backward_elimination(data)
print backward_result
sub_list = feature_list[:-features - 1:-1]

print "Top", str(features), "features"
print "Score:", backward_result[-features - 1]
print sub_list
print odorants[sub_list]

title = 'Backward Elimination of DoOr with %i features' % (features)
path = "../figures/door/be/door_be_progress.png"
toolbox.plot_progress_results(backward_result, features, path)
path = "../figures/door/be/door_be_min_" + str(features) + ".png"
toolbox.plot_fingerprints(title, odorants[sub_list], data[:, sub_list], ors, path, "DoOR units")

#np.savetxt("../results/be_features_door.csv", backward_result[::-1], delimiter=";")
