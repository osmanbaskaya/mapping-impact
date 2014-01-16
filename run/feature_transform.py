#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.feature_extraction.text import CountVectorizer
from pprint import pprint
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction import DictVectorizer
import numpy as np


class FeatureTransformer(object):
    
    def __init__(self, name):
        self.name = name

    def convert_data(self, data):
        raise NotImplementedError, "% not implemented" % "feature_transform"

class SemevalFeatureTransformer(FeatureTransformer):

    def __init__(self, weighted=False):
        super(SemevalFeatureTransformer, self).__init__("SemevalFeatureTransformer")
        #self.vectorizer = CountVectorizer(min_df=0, token_pattern=r'[\w:\.%\d.]+')
    
    def convert_data(self, data, target, rem=None):
        X = []
        y = []
        for key in data:
            X.append(dict(data[key]))
            y.append(target[key][0][0]) # we get only one sense for gold standard
        
        return X, np.array(y)

    def get_vectorizer(self):
        return DictVectorizer(sparse=False)
        
    def get_scaler(self, drange=[0,1]):
        return MinMaxScaler(feature_range=drange)

    def dump_data_libsvm_format(self, X, y, fn):
        d = dict()
        count = 1
        f = open(fn, 'w')
        for label in y:
            if label not in d:
                d[label] = count
                count += 1
        for i in range(X.shape[0]):
            f.write("{} ".format(d[y[i]]))
            for j in range(X.shape[1]):
                if X[i,j] != 0:
                     f.write("{}:{}".format(j+1,X[i,j]))
            f.write('\n')
        f.close()

def main():
    pass

if __name__ == '__main__':
    main()

