#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys

pseudowords = set(open(sys.argv[1]).readlines())

for word in pseudowords:
    word = word.replace('.', '')
    print word,


