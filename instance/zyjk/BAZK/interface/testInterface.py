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
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.195", "root", "Zy123456", "saasuserdev", 3306)  # 测试环境
l_interIsRun = (Xls_PO.getInterIsRun())  # 获取inter中isRun执行筛选列表 ，[[], [], 3]


class testInterface(unittest.TestCase):

    @parameterized.expand(Xls_PO.getCaseParam())
    def test(self, excelNo, caseName, method, interName, param, jsonpathKey, expected, generation, selectSQL, updateSQL):

        ''
        # 判断对象属性是否存在,generation中所有变量。
        if hasattr(testInterface, "code"):param = param.replace("$$code", str(testInterface.code))
        if hasattr(testInterface, "token"):param = param.replace("$$token", str(testInterface.token))
        if hasattr(testInterface, "id"):param = param.replace("$$id", str(testInterface.id))
        if hasattr(testInterface, "roleId"):param = param.replace("$$roleId", str(testInterface.roleId))
        if hasattr(testInterface, "roleName"):param = param.replace("$$roleName", str(testInterface.roleName))

        # 获取 generation中自定义变量
        if hasattr(testInterface, "orgId"): param = param.replace("$$orgId", str(testInterface.orgId))
        if hasattr(testInterface, "userId"): param = param.replace("$$userId", str(testInterface.userId))
        d_generation = Xls_PO.getCaseGeneration()
        testInterface.orgId = d_generation['orgId']
        testInterface.userId = d_generation['userId']
        testInterface.roleName = d_generation['roleName']

        if caseName == "新增宣教文章":
            import base64
            f = open(r"d:\\test\\aaa.png", "rb")
            img = base64.b64encode(f.read())
            # print(img)
            # print(img.decode("utf-8"))  # 转换成字符串
            param = str(param).replace('?', img.decode("utf-8"))



        # 解析
        if method != "":
            d_jsonres, param = Xls_PO.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)
        else:
            # 自定义变量不解析
            Color_PO.consoleColor("31", "36", "[" + str(excelNo + 1) + "] > " + caseName + " > " + generation + "\n", "")

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

        # 8 新增医疗机构
        if caseName == "新增医疗机构":
            orgName = str(param).split("orgName=")[1].split("&")[0]
            Mysql_PO.cur.execute('select id from sys_org where orgName="%s"' % orgName)
            orgId = Mysql_PO.cur.fetchall()
            Xls_PO.setCaseParam(excelNo, "orgId=" + str(orgId[0][0]) + "\norgName=" + str(orgName), '', str(d_jsonres), '', '')
            testInterface.orgId = str(orgId[0][0])

        # 13 新增科室
        if caseName == "新增科室":
            param = dict(eval(param))
            Mysql_PO.cur.execute('select id from sys_dept where localName="%s" and orgId="%s"' % (param['localName'], testInterface.orgId))
            id = Mysql_PO.cur.fetchall()
            Xls_PO.setCaseParam(excelNo, "id=" + str(id[0][0]), '', str(d_jsonres), '', '')
            testInterface.id = str(id[0][0])

        # 18 新增角色
        if caseName == "新增角色":
            param = dict(eval(param))
            Mysql_PO.cur.execute('select id from sys_role where roleName="%s" and status=1' % (param['roleName']))
            roleId = Mysql_PO.cur.fetchall()
            Xls_PO.setCaseParam(excelNo, "roleId=" + str(roleId[0][0]) + ",roleName=" + param['roleName'], '', str(d_jsonres), '', '')
            testInterface.roleId = str(roleId[0][0])





if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='testInterface.py', top_level_dir=None)
    runner = bf(suite)
    reportFile = '../report/saas接口测试报告_' + str(Time_PO.getDatetime()) + '.html'
    runner.report(filename=reportFile, description=localReadConfig.get_system("projectName"))
    # if platform.system() == 'Darwin':
    #     os.system("open " + reportFile)
    #     os.system("open ../config/" + localReadConfig.get_excel("interfaceFile"))
    if platform.system() == 'Windows':
    #     os.system("start " + reportFile)
        os.system("start ..\\config\\" + localReadConfig.get_excel("interfaceFile"))



