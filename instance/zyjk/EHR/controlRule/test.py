# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-10-25
# Description: 质控规则自动化脚本
# 依据：D:\1zy\6 研发二部\1 电子健康档案\2.3.1\V2.3.1开发测试任务.xlsx
# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()

Rule_PO.test2("17a7929801e54f1ca8ab69f18c086b00", "com.benetech.rules.modules.myrules.integrity.DiabetesVisit2412", "310110193902060067", "K0616970X")

# Rule_PO.test3("ac849eaa074545bd862680bf8b76242f", "com.benetech.rules.modules.myrules.availability.DiabetesVisit3995", "310110193902060067", "K0616970X")
