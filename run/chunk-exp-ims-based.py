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
tw_dict = {}
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
devfiles = sys.argv[10:] # development files
gold_dev = [os.path.join(gold_dir, f + '.key') for f in devfiles]
sys_dev = ["{}{}.ans".format(system_key_folder, tw) for tw in devfiles]

wrappers = [
            SVCWrapper('SVM_Linear', kernel='linear', C=1), 
            SVCWrapper('SVM_Gaussian', kernel='rbf', C=1, gamma=0), 
            DecisionTreeWrapper("DecisionTree-Gini", criterion='gini'), 
            DecisionTreeWrapper("DecisionTree-Entropy", criterion='entropy'), 
            BernoulliNBWrapper(), 
            MultinomialNBWrapper()
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
processed = training_word_list[start:end]
for tw in processed:
    ans_file = "{}{}.ans".format(system_key_folder, tw)
    if tw not in set(devfiles):
        sys_ans_dict[tw] = ans_file
        tw_dict[tw] = mapping_utils.get_gold_chunk_filename(tw, chunk_path, chunk_types)

devset = [sys_dev, gold_dev]
exp_length = len(tw_dict[processed[0]])
optimization = False

IMS_path = "ims-training-data/has-{}-instances".format(num_inst_in_training)
inst_num_d = mapping_utils.get_ims_training_set_size(tw_dict.keys(), chunk_types, IMS_path)
#print tw_dict["advocate"]

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
    predictions = dd(list)
    for i in range(exp_length):
        exp = {}
        for tw in tw_dict:
            exp[tw] = tw_dict[tw][i]
        #print "Experiment %d" % (i+1),

        out = os.path.join(system_out_dir, w.name)
        if not os.path.exists(out):
            os.mkdir(out)

        exp_name, ta, te = mapping_utils.get_exp_name(exp, tw, w.name, exp_part)
        #FIXME 2 kere run ediyor
        if te != ta: # Distribution of the test and training should be the same.
            continue
        inst = inst_num_d[ta]
        print system_out_dir, exp_name, ta, te, exp['aa'][-1]
        e = IMSBasedChunkEvaluator(w,exp,sys_ans_dict,devset,inst,optimization,logger)
        score, prediction = e.score_and_predict()
        num_pw = len(score.keys())
        avg_score = sum([s[0] for s in score.values()]) / num_pw
        avg_perp = sum([s[1] for s in score.values()]) / num_pw
        results[exp_name].append(avg_score)
        predictions[exp_name].append(prediction)

    cross_res = [sum(res) / len(res) for res in results.values()]
    mapping_utils.write_prediction2file(predictions, out)
