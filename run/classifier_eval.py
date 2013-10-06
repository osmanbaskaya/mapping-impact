#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from feature_transform import SemevalFeatureTransformer
from data_load import SemevalKeyLoader
from sklearn import cross_validation
import numpy as np
from logger import SemevalLogger
from nlp_utils import calc_perp
from collections import defaultdict as dd


"""
This script is used to test various mapping procedures. Now it supports
two different test set formats (Semeval2013, Semeval2010) but other 
formats can be added in data_load module.

"""

__all__ = ['Evaluator', 'SemevalKeyLoader']


class Evaluator(object):

    def __init__(self, clf_wrapper, trainset, devset, k, optimization, \
                 key_loader, ft, logger):
        self.trainset = trainset
        self.devset = devset
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
    
    def __init__(self, clf_wrapper, trainset, devset, k, optimization, logger): 
        super(SemevalEvaluator, self).__init__(clf_wrapper, trainset, devset, k, 
            optimization, SemevalKeyLoader(), SemevalFeatureTransformer(weighted=False), 
            logger=logger)
        logger.info(self)

    def set_best_estimator(self, params, estimators):

        """ This method finds the best estimator on development set by using
        GridSearchCV and set this estimator as classifier. It also sets 
        is_optimized parameters to avoid unnecessary tuning"""
        
        #print estimators
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
        
        # optimization
        if self.optimization:
            files = [self.devset.data, self.devset.target]
            dev_system_dict, dev_gold_dict = map(self.load_key_file, files)

            if not self.clf_wrapper.is_optimized:
                params = []
                estimators = []
                for tw, val in dev_system_dict.iteritems():
                    X =  self.ft.convert_data(val)
                    y = np.array(dev_gold_dict[tw])
                    cv = cross_validation.ShuffleSplit(len(y), n_iter=10,
                                test_size=0.2, random_state=0)
                    p, e = self.clf_wrapper.optimize(X, y, cv=cv)
                    if p is not None:
                        params.append(p)
                        estimators.append(e)
                    #print p

                self.set_best_estimator(params, estimators)
            self.logger.info("Optimization finished")
        
        
        files = [self.trainset.data, self.trainset.target]
        system_key_dict, gold_dict = map(self.load_key_file, files)

        for tw, val in system_key_dict.iteritems():
            y = gold_dict[tw]
            X =  self.ft.convert_data(val)

            cv = cross_validation.ShuffleSplit(len(y), n_iter=self.k,
                        test_size=0.2, random_state=0)
            #self.logger.info('\nCross Validation:' + str([i for i in cv]))
            try:
                score = cross_validation.cross_val_score(clf, X, y, cv=cv)
            except ValueError, e: # all instances are belongs to the same class
                self.logger.warning("{}\t{}".format(tw, e))
            scores[tw] = (score.mean(), calc_perp(y))
        return scores

    def report(self):
        pass

    def __str__(self):
        return "SemevalEvaluator:k={}, optimization={}, key_loader={}, \
        feature_transformer={}, logger={}".format(self.k, self.optimization, \
        self.key_loader, self.ft, self.logger)

