'''
Check if everything is setup correctly.
'''
try:
  import scipy
  import numpy
  import flask
  import gurobipy
except Exception as inst:
  print inst