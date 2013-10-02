#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from feature_transform import SemevalFeatureTransformer
from data_load import SemevalKeyLoader
import sys
from optparse import OptionParser
from sklearn import cross_validation
import numpy as np
from logger import SemevalLogger
from collections import defaultdict as dd


"""
This script is used to test various mapping procedures. Now it supports
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

    def __init__(self, clf_wrapper, ansfile, keyfile, devfile, k, 
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
        self.clf_wrapper = clf_wrapper
        
        self.X = None
        self.Y = None
        self.X_dev = None

    def load_key_file(self, f):
        return self.key_loader.read_keyfile(f)

    def report(self):
        """This method provides evaluator's details to stderr"""
        raise NotImplementedError
        
class SemevalEvaluator(Evaluator):
    
    def __init__(self, clf_wrapper, ansfile, keyfile, devfile, k, optimization, logger): 
        super(SemevalEvaluator, self).__init__(clf_wrapper, ansfile, keyfile, 
              devfile, k, optimization, SemevalKeyLoader(), 
              SemevalFeatureTransformer(weighted=False), logger=logger)
        logger.info(self)

    def set_best_estimator(self, params, estimators):

        """ This method finds the best estimator on development set by using
        GridSearchCV and set this estimator as classifier. It also sets 
        is_optimized parameters to avoid unnecessary tuning"""
        
        assert len(params) == len(estimators)
        par_list = self.clf_wrapper.parameters.keys()
        d = dd(lambda : [0, None])

        for e in estimators:
            pdict = e.get_params()
            s = ' '.join(map(str, map(pdict.get, par_list)))
            d[s][0] += 1
            d[s][1] = e

        max_par = max(d, key= lambda x: d[x][0])
        self.logger.info("Best set of parameters is: {}".format
                            (zip(par_list, max_par.split())))
        self.clf_wrapper.classifier = d[max_par][1]
        self.clf_wrapper.is_optimized = True

    def score(self):
        scores = {}
        clf = self.clf_wrapper.classifier
        files = [self.ansfile, self.keyfile, self.devfile]
        ans_dict, gold_dict, dev_dict = map(self.load_key_file, files)

        # optimization
        if self.optimization:
            if not self.clf_wrapper.is_optimized:
                params = []
                estimators = []
                for tw, val in dev_dict.iteritems():
                    X =  self.ft.convert_data(val)
                    y = np.array(gold_dict[tw])
                    cv = cross_validation.ShuffleSplit(len(y), n_iter=10,
                                test_size=0.2, random_state=0)
                    p, e = self.clf_wrapper.optimize(X, y, cv=cv)
                    if p is not None:
                        params.append(p)
                        estimators.append(e)

                self.set_best_estimator(params, estimators)

        print self.clf_wrapper.classifier
        for tw, val in ans_dict.iteritems():
            y = gold_dict[tw]
            X =  self.ft.convert_data(val)

            cv = cross_validation.ShuffleSplit(len(y), n_iter=self.k,
                        test_size=0.2, random_state=0)
            self.logger.info('\nCross Validation:' + str([i for i in cv]))
            try:
                score = cross_validation.cross_val_score(clf, X, y, cv=cv)
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

