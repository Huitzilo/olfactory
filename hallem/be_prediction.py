#!/usr/bin/env python
# encoding: utf-8
#
'''
Analysis of stability of backward prediction.

Since we have no test set, like in many machine learning tasks, we generate one from the original data.
For each glomerulus we create 100 samples and classify them according to the glomerulus they are based on.
For different levels of noise, the accuracy of prediction is measured, e.g. how many labels could be predicted correctly.
'''
import datetime
import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
import featureselection
from hallem.data import Hallem
import toydata


data = np.transpose(Hallem().response)

# compute features
feature_list, backward_result = featureselection.backward_elimination(data)

# top 20 features produces by BE
top = (feature_list[-11:])[::-1]
print "features:", top

results = []

# levels of noise which will be added
sd_range = range(0, 50, 10)

for f in range(1, len(top)):
    print f
    features = top[0:f]
    a = []

    for sd in sd_range:
        output = []

        # generate the samples and their classes
        samples, labels = toydata.generate_noise_samples_hallem(noise=sd)

        for sample in samples:
            label = -1

            sd = np.vstack([sample[:, features], data[:, features]])
            mm = pdist(sd)
            output.append(np.argmin(mm[0:24]))

        output = np.asarray(output)
        accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
        a.append(accuracy)
    results.append(a)

results = np.asarray(results)

x = sd_range
y = np.asarray(range(1, results.shape[0] + 1))
X, Y = np.meshgrid(x, y)

Z = results

fig = pl.figure(figsize=(6, 4))
pl.suptitle("NN-Classification with features predicted by BE")
# ax = fig.add_subplot
ax2 = fig.add_subplot(111)
im = ax2.imshow(np.transpose(Z), cmap='YlGnBu', interpolation='none', aspect='auto')
ax2.set_ylabel('sd noise')
ax2.set_xlabel('#features')
ax2.yaxis.set_ticklabels(sd_range)
ax2.yaxis.set_ticks(np.arange(len(sd_range)))
ax2.xaxis.set_ticklabels(range(1, len(top)))
ax2.xaxis.set_ticks(range(len(top)))
cb = pl.colorbar(im, orientation='vertical')
cb.set_label("accuracy")

pl.savefig("figures/be_performance_distorted" + datetime.datetime.now().strftime("%Y_%m_%d") + ".png")