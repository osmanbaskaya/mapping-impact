#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
import gzip
from itertools import count, izip
from collections import defaultdict as dd


if len(sys.argv) != 6:
    print >> sys.stderr, "{}: Wrong number of arg".format(sys.argv[0])
    exit(1)

pseudo_word_file = fopen(sys.argv[1])
tok_f, pos_f, lem_f, raw_f = map(lambda x: fopen(x), sys.argv[2:])

# read pseudoword components
mono_words = set()
for line in pseudo_word_file:
    line = line.split()[1:]
    if len(line) >= 2:
        map(mono_words.add, line)

print >> sys.stderr, "total # of pseudowords' components: {}".format(len(mono_words))

lines = dd(lambda : set())

d = dd(lambda : [[], [], [], []])
out = '../data/monosemous-words/'
c = count(1)
for i, line, tok, pos, lem in zip(c, raw_f, tok_f, pos_f, lem_f):
    if i % 100000 == 0:
        print >> sys.stderr, "{}th line processing".format(i)
    no_word = True
    lem_list = lem.split()
    tok_list = tok.lower().split()
    for i in xrange(len(lem_list)):
        key = None
        lemma = lem_list[i]
        token = tok_list[i]
        if lemma in mono_words:
            key = lemma
        elif token in mono_words:
            key = token
        if key is not None:
            no_word = False
            if line not in lines[key]:
                lines[key].add(line)
                for L, string in izip(d[key], [line, tok, pos, lem]):
                    L.append(string)
    if no_word:
        print >> sys.stderr, "No lemma or token found in line {}: {}".format(i, lem)

for key, collections in d.iteritems():

    print >> sys.stderr, "{}, {}".format(key, len(collections))
    outfiles = map(lambda x: gzip.open(out + key + '.' + x +  '.gz', 'w'), 
                                   'raw tok pos lem'.split())
    size = len(collections[0])
    for f, C in izip(outfiles, collections):
        assert size == len(C), "{}: file sizes not equal"
        f.write(''.join(C))
        f.close()


