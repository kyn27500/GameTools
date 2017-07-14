
# -*- coding: utf-8 -*- 
# 0.更新文件 1.修改名称“项目名-版本号” 2.打包 3.更新版本信息
# author: kongyanan
# date : 2017 - 07 - 14

import sys
import os
import json
import shutil
import subprocess


# 游戏根目录
m_game_root = "/Users/koba/Documents/workspace/svn_diff_game/LifeWinner"
# 最新版本文件
m_lua_version = os.path.join(m_game_root,"src/minimal/GameVersion.lua")
# 版本更新根目录
m_version_root = "/usr/local/Cellar/nginx/1.10.1/html/hot_update/LifeWinner"
#  版本文件地址
m_version_file = os.path.join(m_version_root,"index.html")
# 命令
m_cmd = "cocos run -p android -s "+ m_game_root
# 包名
m_apk_name = "LifeWinner"

def svnupdate(dirPath):
	import svn
	return svn.svnupdate(dirPath)
def svncommit(filePath):
	import svn
	return svn.svncommit(filePath)

def copy(resouse,copyto):
	import copyfile
	copyfile.copyImage(resouse,copyto)

def writeFile(filePath,fileData):
	f = open(filePath,"w")
	f.write(fileData)
	f.close()

def readFile(filePath):
	f = open(filePath,"r")
	fileData = f.read()
	f.close()
	return fileData

def updateVersionFile(pVersionFile):

	pVersionFile["package_name"]= "%s-%s.apk" % (m_apk_name,pVersionFile['publish_version'])

	# apk生成路径
	originPath = os.path.join(m_game_root,"frameworks/runtime-src/proj.android/bin/%s-debug.apk" % (m_apk_name))
	targetPath = os.path.join(m_version_root,pVersionFile["package_name"])
	open(targetPath, "wb").write(open(originPath, "rb").read()) 
	# 保存svn版本号
	
	pVersionFile["filesize"] = os.path.getsize(targetPath)
	pVersionFile["versions"]=[]
	writeFile(m_version_file,json.dumps(pVersionFile,sort_keys=True,indent=4))
	# print "版本信息上传成功！版本号：" + str(pVersionFile['publish_version'])

# 打包前 更新lua版本文件
def updateLuaScriptVersion(code):
	fileStr = readFile(m_lua_version)
	startPos = fileStr.find("publish_version")
	endPos = fileStr.find(",",startPos)
	tmpStr = fileStr.replace(fileStr[startPos:endPos],"publish_version="+str(code))
	writeFile(m_lua_version,tmpStr)
# 执行系统命令
def execSys(cmd):
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# for line in p.stdout.readlines():
	#     print line
	retval = p.wait()
	return retval,p.stdout.read()

def package():
	ret = execSys(m_cmd)
	if ret[0]==0:
		return True
	return False

if  __name__ ==  "__main__":

	_isUsedSvn = False

	# 获取外部传入的参数
	if len(sys.argv)==6:
		# 游戏根目录
		m_game_root = sys.argv[1]
		# 最新版本文件
		m_lua_version = os.path.join(m_game_root,"src/minimal/GameVersion.lua")
		# 版本更新根目录
		m_version_root = sys.argv[2]
		#  版本文件地址
		m_version_file = os.path.join(m_version_root,"index.html")
		# 命令
		m_cmd = "cocos compile -p android -s "+ m_game_root
		# 包名
		m_apk_name = sys.argv[3]

		_isUsedSvn = True

		# 更新文件目录
		m_newsvn_path = sys.argv[4].split(",")
		# 对比 老文件目录
		m_diff_old_path = sys.argv[5]

	if not os.path.exists(m_version_file):
		originalFile = os.path.join(os.getcwd(),"lib/version.html")
		open(m_version_file, "wb").write(open(originalFile, "rb").read()) 

	# 1.更新svn 
	if _isUsedSvn:
		svnupdate(m_game_root)

	# 2.设置版本号
	versironFile = json.loads(readFile(m_version_file))
	versironFile['publish_version'] += 1
	updateLuaScriptVersion(versironFile['publish_version'])

	# 3.打包
	isSuccess = package()

	if isSuccess:
		# 4.设置版本信息
		updateVersionFile(versironFile)
		if _isUsedSvn:
			# 5.提交svn 
			svncommit(m_lua_version)
			# 6.拷贝最新脚本到对比 目录中，以便下次脚本对比，使用最新的脚本

			# 清空对比老文件
			if os.path.exists(m_diff_old_path):
				shutil.rmtree(m_diff_old_path)
			os.makedirs(m_diff_old_path)

			for k in range(1,len(m_newsvn_path)):
				tmp_svnPath = os.path.join(m_newsvn_path[0],m_newsvn_path[k])
				tmp_diffPath = os.path.join(m_diff_old_path,m_newsvn_path[k])

				if not os.path.exists(tmp_diffPath):
					os.makedirs(tmp_diffPath)

				copy(tmp_svnPath,tmp_diffPath)

		print "普天同庆，打包成功！包名：%s，大小：%.2fM" % (versironFile["package_name"],versironFile["filesize"]/1000000.00)

	else:
		print "打包失败，请找相关人员解决！"

	
