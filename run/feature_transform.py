#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler


class FeatureTransformer(object):
    
    def __init__(self, name):
        self.name = name

    def convert_data(self, data):
        raise NotImplementedError, "% not implemented" % "feature_transform"

class SemevalFeatureTransformer(FeatureTransformer):

    def __init__(self, weighted=False):
        super(SemevalFeatureTransformer, self).__init__("SemevalFeatureTransformer")
        self.vectorizer = CountVectorizer(min_df=0, token_pattern=r'[\w:\.%\d.]+')
    
    def convert_data(self, data):
        X = self.vectorizer.fit_transform(data).toarray()
        assert len(set(data)) == len(self.vectorizer.get_feature_names()),\
                "Should be same or using Graded senses?"
        return X
        
    def scale_data(self, X, drange=[-1,1]):
        return MinMaxScaler(feature_range=drange).fit_transform(X)

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

