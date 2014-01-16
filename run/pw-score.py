#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import os
from subprocess import Popen, PIPE
from collections import defaultdict as dd

pw_set = set(open(sys.argv[1]).read().split())
inst_num = sys.argv[2]
devset = set(sys.argv[3:])

diff = pw_set.difference(devset)

print >> sys.stderr, len(pw_set), len(devset), len(diff)

systems = "aiku hdp cw squat ensemble".split()
dists = "semcor uniform".split()

score_exec = "../keys/scorer.py"

system_key = "../keys/{}/mapped/gigaword/default/SVM_Linear-{}-{}.ans.gz"
gold_key = "../keys/gold/gigaword.{}.key"

#score = """{} word.key.tmp gold.key.tmp | grep -P "F1-Score is" | awk '{{print $3}}' """
#score = score.format(score_exec)

word_out = "word{}.key.tmp".format(inst_num)
gold_out = "gold{}.key.tmp".format(inst_num)

s1 = 'zcat {} | grep -P "^{} \\w+" > {}'
g1 = 'cat {} | grep -P "^{} \\w+" > {}'


d = dd(lambda : dd(lambda: dd(str)))
for system in systems:
    print >> sys.stderr, system
    for pw in diff:
        for dist in dists:
            #print pw
            s = system_key.format(system, dist, dist)
            g = gold_key.format(dist)
            process = s1.format(s, pw, word_out)
            os.system(process)
            process = g1.format(g, pw, gold_out)
            os.system(process)
            p1 = Popen([score_exec, word_out, gold_out], stdout=PIPE)
            score = p1.communicate()[0].split()[-1]
            d[system][dist][pw] = score

for dist in dists:
    print '\n', dist, '\n'
    for pw in diff:
        print pw, '\t',
        for system in systems:
            print d[system][dist][pw], '\t',
        print 
