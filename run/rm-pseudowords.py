#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

pseudowords_line = open("pseudoword-samples/pseudowords.998-count.txt").readlines()
exclude = [line.split()[0] for line in open('exclude3.txt').readlines()]

for line in pseudowords_line:
    components = line.split()[1:]
    for c in components:
        all_clear = True
        if c in exclude:
            all_clear = False
            break
    if all_clear:
        print line,

