#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import sys


class ColorLogger(object):
    
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self, mode):
        if mode is None:
            self.disable()
        self.mode = mode

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class SemevalLogger(ColorLogger):

    def __init__(self, ts, devs, wrapper_type, mode):
        super(SemevalLogger, self).__init__(mode)
        self.header = "sys:{}, gold:{}, dev_s:{}, dev_g:{}, wrapper:{}".format(
                      ts.data, ts.target, devs.data, devs.target, wrapper_type)

    def error(self, message):
        if self.mode >= 1:
            #msg = "ERROR: {}\t{}".format(self.header, message),
            msg = "ERROR: {}".format(message),
            #FIXME: Why tuple msg
            print >> sys.stderr, self.FAIL, msg[0], self.ENDC


    def warning(self, message):
        if self.mode >= 2:
            #msg = "WARNING: {}\t{}".format(self.header, message),
            msg = "WARNING: {}".format(message),
            #FIXME: Why tuple msg
            print >> sys.stderr, self.WARNING, msg[0], self.ENDC

    def info(self, message):
        if self.mode >= 3:
            msg = "INFO: {}".format(message),
            #msg = "INFO: {}\t{}".format(self.header, message),
            #FIXME: Why tuple msg
            print >> sys.stderr, self.OKGREEN, msg[0], self.ENDC
    
    def init(self, message):
        if self.mode >= 3:
            #msg = "INFO: {}".format(message),
            msg = "INIT: {}\t{}".format(self.header, message),
            #FIXME: Why tuple msg
            print >> sys.stderr, self.OKBLUE, msg[0], self.ENDC

def main():
    pass

if __name__ == '__main__':
    main()

