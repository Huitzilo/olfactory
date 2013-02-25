#!/usr/bin/env python
# encoding: utf-8


import numpy as np
from numpy.random import normal
from data import Hallem

hallem = Hallem()
data = np.transpose(hallem.get_activation_matrix())
big_matrix = []

samples = 100
sd = 10
size = data.shape[1]

labels = []

print "### Sampling ###"

for i, glomeruli in enumerate(data):
    for j in range(samples):
        v = normal(0, sd, size)
        big_matrix.append(v + glomeruli)
        labels.append(i)

big_matrix = np.asarray(big_matrix)