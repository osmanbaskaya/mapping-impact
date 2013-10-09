#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys 
import os
import gzip
from itertools import cycle

limit = 50
c = cycle(range(1,limit+1))

test_path = 'sentence/test/'
train_path = 'sentence/train/'


def fetch_instances(path, comps):
    all_lines = []
    for comp in comps:
        fn = path + comp + '.gz'
        if os.path.exists(fn):
            all_lines.extend(gzip.open(fn).readlines())
    return (all_lines, len(all_lines))


for line in open(sys.argv[1]):
    print line
    line = line.split()
    base, comps = line[0], line[1:]
    seen = {}
    fname = test_path + base + '.gz'
    test_insts, test_total = fetch_instances(test_path, comps)
    train_insts, train_total = fetch_instances(train_path, comps)
    print test_total, train_total

    



