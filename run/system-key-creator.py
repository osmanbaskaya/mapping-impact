#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Create key file for the system according to a gold standard. That is,
the system key file contains only the instances in gold standard
It is important for the evaluation (especially precision)
"""

import sys

gold_file = open(sys.argv[1])

def create_key_dict(f):
    d = {}
    for i, line in enumerate(f):
        pline = line.split()
        try: 
            key = pline[0] + '__' + pline[1]
        except:
            print >> sys.stderr, "Error in line:", i, pline, f
            exit(1)
        d[key] = line.strip()
    return d

system_dict = create_key_dict(sys.stdin)
gold_dict = create_key_dict(gold_file)

for key in gold_dict.viewkeys():
    print system_dict[key]
