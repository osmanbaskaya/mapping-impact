#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nltk.stem.wordnet import WordNetLemmatizer
import sys

lmtzr = WordNetLemmatizer()

for line in sys.stdin:
    print ' '.join(map(lmtzr.lemmatize, line.split()))




