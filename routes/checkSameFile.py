
 #coding=utf-8
'''
检测文件夹下是否有相同文件
原理：先检测文件大小，然后大小一致的文件会进行MD5值对比，最终得到文件一样
作者：kongyanan
时间：2015-06-07
'''


import os
import sys


# 当前路径
findPath = os.getcwd()
#文件路径修改
#findPath = "D:\\SVN\\client\\BubbleAli\\res"

files = {}


def getFileMd5(filePath):
    file = open(filePath ,'rb')
    import hashlib
    md5=hashlib.md5(file.read()).hexdigest()
    file.close()
    return md5

def list_cwd( dirPath ):
    return os.listdir(dirPath)

def findfiles ( dirPath ):

    for k in list_cwd(dirPath):
        filePath = os.path.join(dirPath,k)
        
        if os.path.isdir(filePath):
            findfiles(filePath)
        else:
#             print(filePath)
            if not (filePath.find(".svn") > 0 or filePath.find(".DS_Store") > 0):
                size = os.path.getsize(filePath)
                arr= files.get(size)
                if arr:
                    files[size].append(filePath)
                else:
                    files[size] = [filePath]

def checksamefile():
    
    for size,arr in files.items():
        if len(arr) > 1:
            md5s = {}
            
            for path in arr:
                md5 = getFileMd5(path)
                if md5s.get(md5):
                    md5s[md5].append(path)
                else:
                    md5s[md5] = [path]
            
            for md5key,pathArr in md5s.items():
                if len(pathArr) > 1:
                    print("******************************")
                    count = 1
                    for p in pathArr:
                        print("%s:%s" % (count,p))
                        count = count + 1
# 
def test(findPath):
    findfiles(findPath)
    checksamefile()

# svn 更新功能
def svnupdate(findPath):
    import svn
    svn.svnupdate()

if __name__ == '__main__':
    
    # 获取外部传入的参数
    if len(sys.argv)==2:
        findPath = sys.argv[1]
    test(findPath)

    print("search over !")
# raw_input()
                
