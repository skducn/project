# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2019-5-7
# Description: OA - 常用工作
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases
# selenium更新： pip3 install -U selenium
#***************************************************************

import os, sys
# sys.path.append("../../../../")
from instance.zyjk.OA.PageObject.OaPO import *
Oa_PO = OaPO()
List_PO = ListPO()
Time_PO = TimePO()
Net_PO = NetPO()
Data_PO = DataPO()
File_PO = FilePO()
Excel_PO = ExcelPO()



#***************************************************************#***************************************************************

# varNo = "5680"

# # 场景1：请假单，请假天数3天
# varNo = Oa_PO.apply("1/7, ", "jinhao", "请假申请", 1, Time_PO.getDatetimeEditHour(0), Time_PO.getDatetimeEditHour(24), "3")
# Oa_PO.audit("2/7, ", varNo, "部门领导", "wanglei01", "同意", "部门领导批准")
# Oa_PO.audit("3/7, ", varNo, "人事总监", "yanlibei", "同意", "yanlibei批准")
# Oa_PO.audit("4/7, ", varNo, "副总", "wanglei01", "同意", "wanglei批准")
# Oa_PO.audit("5/7, ", varNo, "总经理", "yuanyongtao", "同意", "yuanyongtao批准")
# Oa_PO.applyDone("6/7, ", varNo, "jinhao")
# Oa_PO.applyDone("7/7, ", varNo, "yanlibei")

# 场景2：请假单，请假天数1天
varNo = Oa_PO.apply("1/6, ", "jinhao", "请假申请", 1, Time_PO.getDatetimeEditHour(0), Time_PO.getDatetimeEditHour(24), "1")
Oa_PO.audit("2/6, ", varNo, "部门领导", "wanglei01", "同意", "部门领导批准")
Oa_PO.audit("3/6, ", varNo, "人事总监", "yanlibei",  "同意", "yanlibei批准")
Oa_PO.audit("4/6, ", varNo, "副总", "wanglei01", "同意", "wanglei批准")
Oa_PO.applyDone("5/6, ", varNo, "jinhao")
Oa_PO.applyDone("6/6, ", varNo, "yanlibei")