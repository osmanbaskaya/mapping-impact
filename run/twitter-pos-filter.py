#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
from itertools import izip, count
from os.path import basename
import gzip

if len(sys.argv) != 2:
    print >> sys.stderr, "{}: Wrong number of arg".format(sys.argv[0])
    exit(1)

fn = sys.argv[1]
word = basename(fn)

tok_f, pos_f, lem_f, raw_f = map(lambda x: fopen(fn + '.' + x + '.gz'),
                                'tok pos lem raw'.split())

outdir = '../data/twitter/pos-filtering/'
files = map(lambda x: gzip.open(outdir + word + '.' + x + '.gz', 'w'),
                            'tok pos lem raw index'.split())

lists = [[], [], [], [], []]

print >> sys.stderr, "{} processing".format(word)

rem_file = open('../data/twitter/clean/'+word+".clean", 'w')
c = count(0)
for j, tok, pos, lem, line in izip(c, tok_f, pos_f, lem_f, raw_f):
    tok_list = tok.lower().split()
    lem_list = lem.split()
    pos_list = pos.split()
    index = None
    for i in xrange(len(lem_list)):
        if word == lem_list[i]: 
            index = i
        elif word == tok_list[i]:
            index = i
    if index is None:
        print "{}: No match for {}th line:\n\t{}".format(j, word, line)
        rem_file.write("{}\t{}\n".format(word, j))
    for L, string in izip(lists, [tok, pos, lem, line, str(index) + '\n']):
        L.append(string)

for f, L in izip(files, lists):
    f.write(''.join(L))
    f.close()

rem_file.close()
