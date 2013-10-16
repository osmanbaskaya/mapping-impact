#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys
import re
from collections import defaultdict as dd
from itertools import cycle

""" all/ folder contains the only test instances """

#<lava.line-2.inst-2> 

ans_file = sys.argv[1]
path = "hdp-wsi/wsi_input/example/all/%s.n.lemma"
out = 'hdp-twitter-ans/'

regex = re.compile("<\w+\.line-\d+\.inst-\d+>")
d = dd(list)
for line in open(ans_file):
    line = line.split()
    base = line[0][:-2] # removing '.n'
    senses = line[2:]
    d[base].append(' '.join(senses))

for key in d:
    instance_ids = regex.findall(open(path % key).read())
    assert len(instance_ids) % 300 == 0
    elements = zip(cycle([key]), instance_ids, d[key])
    lines = '\n'.join([' '.join(e) for e in elements])
    with open(out + key + '.ans', 'w') as f:
        f.write(lines)
        f.write('\n')


