# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-10-25
# Description: 质控规则自动化脚本
# 依据：D:\1zy\6 研发二部\1 电子健康档案\2.3.1\V2.3.1开发测试任务.xlsx
#Color=['c6efce','006100']#绿
# #Color = ['ffc7ce', '9c0006']  #红
# #Color = ['ffeb9c', '9c6500']  # 黄
# Color = ['ffffff', '000000']  # 黑白

# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
Rule_PO = RulePO()

idCardNo = Rule_PO.isTestData("310110193902060067")

for i in range(Rule_PO.max_row-1):
    if Rule_PO.l_exec[0][i] !=  None:
        if Rule_PO.l_isRun[0][i] != 'N':
            # print(Rule_PO.l_exec[0][i])
            x = eval(Rule_PO.l_exec[0][i])
            if x == "ok":
                Openpyxl_PO.setCellValue(i+2, 22, "ok", ['c6efce','006100'], "rule")
                Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['c6efce','006100'],"rule")
            else:
                Openpyxl_PO.setCellValue(i + 2, 22, "error", ['ffc7ce', '9c0006'], "rule")
                Openpyxl_PO.setCellValue(i + 2, 23, Time_PO.getDatetime_divide(), ['ffc7ce', '9c0006'], "rule")
            Openpyxl_PO.save()



Rule_PO.ruleId_66f1d27307164209b95f51fe8576a2cd_4("一级医院有检验结果（ACR）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit3991", "310110193902060067")
# Rule_PO.ruleId_97384e2480e14d4db9a6f70d33b8d4ff_5("三级医院有检验结果（ACR）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit3989", "310110193902060067")
# Rule_PO.ruleId_e730a482345e4976bb792be43c75788a_6("二级医院有检验结果（ACR）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit3990", "310110193902060067")

# Rule_PO.ruleId_17ff3dd2fe5c4b41a766b130d1333e73_8("与二级医院实验室检验结果逻辑不符合（总胆固醇）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit2225", "310110193902060067")
# Rule_PO.ruleId_27b9cb4fc53d48baac87fc22ad4414be_9("与三级医院实验室检验结果逻辑不符合（总胆固醇）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit2224", "310110193902060067")
# Rule_PO.ruleId_711d9d2122884c74992c8c6c30da738f_10("与一级医院实验室检验结果逻辑不符合（总胆固醇）", "com.benetech.rules.modules.myrules.traceability.DiabetesVisit2226", "310110193902060067")





3