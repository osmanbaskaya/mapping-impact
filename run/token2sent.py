#!/usr/bin/env python

import sys
from os.path import basename
import gzip

filename = sys.argv[1]

tok = gzip.open("../data/processed/tok." + basename(filename), 'w')
lemma = gzip.open("../data/processed/lem." + basename(filename), 'w')
pos = gzip.open("../data/processed/pos." + basename(filename), 'w')


new_line = True
for line in sys.stdin:
    line = line.strip().split("\t")
    if line[0] != "</s>":
        if not new_line:
            line[0] = " " + line[0]
            line[1] = " " + line[1]
            line[2] = " " + line[2]
        tok.write(line[0])
        pos.write(line[1])
        lemma.write(line[2])
        new_line = False
    else:
        tok.write('\n')
        pos.write('\n')
        lemma.write('\n')
        new_line = True

