#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import sys, os
import errno


dataset = sys.argv[3]
if dataset != "gigaword":
    system = sys.argv[1] + "-%s-chunk-keys" % dataset
else:
    system = sys.argv[1] + "-chunk-keys"

inst_num = sys.argv[4] # 10 25 ... 750
system = os.path.join(system, inst_num)
typ = sys.argv[2] # tuned or default
classifiers = os.listdir(system)
distribution_type = "semcor uniform".split() # training and testing is the same dist. 

directory = "../keys/{}/mapped/{}/{}/{}".format(sys.argv[1], sys.argv[3], typ, inst_num)
try:
    os.makedirs(directory)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

process = ""
form = "cat {}/{}/*{}-{}* | gzip > ../keys/{}/mapped/{}/{}/{}/{}-{}-{}.ans.gz & "

print >> sys.stderr, system, dataset, typ

for c in classifiers:
    for d in distribution_type:
            process += form.format(system, c, d, d, sys.argv[1], sys.argv[3], typ, inst_num, c, d, d)

os.system(process + " wait")
