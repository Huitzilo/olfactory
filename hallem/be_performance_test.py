"""
Measuring running time of BE
"""
import numpy as np
import featureselection
import time
import csv


def load_toydata_file(samples=5, features=100):
    path_to_csv = "toydata/" + str(samples) + "_" + str(features) + ".csv"
    data = []
    with open(path_to_csv) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:
            data.append(row)

    return np.asarray(data, dtype=float)


be_times = []
be_scores = []

for i in range(0, 5):

    be_scores_v = []
    be_times_v = []

    for j in range(0, 5):
        samples = 10 * (2 ** i)
        features = 10 * (2 ** j)

        print samples, features

        score_pos = features / 10

        data = load_toydata_file(samples, features)
        start = time.time()
        feature_list, backward_result = featureselection.backward_elimination(data)
        stop = time.time()

        be_times_v.append(stop - start)
        be_scores_v.append(backward_result[-score_pos])


        #print "\n", stop - start, "sec"
    be_times.append(be_times_v)
    be_scores.append(be_scores_v)

be_times = np.asarray(be_times)
be_scores = np.asarray(be_scores)
# print data.shape
np.savetxt("be_perforrmance_times.csv", be_times, delimiter=",")
np.savetxt("be_perforrmance_scores.csv", be_scores, delimiter=",")
