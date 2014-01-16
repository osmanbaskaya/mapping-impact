#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Gold standard creator provides a gold standard file. Important to 
exclude all dev set pseudowords in the gold standard. Addition to this
gold standard file needs to contain only the common set of pseudowords
for all n systems. (that is why one of the input file is *.pw-list.txt)
"""
#ls *.uniform.key |  grep -Pv "^((activeness)|(brahms)|(bathroom)|(ashur)|(al))\."  | xargs -0 -d "\n" cat | wc 

import sys
import os

if len(sys.argv) < 5:
    msg = "Usage: {} chunk_dir common_pw_list chunk_type devset_file(s)"
    print >> sys.stderr, msg.format(sys.argv[0])
    exit(1)

key_path = sys.argv[1]
common_pseudoword_set = set(open(sys.argv[2]).read().split())
chunk_type = sys.argv[3]
devset = set(sys.argv[4:])

diff_set = common_pseudoword_set.difference(devset)
print >> sys.stderr, "Length of the pw-list:", len(common_pseudoword_set)
print >> sys.stderr, "Size of the devset:", len(devset)
print >> sys.stderr, "Size of the keyset:", len(diff_set)

num_file = 0

for pw in diff_set:
    for i in xrange(5):
        fn = "{}.chunk{}.{}.key".format(pw, i, chunk_type)
        with open(os.path.join(key_path, fn)) as f:
            num_file += 1
            for line in f:
                print line,

print >> sys.stderr, "num of file added", num_file
