# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-3-14
# Description: pornhub 获取页面视频地址
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

if platform.system() == "Darwin":
    # Pornhub_PO.run("yinyleon")  # 批量下载， yinyleon既是目录名，又是html文件
    Pornhub_PO.runS("helloelly", 'https://cn.pornhub.com/view_video.php?viewkey=ph63bf0cdd9798e')  # 单个下载， helloelly是目录




# if platform.system() == "Windows":
#     folder = Pornhub_PO.run("yinyleon", "d:/11/44")






