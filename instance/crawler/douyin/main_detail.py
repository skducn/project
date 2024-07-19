# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-7-19
# Description: 解析抖音detail下载视频或音频
# 将抖音detail复制到detail.json, 执行main_detail.py 下载
# json在线解析 https://www.sojson.com/
#***************************************************************

from DyPO import *
Dy_PO = DyPO()

varPath = Dy_PO.getDetail("mp3")
# Dy_PO.getDetail("mp4")

os.system("cd " + varPath + "; open .")


