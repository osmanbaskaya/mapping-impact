#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.feature_extraction.text import CountVectorizer


__all__ = ['semeval_feature_transform',]

def semeval_feature_transform(data):
    vec = CountVectorizer(min_df=0, token_pattern=r'[\w:%]+')
    X = vec.fit_transform(data).toarray()
    return X, vec

def main():
    pass

if __name__ == '__main__':
    main()

