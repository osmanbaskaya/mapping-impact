#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import sys, os


system = sys.argv[1] + "-chunk-keys"
typ = sys.argv[2]
dataset = sys.argv[3]

classifiers = os.listdir(system)

training = "semcor uniform hybrid random".split()
testing = "semcor uniform".split()

process = ""
form = "cat {}/{}/*{}-{}* | gzip > ../keys/{}/mapped/{}/{}/{}-{}-{}.ans.gz & "

for c in classifiers:
    for train in training:
        for test in testing:
            process += form.format(system, c, train, test, sys.argv[1], sys.argv[3], typ, c, train, test)

os.system(process + " wait")
#os.system("wc ../keys/{}/mapped/{}/{}/*".format(sys.argv[1], sys.argv[3], typ))
