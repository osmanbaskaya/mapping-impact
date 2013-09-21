#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from itertools import count, izip
from nlp_utils import fopen
from collections import defaultdict as dd
from os import path

c = count(1)
pseudo_filename = sys.argv[1] # file for pseudoword lists and their components.
giga_filename = sys.argv[2]

base = path.basename(giga_filename)

print >> sys.stderr, "processing {}".format(base)
giga_file = fopen(giga_filename)

files = map(lambda x: fopen('../data/processed/' + x + '.' + base), 'tok pos lem'.split())

outpath = "../data/components/"
outfiles = map(lambda x: open(path.join(outpath, x + '.' + base), 'w'), 
                    'tok pos lem raw'.split())

lines = set()
collections = [[], [], [], []]

# read pseudoword components
mono_words = set()
for line in open(pseudo_filename):
    line = line.split()[1:]
    if len(line) >= 2:
        map(mono_words.add, line)

for i, line, tok, pos, lem in zip(c, giga_file, *files):
    tok_list = tok.lower().split()
    pos_list = pos.split()
    lem_list = lem.split()
    if not len(lem_list) == len(pos_list) == len(tok_list):
        print >> sys.stderr, "{}th line does not have equal number of token for {}".format(i, base)
        continue
    for i in xrange(len(lem_list)):
        lemma = lem_list[i]
        token = tok_list[i]
        if lemma in mono_words or token in mono_words:
            if line not in lines:
                lines.add(line)
                for L, string in izip(collections, [tok, pos, lem, line]):
                    L.append(string)
            break

# write 2 files
for f, C in izip(outfiles, collections):
    f.write(''.join(C))
    f.close()
