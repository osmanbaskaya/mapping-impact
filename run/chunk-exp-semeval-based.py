#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from collections import defaultdict as dd
from classifier_eval import IMSBasedChunkEvaluator
from logger import ChunkLogger
from classifier import *
from pprint import pprint
import mapping_utils
import sys
import os

tw_dict = dd(lambda: dict())
sys_ans_dict = {}

system_key_folder = sys.argv[1]
system_out_dir = sys.argv[2]
training_word_list = [line.strip() for line in open(sys.argv[3]).readlines()]
gold_dir = sys.argv[4]
chunk_path = sys.argv[5]

num_of_chunks = 5
if sys.argv[6] == 's07':
    num_of_chunks = 1

# Development data stuff
devfiles = []
if len(sys.argv) > 7:
    devfiles = sys.argv[7:] # development files
gold_dev = [os.path.join(gold_dir, f + '.key') for f in devfiles]
sys_dev = ["{}{}.ans".format(system_key_folder, tw) for tw in devfiles]

wrappers = [
            SVCWrapper('SVM_Linear', kernel='linear')
            #SVCWrapper('SVM_Gaussian', kernel='rbf', C=1, gamma=1), 
            #DecisionTreeWrapper("DecisionTree-Gini", criterion='gini'), 
            #DecisionTreeWrapper("DecisionTree-Entropy", criterion='entropy'), 
            #BernoulliNBWrapper("SVM_Linear"), 
            #MultinomialNBWrapper('SVM_Linear')
           ]

logger = ChunkLogger(3)
# quick testing
#training_word_list = [
                      #'horne', 
                      #'adams_apple', 
                      #'loot', 
                      #'parliamentarianca',
                      #'para'
                     #]

training_word_list.sort()
processed = training_word_list
training_path = chunk_path
test_path = chunk_path

def get_input_filenames(tw):
    files = []
    for i in range(num_of_chunks):
        fn = "{}.chunk{}.train.key".format(tw, i)
        train_fn = os.path.join(training_path, fn)
        test_fn = os.path.join(test_path, "{}.chunk{}.test.key".format(tw, i))
        files.append((train_fn, test_fn))
    return files

for tw in processed:
    ans_file = "{}{}.ans".format(system_key_folder, tw)
    if tw not in set(devfiles):
        sys_ans_dict[tw] = ans_file
        tw_dict[tw] = get_input_filenames(tw)


devset = [sys_dev, gold_dev]
optimization = False

## Prints all information for the experiment ###
logger.info("Evaluation started for %s" % system_key_folder)
logger.info("Total # of target words: %d" % len(processed))
logger.info("Chunk Path is: %s" % chunk_path)
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

    exp_name = "{}-{}-{}-{}".format(w.name, "semeval", "semeval", 1)
    e = IMSBasedChunkEvaluator(w,tw_dict,sys_ans_dict,devset,optimization,logger)
    prediction = e.predict_by_chunks()
    predictions[exp_name] = prediction
    logger.info("\n%s completed..." % exp_name)

    IMSBasedChunkEvaluator.write_chunk_prediction2file(predictions, out)

