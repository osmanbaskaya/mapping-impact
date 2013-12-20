#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Split the keys according to target words. Our gold file is merged. 
All keys are in the same file.  In order create a development set 
in run/gold/twitter|gigaword, we need to split keys in dev set
into separate files.

input_file should be in the Semeval 2013 format. 
Please check the files in keys/gold

Not: Gigaword icin calismiyor, formatta sorun var.
"""

import sys
import os
from collections import defaultdict as dd

input_file = open(sys.argv[1])
output_dir = sys.argv[2]
devset = set(sys.argv[3:])

d = dd(list)
for line in input_file:
    tw = line.split()[0]
    if tw in devset:
        d[tw].append(line)

for tw in devset:
    with open(os.path.join(output_dir, tw + ".key"), 'w') as f:
        f.write("".join(d[tw]))
