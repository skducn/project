# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2017-7-19
# Description: sh,http://amoffat.github.io/sh/
# sh is a full-fledged subprocess replacement for Python 2.6 - 3.5, PyPy and PyPy3 that allows you to call any program as if it were a function:
#***************************************************************

import sh

# 显示目录清单
print (sh.ls("-l", "/Users/linghuchong"))

# bake命令参数，显示当前目录的字节数
du = sh.du.bake('-shc')
print (du('/users/linghuchong//Downloads/51/Project/common'))

# glob列出文件
list=sh.glob('/users/linghuchong//Downloads/51/Project/common/*')
print(list)

# # 调用自己的程序
r = sh.Command('/Users/linghuchong/Downloads/51/Project/common/yaml1.py')
print(r)



# from sh import ifconfig
# print(ifconfig("wlan0"))


