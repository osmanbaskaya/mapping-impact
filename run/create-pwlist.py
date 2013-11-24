#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


#./create-pwlist.py pseudoword-samples/pseudowords.979-count.txt twitter-new-exclude.txt

import sys, os

orig_f = open(sys.argv[1])
exc_f = open(sys.argv[2])

exclude = set()

for line in exc_f:
    line = line.split()
    psense = os.path.basename(line[1])
    exclude.add(psense)

print >> sys.stderr, "Removing {} of psense".format(len(exclude))

for line in orig_f:
    senses = line.split()[1:]
    bools = [True for s in senses if s in exclude]
    if not any(bools):
        print line,


