#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys 
import os
import gzip
#import re
#from itertools import count

sub_path = 'sub/'
out = 'wordsub/'

def fetch(path, comps):
    all_lines = []
    for comp in comps:
        fn = path + comp + '.gz'
        if os.path.exists(fn):
            lines = gzip.open(fn).readlines()
            all_lines.extend(lines)
    return (all_lines, len(all_lines))

#def replace(base, data):
    #return re.sub('<\w+', '<{}'.format(base), ''.join(data))

for line in open(sys.argv[1]):
    line = line.split()
    base, comps = line[0], line[1:]
    base = base[1:-1]
    base = base.replace("'", "")
    seen = {}
    test_insts, test_total = fetch(sub_path, comps)
    fn = "{}{}".format(out, base)
    pseudoword_file = gzip.open(fn + '.gz', 'w')
    pseudoword_file.write(''.join(test_insts))
    pseudoword_file.close()
