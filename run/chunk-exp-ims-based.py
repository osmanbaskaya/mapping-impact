#! /usr/bin/python
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

chunk_types = ['semcor', 'uniform']
tw_dict = dd(lambda: dict())
sys_ans_dict = {}

#system_key_folder = 'hdp-ans/' 
#system_out_dir = 'def-map-hdp'
#exp_part = 1

system_key_folder = sys.argv[1]
system_out_dir = os.path.join(sys.argv[2], sys.argv[6])
training_word_list = [line.strip() for line in open(sys.argv[3]).readlines()]
gold_dir = sys.argv[4]
chunk_path = sys.argv[5]
num_inst_in_training = int(sys.argv[6])
exp_part = sys.argv[7]
start = int(sys.argv[8])
end = int(sys.argv[9])

# Development data stuff
devfiles = []
if len(sys.argv) > 10:
    devfiles = sys.argv[10:] # development files
gold_dev = [os.path.join(gold_dir, f + '.key') for f in devfiles]
sys_dev = []#["{}{}.ans".format(system_key_folder, tw) for tw in devfiles]

wrappers = [
            SVCWrapper('SVM_Linear', kernel='linear', C=1), 
            #SVCWrapper('SVM_Gaussian', kernel='rbf', C=729, gamma=1), 
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
                      #'parliamentarianca',
                      #'para'
                     #]
#inst_d = mapping_utils.get_ims_training_instances(tw_dict.keys(), chunk_types, IMS_path)

training_word_list.sort()
processed = training_word_list[start:end]
training_path = "ims-training-data/has-{1}-instances".format(num_inst_in_training)
test_path = "ims-test-data/"

def get_input_filenames(tw, ch_type):
    #preliminary.semcor.train.all-but-0.k-10.key
    #lully.uniform.test.4.xml
    files = []
    for i in range(5):
        fn = "{}.{}.train.all-but-{}.k-{}.key".format(tw, ch_type, i, num_inst_in_training)
        train_fn = os.path.join(training_path, fn)
        test_fn = os.path.join(test_path, "{}.{}.test.{}.key".format(tw, ch_type, i))
        files.append((train_fn, test_fn))
    return files

for tw in processed:
    ans_file = "{}{}.ans".format(system_key_folder, tw)
    if tw not in set(devfiles):
        sys_ans_dict[tw] = ans_file
        for ch_type in chunk_types:
            tw_dict[ch_type][tw] = get_input_filenames(tw, ch_type)

devset = [sys_dev, gold_dev]
optimization = False

## Prints all information for the experiment ###
logger.info("Evaluation started for %s" % system_key_folder)
logger.info("Total pseudowords: %d" % len(processed))
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

    for ch_type in chunk_types:
        exp_name = "{}-{}-{}-{}".format(w.name, ch_type, ch_type, exp_part )
        data = tw_dict[ch_type]
        e = IMSBasedChunkEvaluator(w,data,sys_ans_dict,devset,optimization,logger)
        prediction = e.predict()
        predictions[exp_name] = prediction

    logger.info("\n%s completed..." % exp_name)

    #IMSBasedChunkEvaluator.write_prediction2file(predictions, out)

