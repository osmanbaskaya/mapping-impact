#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


from pprint import pprint
from collections import defaultdict as dd
from classifier_eval import ChunkEvaluator
from logger import ChunkLogger
from classifier import *
import mapping_utils
import sys
import os

training_word_list = [line.strip() for line in open(sys.argv[6]).readlines()]

chunk_types = ['semcor', 'uniform', 'random', 'hybrid'] 
#chunk_types = ['uniform', 'hybrid'] 
chunk_path = '../data/chunks/'
tw_dict = {}
sys_ans_dict = {}

#system_key_folder = 'hdp-ans/' 
#system_out_dir = 'def-map-hdp'
#exp_part = 1

system_key_folder = sys.argv[1]
system_out_dir = sys.argv[2]
exp_part = sys.argv[3]
start = int(sys.argv[4])
end = int(sys.argv[5])

# Development data stuff
system_devset_dir = '{}-dev/'.format(system_key_folder.split('-')[0])
gold_dir = "gold/gigaword/"

devfiles = 'activeness brahms bathroom appleton ashur'.split()

sys_dev = [system_devset_dir + f + ".ans" for f in devfiles]
gold_dev = [gold_dir + f + '.gold' for f in devfiles]

devset = [sys_dev, gold_dev]

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
                      #'para'
                     #]

training_word_list.sort()
processed = training_word_list[start:end]
for tw in processed:
    sys_ans_dict[tw] = "{}{}.ans".format(system_key_folder, tw)
    tw_dict[tw] = mapping_utils.get_gold_chunk_filename(tw, chunk_path, chunk_types)

exp_length = len(tw_dict[processed[0]])
logger.info("Evaluation started for %s" % system_key_folder)
optimization = True
print "Total pseudowords: %d" % len(processed)
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

        exp_name, test_chunk = mapping_utils.get_exp_name(exp, tw, w.name, exp_part)
        if test_chunk not in ['semcor', 'uniform']:
            continue

        e = ChunkEvaluator(w, exp, sys_ans_dict, devset, optimization, logger=logger)
        score, prediction = e.score_and_predict()
        print system_out_dir, exp_name
        num_pw = len(score.keys())
        avg_score = sum([s[0] for s in score.values()]) / num_pw
        avg_perp = sum([s[1] for s in score.values()]) / num_pw
        results[exp_name].append(avg_score)
        predictions[exp_name].append(prediction)
        #print "ChunkScore:", exp_name, total_score, total_perp / num_pw

    #pprint(predictions)
    cross_res = [sum(res) / len(res) for res in results.values()]
    #pprint( zip(results.keys(), cross_res) )
    #mapping_utils.write_prediction2file(predictions, "def-map-aiku/")
    mapping_utils.write_prediction2file(predictions, out)
