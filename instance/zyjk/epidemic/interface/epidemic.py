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
# pip3 install web.py
# *****************************************************************

import unittest, platform, os, sys
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
import xls as xls
xls1 = xls.XLS()


class epidemic(unittest.TestCase):

    @parameterized.expand(xls1.getCaseParam())
    def test5(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql):
        ' '
        xls1.result(excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern=os.path.split(__file__)[-1], top_level_dir=None)
    runner = bf(suite)
    iFile = localReadConfig.get_system("iFile")
    rptName = localReadConfig.get_system("rptName")
    xlsName = localReadConfig.get_system("xlsName")
    if platform.system() == 'Darwin':
        runner.report(filename=rptName, description=iFile)
        os.system("open " + rptName)
        os.system("open " + xlsName)
    elif platform.system() == 'Windows':
        runner.report(filename=rptName, description=iFile)
        os.system("start " + rptName)
        os.system("start " + xlsName)