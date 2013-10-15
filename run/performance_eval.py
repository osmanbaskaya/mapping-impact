#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


from pprint import pprint
from collections import defaultdict as dd
from classifier import SVCWrapper
from classifier_eval import ChunkEvaluator
from logger import ChunkLogger
from itertools import combinations, izip
import sys

training_word_list = sys.argv[1:]
print "Total pseudowords: %d" % len(training_word_list)

class Dataset(object):

    def __init__(self, data, target):
        self.data = data # 
        self.target = target

def get_gold_chunk_filename(word, chunk_path, types):
    gold_data = []
    form = "{}{}.chunk{}.{}.key"
    for train_type in types:
        for test_type in types:
            for train_idx, test_id in izip(combinations(range(5), 4), range(4,-1,-1)):
                g = []
                for tidx in train_idx:
                    fn = form.format(chunk_path, word, tidx, train_type)
                    g.append(fn)
                g.append(form.format(chunk_path, word, test_id, test_type))
                gold_data.append(g)
    return gold_data

chunk_types = ['semcor', 'uniform', 'random', 'hybrid'] 
chunk_path = '../data/chunks/'
training_word_list = ['horne']
tw_dict = {}
sys_ans_dict = {}
system_key_folder = 'ans3/' 

# Development data stuff
#dev_sys_fs = ['../data/keys/leon.key2',]
#dev_gold_fs = ['ans2/leon.ans',]
#devset = Dataset(dev_sys_fs[0], dev_gold_fs[0])
devset = []

w = SVCWrapper()
logger = ChunkLogger(3)
for tw in training_word_list:
    sys_ans_dict[tw] = "{}{}.ans".format(system_key_folder, tw)
    tw_dict[tw] = get_gold_chunk_filename(tw, chunk_path, chunk_types)

exp_length = len(tw_dict[training_word_list[0]])
results = dd(list)
logger.info("Evaluation started")
for i in range(exp_length):
    exp = {}
    for tw in tw_dict:
        exp[tw] = tw_dict[tw][i]
    #print "Experiment %d" % (i+1),
    detail = [tt.rsplit('.', 3)[1:3] for tt in exp[tw]]
    tr, te = detail[0][1], detail[-1][1]
    chunk = "%s-%s-%s" % (tr, te, detail[-1][0])
    #pprint( exp )
    e = ChunkEvaluator(w, exp, sys_ans_dict, devset, 5, False, logger=logger)
    score, prediction = e.score_and_predict()
    print chunk
    print
    print score
    print
    pprint( prediction['horne'][:5] )
    num_pw = len(score.keys())
    total_score = sum([s[0] for s in score.values()])
    total_perp = sum([s[1] for s in score.values()])
    results[chunk].append(total_score)
    print "ChunkScore:", chunk, total_score, total_perp / num_pw

#pprint(results)
cross_res = [sum(res) / len(res) for res in results.values()]
pprint( zip(results.keys(), cross_res) )


