#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import numpy as np

def delete_features(f1, f2, X_train, X_test):
    
    a = set(f1)
    b = set(f2)
    c = a.difference(b).union(b.difference(a))

    remove_list = []
    for i, e in enumerate(f1):
        if e in c:
            remove_list.append(i)

    X_train = np.delete(X_train, remove_list, axis=1)

    remove_list = []
    for i, e in enumerate(f2):
        if e in c:
            remove_list.append(i)
    
    X_test = np.delete(X_test, remove_list, axis=1)

    return X_train, X_test



def main():
    X_train = np.array([[1,2,3,6,7], [4,5,6,8,7], [12,13,66,16,20], [4,2,22,6,3]])
    X_test = np.array([[1,2,3,6,7], [4,5,6,8,7], [12,13,66,16,20], [4,2,22,6,3]])
    features1 = ["f1", "f2", "f3", "f8", "f5"]
    features2 = ["f1","f2", "f3", "f6", "f7"]

    print X_train
    print
    print X_test
    print
    print "-----"
    X_train, X_test = delete_features(features1, features2, X_train, X_test)
    print X_train
    print
    print X_test

if __name__ == '__main__':
    main()

