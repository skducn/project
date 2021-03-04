# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-3-4
# Description   : SAAS 高血压
# 接口文档: http://192.168.0.213:8801/doc.html
# saas高血压: hypertension
# *****************************************************************
import unittest
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
import instance.zyjk.SAAS.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from instance.zyjk.SAAS.frame1.iDriven import *
http = HTTP()
from instance.zyjk.SAAS.frame1.xls import *
xls = XLS()
from PO.DataPO import *
data_PO = DataPO()

class run(unittest.TestCase):
    @parameterized.expand(xls.getCaseParam())
    def test11(self, excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote):
        ' '
        if interMethod == "header": xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)
        elif interMethod == "post": xls.result(excelNo, interCase, interUrl, interMethod, dict(eval(interParam)), interCheck, interExpected, d_KeyValueQuote)
        elif interMethod == "get": xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)
        else: xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, d_KeyValueQuote)   # postget

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.discover('.', pattern='run.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    runner.report(filename='report\\' + reportName, description= projectName + '测试报告')
    # runner.report(filename='./report/report_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.html', description='logo的测试报告')
    if platform.system() == 'Darwin':
        os.system("open ./report/report.html")
        os.system("open ./config/interface.xlsx")
    if platform.system() == 'Windows':
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\interface.xlsx")



