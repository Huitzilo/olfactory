#!/usr/bin/env python
# encoding: utf-8
# preparing the data
import pickle
import numpy as np
import csv
import os


class DoOR(object):
    """

    """


    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
        self.response = []
        self.or_names = None
        self.odorant_molIds = None
        self.odorant_names = None
        self.rep2glom = []

        self.load_file()
        self.load_rep2glom()

    def load_file(self):
        """
            Converting data stored in a file to numpy arrays.
        """
        path_to_file = os.path.join(self.path, 'DoOR_targets.pkl')
        f = open(path_to_file, 'receptor_index')
        p = pickle.load(f)
        f.close()

        self.or_names = np.asarray(p.keys())

        #Molids are defined by Jan in a range from 1 to 1000
        #starting at 0 to avoid indication problems
        self.odorant_molIds = np.arange(0, 1001)
        self.response = np.zeros((len(self.or_names), len(self.odorant_molIds)))

        for i, or_spectra in enumerate(p.items()):
            self.response[i, (or_spectra[1]).keys()] = (or_spectra[1]).values()

        #keeping the odorants where there is data, e.g. where standard deviation or mean are unequal to zero
        info_mask = (np.std(self.response, axis=0) != 0) | (np.mean(self.response, axis=0) != 0)

        self.response = self.response[:, info_mask]
        self.odorant_molIds = self.odorant_molIds[info_mask]
        self.odorant_names = self.molId_to_name(self.odorant_molIds)

    def load_rep2glom(self):
        """
        Loading a file that contains the mapping receptor <--> glomerulus
        """
        #which ors belong to which glom?
        path_to_csv = os.path.join(self.path, "receptor2glom.csv")
        with open(path_to_csv, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            reader.next(),
            for row in reader:
                self.rep2glom.append(row)

        self.rep2glom = np.asarray(self.rep2glom)


    def get_dorsal_data(self):
        """
        Returns a subset of the original data, that just contains the response of receptors that map to dorsal glomeruli.

        Returns
        -------
        response:   numpy.array
                    response matrix for "dorsal" receptors

        or:         numpy.array
                    list of receptor names that map to glomeruli

        odorants:   numpy.array
                    list of odorant names

        """
        dorsal_gloms = []
        path_to_csv = os.path.join(self.path, "glom_dorsal.csv")
        with open(path_to_csv, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                dorsal_gloms.append(row[0])

        dorsal_gloms = np.asarray(dorsal_gloms, dtype=str)

        #get indices of dorsal gloms
        glom_mask = np.in1d(self.rep2glom[:, 2], dorsal_gloms)

        #removing receptors which are actually neurons or for which we have no good data available at the moment (10.08.2013)
        del_mask = np.in1d(self.rep2glom[:, 1], ["ab5B", "Or49a", "Or33a", "ab2B"])
        glom_mask = np.bitwise_and(glom_mask, np.logical_not(del_mask))

        print "removed:"
        print self.rep2glom[del_mask, 1:3]
        print "NOT FOUND: ", np.setdiff1d(dorsal_gloms, np.unique(self.rep2glom[glom_mask, 2]))
        print "FOUND (%i)" % (len(self.rep2glom[glom_mask]))
        print np.array2string(self.rep2glom[glom_mask, 1:3])

        # get indices for ORs which are mapped to a dorsal glom
        ors_mask = np.in1d(self.or_names, self.rep2glom[glom_mask, 1])

        return self.response[ors_mask, :], self.or_names[ors_mask], self.odorant_names

    def molId_to_name(self, indices):
        """
        Maps molIds to names and returns the list.

        Parameters
        ----------
        indices:    numpy.array
                    list of molIds

        Returns
        -------
        odorants:   numpy.array
                    list of corresponding names
        """
        with open(os.path.join(self.path, 'molname.pckl'), 'receptor_index') as f:
            mol2name = pickle.load(f)

        return np.asarray([mol2name[i][0] for i in indices])