#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import re
from nlp_utils import fopen, calc_perp
from collections import defaultdict as dd


sys_f = sys.argv[1]
gold_file = sys.argv[2]
dist = sys.argv[3]

perp_dict = dd(list)

for line in fopen(gold_file):
    L = line.split()
    tw, gold_tag = L[0], L[-1]
    perp_dict[tw].append(gold_tag)

regex = re.compile(".*/(.*)\.{}\.key".format(dist))

for line in fopen(sys_f):
    if line.startswith("Scores for"):
        tw = regex.match(line).group(1)
    else:
        line = line.split()
        if len(line) != 0:
            if line[0] == "F1-Score":
                f1_score = line[-1]
                print "{}\t{}\t{}".format(tw, f1_score, calc_perp(perp_dict[tw]))
