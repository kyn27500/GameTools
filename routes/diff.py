
# -*- coding: utf-8 -*- 
# 检测出差异文件， 
# author: kongyanan
# date : 2015 - 07 - 30

import sys
import os
import hashlib
import shutil
import time
import json
from zipfile import *
import zipfile

# 上版本文件
m_old_path = os.path.join(os.getcwd(),"diff/old")
# 最新版本文件
m_new_path = os.path.join(os.getcwd(),"diff/new")
# 差异文件
m_diff_path = os.path.join(os.getcwd(),"diff/hot_update")
# 打包的差异文件
m_zip_path = os.path.join(os.getcwd(),"public/hot_update")
# 版本更新文件
m_version_file = os.path.join(os.getcwd(),"public/version.html")


m_config_name = "config.kongyanan" 

class FileObj(object):
	"""文件处理"""
	def __init__(self, path ):
		super(FileObj, self).__init__()
		self.path = path

	def getPath(self):
		return self.path

	def getMd5(self):
		if os.path.isfile(self.path):
			f = open(self.path,'rb')
			fileStr = f.read()
			m = hashlib.md5(fileStr)
			self.md5 = m.hexdigest()
			f.close()
			return self.md5



class  FileTool(object):
	"""docstring for  FileTool"""
	def __init__(self, dirPath):
		super( FileTool, self).__init__()
		self.dirPath = dirPath
		self.configPath = os.path.join(dirPath,m_config_name)

	def getFileMap(self):
		tempMap = {}
		if os.path.exists(self.configPath):
			configfile = open(self.configPath)
			tempMap = eval(configfile.read())
			configfile.close()
			return tempMap
		else:
			self.findAllFile(self.dirPath,tempMap)
			self.saveConfigFile(tempMap)
			return tempMap

	def findAllFile(self,dirPath,tempMap):
		fileslist = os.listdir(dirPath)
		for f in fileslist:
			if f == m_config_name:
				pass
			fpath = os.path.join(dirPath,f)
			if os.path.isdir(fpath):
				if f[0] == '.':
					pass
				else:
					self.findAllFile(fpath,tempMap)
			else:
				if f == ".DS_Store":
					pass
				else:
					fb = FileObj(fpath)
					tempMap[fpath] = fb.getMd5()

	def saveConfigFile( self ,configMap ):

		f = open(self.configPath,"w")
		f.write(str(configMap))
		f.close()


def dealFile(newPath , count):
	oldPath = newPath.replace(m_new_path,m_old_path)
	diffPath = newPath.replace(m_new_path,m_diff_path)
	if os.path.exists(oldPath):
		os.remove(oldPath)

	if not os.path.exists(os.path.dirname(oldPath)):
		os.makedirs(os.path.dirname(oldPath))

	if not os.path.exists(os.path.dirname(diffPath)):
		os.makedirs(os.path.dirname(diffPath))	

	shutil.copyfile(newPath,oldPath)
	shutil.copyfile(newPath,diffPath)

	count = count + 1
	# print("%s:%s" % (str(count),diffPath.replace(m_diff_path+"/","")))
	return count

def dozip():
	zipName = str(int(time.time()))+".zip"
	f = zipfile.ZipFile(os.path.join(m_zip_path,zipName),'w',zipfile.ZIP_DEFLATED)
	for dirpath, dirnames, filenames in os.walk(m_diff_path):
		for filename in filenames:
			# f.write(os.path.join(dirpath,filename))
			abs_path = os.path.join(os.path.join(dirpath, filename))
			rel_path = os.path.relpath(abs_path,os.path.dirname(m_diff_path))
			f.write(abs_path, rel_path)

	f.close()


	# print("\nzip name:%s" % zipName)
	# print("zip size:%d " % os.path.getsize(os.path.join(m_zip_path,zipName)))
	# print("zip finish time:" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
	global zip_info
	zipSize = str(os.path.getsize(os.path.join(m_zip_path,zipName)))
	zip_info = [zipName,zipSize]

def svnupdate(dirPath):
	import svn
	return svn.svnupdate(dirPath)

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

def updateVersionFile():
	# 保存svn版本号
	versionFile = json.loads(readFile(m_version_file))

	versionFile['script_version'] += 1 

	scriptInfo = {
		"ver":versionFile['script_version'],
		"size":zip_info[1],
		"files":zip_info[0],
		"compel":"0",
		"path":"hot_update"
	}
	versionFile["versions"].append(scriptInfo)
	writeFile(m_version_file,json.dumps(versionFile,sort_keys=True,indent=4))
	print "版本信息上传成功！脚本版本号：" + str(versionFile['script_version'])

if  __name__ ==  "__main__":

	_isUsedSvn = False
	zip_info = []
	# 获取外部传入的参数
	if len(sys.argv)==7:
		m_old_path = sys.argv[1]
		m_new_path = sys.argv[2]
		m_diff_path= sys.argv[3]
		m_zip_path = sys.argv[4]
		m_newsvn_path = sys.argv[5].split(",")
		m_version_file = sys.argv[6]
		_isUsedSvn = True

	# 清理new文件夹下的config文件
	new_config_path = os.path.join(m_new_path,m_config_name)
	if os.path.exists(new_config_path):
		# print("-- clean up :" + new_config_path)
		os.remove(new_config_path)

	# 清空差异文件夹
	if os.path.exists(m_diff_path):
		shutil.rmtree(m_diff_path)
	os.makedirs(m_diff_path)

	if not os.path.exists(m_old_path):
		os.makedirs(m_old_path)
	if not os.path.exists(m_new_path):
		os.makedirs(m_new_path)
	if not os.path.exists(m_zip_path):
		os.makedirs(m_zip_path)
	if not os.path.exists(m_version_file):
		originalFile = os.path.join(os.getcwd(),"lib/version.html")
		open(m_version_file, "wb").write(open(originalFile, "rb").read()) 

	# 更新svn 并拷贝文件到 对比文件夹中
	if _isUsedSvn:
		for k in range(1,len(m_newsvn_path)):
			tmp_svnPath = os.path.join(m_newsvn_path[0],m_newsvn_path[k])
			tmp_diffPath = os.path.join(m_new_path,m_newsvn_path[k])

			if not os.path.exists(tmp_diffPath):
				os.makedirs(tmp_diffPath)

			svnupdate(tmp_svnPath)	
			copy(tmp_svnPath,tmp_diffPath)

	# 旧版本 文件
	oldFileTool = FileTool(m_old_path)
	oldmap = oldFileTool.getFileMap()
	# 新版本文件
	newFileTool = FileTool(m_new_path)
	newmap = newFileTool.getFileMap()

	# 对比
	count = 0
	for key in newmap:
		oldkey = key.replace(m_new_path,m_old_path)

		if oldmap.has_key(oldkey):
			if newmap.get(key) != oldmap.get(oldkey):
				oldmap[oldkey] = newmap.get(key)
				count = dealFile(key,count)

		else:
			oldmap[oldkey] = newmap.get(key)
			count = dealFile(key,count)

	if count ==0:
		print("无差异文件!")
	else:	
		# 保存当前文件md5配置
		oldFileTool.saveConfigFile(oldmap)
		# 打包
		dozip()
		print "差异文件打包成功！	包名："+zip_info[0]+"		大小："+zip_info[1]+"	字节"
		# 更新版本文件
		updateVersionFile()

	# raw_input()
