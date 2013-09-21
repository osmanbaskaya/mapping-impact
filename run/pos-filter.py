#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
from itertools import izip
from os.path import basename
import gzip

if len(sys.argv) != 2:
    print >> sys.stderr, "{}: Wrong number of arg".format(sys.argv[0])
    exit(1)

fn = sys.argv[1]
word = basename(fn)

tok_f, pos_f, lem_f, raw_f = map(lambda x: fopen(fn + '.' + x + '.gz'),
                                'tok pos lem raw'.split())

outdir = '../data/pos-filtering/'
files = map(lambda x: gzip.open(outdir + word + '.' + x + '.gz', 'w'),
                            'tok pos lem raw index'.split())

lists = [[], [], [], [], []]

print >> sys.stderr, "{} processing".format(word)

for tok, pos, lem, line in izip(tok_f, pos_f, lem_f, raw_f):
    tok_list = tok.lower().split()
    lem_list = lem.split()
    pos_list = pos.split()
    index = None
    for i in xrange(len(lem_list)):
        if word == lem_list[i]: 
            index = i
        elif word == tok_list[i]:
            index = i
    assert index is not None, "{}: No match for line:\n\t{}".format(word, line)
    p = pos_list[index]
    if p.lower()[0] == 'n':
        for L, string in izip(lists, [tok, pos, lem, line, str(index) + '\n']):
            L.append(string)

for f, L in izip(files, lists):
    f.write(''.join(L))
    f.close()
