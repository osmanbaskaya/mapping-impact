#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" Data Loader for Semeval 2013, Semeval 2010 """

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
        # car.n car.n.1 car.sense.3/10 car.sense.6/11
        lines = open(keyfile).readlines()
        senses = dd(dict)
        for line in lines:
            line = line.split()
            size = len(line)
            assert size >= 3, "Keyfile does not meet the Semeval constraints"
            if delim in line[2]:
                ss = [ll.split(delim) for ll in line[2:]]
                # rating should be parse as float
                ss = [(ll[0], float(ll[1])) for ll in ss]
            else:
                ss = [(ll, 1) for ll in line[2:]]
            senses[line[0]][line[1]] = ss
        return senses
    
class ChunkLoader(KeyLoader):

    def __init__(self):
       super(ChunkLoader, self).__init__("ChunkLoader")
    
    # override
    def read_keyfile(self, keyfile, delim='/'):
        # car.n car.n.1 car.sense.3/10 car.sense.6/11
        lines = open(keyfile).readlines()
        senses = dd(dict)
        for line in lines:
            line = line.split()
            size = len(line)
            assert size >= 3, "Keyfile does not meet the Semeval constraints"
            if delim in line[2]:
                ss = [ll.split(delim) for ll in line[2:]]
                # rating should be parse as float
                ss = [(ll[0], float(ll[1])) for ll in ss]
            else:
                ss = [(ll, 1) for ll in line[2:]]
            senses[line[0]][line[1]] = ss
        return senses
    
