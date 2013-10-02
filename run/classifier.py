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
        self.parameters = {'kernel':('linear', 'rbf'), 'C':[0.1, 1, 10, 100, 1000]}
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
        except ValueError, e: # all instances are belongs to the same class
            pass

        return best_params, best_estimator
        

def main():
    pass

if __name__ == '__main__':
    main()

