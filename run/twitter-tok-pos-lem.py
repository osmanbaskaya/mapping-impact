#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import os
import sys

filename = sys.argv[1]

inp = "cat {} | cut -f2- "
awk = """awk '{print $0, "</s>"}'"""
tagger = "../bin/tree-tagger/cmd/tree-tagger-english"
token2sent = "./twitter-token2sent.py {}"

process = " | ".join([inp.format(filename), awk, tagger, token2sent.format(filename)])
os.system(process)
