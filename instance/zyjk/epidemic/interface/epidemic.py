# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# pip3 install nose-parameterized   for cmd
# pip3 install BeautifulReport for cmd
# pip3 install --upgrade pip
# 提示语:Done 在 C:\Python39\Lib\site-packages\BeautifulReport\BeautifulReport.py
# pip3 install web.py
# *****************************************************************

import unittest, platform, os, sys
from datetime import date, datetime, timedelta
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
import xls as xls
xls1 = xls.XLS()

class epidemic(unittest.TestCase):

    @parameterized.expand(xls1.getCaseParam())
    def test5(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, globalVar, sql, tester, caseQty):
        ' '
        xls1.result(excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, globalVar, sql, tester, caseQty)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern=os.path.split(__file__)[-1], top_level_dir=None)
    runner = bf(suite)
    iDoc = localReadConfig.get_system("iDoc")
    # rptName = localReadConfig.get_system("rptName")
    xlsName = localReadConfig.get_system("xlsName")
    rptTime = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    if platform.system() == 'Darwin':
        # runner.report(filename=rptName, description=iDoc)
        runner.report(filename='./report/iReport_' + rptTime + '.html', description=iDoc)
        os.system("open ./report/iReport_" + rptTime + ".html")
        os.system("open " + xlsName)
    elif platform.system() == 'Windows':
        runner.report(filename='./report/iReport_' + rptTime + '.html', description=iDoc)
        # runner.report(filename=rptName, description=iDoc)
        os.system("start ./report/iReport_" + rptTime + ".html")
        # os.system("start " + xlsName)