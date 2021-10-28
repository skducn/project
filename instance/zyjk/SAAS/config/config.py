# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: SASS 高血压
# *****************************************************************

import os, datetime, xlrd, xlwt
from xlutils.copy import copy

# 测试环境
varURL = "https://saas.shengyunmedical.com:8322/admin/login"


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
