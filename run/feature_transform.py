#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.feature_extraction.text import CountVectorizer


class FeatureTransformer(object):
    
    def __init__(self, name):
        self.name = name

    def convert_data(self, data):
        raise NotImplementedError, "% not implemented" % "feature_transform"

class SemevalFeatureTransformer(FeatureTransformer):

    def __init__(self, weighted=False):
        super(SemevalFeatureTransformer, self).__init__("SemevalFeatureTransformer")
        self.vectorizer = CountVectorizer(min_df=0, token_pattern=r'[\w:%]+')

    def convert_data(self, data):
        X = self.vectorizer.fit_transform(data).toarray()
        return X

def main():
    pass

if __name__ == '__main__':
    main()

