# -*- coding: utf-8 -*-
#Author: kyn
#Date: 2015-10-10
#Purpose: 解析excel数据表到lua
import os
import sys
import string
import xlrd
reload(sys)
sys.setdefaultencoding('utf8') 

# excel 路径
# xls_path = "/Users/wangmeili/Documents/ExcelTolua"
xls_path = "/Users/koba/Documents/workspace/NodeJs/gametools/test"
# lua文件导出的路径
lua_path = "/Users/koba/Documents/workspace/NodeJs/gametools/test/out"
# 
testXlsx = "/Users/koba/Documents/workspace/NodeJs/gametools/test/004.xlsx"


_errorDes = "data error"
_isError = False

# 按类型解析数据
dataType = ["number","string","array1"]	#定义数据类别 array1：一维数组

# 查找所有 xls
def findAllFile(dirPath,callback):
	fileList = os.listdir(dirPath)
	for f in fileList:
		if f[0] == "." or not (sourceFile.find(".svn") > 0 or sourceFile.find(".DS_Store") > 0):
			continue
		filePath = os.path.join(dirPath,f)
		
		if os.path.isdir(filePath):
			findAllFile(filePath,callback)
		else:
			if string.find(f,".xls") > -1 or string.find(f,".xlsx") > -1:
				print(filePath)
				callback(filePath)

#分割字符串
def split(pData):
	pData = pData.lower()
	if pData.find("-") != -1:
		ret = pData.split("-")
	elif pData.find("_") != -1:
		ret = pData.split("_")
	return ret

# 检查表大小
def checkTableSize(pTabData):
	# 获取表格默认大小
	nrows = pTabData.nrows
	ncols = pTabData.ncols
	print(nrows,ncols)
	# 检测行
	for row in range(nrows):
		cell = pTabData.cell(row,0)
		if cell.ctype==2:
			if row >= 3:
				if cell.value == row-2:
					retRow = row-2
				# else:
				# 	return "ID 错误"
	# 检查列
	for col in range(ncols):
		cell = pTabData.cell(0,col)
		if cell.ctype==2:
			if col >= 1:
				if cell.value == col:
					retCol = col
				# else:
				# 	return "ID 错误"
	return retRow,retCol

# 获取表格表头数据
def getTabTitleByExcel(pTabData,pCol):
	tabKey = []
	tabKeyType=[]
	for col in range(pCol):
		keyCell = pTabData.cell(2,col+1)
		typeCell = pTabData.cell(1,col+1)
		if keyCell.ctype == 0:
			tabKey.append("Error")
		else:
			tabKey.append(keyCell.value)

		if typeCell.ctype == 0:
			tabKeyType.append("Error")
		else:
			tabKeyType.append(split(typeCell.value))

	return tabKey,tabKeyType

# 获取表格数据
def getDataByExcel(pTabData,pRow,pCol):
	ret = []
	for row in range(pRow):
		coltab=[]
		for col in range(pCol):
			coltab.append(pTabData.cell(row+3,col+1).value)
		ret.append(coltab)
	return ret


# 文件介绍
_fileDes='''-- Filename: %s.lua
-- Author: auto-created by kong`s ParseExcel(to lua) tool.
-- methods: X.keys = {}, X.getDataById(id), X.getArrDataByField(fieldName, fieldValue)
-- Function: no description.\n
'''
_fileKeys = "local keys = {\n\t\"%s\"\n}\n\n"
_fileData = "local data = {\n%s}\n\n"
_fileDataItem = "\tid%s={%s},\n"
_fileReturn = "%s = DB_Template.new (keys, data)\nreturn %s"

# 构造输出lua
def getLuaText(pTabTitle,pData,fileName):
	# 页面内容分四部分，介绍，keys,data,retrun template

	# 文件介绍
	luaFileName = "DB_%s" % (fileName.capitalize())
	fileStr1 = _fileDes%(luaFileName)
	# 文件keys
	fileStr2 = _fileKeys%('\",\"'.join(pTabTitle[0]))

	# 文件数据内容
	filedata = parseData(pTabTitle[1],pData)
	fileStr3 = _fileData%filedata
	# print(list(pTabTitle))

	# 文件返回
	fileStr4 = _fileReturn%(luaFileName,luaFileName)
	fileStr = fileStr1+fileStr2+fileStr3+fileStr4

	return fileStr

# lua文件数据内容整理
def parseData(pKeyType,pData):

	ret = ""
	for row in range(len(pData)):
		item=[str(row+1)]

		for col in range(len(pData[1])):
			item.append(parseDataByType(pKeyType[col],pData[row][col]))
		fileItem = _fileDataItem%(row+1,", ".join(item))
		ret = ret+fileItem
	return ret

# 根据不同类型，返回相应数据（以后添加类型直接改这里）
def parseDataByType(pkeyType,pData):
	
	isMustHasData = pkeyType[1] == "yes"
	isHasData = pData != ''

	# 检测是否必填数据，但没有数据（漏写数据）
	if isMustHasData and (not isHasData):
		return "errordata"
	elif(not isHasData):
		return "nil"
	else:

		# 数字
		if pkeyType[0] == dataType[0]:
			if int(pData) == pData:
				return str(int(pData))
			else:
				return str(pData)
		# 字符串
		elif pkeyType[0] == dataType[1]:
			return "\"%s\"" % pData
		# 数组
		elif pkeyType[0] == dataType[2]:
			tmp=[]
			for val in pData:
				tmp.append(str(val))

			return "{%s}" % ", ".join(tmp)


# 写文件
def writeToLua(filePath,fileName,fileData):


	fDirPath = os.path.dirname(filePath)
	fDirPath = fDirPath.replace(xls_path,lua_path)
	if not os.path.exists(fDirPath):
		os.mkdir(fDirPath)

	filePath = os.path.join(fDirPath,"%s.lua" % (fileName))
	f = open(filePath,"w")
	f.write(fileStr)
	f.close()


if __name__ == '__main__':

	if not os.path.exists(lua_path):
		os.mkdir(lua_path)


	data = xlrd.open_workbook(testXlsx)
	pTabData = data.sheet_by_index(0)		#通过索引顺序获取

	# findAllFile(xls_path,parseExcel)
	size = checkTableSize(pTabData)
	tabTitle = getTabTitleByExcel(pTabData,size[1])
	data1 = getDataByExcel(pTabData,size[0],size[1])
	# for i in range(pTabData.nrows):
	# 	print(pTabData.row_values(i))
	# print(size)
	# print(tabTitle)
	print(data1)

	fileStr = getLuaText(tabTitle,data1,"testExcel")
	writeToLua(lua_path,"testExcel",fileStr)
	print(fileStr)
