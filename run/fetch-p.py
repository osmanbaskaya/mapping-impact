#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from os.path import basename
from itertools import count
from nlp_utils import fopen
import gzip

filename = sys.argv[1]

START_TOKEN = '<P>\n'
END_TOKEN = '</P>\n'

parag = ""
is_parag = False

c = count(1)

out = gzip.open('../data/raw/out-' + basename(filename), 'w')

for line in fopen(filename):
    if line == START_TOKEN:
        is_parag = True
        continue
    elif line == END_TOKEN:
        is_parag = False
        #print "{}, {}".format(c.next(), parag.strip())
        print >> out, parag.strip()
        c.next()
        parag = ""
        continue
    if is_parag:
        parag = parag + ' ' + line.strip()

print "{}: {} paragraphs fetched".format(basename(filename), c.next()-1)
