#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Given directory needs to be filled with the ensemble ans 
files. So this module does that very well.  
"""

import sys
import os

pw_set = set(open(sys.argv[1]).read().split())
gold_f = sys.argv[2]
out_dir = sys.argv[3]
system_dirs = sys.argv[4:]

print >> sys.stderr, sys.argv

def create_system_dicts(f):
    d = {}
    for line in f:
        line = line.split()
        key = line[0] + '___' + line[1]
        d[key] = line[2:]
    return d

def write2file(pw):
    print >> sys.stderr, pw, "is processing"
    out = "{}/{}.ans".format(out_dir, pw)
    f = open(out, 'w')
    files = [os.path.join(d, pw) + ".ans" for d in system_dirs]
    key_files = map(lambda fn: open(fn),  [fn for fn in files if os.path.isfile(fn)])
    system_dicts = map(create_system_dicts, key_files)
    keys = create_system_dicts(open(gold_f)).keys()
    for key in keys:
        sline = []
        sline.extend(key.split("___"))
        for i, d in enumerate(system_dicts):
            if key in d:
                for j in xrange(len(d[key])):
                    sline.append("s%d-" %i + d[key][j])
        if len(sline) < 3:
            continue # skip if there is no answer from any system
        f.write(" ".join(sline))
        f.write("\n")
    f.close()

for pw in pw_set:
    write2file(pw)
