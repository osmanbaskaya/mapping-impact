#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys

__author__ = "Osman Baskaya"


if len(sys.argv) != 3:
    print >> sys.stderr, "Usage {} system_ans_file gold_file".format(sys.argv[0])
    exit()


s_file = sys.argv[1]
g_file = sys.argv[2]

system = {}
gold = {}

def load_key(filename):
    d = {}
    total_line = 0
    for line in open(filename):
        total_line += 1
        tw, inst_id, sense = line.split()
        key = "{}__{}".format(tw, inst_id)
        d[key] = sense

    return (d, total_line)

system, sys_line = load_key(s_file) # system key
gold, gold_line = load_key(g_file) # gold key

common_set = set(system.keys()).intersection(set(gold.keys()))
true_pos = 0
for c in common_set:
    if system[c] == gold[c]:
        true_pos += 1

precision = true_pos / sys_line
recall = true_pos / gold_line
print '\nScores for system_file: "{}" \t gold_file: "{}"'.format(s_file, g_file)
print "\tPrecision is {} ({} correct of {} attempted)".format(precision, true_pos, sys_line)
print "\tRecall is {} ({} correct of {} attempted)".format(recall, true_pos, gold_line)
print "\tF1-Score is {}\n".format((2 * precision * recall) / (precision + recall))





