#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
from itertools import izip, combinations
import os
from collections import defaultdict as dd

def get_exp_name(exp, tw, cls_name, exp_part):

    detail = [tt.rsplit('.', 3)[1:3] for tt in exp[tw]]
    tr, te = detail[0][1], detail[-1][1]
    #exp_name = "%s-%s-%s-%s" % (cls_name, tr, te, detail[-1][0])
    exp_name = "{}-{}-{}-{}".format(cls_name, tr, te, exp_part)
    return exp_name, tr, te

def get_ims_training_set_size(pw_list, dist_types, ims_training_path):
    d = dd(dict)
    for dtype in dist_types:
        for pw in pw_list:
            fn = "{}.{}.key".format(pw, dtype)
            counts = dd(int)
            for line in open(os.path.join(ims_training_path, fn)):
                tag = line.split()[-1]
                counts[tag] += 1
            d[dtype][pw] = counts
    return d


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

class Dataset(object):

    def __init__(self, data, target):
        self.data = data # 
        self.target = target


def write_prediction2file(predictions, out_path):

    d = dd(list)
    for exp_name, chunks in predictions.iteritems():
        for chunk in chunks:
            for tw, pred in chunk.iteritems():
                for inst_id, label in pred:
                    s = "{} {} {}".format(tw, inst_id, label)
                    d[exp_name].append(s)


    for key, val in d.iteritems():
        f = open(os.path.join(out_path, key), 'w')
        f.write('\n'.join(val))
        f.write('\n')


                
