#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

""" Evaluation suite for chunking experiments.  """

import sys
import os
from multiprocessing import Pool
from subprocess import Popen, PIPE

def calc_score(pair):
    f, gold = pair
    return Popen([score_exec, f, gold], stdout=PIPE).communicate()[0]

if len(sys.argv) != 5:
    msg = "Usage: {} system mapped/induced gigaword/twitter default/tuned"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(1)

gold_form = "../keys/gold/{}.{}.key"
score_exec = "../keys/scorer.py"

system = sys.argv[1]
typ = sys.argv[2]
corpus = sys.argv[3]
cls = sys.argv[4] # classifiers are tuned or default (no tuning)

key_path = "../keys/{}/{}/{}/{}/".format(system, typ, corpus, cls)

pool = Pool(processes=16)

pairs = []
print >> sys.stderr, "Key path:", key_path
for res in os.listdir(key_path):
    test_set = res.rsplit('-', 1)[-1].split('.')[0]
    gold = gold_form.format(corpus, test_set)
    pairs.append((key_path + res, gold))

print ''.join(pool.map(calc_score, pairs))
