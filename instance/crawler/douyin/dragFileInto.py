# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-21
# Description: 将文件拖入dragFileInto.bat 后下载
# 用法：
# 1，将文件名改为 h43oYWf ， 如 'https://v.douyin.com/h43oYWf' 最后的id
# 2，将文件拖入 dragFileInto.bat
# 3，完成下载
#***************************************************************


from DyPO import *
douyin = DyPO()


print("下载中...")
douyin.getVidoeByPhone(os.path.split(sys.argv[1])[1], "d:\\11")

print("\n已完成")




