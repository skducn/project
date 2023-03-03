# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-12-21
# Description: 读取抖音口令watchword.txt
# fileinput用法：http://www.51testing.com/html/50/n-7794050.html

# watchword = "https://www.douyin.com/video/7151241259796008222"
#***************************************************************

from DyPO import *
douyin = DyPO()

import fileinput

with fileinput.input(files=('url.txt',), openhook=fileinput.hook_encoded('utf-8', 'surrogateescape')) as file:
    for line in file:
        # print(line)
        id = str(line).split("https://v.douyin.com/")[1].split('/')[0]
        vUrl = "https://v.douyin.com/" + id


douyin.downVideo(vUrl, "d:/11/44")




