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
from PO.DataPO import *
Data_PO = DataPO()



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

    def getHealthInterposalRule(self, Openpyxl_PO):

        '''
        获取 健康干预 - 干预规则 的值，匹配 getIdcard
        :return:
        [["高血压已患='是'", "糖尿病已患='是'"]]
        '''

        return Openpyxl_PO.getColValueByCol([7], [1], "健康干预")

    def insertEMPI(self, varParams):

        # 新增患者主索引

        Sqlserver_PO.insertExec(varParams)

    def getDiseaseIdcard(self, Openpyxl_PO):

        '''
        疾病身份证 sheet
        :param Openpyxl_PO:
        :return:  返回字典 {'YH_JB001': '310101202308070001', 'YH_JB002': '310101202308070002'}
        '''

        l_code_Idcard = Openpyxl_PO.getColByPartialColByUnwantedRow([1, 3], [1], "疾病身份证")
        d_code_Idcard = dict(zip(l_code_Idcard[0], l_code_Idcard[1]))
        return (d_code_Idcard)  # {'YH_JB001': '310101202308070001', 'YH_JB002': '310101202308070002'}

    def i_AssessRuleRecord(self, var, token):

        '''
        跑规则  i_AssessRuleRecord
        :param var:
        :param token:
        :return:
        '''

        command = "curl -X GET \"http://192.168.0.243:8011/server/tAssessInfo/rerunExecuteRule/" + str(var) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(token) + "\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        var = "ResponseError: i_AssessRuleRecord(), " + str(str_r)
        if 'code' in d_r:
            if d_r['code'] != 200:
                Color_PO.consoleColor("31", "31", var, "")
                # print(var)
                return ([{'name': '跑规则', 'value': var}])
            else:
                return ({'name': '跑规则', 'value': 200})
        else:
            # {"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ({'name':'跑规则', 'value': var})

    def i_newAssess(self, varIdcard, token):

        '''
        新增评估
        :param varIdcard:
        :param token:
        :return:
        '''

        # command = "curl -X GET \"http://192.168.0.243:8011/server/qyyh/addAssess/" + str(
        #     varIdcard) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(token) + "\""
        command = "curl -X POST \"http://192.168.0.243:8014/tAssessInfo/startAssess\" -H \"token:" + \
                  token + "\" -H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\" -H \"Authorization:\" " \
                               "-H \"Content-Type:application/json\" -d \"{\\\"categoryCode\\\":\\\"\\\",\\\"idCard\\\":\\\"" + str(
            varIdcard) + "\\\",\\\"orgCode\\\":\\\"\\\"}\""

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        # str_r = '{"code":340,"msg":null}'
        d_r = json.loads(str_r)
        var = "ResponseError: i_newAssess(), " + str(str_r)
        if 'code' in d_r:
            if d_r['code'] != 200:
                Color_PO.consoleColor("31", "31", var, "")
                # print(var)
                return ([{'name':'新增评估', 'value' : var}])
            else:
                return ([{'name':'新增评估', 'value': 200}])
        else:
            # {"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name':'新增评估', 'value': var}])




    def outResult1(self, varQty, varLog, k, varSheetName, Openpyxl_PO):

        if varQty == "1" or varQty == 1 :
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
            Color_PO.consoleColor("31", "36", "[" + str(k) + " => OK]\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
            Color_PO.consoleColor("31", "31", "[" + str(k) + " => ERROR]\n", "")
            Openpyxl_PO.setCellValue(k, 2, varLog, varSheetName)
            Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)

    def outResult2(self, varQty, varLog, k, varSheetName, Openpyxl_PO):

        if varQty == "2" or varQty == 2 :
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
            Color_PO.consoleColor("31", "36", "[" + str(k) + " => OK]\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
            Color_PO.consoleColor("31", "31", "[" + str(k) + " => ERROR]\n", "")
            Openpyxl_PO.setCellValue(k, 2, varLog, varSheetName)
            Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)

    def outResultGW(self, result, log, k, v5, varSheetName, Openpyxl_PO):

        ''' GW 前置条件'''

        if result == 1:
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
            Color_PO.consoleColor("31", "36", "[" + str(v5) + " => OK]\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
            Color_PO.consoleColor("31", "31", "[" + str(v5) + " => ERROR]\n", "")
            Openpyxl_PO.setCellValue(k, 2, log, varSheetName)
            Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)

    def runRule_AsteriskRule(self, var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # ChcRule_PO.run('健康评估', None, "r6", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "OK", "r6", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ERROR", "r6", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ALL", "r6", Openpyxl_PO, TOKEN)

        for k, v in d_paramCode.items():
            # print(v) # ['OK', "r2,'I10','1'", 'GY_YH001001', 'YH_JB001', None]
            if v[1] != None:
                # 测试规则不能为空

                if var1 == None and v[0] == None:
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "OK" and v[0] == "OK":
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "ERROR" and v[0] == "ERROR":
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "ALL":
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)

    def _getIdcard(self, d, k, varSheetName, Openpyxl_PO, TOKEN):
        # 在"疾病身份证" sheet中获取对应的身份证
        varIdcard = None
        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
        for k1, v1 in d_code_Idcard.items():
            if k1 == d['diseaseRuleCode']:
                varIdcard = v1
                break
        d["varIdcard"] = varIdcard
        if varIdcard != None:
            varQty, varLog = self.rule(d, Openpyxl_PO, TOKEN)  # PG_JZS001, r1, Openpyxl_PO, TOKEN
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
        else:
            print("error, 身份证为None")
    def _getIdcard2(self,d, k, varSheetName, Openpyxl_PO, TOKEN):
        # 在"疾病身份证" sheet中获取对应的身份证
        varIdcard = None
        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
        for k1, v1 in d_code_Idcard.items():
            if k1 == d['diseaseRuleCode']:
                varIdcard = v1
                break
        d["varIdcard"] = varIdcard
        if varIdcard != None:
            varQty, varLog = self.rule(d, Openpyxl_PO, TOKEN)  # PG_JZS001, r1, Openpyxl_PO, TOKEN
            if d['hitQty'] == 2:
                self.outResult2(varQty, varLog, k, varSheetName, Openpyxl_PO)
            elif d['hitQty'] == None:
                self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
        else:
            print("error, 身份证为None")

    def param1(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]  # OK
            d['testRuleName'] = l_v1[0]  # r1
            d['testRuleParam'] = l_v1[1].replace(".and.", ',')  # AGE='58'.and.DRINKING_FREQUENCY_CODE='3'
            d['interventionRule'] = v[2]  # GY_GW001001  //干预规则编码
            varQty, varLog = self.rule(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误 或 TOKEN没有传入!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)

    def param2(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2].replace(".and.", ',')
            d['interventionRule'] = v[2]
            varQty, varLog = self.rule(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)

    def param4(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['testRuleParam3'] = l_v1[3]
            d['testRuleParam4'] = l_v1[4]
            d['interventionRule'] = v[2]
            varQty, varLog = self.rule(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)

    def param1_idcard(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = l_v1[1]
            d['interventionRule'] = v[2]
            d['diseaseRuleCode'] = v[3]
            self._getIdcard(d, k, varSheetName, Openpyxl_PO, TOKEN)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)

    def param2_idcard(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['interventionRule'] = v[2]
            d['diseaseRuleCode'] = v[3]
            self._getIdcard(d, k, varSheetName, Openpyxl_PO, TOKEN)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)

    def param1_idcard_hitQty2(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = l_v1[1] .replace(".and.", ',')
            d['interventionRule'] = v[2]
            d['diseaseRuleCode'] = v[3]
            d['hitQty'] = v[4]
            self._getIdcard2(d, k, varSheetName, Openpyxl_PO, TOKEN)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)

    def param3_idcard_hitQty2(self, v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN):
        Color_PO.consoleColor("31", "36", ("[" + str(varSheetName) + " => " + str(k) + "(" + str(l_v1[0]) + ")]"), "")
        try:
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['testRuleParam3'] = l_v1[3] .replace(".and.", ',')
            d['interventionRule'] = v[2]
            d['diseaseRuleCode'] = v[3]
            d['hitQty'] = v[4]
            self._getIdcard2(d, k, varSheetName, Openpyxl_PO, TOKEN)
        except:
            Color_PO.consoleColor("31", "31", "FormatError: '" + str(v[1]) + "'格式错误!", "")
            self.outResult1(0, "测试规则的格式错误!", k, varSheetName, Openpyxl_PO)


    def main_rule(self, k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN):

        # print(v)  # [None, "r11,AGE='58'.and.DRINKING_FREQUENCY_CODE='3'", 'GY_GW001001', 'GW_JB001', 2]

        try:
            l_v1 = Str_PO.str2list(v[1])
            # print(l_v1)  # ['r11', "AGE='58'.and.DRINKING_FREQUENCY_CODE='3'"]
            varParam = l_v1[1] .replace(".and.", ',')
        except:
            Color_PO.consoleColor("31", "31", "FormatError: Sheet '" + varSheetName + "', line " + str(k) + ", 测试规则 '" + str(v[1]) + "' is not standardized!", "")
            # print("FormatError: Sheet '" + varSheetName + "', line " + str(k) + ", 测试规则 '" + str(v[1]) + "' is not standardized!")
            # sys.exit(0)

        if (l_v1[0] == "r1" and var3_rule == "r1") or (l_v1[0] == "r6" and var3_rule == "r6") or (l_v1[0] == "r12" and var3_rule == "r12"):
            # 带参数1
            self.param1(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif (l_v1[0] == "r3" and var3_rule == "r3") or (l_v1[0] == "r4" and var3_rule == "r4") or (l_v1[0] == "r8" and var3_rule == "r8"):
            # 带参数2
            self.param2(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r7" and var3_rule == "r7":
            # 带参数4
            self.param4(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif (l_v1[0] == "r9" and var3_rule == "r9") or (l_v1[0] == "r10" and var3_rule == "r10") :
            # 带参数1（自动匹配身份证）
            self.param1_idcard(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r2" and var3_rule == "r2":
            # 带参数2（自动匹配身份证）
            self.param2_idcard(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r11" and var3_rule == "r11":
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r5" and var3_rule == "r5":
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "GW" and var3_rule == "GW":

            d = {}
            d['result'] = v[0]
            d['diseaseRuleCode'] = v[3]
            d['interventionRule'] = v[2]
            Color_PO.consoleColor("31", "36", (str(varSheetName) + ", line " + str(k) + ", " + str(v[3])).center(100, "_"), "")
            # print(str(varSheetName) + ", line " + str(k) + ", " + str(v[3])).center(100, "_")

            # 格式化测试规则
            # print(l_v1) # ['GW', 'QTY0:0', 'PG_SHXG005:1', 'PG_SHXG007:1', 'PG_STZB005:1', 'PG_JZS006:1', 'PG_JWS015:1', 'PG_JWS013:1']
            l_v1.pop(0)
            d_v1 = List_PO.list2dictByKeyValue(l_v1)

            # 3，获取身份证（在"疾病身份证" sheet中获取对应的身份证）
            varIdcard = None
            d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
            for k1, v1 in d_code_Idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard

            # 4，执行语句及输出
            d_all, log = self.gw(d, Openpyxl_PO, TOKEN)
            print("预期：", d_v1)
            print("实测：", d_all)
            if d_all == d_v1:
                self.outResultGW(1, log, k, v[3], varSheetName, Openpyxl_PO)
            else:
                self.outResultGW(0, log, k, v[3], varSheetName, Openpyxl_PO)


    def runRule_AsteriskNone(self, var1, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # ChcRule_PO.run('健康评估', None, None, Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "OK", None, Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ERROR", None, Openpyxl_PO, TOKEN)

        for k, v in d_paramCode.items():
            # print(v)  # [None, "r2,'I10','1'", 'GY_YH001001', 'YH_JB001', None]

            if v[1] != None:

                if var1 == None and v[0] == None:
                    self.main(k, v, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "OK" and v[0] == "OK":
                    self.main(k, v, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "ERROR" and v[0] == "ERROR":
                    self.main(k, v, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "ALL":
                    self.main(k, v, varSheetName, Openpyxl_PO, TOKEN)

    def main(self, k, v, varSheetName, Openpyxl_PO, TOKEN):

        try:
            l_v1 = Str_PO.str2list(v[1])
            # print(l_v1)  # ['r11', "AGE='58'.and.DRINKING_FREQUENCY_CODE='3'"]
            varParam = l_v1[1] .replace(".and.", ',')
        except:
            Color_PO.consoleColor("31", "31", "FormatError: Sheet '" + varSheetName + "', line " + str(k) + ", 测试规则 '" + str(v[1]) + "' is not standardized!", "")
            # print("FormatError: Sheet '" + varSheetName + "', line " + str(k) + ", 测试规则 '" + str(v[1]) + "' is not standardized!")


        if (l_v1[0] == "r1") or (l_v1[0] == "r6") or (l_v1[0] == "r12") :
            # 带参数1
            self.param1(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif (l_v1[0] == "r3") or (l_v1[0] == "r4" ) or (l_v1[0] == "r8"):
            # 带参数2
            self.param2(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r7":
            # 带参数4
            self.param4(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif (l_v1[0] == "r9") or (l_v1[0] == "r10"):
            # 带参数1（自动匹配身份证）
            self.param1_idcard(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r2":
            # 带参数2（自动匹配身份证）
            self.param2_idcard(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r11" :
            # 带参数1，健康干预两次命中（干预+疾病评估）
            self.param1_idcard_hitQty2(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)
        elif l_v1[0] == "r5" :
            # 带参数3，健康干预两次命中（干预+疾病评估）
            self.param3_idcard_hitQty2(v, l_v1, k, varSheetName, Openpyxl_PO, TOKEN)


    def run(self, varSheetName, var1, var3_rule, Openpyxl_PO, TOKEN):

        '''
        :param Openpyxl_PO:
        :param TOKEN:
        :return:
        '''

        # 1，获取 测试结果、测试规则、干预规则编码等数据
        if varSheetName == "健康干预":
            l_varColNums = [1, 3, 5, 7, 8]
            l_paramCode = (Openpyxl_PO.getColByPartialColByUnwantedRow(l_varColNums, [1], varSheetName))  # 获取第1,3,5,7列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
            # print(l_paramCode[2])  # GY_YH001001  //干预规则编码
            # print(l_paramCode[3])  # YH_JB008  //疾病评估规则编码
            # print(l_paramCode[4])  # 2  //命中次数
        elif varSheetName == "健康评估":
            l_varColNums = [1, 3, 5, 6]
            l_paramCode = (Openpyxl_PO.getColByPartialColByUnwantedRow(l_varColNums, [1], varSheetName))  # 获取第1,3,5列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
            # print(l_paramCode[2])  # PG_SHXG001   //评估规则编码
            # print(l_paramCode[3])  # 家族史
        elif varSheetName == "疾病评估规则（已患和高风险）":
            l_varColNums = [1, 3, 9, 5]
            l_paramCode = (Openpyxl_PO.getColByPartialColByUnwantedRow(l_varColNums, [1], varSheetName))  # 获取第1,3,5列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
            # print(l_paramCode[2])  # PG_JWS018  //健康评估规则库编码
            # print(l_paramCode[3])  # YH_JB001  //疾病评估规则编码
        elif varSheetName == "健康干预_中医体质辨识":
            l_varColNums = [1, 3, 5, 7]
            l_paramCode = (Openpyxl_PO.getColByPartialColByUnwantedRow(l_varColNums, [1], varSheetName))  # 获取第1,3,5列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r12,ABNORMAL_STATUS
            # print(l_paramCode[2])  # GY_TZBS01  //干预规则编码
            # print(l_paramCode[3])  # YH_JB001  //干预规则

        # 换成字典
        list1 = []
        listall = []
        for i in range(len(l_paramCode[1])):
            for j in range(len(l_varColNums)):
                list1.append(l_paramCode[j][i])
            listall.append(list1)
            list1 = []
        d_paramCode = List_PO.list2dictByIndex(listall, 2)
        print(d_paramCode)  # {2: ['OK', "r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'", 'GY_YH001001', "高血压已患='是'"], 3: ['OK', "r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='E11'", 'GY_YH002001', "糖尿病已患='是'"]}
        sys.exit(0)

        if var1 == None:
            if var3_rule == None:
                # 执行测试结果为空的所有用例
                # ChcRule_PO.run('健康评估', None, None, Openpyxl_PO, TOKEN)
                self.runRule_AsteriskNone(var1, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
            else:
                # 执行测试结果为空的r1用例
                # ChcRule_PO.run('健康评估', None, "r1", Openpyxl_PO, TOKEN)
                self.runRule_AsteriskRule(var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
        else:
            if var3_rule == None:
                # 执行测试结果为ERROR/OK的所有用例
                # ChcRule_PO.run('健康评估', "ERROR", None, Openpyxl_PO, TOKEN)
                # ChcRule_PO.run('健康评估', "OK", None, Openpyxl_PO, TOKEN)
                self.runRule_AsteriskNone(var1, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
            else:
                # 执行测试结果为ERROR/OK的r11用例
                # ChcRule_PO.run('健康评估', "OK", "r1", Openpyxl_PO, TOKEN)
                # ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)
                self.runRule_AsteriskRule(var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
        Openpyxl_PO.setAllCellDimensionsHeight(30, varSheetName)



    def rule(self, d, Openpyxl_PO, TOKEN):

        # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam1': "'E11'", 'testRuleParam2': "'1'", 'ruleCode': 'GY_YH002001', 'diseaseRuleCode': 'YH_JB002', 'varIdcard': '310101202308070002'}

        log = ""
        varQTY = 0
        varQ2 = 0

        # 1，遍历所有列获取值
        l_all = Openpyxl_PO.getColValue("testRule")
        i_newAssessStatus = 0
        for i in range(len(l_all)):
            if d['testRuleName'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:

                        if 'varIdcard' in d:
                            command = str(command).replace("{身份证}", d['varIdcard'])
                        if 'testRuleParam1' in d:
                            command = str(command).replace("{测试规则参数1}", d['testRuleParam1'])
                        if 'testRuleParam2' in d:
                            command = str(command).replace("{测试规则参数2}", d['testRuleParam2'])
                        if 'testRuleParam3' in d:
                            command = str(command).replace("{测试规则参数3}", d['testRuleParam3'])
                        if 'testRuleParam4' in d:
                            command = str(command).replace("{测试规则参数4}", d['testRuleParam4'])
                        if 'testRuleParam' in d:
                            command = str(command).replace("{测试规则参数}", d['testRuleParam'])
                        if 'interventionRule' in d:
                            command = str(command).replace("{规则编码}", d['interventionRule'])
                        if "{随机数}" in command:
                            command = str(command).replace("{随机数}", Data_PO.getPhone())

                        varID = Openpyxl_PO.getCell(21, 1, "testRule")
                        varIdcard = Openpyxl_PO.getCell(22, 1, "testRule")
                        varQTY = Openpyxl_PO.getCell(23, 1, "testRule")
                        varRunRule = Openpyxl_PO.getCell(24, 1, "testRule")
                        varNewAssess = Openpyxl_PO.getCell(25, 1, "testRule")
                        varGUID = Openpyxl_PO.getCell(26, 1, "testRule")
                        varQ2 = Openpyxl_PO.getCell(27, 1, "testRule")

                        if varID != None:
                            if "varID=" in varID:
                                varID = varID.split("varID=")[1].split(")")[0]
                                command = str(command).replace("{varID}", varID)
                        if varIdcard != None:
                            if "varIdcard" in varIdcard:
                                varIdcard = varIdcard.split("varIdcard=")[1].split(")")[0]
                                command = str(command).replace("{varIdcard}", varIdcard)
                        # print(varQTY)
                        if varQTY != None:
                            if "varQTY" in varQTY:
                                varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                        if varGUID != None:
                            if "varGUID" in varGUID:
                                varGUID = varGUID.split("varGUID=")[1].split(")")[0]
                                command = str(command).replace("{varGUID}", varGUID)

                        if varRunRule != None and varRunRule != "":
                            # print(type(varRunRule))
                            # varRunRule = varRunRule.split("varRunRule=")[1].split(")")[0]
                            log = log + "\n" + varRunRule
                        if varNewAssess != None and varNewAssess != "":
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            log = log + "\n" + varNewAssess

                        # 步骤日志
                        log = log + "\n" + str(j + 1) + ", " + command

                        if "hitQty" in d:
                            if d['hitQty'] == 2:
                                if '{疾病评估规则编码}' in command:
                                    command = str(command).replace("{疾病评估规则编码}", d['diseaseRuleCode'])
                                    a = eval(command)
                                    if "Q2" in a[0]:
                                        varQ2 = a[0]['Q2']
                                        Openpyxl_PO.setCellValue(27, 1, "varQ2=" + str(varQ2), "testRule")
                                else:
                                    a = eval(command)
                                    sleep(1)

                                Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                            else:
                                if '{疾病评估规则编码}' not in command:
                                    Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                                varQ2 = 0
                                a = eval(command)
                                sleep(1)
                        else:
                            varQ2 = 0
                            if '{疾病评估规则编码}' not in command:
                                Color_PO.consoleColor("31", "33", str(j + 1) + ", " + command, "")
                                if "{" in command and "}" in command :
                                    varName = command.split("{")[1].split("}")[0]
                                    Color_PO.consoleColor("31", "31", "FormatError: {" + varName + "} 没有正确赋值!", "")
                                else:
                                    a = eval(command)
                                    sleep(1)


                        if a != None:
                            if isinstance(a, list) and a != []:
                                if isinstance(a[0], dict):
                                    # print(a[0])

                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        Openpyxl_PO.setCellValue(21, 1, "varID=" + str(varID), "testRule")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        Openpyxl_PO.setCellValue(22, 1, "varIdcard=" + str(varIdcard), "testRule")
                                    if "QTY" in a[0]:
                                        print(a[0])
                                        varQTY = a[0]['QTY']
                                        Openpyxl_PO.setCellValue(23, 1, "varQTY=" + str(varQTY), "testRule")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        Openpyxl_PO.setCellValue(26, 1, "varGUID=" + str(varGUID), "testRule")
                                    if "name" in a[0]:
                                        Openpyxl_PO.setCellValue(24, 1, "", "testRule")
                                        Openpyxl_PO.setCellValue(25, 1, "", "testRule")
                                        if "跑规则" == a[0]['name']:
                                            if a[0]['value'] != 200 :
                                                Openpyxl_PO.setCellValue(24, 1, str(a[0]['value']), "testRule")
                                        if "新增评估" == a[0]['name']:
                                            if a[0]['value'] != 200 :
                                                Openpyxl_PO.setCellValue(25, 1, str(a[0]['value']), "testRule")

                    else:
                        break
        Openpyxl_PO.setCellValue(21, 1, "", "testRule")
        Openpyxl_PO.setCellValue(22, 1, "", "testRule")
        Openpyxl_PO.setCellValue(23, 1, "", "testRule")
        Openpyxl_PO.setCellValue(24, 1, "", "testRule")
        Openpyxl_PO.setCellValue(25, 1, "", "testRule")
        Openpyxl_PO.setCellValue(26, 1, "", "testRule")
        Openpyxl_PO.setCellValue(27, 1, "", "testRule")

        print(varQTY)
        print(varQ2)
        varQTY = int(varQTY) + int(varQ2)
        return varQTY, log

    def gw(self, d, Openpyxl_PO, TOKEN):

        # print(d)  # {'result': None, 'diseaseRuleCode': 'GW_JB009', 'ruleCode': "('GW_JB009','PG_JWS026','PG_JWS027','PG_JWS028','PG_JWS031','PG_JWS032')", 'varIdcard': '410101202308070009'}

        d_all = {}
        log = ""
        varQTY = ""
        i_newAssessStatus = 0

        # 1，遍历所有列获取值
        l_all = Openpyxl_PO.getAllCol("GW")
        for i in range(len(l_all)):
            if d['diseaseRuleCode'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:

                        # 调试
                        # if command == "exit":
                        #     Openpyxl_PO.setCellValue(21, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(22, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(23, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(24, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(25, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(26, 1, "", "testRule")
                        #     Openpyxl_PO.setCellValue(27, 1, "", "testRule")
                        #     return d_all, log

                        if 'varIdcard' in d:
                            command = str(command).replace("{身份证}", d['varIdcard'])
                        if 'interventionRule' in d:
                            command = str(command).replace("{规则编码}", d['interventionRule'])
                        if "{随机数}" in command:
                            command = str(command).replace("{随机数}", Data_PO.getPhone())
                        if 'diseaseRuleCode' in d:
                            command = str(command).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

                        varID = Openpyxl_PO.getCell(21, 1, "testRule")
                        varIdcard = Openpyxl_PO.getCell(22, 1, "testRule")
                        # varQTY = Openpyxl_PO.getCellValue(23, 1, "testRule")
                        varRunRule = Openpyxl_PO.getCell(24, 1, "testRule")
                        varNewAssess = Openpyxl_PO.getCell(25, 1, "testRule")
                        varGUID = Openpyxl_PO.getCell(26, 1, "testRule")
                        # varQTY0 = Openpyxl_PO.getCellValue(27, 1, "testRule")

                        if varID != None:
                            if "varID=" in varID:
                                varID = varID.split("varID=")[1].split(")")[0]
                                command = str(command).replace("{varID}", varID)
                        if varIdcard != None:
                            if "varIdcard" in varIdcard:
                                varIdcard = varIdcard.split("varIdcard=")[1].split(")")[0]
                                command = str(command).replace("{varIdcard}", varIdcard)
                        # if varQTY != None:
                        #     if "varQTY" in varQTY:
                        #         varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                        #         command = str(command).replace("{varQTY}", varQTY)
                        if varRunRule != None and varRunRule != "":
                            # print(type(varRunRule))
                            # varRunRule = varRunRule.split("varRunRule=")[1].split(")")[0]
                            log = log + "\n" + varRunRule
                        if varNewAssess != None and varNewAssess != "":
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            log = log + "\n" + varNewAssess
                        if varGUID != None:
                            if "varGUID" in varGUID:
                                varGUID = varGUID.split("varGUID=")[1].split(")")[0]
                                command = str(command).replace("{varGUID}", varGUID)
                        # if varQTY0 != None:
                        #     if "varQTY0" in varQTY0:
                        #         varQTY0 = varQTY0.split("varQTY0=")[1].split(")")[0]
                        #         print(varQTY0)
                        #         command = str(command).replace("{varQTY0}", varQTY0)

                        Color_PO.consoleColor("31", "33", str(j+1) + ", " + command, "")
                        log = log + "\n" + str(j+1) + ", " + command  # 步骤日志
                        a = eval(command)

                        if a != None:
                            if isinstance(a, list):
                                if isinstance(a[0], dict):
                                    # print(a[0])

                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        Openpyxl_PO.setCellValue(21, 1, "varID=" + str(varID), "testRule")
                                        # Openpyxl_PO.setCellValue(33, 1, str(varID), "testRule")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        Openpyxl_PO.setCellValue(22, 1, "varIdcard=" + str(varIdcard), "testRule")
                                    if "QTY" in a[0]:
                                        varQTY = a[0]['QTY']
                                        Openpyxl_PO.setCellValue(23, 1, "varQTY=" + str(varQTY), "testRule")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        Openpyxl_PO.setCellValue(26, 1, "varGUID=" + str(varGUID), "testRule")
                                    if "QTY0" in a[0]:
                                        # varQTY0 = a[0]['QTY0']
                                        d_all['QTY0'] = str(a[0]['QTY0'])
                                        # print(varQTY0)
                                        # Openpyxl_PO.setCellValue(27, 1, "varQTY0=" + str(varQTY0), "testRule")
                                    if "name" in a[0]:
                                        Openpyxl_PO.setCellValue(24, 1, "", "testRule")
                                        Openpyxl_PO.setCellValue(25, 1, "", "testRule")
                                        if "跑规则" == a[0]['name']:
                                            if a[0]['value'] != 200:
                                                Openpyxl_PO.setCellValue(24, 1, str(a[0]['value']), "testRule")
                                        if "新增评估" == a[0]['name']:
                                            if a[0]['value'] != 200:
                                                Openpyxl_PO.setCellValue(25, 1, str(a[0]['value']), "testRule")

                                    # JB001
                                    if d['diseaseRuleCode'] == 'GW_JB001':
                                        if "GW_JB001" in a[0]: d_all['GW_JB001'] = str(a[0]['GW_JB001'])
                                        if "PG_Age001" in a[0]: d_all['PG_Age001'] = str(a[0]['PG_Age001'])
                                        if "PG_SHXG001" in a[0]:d_all['PG_SHXG001'] = str(a[0]['PG_SHXG001'])
                                        if "PG_SHXG002" in a[0]:d_all['PG_SHXG002'] = str(a[0]['PG_SHXG002'])
                                        if "PG_STZB001" in a[0]:d_all['PG_STZB001'] = str(a[0]['PG_STZB001'])
                                        if "PG_STZB002" in a[0]:d_all['PG_STZB002'] = str(a[0]['PG_STZB002'])
                                        if "PG_SHXG004" in a[0]:d_all['PG_SHXG004'] = str(a[0]['PG_SHXG004'])
                                        if "PG_JYZB001" in a[0]:d_all['PG_JYZB001'] = str(a[0]['PG_JYZB001'])
                                        if "PG_JYZB002" in a[0]:d_all['PG_JYZB002'] = str(a[0]['PG_JYZB002'])
                                        if "PG_JZS001" in a[0]: d_all['PG_JZS001'] = str(a[0]['PG_JZS001'])
                                        if "PG_JWS001" in a[0]: d_all['PG_JWS001'] = str(a[0]['PG_JWS001'])
                                    elif d['diseaseRuleCode'] == 'GW_JB002':
                                        if "GW_JB002" in a[0]: d_all['GW_JB002'] = str(a[0]['GW_JB002'])
                                        if "PG_Age002" in a[0]: d_all['PG_Age002'] = str(a[0]['PG_Age002'])
                                        if "PG_JYZB003" in a[0]: d_all['PG_JYZB003'] = str(a[0]['PG_JYZB003'])
                                        if "PG_JWS002" in a[0]: d_all['PG_JWS002'] = str(a[0]['PG_JWS002'])
                                        if "PG_JWS003" in a[0]: d_all['PG_JWS003'] = str(a[0]['PG_JWS003'])
                                        if "PG_JWS004" in a[0]: d_all['PG_JWS004'] = str(a[0]['PG_JWS004'])
                                        if "PG_JWS005" in a[0]: d_all['PG_JWS005'] = str(a[0]['PG_JWS005'])
                                        if "PG_JWS006" in a[0]: d_all['PG_JWS006'] = str(a[0]['PG_JWS006'])
                                        if "PG_JWS007" in a[0]: d_all['PG_JWS007'] = str(a[0]['PG_JWS007'])
                                        if "PG_JZS002" in a[0]: d_all['PG_JZS002'] = str(a[0]['PG_JZS002'])
                                        if "PG_YWZL001" in a[0]: d_all['PG_YWZL001'] = str(a[0]['PG_YWZL001'])
                                        if "PG_SHXG004" in a[0]: d_all['PG_SHXG004'] = str(a[0]['PG_SHXG004'])
                                        if "PG_JYZB004" in a[0]: d_all['PG_JYZB004'] = str(a[0]['PG_JYZB004'])
                                        if "PG_JYZB005" in a[0]: d_all['PG_JYZB005'] = str(a[0]['PG_JYZB005'])
                                        if "PG_YWZL002" in a[0]: d_all['PG_YWZL002'] = str(a[0]['PG_YWZL002'])
                                        if "PG_STZB001" in a[0]: d_all['PG_STZB001'] = str(a[0]['PG_STZB001'])
                                        if "PG_STZB003" in a[0]: d_all['PG_STZB003'] = str(a[0]['PG_STZB003'])
                                    elif d['diseaseRuleCode'] == 'GW_JB003':
                                        if "GW_JB003" in a[0]: d_all['GW_JB003'] = str(a[0]['GW_JB003'])
                                        if "PG_JWS008" in a[0]: d_all['PG_JWS008'] = str(a[0]['PG_JWS008'])
                                        if "PG_JWS007" in a[0]: d_all['PG_JWS007'] = str(a[0]['PG_JWS007'])
                                        if "PG_JWS001" in a[0]: d_all['PG_JWS001'] = str(a[0]['PG_JWS001'])
                                        if "PG_JZS003" in a[0]: d_all['PG_JZS003'] = str(a[0]['PG_JZS003'])
                                        if "PG_SHXG004" in a[0]: d_all['PG_SHXG004'] = str(a[0]['PG_SHXG004'])
                                        if "PG_SHXG005" in a[0]: d_all['PG_SHXG005'] = str(a[0]['PG_SHXG005'])
                                        if "PG_JYZB001" in a[0]: d_all['PG_JYZB001'] = str(a[0]['PG_JYZB001'])
                                        if "PG_STZB004" in a[0]: d_all['PG_STZB004'] = str(a[0]['PG_STZB004'])
                                        if "PG_JWS009" in a[0]: d_all['PG_JWS009'] = str(a[0]['PG_JWS009'])
                                        if "PG_JWS010" in a[0]: d_all['PG_JWS010'] = str(a[0]['PG_JWS010'])
                                        if "PG_JWS011" in a[0]: d_all['PG_JWS011'] = str(a[0]['PG_JWS011'])
                                    elif d['diseaseRuleCode'] == 'GW_JB004':
                                        if "GW_JB004" in a[0]: d_all['GW_JB004'] = str(a[0]['GW_JB004'])
                                        if "PG_Age003" in a[0]: d_all['PG_Age003'] = str(a[0]['PG_Age003'])
                                        if "PG_JWS001" in a[0]: d_all['PG_JWS001'] = str(a[0]['PG_JWS001'])
                                        if "PG_JWS007" in a[0]: d_all['PG_JWS007'] = str(a[0]['PG_JWS007'])
                                        if "PG_JZS004" in a[0]: d_all['PG_JZS004'] = str(a[0]['PG_JZS004'])
                                        if "PG_JZS005" in a[0]: d_all['PG_JZS005'] = str(a[0]['PG_JZS005'])
                                        if "PG_JYZB006" in a[0]: d_all['PG_JYZB006'] = str(a[0]['PG_JYZB006'])
                                        if "PG_JYZB007" in a[0]: d_all['PG_JYZB007'] = str(a[0]['PG_JYZB007'])
                                        if "PG_JYZB008" in a[0]: d_all['PG_JYZB008'] = str(a[0]['PG_JYZB008'])
                                        if "PG_JYZB009" in a[0]: d_all['PG_JYZB009'] = str(a[0]['PG_JYZB009'])
                                        if "PG_JWS012" in a[0]: d_all['PG_JWS012'] = str(a[0]['PG_JWS012'])
                                    elif d['diseaseRuleCode'] == 'GW_JB005':
                                        if "GW_JB005" in a[0]: d_all['GW_JB005'] = str(a[0]['GW_JB005'])
                                        # if "PG_Age004" in a[0]: d_all['PG_Age004'] = str(a[0]['PG_Age004'])
                                        if "PG_SHXG005" in a[0]: d_all['PG_SHXG005'] = str(a[0]['PG_SHXG005'])
                                        if "PG_JWS013" in a[0]: d_all['PG_JWS013'] = str(a[0]['PG_JWS013'])
                                        if "PG_JZS006" in a[0]: d_all['PG_JZS006'] = str(a[0]['PG_JZS006'])
                                        if "PG_SHXG007" in a[0]: d_all['PG_SHXG007'] = str(a[0]['PG_SHXG007'])
                                        if "PG_JWS015" in a[0]: d_all['PG_JWS015'] = str(a[0]['PG_JWS015'])
                                        if "PG_STZB005" in a[0]: d_all['PG_STZB005'] = str(a[0]['PG_STZB005'])
                                    elif d['diseaseRuleCode'] == 'GW_JB006':
                                        if "GW_JB006" in a[0]: d_all['GW_JB006'] = str(a[0]['GW_JB006'])
                                        if "PG_Age005" in a[0]: d_all['PG_Age005'] = str(a[0]['PG_Age005'])
                                        if "PG_JWS016" in a[0]: d_all['PG_JWS016'] = str(a[0]['PG_JWS016'])
                                        if "PG_JWS017" in a[0]: d_all['PG_JWS017'] = str(a[0]['PG_JWS017'])
                                        if "PG_JWS018" in a[0]: d_all['PG_JWS018'] = str(a[0]['PG_JWS018'])
                                        if "PG_JZS007" in a[0]: d_all['PG_JZS007'] = str(a[0]['PG_JZS007'])
                                        if "PG_SHXG009" in a[0]: d_all['PG_SHXG009'] = str(a[0]['PG_SHXG009'])
                                        if "PG_SHXG005" in a[0]: d_all['PG_SHXG005'] = str(a[0]['PG_SHXG005'])
                                    elif d['diseaseRuleCode'] == 'GW_JB007':
                                        if "GW_JB007" in a[0]: d_all['GW_JB007'] = str(a[0]['GW_JB007'])
                                        if "PG_Age006" in a[0]: d_all['PG_Age006'] = str(a[0]['PG_Age006'])
                                        if "PG_JWS021" in a[0]: d_all['PG_JWS021'] = str(a[0]['PG_JWS021'])

                                    elif d['diseaseRuleCode'] == 'GW_JB009':
                                        if "GW_JB009" in a[0]: d_all['GW_JB009'] = str(a[0]['GW_JB009'])
                                        if "PG_Age007" in a[0]: d_all['PG_Age007'] = str(a[0]['PG_Age007'])
                                        if "PG_JWS026" in a[0]: d_all['PG_JWS026'] = str(a[0]['PG_JWS026'])
                                        if "PG_JWS027" in a[0]: d_all['PG_JWS027'] = str(a[0]['PG_JWS027'])
                                        if "PG_JWS028" in a[0]: d_all['PG_JWS028'] = str(a[0]['PG_JWS028'])
                                        if "PG_JWS031" in a[0]: d_all['PG_JWS031'] = str(a[0]['PG_JWS031'])
                                        if "PG_JWS032" in a[0]: d_all['PG_JWS032'] = str(a[0]['PG_JWS032'])
                                    elif d['diseaseRuleCode'] == 'GW_JB010':
                                        if "GW_JB010" in a[0]: d_all['GW_JB010'] = str(a[0]['GW_JB010'])
                                        if "PG_Age008" in a[0]: d_all['PG_Age008'] = str(a[0]['PG_Age008'])
                                        if "PG_JWS033" in a[0]: d_all['PG_JWS033'] = str(a[0]['PG_JWS033'])
                                        if "PG_JWS034" in a[0]: d_all['PG_JWS034'] = str(a[0]['PG_JWS034'])
                                        if "PG_JWS035" in a[0]: d_all['PG_JWS035'] = str(a[0]['PG_JWS035'])
                                        if "PG_JYZB010" in a[0]: d_all['PG_JYZB010'] = str(a[0]['PG_JYZB010'])
                                        if "PG_JWS037" in a[0]: d_all['PG_JWS037'] = str(a[0]['PG_JWS037'])
                                    elif d['diseaseRuleCode'] == 'GW_JB011':
                                        if "GW_JB011" in a[0]: d_all['GW_JB011'] = str(a[0]['GW_JB011'])
                                        if "PG_JWS041" in a[0]: d_all['PG_JWS041'] = str(a[0]['PG_JWS041'])
                                        if "PG_JWS043" in a[0]: d_all['PG_JWS043'] = str(a[0]['PG_JWS043'])

                            # if isinstance(a, tuple):
                            #     if "跑规则" in a[0]:
                            #         varRunRule = a[1]
                            #         Openpyxl_PO.setCellValue(24, 1, "varRunRule=" + str(varRunRule), "testRule")
                            #     if "新增评估" in a[0]:
                            #         varNewAssess = a[1]
                            #         Openpyxl_PO.setCellValue(25, 1, "varNewAssess=" + str(varNewAssess), "testRule")
                    else:
                        break
        Openpyxl_PO.setCellValue(21, 1, "", "testRule")
        Openpyxl_PO.setCellValue(22, 1, "", "testRule")
        Openpyxl_PO.setCellValue(23, 1, "", "testRule")
        Openpyxl_PO.setCellValue(24, 1, "", "testRule")
        Openpyxl_PO.setCellValue(25, 1, "", "testRule")
        Openpyxl_PO.setCellValue(26, 1, "", "testRule")
        Openpyxl_PO.setCellValue(27, 1, "", "testRule")

        log = log + "\n" + str(d_all)
        return d_all, log
