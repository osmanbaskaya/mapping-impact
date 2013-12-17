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
            clf = grid_search.GridSearchCV(self.classifier, parameters, cv=cv)
            clf.fit(X, y)
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
    
    def __init__(self, name, kernel='rbf', C=1, gamma=0):
        super(SVCWrapper, self).__init__(name, SVC(kernel=kernel, C=C, gamma=gamma))
        gamma = range(0,6)
        C = [0.003, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 40]
        if self.classifier.kernel == "rbf":
            self.parameters = {'C': C, 'gamma': gamma}
        elif self.classifier.kernel == "linear":
            self.parameters = {'C': C}
 
class MultinomialNBWrapper(ClassifierWrapper):
    
    def __init__(self):
        super(MultinomialNBWrapper, self).__init__("MultinomialNB", MultinomialNB())
        self.is_optimized = True
        self.parameters = {'alpha': np.linspace(0,1,11)}

class BernoulliNBWrapper(ClassifierWrapper):
    
    def __init__(self):
        super(BernoulliNBWrapper, self).__init__("BernoulliNBWrapper", BernoulliNB())
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

