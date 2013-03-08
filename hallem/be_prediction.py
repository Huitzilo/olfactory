#!/usr/bin/env python
# encoding: utf-8
#

import datetime

import numpy as np
from scipy.spatial.distance import pdist
import matplotlib.pyplot as pl

from hallem.data import Hallem
import sample_generator

# top 20 features of BE

# top 20 features produces by BE from 26.02.2013
top = [91, 44, 3, 7, 64, 33, 63, 84, 78, 83, 95, 0, 75, 9, 85, 8, 49, 90, 6, 5]

data = np.transpose(Hallem().get_activation_matrix())
# samples, labels = sample_generator.generate_samples(sd=10)

# a = []
#
# start = time()
#
# results = []
#
# for f in range(len(top)):
#     features = top[0:f]
#     output = []
#
#     for sample in samples:
#         min = 1000000
#         label = -1
#
#         s = np.vstack([sample[:, features], data[:, features]])
#         mm = pdist(s)
#         output.append(np.argmin(mm[0:24]))
#
#         # for i, glom in enumerate(data):
#         #     d = euclidean(sample[:, features], glom[:, features])
#         #     if min > d:
#         #         min = d
#         #         label = i
#         # output.append(label)
#
#
#     output = np.asarray(output)
#     accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
#     # print f, accuracy
#     a.append(accuracy)
#
# end = time()
# print round(1000*(end - start),2), "ms"
#
# f = pl.figure(figsize=(20, 10))
# ax = f.add_subplot(111)
# ax.plot(range(1, len(a) + 1), a, label="accuracy")
# ax.set_xlabel("#features")
# ax.set_title("Accuracy with #features")
# ax.set_ylabel("accuracy")
# pl.savefig("figures/be_prediction.png")
#
# a = []
# sd_range = range(1, 151, 10)
# for s in sd_range:
#     samples, labels = sample_generator.generate_samples(sd=s)
#     features = top[0:5]
#     output = []
#     for sample in samples:
#
#         min = 1000000
#         label = -1
#
#         matrix = np.vstack([sample[:, features], data[:, features]])
#         mm = pdist(matrix)
#         output.append(np.argmin(mm[0:24]))
#
#         # output.append(label)
#     print s
#     output = np.asarray(output)
#     accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
#     a.append(accuracy)
#
# f2 = pl.figure(figsize=(20, 10))
# ax2 = f2.add_subplot(111)
# ax2.plot(sd_range, a, label="accuracy")
# ax2.set_xlabel("sd")
# ax2.set_title("sd")
# ax2.set_ylabel("accuracy")
# pl.savefig("figures/be_prediction_sd.png")


results = []

sd_range = range(1, 161, 5)

for f in range(1, len(top)):
    print f
    features = top[0:f]
    a = []

    for sd in sd_range:
        output = []
        samples, labels = sample_generator.generate_samples(sd=sd)

        for sample in samples:
            min = 1000000
            label = -1

            sd = np.vstack([sample[:, features], data[:, features]])
            mm = pdist(sd)
            output.append(np.argmin(mm[0:24]))

        output = np.asarray(output)
        accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
        # print f, accuracy
        a.append(accuracy)
    results.append(a)

results = np.asarray(results)

x = sd_range
y = np.asarray(range(1, results.shape[0] + 1))
X, Y = np.meshgrid(x, y)

Z = results

fig = pl.figure(figsize=(20, 12))
pl.suptitle("Backward Elimination Classification on 100 Samples per Glomeruli")
ax = fig.add_subplot(121, projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='YlGnBu', vmin=0, vmax=1, linewidth=0)
ax.set_xlabel('sd noise')
ax.set_xlim3d(0, np.max(sd_range) + 5)
ax.set_ylabel('#features')
ax.set_ylim3d(0, len(top))
ax.set_zlabel('accuracy')
ax.set_zlim3d(0, 1)
ax.view_init(azim=315)
# pl.show()


ax2 = fig.add_subplot(122)
im = ax2.imshow(np.transpose(Z), cmap='YlGnBu', interpolation='none', aspect='auto')
ax2.set_ylabel('sd noise')
ax2.set_xlabel('#features')
ax2.yaxis.set_ticklabels(sd_range)
ax2.yaxis.set_ticks(np.arange(len(sd_range)))
pl.colorbar(im, orientation='vertical')

pl.savefig("figures/eu_sd_acc_3d" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".png")