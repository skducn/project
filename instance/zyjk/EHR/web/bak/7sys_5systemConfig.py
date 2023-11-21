# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-6
# Description: 电子健康档案数据监控中心（PC端）之 系统配置
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.excelPO import *
from instance.zyjk.CRM.PageObject.thirdSitePO import *
thirdSite_PO = ThirdSitePO()
monitor_PO = Monitor()
excel_PO = ExcelPO()

# 开发环境
varURL = 'https://192.168.0.36:19090/dev_ehr_admin/#/user'
# 测试环境
# varURL =

webdriver_PO = WebdriverPO("chrome")
webdriver_PO.open(varURL)
webdriver_PO.driver.maximize_window()  # 全屏
level_PO = LevelPO(webdriver_PO.driver)
level_PO.inputXpath("//input[@type='text']", "admin")
level_PO.inputXpath("//input[@type='password']", "admin@123456")
level_PO.clickXpath("//button[@type='button']", 2)

# .............................................................................................................................................................
# 系统配置
level_PO.clickXpathsContain("//a", "href", '#/setting', 2)

x = level_PO.getXpathText("//span[@类与实例='el-pagination__total']")
x = x.replace("共 ", "").replace(" 条", "")
print(x)

level_PO.clickXpath("//input[@placeholder='请选择']", 6)  # 定位第一下拉框
# x = level_PO.getXpathsText("//span")
# x = level_PO.getXpathText("//div[@类与实例='el-select-dropdown el-popper']/div[1]/div[1]/ul/li[2]/span")  # 选择更新渠道
# print(x)
level_PO.clickXpath("//div[@类与实例='el-select-dropdown el-popper']/div[1]/div[1]/ul/li[2]/span", 2)  # 选择更新渠道
# level_PO.clickXpath("//span[@类与实例='el-pagination__sizes']/div/div/input", 2)  # 定位 10条/页
# a = level_PO.getXpathsText("//div[@类与实例='el-scrollbar']/div[1]/ul/li[3]/span")
# print(a)


x = level_PO.getXpathsText("//tr[@类与实例='el-table__row warning-row']")
print(x)

