#!/usr/bin/env python
# encoding: utf-8
import csv
import numpy as np


"""
    The Hallem Data nicely prepared for you
"""
class Hallem(object):

    def __init__(self):
        self.data = []
        self.or_list = None
        self.odorant_list = None
        self.load_csv()

    def load_csv(self):
        path_to_csv = "data/halemdata.csv"
        with open(path_to_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader:
                self.data.append(row)

        self.data = np.asarray(self.data)
        self.or_list = self.data[1, 6:]
        self.odorant_list = self.data[2:, 0]

    def get_activation_matrix(self):
        return np.asarray(self.data[2:, 6:], dtype=float)