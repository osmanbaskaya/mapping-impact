#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import cross_validation
from feature_transform import CountTransformer
from data_load import SemevalKeyLoader
import sys
from optparse import OptionParser
import numpy as np
from nlp_utils import ColorLogger


"""
This scripts is used to test various mapping procedures. Now it supports
two different test set formats (Semeval2013, Semeval2010) but other 
formats can be added in data_load module.



"""

__all__ = ['Evaluator', 'SemevalKeyLoader']

parser = OptionParser()
parser.add_option("-i", "--ans_file", dest="ansfile", default=None,
                  help="System's Answer file", metavar="System File")
parser.add_option("-g", "--key_file", dest="keyfile", default=None,
                  help="gold dataset file", metavar="GOLD")
parser.add_option("-k", "--num_fold", dest="k", default=None,
        help="k in k-Fold Cross validation", metavar="TYPE")
parser.add_option("-s", "--seed", dest="seed", default=None,
        help="SEED Value", metavar="SEED")
parser.add_option("-d", "--debug", dest="debug_level", default=0,
        help="Debug Level for logger", metavar="DEBUG_LEVEL")
#parser.add_option("-l", "--key_loader", dest="loader", default=None,
        #help="Key Loader type: semeval | dummy", metavar="KEY_LOADER")

#mandatories = ['keyfile', 'k', 'ansfile']
mandatories = []

def input_check(opts, mandatories):
    """ Making sure all mandatory options appeared. """ 
    run = True
    for m in mandatories:
        if not opts.__dict__[m]: 
            print >> sys.stderr, "mandatory option is missing: %s" % m
            run = False
    if not run:
        print >> sys.stderr
        parser.print_help()
        exit(-1)

#(opts, args) = parser.parse_args() 
#input_check(opts, mandatories)
#keyfile = opts.keyfile
#ansfile = opts.ansfile
#k = int(opts.k)
#debug_level = int(opts.debug_level)

debug_level = 1

class Evaluator(object):

    def __init__(self, cls_wrapper, ansfile, keyfile, devfile, k, 
                optimization, key_loader, feature_transformer, logger):
        self.ansfile = ansfile
        self.keyfile = keyfile
        self.devfile = devfile
        self.k = k # k in k-fold cross validation
        self.optimization = optimization # parameter optimization true/false
        self.key_loader = key_loader
        self.feature_transformer = feature_transformer
        self.logger = logger
        if logger is None:
            self.logger = ColorLogger(debug_level)
        self.cls_wrapper = cls_wrapper

    def load_key_files(self):
        ans_dict = self.key_loader.read_keyfile(self.ansfile)
        gold_dict = self.key_loader.read_keyfile(self.keyfile)
        return ans_dict, gold_dict

    def report(self):
        """This method provides evaluator's details to stderr"""
        raise NotImplementedError
        
class SemevalEvaluator(Evaluator):
    
    def __init__(self, cls_wrapper, ansfile, keyfile, devfile, k, optimization):
        super(SemevalEvaluator, self).__init__(cls_wrapper, ansfile, keyfile, 
                devfile, k, optimization, SemevalKeyLoader(), CountTransformer(), None)


#X, vec = semeval_feature_transform(ans_dict['add.v'])
#print X[:10]
#print vec.get_feature_names()
print debug_level
#exit()



# onemli
#classifiers = [svm.SVC, MultinomialNB,]
#m, n = len(classifiers), len(gold_dict.keys())
#results = np.zeros([m,n])
#stds = np.zeros([m,n])

#kfolds = dict()

#for i, c in enumerate(classifiers):
    #for j, tw in enumerate(gold_dict.keys()):
        #data = ans_dict[tw]
        #X = data.reshape(data.shape[0], 1)
        #Y = gold_dict[tw]
        #clf = c()
        #cv = cross_validation.ShuffleSplit(len(Y), n_iter=k,
                    #test_size=0.2, random_state=0)
        #scores = cross_validation.cross_val_score(clf, X, Y, cv=k)
        #results[i,j], stds[i,j] = scores.mean(), scores.std()

