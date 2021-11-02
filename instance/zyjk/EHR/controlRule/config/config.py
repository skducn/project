# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 电子健康档案 - 质控配置文件
# *****************************************************************


from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO(".\config\diabetesVisitRule2.3.1.xlsx")
# 获取rule表总行数
l_RowCol = Openpyxl_PO.l_getTotalRowCol("rule")
# print(l_RowCol[0])
# 获取 ruleId,ruleSql,comment,a执行
l_ruleId = (Openpyxl_PO.l_getColDataByPartCol([1], [1], "rule"))
l_ruleSql = (Openpyxl_PO.l_getColDataByPartCol([6], [1], "rule"))
l_comment = (Openpyxl_PO.l_getColDataByPartCol([7], [1], "rule"))
l_isRun = (Openpyxl_PO.l_getColDataByPartCol([20], [1], "rule"))
l_exec = (Openpyxl_PO.l_getColDataByPartCol([21], [1], "rule"))
Openpyxl_PO.freeze("h2")
Openpyxl_PO.filter("all")
# Openpyxl_PO.ws(40)



# 获取 diabetes表 1，2列的所有数据
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




