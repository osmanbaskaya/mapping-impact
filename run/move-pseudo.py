#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import os, shutil

out = '../data/pos-filtering/'
missing = open('dropbox-missing.txt').readlines()
files = os.listdir(out)

total = 0
for f in files:
    fn = f.rsplit('.', 2)[0]
    for m in missing:
        m = m.strip()
        if m == fn:
            total += 1
            shutil.copy(out + f, 'missing/' + f)

print total, len(missing)
assert len(missing) == (total / 5)








