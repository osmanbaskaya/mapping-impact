#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn import grid_search
from sklearn.svm import SVC

class ClassifierWrapper(object):

    def __init__(self, name, classifier):
        self.name = name
        self.classifer = classifier

    def optimize(self):
        raise NotImplementedError, "optimizate def has not impl. yet"


class SVCWrapper(ClassifierWrapper):
    

    def __init__(self):
        super(SVCWrapper, self).__init__("SVC", SVC)

    def optimize(self, parameters):
        """Hyperparameter optimization"""
        raise NotImplementedError, "parameter_optimization def has not impl. yet"
        clf = grid_search.GridSearchCV(self.classifier, parameters)
        return clf
        

def main():
    pass

if __name__ == '__main__':
    main()

