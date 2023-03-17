# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: pornhub 获取html页面中的视频链接，并保存到 2videoUrl
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()
Pornhub_PO.html2url("1html", '2phFolderUrl', '2folderUrl')

os.system("open 2phFolderUrl")