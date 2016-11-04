# -*- coding: utf-8 -*- 
# svn 工具
# author: kongyanan
# date : 2016-11-03

import os
import sys
import re
import subprocess

# svn路径(测试使用)
svnPath = "/Users/koba/Documents/workspace/testsvn/src"
# svnPath = "/Users/koba/Documents/mobile_client/SYC_client"



# 执行系统命令
def execSys(cmd):
	
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# for line in p.stdout.readlines():
	#     print line,
	retval = p.wait()
	return retval,p.stdout.read()

# 获取最新版本号
def getVesionCode(pSvnPath):
	cmd_svninfo = "svn info " + pSvnPath + " | grep Revision"
	ret = execSys(cmd_svninfo)
	if ret[0] == 0:
		return ret[1][10:]

#更新
def svnupdate(pSvnPath):
	cmd_svnupdate = "svn update " + pSvnPath + " | grep revision"
	ret = execSys(cmd_svnupdate)

	if ret[0]==0:
		return ret[1][12:-2]
def svncommit(pSvnPath):

	svnadd(svnPath)

	cmd_svnupdate = "svn commit " + pSvnPath + "/* -m 'robot commit' | grep revision"

	ret = execSys(cmd_svnupdate)

	if ret[0]==0:
		return ret[1][19:-2]

def svnadd(pSvnPath):
	cmd_svnadd = "svn add " + pSvnPath + "/*"
	ret = execSys(cmd_svnadd)
	return ret[1]

def test():
	print("test----------------")
	# str1 = getVesionCode(svnPath)
	# str1 = svnadd(svnPath)
	str1 = svncommit(svnPath)
	print "当前版本号：" + str1

if __name__ == '__main__':
	test()