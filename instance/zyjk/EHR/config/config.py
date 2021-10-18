# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 电子健康档案数据监控中心 配置文件
# *****************************************************************

import os, datetime, xlrd, xlwt
from xlutils.copy import copy

# 测试环境
varURL = "http://192.168.0.243:8082/"
# dimUsername = "admin"
# dimPassword = "admin@123456"


# # 开发环境
# varURL = "http://192.168.0.36:19090/dev_ehr_admin/#/user"
# dimUsername = "test"
# dimPassword = "1qaz@WSX3edc"
#

# # 初始化参数化
# varExcel = os.path.abspath(r"case.xls")
# varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# sheetMain = bk.sheet_by_name("main")
# sheetTestCase = bk.sheet_by_name("testcase")
# styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
# styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
# styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')
