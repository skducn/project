# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# *****************************************************************

import unittest, platform, os
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf

import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()

import xls as xls
xls1 = xls.XLS()


class run(unittest.TestCase):
    @parameterized.expand(xls1.getCaseParam())
    def test11(self, excelNo, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql):
        ' '
        xls1.result(excelNo, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='run.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    if platform.system() == 'Darwin':
        runner.report(filename='./report/' + reportName, description=projectName + '测试报告')
        os.system("open ./report/report.html")
        os.system("open ./config/interface.xlsx")
    if platform.system() == 'Windows':
        runner.report(filename='report\\' + reportName, description=projectName + '测试报告')
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\interface.xlsx")