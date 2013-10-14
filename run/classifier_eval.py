#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from feature_transform import SemevalFeatureTransformer
import re
from data_load import SemevalKeyLoader
from sklearn import cross_validation
from logger import SemevalLogger, ColorLogger
import numpy as np
from pprint import pprint
from nlp_utils import calc_perp
from collections import defaultdict as dd


"""
This script is used to test various mapping procedures. Now it supports
two different test set formats (Semeval2013, Semeval2010) but other 
formats can be added in data_load module.

"""

__all__ = ['Evaluator', 'SemevalEvaluator', 'ChunkEvaluator']

class Evaluator(object):

    def __init__(self, clf_wrapper, k, optimization, \
                 key_loader, ft, logger):
        self.k = k # k in k-fold cross validation
        self.optimization = optimization # parameter optimization true/false
        self.key_loader = key_loader
        self.ft = ft #feature transformer
        self.logger = logger
        self.clf_wrapper = clf_wrapper
        
        self.logger.init(self)
    
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
        #self.logger.info("Best set of parameters is: {}".format
                            #(zip(par_list, max_par.split())))
        self.clf_wrapper.classifier = d[max_par][1]
        self.clf_wrapper.is_optimized = True

    def load_key_file(self, f):
        return self.key_loader.read_keyfile(f)
    
    def report(self):
        """This method provides evaluator's details to stderr"""
        raise NotImplementedError
        
class SemevalEvaluator(Evaluator):
    
    def __init__(self, clf_wrapper, trainset, devset, k, optimization, logger=None): 
        super(SemevalEvaluator, self).__init__(clf_wrapper, k, 
            optimization, SemevalKeyLoader(), SemevalFeatureTransformer(weighted=False), 
            logger=logger)
        
        self.trainset = trainset
        self.devset = devset

    def score(self):
        scores = {}
        # optimization
        if self.optimization:
            files = [self.devset.data, self.devset.target]
            dev_system_dict, dev_gold_dict = map(self.load_key_file, files)

            if not self.clf_wrapper.is_optimized:
                params = []
                estimators = []
                for tw, data in sorted(dev_system_dict.iteritems()):
                    target = dev_gold_dict[tw]
                    X, y = self.ft.convert_data(data, target)
                    X = self.ft.scale_data(X, drange=[-1,1])
                    cv = cross_validation.KFold(len(y), n_folds=self.k)
                    p, e = self.clf_wrapper.optimize(X, y, cv=cv)
                    if p is not None:
                        params.append(p)
                        estimators.append(e)
                    #print p

                self.set_best_estimator(params, estimators)
            self.logger.info("Optimization finished")
        
        files = [self.trainset.data, self.trainset.target]
        system_key_dict, gold_dict = map(self.load_key_file, files)
        self.logger.info(self.clf_wrapper.classifier)

        for tw, val in system_key_dict.iteritems():
            target = gold_dict[tw]
            X, y = self.ft.convert_data(val, target)
            cv = cross_validation.KFold(len(y), n_folds=self.k)
            #self.logger.info('\nCross Validation:' + str([i for i in cv]))
            try:
                score = cross_validation.cross_val_score(
                    self.clf_wrapper.classifier, X, y, cv=cv)
            except ValueError, e: # all instances are belongs to the same class
                self.logger.warning("{}\t{}".format(tw, e))
            scores[tw] = (score.mean(), calc_perp(y))
            #self.ft.dump_data_libsvm_format(X, y, 'libsvm-input/' + tw)
        return scores

    def report(self):
        pass

    def __str__(self):
        return "SemevalEvaluator:k={}, optimization={}, key_loader={}, \
        feature_transformer={}, logger={}".format(self.k, self.optimization, \
        self.key_loader, self.ft, self.logger)


class ChunkEvaluator(Evaluator):

    def __init__(self, clf_wrapper, tw_dict, system_files, devset, k, optimization, logger): 
        super(ChunkEvaluator, self).__init__(clf_wrapper, k, 
            optimization, SemevalKeyLoader(), SemevalFeatureTransformer(weighted=False), 
            logger=logger)

        self.system_files = system_files
        self.devset = devset
        
        self.gold_dict = {}
        self.instances = {}

        for key, values in tw_dict.iteritems():
            vv = map(self.load_key_file, values)
            self.gold_dict[key] =  [vv[i][key] for i in range(len(vv))]
            self.instances[key] = [vv[i][key].keys() for i in range(len(vv))]

        self.get_system_answers()

    def get_system_answers(self):
        
        self.system_key_dict = {}

        for tw, val in self.system_files.iteritems():
            values =  [val] * len(self.instances[tw])
            vv = map(self.load_key_file, values)
            self.system_key_dict[tw] =  [vv[i][tw] for i in range(len(vv))]
            # Now we need to clear the chunks from other instances
            include_lists = self.instances[tw]
            for i, inc in enumerate(include_lists):
                d = self.system_key_dict[tw][i]
                self.system_key_dict[tw][i] = dict(zip(inc, map(d.get, inc)))


    def score(self):
        scores = {}
        # optimization
        if self.optimization:
            files = [self.devset.data, self.devset.target]
            dev_system_dict, dev_gold_dict = map(self.load_key_file, files)

            if not self.clf_wrapper.is_optimized:
                params = []
                estimators = []
                for tw, data in sorted(dev_system_dict.iteritems()):
                    target = dev_gold_dict[tw]
                    X, y = self.ft.convert_data(data, target)
                    X = self.ft.scale_data(X)
                    cv = cross_validation.KFold(len(y), n_folds=self.k)
                    p, e = self.clf_wrapper.optimize(X, y, cv=cv)
                    if p is not None:
                        params.append(p)
                        estimators.append(e)
                    #print p

                self.set_best_estimator(params, estimators)
            self.logger.info("Optimization finished")
        
        self.logger.info(self.clf_wrapper.classifier)

        for tw, chunks in self.system_key_dict.iteritems():

            m = len(chunks)
            chunk_score = np.zeros(m)
            for i in range(m):
                c = chunks[:]
                g = self.gold_dict[tw][:]
                test_data = c.pop(i)
                test_gold = g.pop(i)

                val = {}
                map(val.update, c)

                target = {}
                map(target.update, g)

                #print len(val), len(target)
                
                #print len(c), len(chunks)
                #print len(g), len(self.gold_dict[tw])
                #exit()

                X_train, y_train = self.ft.convert_data(val, target)
                X_train = self.ft.scale_data(X_train)
                X_test, y_test = self.ft.convert_data(test_data, test_gold)
                X_test = self.ft.scale_data(X_test)

                score = 0.0
                try:
                    self.clf_wrapper.classifier.fit(X_train, y_train)
                    score = self.clf_wrapper.classifier.score(X_test, y_test)
                    #prediction = self.clf_wrapper.classifier.predict(X_test)
                except ValueError, e: # all instances are belongs to the same class
                    pass
                    #self.logger.warning("{}\t{}".format(tw, e))
                chunk_score[i] = score
                print score
            scores[tw] = (chunk_score.mean())

            #self.ft.dump_data_libsvm_format(X, y, 'libsvm-input/' + tw)
        return scores
            


