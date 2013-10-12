#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys, os

inp_fold = sys.argv[1]
outp_fold = sys.argv[2]

OUT = '../data/cleaner-tweets/'

for f in os.listdir(inp_fold):
    rem_lines = open(os.path.join(inp_fold, f)).readlines()
    rem_index = [int(line.split()[1]) for line in rem_lines]
    if len(rem_index) > 0:
        print >> sys.stderr, "Cleaning %s" % f
        fn = f.replace('.clean', '.tsv')
        tweet_lines = open(os.path.join(outp_fold, fn)).readlines()
        map(tweet_lines.pop, sorted(rem_index, reverse=True))
        new_file = open(os.path.join(OUT, fn), 'w')
        new_file.write(''.join(tweet_lines))
        new_file.close()

