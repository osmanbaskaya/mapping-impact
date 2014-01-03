#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
ensemble-ans/ directory needs to be filled with the ensemble ans 
files. So this module does that very well.  
Important: Assuming that

"""

import sys
import os

pw_set = set(open(sys.argv[1]).read().split())
system_dirs = sys.argv[2:]

def create_system_dicts(f):
    d = {}
    for line in f:
        line = line.split()
        key = line[0] + '___' + line[1]
        d[key] = line[2:]

    return d

def write2file(pw):
    print >> sys.stderr, pw, "is processing"
    out = "ensemble-ans/{}.ans".format(pw)
    f = open(out, 'w')
    key_files = map(open, [os.path.join(d, pw) + ".ans" for d in system_dirs])
    system_dicts = map(create_system_dicts, key_files)
    for key in system_dicts[0].keys():
        sline = []
        sline.extend(key.split("___"))
        for i, d in enumerate(system_dicts):
            for j in xrange(len(d[key])):
                sline.append("s%d-" %i + d[key][j])
        f.write(" ".join(sline))
        f.write("\n")
    f.close()

for pw in pw_set:
    write2file(pw)
