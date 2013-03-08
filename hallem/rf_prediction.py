#!/usr/bin/env python
# encoding: utf-8


import numpy as np
from sklearn.ensemble import RandomForestClassifier
from hallem.data import Hallem
import sample_generator

hallem = Hallem()
data = np.transpose(hallem.get_activation_matrix())

big_matrix, labels = sample_generator.generate_samples()

f = []
a = []
b1 = True
b2 = True

rf = RandomForestClassifier()
# fitting to labels 0:23, e.g. one label per glomerulus
rf.fit(data, range(data.shape[0]))

result = rf.predict(big_matrix)

print result


# f2 = pl.figure(figsize=(15, 5))
# ax2 = f2.add_subplot(111)
# ax2.set_title("Regularisation of Logistic Regression")
# ln1 = ax2.plot(c_range[0:len(a)], a, label="accuracy")
# ax3 = ax2.twinx()
# ln2 = ax3.plot(c_range[0:len(f)], f, 'r', label='#features')
#
# ax2.set_ylabel("accuracy")
# ax2.set_xlabel("regularisation")
# ax3.set_ylabel("#features")
# ax3.set_ylim(0, 74.6)
# ax2.set_ylim(0, 1.5)
# ax2.grid()
# lns = ln1 + ln2
# labs = [l.get_label() for l in lns]
# ax2.legend(lns, labs, loc=0)
# pl.savefig("figures/lr_regularisation2" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".jpg")

# m = np.unique(f[f < 21])
# indices = []
# for c in m:
#     indices.append(np.max(np.where(f == c)))

# pf = []
# for index in indices:
#     lr = LogisticRegression(penalty='l1', C=c_range[index])
#     lr.fit(data, range(data.shape[0]))
#     odorants = np.where((np.sum(np.abs(lr.coef_), 0)))[0]
#
#     c = 1000
#     lr = LogisticRegression(penalty='l1', C=c)
#     lr.fit(data[:, odorants], range(data.shape[0]))
#     output = lr.predict(big_matrix[:, odorants])
#     accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
#     pf.append(accuracy)
#     print "c=", c_range[index], "yielded ", f[index], "features with acc=", a[
#         index], "improved to", accuracy, "accuracy on secondary LR with C=", c
#
# f4 = pl.figure(figsize=(15, 5))
# ax4 = f4.add_subplot(111)
# ax4.set_title("Regularisation of Logistic Regression")
# ax4.set_xlabel("#features")
# ax4.set_ylabel("accuracy")
# ax4.grid()
# ln41 = ax4.plot(m, pf, label="C=100")
#
# lns = ln41
# labs = [l.get_label() for l in lns]
# ax4.legend(lns, labs, loc=5)
#
# pl.savefig("figures/lr_regularisation_improved_" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".jpg")

# sd_range = range(1, 161, 5)
#
# results = []
# number_f = []
# for index in indices:
#
#     # compute the odorants
#     rf = LogisticRegression(penalty='l1', C=c_range[index])
#     rf.fit(data, range(data.shape[0]))
#     odorants = np.where((np.sum(np.abs(rf.coef_), 0)))[0]
#     number_f.append(len(odorants))
#
#     c = 1000
#     rf = LogisticRegression(penalty='l1', C=c)
#     rf.fit(data[:, odorants], range(data.shape[0]))
#     a = []
#     for sd in sd_range:
#         samples, labels = sample_generator.generate_samples(sd=sd)
#
#         c = 1000
#         output = rf.predict(samples[:, odorants])
#         accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
#         a.append(accuracy)
#
#     results.append(a)
#
# results = np.asarray(results)
#
# x = sd_range
# y = number_f
# X, Y = np.meshgrid(x, y)
#
# Z = results
# l = [str(x) + "" for x in number_f]
#
# print l
# fig = pl.figure(figsize=(20, 12))
# pl.suptitle("Logistic Regression Classification on 100 Samples per Glomeruli")
# ax = fig.add_subplot(121, projection='3d')
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='YlGnBu', vmin=0, vmax=1, linewidth=0)
# ax.set_xlabel('sd noise')
# ax.set_xlim3d(0, np.max(sd_range) + 5)
# ax.w_yaxis.set_ticklabels(l)
# ax.w_yaxis.set_ticks(np.arange(len(l))  )
# ax.set_ylabel('#features')
# ax.set_zlabel('accuracy')
# ax.set_zlim3d(0, 1)
# ax.view_init(azim=315)
#
#
# ax2 = fig.add_subplot(122)
# im = ax2.imshow(np.transpose(Z), cmap='YlGnBu', interpolation='none', aspect='auto')
# ax2.set_ylabel('sd noise')
# ax2.set_xlabel('#features')
# ax2.xaxis.set_ticklabels(l)
# ax2.xaxis.set_ticks(np.arange(len(l)))
# ax2.yaxis.set_ticklabels(sd_range)
# ax2.yaxis.set_ticks(np.arange(len(sd_range)))
# pl.colorbar(im, orientation='vertical')
# pl.savefig("figures/lr_sd_acc_3d" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".png")