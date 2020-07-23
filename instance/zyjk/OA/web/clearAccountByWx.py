# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-7-22
# Description: 小程序登录时清除账号权限
#***************************************************************

import os, sys
sys.path.append("../../../../")
from PO.MysqlPO import *

mysql_PO = MysqlPO("192.168.0.39", "ceshi", "123456", "TD_OA", 3336)
mysql_PO.cur.execute("update user SET VX_MARK='', IMEI='', MODEL='',PLATFORM='', NOT_LOGIN=0, LIMIT_LOGIN=0 ")
mysql_PO.conn.commit()