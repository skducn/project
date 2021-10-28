# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 电子健康档案 - 质控配置文件
# *****************************************************************


from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO(".\config\diabetesVisitRule2.3.1.xlsx")
l_diabetes = (Openpyxl_PO.l_getColDataByPartCol([1, 2], [1], "diabetes"))

from PO.FilePO import *
File_PO = FilePO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.ListPO import *
List_PO = ListPO()

from PO import SqlserverPO
Sqlserver_PO = SqlserverPO.SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")  # 测试环境

# 日志文件
logFile = './log/controlRul_' + Time_PO.getDate() + '.log'




