# -*- coding: utf-8 -*-
#Author: kyn
#Date: 2015-10-10
#Purpose: 解析excel数据表到lua
import os
import sys
import string
import xlrd
import json
reload(sys)
sys.setdefaultencoding('utf8') 

# excel 路径
xls_path = "/Users/koba/Documents/workspace/kyn27500.game/xls"
# lua文件导出的路径
lua_path = "/Users/koba/Documents/workspace/kyn27500.game/db"

# svnVersionFile 文件
svn_version_file = os.path.join(os.getcwd(),"lib/LocalFile.json")


_errorDes = ["数据错误：","文件名","行数","列数"]
_isError = False

# 按类型解析数据
dataType = ["number","string","array1"]	#定义数据类别 array1：一维数组

# 查找所有 xls
def findAllFile(dirPath,callback):
	fileList = os.listdir(dirPath)
	for f in fileList:

		# 检查是否有错误
		if _isError:
			break

		filePath = os.path.join(dirPath,f)

		if f[0] == "." or f.find(".svn") > 0 or f.find(".DS_Store") > 0 or f.startswith("~$"):
			continue
	
		if os.path.isdir(filePath):
			findAllFile(filePath,callback)
		else:
			if f.endswith(".xls") or f.endswith(".xlsx"):
				# print(filePath)
				callback(filePath,f)

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

	global _isError,_errorDes
	# 获取表格默认大小
	nrows = pTabData.nrows
	ncols = pTabData.ncols

	retRow=0
	retCol=0
	# 检测行
	for row in range(nrows):
		cell = pTabData.cell(row,0)
		if cell.ctype>0:
			if row >= 3:
				if cell.value == row-2:
					retRow = row-2
				else:
					_isError = True
					_errorDes[0]="表头ID错误"
					_errorDes[2]=row+1
					_errorDes[3]=1
	# 检查列
	for col in range(ncols):
		cell = pTabData.cell(0,col)
		if cell.ctype>0:
			retCol = col


	return retRow,retCol

# 获取表格表头数据
def getTabTitleByExcel(pTabData,pCol):

	global _isError,_errorDes

	tabKey = []
	tabKeyType=[]
	for col in range(pCol):
		keyCell = pTabData.cell(2,col+1)
		typeCell = pTabData.cell(1,col+1)
		if keyCell.ctype == 0:
			tabKey.append("Error")

			_isError = True
			_errorDes[0]="表头错误"
			_errorDes[2]=3
			_errorDes[3]=col+2

		else:
			tabKey.append(keyCell.value)

		if typeCell.ctype == 0:
			tabKeyType.append(split("string-no"))

			_isError = True
			_errorDes[0]="表头错误"
			_errorDes[2]=2
			_errorDes[3]=col+2

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

# ******************************************************* 格式化输出数据
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
# *******************************************************

# 构造输出lua
def getLuaText(pTabTitle,pData,fileName):
	# 页面内容分四部分，介绍，keys,data,retrun template

	# 文件介绍
	luaFileName = "DB_%s" % (fileName.split(".")[0].capitalize())
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

	return luaFileName,fileStr

# lua文件数据内容整理
def parseData(pKeyType,pData):
	global _isError,_errorDes
	isFirst = not _isError
	ret = ""
	for row in range(len(pData)):
		item=[str(row+1)]

		for col in range(len(pData[1])):
			item.append(parseDataByType(pKeyType[col],pData[row][col]))
			if isFirst and _isError:
				_errorDes[2]=row+4
				_errorDes[3]=col+2
				isFirst = False
		fileItem = _fileDataItem%(row+1,", ".join(item))
		ret = ret+fileItem
	return ret

# 根据不同类型，返回相应数据（以后添加类型直接改这里）
def parseDataByType(pkeyType,pData):
	global _isError

	isMustHasData = pkeyType[1] == "yes"
	isHasData = pData != ''
	# 检测是否必填数据，但没有数据（漏写数据）
	if isMustHasData and (not isHasData):
		_isError = True
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
			# TODO 修改 数组模块
			# tmp=[]
			# for val in pData:
			# 	tmp.append(str(val))

			# return "{%s}" % ", ".join(tmp)
			if pData != 'nil':
				rrr = []
				vtmp = pData.split(',')
				if len(vtmp)>0:
					for i in range(len(vtmp)):
						print vtmp[i]
						vvtmp = vtmp[i].split('=')
						if len(vvtmp) == 2:
							fff = vvtmp[0]
							sss = ("\"%s\"" % (vvtmp[1].replace('\"','\\\"')))
							if sss == '"true"':
								sss = 'true'
							elif sss == '"false"':
								sss = 'false'
							if fff.isdigit() :
								rrr.append('['+str(fff)+']='+sss)
							else:
								rrr.append(str(fff)+'='+sss)
						else:
							rrr.append(str(vtmp[i]))
					pData = '{%s}' %','.join(rrr)
				else:
					pData = '{%s}' % (pData.replace('\"','\\\"'))

                return pData


# 写文件
def writeToLua(filePath,fileName,fileData):
	fDirPath = os.path.dirname(filePath)
	fDirPath = fDirPath.replace(xls_path,lua_path)
	if not os.path.exists(fDirPath):
		os.mkdir(fDirPath)
	filePath = os.path.join(fDirPath,"%s.lua" % (fileName))
	writeFile(filePath,fileData)

# 解析 excel
def parseExcel(filePath,fileName):
	# print(filePath,fileName)
	# 读取数据
	excel = xlrd.open_workbook(filePath)
	pTabData = excel.sheet_by_index(0)
	# 表格数据大小[行数，列数]
	tabsize = checkTableSize(pTabData)
	# 表格表头字段[表字段，表字段类型]
	tabTitle = getTabTitleByExcel(pTabData,tabsize[1])
	# excel数据部分[行][列]二维数组
	data = getDataByExcel(pTabData,tabsize[0],tabsize[1])
	# 解析后的数据[文件名，文件内容]
	filedata = getLuaText(tabTitle,data,fileName)
	# 写入文件
	writeToLua(filePath,filedata[0],filedata[1])
	# 打印刚写完的文件路径
	print(filePath)

	global _isError,_errorDes
	if _isError:
		_errorDes[1] = fileName

def print_test(a,b):
	print(a,b)

def svnupdate(dirPath):
	import svn
	return svn.svnupdate(dirPath)

def svncommit(dirPath):
	import svn
	svn.svnadd(dirPath)
	return svn.svncommit(dirPath)

def writeFile(filePath,fileData):
	f = open(filePath,"w")
	f.write(fileData)
	f.close()

def readFile(filePath):
	f = open(filePath,"r")
	fileData = f.read()
	f.close()
	return fileData

if __name__ == '__main__':

	isUsedSvn = False
	_isError = False
	xlsVersion = 0
	localFile = {}
	# 获取外部传入的参数
	if len(sys.argv)==3:
		xls_path = sys.argv[1]
		lua_path = sys.argv[2]
		isUsedSvn = True
		# 更新excel SVN
		xlsVersion = svnupdate(xls_path)

		svncommit(lua_path)

		# 检查版本号是否一致，减少转换
		if os.path.exists(svn_version_file):
			localFile = json.loads(readFile(svn_version_file))

	# 对比 svn版本号
	if localFile['excelSvnVersion'] == xlsVersion:
		print("Excel文件无任何修改，请提交SVN！	当前版本号： "+xlsVersion)
	else:	
		# 检查并创建目录
		if not os.path.exists(lua_path):
			os.makedirs(lua_path)

		# 生成模板文件
		templeFile = os.path.join(lua_path,"DB_Template.lua")
		if not os.path.exists(templeFile):
			sourceFile = os.path.join(os.getcwd(),"lib/DB_Template.lua")
			open(templeFile, "wb").write(open(sourceFile, "rb").read()) 

		# 扫描所有excel文件，并读取内容
		findAllFile(xls_path,parseExcel)
		# 检查是否有错误
		if _isError:
			print("%s:*********************************** 文件名：%s , %s行  %s列" % (_errorDes[0],_errorDes[1],_errorDes[2],_errorDes[3]))
		else:
			# TODO 提交svn
			print("数据转换完毕！")
			if isUsedSvn:
				version = svncommit(lua_path)
				if version:
					print("当前版本号：%s" % version)

				# 保存svn版本号
				localFile['excelSvnVersion'] = xlsVersion
				writeFile(svn_version_file,json.dumps(localFile,sort_keys=True,indent=4))

			



