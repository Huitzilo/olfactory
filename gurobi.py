#!/usr/bin/env python
# encoding: utf-8
"""
    Call this script from the gurobi shell, e.g.
    1. start shell: gurobi.sh
    2. import this file
    3. run optimize_distance() or optimize_features()
"""
from gurobipy import *
import numpy as np


def optimize_distance(data, number_features=10, feature_names=None):
  '''
      Generates a linear programming problem to find the optimal features for the given matrix.
  '''
  print "Number of data points:", data.shape[0]
  print "Number of features", data.shape[1]

  matrix = []
  for i, x in enumerate(data):
    for j in range(i + 1, len(data)):
      matrix.append(np.power(data[i] - data[j], 2))

  matrix = np.asarray(matrix)
  number_features = 2

  try:
    # Create a new model
    m = Model("mip1")

    # Create variables
    for i in range(data.shape[1]):
      m.addVar(vtype=GRB.BINARY, name="x" + str(i))

    z = m.addVar(vtype=GRB.INTEGER, lb=0, ub=GRB.INFINITY, name="z")

    m.update()

    vars = m.getVars()


    # Set constraints
    odorants_exp = LinExpr()
    for v in vars[:-1]:
      odorants_exp += v
    m.addConstr(odorants_exp, GRB.EQUAL, number_features)

    for row in matrix:
      row_exp = LinExpr()
      for i in range(len(row)):
        row_exp += row[i] * vars[i]

      row_exp += -1 * z
      m.addConstr(row_exp, GRB.GREATER_EQUAL, 0)


    # Set objective
    m.setObjective(z, GRB.MAXIMIZE)

    m.update()
    m.optimize()

    x = []
    for v in m.getVars():
      x.append(v.x)

    print 'Value of objective:', np.sqrt(m.objVal)

    if feature_names:
      print

    else:
      print np.where(np.asarray(x) == 1.0)[0]

  except GurobiError as inst:
    print 'Error reported'
    print inst


print "yes"