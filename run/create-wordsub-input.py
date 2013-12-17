#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys 
import os
import gzip
#import re
#from itertools import count

sub_path = sys.argv[2] # sub vector path
out = sys.argv[3] # output path. that is wordsub

# existed pseudowords (this is for the twitter dataset)
### twitter ###
#existed = set([tw.strip() for tw in open(sys.argv[4]).readlines()])
### twitter ###

def fetch(path, comps):
    all_lines = []
    for comp in comps:
        fn = path + comp + '.gz'
        if os.path.exists(fn):
            lines = gzip.open(fn).readlines()
            all_lines.extend(lines)
    return (all_lines, len(all_lines))

#FIXME unnecessary fetching with some pseuwords that share the same components
for line in open(sys.argv[1]):
    line = line.split()
    base, comps = line[0], line[1:]
    base = base[1:-1]
    base = base.replace("'", "")
    #### Twitter #####
    #if base in existed:
        #test_insts, test_total = fetch(sub_path, comps)
        #fn = "{}{}".format(out, base)
        #pseudoword_file = gzip.open(fn + '.gz', 'w')
        #pseudoword_file.write(''.join(test_insts))
        #pseudoword_file.close()
    #### Twitter ####
    test_insts, test_total = fetch(sub_path, comps)
    fn = "{}{}".format(out, base)
    pseudoword_file = gzip.open(fn + '.gz', 'w')
    pseudoword_file.write(''.join(test_insts))
    pseudoword_file.close()
