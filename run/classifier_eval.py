#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from feature_transform import SemevalFeatureTransformer
from data_load import SemevalKeyLoader
import sys
from pprint import pprint
from sklearn import cross_validation
from logger import SemevalLogger, ColorLogger
from nlp_utils import calc_perp, delete_features
from collections import defaultdict as dd
import os
import random

"""
This script is used to test various mapping procedures. Now it supports
two different test set formats (Semeval2013, Semeval2010) but other 
formats can be added in data_load module.

"""

__all__ = ['Evaluator', 'SemevalEvaluator', 'ChunkEvaluator', 'IMSBasedChunkEvaluator']

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

            X, y, instance_list = self.ft.convert_data(dict(all_val), dict(all_target))
            vectorizer = self.ft.get_vectorizer()
            X = vectorizer.fit_transform(X)
            if self.clf_wrapper.name in ["SVM_Linear", "SVM_Gaussian"]:
                X = self.ft.get_scaler().fit_transform(X)
            self.logger.info("Scaling done for tuning data")
            cv = cross_validation.KFold(len(y), n_folds=5)
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
                    X, y, inst_data = self.ft.convert_data(data, target)
                    vectorizer = self.ft.get_vectorizer()
                    X = vectorizer.fit_transform(X)
                    if self.clf_wrapper.name in ["SVM_Linear", "SVM_Gaussian"]:
                        X = self.ft.get_scaler().fit_transform(X)
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
            X, y, inst_data = self.ft.convert_data(val, target)
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

            X_train, y_train, dummy = self.ft.convert_data(val, target)
            vectorizer = self.ft.get_vectorizer()
            X_train = vectorizer.fit_transform(X_train)
            if self.clf_wrapper.name in ["SVM_Linear", "SVM_Gaussian"]:
                scaler = self.ft.get_scaler()
                X_train = scaler.fit_transform(X_train)

            #features1 = self.ft.vectorizer.get_feature_names()
            X_test, y_test, dummy = self.ft.convert_data(test_data, test_gold)
            X_test = vectorizer.transform(X_test)
            
            if self.clf_wrapper.name in ["SVM_Linear", "SVM_Gaussian"]:
                X_test = scaler.transform(X_test)

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

            #print "predictions"
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

    @staticmethod
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

class IMSBasedChunkEvaluator(Evaluator):

    def __init__(self,clf_wrapper,dataset,system_files,devset,optimization, logger): 
        super(IMSBasedChunkEvaluator, self).__init__(clf_wrapper, optimization, 
         SemevalKeyLoader(), SemevalFeatureTransformer(weighted=False), logger=logger)

        self.system_files = system_files
        self.dataset = dataset
        self.devset = devset
        
    def _prepare(self, tw, train_file, test_file):

        system_keys = self.load_key_file(self.system_files[tw])[tw]

        #tr_gold = self.load_key_file(train_file)[tw + ".n"] # ims keys has .n
        #te_gold = self.load_key_file(test_file)[tw + ".n"] # ims keys has .n

        tr_gold = self.load_key_file(train_file)[tw] # ims keys has .n
        te_gold = self.load_key_file(test_file)[tw] # ims keys has .n

        tr_inst = tr_gold.keys()
        te_inst = te_gold.keys()
        
        system_tr_dict = dict(zip(tr_inst, map(system_keys.get, tr_inst)))
        system_te_dict = dict(zip(te_inst, map(system_keys.get, te_inst)))

        assert len(tr_inst) == len(system_tr_dict)
        assert len(te_inst) == len(system_te_dict)

        X_train, y_train, inst_list_tr = self.ft.convert_data(system_tr_dict, tr_gold)

        vectorizer = self.ft.get_vectorizer()
        X_train = vectorizer.fit_transform(X_train)
        if self.clf_wrapper.name in ["SVM_Linear", "SVM_Gaussian"]:
            scaler = self.ft.get_scaler()
            X_train = scaler.fit_transform(X_train)

        X_test, y_test, inst_list_te = self.ft.convert_data(system_te_dict, te_gold)
        X_test = vectorizer.transform(X_test)

        if self.clf_wrapper.name in ["SVM_Linear", "SVM_Gaussian"]:
            X_test = scaler.transform(X_test)
        
        return X_train, X_test, y_train, y_test, inst_list_te


    def predict(self):
        predictions = dict()
        # optimization
        self.optimize()
        self.logger.info(self.clf_wrapper.classifier)

        for tw, chunks in self.dataset.viewitems():
            tw_predictions = []
            #tw_scores = []
            for i, datasets in enumerate(chunks): #test set and train set
                tr, te  = datasets
                X_train, X_test, y_train, y_test, test_inst_order = self._prepare(tw,tr,te)

                #score = 0.0
                try:
                    self.clf_wrapper.classifier.fit(X_train, y_train)
                    prediction = self.clf_wrapper.classifier.predict(X_test)
                    #score = self.clf_wrapper.classifier.score(x_test, y_test)
                except ValueError, e: # all instances are belongs to the same class
                    self.logger.warning("{}-{}: {}".format(self.clf_wrapper.name, tr, e))
                    if str(e) == "The number of classes has to be greater than one.":
                        prediction = [y_train[0]] * len(y_test)
                        #score = sum(prediction == y_test) / float(len(y_test))
                    if str(e) == "Input X must be non-negative.":
                        pass
                
                tw_predictions.extend(zip(test_inst_order, prediction))
            predictions[tw] = dict(tw_predictions)
        return predictions

    def predict_by_chunks(self):
        predictions = dd(dict)
        # optimization
        self.optimize()
        self.logger.info(self.clf_wrapper.classifier)

        for tw, chunks in self.dataset.viewitems():
            tw_predictions = dd(list)
            #tw_scores = []
            for i, datasets in enumerate(chunks): #test set and train set
                tr, te  = datasets
                X_train, X_test, y_train, y_test, test_inst_order = self._prepare(tw,tr,te)

                #score = 0.0
                try:
                    self.clf_wrapper.classifier.fit(X_train, y_train)
                    prediction = self.clf_wrapper.classifier.predict(X_test)
                    #score = self.clf_wrapper.classifier.score(x_test, y_test)
                except ValueError, e: # all instances are belongs to the same class
                    self.logger.warning("{}-{}: {}".format(self.clf_wrapper.name, tr, e))
                    if str(e) == "The number of classes has to be greater than one.":
                        print >> sys.stderr, "initialization", y_train[0]
                        prediction = [y_train[0]] * len(y_test)
                        #score = sum(prediction == y_test) / float(len(y_test))
                    if str(e) == "Input X must be non-negative.":
                        pass
                tw_predictions[i].extend(zip(test_inst_order, prediction))
            for i in xrange(len(chunks)):
                predictions[i][tw] = dict(tw_predictions[i])
        return predictions

    @staticmethod
    def write_chunk_prediction2file(predictions, out_path):
        d = dd(lambda: dd(list))
        for exp_name, preds in predictions.viewitems():
            for chunk_id, chunk_preds in preds.viewitems():
                for tw, pred in chunk_preds.iteritems():
                    for inst_id, label in pred.viewitems():
                        s = "{} {} {}".format(tw, inst_id, label)
                        d[exp_name][chunk_id].append(s)

        for exp_name, chunk_vals in d.iteritems():
            for chunk_id, val in chunk_vals.viewitems():
                out_f = os.path.join(out_path, "{}-{}".format(exp_name, chunk_id))
                print out_f
                f = open(out_f, 'w')
                f.write('\n'.join(val))
                f.write('\n')

    @staticmethod
    def write_prediction2file(predictions, out_path):
        d = dd(list)
        for exp_name, preds in predictions.viewitems():
            for tw, pred in preds.iteritems():
                for inst_id, label in pred.viewitems():
                    s = "{} {} {}".format(tw, inst_id, label)
                    d[exp_name].append(s)
        

        for key, val in d.iteritems():
            out_f = os.path.join(out_path, key)
            print out_f
            f = open(out_f, 'w')
            f.write('\n'.join(val))
            f.write('\n')

    def data_dump(self, f, X_train, X_test, y_train, y_test):
        from sklearn.datasets import dump_svmlight_file
        ddd = dict()
        new_y_train = []
        last = 0
        for yy in y_train:
            if yy in ddd:
                yy = (ddd[yy])
            else:
                ddd[yy] = last
                yy = last
                last += 1
            new_y_train.append(yy)

        dump_svmlight_file(X_train, new_y_train, f + ".svmlight.train")
        
        new_y_test = []
        for yy in y_test:
            if yy in ddd:
                yy = (ddd[yy])
            else:
                ddd[yy] = last
                yy = last
                last += 1
            new_y_test.append(yy)
        
        dump_svmlight_file(X_test, new_y_test, f + ".svmlight.test")
