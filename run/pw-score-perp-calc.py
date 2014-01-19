#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module calculates F1-Score and sense perplexity of each pseudoword for a given
classifier
"""

import sys
import os
from tempfile import NamedTemporaryFile
from collections import defaultdict as dd
from multiprocessing import Pool
from subprocess import Popen, PIPE
from itertools import izip
from nlp_utils import fopen, calc_perp


key_file = sys.argv[1]
gold_file = sys.argv[2]
out_path = sys.argv[3]

base = key_file.replace("../keys/", '').replace('/', '__').replace(".ans.gz", "")
print >> sys.stderr, base

score_exec = "../keys/scorer.py"

def calc_score(t):
    system_f, gold_f = t
    p1 = Popen([score_exec, system_f, gold_f], stdout=PIPE)
    s = Popen(['grep', 'F1-Score'], stdin=p1.stdout, stdout=PIPE).communicate()[0]
    return s.replace("F1-Score is", "").strip()

tw_dict = dd(list)
perp_dict = dd(list)
for line in fopen(key_file):
    L = line.split()
    tw, gold_tag = L[0], L[-1]
    tw_dict[tw].append(line)

gold_dict = dd(list)
for line in fopen(gold_file):
    L = line.split()
    tw, gold_tag = L[0], L[-1]
    perp_dict[tw].append(gold_tag)
    gold_dict[tw].append(line)


keys = tw_dict.keys()

if len(keys) != len(gold_dict.keys()):
    print >> sys.stderr, "pseudoword numbers not equal between system and gold keys"

perplexities = dict()
files = []
for key in keys:
    perplexities[key] = calc_perp(perp_dict[key])
    f_system = NamedTemporaryFile(mode='w', delete=False)
    f_gold = NamedTemporaryFile(mode='w', delete=False)
    f_system.write(''.join(tw_dict[key]))
    f_gold.write(''.join(gold_dict[key]))
    f_system.flush()
    f_gold.flush()
    files.append((f_system.name, f_gold.name)) 

pool = Pool(processes=20)
scores = pool.map(calc_score, files)

output = []
for tw, score in izip(keys, scores):
    output.append("{}\t{}\t{}".format(tw, score, perplexities[tw]))

with open(os.path.join(out_path, base), 'w') as fn:
    fn.write('\n'.join(output))
