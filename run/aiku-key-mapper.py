#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

""" dosya adini ilk sutuna, orta sutuna arayip bularak keys/foo.key dosyasinda. """

import sys 
import os
import re

ans_f = sys.argv[1]
gold_f = sys.argv[2]

word = os.path.basename(gold_f).rsplit('.', 1)[0]
out_f = open('ans2/%s.ans' % word, 'w')

ans_regex = re.compile('(\w+)\.test\.(\d+)')
gold_reg = '{}\.line-\d+\.inst-{}'
ss = []

g_lines = open(gold_f).read()
for a_line in open(ans_f):
    m = ans_regex.search(a_line)
    psense, inst_id = m.group(1), m.group(2)
    m = re.search(gold_reg.format(psense, inst_id), g_lines)
    ginst_id = m.group(0)
    ss.append("{} {} {}\n".format(word, ginst_id, ' '.join(a_line.split()[2:])))

out_f.write(''.join(ss))
out_f.close()
