# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-3-4
# Description   : SAAS 高血压
# 开发环境接口文档: http://192.168.0.213:8801/doc.html
# 测试环境接口文档：http://103.25.65.103:4488/doc.html
# saas高血压: hypertension
# *****************************************************************
import unittest,platform,os
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
from readConfig import *
localReadConfig = ReadConfig()
from iDriven import *
http = HTTP()
from xls import *
xls = XLS()
from PO.DataPO import *
data_PO = DataPO()

class run(unittest.TestCase):
    @parameterized.expand(xls.getCaseParam())
    def test11(self, excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote):
        ' '
        xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='run.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    runner.report(filename='report\\' + reportName, description= projectName + '测试报告')
    # runner.report(filename='./report/report_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.html', description='logo的测试报告')
    if platform.system() == 'Darwin':
        os.system("open ./report/report.html")
        os.system("open ./config/" + localReadConfig.get_system("excelName"))
    if platform.system() == 'Windows':
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\" + localReadConfig.get_system("excelName"))



