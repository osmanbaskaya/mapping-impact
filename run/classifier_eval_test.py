#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from classifier_eval import SemevalEvaluator
#import sys
#from optparse import OptionParser
from itertools import izip, count
from classifier import SVCWrapper, BernoulliNBWrapper, MultinomialNBWrapper#, MNLogitWrapper
from logger import SemevalLogger
import numpy as np
from pprint import pprint


#parser = OptionParser()
#parser.add_option("-i", "--ans_file", dest="ansfile", default=None,
                  #help="System's Answer file", metavar="System File")
#parser.add_option("-g", "--key_file", dest="keyfile", default=None,
                  #help="gold dataset file", metavar="GOLD")
#parser.add_option("-k", "--num_fold", dest="k", default=None,
        #help="k in k-Fold Cross validation", metavar="TYPE")
#parser.add_option("-s", "--seed", dest="seed", default=None,
        #help="SEED Value", metavar="SEED")
#parser.add_option("-d", "--debug", dest="debug_level", default=0,
        #help="Debug Level for logger", metavar="DEBUG_LEVEL")
#parser.add_option("-l", "--key_loader", dest="loader", default=None,
        #help="Key Loader type: semeval | dummy", metavar="KEY_LOADER")

#mandatories = ['keyfile', 'k', 'ansfile']
#mandatories = []

#def input_check(opts, mandatories):
    #""" Making sure all mandatory options appeared. """ 
    #run = True
    #for m in mandatories:
        #if not opts.__dict__[m]: 
            #print >> sys.stderr, "mandatory option is missing: %s" % m
            #run = False
    #if not run:
        #print >> sys.stderr
        #parser.print_help()
        #exit(-1)

#(opts, args) = parser.parse_args() 
#input_check(opts, mandatories)
#keyfile = opts.keyfile
#ansfile = opts.ansfile
#k = int(opts.k)
#debug_level = int(opts.debug_level)

### PARAMETERS ###
#sys_fs = ['system.key',]
#gold_fs = ['gold.key',]
#dev_sys_fs = ['dev-system.key',]
#dev_gold_fs = ['dev-gold.key',]
sys_fs = ['all.key',]
gold_fs = ['all.key',]
dev_sys_fs = ['all.key',]
dev_gold_fs = ['all.key',]
k = 5
opt = True #optimization

class Dataset(object):

    def __init__(self, data, target):
        self.data = data # 
        self.target = target

wrappers = [SVCWrapper(), BernoulliNBWrapper(), MultinomialNBWrapper()]
counter = count(0)
score_matrix = np.zeros([len(sys_fs), len(wrappers)])

debug_mode = 3
for i, sys, g, dev_sys, dev_g in izip(counter, sys_fs, gold_fs, dev_sys_fs, dev_gold_fs):
    trainset = Dataset(sys, g)
    devset = Dataset(dev_sys, dev_g)
    for j, w in enumerate(wrappers):
        logger = SemevalLogger(trainset, devset, w.name, debug_mode)
        e = SemevalEvaluator(w, trainset, devset, k, optimization=opt, logger=logger)
        scores = e.score()
        pprint(scores)
        #e.report()
