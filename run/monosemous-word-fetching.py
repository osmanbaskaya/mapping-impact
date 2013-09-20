#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from itertools import count
from nlp_utils import fopen
from os import path

c = count(1)
pseudo_filename = sys.argv[1] # file for pseudoword lists and their components.
giga_filename = sys.argv[2]

base = path.basename(giga_filename)

print >> sys.stderr, "processing {}".format(base)
giga_file = fopen(giga_filename)

files = map(lambda x: fopen('../data/processed/' + x + '.' + base), 'tok pos lem'.split())

outpath = "../data/word-components/"
outfiles = map(lambda x: open(path.join(outpath, x + '.' + base), 'w'), 
                    'tok pos lem raw'.split())

# read pseudoword components
mono_words = set()
for line in open(pseudo_filename):
    line = line.split()[1:]
    if len(line) >= 2:
        map(mono_words.add, line)

for i, line, tok, pos, lem in zip(c, giga_file, *files):
    line_list = line.split()
    tok_list = tok.split()
    pos_list = pos.split()
    lem_list = lem.split()
    if not len(lem_list) == len(pos_list) == len(tok_list):
        print >> sys.stderr, "{}th line does not have equal number of token for {}".format(i, base)
        continue
    for lemma in lem_list:
        if lemma in mono_words:
            #print "{}\n{}\n{}\n{}".format(tok, pos, lem, line)
            outfiles[0].write(tok)
            outfiles[1].write(pos)
            outfiles[2].write(lem)
            outfiles[3].write(line)
            break


