#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module is for using our mapping functions (SVM linear etc.) on different data sets.
Chunks are not given or specified; module uses sklearn cross validation chunks.
"""

from collections import defaultdict as dd
from classifier_eval import CVBasedEvaluator
from logger import ChunkLogger
from classifier import *
import sys
import os

sys_ans_dict = {}

system_key_folder = sys.argv[1]
system_out_dir = sys.argv[2]
training_word_list = [line.strip() for line in open(sys.argv[3]).readlines()]
gold_dir = sys.argv[4]
exp_part = sys.argv[5]
start = int(sys.argv[6])
end = int(sys.argv[7])

# Development data stuff
devfiles = sys.argv[8:] # development files
gold_dev = [os.path.join(gold_dir, f + '.key') for f in devfiles]
sys_dev = ["{}{}.ans".format(system_key_folder, tw) for tw in devfiles]

wrappers = [
            SVCWrapper('SVM_Linear', kernel='linear', C=1), 
            #SVCWrapper('SVM_Gaussian', kernel='rbf', C=1, gamma=0), 
            #DecisionTreeWrapper("DecisionTree-Gini", criterion='gini'), 
            #DecisionTreeWrapper("DecisionTree-Entropy", criterion='entropy'), 
            #BernoulliNBWrapper(), 
            #MultinomialNBWrapper()
           ]

logger = ChunkLogger(3)
# quick testing
#training_word_list = [
                      #'horne', 
                      #'adams_apple', 
                      #'loot', 
                      #'para'
                     #]

training_word_list.sort()
processed = training_word_list[start:end]
for tw in processed:
    ans_file = "{}.ans".format(os.path.join(system_key_folder, tw))
    gold_file = "{}.key".format(os.path.join(gold_dir, tw))
    if tw not in set(devfiles):
        sys_ans_dict[tw] = (ans_file, gold_file)

devset = [sys_dev, gold_dev]
exp_length = len(sys_ans_dict)
optimization = False

### Prints all information for the experiment ###
logger.info("Evaluation started for %s" % system_key_folder)
logger.info("Total pseudowords: %d" % len(processed))
logger.info("Dev. set: %s" % devset[0])
logger.info("Gold Dev. set: %s" % devset[1])
logger.info("Optimization: %s" % optimization)
logger.info("Gold key directory: %s" % gold_dir)
logger.info("Number of classifiers: %d" % len(wrappers))

for w in wrappers:
    results = dd(list)
    predictions = dict()

    out = os.path.join(system_out_dir, w.name)
    if not os.path.exists(out):
         os.mkdir(out)

    exp_name = "{}-{}-{}-{}".format(w.name, "on", "on", exp_part)
    e = CVBasedEvaluator(w, sys_ans_dict, devset, optimization, logger)
    prediction = e.predict()
    predictions[exp_name] = prediction
    logger.info("\n%s completed..." % exp_name)

    CVBasedEvaluator.write_chunk_prediction2file(predictions, out)

