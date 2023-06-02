# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: pornhub 获取html页面中的视频链接，并保存到 2videoUrl
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

Pornhub_PO.html2url("html.txt", 'ph.txt', 'url.txt')

Pornhub_PO.setFileList()

os.system("open ph.txt")