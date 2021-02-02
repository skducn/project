# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : EHR 接口自动化框架之 unittest for python3
# URL: http://192.168.0.102:8080
# http://192.168.0.241:8060/healthRecord/swagger-ui.html#/
# DB: sqlServer
# https://md5jiami.51240.com/   md5加密
# e88cc96bfdf739b52e9893226b941129
# *****************************************************************

import unittest, platform

from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf

from instance.zyjk.EHR.frame1.configEmail import *
email = Email()

import instance.zyjk.EHR.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
on_off = localReadConfig.get_email("on_off")

from instance.zyjk.EHR.frame1.iDriven import *
http = HTTP()

from instance.zyjk.EHR.frame1.xls import *
xls = XLS()

# from PO.sqlserverPO import *
# SqlServer_PO = SqlServerPO("192.168.0.35", "test", "123456", "healthrecord_test")  # 测试环境

from PO.DataPO import *
data_PO = DataPO()

# l_interIsRun = (xls.getInterIsRun())  # 初始化inter中isRun执行筛选列表 ，[[], [], 3]
# 获取接口文档中接口名与属性名，生成字典
# print(xls.d_inter)
# {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,userid,id'}

# **********************************************************************************************************************************

class runAllEHR(unittest.TestCase):
    @parameterized.expand(xls.getCaseParam())
    def test11(self, excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, dictKey):
        ' '
        if interMethod == "postLogin": xls.result(excelNo, interCase, interUrl, interMethod, dict(eval(interParam)), interCheck, interExpected, dictKey)
        elif interMethod == "post": xls.result(excelNo, interCase, interUrl, interMethod, dict(eval(interParam)), interCheck, interExpected, dictKey)
        elif interMethod == "get": xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, dictKey)
        else: xls.result(excelNo, interCase, interUrl, interMethod, interParam, interCheck, interExpected, dictKey)   # postget

if __name__ == '__main__':

    suite = unittest.defaultTestLoader.discover('.', pattern='runAllEHR.py', top_level_dir=None)
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
    # if on_off == 'on':
    #     email.send_email()


