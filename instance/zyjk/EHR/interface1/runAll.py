# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : EHR 接口自动化框架之 unittest for python3
# URL: http://192.168.0.102:8080
# DB: sqlServer
# *****************************************************************

import os, sys, json, jsonpath, unittest, platform
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
l_interIsRun = (xls.getInterIsRun())  # 获取inter中isRun执行筛选列表 ，[[], [], 3]
# print(xls.d_inter)
# 获取接口文档中接口名与属性名，生成字典
# {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,userid,id'}


class runAll(unittest.TestCase):

    # 登录
    @parameterized.expand(xls.getCaseParam(l_interIsRun, '/healthRecord/app/login'))
    def test1(self, excelNo, caseName, method, interName, param, jsonpathKey, expected):
        """ 登录获取token """
        d_jsonres = xls.result(excelNo, caseName, method, interName, param, jsonpathKey, expected, xls.d_inter, '')
        if "refresh_token" in d_jsonres :
            token = jsonpath.jsonpath(d_jsonres, expr='$.refresh_token')
            runAll.token = token[0]
            token = "token=" + str(runAll.token)
            print(token)
            xls.setCaseParam(excelNo,token,'pass',str(d_jsonres))

    # 获取密保
    @parameterized.expand(xls.getCaseParam(l_interIsRun, '/healthRecord/encrypted/getQuestionList'))
    def test2(self, excelNo, caseName, method, interName, param, jsonpathKey, expected):
        ''' 获取密保'''
        d_jsonres = xls.result(excelNo, caseName, method, interName, param, jsonpathKey, expected, xls.d_inter, '')
        if d_jsonres:
            # 获取根节点下的 userId 节点的值，用于关联下个接口
            if "userid" in d_jsonres:
                userid = jsonpath.jsonpath(d_jsonres, expr='$.data.userId')
                runAll.userid = userid[0]
                userid = "userId=" + str(runAll.userid)
                xls.setCaseParam(excelNo, userid, 'pass', str(d_jsonres))
            else:
                xls.setCaseParam(excelNo, '', 'pass', str(d_jsonres))


    # @parameterized.expand(xls.getCaseParam(l_interIsRun, '/inter/HTTP/logout'))
    # def testlogout(self, excelNo, caseName, method, interName, param, jsonpathKey, expected):
    #     """ 登出 ，关联userid，token"""
    #     try:
    #         useridValue = runAll.userid
    #         tokenValue = runAll.token
    #     except:
    #         xls.setCaseParam(excelNo, '', 'Fail', 'userid或token不存在！')
    #     d_jsonres = xls.result(excelNo, caseName, method, interName, param, jsonpathKey, expected, xls.d_inter, 'userid',runAll.userid,'token',runAll.token)
    #     if d_jsonres:
    #         xls.setCaseParam(excelNo, '', 'pass', str(d_jsonres))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='runAll.py',top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    runner.report(filename='./report/'+ reportName, description= projectName + '测试报告')
    # runner.report(filename='./report/report_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.html', description='logo的测试报告')
    if platform.system() == 'Darwin':
        os.system("open .\\report\\report.html")
        os.system("open .\\config\\interface.xls")
    if platform.system() == 'Windows':
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\interface.xls")
    if on_off == 'on':
        email = Email()
        email.send_email()


