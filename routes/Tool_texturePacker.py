#coding=utf-8
# 资源打包工具
# Create by kongyanan at 2017-05-22
# 
# TexturePacker 
# --format cocos2d
# --data a.plist 
# --sheet a.png 
# --texture-format png
# --size-constraints AnySize 
# --opt RGBA4444
# --trim
# --enable-rotation
# --smart-update

import os
import sys

# 可修改变量*************************************************

# 资源目录
sourcePath = "/Users/koba/Documents/res/"
# 目标目录
targetPath = "/Users/koba/Documents/res1/"
# 忽略文件夹
ignoreDir = ["font","shader","sound","error"]
# 忽略文件
ignoreFile = []
# 图片多，需要生成N张plist
moreDir = ["PNG","help"] 

# 通用参数
params = "--format cocos2d-v2 --texture-format png  --size-constraints AnySize  --opt RGBA8888 --trim --smart-update --enable-rotation"
# 打包指令
cmd = "TexturePacker %s --data %s.plist  --sheet %s.png "+params
cmds = "TexturePacker %s --multipack --data %s{n}.plist  --sheet %s{n}.png "+params
# 数据分组
res_data={}
res_dir = {}

# 公共方法*************************************************** 
# 查找文件
def findfiles (dirPath,callback):
    for k in os.listdir(dirPath):
        filePath = os.path.join(dirPath,k)
        if os.path.isdir(filePath) and k not in ignoreDir:
			res_dir[k] = filePath
			findfiles(filePath,callback)
        else:
            if not (filePath.find(".svn") > 0 or filePath.find(".DS_Store") > 0):
            	callback(filePath,dirPath.split("/")[-1])


# 资源整理**************************************************************************

# 添加数据到分组
def addFileList(filePath,parentDir):
	if filePath.endswith(".png"):
		if res_data.has_key(parentDir):
			res_data[parentDir].append(filePath)
		else:
			res_data[parentDir]=[]
			res_data[parentDir].append(filePath)

# 打包图片
def packerPng(resData):

	for name in resData:
		filePath = targetPath + name
		print("-------->正在生成文件："+filePath)
		pngFileStr = ""
		for png in resData[name]:
			pngFileStr += png+" "

		if name in moreDir:
			os.system(cmds%(pngFileStr,filePath,filePath))
		else:	
			os.system(cmd%(pngFileStr,filePath,filePath))

if __name__ == '__main__':

	# 获取res和src下的资源文件
	findfiles(sourcePath,addFileList)

	if not os.path.exists(targetPath):
		os.makedirs(targetPath)
	packerPng(res_data)

	print("\n---------------- 打包完成 ----------------")

