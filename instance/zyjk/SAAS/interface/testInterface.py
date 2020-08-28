# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-8-27
# Description   : SAAS 接口自动化框架
# https://md5jiami.51240.com/   md5加密
# *****************************************************************

import os, sys, json, jsonpath, unittest, platform, time
from datetime import datetime
from time import sleep
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
import instance.zyjk.SAAS.PageObject.ReadConfigPO as readConfig
localReadConfig = readConfig.ReadConfigPO()
from instance.zyjk.SAAS.PageObject.XlsPO import *
Xls_PO = XlsPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
data_PO = DataPO()
l_interIsRun = (Xls_PO.getInterIsRun())  # 获取inter中isRun执行筛选列表 ，[[], [], 3]


class testInterface(unittest.TestCase):

    @parameterized.expand(Xls_PO.getCaseParam())
    def test11(self, excelNo, caseName, method, interName, param, jsonpathKey, expected, selectSQL, updateSQL):

        ''
        # ' 判断对象属性是否存在 '
        if hasattr(testInterface, "code"):param = param.replace("$$code", str(testInterface.code))

        # **********************************************************************************************************************************
        if method == "post":
            d_jsonres = Xls_PO.result(excelNo, caseName, method, interName, dict(eval(param)), jsonpathKey, expected)
        elif method == "get":
            d_jsonres = Xls_PO.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)
        # **********************************************************************************************************************************

        # 登录
        if caseName == "登录":
            token = jsonpath.jsonpath(d_jsonres, expr='$.data.token')
            testInterface.token = token[0]
            Xls_PO.setCaseParam(excelNo, "token=" + token[0], '', str(d_jsonres), '', '')

        # 根据token获取code
        if caseName == "根据token获取code":
            data = jsonpath.jsonpath(d_jsonres, expr='$.data')
            testInterface.code = data[0]
            Xls_PO.setCaseParam(excelNo, "code=" + data[0], '', str(d_jsonres), '', '')

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='testInterface.py', top_level_dir=None)
    runner = bf(suite)
    reportFile = '../report/saas接口测试报告_' + str(Time_PO.getDatetime()) + '.html'
    runner.report(filename=reportFile, description=localReadConfig.get_system("projectName"))
    if platform.system() == 'Darwin':
        os.system("open " + reportFile)
        os.system("open ../config/" + localReadConfig.get_excel("interfaceFile"))
    if platform.system() == 'Windows':
        os.system("start " + reportFile)
        os.system("start ..\\config\\" + localReadConfig.get_excel("interfaceFile"))



