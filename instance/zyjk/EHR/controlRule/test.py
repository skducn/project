# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-10-25
# Description: 质控规则自动化脚本
# 依据：D:\1zy\6 研发二部\1 电子健康档案\2.3.1\V2.3.1开发测试任务.xlsx
# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()

Rule_PO.isTestData("310110193902060067")
Rule_PO.ruleId_17a7929801e54f1ca8ab69f18c086b00_2("药物名称未填写", "com.benetech.rules.modules.myrules.integrity.DiabetesVisit2412", "310110193902060067")
Rule_PO.ruleId_ac849eaa074545bd862680bf8b76242f_3("药品名称与药物类型不匹配", "com.benetech.rules.modules.myrules.availability.DiabetesVisit3995", "310110193902060067")

Rule_PO.ruleId_66f1d27307164209b95f51fe8576a2cd_4("一级医院有检验结果（ACR）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit3991", "310110193902060067")
Rule_PO.ruleId_97384e2480e14d4db9a6f70d33b8d4ff_5("三级医院有检验结果（ACR）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit3989", "310110193902060067")
Rule_PO.ruleId_e730a482345e4976bb792be43c75788a_6("二级医院有检验结果（ACR）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit3990", "310110193902060067")


