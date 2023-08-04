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
        print("http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var))
        if d_r['code'] != 200:
            print(d_r)


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
        # print("http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var))
        # if d_r['code'] != 200:
        #     print(d_r)


    def getResult(self, varID, varRuleCode):

        # 校验评估规则结果表
        l_result = Sqlserver_PO.execQuery("select ID from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE='%s'" % (varID, varRuleCode))
        print("select * from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE= '" + str(varRuleCode) + "'")
        return l_result

        # print(l_result[0]['RULE_CODE'])  # PG_AGE002
        # if l_result[0]['RULE_CODE'] == varRuleCode:
        #     # print("ok")
        #     return 1
        # else:
        #     # print("error")
        #     return 0


    def insertEMPI(self, varParams):

        # 新增患者主索引

        Sqlserver_PO.insertExec(varParams)

    def healthAssessment(self, Openpyxl_PO, TOKEN):

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