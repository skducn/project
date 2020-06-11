# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: OA 配置文件
# *****************************************************************

import string, numpy
from string import digits
from PO.WebPO import *
from PO.ListPO import *
from PO.TimePO import *
from PO.ColorPO import *
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.FilePO import *
from PO.StrPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
Time_PO = TimePO()
Color_PO = ColorPO()

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "bitest", 3306)  # 测试数据库

# 39 环境
varURL = "http://192.168.0.39"

# 日志文件
logFile = './log/oa_' + Time_PO.getDate() + '.log'



