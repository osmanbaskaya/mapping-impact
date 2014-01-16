#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module creates pw-list.txt according to polysemy level (= sys.argv[1])
"""

import sys

polysemy_level = int(sys.argv[1])
pw_list_file = open(sys.argv[2]).read().split()
pseudoword_file = open(sys.argv[3])

for line in pseudoword_file
