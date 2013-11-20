#!/usr/bin/env python
"""
    Generates a linear programming problem to find the optimal subset for the Hallem data an solves it actually.

    Call this script from the gurobi shell, e.g.
        gurobi.sh gurobi_optimize_distance.py


    Purpose of this script is to find the maximal distance for a given number of features.
"""
# encoding: utf-8
from gurobipy import *
from data import Hallem
import numpy as np


#loading the data
hallem = Hallem()
data = np.transpose(hallem.response) # Glomeruli x Odorants instead of Odorants x Glomeruli


# !!! testing removing of strongly correlated features !!!
# r_index = 53
# data = np.delete(data, r_index, axis=1)

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

    print 'Obj:', m.objVal, str(np.sqrt(m.objVal)).replace(".", ",")

    features_names = hallem.odorant_list

    # !!! testing removing of strongly correlated features !!!
    # print "removed features: " + features_names[r_index]
    # features_names = np.delete(features_names, r_index)

    print np.where(np.asarray(x) == 1.0)[0]
    #print features_names[np.where(np.asarray(x) == 1.0)[0]]

except GurobiError:
    print 'Error reported'