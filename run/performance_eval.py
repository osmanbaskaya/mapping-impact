#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


from pprint import pprint
from classifier import SVCWrapper
from classifier_eval import ChunkEvaluator
from logger import ChunkLogger

class Dataset(object):

    def __init__(self, data, target):
        self.data = data # 
        self.target = target


def get_gold_chunk_filename(word, chunk_path, chunk_type, n=5):
    gold_data = []
    for i in range(n):
        fn = "{}{}.chunk{}.{}.key".format(chunk_path,word,i,chunk_type)
        gold_data.append(fn)
    return gold_data

chunk_path = '../data/chunks/'
chunk_type = 'uniform'
training_word_list = ['lessing',]
tw_dict = {}
system_ans_dict = {}
system_key_folder = 'ans2/' 

dev_sys_fs = ['../data/keys/leon.key2',]
dev_gold_fs = ['ans2/leon.ans',]
devset = Dataset(dev_sys_fs[0], dev_gold_fs[0])


for tw in training_word_list:
    tw_dict[tw] = get_gold_chunk_filename(tw, chunk_path, chunk_type)
    system_ans_dict[tw] = "{}{}.ans".format(system_key_folder, tw)

w = SVCWrapper()
e = ChunkEvaluator(w, tw_dict, system_ans_dict, devset, 5, True, logger=ChunkLogger(3))
print e.score()

#for i in range(5):
    #pprint(e.gold_dict['lessing'][i])
    #print "###############\n"
    #pprint(e.system_key_dict['lessing'][i])
    #print "----\n"

