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
from nlp_utils import calc_perp, delete_features
from collections import defaultdict as dd
import os

"""
This script is used to test various mapping procedures. Now it supports
two different test set formats (Semeval2013, Semeval2010) but other 
formats can be added in data_load module.

"""

__all__ = ['Evaluator', 'SemevalEvaluator', 'ChunkEvaluator']

class Evaluator(object):

    def __init__(self, clf_wrapper, optimization, \
                 key_loader, ft, logger):
        self.optimization = optimization # parameter optimization true/false
        self.key_loader = key_loader
        self.ft = ft #feature transformer
        self.logger = logger
        self.clf_wrapper = clf_wrapper
        
        self.logger.init(self)
    
    def optimize(self):

        """ This method finds the best estimator on development set by using
        GridSearchCV and set this estimator as classifier. It also sets 
        is_optimized parameters to avoid unnecessary tuning"""

        if self.optimization and not self.clf_wrapper.is_optimized:

            all_val = []
            all_target = []
            
            for sys_file, gold_file in zip(self.devset[0], self.devset[1]):

                tw = os.path.basename(sys_file)[:-4]
                val, target = map(self.load_key_file, (sys_file, gold_file))

                for k, v in val[tw].iteritems():
                    all_val.append((k,v))

                for k, v in target[tw].iteritems():
                    all_target.append((k,v))

            X, y = self.ft.convert_data(dict(all_val), dict(all_target))
            X = self.ft.scale_data(X)
            self.logger.info("Scaling done for tuning data")
            cv = cross_validation.KFold(len(y), n_folds=10)
            p, e, s = self.clf_wrapper.optimize(X, y, cv=cv)
            msg = "Best_params:{}, Best Score:{}, Best Estimator".format(p, s, e)
            self.logger.info(msg)
            self.clf_wrapper.classifier = e
            self.clf_wrapper.is_optimized = True
            self.logger.info("Optimization finished")
    
    def load_key_file(self, f):
        return self.key_loader.read_keyfile(f)
    
    def report(self):
        """This method provides evaluator's details to stderr"""
        raise NotImplementedError
        
class SemevalEvaluator(Evaluator):
    
    def __init__(self, clf_wrapper, trainset, devset, k, optimization, logger=None): 
        super(SemevalEvaluator, self).__init__(clf_wrapper, optimization, 
         SemevalKeyLoader(), SemevalFeatureTransformer(weighted=False), logger=logger)
        
        self.k = k # k in k-fold cross validation
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
                tuned_scores = []
                for tw, data in sorted(dev_system_dict.iteritems()):
                    target = dev_gold_dict[tw]
                    X, y = self.ft.convert_data(data, target)
                    X = self.ft.scale_data(X)
                    cv = cross_validation.KFold(len(y), n_folds=self.k)
                    p, e, s = self.clf_wrapper.optimize(X, y, cv=cv)
                    if p is not None:
                        params.append(p)
                        estimators.append(e)
                        tuned_scores.append(s)
                    #print p

                self.set_best_estimator(params, estimators, tuned_scores)
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

    def __init__(self, clf_wrapper, tw_dict, system_files, devset, optimization, logger): 
        super(ChunkEvaluator, self).__init__(clf_wrapper, optimization, 
         SemevalKeyLoader(), SemevalFeatureTransformer(weighted=False), logger=logger)

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
        self.logger.info("Reading all system answers done")

    def _prepare(self, tw, chunks):

            c = chunks[:]
            g = self.gold_dict[tw][:]

            # last chunk will be the test chunk.
            test_data = c.pop()
            test_gold = g.pop()

            # data of the remaining chunks are incorporated
            val = {}
            map(val.update, c)

            # gold labels of the remaining chunks are incorporated
            target = {}
            map(target.update, g)

            #print len(val), len(target)
            
            #print len(c), len(chunks)
            #print len(g), len(self.gold_dict[tw])

            X_train, y_train = self.ft.convert_data(val, target)
            X_train = self.ft.scale_data(X_train)
            features1 = self.ft.vectorizer.get_feature_names()
            X_test, y_test = self.ft.convert_data(test_data, test_gold)

            # check the order 
            #pprint(X_test.tolist()[:10])
            #pprint(zip(test_data.keys(), y_test)[:10])
            #print self.ft.vectorizer.get_feature_names()

            X_test = self.ft.scale_data(X_test)
            features2 = self.ft.vectorizer.get_feature_names()
            # Feature space should be the same for both training and testing

            if features1 != features2:
                X_train, X_test = delete_features(features1, features2, X_train, X_test)

            return X_train, X_test, y_train, y_test, test_data.keys()
    
    def predict(self):
        predictions = {}
        # optimization
        self.optimize()
        self.logger.info(self.clf_wrapper.classifier)
        
        for tw, chunks in self.system_key_dict.iteritems():

            X_train, X_test, y_train, y_test, test_inst_order = self._prepare(tw,chunks)
            
            try:
                self.clf_wrapper.classifier.fit(X_train, y_train)
                prediction = self.clf_wrapper.classifier.predict(X_test)
            except ValueError, e: # all instances are belongs to the same class
                self.logger.warning("{}-{}: {}".format(self.clf_wrapper.name, tw, e))
                if str(e) == "The number of classes has to be greater than one.":
                    prediction = [y_train[0]] * len(y_test)

            predictions[tw] = (zip(test_inst_order, prediction))

            print "predictions"
        return predictions

    def score(self):
        scores = {}
        # optimization
        self.optimize()
        self.logger.info(self.clf_wrapper.classifier)
        
        for tw, chunks in self.system_key_dict.iteritems():

            X_train, X_test, y_train, y_test, test_inst_order = self._prepare(tw,chunks)
            
            score = 0.0
            try:
                self.clf_wrapper.classifier.fit(X_train, y_train)
                score = self.clf_wrapper.classifier.score(X_test, y_test)
            except ValueError, e: # all instances are belongs to the same class
                self.logger.warning("{}-{}: {}".format(self.clf_wrapper.name, tw, e))
                if str(e) == "The number of classes has to be greater than one.":
                    prediction = [y_train[0]] * len(y_test)
                    score = sum(prediction == y_test) / float(len(y_test))
            
            scores[tw] = (score, calc_perp(y_test))
        #self.ft.dump_data_libsvm_format(X, y, 'libsvm-input/' + tw)
        return scores

    def score_and_predict(self):
        scores = {}
        predictions = {}
        # optimization
        self.optimize()
        self.logger.info(self.clf_wrapper.classifier)
        
        for tw, chunks in self.system_key_dict.iteritems():

            X_train, X_test, y_train, y_test, test_inst_order = self._prepare(tw,chunks)
            
            score = 0.0
            try:
                self.clf_wrapper.classifier.fit(X_train, y_train)
                prediction = self.clf_wrapper.classifier.predict(X_test)
                score = self.clf_wrapper.classifier.score(X_test, y_test)
            except ValueError, e: # all instances are belongs to the same class
                self.logger.warning("{}-{}: {}".format(self.clf_wrapper.name, tw, e))
                if str(e) == "The number of classes has to be greater than one.":
                    prediction = [y_train[0]] * len(y_test)
                    score = sum(prediction == y_test) / float(len(y_test))
                if str(e) == "Input X must be non-negative.":
                    pass

            
            scores[tw] = (score, calc_perp(y_test))
            predictions[tw] = (zip(test_inst_order, prediction))
        #self.ft.dump_data_libsvm_format(X, y, 'libsvm-input/' + tw)
        return scores, predictions




