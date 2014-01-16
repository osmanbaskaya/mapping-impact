#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import re
from collections import defaultdict as dd
from itertools import product


test_set = sys.argv[1]
files = map(open, sys.argv[2:])

#regex = re.compile(".*/keys/(\w+)/.*/()\.ans.gz.*/\w+\.(\w+).key")
regex = re.compile(".*/keys/(\w+)/.*/(\d+)/(.*)-\w+-\w+.ans.gz.*\.(.*).key")
pr_regex = re.compile(".*(0\.\d+)")

systems = "aiku hdp cw squat ensemble".split()
classifiers = "BernoulliNBWrapper MultinomialNB SVM_Linear SVM_Gaussian \
               DecisionTree-Entropy DecisionTree-Gini".split()

def f1_score(p, r):
    p = float(p)
    r = float(r)
    return 2 * p * r / (p+r)

d = dd(lambda: dd(lambda: dd(lambda: dd(list))))
for f in files:
    #match = re.match(".*/(\w+)mapped-ims(\d+)-.*.scores", f.name)
    info = []
    scores = []
    for line in f:
        line = line.strip()
        if line.startswith("Scores"):
            match = regex.search(line)
            s, inst, m, t = match.group(1), match.group(2), match.group(3), match.group(4) 
            inst = int(inst)
        if line.startswith("Precision") or line.startswith("Recall"):
            pr = pr_regex.search(line).group(1)
            d[s][inst][t][m].append(pr)

m = len(systems)
c = 0

curr_clf = ""
for clf in classifiers:
    for s in systems:
        if clf != curr_clf:
            print '\n'
            curr_clf = clf
        for i in sorted(d[s].keys()):
            print >> sys.stderr, clf, s, i
            print f1_score(*d[s][i][test_set][clf]), '\t',
        print

#for ts, clf, s in product(train_sets, classifiers, systems):
    #clf = clf + "-" + "-".join([ts, test_set])
    #print >> sys.stderr, clf, s
    #print >> sys.stderr, s, clf
    #if c % m == 0 and c != 0:
        #print "\n"
    #print "\t".join(d[s][test_set][clf])
    #c += 1
