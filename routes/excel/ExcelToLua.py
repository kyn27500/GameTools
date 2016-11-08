# -*- coding: utf-8 -*-
#Author: kyn
#Date: 2015-10-10
#Purpose: 解析excel数据表到lua

# excel 路径
# xls_path = "/Users/wangmeili/Documents/ExcelTolua"
xls_path = "/Users/wangmeili/Documents/workspace/nodejs/GameTools/test"
# lua文件导出的路径
lua_path = "/Users/wangmeili/Documents/workspace/nodejs/GameTools/test"

import os
import sys
import string
import xlrd
reload(sys)
sys.setdefaultencoding('utf8') 

tab = "	"
errorstr = "data error"
errorFlag = 0

# 按类型解析数据
dataType = {"number" : 1 ,"string" : 2 ,"array1" : 3}	#定义数据类别 array1：一维数组

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
def checkTableSize():
	data = xlrd.open_workbook("/Users/wangmeili/Documents/workspace/nodejs/GameTools/test/004.xlsx")
	pTabData = data.sheet_by_index(0)		#通过索引顺序获取
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

# 获取表格数据
def getDataByExcel(pRow,pCol):
	data = xlrd.open_workbook("/Users/wangmeili/Documents/workspace/nodejs/GameTools/test/004.xlsx")
	pTabData = data.sheet_by_index(0)		#通过索引顺序获取

	ret = {}
	for row in range(pRow):
		ret[row]={}
		for col in range(pCol):
			ret[row][col] = pTabData.cell(row+3,col+1).value
	return ret

def parseDataByType( dType , cell ):
	
	ctype = split(dType)
	cType = cell.ctype 		# 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
	cValue = cell.value

	if cmp(str(dType[1]),"yes") == 0:
		if cType == 0:
			errorFlag = 1
			return errorstr
	else:
		if cType == 0:
			return "nil"

	if dataType[dType[0]] == 1:
		if cType == 1:
			return int(cValue.strip())
		elif cType == 2:
			return int(cValue)
	elif dataType[dType[0]] == 2:
		return "\"%s\"" % (cValue)
	elif dataType[dType[0]] == 3:
		return "{%s}" % (cValue)

# 写文件
def writeToLua(filePath,fileKeys,fileContent):
	# filePath = filePath.replace("\\\\","/")

	fDirPath = os.path.dirname(filePath)
	fDirPath = fDirPath.replace(xls_path,lua_path)
	if not os.path.exists(fDirPath):
		os.mkdir(fDirPath)

	fileName = "DB_%s" % (filePath[filePath.rindex("\\")+1:filePath.find(".")].capitalize())

	fileStart ='''
-- Filename: %s.lua
-- Author: auto-created by kong`s ParseExcel(to lua) tool.
-- methods: X.keys = {}, X.getDataById(id), X.getArrDataByField(fieldName, fieldValue)
-- Function: no description.\n
'''
	fileStart = fileStart % (fileName)

	fileEnd = '''
%s = DB_Template.new (keys, data)
return %s
'''
	fileEnd = fileEnd % (fileName,fileName)

	fileStr = fileStart + fileKeys + fileContent + fileEnd

	filePath = os.path.join(fDirPath,"%s.lua" % (fileName))
	f = open(filePath,"w")
	f.write(fileStr)
	f.close()

# 读取 excel 表
def parseExcel(filePath):
	fileContent = "local data = {\n"
	fileKeys = "local keys = {\n" + tab
	data = xlrd.open_workbook(filePath)
	# table = data.sheets()[0]          #通过索引顺序获取
	table = data.sheet_by_index(0)		#通过索引顺序获取

	nrows = table.nrows

	ncols = table.ncols

	# get file keys 
	for col in range(ncols):
		if table.cell(1,col).ctype == 0:
				continue
		fileKeys = "%s\"%s\"," % (fileKeys,str(table.cell(2,col).value).strip())
	fileKeys = "%s\n}\n\n" % (fileKeys[0:-1])

	# get file content
	for row in range(3,nrows):
		rowStr = ""
		for col in range(ncols):
			# 该列类型为空，直接返回
			if table.cell(1,col).ctype == 0:
				continue
			# 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
			cell = table.cell(row,col)
			dataType = table.cell(1,col).value
			if col == 0:
				dataType = "number_yes"
			curValue = parseDataByType(dataType,cell)

			if col == 0:
				rowStr = "id"+str(curValue)+" = {"
			
			rowStr = "%s %s," % (rowStr,curValue)

		if errorFlag == 1:
			break
		rowStr = "%s%s},\n" % (tab,rowStr[0:-1])
		fileContent = fileContent + rowStr
	fileContent = "%s\n}\n" % (fileContent[0:-2])

	writeToLua(filePath,fileKeys,fileContent)
    
if __name__ == '__main__':

	if not os.path.exists(lua_path):
		os.mkdir(lua_path)

	# findAllFile(xls_path,parseExcel)

	# print(split("number_yes"))
	size = checkTableSize()
	data = getDataByExcel(size[0],size[1])
	print(data)



