# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-8-1
# Description:
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import re, subprocess, requests, os, psutil, json
import sys

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "utf8")  # 测试环境
from PO.StrPO import *
Str_PO = StrPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()

class ChcRulePO():

    def clsApp(self, varApp):

        '''
        关闭应用程序
        :param varApp:
        :return:
         # clsApp("chrome.exe")
        '''

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def getToken(self, varUser, varPass):

        # 1,获取登录用户的token
        command = "curl -X POST \"http://192.168.0.243:8012/login\" -H \"accept: */*\" -H \"Content-Type: application/json\" -d \"{ \\\"password\\\": \\\"" + str(varPass) + "\\\", \\\"username\\\": \\\"" + str(varUser) + "\\\"}\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r['data']['access_token'])
        return d_r['data']['access_token']

    def runRule(self, var, token):

        '''
        跑规则
        :param var:
        :param token:
        :return:
        '''

        command = "curl -X GET \"http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(token) + "\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        if d_r['code'] != 200:
            print("跑规则, http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var) + ", " + str(d_r))
            return (str(d_r['code']), "跑规则, http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var) + ", " + str(d_r))
        else:
            print("跑规则, http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var) + ", " + str(d_r['code']))
            return (str(d_r['code']), "跑规则, http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var) + ", " + str(d_r['code']))



    def newAssess(self, varIdcard, token):

        '''
        新增评估
        :param varIdcard:
        :param token:
        :return:
        '''

        command = "curl -X GET \"http://192.168.0.243:8011/server/qyyh/addAssess/" + str(
            varIdcard) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(token) + "\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        print(str_r)
        d_r = json.loads(str_r)
        if d_r['code'] != 200:
            print("新增评估, http://192.168.0.243:8011/server/qyyh/addAssess/" + str(varIdcard) + ", " + str(d_r))
            return (str(d_r['code']), "新增评估, http://192.168.0.243:8011/server/qyyh/addAssess/" + str(varIdcard)+ ", " + str(d_r))
        else:
            print("新增评估, http://192.168.0.243:8011/server/qyyh/addAssess/" + str(varIdcard) + ", " + str(d_r['code']))
            return (str(d_r['code']), "新增评估, http://192.168.0.243:8011/server/qyyh/addAssess/" + str(varIdcard) + ", " + str(d_r['code']))


    def getResult(self, varID, varRuleCode):

        # 校验评估规则结果表
        l_result = Sqlserver_PO.execQuery("select ID from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE='%s'" % (varID, varRuleCode))
        # print("select * from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE= '" + str(varRuleCode) + "'")
        Color_PO.consoleColor("31", "33", "select * from T_ASSESS_RULE_RECORD where ASSESS_ID ='" + str(varID) + "' and RULE_CODE= '" + str(varRuleCode) + "'", "")
        log = "select * from T_ASSESS_RULE_RECORD where ASSESS_ID ='" + str(varID) + "' and RULE_CODE= '" + str(varRuleCode) + "'"
        return l_result, log

    def insertEMPI(self, varParams):

        # 新增患者主索引

        Sqlserver_PO.insertExec(varParams)


    def run(self, varRuleLib, Openpyxl_PO, TOKEN):

        '''
        健康评估规则库
        :param Openpyxl_PO:
        :param TOKEN:
        :return:
        '''

        # 获取"健康评估规则库"的规则编码和自动化规则
        l_paramCode = (Openpyxl_PO.getColValueByCol([1, 3, 4], [1], varRuleLib))  # 获取第5、7列值，忽略第一行数据
        # print(l_paramCode[0])  # OK
        # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
        # print(l_paramCode[2])  # GY_YH001001

        list1 = []
        listall = []
        for i in range(len(l_paramCode[1])):
            list1.append(l_paramCode[0][i])
            list1.append(l_paramCode[1][i])
            list1.append(l_paramCode[2][i])
            listall.append(list1)
            list1 = []
        # print(listall)
        d_paramCode = List_PO.list2dictByIndex(listall, 2)
        # print(d_paramCode)  # {2: ['OK', "r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'", 'GY_YH001001'], 3: ['OK', "r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='E11'", 'GY_YH002001']}
        # sys.exit(0)

        # 遍历每条规则
        for k, v in d_paramCode.items():

            # if v[1] != None :
                # 跑所有规则

            if v[1] != None and v[0] != "OK":
                # 结果为OK的规则不跑

                # print(str(k) + " => run")
                # varResult = v[0]  # OK
                varRuleCode = v[2]  # GY_YH001001
                # try:
                l_v1 = Str_PO.str2list(v[1])
                varTbl = l_v1[1]  # T_HIS_DIAGNOSIS
                varField = l_v1[2]  # IDCARD
                varParam = l_v1[3]  # IAGNOSIS_CODE='I10'
                varParam = varParam.replace(".and.", ',')
                print(str(k) + " => run(" + l_v1[0] + ")")

                if l_v1[0] == "r1":
                    l_result = self.r1(varRuleCode, varTbl, varField, varParam, TOKEN)
                elif l_v1[0] == "r2":
                    l_result = self.r2(varRuleCode, varTbl, varField, varParam, TOKEN)

                if l_result == 0:
                    Openpyxl_PO.setCellValue(k, 1, "OK", varRuleLib)
                    Color_PO.consoleColor("31", "36", str(k) + " => OK\n", "")
                    # print(No, " = > OK\n")
                    Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varRuleLib)
                else:
                    Openpyxl_PO.setCellValue(k, 1, "ERROR", varRuleLib)
                    Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varRuleLib)
                    Color_PO.consoleColor("31", "31", str(k) + " => ERROR\n", "")
                    Openpyxl_PO.setCellValue(k, 2, l_result, varRuleLib)
                    Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varRuleLib)
                # except:
                #     Color_PO.consoleColor("31", "31", str(k) + " => ERROR, 自动化规则格式错误!\n", "")



    def r1(self, varRuleCode, varTbl, varField, varParam, TOKEN):

        log = ""

        # 1,获取数据id
        l_value = Sqlserver_PO.execQuery("select top 1 %s from %s" % (varField, varTbl))  # 获取表中第一条记录的id
        Color_PO.consoleColor("31", "33", varField + " = select top 1 " + varField + " from " + varTbl, "")
        log = varField + " = select top 1 " + varField + " from " + varTbl + "\n"
        varId = l_value[0][varField]

        # 2，修改数据
        Sqlserver_PO.execute("update %s set %s where %s='%s'" % (varTbl, varParam, varField, varId))
        Color_PO.consoleColor("31", "33", "update " + varTbl + " set " + varParam + " where " + varField + "='" + str(varId) + "'", "")
        log = log + "update " + varTbl + " set " + varParam + " where " + varField + "='" + str(varId) + "'"

        # 3，跑规则
        ruleStatus, log2 = self.runRule(varId, TOKEN)
        log = log + str(log2) + "\n"

        if ruleStatus == 200:
            # 4，检查"评估规则结果表"
            l_result, log3 = self.getResult(varId, varRuleCode)
            if l_result != []:
                return 0
            else:
                return log + log3
        else:
            return log

    def r2(self, varRuleCode, varTbl, varField, varParam, TOKEN):

        log = ""

        # 1，修改数据(规则)
        Sqlserver_PO.execute("update top(1) %s set %s " % (varTbl, varParam))
        Color_PO.consoleColor("31", "33", "update top(1) " + varTbl + " set " + varParam, "")
        log = "update top(1) " + varTbl + " set " + varParam + "\n"

        # 2, 获取身份证
        l_var = Sqlserver_PO.execQuery("select top(1) %s from %s" % (varField, varTbl))
        Color_PO.consoleColor("31", "33", "ID_CARD = select top(1) " + varField + " from " + varTbl, "")
        varIDcard = l_var[0][varField]  # 110101196407281506  //身份证
        log = log + "ID_CARD = select top(1) " + varField + " from " + varTbl + "\n"

        # 3，删除T_ASSESS_INFO中对应的身份证数据
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD='%s'" % (varIDcard))
        Color_PO.consoleColor("31", "33", "delete from T_ASSESS_INFO where ID_CARD = '" + str(varIDcard) + "'", "")
        log = log + "delete from T_ASSESS_INFO where ID_CARD = '" + str(varIDcard) + "'" + "\n"

        # 4,新增评估
        log1 = self.newAssess(varIDcard, TOKEN)
        log = log + str(log1) + "\n"
        sleep(2)

        # 5, 获取评估表id
        l_var = Sqlserver_PO.execQuery("select id from T_ASSESS_INFO where ID_CARD='%s'" % (str(varIDcard)))
        Color_PO.consoleColor("31", "33", "select id from T_ASSESS_INFO where ID_CARD = '" + str(varIDcard) + "'", "")
        varId = l_var[0]['id']
        log = log + "select id from T_ASSESS_INFO where ID_CARD = '" + str(varIDcard) + "'" + "\n"

        # 6，跑规则
        log2 = self.runRule(varId, TOKEN)
        log = log + str(log2) + "\n"

        # 7，检查"评估规则结果表"
        l_result, log3 = self.getResult(varId, varRuleCode)
        if l_result != []:
            return 0
        else:
            return log + log3


    def r3(self, varRuleCode, varTbl, varField, varParam, TOKEN):

        log = ""

        # 1，修改数据1(规则)
        Sqlserver_PO.execute("update %s set %s where IDCARD='653101195005139999'" % (varTbl, varParam))
        Color_PO.consoleColor("31", "33", "update " + varTbl + " set " + varParam, " where IDCARD='653101195005139999'")
        log = "update " + varTbl + " set " + varParam, " where IDCARD='653101195005139999'\n"

        # 2，删除T_ASSESS_INFO中对应的身份证数据
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD='653101195005139999'")
        Color_PO.consoleColor("31", "33", "delete from T_ASSESS_INFO where ID_CARD='653101195005139999'", "")
        log = log + "delete from T_ASSESS_INFO where ID_CARD='653101195005139999'\n"

        # 3,新增评估
        log1 = self.newAssess('653101195005139999', TOKEN)
        log = log + str(log1) + "\n"
        sleep(2)

        # 4, 修改数据2(规则) 获取评估表id
        l_var = Sqlserver_PO.execQuery("update T_ASSESS_INFO set %s where ID_CARD='653101195005139999'")
        Color_PO.consoleColor("31", "33", "update T_ASSESS_INFO set %s where ID_CARD='653101195005139999'", "")
        varId = l_var[0]['id']
        log = log + "update T_ASSESS_INFO set %s where ID_CARD='653101195005139999'\n"

        # 5, 获取评估表id
        l_var = Sqlserver_PO.execQuery("select id from %s where ID_CARD='653101195005139999'")
        Color_PO.consoleColor("31", "33", "select id from %s where ID_CARD='653101195005139999'", "")
        varId = l_var[0]['id']
        log = log + "select id from %s where ID_CARD='653101195005139999'\n"

        # 6，跑规则
        log2 = self.runRule(varId, TOKEN)
        log = log + str(log2) + "\n"

        # 7，检查"评估规则结果表"
        l_result, log3 = self.getResult(varId, varRuleCode)
        if l_result != []:
            return 0
        else:
            return log + log3






    def healthAssessment(self, Openpyxl_PO: object, TOKEN: object) -> object:

        '''
        健康评估规则库
        :param Openpyxl_PO:
        :param TOKEN:
        :return:
        '''

        # 获取"健康评估规则库"的规则编码和自动化规则
        l_codeParam = (Openpyxl_PO.getColValueByCol([5, 7], [1], '健康评估规则库'))  # 获取第5、7列值，忽略第一行数据
        d_paramCode = dict(zip(l_codeParam[1], l_codeParam[0]))
        print(d_paramCode)
        No = 2
        for k, v in d_paramCode.items():
            k = Str_PO.str2list(k)

            if k != None:
                if k[0] == 'r1':
                    print(No, k, v)
                    varTbl = k[1]  # T_ASSESS_INFO
                    varParam = k[3]  # AGE=55
                    varParam = varParam.replace(".and.", ',')

                    # 1,获取数据id
                    l_value = Sqlserver_PO.execQuery("select top 1 %s from %s" % (k[2], varTbl))  # 获取表中第一条记录的id
                    varId = l_value[0][k[2]]
                    # print(v[2] + " = " + str(varId))  # ID = 1

                    # 2，修改数据
                    # print("update " + varTbl + " set " + varParam + " where " + v[2] + "=" + str(varId))
                    Color_PO.consoleColor("31", "33",
                                          "update " + varTbl + " set " + varParam + " where " + k[2] + "=" + str(varId),
                                          "")
                    Sqlserver_PO.execute("update %s set %s where %s='%s'" % (varTbl, varParam, k[2], varId))

                    # 3，跑规则
                    self.runRule(varId, TOKEN)

                    # 4，检查"评估规则结果表"
                    l_result = (self.getResult(varId, v))

                    if l_result != []:
                        # print(l_result)  # [{'ID': 26162}]
                        # print(No, " = > OK\n")
                        Color_PO.consoleColor("31", "36", str(No) + " => OK\n", "")
                        Openpyxl_PO.setCellValue(No, 8, "OK", "健康评估规则库")
                    else:
                        # print(No, " = > ERROR\n")
                        Color_PO.consoleColor("31", "31", str(No) + " => ERROR\n", "")
                        Openpyxl_PO.setCellValue(No, 8, "ERROR", "健康评估规则库")
                    Openpyxl_PO.setCellValue(No, 9, Time_PO.getDateTimeByDivide(), "健康评估规则库")
                    Openpyxl_PO.setCellValue(1, 8, "自动化测试结果", "健康评估规则库")

            No = No + 1
        Openpyxl_PO.open()
    def healthInterposal(self, Openpyxl_PO, TOKEN):

        '''
        健康干预规则库
        :param Openpyxl_PO:
        :param TOKEN:
        :return:
        '''

        # 获取"健康评估规则库"的规则编码和自动化规则
        l_codeParam = (Openpyxl_PO.getColValueByCol([2, 8], [1], '健康干预规则库'))  # 获取第2、9列值，忽略第一行数据
        d_paramCode = dict(zip(l_codeParam[1], l_codeParam[0]))
        print(d_paramCode)
        No = 2
        for k, v in d_paramCode.items():
            k = Str_PO.str2list(k)
            if k != None:

                if k[0] == 'r2':
                    print(No, k, v)
                    varTbl = k[1]  # T_ASSESS_INFO
                    varParam = k[3]  # AGE=55
                    varParam = varParam.replace(".and.", ',')

                    # 1，修改数据
                    # print("update " + varTbl + " set " + varParam + " where id=1")
                    Color_PO.consoleColor("31", "33", "update " + varTbl + " set " + varParam + " where id=1", "")
                    Sqlserver_PO.execute("update %s set %s where id=1" % (varTbl, varParam))
                    l_var = Sqlserver_PO.execQuery("select %s from %s where id=1" % (k[2], varTbl))
                    # print("select " + v[2] + " from " + varTbl + " where id=1")
                    varIDcard = l_var[0]['IDCARD']
                    print("身份证：" + str(varIDcard))

                    # 2,新增评估
                    self.newAssess(varIDcard, TOKEN)

                    # 3, 获取评估表id
                    l_var = Sqlserver_PO.execQuery("select id from T_ASSESS_INFO where ID_CARD='%s'" % (varIDcard))
                    # print(l_var)
                    varId = l_var[0]['id']
                    # print(varId)

                    # 4，跑规则
                    self.runRule(varId, TOKEN)

                    # 5，检查"评估规则结果表"
                    l_result = (self.getResult(varId, v))
                    if l_result != []:
                        # print(No, " = > OK\n")
                        Color_PO.consoleColor("31", "36", str(No) + " => OK\n", "")
                        Openpyxl_PO.setCellValue(No, 9, "OK", "健康干预规则库")
                    else:
                        # print(No, " = > ERROR\n")
                        Color_PO.consoleColor("31", "31", str(No) + " => ERROR\n", "")
                        Openpyxl_PO.setCellValue(No, 9, "ERROR", "健康干预规则库")
                    Openpyxl_PO.setCellValue(No, 10, Time_PO.getDateTimeByDivide(), "健康干预规则库")
                    # Openpyxl_PO.setCellValue(1, 8, "自动化测试结果", "健康干预规则库")
            No = No + 1
        Openpyxl_PO.open()