
#coding=utf-8
#Author: kyn
#Date: 2015-10-10
#Purpose: 解析excel数据表到lua

# excel 路径
xls_path = "/Users/wangmeili/Documents/ExcelTolua"
# lua文件导出的路径
lua_path = xls_path

import os
import sys
import string
import xlrd

def findAllFile(dirPath,callback):
	fileList = os.listdir(dirPath)
	for f in fileList:

		filePath = os.path.join(dirPath,f)

		if os.path.isdir(filePath):
			findAllFile(filePath)
		else:
			if string.find(f,".xls") > -1 or string.find(f,".xlsx") > -1:
				callback(filePath)


dataType = {"number" : 1 ,"string" : 2 ,"array1" : 3}	#定义数据类别 array1：一维数组
def parseDataByType( dType ,dData):
	dType.lower()
	print(dType + "      "+dData)
	if dType.find("-") != -1:
		dType = dType.split("-")
	elif dType.find("_") != -1:
		dType = dType.split("_")

	if cmp(str(dType[1]),"yes") == 0:
		if cmp(dData,"nil") == 0:
			print("")
			return "value error"
	else:
		if cmp(dData,"nil") == 0:
			return dData
	
	if dataType[str(dType[0])] == 1:
		return dData
	elif dataType[str(dType[0])] == 2:
		return "\" %s \"" % (dData)
	elif dataType[str(dType[0])] == 3:
		return "{%s}" % (dData)

tabSpace = "	"
def parseExcel(filePath):
	fileContent = ""

	data = xlrd.open_workbook(filePath)
	# table = data.sheets()[0]          #通过索引顺序获取
	table = data.sheet_by_index(0)		#通过索引顺序获取

	nrows = table.nrows

	ncols = table.ncols

	for row in range(3,nrows):
		rowStr = "id"+str(row)+" = {"
		for col in range(ncols):
			# 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
			if table.cell(row,col).ctype == 0 or table.cell(1,col).value == "":
				pass
			curValue = parseDataByType(table.cell(1,col).value,str(table.cell(row,col).value))
			print(str(row)+","+str(col)+tabSpace+tabSpace+str(table.cell(row,col).ctype)+tabSpace+str(table.cell(row,col).value))
			# print table.cell(row,col).ctype
			# print table.cell(row,col).value


	return fileContent
    
if __name__ == '__main__':
	findAllFile(xls_path,parseExcel)
