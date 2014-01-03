#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Key creator for ensemble system.
Important: Program assumes all instances are the same for all systems.

"""

import sys

key_files = map(open, sys.argv[1:])

def create_system_dicts(f):
    d = {}
    for line in f:
        line = line.split()
        key = line[0] + '___' + line[1]
        d[key] = line[2:]

    return d

system_dicts = map(create_system_dicts, key_files)

for key in system_dicts[0].keys():
    sline = []
    sline.extend(key.split("___"))
    for i, d in enumerate(system_dicts):
        for j in xrange(len(d[key])):
            sline.append("s%d-" %i + d[key][j])
    print " ".join(sline)
