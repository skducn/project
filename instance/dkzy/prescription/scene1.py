# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-3-15
# Description: 电科智药，审方处方web，业务1
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from dkzy.prescription.config.config import *
from dkzy.prescription.PageObject.PrescriptionPO import *

# # 加启动配置 (解决：Chrome正受到自动测试软件的控制)
# options = webdriver.ChromeOptions()
# options.add_argument('disable-infobars')
#
#
# # 打开chrome浏览器
# path = "C:\Python27\Scripts\chromedriver.exe"
# driverC = webdriver.Chrome(executable_path=path,chrome_options=options)
# Level_C = LevelPO(driverC)
# Prescription_C = PrescriptionPO(Level_C)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 环境

'''登录C'''
Level_C.openURL(1200, 900, varUrlC, 3)
Level_C.inputXpath("//input[@ng-model='account']", u"666001")
Level_C.inputXpath("//input[@ng-model='password']", u"123456")
Level_C.clickLinktext("登录", 2)
Level_C.clickXpath("//div[@ng-click='consult(1)']", 2)

sleep(1212)

'''登录B'''
driverB = webdriver.Chrome()
Level_B = LevelPO(driverB)
Prescription_B = PrescriptionPO(Level_B)
Level_B.openURL(1200, 900, varUrlB, 3)
Prescription_B.login("15011230201", "111111")
Level_B.setMaximize()



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

'''药事服务'''
Level_B.clickLinktext("药事服务", 2)
Prescription_B.drugServer()

#
# '''退出系统'''
# Level_B.clickLinktext("退出", 2)
# Level_B.clickLinktext("是", 2)



