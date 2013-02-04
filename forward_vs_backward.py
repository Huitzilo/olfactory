#!/usr/bin/env python
# encoding: utf-8
import pylab as pl
import numpy as np

import forward_selection
import backward_elimination


x = forward_selection.forward_result
y = backward_elimination.backward_result[1:]
y = y[::-1]

print len(x)
print len(y)

print x
print y
pl.figure(figsize=(7, 7))
pl.plot(np.arange(len(x)), y, 'red')
pl.plot(np.arange(len(x)), x, 'blue')
pl.xlabel("#features")
pl.legend(['backward', 'forward'])
pl.ylabel("euclidean distance")
pl.savefig("figures/forward vs backward.png")