#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
import gzip

inp = '../data/pos-filtering/%s.tok.gz'

curr = ""
c = 1
f = None
for line in sys.stdin:
    tw, ln, offset = line.split()
    ln = int(ln) - 1
    offset = int(offset)
    if curr != tw:
        curr = tw
        c = 1
        f = gzip.open(inp % tw)
        lines = f.readlines()
    ll = lines[ln]
    ll = ll.split()
    print "%s <%s.test.%d> %s" % (' '.join(ll[offset-3:offset]), tw, c, 
                                      ' '.join(ll[offset+1:offset+4]))
    c += 1
