#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.naive_bayes import MultinomialNB
from sklearn import cross_validation, grid_search
from sklearn import svm
from feature_transform import semeval_feature_transform
from data_load import Semeval2013KeyLoader, Semeval2010KeyLoader
import sys
from optparse import OptionParser
import numpy as np


"""
This scripts is used to test various mapping procedures. Now it supports
two different test set formats (Semeval2013, Semeval2010) but other 
formats can be added in data_load module.



"""

parser = OptionParser()
parser.add_option("-i", "--ans_file", dest="ansfile", default=None,
                  help="System's Answer file", metavar="System File")
parser.add_option("-g", "--key_file", dest="keyfile", default=None,
                  help="gold dataset file", metavar="GOLD")
parser.add_option("-k", "--num_fold", dest="k", default=None,
        help="k in k-Fold Cross validation", metavar="TYPE")
parser.add_option("-s", "--seed", dest="seed", default=None,
        help="SEED Value", metavar="SEED")
parser.add_option("-l", "--key_loader", dest="loader", default=None,
        help="Key Loader type: Semeval2013 | Semeval2010", metavar="KEY_LOADER")

mandatories = ['keyfile', 'k', 'loader', 'ansfile']

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

(opts, args) = parser.parse_args() 
input_check(opts, mandatories)
keyfile = opts.keyfile
ansfile = opts.ansfile
k = int(opts.k)
loader_type = opts.loader

if loader_type == 'Semeval2013':
    KeyLoader = Semeval2013KeyLoader
elif loader_type == 'Semeval2010':
    KeyLoader = Semeval2010KeyLoader
else:
    raise ValueError, "{}, KeyLoader class not valid".format(loader_type)


class Evaluator(object):

    def __init__(self, ansfile, keyfile, devfile, k, optimization):
        raise NotImplementedError
        self.ansfile = ansfile
        self.keyfile = keyfile
        self.devfile = devfile
        self.k = k # k in k-fold cross validation
        self.optimization = optimization # parameter optimization true/false

class Semeval2010Evaluator(Evaluator):
    
    def __init__(self, ansfile, keyfile, devfile, k, optimization):
        raise NotImplementedError
        super(Evaluator, self).__init__(ansfile, keyfile, devfile, k, optimization)

class Semeval2013Evaluator(Evaluator):
    
    def __init__(self):
        raise NotImplementedError

ans_dict = KeyLoader.read_keyfile(ansfile)
gold_dict = KeyLoader.read_keyfile(keyfile)

print ans_dict['add.v'][:10]

X, vec = semeval_feature_transform(ans_dict['add.v'])
print X[:10]
print vec.get_feature_names()
exit()


def parameter_optimization(clf_type, parameters):
    raise NotImplementedError, "parameter_optimization def has not impl. yet"
    svr = svm.SVC()
    clf = grid_search.GridSearchCV(svr, parameters)
    return clf


classifiers = [svm.SVC, MultinomialNB,]
m, n = len(classifiers), len(gold_dict.keys())
results = np.zeros([m,n])
stds = np.zeros([m,n])

kfolds = dict()

for i, c in enumerate(classifiers):
    for j, tw in enumerate(gold_dict.keys()):
        data = ans_dict[tw]
        X = data.reshape(data.shape[0], 1)
        Y = gold_dict[tw]
        clf = c()
        cv = cross_validation.ShuffleSplit(len(Y), n_iter=k,
                    test_size=0.2, random_state=0)
        scores = cross_validation.cross_val_score(clf, X, Y, cv=k)
        results[i,j], stds[i,j] = scores.mean(), scores.std()

