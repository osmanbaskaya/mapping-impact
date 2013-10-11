#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys, os

files = sys.argv[1:-1]
out = sys.argv[-1]

for f in files:
    fn = os.path.basename(f).replace('tsv', 'raw.gz')
    process = "cat {} | cut -f2- | gzip > {}".format(f, os.path.join(out,fn))
    os.system(process)

