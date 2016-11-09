import py_compile
import sys
import os
# coding=utf-8
fileName = "ExcelToLua.py"
curDir = os.getcwd()


py_compile.compile(os.path.join(curDir,fileName))


# compileall.compile_dir(curDir)