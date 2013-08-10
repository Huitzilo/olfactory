#!/usr/bin/env python
# encoding: utf-8
import csv
import numpy as np
import os


class Hallem(object):
    '''
    Loads and prepares the Hallem data
    '''

    def __init__(self):
        self.response = []
        self.or_list = None
        self.odorant_list = None
        self.load_csv()

    def load_csv(self):
        path_to_csv = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'halemdata.csv')
        d = []
        with open(path_to_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            for row in reader:
                d.append(row)

        d = np.asarray(d)
        self.response = np.asarray(d[2:, 5:], dtype=float)
        self.or_list = d[1, 5:]
        self.odorant_list = d[2:, 0]

    def get_odorant_index(self, name):
        return np.where(self.odorant_list == name)[0][0]

    def get_or_index(self, name):
        return np.where(self.or_list == name)