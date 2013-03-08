import pickle
import csv
import numpy as np
import stepwiseregression
import toolbox

# preparing the data
global csvfile, reader, row
f = open('/Users/marcus/Owncloud/Shared/optStimset/DoOR_resp.pckl', 'r')
data = pickle.load(f)
f.close()

dorsal = []
path_to_csv = "/Users/marcus/OwnCloud/Shared/optStimset/glom_dorsal.csv"
with open(path_to_csv, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        dorsal.append(row[0])

rep2glom = []
path_to_csv = "/Users/marcus/OwnCloud/Shared/optStimset/receptor2glom.csv"
with open(path_to_csv, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.next(),
    for row in reader:
        rep2glom.append(row)

rep2glom = np.asarray(rep2glom)

dorsal_index = np.in1d(rep2glom[:, 2], dorsal)
receptorid_ = data['receptorid']
r = np.in1d(receptorid_, rep2glom[dorsal_index, 1])

response = np.asarray(data['resp'])[r]

# replacing nan with 0
response[np.where(np.isnan(response))] = 0

print "number of features: ", len(response[0])
print "number of datasets: ", len(response[:, 0])

f, b = stepwiseregression.backward_elimination(response)

features = 5
path = "figures/door_be_" + str(features) + ".png"
title = 'Backward Elimination of DoOr'
feature_names = np.asarray(data['molid'])[f]
data_names = np.asarray(data['receptorid'])[r]

toolbox.plot_stepwise_regression_results(title, feature_names, f, b, response, data_names, path, features)