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

import os, sys, json, jsonpath, unittest, platform,time
from datetime import datetime
from time import sleep
from parameterized import parameterized
from BeautifulReport import BeautifulReport as bf

from instance.zyjk.EHR.frame1.configEmail import *
email = Email()

import instance.zyjk.EHR.frame1.reflection

import instance.zyjk.EHR.frame1.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
on_off = localReadConfig.get_email("on_off")

from instance.zyjk.EHR.frame1.iDriven import *
http = HTTP()

from instance.zyjk.EHR.frame1.xls import *
xls = XLS()

from PO.DataPO import *
data_PO = DataPO()
l_interIsRun = (xls.getInterIsRun())  # 获取inter中isRun执行筛选列表 ，[[], [], 3]

# 获取接口文档中接口名与属性名，生成字典
# print(xls.d_inter)
# {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,userid,id'}
# from PO.sqlserverPO import *
# SqlServer_PO = SqlServerPO("192.168.0.35", "test", "123456", "healthrecord_test")  # 测试环境

class runAllEHR(unittest.TestCase):

    @parameterized.expand(xls.getCaseParam())
    def test11(self, excelNo, caseName, method, interName, param, jsonpathKey, expected, checkDB, execDB):
        ' '
        # 判断对象属性是否存在
        if hasattr(runAllEHR, "userId"):param = param.replace("$$userId", str(runAllEHR.userId))  # 用户id
        if hasattr(runAllEHR, "idCard"):param = param.replace("$$idCard", str(runAllEHR.idCard))  # 身份证
        if hasattr(runAllEHR, "dateOfBirth"):param = param.replace("$$dateOfBirth", str(runAllEHR.dateOfBirth))  # 出生日期
        if hasattr(runAllEHR, "archiveNum"):param = param.replace("$$archiveNum", str(runAllEHR.archiveNum))  # 档案编号
        if hasattr(runAllEHR, "dateOfCreateArchive"): param = param.replace("$$dateOfCreateArchive", str(runAllEHR.dateOfCreateArchive))  # 档案创建日期

        # 15 检验身份证号码是否建档
        tmp_idCard = 'off'
        if "??idCard" in param:
            newIdCard = str(data_PO.randomIdCard())  # 随机生成身份证18位
            param = param.replace('??idCard', newIdCard)
            runAllEHR.idCard = newIdCard
            yearMonthDay = data_PO.getIdCardBirthday(newIdCard)  # 获取身份证年月日，如 1990-12-12
            dateOfBirth = yearMonthDay[0] + "-" + yearMonthDay[1] + "-" + yearMonthDay[2]
            runAllEHR.dateOfBirth = dateOfBirth
            tmp_idCard = 'on'

        # 17 保存档案
        tmp_dateOfCreateArchive = 'off'
        tmp_contactsName = 'off'
        tmp_name1 = 'off'
        tmp_name2 = 'off'
        tmp_phone = 'off'
        tmp_contactsPhone = 'off'
        if "??dateOfCreateArchive" in param:
            dateOfCreateArchive = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            param = param.replace("??dateOfCreateArchive", dateOfCreateArchive)  # 建档日期 是当前日期 年-月-日
            runAllEHR.dateOfCreateArchive = dateOfCreateArchive
            tmp_dateOfCreateArchive = 'on'
        if "??contactsName" in param:
            contactsName = data_PO.randomUserName()
            param = param.replace("??contactsName", contactsName)
            runAllEHR.contactsName = contactsName
            tmp_contactsName = 'on'
        if "??name1" in param:
            if "??name2" in param:
                name1 = data_PO.randomUserName()
                name2 = data_PO.randomUserName()
                param = param.replace("??name1", name1)
                param = param.replace("??name2", name2)
                runAllEHR.name1 = name1
                runAllEHR.name2 = name2
                tmp_name1 = "on"
                tmp_name2 = "on"
        if "??contactsPhone" in param:
            if "??phone" in param:
                contactsPhone = data_PO.randomPhone()
                phone = data_PO.randomPhone()
                param = param.replace("??contactsPhone", contactsPhone)
                param = param.replace("??phone", phone)
                runAllEHR.contactsPhone = contactsPhone
                runAllEHR.phone = phone
                tmp_phone = "on"
                tmp_contactsPhone = "on"

        # **********************************************************************************************************************************
        if method == "post":
            d_jsonres = xls.result(excelNo, caseName, method, interName, dict(eval(param)), jsonpathKey, expected)
        elif method == "postLogin":
            d_jsonres = xls.result(excelNo, caseName, method, interName, dict(eval(param)), jsonpathKey, expected)
        elif method == "get":
            d_jsonres = xls.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)
        else:   # postget
            d_jsonres = xls.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)
        # **********************************************************************************************************************************

        # rtncheckDB, rtnexecDB = SqlServer_PO.dbSelect(checkDB, execDB)
        # xls.setCaseParam(excelNo, '', '', str(d_jsonres),rtncheckDB, rtnexecDB)

        # 登录11
        if caseName == "登录11":
            token = jsonpath.jsonpath(d_jsonres, expr='$.token')
            runAllEHR.token = token[0]
            userId = jsonpath.jsonpath(d_jsonres, expr='$.userInfo.uid')
            runAllEHR.userId = str(userId[0])
            # rtncheckDB, rtnexecDB = SqlServer_PO.dbSelect(checkDB, execDB)
            # xls.setCaseParam(excelNo, 'token=' + token[0] + "\n" + 'userId=' + str(userId[0]), 'pass',
            #                      str(d_jsonres), str(rtncheckDB), str(rtnexecDB))

        # 15 检验身份证号码是否建档
        if tmp_idCard == 'on':
            xls.setCaseParam(excelNo, "idCard=" + newIdCard + "\n" + "dateOfBirth=" + dateOfBirth, 'pass', str(d_jsonres), '', '')

        # 17 保存档案
        if "/app/recordManager/save" == interName:
            archiveNum = jsonpath.jsonpath(d_jsonres, expr='$.data.archiveNum')
            runAllEHR.archiveNum = str(archiveNum[0])
            if tmp_dateOfCreateArchive == 'on' and tmp_contactsName == 'on' and tmp_name1 == 'on' and tmp_name2 == 'on' and tmp_phone == 'on' and tmp_contactsPhone == 'on':
                xls.setCaseParam(excelNo, 'archiveNum=' + str(archiveNum[0]) + "\n" + 'dateOfCreateArchive=' + str(dateOfCreateArchive) + "\n" + 'contactsName=' + contactsName + "\n" + 'name1=' + name1 + "\n" + 'name2=' + name2 + "\n" + 'contactsPhone=' + contactsPhone + "\n" + 'phone=' + phone, 'pass', str(d_jsonres), '', '')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='runAllEHR.py', top_level_dir=None)
    runner = bf(suite)
    projectName = localReadConfig.get_system("projectName")
    reportName = localReadConfig.get_system("reportName")
    runner.report(filename='report\\' +  reportName, description= projectName + '测试报告')
    # runner.report(filename='./report/report_' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.html', description='logo的测试报告')
    if platform.system() == 'Darwin':
        os.system("open ./report/report.html")
        os.system("open ./config/interface.xls")
    if platform.system() == 'Windows':
        os.system("start .\\report\\report.html")
        os.system("start .\\config\\interface.xls")
    if on_off == 'on':

        email.send_email()


