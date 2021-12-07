# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# 接口文旦2：http://192.168.0.243:8001/doc.html#/
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# pip3 install nose-parameterized   for cmd
# pip3 install BeautifulReport for cmd
# pip3 install --upgrade pip
# 提示语:Done 在 C:\Python39\Lib\site-packages\BeautifulReport\BeautifulReport.py
# pip3 install web.py
# *****************************************************************

import unittest
from parameterized import parameterized
import xls as xls
xls1 = xls.XLS()

class epidemic(unittest.TestCase):
    @parameterized.expand(xls1.getCaseParam())
    def test(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, g_dict, g_sql, g_script, tester, caseQty):
        ' '
        xls1.result(excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, g_dict, g_sql, g_script, tester, caseQty)


