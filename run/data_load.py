#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" Data Loader for Semeval 2013, Semeval 2010 """

import numpy as np
from collections import defaultdict as dd

__all__ = ['SemevalKeyLoader', ]

class KeyLoader(object):

    def __init__(self, dataset):
        self.dataset = dataset

    def read_keyfile(self, keyfile):
        raise NotImplementedError

class SemevalKeyLoader(KeyLoader):

    def __init__(self):
       super(SemevalKeyLoader, self).__init__("semeval")

    # override
    def read_keyfile(self, keyfile, delim='/'):
        lines = open(keyfile).readlines()
        senses = dd(list)
        for line in lines:
            line = line.split()
            size = len(line)
            assert size >= 3, "Keyfile does not meet the Semeval constraints"
            if size == 3:
                if '/' in line[2]:
                    senses[line[0]].append(line[2].split(delim)[0])
                else:
                    senses[line[0]].append(line[2])
            else:
                raise NotImplementedError, "This case is not implemented yet."
        assert len(lines) == sum([len(senses[s]) for s in senses])
        for s, L in senses.iteritems():
            senses[s] = np.array(L, dtype=str)
        return senses
