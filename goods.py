#!/usr/bin/env python
#coding: utf-8
'''
商品业务逻辑
'''
__author__ = 'Cui.D.H'

import sys, os, time, atexit, string
from signal import SIGTERM
from multiprocessing import Process
from time import sleep
from core.MySQL import MySQL


class Goods(Process):
    def run(self):
        while True:
            print 'goods ' + time.ctime()
            sleep(5)

