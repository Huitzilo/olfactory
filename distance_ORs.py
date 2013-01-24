#!/usr/bin/env python
# encoding: utf-8
"""
Created by  on 2012-01-27.
Copyright (c) 2012. All rights reserved.
"""
from data import Hallem
import pylab as pl
import numpy as np
from scipy import stats

hallem = Hallem()

data = hallem.get_activation_matrix()

# euclidean distance
dist = []
for i in range(len(data[0])):
    x = data[:, i]
    tmp = []
    for j in range(len(data[0])):
        y = data[:, j]
        e = np.sqrt(sum(np.power(x-y,2)))
        tmp.append(e)
    dist.append(tmp)

dist = np.asarray(dist)
pl.pcolor(dist)
pl.colorbar()
pl.show()

# manhattan distance
#dist = []
#for i in range(len(data[0])):
#    x = data[:, i]
#    tmp = []
#    for j in range(len(data[0])):
#        y = data[:, j]
#        e = sum(abs(x-y))
#        tmp.append(e)
#    dist.append(tmp)
#
#dist = np.asarray(dist)
#pl.pcolor(dist)
#pl.colorbar()
#pl.show()