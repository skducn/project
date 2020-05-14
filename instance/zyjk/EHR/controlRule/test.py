# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-5-12
# Description: 质控规则自动化脚本 for noOK
# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()
Excel_PO = ExcelPO()

 # 3，执行质控存储过程 ?未解决

# Rule_PO.execSqlFile1("controlRule.sql")
# Rule_PO.execQuery("exec proControl")

Rule_PO.execProcedure('proControl')
# Rule_PO.execProcedure('testJohn')





