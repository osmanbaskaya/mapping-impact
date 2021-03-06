#!/usr/bin/env python

from collections import defaultdict as dd
import gzip
import re
import sys


pseudoword = sys.argv[1].replace(".kmeans.gz", "").replace('kmeans/', '')


cluster = {}
for line in gzip.open(sys.argv[1]):
    line = line.strip().split("\t")
    cluster[line[0]] = line[1]

match = re.compile("<(\w+\.test)\.([^>]+)>")
sense_counts = dd(lambda: dd(lambda: dd(int)))
for line in sys.stdin:
    line = line.strip().split("\t")
    m = match.search(line[0])
    sense_counts[m.group(1)][m.group(2)][cluster[line[1]]] += 1

for word in sense_counts.keys():
    for instance, counts in sense_counts[word].iteritems():
        print "%s %s %s" % (word,
                            word + '.' + instance,
                            ' '.join(("%s.%s/%d" % (pseudoword, x[0], x[1]) \
                            for x in counts.iteritems())))
