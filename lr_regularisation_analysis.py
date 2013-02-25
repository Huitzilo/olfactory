#!/usr/bin/env python
# encoding: utf-8


import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as pl

from data import Hallem
import sample_generator


hallem = Hallem()
data = np.transpose(hallem.get_activation_matrix())
big_matrix = sample_generator.big_matrix
labels = sample_generator.labels

x = np.arange(0.001, 0.05, 0.0001)
f = []
a = []
b1 = True
b2 = True

print "### regularizationaraitining"

## Probing over C
for features in x:
    lr = LogisticRegression(penalty='l1', C=features)
    lr.fit(data, range(data.shape[0]))
    f.append(np.sum(np.sum(np.abs(lr.coef_), 0) > 0))
    output = lr.predict(big_matrix)
    accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
    a.append(accuracy)

f = np.asarray(f)

f2 = pl.figure(figsize=(15, 5))
ax2 = f2.add_subplot(111)
ax2.set_title("Regularisation of Logistic Regression")
ln1 = ax2.plot(x[0:len(a)], a, label="accuracy")
ax3 = ax2.twinx()
ln2 = ax3.plot(x[0:len(f)], f, 'r', label='#features')

ax2.set_ylabel("accuracy")
ax2.set_xlabel("regularisation")
ax3.set_ylabel("#features")
ax3.set_ylim(0, 74.6)
ax2.set_ylim(0, 1.5)
ax2.grid()
lns = ln1 + ln2
labs = [l.get_label() for l in lns]
ax2.legend(lns, labs, loc=0)
pl.savefig("figures/lr_regularisation2.jpg")

m = np.unique(f[f < 25])
indices = []
for features in m:
    indices.append(np.max(np.where(f == features)))

pf = []
for index in indices:
    lr = LogisticRegression(penalty='l1', C=x[index])
    lr.fit(data, range(data.shape[0]))
    odorants = np.where((np.sum(np.abs(lr.coef_), 0)))[0]

    lr = LogisticRegression(penalty='l1', C=100)
    lr.fit(data[:, odorants], range(data.shape[0]))
    output = lr.predict(big_matrix[:, odorants])
    accuracy = 1 - np.count_nonzero(output - labels) / float(len(labels))
    pf.append(accuracy)
    print "c=", x[index], "yielded ", f[index], "features with acc=", a[
        index], "improved to", accuracy, "accuracy on secondary LR with C=100"

f4 = pl.figure(figsize=(15, 5))
ax4 = f4.add_subplot(111)
ax4.set_title("Regularisation of Logistic Regression")
ax4.set_xlabel("#features")
ax4.set_ylabel("accuracy")
ax4.grid()
ln41 = ax4.plot(m, pf, label="C=100")

lns = ln41
labs = [l.get_label() for l in lns]
ax4.legend(lns, labs, loc=5)

pl.savefig("figures/lr_regularisation_improved_.jpg")