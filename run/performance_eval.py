#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


from pprint import pprint
from classifier import SVCWrapper
from classifier_eval import ChunkEvaluator
from logger import ChunkLogger
from itertools import combinations, izip

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
training_word_list = ['lessing', 'leon']
tw_dict = {}
sys_ans_dict = {}
system_key_folder = 'ans2/' 

# Development data stuff
dev_sys_fs = ['../data/keys/leon.key2',]
dev_gold_fs = ['ans2/leon.ans',]
devset = Dataset(dev_sys_fs[0], dev_gold_fs[0])

w = SVCWrapper()
logger = ChunkLogger(0)
for tw in training_word_list:
    sys_ans_dict[tw] = "{}{}.ans".format(system_key_folder, tw)
    tw_dict[tw] = get_gold_chunk_filename(tw, chunk_path, chunk_types)

exp_length = len(tw_dict[training_word_list[0]])
for i in range(exp_length):
    exp = {}
    for tw in tw_dict:
        exp[tw] = tw_dict[tw][i]
    print "Experiment %d" % (i+1),
    print [tt.rsplit('.', 3)[1:3] for tt in exp[tw]]
    e = ChunkEvaluator(w, exp, sys_ans_dict, devset, 5, False, logger=logger)
    print e.score()





