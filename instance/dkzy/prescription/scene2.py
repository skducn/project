# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-13
# Description: 电科智药，处方web 问诊记录
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from dkzy.prescription.config.config import *
from dkzy.prescription.PageObject.PrescriptionPO import *


Level_B = LevelPO(driverB)
Prescription_B = PrescriptionPO(Level_B)

'''登录B'''
Level_B.openURL(1200, 900, varUrlB, 2)  # 测试环境
Prescription_B.login(u"15011230105", u"111111")  # 医生
Level_B.setMaximize()

'''问诊记录'''
Level_B.clickLinktext(u"问诊记录", 2)
Prescription_B.diagnosisRecord(u"医生")



# Level_B.clickLinktext(u"日常接诊", 2)

# '''药品信息查询 - 查询、重置、新增、详情'''
# Level_B.clickLinktext("药品信息查询", 2)
# Prescription_B.drugInfo()

# '''历史审核处方'''
# Level_B.clickLinktext("历史审核处方", 2)
# Prescription_B.historyAudit()
#
# '''服务统计'''
# Level_B.clickLinktext("服务统计", 2)
# Prescription_B.serverStatistic()



#
# '''退出系统'''
# Level_B.clickLinktext("退出", 2)
# Level_B.clickLinktext("是", 2)



