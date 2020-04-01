# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : PIM 接口自动化框架之 unittest for python3
# URL: http://192.168.0.16:8081
# http://192.168.0.16:8081/pim/doc.html
# DB: sqlServer
# *****************************************************************

import os, sys, json, jsonpath, unittest, platform,time
from datetime import datetime
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf
from time import sleep
import reflection
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
on_off = localReadConfig.get_email("on_off")
from iDriven import HTTP
http = HTTP()
from configEmail import Email
from xls import XLS
xls = XLS()
from Public.PageObject.ThirdPO import *
thirdPO = ThirdPO()
l_interIsRun = (xls.getInterIsRun())  # 获取inter中isRun执行筛选列表 ，[[], [], 3]
# 获取接口文档中接口名与属性名，生成字典
# print(xls.d_inter)
# {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,userid,id'}


class runAllPIM(unittest.TestCase):

    @parameterized.expand(xls.getCaseParam())
    def test11(self, No, case, method, url, param, assertion, expected):
        '''PIM'''
        # 判断对象属性是否存在
        # **********************************************************************************************************************************
        if method == "post":
            d_jsonres = xls.result(No, case, method, url, dict(eval(param)), assertion, expected, xls.d_inter, '')
        elif method == "get":
            d_jsonres = xls.result(No, case, method, url, param, assertion, expected, xls.d_inter, '')
        # **********************************************************************************************************************************

        # 11 登录
        if 'token' in str(d_jsonres):
            token = jsonpath.jsonpath(d_jsonres, expr='$.extra.token')
            runAllPIM.token = token[0]
            xls.setCaseParam(No, 'token=' + token[0], 'pass', str(d_jsonres))



if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='runAllPIM.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    runner.report(filename='./report/'+ reportName, description= projectName + '测试报告')
    # runner.report(filename='./report/report_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.html', description='logo的测试报告')
    if platform.system() == 'Darwin':
        os.system("open .\\report\\report.html")
        os.system("open .\\config\\inter_PIM.xls")
    if platform.system() == 'Windows':
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\inter_PIM.xls")
    if on_off == 'on':
        email = Email()
        email.send_email()


