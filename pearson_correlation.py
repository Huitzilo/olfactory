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
from scipy import spatial
from scipy import cluster

hallem = Hallem()

data = hallem.get_activation_matrix()



# Analyse the correlation of odorants
#correlation = []
#for i in range(len(data[:, 0])):
#    x = data[i]
#    tmp = []
#    for j in range(len(data[:, 0])):
#        y = data[j]
#        p = stats.pearsonr(x,y)[0]
#
#        #if (p>.93) and i != j:
#            #print "p = ", p ," for" , hallem.odorant_list[i],"(", i , ") - ", hallem.odorant_list[j], "(", j , ")"
#        tmp.append(p)
#    correlation.append(tmp)
#
#
#print "\n\nOR\n\n"

# Analyse the correlation of ORs
correlation = []
for i in range(len(data[0])):
    x = data[:, i]
    tmp = []
    for j in range(len(data[0])):
        y = data[:, j]
        p = stats.pearsonr(x,y)[0]
        tmp.append(p)
    correlation.append(tmp)

correlation = abs(np.asarray(correlation))

correlation = np.asarray(correlation)
pl.subplot(121)
link = cluster.hierarchy.linkage(correlation, method="single")
dend = cluster.hierarchy.dendrogram(link, orientation="right")

#pl.show()

final = []
for i in dend['ivl']:
    final.append(correlation[int(i)])

final = abs(np.asarray(final))
pl.subplot(122)
pl.pcolor(final)
pl.colorbar()
pl.show()