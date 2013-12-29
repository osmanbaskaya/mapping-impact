#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

all_comps = set()
clean_comps = set()

all_comp_file = 'pseudoword-samples/pseudowords.979-count.txt'
clean_file = 'pseudoword-list-excluded.txt'

for line in open(all_comp_file).readlines():
    line = line.split()[1:]
    map(all_comps.add, line)

for line in open(clean_file).readlines():
    line = line.split()[1:]
    map(clean_comps.add, line)

print "PSEUDOWORD ",
for c in all_comps.difference(clean_comps):
    print c,
