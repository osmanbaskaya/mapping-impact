#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import os
import gzip

inp = os.path.join(sys.argv[1], "%s.tok.gz")

curr = ""
f = None
for line in sys.stdin:
    inst, tw, ln, offset = line.split()
    ln = int(ln) - 1
    offset = int(offset)
    if curr != tw:
        curr = tw
        f = gzip.open(inp % tw)
        lines = f.readlines()
    ll = lines[ln]
    ll = ll.split()
    print "{} <{}> {}".format(' '.join(ll[:offset]), inst,
                                      ' '.join(ll[offset+1:]))
