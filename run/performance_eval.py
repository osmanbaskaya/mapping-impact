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

training_word_list = sys.argv[1:]

chunk_types = ['semcor', 'uniform', 'random', 'hybrid'] 
chunk_path = '../data/chunks/'
tw_dict = {}
sys_ans_dict = {}

system_key_folder = 'hdp-ans/' 
system_out_dir = 'def-map-hdp'

# Development data stuff
#dev_sys_fs = ['../data/keys/leon.key2',]
#dev_gold_fs = ['ans2/leon.ans',]
#devset = mapping_utils.Dataset(dev_sys_fs[0], dev_gold_fs[0])
devset = []

wrappers = [
            #DecisionTreeWrapper(), 
            SVCWrapper(), 
            #BernoulliNBWrapper(), 
            #MultinomialNBWrapper()
           ]

logger = ChunkLogger(3)
#training_word_list = [
                      #'horne', 
                      #'adams_apple', 
                      #'loot', 
                      #'para'
                     #]
for tw in training_word_list:
    sys_ans_dict[tw] = "{}{}.ans".format(system_key_folder, tw)
    tw_dict[tw] = mapping_utils.get_gold_chunk_filename(tw, chunk_path, chunk_types)

exp_length = len(tw_dict[training_word_list[0]])
logger.info("Evaluation started for %s" % system_key_folder)

print "Total pseudowords: %d" % len(training_word_list)
for w in wrappers:
    results = dd(list)
    predictions = dd(list)
    for i in range(exp_length):
        exp = {}
        for tw in tw_dict:
            exp[tw] = tw_dict[tw][i]
        #print "Experiment %d" % (i+1),

        exp_name = mapping_utils.get_exp_name(exp, tw, w.name)
        e = ChunkEvaluator(w, exp, sys_ans_dict, devset, False, logger=logger)
        score, prediction = e.score_and_predict()
        print exp_name
        #print
        #print "Score is:", score
        #print
        #pprint( prediction['horne'][:5] )
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
    mapping_utils.write_prediction2file(predictions, system_out_dir)
