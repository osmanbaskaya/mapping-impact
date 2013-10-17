#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn import grid_search
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
#from statsmodels.discrete.discrete_model import MNLogit
import numpy as np
import sys


class ClassifierWrapper(object):

    def __init__(self, name, classifier):
        self.name = name
        self.classifier = classifier
        self.is_optimized = False

    def optimize(self, X, y, cv, parameters=None):
        """Hyperparameter optimization"""
        best_params = best_estimator = None
        if parameters is None:
            parameters = self.parameters
        try:
            clf = grid_search.GridSearchCV(self.classifier, parameters, cv=cv)
            clf.fit(X, y)
            best_params = clf.best_params_
            best_estimator = clf.best_estimator_
        except ValueError, e: # all instances belong to the same class
            print >> sys.stderr, e
        #FIXME: Why do we get index errors for book.v
        except IndexError, e:
            print >> sys.stderr, e
        try:
            print "Best Score", y[0], clf.best_score_
        except AttributeError:
            pass
        return best_params, best_estimator


class SVCWrapper(ClassifierWrapper):
    
    def __init__(self, name, kernel):
        super(SVCWrapper, self).__init__(name, SVC(kernel=kernel))
        #FIXME: add gamma parameter? Check ranges
        self.parameters = {'kernel':('linear', 'rbf'), 'C':[0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10]}
        #self.parameters = {'kernel':('linear', 'rbf'), 'C':[10]}

class MultinomialNBWrapper(ClassifierWrapper):
    
    def __init__(self):
        super(MultinomialNBWrapper, self).__init__("MultinomialNB", MultinomialNB())
        #FIXME: Check ranges
        self.parameters = {'alpha': np.linspace(0,1,11)}

class BernoulliNBWrapper(ClassifierWrapper):
    
    def __init__(self):
        super(BernoulliNBWrapper, self).__init__("BernoulliNBWrapper", BernoulliNB())
        #FIXME: Check ranges
        self.parameters = {'alpha': np.linspace(0,1,11)}

class DecisionTreeWrapper(ClassifierWrapper):
    
    def __init__(self):
        super(DecisionTreeWrapper, self).__init__("DecisionTreeWrapper",
                                    DecisionTreeClassifier(criterion="entropy"))
        #FIXME: Check ranges
        self.parameters = {}

#class MNLogitWrapper(ClassifierWrapper):

    #def __init__(self):
        #raise NotImplementedError, "soon"
        #super(MNLogitWrapper, self).__init__("MNLogitWrapper", MNLogitW())
        #self.parameters = {}
        #print self.name
    
def main():
    pass

if __name__ == '__main__':
    main()

