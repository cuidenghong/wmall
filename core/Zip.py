#!/usr/bin/env python
#coding: utf-8
"""
文件打包
"""
import os,sys
import zipfile

class Zip:

    def __init__(self,dirname, zipfilename):
        filelist = []
        fulldirname = os.path.abspath(dirname)
        fullzipfilename = os.path.abspath(zipfilename)
        print "Start to zip %s to %s ..." % (fulldirname, fullzipfilename)
        #判断目录是否存在
        if not os.path.exists(fulldirname):
            print "Dir/File %s is not exist, Press any key to quit..." % fulldirname
            inputStr = raw_input()
            return
        #判断压缩文件是否存在
        if os.path.isdir(fullzipfilename):
            tmpbasename = os.path.basename(dirname)
            fullzipfilename = os.path.normpath(os.path.join(fullzipfilename, tmpbasename))

        #Get file(s) to zip ...
        if os.path.isfile(dirname):
            filelist.append(dirname)
            dirname = os.path.dirname(dirname)
        else:
            #get all file in directory
            for root, dirlist, files in os.walk(dirname):
                for filename in files:
                    filelist.append(os.path.join(root,filename))

        #Start to zip file ...
        destZip = zipfile.ZipFile(fullzipfilename, "w")
        for eachfile in filelist:
            destfile = eachfile[len(dirname):]
            print "Zip file %s..." % destfile
            destZip.write(eachfile, destfile)
        destZip.close()

        return true

    def unzip_dir(zipfilename, unzipdirname):
        fullzipfilename = os.path.abspath(zipfilename)
        fullunzipdirname = os.path.abspath(unzipdirname)
        print "Start to unzip file %s to folder %s ..." % (zipfilename, unzipdirname)
        #Check input ...
        if not os.path.exists(fullzipfilename):
            print "Dir/File %s is not exist, Press any key to quit..." % fullzipfilename
            inputStr = raw_input()
            return
        if not os.path.exists(fullunzipdirname):
            os.mkdir(fullunzipdirname)

        #Start extract files ...
        srcZip = zipfile.ZipFile(fullzipfilename, "r")
        for eachfile in srcZip.namelist():
            print "Unzip file %s ..." % eachfile
            eachfilename = os.path.normpath(os.path.join(fullunzipdirname, eachfile))
            eachdirname = os.path.dirname(eachfilename)
            if not os.path.exists(eachdirname):
                os.makedirs(eachdirname)
            fd=open(eachfilename, "wb")
            fd.write(srcZip.read(eachfile))
            fd.close()
        srcZip.close()

        return true