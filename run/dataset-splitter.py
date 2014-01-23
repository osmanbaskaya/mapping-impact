#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Divide Semeval Dataset chunks into target word chunks.
"""

import sys
import os
from collections import defaultdict as dd

train_f = sys.argv[1] # training chunk
test_f = sys.argv[2] # testing chunk
output_dir = sys.argv[3]
chunk_num = sys.argv[4]

chunk_name = "{}.chunk{}.{}.key"

def get_tw_lines(fn):
    d = dd(list)
    for line in open(fn):
        L = line.split()
        if len(L) != 0: # some file has empty line at the end of the file
            d[L[0]].append(line)
    return d

def write2file(d, typ):
    for tw, lines in d.viewitems():
        fn = chunk_name.format(tw, chunk_num, typ)
        with open(os.path.join(output_dir, fn), 'w') as f:
            f.write("".join(lines))

write2file(get_tw_lines(train_f), "train")
write2file(get_tw_lines(test_f), "test")
