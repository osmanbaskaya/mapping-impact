#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Semeval System key splitter
"""

import sys
import os
from collections import defaultdict as dd

system_f = sys.argv[1] # system key
# we really do not like directories ending w/ .txt .key. Next line is coming for!
output_dir = "%s-ans" % sys.argv[2].rsplit('.', 1)[0] 

print >> sys.stderr, output_dir

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

tw_f_name = "{}.ans"

def get_tw_lines(fn):
    d = dd(list)
    for line in open(fn):
        L = line.split()
        if len(L) != 0: # some file has empty line at the end of the file
            d[L[0]].append(line)
    return d

def write2file(d):
    for tw, lines in d.viewitems():
        fn = tw_f_name.format(tw)
        with open(os.path.join(output_dir, fn), 'w') as f:
            f.write("".join(lines))

write2file(get_tw_lines(system_f))
