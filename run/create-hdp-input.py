#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys 
import os
import gzip
import re

test_path = 'twitter-sentence/test/'
train_path = 'twitter-sentence/train/'

out = 'hdp-wsi/wsi_input/example/'
all_fold = out + 'all/'
num_file_name = out + 'num_test_instances.all.txt'

def fetch(path, comps):
    all_lines = []
    for comp in comps:
        fn = path + comp + '.gz'
        if os.path.exists(fn):
            lines = gzip.open(fn).readlines()
            all_lines.extend(lines)

    return (all_lines, len(all_lines))

def replace(base, test, train):
    test.extend(train)
    return re.sub('<\w+\..*\d+>', '{}'.format(base), ''.join(test))

num_file = open(num_file_name, 'w')
for line in open(sys.argv[1]):
    line = line.split()
    base, comps = line[0], line[1:]
    base = base[1:-1]
    base = base.replace("'", "")
    seen = {}
    test_insts, test_total = fetch(test_path, comps)
    train_insts, train_total = fetch(train_path, comps)
    num_file.write("{}.n {}\n".format(base, test_total))
    fn = "{}{}.n.lemma".format(all_fold, base)
    pseudoword_file = open(fn, 'w')
    s = replace(base, test_insts, train_insts)
    #FIXME: HDP Sorun cikartiyor alttaki satir olmadiginda. HDP tarafinda fixle
    pseudoword_file.write(s.replace('#', '*'))
    pseudoword_file.close()



