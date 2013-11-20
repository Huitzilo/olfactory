#!/usr/bin/env python
# encoding: utf-8
import numpy as np
import scipy as sp


def correlation(matrix):
  '''
  Given a matrix, compute the correlation of its rows to each other.
  '''
  corr = []
  for i, rowA in enumerate(matrix):
    for j, rowB in enumerate(matrix):
      if j > i:
        c = sp.stats.pearsonr(rowA, rowB)[0]
        corr.append((i, j, c))

  corr = np.asarray(corr)
  return corr