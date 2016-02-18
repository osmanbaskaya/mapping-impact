# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"
import sys
from collections import Counter, defaultdict as dd
import os
from nlp_utils import calc_perp

key_file = sys.argv[1]

d = dd(list)
all_senses = []
total_num_instance = 0
for line in open(key_file):
    total_num_instance += 1
    word, instance_id, sense = line.split()
    d[word].append(sense)
    all_senses.append(sense)

basename = os.path.splitext(os.path.basename(key_file))[0]
print basename

with open("instance-num-%s.txt" % basename, 'w') as f:
    f.write("{}\t{}\t{}\t{}\n".format("Word", "Number of Instance", "Number of Sense", 
                                      "Perplexity"))
    sense_dist = dd(int)
    for word, senses in d.iteritems():
        num_sense = len(set(senses))
        perplexity = calc_perp(senses)
        f.write("{}\t{}\t{}\t{}\n".format(word, len(senses), num_sense, perplexity))
        sense_dist[num_sense] += 1


with open("sense-dist-%s.txt" % basename, 'w') as f:
    f.write("Total # of Instance: {}\tTotal # of words: {}\n".format(total_num_instance, len(d)))
    f.write("Mean # of instance: {}\n".format(float(total_num_instance) / len(d)))
    f.write("Dataset Perplexity: {}\n".format(calc_perp(all_senses)))
    for n, c in sorted(sense_dist.items()):
        f.write("{}\t{}\n".format(n, c))
