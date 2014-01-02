#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import sys, os


dataset = sys.argv[3]
if dataset != "gigaword":
    system = sys.argv[1] + "-%s-chunk-keys" % dataset
else:
    system = sys.argv[1] + "-chunk-keys"

typ = sys.argv[2]
classifiers = os.listdir(system)
training = "semcor uniform hybrid random".split()
testing = "semcor uniform".split()

process = ""
form = "cat {}/{}/*{}-{}* | gzip > ../keys/{}/mapped/{}/{}/{}-{}-{}.ans.gz & "

print >> sys.stderr, system, dataset, typ

for c in classifiers:
    for train in training:
        for test in testing:
            process += form.format(system, c, train, test, sys.argv[1], sys.argv[3], typ, c, train, test)

os.system(process + " wait")
