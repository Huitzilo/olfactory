#!/usr/bin/env python
# encoding: utf-8
'''
    Generates a linear programming problem to find the optimal subset for the dorsal DoOR data an solves it actually.

    Call this script from the gurobi shell, e.g.
        gurobi.sh gurobi_optimize_odorants.py

    Purpose of this script is to find the minimal number of odorants required to have a minimal distance.
'''
from gurobipy import *
import numpy as np
from data import DoOR

door = DoOR()

minimal_distance = 0.4
data, ors, odorants = door.get_dorsal_data()
print data.shape

matrix = []
for i, x in enumerate(data):
    for j in range(i + 1, len(data)):
        matrix.append(np.power(data[i] - data[j], 2))

matrix = np.asarray(matrix)
print matrix.shape

try:

    # Create a new model
    m = Model("mip1")

    # Create variables

    for i in range(data.shape[1]):
        m.addVar(vtype=GRB.BINARY, name="x" + str(i))

    m.update()
    vars = m.getVars()

    # Set objective
    obj_exp = LinExpr()
    for v in vars:
        obj_exp += v

    m.setObjective(obj_exp, GRB.MINIMIZE)

    # Set constraints
    for row in matrix:
        row_exp = LinExpr()
        for i in range(len(row)):
            row_exp += row[i] * vars[i]

        m.addConstr(row_exp, GRB.GREATER_EQUAL, minimal_distance ** 2)

    m.update()
    m.write("odorants.lp")
    m.optimize()

    if m.status == GRB.OPTIMAL:
        x = []
        for v in m.getVars():
            x.append(v.x)
            print v.varName, v.x

        print 'Obj:', m.objVal
        print np.where(np.asarray(x) == 1.0)[0]

    else:
        print "calc"


except GurobiError:
    print 'Error reported'

