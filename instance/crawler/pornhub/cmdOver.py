# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-12-27
# Description: pornhub
# phover HelloElly https://cn.pornhub.com/view_video.php?viewkey=ph63c016e42d06c
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

import sys
query1 = sys.argv[1]
query2 = sys.argv[2]
Pornhub_PO.downloadOneOver(query1, query2)
