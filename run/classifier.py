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
        print >> sys.stderr, "Parameter space:{}".format(parameters)
        try:
            clf = grid_search.GridSearchCV(self.classifier, parameters, cv=cv, verbose=1,
                                          n_jobs=20)
            clf.fit(X, y)
            print >> sys.stderr, clf.grid_scores_
            best_params = clf.best_params_
            best_estimator = clf.best_estimator_
        except ValueError, e: # all instances belong to the same class
            print >> sys.stderr, e
        #FIXME: Why do we get index errors for book.v
        except IndexError, e:
            print >> sys.stderr, e
        #try:
            #msg = "Best_params:{}, Best Score:{}".format(best_params, clf.best_score_)
            #print >> sys.stderr, msg
        #except AttributeError:
            #pass
        return best_params, best_estimator, clf.best_score_


class SVCWrapper(ClassifierWrapper):
    
    def __init__(self, name, **kwargs):
        super(SVCWrapper, self).__init__(name, SVC(**kwargs))
        gamma = 10.0 ** np.arange(-5, 4)
        C = 10.0 ** np.arange(-2, 6)
        #C = [0.003, 0.03, 0.3, 1, 9, 27, 81, 243, 729, 2000, 6000]
        if self.classifier.kernel == "rbf":
            self.parameters = {'C': C, 'gamma': gamma}
        elif self.classifier.kernel == "linear":
            self.parameters = {'C': C}
 
class MultinomialNBWrapper(ClassifierWrapper):
    
    def __init__(self, name="MultinomialNB"):
        super(MultinomialNBWrapper, self).__init__(name, MultinomialNB())
        self.is_optimized = True
        self.parameters = {'alpha': np.linspace(0,1,11)}

class BernoulliNBWrapper(ClassifierWrapper):
    
    def __init__(self, name="BernoulliNBWrapper"):
        super(BernoulliNBWrapper, self).__init__(name, BernoulliNB())
        self.parameters = {'alpha': np.linspace(0,1,11)}
        self.is_optimized = True

class DecisionTreeWrapper(ClassifierWrapper):
    
    def __init__(self, name, criterion):
        super(DecisionTreeWrapper, self).__init__(name,
                                    DecisionTreeClassifier(criterion=criterion))
        self.is_optimized = True

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

