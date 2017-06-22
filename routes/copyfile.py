# -*- coding: utf-8 -*-
import os
import sys
import shutil



def copyImage(pPath,newPath):

	for file in os.listdir(pPath):
		sourceFile = os.path.join(pPath,file)
		targetFile = os.path.join(newPath,file)
		if os.path.isfile(sourceFile):
			if not (sourceFile.find(".svn") > 0 or sourceFile.find(".DS_Store") > 0):
				# print(targetFile)
				open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
		else:
			if not (sourceFile.find(".svn") > 0 or sourceFile.find(".DS_Store") > 0):
				# print(targetFile)
				if not os.path.exists(targetFile):
					# print(targetFile)
					os.makedirs(targetFile)
				copyImage(sourceFile,targetFile)

def main():

	# print(sys.argv)
	oldPath = sys.argv[1]
	newPath = sys.argv[2]

	if not os.path.exists(newPath):
		os.makedirs(newPath)
	
	print("\n开始拷贝...")
	copyImage(oldPath,newPath)
	print("\n拷贝结束...")

if __name__ == '__main__':
	main()