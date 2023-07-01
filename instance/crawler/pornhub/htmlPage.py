# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: pornhub ，解析html.txt中的视频链接
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

Pornhub_PO.html2url("html.txt", 'ph.txt', 'url.txt')

os.system("open ph.txt")