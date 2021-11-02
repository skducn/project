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
Openpyxl_PO.closeExcelPid('EXCEL.EXE')
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

if platform.system() == 'Darwin':
    os.system("open ./config/diabetesVisitRule2.3.1.xlsx")
if platform.system() == 'Windows':
    os.system("start .\\config\\diabetesVisitRule2.3.1.xlsx")