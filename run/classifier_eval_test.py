#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from classifier_eval import SemevalEvaluator
from classifier import SVCWrapper


ansfile = 'dummy.key'
keyfile = 'dummy.key'
devfile = 'dummy.key'
k = 10
opt = True #optimization



wrapper = SVCWrapper()
e = SemevalEvaluator(wrapper, ansfile, keyfile, devfile, k, opt)
print e.__dict__

