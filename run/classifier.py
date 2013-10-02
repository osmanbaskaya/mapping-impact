#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn import grid_search
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB

class ClassifierWrapper(object):

    def __init__(self, name, classifier):
        self.name = name
        self.classifier = classifier

    def optimize(self):
        raise NotImplementedError, "optimizate def has not impl. yet"


class SVCWrapper(ClassifierWrapper):
    
    def __init__(self):
        super(SVCWrapper, self).__init__("SVC", SVC())
        #FIXME: add gamma parameter
        self.parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
        self.is_optimized = False

    def optimize(self, parameters=None):
        """Hyperparameter optimization"""
        raise NotImplementedError, "parameter_optimization def has not impl. yet"
        if not self.is_optimized:
            if parameters is None:
                parameters = self.parameters
            clf = grid_search.GridSearchCV(self.classifier, parameters)
        self.is_optimized = True

def main():
    pass

if __name__ == '__main__':
    main()

