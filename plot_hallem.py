#!/usr/bin/env python
# encoding: utf-8
"""
Created by  on 2012-01-27.
Copyright (c) 2012. All rights reserved.
"""
from data import Hallem
import pylab as pl
import numpy as np

hallem = Hallem()


#fig = pl.figure()
#for i in range(len(hallem.or_list)):
#    name_or = hallem.or_list[i]
#    val_or = hallem.get_activation_matrix()[:, i]
#    pl.subplot(len(hallem.or_list), 1, i)
#    pl.bar(range(len(val_or)), val_or)
#    pl.ylabel(name_or)




fig2 = pl.figure()
#for i in range(len(hallem.odorant_list)):
#    val_odorants = hallem.get_activation_matrix()[i, :]

pl.plot()
pl.boxplot(np.transpose(hallem.get_activation_matrix()), bootstrap=10000)
#pl.xticks(range(len(hallem.odorant_list)),str(hallem.odorant_list)
pl.show()