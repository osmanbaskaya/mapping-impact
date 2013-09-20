#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from nlp_utils import fopen
import gzip
from itertools import count


def write2files(files, strings):
    
    for i in xrange(len(files)):
        files[i].write(strings[i])
    map(lambda x: x.close(), files)

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


#ll = list(mono_words)
#ll.sort()
#for l in ll:
    #print l
#exit()

print >> sys.stderr, "total # of pseudowords' components: {}".format(len(mono_words))

d = dict()
out = '../data/monosemous-words/'
c = count(1)
for i, line, tok, pos, lem in zip(c, raw_f, tok_f, pos_f, lem_f):
    no_word = True
    lem_list = lem.split()
    for lemma in lem_list:
        if lemma in mono_words:
            no_word = False
            if lemma not in d:
                outfiles = map(lambda x: gzip.open(out + lemma + '.' + x +  '.gz', 'w'), 
                               'tok pos lem raw'.split())
                d[lemma] = outfiles
            else:
                d[lemma] = map(lambda x: gzip.open(out + lemma + '.' + x +  '.gz', 'a+'), 
                               'tok pos lem raw'.split())
            write2files(d[lemma], [tok, pos, lem, line])
            #break # write the first occured lemma & skip others if any
    if no_word:
        print >> sys.stderr, "No lemma found in line {}: {}".format(i, lem)


