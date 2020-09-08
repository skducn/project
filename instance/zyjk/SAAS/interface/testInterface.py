# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2020-8-27
# Description   : SAAS 接口自动化框架
# http://192.168.0.213:8801/doc.html   SAAS接口文档
# http://192.168.0.213/admin/login web页 18622222222,123456
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
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "saasuserdev", 3306)  # 测试环境
l_interIsRun = (Xls_PO.getInterIsRun())  # 获取inter中isRun执行筛选列表 ，[[], [], 3]


class testInterface(unittest.TestCase):

    @parameterized.expand(Xls_PO.getCaseParam())
    def test(self, excelNo, caseName, method, interName, param, jsonpathKey, expected, selectSQL, updateSQL):

        ''
        # 判断对象属性是否存在
        if hasattr(testInterface, "code"):param = param.replace("$$code", str(testInterface.code))
        if hasattr(testInterface, "token"):param = param.replace("$$token", str(testInterface.token))
        if hasattr(testInterface, "orgId"):param = param.replace("$$orgId", str(testInterface.orgId))
        if hasattr(testInterface, "id"):param = param.replace("$$id", str(testInterface.id))

        # 获取 generation值，字典
        d_generation = Xls_PO.getCaseGeneration()
        testInterface.orgId = d_generation['orgId']

        # 解析
        d_jsonres, param = Xls_PO.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)

        # 5 登录
        if caseName == "登录":
            token = jsonpath.jsonpath(d_jsonres, expr='$.data.token')
            testInterface.token = token[0]
            Xls_PO.setCaseParam(excelNo, "token=" + token[0], '', str(d_jsonres), '', '')

        # 6 根据token获取code
        if caseName == "根据token获取code":
            data = jsonpath.jsonpath(d_jsonres, expr='$.data')
            testInterface.code = data[0]
            Xls_PO.setCaseParam(excelNo, "code=" + data[0], '', str(d_jsonres), '', '')

        # 9 新增医疗机构
        if caseName == "新增医疗机构":
            orgName = str(param).split("orgName=")[1].split("&")[0]
            Mysql_PO.cur.execute('select id from sys_org where orgName="%s"' % orgName)
            orgId = Mysql_PO.cur.fetchall()
            Xls_PO.setCaseParam(excelNo, "orgId=" + str(orgId[0][0]), '', str(d_jsonres), '', '')
            testInterface.orgId = str(orgId[0][0])

        # 11 新增科室
        if caseName == "新增科室":
            param = dict(eval(param))
            Mysql_PO.cur.execute('select id from sys_dept where localName="%s" and orgId="%s"' % (param['localName'], testInterface.orgId))
            id = Mysql_PO.cur.fetchall()
            Xls_PO.setCaseParam(excelNo, "id=" + str(id[0][0]), '', str(d_jsonres), '', '')
            testInterface.id = str(id[0][0])


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



