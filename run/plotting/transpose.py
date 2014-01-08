#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys

rows = []
for line in sys.stdin:
    line = line.strip().split(',')
    rows.append(line)


for i in range(len(rows[0])):
    for row in rows:
        print row[i], '\t',
    print


