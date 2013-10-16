#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import os

inst = "hdp-wsi/wsi_input/example/num_test_instances.all.txt"
wsi_input_folder = "hdp-wsi/wsi_input/example/all/"
key_folder = "/scratch/1/obaskaya/mapping-impact/data/twitter/keys"
existed = set([f[:-4] + ".n" for f in os.listdir(key_folder) if f.endswith('.key')])


print "Existed number of pseudoword is %d" % len(existed) 
lines = open(inst).readlines()
f = open(inst, 'w')
total = 0
for line in lines:
    ll, num = line.split()
    if ll in existed:
        f.write(line)
        total += int(num)
    else:
        if os.path.exists(wsi_input_folder + ll + '.lemma'):
            os.remove(wsi_input_folder + ll + '.lemma')

print "Total instances %d" % total
f.close()





