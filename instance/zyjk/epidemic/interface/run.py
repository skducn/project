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
# 提示语:Done 在C:\Python39\Lib\site-packages\BeautifulReport\BeautifulReport.py
# *****************************************************************

import unittest, platform, os, sys
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
        runner.report(filename='./data/' + reportName, description=projectName + '测试报告')
        os.system("open ./data/" + localReadConfig.get_system("reportName"))
        os.system("open " + localReadConfig.get_system("excelName"))
    if platform.system() == 'Windows':
        runner.report(filename='data\\' + reportName, description=projectName + '测试报告')
        os.system("start .\\data\\" + localReadConfig.get_system("reportName"))
        os.system("start " + localReadConfig.get_system("excelName"))