#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from os.path import basename
import gzip

exclude = set(["<USERID>", "<URL>"])

filename = sys.argv[1]
fn = basename(filename).replace('.tsv', '')

tok = gzip.open('../data/twitter/monosemous-words/' + fn + '.tok.gz', 'w')
pos = gzip.open('../data/twitter/monosemous-words/' + fn + '.pos.gz', 'w')
lemma = gzip.open('../data/twitter/monosemous-words/' + fn + '.lem.gz', 'w')

new_line = True
for line in sys.stdin:
    line = line.strip().split("\t")
    if line[0] != "</s>":
        if len(line) != 3:
            line = [line[0], "N", line[0]]
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

