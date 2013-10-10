#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys, os

if len(sys.argv) != 4:
    print "Usage: {} targetword seed kval".format(sys.argv[0])
    exit(1)

tw = sys.argv[1]
seed = sys.argv[2]
kval = sys.argv[3]

inp = 'zcat pairs/{}.pairs.gz'.format(tw)

scode = "scode -i 1 -a -r 1 -d 25 -z 0.166 -p 50 -u 0.2 -s {} -v ".format(seed)
scode_out = "gzip > scode/{}.scode.gz "

process = " | ".join([inp, scode, scode_out.format(tw)])
os.system(process + " & wait")
#print process

column = "perl -ne 'print if s/^1://'";
kmeans_input_base= "zcat scode/{}.scode.gz".format(tw)
kmeans_base = "wkmeans -r 2 -l -w -v -s {} -k {}".format(seed, kval)
kmeans_out_base = "gzip > kmeans/{}.kmeans.gz".format(tw)


process = " | ".join([kmeans_input_base, column, kmeans_base, kmeans_out_base])
#print process
os.system(process + " & wait")

word_filter = "grep -P '^<\w+\.test\.\d+>'"
sense_find = "find-sense-test.py kmeans/{}.kmeans.gz >> ans/{}.ans".format(tw, tw)
process = " | ".join([inp, word_filter, sense_find])
#print process
os.system(process + " & wait")
# remove the temp file and files in it.
#shutil.rmtree(path)
