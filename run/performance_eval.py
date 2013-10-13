#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


from pprint import pprint
from classifier import SVCWrapper, BernoulliNBWrapper, MultinomialNBWrapper#, MNLogitWrapper
from classifier_eval import *
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
chunk_type = 'hybrid'
training_word_list = ['lessing', 'leon',]
tw_dict = {}
system_ans_dict = {}
system_key_folder = 'ans/' 

for tw in training_word_list:
    tw_dict[tw] = get_gold_chunk_filename(tw, chunk_path, chunk_type)
    system_ans_dict[tw] = "{}{}.ans".format(system_key_folder, tw)

w = SVCWrapper()
e = ChunkEvaluator(w, tw_dict, system_ans_dict, 5, True, logger=ChunkLogger(3))
