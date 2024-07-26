# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-7-19
# Description: 解析抖音detail下载视频或音频 for cli
# 将抖音detail复制到detail.json, 执行main_detail.py 下载
# json在线解析 https://www.sojson.com/
# todo Alfred中输入 "dydetail mp3|mp4 "，执行以下脚本
# conda activate py308
# python /Users/linghuchong/Downloads/51/Python/project/instance/crawler/douyin/clidydetail {query}"
#***************************************************************

from DyPO import *
Dy_PO = DyPO()

query = sys.argv[1]

if query == "mp3" or query == "3":
    varPath = Dy_PO.getDetail("mp3")
elif query == "mp4" or query == "4":
    varPath = Dy_PO.getDetail("mp4")

os.system("cd '" + varPath + "'; open .")






