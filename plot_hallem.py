#!/usr/bin/env python
# encoding: utf-8
"""

Just plotting the hallem rows (Odorants) as a boxplot to get a look and
feel which odorant might carry the most/the least information

Created by  on 2012-01-27.
Copyright (c) 2012. All rights reserved.
"""
import pylab as pl
import numpy as np

from data import Hallem


hallem = Hallem()
fig2 = pl.figure()
pl.plot()
pl.boxplot(np.transpose(hallem.get_activation_matrix()), bootstrap=10000)
pl.show()