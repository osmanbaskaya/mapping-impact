#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from feature_transform import SemevalFeatureTransformer
from data_load import SemevalKeyLoader
import sys
from optparse import OptionParser
from sklearn import cross_validation
from logger import SemevalLogger


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

class Evaluator(object):

    def __init__(self, cls_wrapper, ansfile, keyfile, devfile, k, 
                optimization, key_loader, ft, logger):
        self.ansfile = ansfile
        self.keyfile = keyfile
        self.devfile = devfile
        self.k = k # k in k-fold cross validation
        self.optimization = optimization # parameter optimization true/false
        self.key_loader = key_loader
        self.ft = ft #feature transformer
        self.logger = logger
        if logger is None:
            self.logger = SemevalLogger(3)
        self.cls_wrapper = cls_wrapper
        
        self.X = None
        self.Y = None
        self.X_dev = None

    def load_key_files(self):
        files = [self.ansfile, self.keyfile, self.devfile]
        return map(self.key_loader.read_keyfile, files)
    
    #def convert_data(self):
        #"""This method makes preprocessing steps and set test_set, training_set
        #development_set parameters"""
        #raise NotImplementedError

    def report(self):
        """This method provides evaluator's details to stderr"""
        raise NotImplementedError
        
class SemevalEvaluator(Evaluator):
    
    def __init__(self, cls_wrapper, ansfile, keyfile, devfile, k, optimization, logger): 
        super(SemevalEvaluator, self).__init__(cls_wrapper, ansfile, keyfile, 
              devfile, k, optimization, SemevalKeyLoader(), 
              SemevalFeatureTransformer(weighted=False), logger=logger)
        logger.info(self)

    def score(self):
        scores = {}
        cls = self.cls_wrapper.classifier
        ans_dict, gold_dict, dev_dict = self.load_key_files()
        for tw, val in ans_dict.iteritems():
            Y = gold_dict[tw]
            X =  self.ft.convert_data(val)

            cv = cross_validation.ShuffleSplit(len(Y), n_iter=self.k,
                        test_size=0.2, random_state=0)
            #FIXME: debug argument missing
            self.logger.info('\nCross Validation:' + str([i for i in cv]))
            try:
                score = cross_validation.cross_val_score(cls, X, Y, cv=cv)
            except ValueError, e: # all instances are belongs to the same class
                self.logger.warning("{}\t{}".format(tw, e))
            scores[tw] = score
        return scores

    def report(self):
        pass

    def __str__(self):
        return "SemevalEvaluator:k={}, optimization={}, key_loader={}, \
        feature_transformer={}, logger={}".format(self.k, self.optimization, \
        self.key_loader, self.ft, self.logger)

#X, vec = semeval_feature_transform(ans_dict['add.v'])
#print X[:10]
#print vec.get_feature_names()
#exit()

# onemli
#classifiers = [svm.SVC, MultinomialNB,]
#m, n = len(classifiers), len(gold_dict.keys())
#results = np.zeros([m,n])
#stds = np.zeros([m,n])

#kfolds = dict()

#for i, tw in enumerate(gold_dict.keys()):
    #for j, c in enumerate(classifiers):
        #data = ans_dict[tw]
        #X = data.reshape(data.shape[0], 1)
        #Y = gold_dict[tw]
        #clf = c()
        #cv = cross_validation.ShuffleSplit(len(Y), n_iter=k,
                    #test_size=0.2, random_state=0)
        #scores = cross_validation.cross_val_score(clf, X, Y, cv=k)
