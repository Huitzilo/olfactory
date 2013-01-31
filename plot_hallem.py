#!/usr/bin/env python
# encoding: utf-8
"""

Just plotting the hallem rows (Odorants) as a boxplot to get a look and
feel which odorant might carry the most/the least information

"""
import pylab as pl
import numpy as np

from data import Hallem


hallem = Hallem()
fig2 = pl.figure()
pl.plot()
pl.boxplot(np.transpose(hallem.get_activation_matrix()), bootstrap=10000)
pl.show()