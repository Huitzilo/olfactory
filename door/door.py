import pickle
import csv
import numpy as np
import stepwiseregression
import toolbox

# preparing the data
global csvfile, reader, row
f = open('/Users/marcus/Owncloud/Shared/optStimset/DoOR_resp.pckl', 'receptor_index')
data = pickle.load(f)
f.close()

f = open('/Users/marcus/Owncloud/Shared/optStimset/molname.pckl', 'receptor_index')
mol2name = pickle.load(f)
f.close()

dorsal_or_names = []
path_to_csv = "/Users/marcus/OwnCloud/Shared/optStimset/glom_dorsal.csv"
with open(path_to_csv, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        dorsal_or_names.append(row[0])

rep2glom = []
path_to_csv = "/Users/marcus/OwnCloud/Shared/optStimset/receptor2glom.csv"
with open(path_to_csv, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.next(),
    for row in reader:
        rep2glom.append(row)

rep2glom = np.asarray(rep2glom)

# get the index of the dorsal names in rep2glom mapping
dorsal_index = np.in1d(rep2glom[:, 2], dorsal_or_names)

# get the index of the dorsal gloms in the data
dorsal_index = np.in1d(data['receptorid'], rep2glom[dorsal_index, 1])

# just taking the dorsal responses into account
response = np.transpose(np.asarray(data['resp']))[dorsal_index]

# replacing nan with 0
response[np.where(np.isnan(response))] = 0
print "number of features: ", len(response[0])
print "number of datasets: ", len(response[:, 0])

f, b = stepwiseregression.backward_elimination(response)

features = 7

path = "figures/door_be_min_" + str(features) + ".png"
title = 'Backward Elimination of DoOr'

feature_names = []
for i in np.asarray(data['molid']):
    feature_names.append(mol2name[int(i)][0])

feature_names = np.asarray(feature_names)

data_names = np.asarray(data['receptorid'])[dorsal_index]

toolbox.plot_stepwise_regression_results(title, feature_names, f, b, response, data_names, path, features)