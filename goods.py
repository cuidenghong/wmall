#!/usr/bin/env python
#coding: utf-8
'''
商品业务逻辑
'''
__author__ = 'Cui.D.H'

import sys, os, time, atexit, string
import json
import urllib
from signal import SIGTERM
from multiprocessing import Process
from time import sleep
from core.MySQL import MySQL
from core.MyRedis import MyRedis
from core.Zip import Zip

class Goods(Process):

    __db =  MySQL()
    __redis = MyRedis()
    __imgDir = '/mnt/hgfs/www/python/wmall/download/'
    __uploadUrl = 'http://t.pic.dodoca.com/'

    def run(self):
        while True:
            #获取队列
            lists = self.getGoodsQueue()
            if lists:
                #获取商品信息
                goodsInfo = self.getGoodsInfo(lists['goodsId'])
                userid = lists['userid']
                goodsId = goodsInfo[0][0]
                if goodsId:
                    #获取图片信息
                    picInfo = self.getPicInfo(goodsId)
                    if picInfo:
                        for pic in picInfo:
                            imgUrl = pic[0]
                            if imgUrl:
                                filename = imgUrl.split('/')
                                filename = filename[-1]
                                #下载图片
                                self.getPic(imgUrl,filename,userid)
                        #图片打包
                        dirname = self.__imgDir + userid
                        zipfilename = dirname + '/' + userid + '.zip'
                        zip = Zip()
                        zip.zip_dir(dirname,zipfilename)

                print 'goods ' + time.ctime()
            else:
                print 'is not goods'
            sleep(5)

    """
    从redis获取list
    """
    def getGoodsQueue(self):
        sKey = 'goods_queue'
        lists = self.__redis.lpop(sKey)
        if lists:
            return json.loads(lists)

    """
    从数据库获取商品信息
    """
    def getGoodsInfo(self,goodsId):
        if goodsId:
            sql = "select pic_id from wx_goods where id = %s " % goodsId
            rs = self.__db.query(sql)
            return self.__db.fetchAllRows()
        else:
            return False

    """
    查询图片信息
    """
    def getPicInfo(self,id):
        if id:
            sql = "select org from pic_data where id in (%s)  " % id
            rs = self.__db.query(sql)
            return self.__db.fetchAllRows()
        else:
            return False

    """
    下载图片保存到本地
    """
    def getPic(self,imgUrl,filename,userid):
        if imgUrl:
            #判断文件目录是否存在
            if not os.path.exists(self.__imgDir + userid):
                os.makedirs(self.__imgDir + userid)
            imgDir = self.__imgDir + userid + '/' + filename
            imgUrl = self.__uploadUrl + imgUrl
            try:
                 urllib.urlretrieve(imgUrl,imgDir)
            except:


