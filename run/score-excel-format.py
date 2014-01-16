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
regex = re.compile(".*/keys/(\w+)/.*/(.*).ans.gz.*\.(.*).key")
pr_regex = re.compile(".*(0\.\d+)")

systems = "aiku hdp cw squat ensemble".split()
classifiers = "BernoulliNBWrapper MultinomialNB SVM_Linear SVM_Gaussian \
               DecisionTree-Entropy DecisionTree-Gini".split()
train_sets = "semcor uniform hybrid random".split()


d = dd(lambda: dd(lambda: dd(list)))
for f in files:
    info = []
    scores = []
    for line in f:
        line = line.strip()
        if line.startswith("Scores"):
            match = regex.search(line)
            s, m, t = match.group(1), match.group(2), match.group(3) #system, mapping, test
        if line.startswith("Precision") or line.startswith("Recall"):
            pr = pr_regex.search(line).group(1)
            d[s][t][m].append(pr)

m = len(systems)
c = 0
for ts, clf, s in product(train_sets, classifiers, systems):
    clf = clf + "-" + "-".join([ts, test_set])
    print >> sys.stderr, clf, s
    #print >> sys.stderr, s, clf
    if c % m == 0 and c != 0:
        print "\n"
    print "\t".join(d[s][test_set][clf])
    c += 1
