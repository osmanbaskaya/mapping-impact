#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import gzip
from collections import defaultdict as dd
import re
import sys
from os import path

data = gzip.open(sys.argv[1])
out_dir = sys.argv[2]

d = dd(list)

def write2file(d, out):
    for key, values in d.iteritems():
        f = gzip.open(path.join(out, key) + '.gz', 'w')
        f.write(''.join(values))
        f.close()

for line in data:
    testm = re.search('<(\w+)', line)
    d[testm.group(1)].append(line)

write2file(d, out_dir)





