# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: OA 配置文件
# *****************************************************************

from PO.TimePO import *
Time_PO = TimePO()

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.233", "ceshi", "123456", "TD_APP", 3336)  # 测试数据库


varURL = "http://192.168.0.65/"

# 日志文件
logFile = './log/oa_' + Time_PO.getDate() + '.log'



