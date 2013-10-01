#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.feature_extraction.text import CountVectorizer


class FeatureTransformer(object):
    
    def __init__(self):
        pass

    def semeval_feature_transform(self, data):
        raise NotImplementedError, "% not implemented" % "feature_transform"

class CountTransformer(FeatureTransformer):

    def __init__(self):
        super(CountTransformer, self).__init__()

    def semeval_feature_transform(self, data):
        vec = CountVectorizer(min_df=0, token_pattern=r'[\w:%]+')
        X = vec.fit_transform(data).toarray()
        return X, vec

def main():
    pass

if __name__ == '__main__':
    main()

