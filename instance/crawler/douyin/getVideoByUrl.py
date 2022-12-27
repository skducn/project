# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-21
# Description: 读取抖音口令watchword.txt
# fileinput用法：http://www.51testing.com/html/50/n-7794050.html
#***************************************************************

from DyPO import *
douyin = DyPO()

import fileinput

with fileinput.input(files=('url.txt',), openhook=fileinput.hook_encoded('utf-8', 'surrogateescape')) as file:
    for line in file:
        # print(line)
        watchword = str(line).split("https://v.douyin.com/")[1].split('/')[0]

print(watchword)
douyin.getVidoeByPhone(watchword, "d:\\11")
print("\n已完成")




