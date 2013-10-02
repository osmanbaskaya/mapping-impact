#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from classifier_eval import SemevalEvaluator
from itertools import izip, count
from classifier import SVCWrapper
from logger import SemevalLogger


ansfiles = ['dummy.key',]
keyfiles = ['dummy.key',]
devfiles = ['dummy.key',]
k = 10
opt = True #optimization
wrappers = [SVCWrapper(),]

counter = count(0)

debug_mode = 3
for i, ans, key, dev in izip(counter, ansfiles, keyfiles, devfiles):
    for j, w in enumerate(wrappers):
        logger = SemevalLogger(ans, key, dev, w.name, debug_mode)
        e = SemevalEvaluator(w, ans, key, dev, k, optimization=True, logger=logger)
        scores = e.score()
        print scores['book.v']
        exit()
        e.cls_wrapper.classifier.optimize()
        e.report()
