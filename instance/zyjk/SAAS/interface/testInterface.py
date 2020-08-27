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
        ' '
        # 判断对象属性是否存在
        if hasattr(testInterface, "userId"):param = param.replace("$$userId", str(testInterface.userId))  # 用户id
        if hasattr(testInterface, "idCard"):param = param.replace("$$idCard", str(testInterface.idCard))  # 身份证
        if hasattr(testInterface, "dateOfBirth"):param = param.replace("$$dateOfBirth", str(testInterface.dateOfBirth))  # 出生日期
        if hasattr(testInterface, "archiveNum"):param = param.replace("$$archiveNum", str(testInterface.archiveNum))  # 档案编号
        if hasattr(testInterface, "dateOfCreateArchive"): param = param.replace("$$dateOfCreateArchive", str(testInterface.dateOfCreateArchive))  # 档案创建日期

        # 15 检验身份证号码是否建档
        tmp_idCard = 'off'
        if "??idCard" in param:
            newIdCard = str(data_PO.randomIdCard())  # 随机生成身份证18位
            param = param.replace('??idCard', newIdCard)
            testInterface.idCard = newIdCard
            yearMonthDay = data_PO.getIdCardBirthday(newIdCard)  # 获取身份证年月日，如 1990-12-12
            dateOfBirth = yearMonthDay[0] + "-" + yearMonthDay[1] + "-" + yearMonthDay[2]
            testInterface.dateOfBirth = dateOfBirth
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
            testInterface.dateOfCreateArchive = dateOfCreateArchive
            tmp_dateOfCreateArchive = 'on'
        if "??contactsName" in param:
            contactsName = data_PO.randomUserName()
            param = param.replace("??contactsName", contactsName)
            testInterface.contactsName = contactsName
            tmp_contactsName = 'on'
        if "??name1" in param:
            if "??name2" in param:
                name1 = data_PO.randomUserName()
                name2 = data_PO.randomUserName()
                param = param.replace("??name1", name1)
                param = param.replace("??name2", name2)
                testInterface.name1 = name1
                testInterface.name2 = name2
                tmp_name1 = "on"
                tmp_name2 = "on"
        if "??contactsPhone" in param:
            if "??phone" in param:
                contactsPhone = data_PO.randomPhone()
                phone = data_PO.randomPhone()
                param = param.replace("??contactsPhone", contactsPhone)
                param = param.replace("??phone", phone)
                testInterface.contactsPhone = contactsPhone
                testInterface.phone = phone
                tmp_phone = "on"
                tmp_contactsPhone = "on"

        # **********************************************************************************************************************************
        if method == "post":
            d_jsonres = Xls_PO.result(excelNo, caseName, method, interName, dict(eval(param)), jsonpathKey, expected)
        elif method == "postLogin":
            d_jsonres = Xls_PO.result(excelNo, caseName, method, interName, dict(eval(param)), jsonpathKey, expected)
        elif method == "get":
            d_jsonres = Xls_PO.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)
        else:   # postget
            d_jsonres = Xls_PO.result(excelNo, caseName, method, interName, param, jsonpathKey, expected)
        # **********************************************************************************************************************************

        # rtnselectSQL, rtnupdateSQL = SqlServer_PO.dbSelect(selectSQL, updateSQL)
        # Xls_PO.setCaseParam(excelNo, '', '', str(d_jsonres),rtnselectSQL, rtnupdateSQL)

        # 登录11
        if caseName == "登录11":
            token = jsonpath.jsonpath(d_jsonres, expr='$.token')
            testInterface.token = token[0]
            userId = jsonpath.jsonpath(d_jsonres, expr='$.userInfo.uid')
            testInterface.userId = str(userId[0])
            Xls_PO.setCaseParam(excelNo, "token=" + token[0] + "\n" + "userId=" + str(userId[0]), '',str(d_jsonres), '', '')

            # rtnselectSQL, rtnupdateSQL = SqlServer_PO.dbSelect(selectSQL, updateSQL)
            # Xls_PO.setCaseParam(excelNo, 'token=' + token[0] + "\n" + 'userId=' + str(userId[0]), 'pass',
            #                      str(d_jsonres), str(rtnselectSQL), str(rtnupdateSQL))

        # 15 检验身份证号码是否建档
        if tmp_idCard == 'on':
            Xls_PO.setCaseParam(excelNo, "idCard=" + newIdCard + "\n" + "dateOfBirth=" + dateOfBirth, '', str(d_jsonres), '', '')

        # 17 保存档案
        if "/app/recordManager/save" == interName:
            archiveNum = jsonpath.jsonpath(d_jsonres, expr='$.data.archiveNum')
            testInterface.archiveNum = str(archiveNum[0])
            if tmp_dateOfCreateArchive == 'on' and tmp_contactsName == 'on' and tmp_name1 == 'on' and tmp_name2 == 'on' and tmp_phone == 'on' and tmp_contactsPhone == 'on':
                Xls_PO.setCaseParam(excelNo, 'archiveNum=' + str(archiveNum[0]) + "\n" + 'dateOfCreateArchive=' + str(dateOfCreateArchive) + "\n" + 'contactsName=' + contactsName + "\n" + 'name1=' + name1 + "\n" + 'name2=' + name2 + "\n" + 'contactsPhone=' + contactsPhone + "\n" + 'phone=' + phone, 'pass', str(d_jsonres), '', '')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern='testInterface.py', top_level_dir=None)
    runner = bf(suite)
    reportFile = '../report/saas接口测试报告_' + str(Time_PO.getDatetime()) + '.html'
    runner.report(filename=reportFile, description=localReadConfig.get_system("projectName"))
    if platform.system() == 'Darwin':
        os.system("open " + reportFile)
        os.system("open ../config/" + localReadConfig.get_system("excelName"))
    if platform.system() == 'Windows':
        os.system("start " + reportFile)
        os.system("start ..\\config\\" + localReadConfig.get_system("excelName"))



