#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn import svm
from data_load import Semeval2013KeyLoader, Semeval2010KeyLoader
import sys
from optparse import OptionParser

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

ans_dict = KeyLoader.read_keyfile(ansfile)
gold_dict = KeyLoader.read_keyfile(keyfile)
#print senses['add.v'][:4]

kfolds = dict()
for tw, Y in gold_dict.iteritems():
    kfolds[tw] = KFold(len(Y), n_folds=k, indices=False)
    print tw, kfolds[tw]
    X = ans_dict[tw]
    for train, test in kfolds[tw]:
        X_train = X[train]
    

classifiers = [MultinomialNB, svm.SVC]

for c in classifiers:
    clf = c()
    print >> sys.stderr, "{}: Processing".format(clf)

