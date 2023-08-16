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

        l_code_Idcard = Openpyxl_PO.getColValueByCol([1, 3], [1], "疾病身份证")
        d_code_Idcard = dict(zip(l_code_Idcard[0], l_code_Idcard[1]))
        return (d_code_Idcard)  # {'YH_JB001': '310101202308070001', 'YH_JB002': '310101202308070002'}

    def i_AssessRuleRecord(self, var, token):

        '''
        跑规则  i_AssessRuleRecord
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
            log = "跑规则, " + str(d_r)
            print(log)
            return ("跑规则", log)
        else:
            log = "跑规则, 200"
            print(log)
            return ("跑规则", log)

    def i_newAssess(self, varIdcard, token):

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
        # print(str_r)
        d_r = json.loads(str_r)
        if 'code' in d_r:
            if d_r['code'] != 200:
                log = "新增评估, " + str_r
                print(log)
                return ("新增评估", log)
            else:
                log = "新增评估, 200 "
                print(log)
                return ("新增评估", log)
        else:
            # {"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            log = "新增评估, " + str_r
            print(log)
            return ("新增评估", log)

    def outResult1(self, varQty, varLog, k, varSheetName, Openpyxl_PO):

        if varQty == "1" or varQty == 1 :
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
            Color_PO.consoleColor("31", "36", str(k) + " => OK\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
            Color_PO.consoleColor("31", "31", str(k) + " => ERROR\n", "")
            Openpyxl_PO.setCellValue(k, 2, varLog, varSheetName)
            Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)

    # def outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO):
    #
    #     if varQty == 1:
    #         Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
    #         Color_PO.consoleColor("31", "36", str(k) + " => OK\n", "")
    #         Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
    #         Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
    #         Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
    #     else:
    #         Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
    #         Color_PO.consoleColor("31", "31", str(k) + " => ERROR\n", "")
    #         Openpyxl_PO.setCellValue(k, 2, varLog, varSheetName)
    #         Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
    #         Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)


    def outResultGW(self, result, log, k, varSheetName, Openpyxl_PO):

        ''' GW 前置条件'''

        if result == 1:
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
            Color_PO.consoleColor("31", "36", str(k) + " => OK\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
            Color_PO.consoleColor("31", "31", str(k) + " => ERROR\n", "")
            Openpyxl_PO.setCellValue(k, 2, log, varSheetName)
            Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)





    def runRule_AsteriskRule(self, var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # ChcRule_PO.run('健康评估', None, "r6", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "OK", "r6", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ALL", "r6", Openpyxl_PO, TOKEN)

        for k, v in d_paramCode.items():
            # print(v)  # ['OK', 'r1,AGE=55', 'PG_Age001', '年龄']

            if v[1] != None:
                if var1 == None and v[0] == None:
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "OK" and v[0] == "OK":
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "ERROR" and v[0] == "ERROR":
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
                elif var1 == "ALL":
                    self.main_rule(k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN)
    def main_rule(self, k, v, var3_rule, varSheetName, Openpyxl_PO, TOKEN):

        # print(v)  # ["OK", 'r1,AGE=55', 'PG_Age001', '年龄']

        try:
            l_v1 = Str_PO.str2list(v[1])
            varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
            varParam = varParam.replace(".and.", ',')
        except:
            print("error, 测试规则 " + str(v[1]) + " 格式错误！")

        # print(l_v1)

        if l_v1[0] == "r1" and var3_rule == "r1":
            # 实例：r1,DIAGNOSIS_CODE='I10'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r2" and var3_rule == "r2":
            # 实例： r2, 'I10'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            d['diseaseRuleCode'] = v[3]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001'}

            # 在"疾病身份证" sheet中获取对应的身份证
            varIdcard = None
            d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
            for k1, v1 in d_code_Idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001', 'varIdcard': '310101202308070001'}

            if varIdcard != None:
                varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)  # 家族史, PG_JZS001, r1, Openpyxl_PO, TOKEN
                self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
            else:
                print("error, 身份证为None")

        elif l_v1[0] == "r3" and var3_rule == "r3":
            # 实例："r3,'I10'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r4" and var3_rule == "r4":
            # 分解 "r4,  '01','JB002'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r5" and var3_rule == "r5":
            # 实例： r5,'I10',HALOPHILIA_CODE=2
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)


        elif l_v1[0] == "r6" and var3_rule == "r6":
            # 分解 "r6, '01'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r7" and var3_rule == "r7":
            # 实例："r7,"I10","N03"
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r8" and var3_rule == "r8":
            # 实例： r8,'现在每天吸'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r9" and var3_rule == "r9":
            # 实例： r9,'高血压'
            d = {}
            # print(v)
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            d['diseaseRuleCode'] = v[3]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001'}

            # 在"疾病身份证" sheet中获取对应的身份证
            varIdcard = None
            d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
            for k1, v1 in d_code_Idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001', 'varIdcard': '310101202308070001'}

            if varIdcard != None:
                varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)  # PG_JZS001, r1, Openpyxl_PO, TOKEN
                self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
            else:
                print("error, 身份证为None")

        elif l_v1[0] == "r10" and var3_rule == "r10":
            # 实例： r9,'高血压'
            d = {}
            # print(v)
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            d['diseaseRuleCode'] = v[3]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001'}

            # 在"疾病身份证" sheet中获取对应的身份证
            varIdcard = None
            d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
            for k1, v1 in d_code_Idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001', 'varIdcard': '310101202308070001'}

            if varIdcard != None:
                varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)  # PG_JZS001, r1, Openpyxl_PO, TOKEN
                self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
            else:
                print("error, 身份证为None")


        elif l_v1[0] == "GW" and var3_rule == "GW":
            # 实例：GW_JB004

            print(v)
            d = {}
            d['result'] = v[0]
            d['diseaseRuleCode'] = v[3]  # GW_JB004
            d['ruleCode'] = v[2] # ('GW_JB004','PG_AGE003','PG_JWS001','PG_JWS007','PG_JWS012','PG_JZS004','PG_JZS005','PG_JYZB006','PG_JYZB007','PG_JYZB008','PG_JYZB009')
            # print(d)

            # print(l_v1)
            l_v1.pop(0)
            d_v1 = List_PO.list2dictByKeyValue(l_v1)
            print("d_v1", d_v1)

            # sys.exit(0)

            print(str(k) + " => (" + v[3] + ")")
            # 在"疾病身份证" sheet中获取对应的身份证
            varIdcard = None
            d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
            for k1, v1 in d_code_Idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard

            d_all, log = self.gw(d, Openpyxl_PO, TOKEN)
            print("d_v11", d_v1)
            print("d_all", d_all)
            print("d_v11", str(d_v1))
            print("d_all", str(d_all))

            if d_all == d_v1:
                self.outResultGW(1, log, k, varSheetName, Openpyxl_PO)
            else:
                self.outResultGW(0, log, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r11" and var3_rule == "r11":
            # 实例： r11,AGE=66,AGE=65
            d = {}
            print(v)
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[3]
            print(d)
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)


    def runRule_AsteriskNone(self, var1, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # ChcRule_PO.run('健康评估', None, None, Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "OK", "", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ERROR", "", Openpyxl_PO, TOKEN)
        # ChcRule_PO.run('健康评估', "ALL", "", Openpyxl_PO, TOKEN)

        for k, v in d_paramCode.items():
            # print(v)  # ['OK', 'r1,AGE=55', 'PG_Age001', '年龄']

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
            varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
            varParam = varParam.replace(".and.", ',')
        except:
            print("error, 测试规则 " + str(v[1]) + " 格式错误！")

        if l_v1[0] == "r1":
            # 实例：r1,DIAGNOSIS_CODE='I10'

            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r2":
            # 实例： r2, 'I10'

            print(v)

            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            d['diseaseRuleCode'] = v[3]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001'}

            # 在"疾病身份证" sheet中获取对应的身份证
            varIdcard = None
            d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
            for k1, v1 in d_code_Idcard.items():
                if k1 == d['diseaseRuleCode']:
                    varIdcard = v1
                    break
            d["varIdcard"] = varIdcard
            # print(d)  # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001', 'varIdcard': '310101202308070001'}

            if varIdcard != None:
                varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)  # 家族史, PG_JZS001, r1, Openpyxl_PO, TOKEN
                self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)
            else:
                print("error, 身份证为None")



        elif l_v1[0] == "r7":
            # 实例："r7,"I10","N03"
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r3":
            # 实例："r3,'I10'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)



        elif l_v1[0] == "r6":

            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam'] = varParam
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r4":
            # 分解 "r4,  '01','JB002'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r5":
            # 实例： r5,'I10',HALOPHILIA_CODE=2
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)

        elif l_v1[0] == "r8":
            # 实例： r8,'现在每天吸'
            d = {}
            d['result'] = v[0]
            d['testRuleName'] = l_v1[0]
            d['testRuleParam1'] = l_v1[1]
            d['testRuleParam2'] = l_v1[2]
            d['ruleCode'] = v[2]
            print(str(k) + " => (" + d['testRuleName'] + ")")
            varQty, varLog = self.r1(d, Openpyxl_PO, TOKEN)
            self.outResult1(varQty, varLog, k, varSheetName, Openpyxl_PO)




    def run(self, varSheetName, var1, var3_rule, Openpyxl_PO, TOKEN):

        '''
        :param Openpyxl_PO:
        :param TOKEN:
        :return:
        '''

        # 1，获取 测试结果、测试规则、干预规则编码等数据
        if varSheetName == "健康干预":
            l_varColNums = [1, 3, 5, 7]
            l_paramCode = (Openpyxl_PO.getColValueByCol(l_varColNums, [1], varSheetName))  # 获取第1,3,5,7列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
            # print(l_paramCode[2])  # GY_YH001001  //干预规则编码
            # print(l_paramCode[3])  # YH_JB008  //疾病评估规则编码
        elif varSheetName == "健康评估":
            l_varColNums = [1, 3, 5, 6]
            l_paramCode = (Openpyxl_PO.getColValueByCol(l_varColNums, [1], varSheetName))  # 获取第1,3,5列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
            # print(l_paramCode[2])  # PG_SHXG001   //评估规则编码
            # print(l_paramCode[3])  # 家族史
        elif varSheetName == "疾病评估规则（已患和高风险）":
            l_varColNums = [1, 3, 9, 5]
            l_paramCode = (Openpyxl_PO.getColValueByCol(l_varColNums, [1], varSheetName))  # 获取第1,3,5列值，忽略第一行数据
            # print(l_paramCode[0])  # OK
            # print(l_paramCode[1])  # r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'
            # print(l_paramCode[2])  # PG_JWS018  //健康评估规则库编码
            # print(l_paramCode[3])  # YH_JB001  //疾病评估规则编码


        # 换成字典
        list1 = []
        listall = []
        for i in range(len(l_paramCode[1])):
            for j in range(len(l_varColNums)):
                list1.append(l_paramCode[j][i])
            listall.append(list1)
            list1 = []
        d_paramCode = List_PO.list2dictByIndex(listall, 2)
        # print(d_paramCode)  # {2: ['OK', "r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='I10'", 'GY_YH001001', "高血压已患='是'"], 3: ['OK', "r2,T_HIS_DIAGNOSIS,IDCARD,DIAGNOSIS_CODE='E11'", 'GY_YH002001', "糖尿病已患='是'"]}


        if var1 == "ALL":
            if var3_rule == None:
                # 遍历所有记录
                # ChcRule_PO.run('健康评估', "ALL", None, Openpyxl_PO, TOKEN)
                self.runRule_AsteriskNone(varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
            else:
                # 遍历所有及指定测试规则的记录，如只执行r1
                # ChcRule_PO.run('健康评估', "ALL", "r1", Openpyxl_PO, TOKEN)
                self.runRule_AsteriskRule(var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
        else:
            if var1 == None:
                if var3_rule == None:
                    # ChcRule_PO.run('健康评估', None, None, Openpyxl_PO, TOKEN)
                    self.runRule_AsteriskNone(var1, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
                else:
                    # ChcRule_PO.run('健康评估', None, "r6", Openpyxl_PO, TOKEN)
                    self.runRule_AsteriskRule(var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
            else:
                if var3_rule == None:
                    # 遍历指定结果的记录，如OK
                    # ChcRule_PO.run('健康评估', "ERROR", None, Openpyxl_PO, TOKEN)
                    # ChcRule_PO.run('健康评估', "OK", None, Openpyxl_PO, TOKEN)
                    self.runRule_AsteriskNone(var1, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
                else:
                    # 遍历指定结果及指定测试规则的记录，如ok，r1
                    # ChcRule_PO.run('健康评估', "OK", "r1", Openpyxl_PO, TOKEN)
                    # ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)
                    self.runRule_AsteriskRule(var1, var3_rule, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
        Openpyxl_PO.setAllCellDimensionsHeight(30, varSheetName)
        Openpyxl_PO.open()

    def r1old(self, varSort, varRuleCode, varParam, TOKEN):

        # 家族史，PG_Age001, AGE=55

        log = ""

        if varSort != '家族史':

            # 1, 评估表里自动获取第一条记录的身份证和ID
            l_value = Sqlserver_PO.execQuery("select top(1) ID,ID_CARD from T_ASSESS_INFO")
            # print(l_value)  # [{'ID': 1, 'ID_CARD': '310109195411072438'}]
            varID = l_value[0]['ID']
            varID_CARD = l_value[0]['ID_CARD']
            sql = "select top(1) ID,ID_CARD from T_ASSESS_INFO"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 2，更新规则要求
            Sqlserver_PO.execute("update T_ASSESS_INFO set %s where ID_CARD='%s'" % (varParam, varID_CARD))
            sql = "update T_ASSESS_INFO set " + varParam + " where ID_CARD = '" + str(varID_CARD) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 3，删除评估规则结果表中对应评估ID的记录
            Sqlserver_PO.execute("delete from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE ='%s'" % (varID, varRuleCode))
            sql = "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 4，跑规则
            i_ruleStatus, log2 = self.i_AssessRuleRecord(varID, TOKEN)
            log = log + log2 + "\n"
            if i_ruleStatus == 200:

                # 5，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log
            else:
                return log
        return "warning，不适用r1测试规则，未执行！"

    def r2(self, varIdcard, varRuleCode, varParam, TOKEN):

        # 310101202308070001, GY_YH001001，DIAGNOSIS_CODE='I10'

        log = ""

        # 1，删除评估表中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD='%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 2，删除"诊断疾病表"中对应身份证记录
        Sqlserver_PO.execute("delete from T_HIS_DIAGNOSIS where IDCARD = '%s'" % (varIdcard))
        sql = "delete from T_HIS_DIAGNOSIS where IDCARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 3，诊断疾病表，新增规则记录
        sql = "INSERT INTO T_HIS_DIAGNOSIS(IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_DATE, CREATE_DATE) VALUES (" + str(varIdcard) + " , " + str(varParam) + ",  '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')"
        Sqlserver_PO.execute(sql)
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 4，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 5, 获取评估表id
            l_var = Sqlserver_PO.execQuery("select id from T_ASSESS_INFO where ID_CARD='%s'" % (varIdcard))
            varASSESS_ID = l_var[0]['id']
            sql = "select id from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            sql1 = " \nASSESS_ID = " + str(varASSESS_ID)
            Color_PO.consoleColor("31", "33", sql, "\nASSESS_ID = " + str(varASSESS_ID))
            log = log + sql + sql1 + "\n"

            # 6，删除评估规则结果表中对应评估ID的记录
            Sqlserver_PO.execute("delete from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE ='%s'" % (varASSESS_ID, varRuleCode))
            sql = "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 7，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varASSESS_ID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 8，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varASSESS_ID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

            else:
                return log
        else:
            return log

    def r3(self, varRuleCode, varParam, TOKEN):

        # GY_YH001001，'I10'

        varIdcard = "110101196407281506"

        log = ""

        # 1，删除评估表中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD='%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"


        # 2，更新规则要求
        Sqlserver_PO.execute("update T_HIS_DIAGNOSIS set DIAGNOSIS_CODE=%s where IDCARD='%s'" % (varParam, varIdcard))
        sql = "update T_HIS_DIAGNOSIS set DIAGNOSIS_CODE = '" + str(varParam) + "' where IDCARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 3，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 4, 获取评估表id
            l_var = Sqlserver_PO.execQuery("select id from T_ASSESS_INFO where ID_CARD='%s'" % (varIdcard))
            varASSESS_ID = l_var[0]['id']
            sql = "select id from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            sql1 = " \nASSESS_ID = " + str(varASSESS_ID)
            Color_PO.consoleColor("31", "33", sql, "\nASSESS_ID = " + str(varASSESS_ID))
            log = log + sql + sql1 + "\n"

            # 5，删除评估规则结果表中对应评估ID的记录
            Sqlserver_PO.execute("delete from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE ='%s'" % (varASSESS_ID, varRuleCode))
            sql = "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 6，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varASSESS_ID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 7，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varASSESS_ID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql  + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

            else:
                return log
        else:
            return log

    def r7(self, varRuleCode, varParam1, varParam2, TOKEN):

        # GY_YH001001，"I10","N03"

        varIdcard = "310101202308070004"

        log = ""

        # 1，删除评估表中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD='%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 2，删除"诊断疾病表"中对应身份证记录
        Sqlserver_PO.execute("delete from T_HIS_DIAGNOSIS where IDCARD = '%s'" % (varIdcard))
        sql = "delete from T_HIS_DIAGNOSIS where IDCARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 3，诊断疾病表，新增规则记录
        sql = "INSERT INTO T_HIS_DIAGNOSIS(IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_DATE, CREATE_DATE) VALUES (" + str(varIdcard) + " , " + str(varParam1) + ",  '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')"
        Sqlserver_PO.execute(sql)
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 4，诊断疾病表，新增规则记录
        sql = "INSERT INTO T_HIS_DIAGNOSIS(IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_DATE, CREATE_DATE) VALUES (" + str(varIdcard) + " , " + str(varParam2) + ",  '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')"
        Sqlserver_PO.execute(sql)
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"


        # 5，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 6, 获取评估表id
            l_var = Sqlserver_PO.execQuery("select id from T_ASSESS_INFO where ID_CARD='%s'" % (varIdcard))
            varASSESS_ID = l_var[0]['id']
            sql = "select id from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            sql1 = " \nASSESS_ID = " + str(varASSESS_ID)
            Color_PO.consoleColor("31", "33", sql, "\nASSESS_ID = " + str(varASSESS_ID))
            log = log + sql + sql1 + "\n"

            # 7，删除评估规则结果表中对应评估ID的记录
            Sqlserver_PO.execute("delete from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE ='%s'" % (varASSESS_ID, varRuleCode))
            sql = "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 8，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varASSESS_ID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 9，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varASSESS_ID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

            else:
                return log
        else:
            return log

    def r4(self, varRuleCode, varParam1, varParam2, TOKEN):

        # GY_YH001001，'01','JB002'

        log = ""

        varIdcard = '110101196407281506'

        # 1，删除"评估表"中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD = '%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD ='" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 2，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 3，获取"评估表"中评估id
            l_var = Sqlserver_PO.execQuery("select ID from T_ASSESS_INFO where ID_CARD = '%s' " % (varIdcard))
            # print(l_var[0]['ID'])
            varID = l_var[0]['ID']
            sql = "select ID from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 4，删除"评估既往史表"中对应身份证的记录
            Sqlserver_PO.execute("delete from T_ASSESS_PREVIOUS_HISTORY where IDCARD = '%s'" % (varIdcard))
            sql = "delete from T_ASSESS_PREVIOUS_HISTORY where IDCARD = '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 5，新增一条评估既往史记录
            sql = "INSERT INTO T_ASSESS_PREVIOUS_HISTORY (IDCARD, ASSESS_ID, ASSOCIATION_TYPE, MSG_NAME, OCCUR_DATE, CREATE_DATE, MSG_CODE) VALUES (" + str(varIdcard) + ", " + str(varID) + ", " + str(varParam1) + ", '手术1', '2023-07-01', '2023-07-29 16:31:45.1600000', " + str(varParam2) + ")"
            Sqlserver_PO.execute(sql)
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 6，删除评估规则结果表中对应评估ID的记录
            Sqlserver_PO.execute("delete from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s'" % (varID, varRuleCode))
            sql = "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 7，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 8，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE= '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql  + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

        else:
            return log

    def r5(self, varRuleCode, varParam1, varParam2, TOKEN):

        # GY_YH001001，'I10',HALOPHILIA_CODE=2

        log = ""

        varIdcard = '310101202308070001'

        # 1，删除"评估表"中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD = '%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD ='" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 2，删除 T_HIS_DIAGNOSIS
        Sqlserver_PO.execute("delete from T_HIS_DIAGNOSIS where IDCARD = '%s'" % (varIdcard))
        sql = "delete from T_HIS_DIAGNOSIS where IDCARD = '" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 3，诊断疾病表，新增规则记录
        sql = "INSERT INTO T_HIS_DIAGNOSIS(IDCARD, DIAGNOSIS_CODE, DIAGNOSIS_DATE, CREATE_DATE) VALUES (" + str(
            varIdcard) + " , " + str(varParam1) + ",  '2023-07-29 16:02:19.000', '2023-07-31 09:39:24.3700000')"
        Sqlserver_PO.execute(sql)
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 4，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 5，删除"评估既往史表"中对应身份证的记录
            Sqlserver_PO.execute("update T_ASSESS_INFO set %s where ID_CARD = '%s'" % (str(varParam2), varIdcard))
            sql = "update T_ASSESS_INFO set " + str(varParam2) + " where ID_CARD =  '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 6，获取"评估表"中评估id
            l_var = Sqlserver_PO.execQuery("select ID from T_ASSESS_INFO where ID_CARD = '%s' " % (varIdcard))
            varID = l_var[0]['ID']
            sql = "select ID from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 7，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 8，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE= '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

        else:
            return log

    def r6(self, varRuleCode, varParam1, TOKEN):

        # GY_YH001001，'高血压'

        log = ""

        varIdcard = '110101196407281506'

        # 1，删除"评估表"中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD = '%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD ='" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 2，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 3，获取"评估表"中评估id
            l_var = Sqlserver_PO.execQuery("select ID from T_ASSESS_INFO where ID_CARD = '%s' " % (varIdcard))
            # print(l_var[0]['ID'])
            varID = l_var[0]['ID']
            sql = "select ID from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 4，删除"评估既往史表"中对应身份证的记录
            Sqlserver_PO.execute("delete from T_ASSESS_FAMILY_HISTORY where IDCARD = '%s'" % (varIdcard))
            sql = "delete from T_ASSESS_FAMILY_HISTORY where IDCARD = '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 5，新增一条
            sql = "INSERT INTO T_ASSESS_FAMILY_HISTORY(IDCARD, ASSESS_ID, DISEASE_NAME, FAMILY_TIES, SERVER_DATE, CREATE_DATE) VALUES (" + str(varIdcard) + ", " + str(varID) + ", " + str(varParam1) + ", '父亲', '1900-01-01', '2023-07-29 14:00:38.9466667')"
            Sqlserver_PO.execute(sql)
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 6，删除评估规则结果表中对应评估ID的记录
            Sqlserver_PO.execute("delete from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s'" % (varID, varRuleCode))
            sql = "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 7，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 8，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql  + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

        else:
            return log

    def r8(self, varRuleCode, varParam1, varParam2, TOKEN):

        # GY_YH001001，r8,'现在每天吸'

        log = ""

        varIdcard = '120101199104058611'

        # 1，新增一条
        sql = "INSERT INTO TB_DC_HTN_VISIT (GUID,CARDID, NAME, AGE, EHRNUM, ORGCODE, VISITDATE, VISITWAYCODE , VISITWAYVALUE , OTHERVISIT , VISITDOCNO , VISITDOCNAME , VISITORGCODE , VISITORGNAME , VISTSTATUSCODE , VISITSTATUSVALUE , NEXTVISIDATE , MANAGEGROUP , LOSTVISITCODE , LOSTVISITNAME , OTHERLOSTVISITNAME , LOSTVISITDATE , MOVEPROVINCECODE , MOVEPROVINCEVALUE , MOVECITYCODE , MOVECITYVALUE , MOVEDISTRICTCODE , MOVEDISTRICTVALUE , MOVESTREETCODE , MOVESTREETVALUE , MOVENEIGHBORHOODCODE , MOVENEIGHBORHOODVALUE , MOVEVILLAGEVALUE , MOVEHOUSENUMBER , MOVEORGCODE , MOVEORGNAME , DANGEROUSLEVELCODE , DANGEROUSLEVELNAME , DEATHREASON , SBP , DBP , ISMANUALINPUT , HEIGHT , WEIGHT , TARGETWEIGHT , BMI , WAISTLINE , TARGETBMI , FASTINGBLOODSUGARVALUE , FASTINGBLOODSUGARCODE , FASTINGBLOODSUGARNAME , FASTINGBLOODSUGARSIGN , CHOLESTEROL , HIGHCHOLESTEROL , LOWCHOLESTEROL , TRIGLYCERIDES , UACR , BCTV , BUATV , HOMOCYSTEINEDETECTION , BLOODPOTASSIUM , BLOODSODIUM , BLOODLIPIDS , URICACID , CREATININE , HEMOGLOBIN , HEMAMEBA , PLATELET , URINEPROTEIN , URINESUGAR , GLYCOSYLATEDHEMOGLOBIN , SERUMCPROTEIN , URINEPROTEINQUANTITY , ECG , ECHOCARDIOGRAM , CAROTIDULTRASOUND , CHESTXRAY , PULSEWAVE , REGULARACTIVITYSIGN , REGULARACTIVITIESTYPES , HASPAPERCARD , DRUGCOMPLIANCECODE , DRUGCOMPLIANCENAME , BPWAYCODE , BPWAYNAME , HEARTRATE , SMOKINGVOLUME , DRINKINGVOLUME , POSITIVESIGNS , SMOKINGSTATUSCODE , SMOKINGSTATUSNAME , TARGETSMOKE , QUITSMOKING , DRINKINGFREQUENCYCODE , DRINKINGFREQUENCYNAME , TARGETDRINK , TARGETSALTUPTAKESTATUS , REASONABLEDIETEVALUATION , PSYCHOLOGYEVALUATION , COMPLIANCEEVALUATION , SALTUPTAKESTATUS , SALTUPTAKESTATUSNAME , PSYCHOLOGYSTATUS , PSYCHOLOGYSTATUSNAME , COMPLIANCESTATUS , COMPLIANCESTATUSNAME , SPORTFREQUENCE , SPORTTIME , EXERCISEDESCRIPTION , EXERCISEFREQUENCYCODE , EXERCISEFREQUENCYNAME , TARGETSPORTFREQUENCYCODE , TARGETSPORTFREQUENCYNAME , TARGETSPORTTIMES , TARGETSTAPLEFOOD , SYMPTOMCODE , SYMPTOMVALUE , SYMPTOMOTHER , ISUSEDRUG , NOUSEDRUGREASONCODE , NOUSEDRUGREASONVALUE , NOUSEDRUGSIDEEFFECTS , OTHERNOUSEDRUGREASON , NOUSEDRUGLAW , NOUSEDRUGLAWREASON , LAWSIDEEFFECTSFLAG , LAWSIDEEFFECTS , OTHERLAWREASON , TREATMENTMEASURES , CLINICALINFO , AUXILIARYCHECK , INTERVENENUM , BEFOREINTERVENEDATE , ISINTERVENE , SYNDROME , INTERVENEMEASURES , MEASURESCONTENT , OTHERINTERVENEMEASURES , OTHERMEASURESCONTENT , PROPOSAL , ACCEPTABILITY , ISACCEPTHEALTHEDU , HEALTHEDUTYPE , VISITTYPE , REFERRALREASON , REFERRALORGDEPT , SYNSTATUS , EMPIGUID , ISGOVERNANCE ) VALUES (newid(),'001', NULL, NULL, NULL, '0000001', '2023-08-01 10:51:23.000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '140', '90', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, " + str(varParam1) + ", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '5001', '0')"
        Sqlserver_PO.execute(sql)
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 2，删除"评估表"中对应身份证的记录
        Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD = '%s'" % (varIdcard))
        sql = "delete from T_ASSESS_INFO where ID_CARD ='" + str(varIdcard) + "'"
        Color_PO.consoleColor("31", "33", sql, "")
        log = log + sql + "\n"

        # 3，新增评估
        i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        log = log + log1 + "\n"
        sleep(2)
        if i_i_newAssessResult == 200:

            # 4，获取"评估表"中评估id
            l_var = Sqlserver_PO.execQuery("select ID from T_ASSESS_INFO where ID_CARD = '%s' " % (varIdcard))
            # print(l_var[0]['ID'])
            varID = l_var[0]['ID']
            sql = "select ID from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
            Color_PO.consoleColor("31", "33", sql, "")
            log = log + sql + "\n"

            # 5，跑规则
            i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varID, TOKEN)
            log = log + log2 + "\n"
            if i_i_AssessRuleRecordStatus == 200:

                # 6，
                Sqlserver_PO.execute("update T_ASSESS_INFO set %s where ID_CARD = '%s'" % (varParam2, varIdcard))
                sql = "update T_ASSESS_INFO set " + str(varParam2) + " where ID_CARD ='" + str(varIdcard) + "'"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql + "\n"

                # 7，检查"评估规则结果表"
                l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varID, varRuleCode))
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                log = log + sql + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

        else:
            return log




    def GW123(self, d, Openpyxl_PO):

        log = ""

        # print(varRuleCode)  # GW_JB004
        print(d)

        # 1,获取身份证
        d_CodeIdcard = self.getDiseaseIdcard(Openpyxl_PO)
        varIdcard = None
        for k, v in d_CodeIdcard.items():
            if k == d['diseaseRuleCode']:
                varIdcard = v
                break
        print(varIdcard)  # '410101202308070004'

        # 2，遍历所有列得到列值
        l_all = Openpyxl_PO.getColValue("GW")
        # print(l_all)

        i_newAssessStatus = 0
        for i in range(len(l_all)):
            if d['diseaseRuleCode'] == l_all[i][0] :
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    print(command)

                    l_var = Openpyxl_PO.getOneRowValue(0, "GW")
                    for k in range(len(l_var)):
                        if l_var[k] == varRuleCode:
                            varTitleCol = k + 1
                    # print(varTitleCol)


                    command = str(command).replace("{身份证}", varIdcard)

                    varID = Openpyxl_PO.getCellValue(1, 66, "GW")
                    varQTY = Openpyxl_PO.getCellValue(2, 67, "GW")

                    if "varID=" in varID:
                        varID = varID.split("varID=")[1].split(")")[0]
                        print(varID)
                        command = str(command).replace("{varID}", varID)
                    elif "varQTY" in varQTY:
                        varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                        print(varQTY)
                        command = str(command).replace("{varQTY}", varQTY)

                    Color_PO.consoleColor("31", "33", command, "")
                    a = eval(command)
                    print(a)
                    if a != None:
                        if isinstance(a, list):
                            if isinstance(a[0], dict):
                                print(a[0])
                                if "ID" in a[0]:
                                    varID = a[0]['ID']
                                    # print(varID)
                                    Openpyxl_PO.setCellValue(1, 66, "varID=" + str(varID), "GW")
                                if "QTY" in a[0]:
                                    varQTY = a[0]['QTY']
                                    Openpyxl_PO.setCellValue(2, 67, "varQTY=" + str(varQTY), "GW")





                break


        # sys.exit(0)
        #
        # varIdcard = '120101199104058611'
        #
        # # 1，新增一条
        # sql = "INSERT INTO TB_DC_HTN_VISIT (GUID,CARDID, NAME, AGE, EHRNUM, ORGCODE, VISITDATE, VISITWAYCODE , VISITWAYVALUE , OTHERVISIT , VISITDOCNO , VISITDOCNAME , VISITORGCODE , VISITORGNAME , VISTSTATUSCODE , VISITSTATUSVALUE , NEXTVISIDATE , MANAGEGROUP , LOSTVISITCODE , LOSTVISITNAME , OTHERLOSTVISITNAME , LOSTVISITDATE , MOVEPROVINCECODE , MOVEPROVINCEVALUE , MOVECITYCODE , MOVECITYVALUE , MOVEDISTRICTCODE , MOVEDISTRICTVALUE , MOVESTREETCODE , MOVESTREETVALUE , MOVENEIGHBORHOODCODE , MOVENEIGHBORHOODVALUE , MOVEVILLAGEVALUE , MOVEHOUSENUMBER , MOVEORGCODE , MOVEORGNAME , DANGEROUSLEVELCODE , DANGEROUSLEVELNAME , DEATHREASON , SBP , DBP , ISMANUALINPUT , HEIGHT , WEIGHT , TARGETWEIGHT , BMI , WAISTLINE , TARGETBMI , FASTINGBLOODSUGARVALUE , FASTINGBLOODSUGARCODE , FASTINGBLOODSUGARNAME , FASTINGBLOODSUGARSIGN , CHOLESTEROL , HIGHCHOLESTEROL , LOWCHOLESTEROL , TRIGLYCERIDES , UACR , BCTV , BUATV , HOMOCYSTEINEDETECTION , BLOODPOTASSIUM , BLOODSODIUM , BLOODLIPIDS , URICACID , CREATININE , HEMOGLOBIN , HEMAMEBA , PLATELET , URINEPROTEIN , URINESUGAR , GLYCOSYLATEDHEMOGLOBIN , SERUMCPROTEIN , URINEPROTEINQUANTITY , ECG , ECHOCARDIOGRAM , CAROTIDULTRASOUND , CHESTXRAY , PULSEWAVE , REGULARACTIVITYSIGN , REGULARACTIVITIESTYPES , HASPAPERCARD , DRUGCOMPLIANCECODE , DRUGCOMPLIANCENAME , BPWAYCODE , BPWAYNAME , HEARTRATE , SMOKINGVOLUME , DRINKINGVOLUME , POSITIVESIGNS , SMOKINGSTATUSCODE , SMOKINGSTATUSNAME , TARGETSMOKE , QUITSMOKING , DRINKINGFREQUENCYCODE , DRINKINGFREQUENCYNAME , TARGETDRINK , TARGETSALTUPTAKESTATUS , REASONABLEDIETEVALUATION , PSYCHOLOGYEVALUATION , COMPLIANCEEVALUATION , SALTUPTAKESTATUS , SALTUPTAKESTATUSNAME , PSYCHOLOGYSTATUS , PSYCHOLOGYSTATUSNAME , COMPLIANCESTATUS , COMPLIANCESTATUSNAME , SPORTFREQUENCE , SPORTTIME , EXERCISEDESCRIPTION , EXERCISEFREQUENCYCODE , EXERCISEFREQUENCYNAME , TARGETSPORTFREQUENCYCODE , TARGETSPORTFREQUENCYNAME , TARGETSPORTTIMES , TARGETSTAPLEFOOD , SYMPTOMCODE , SYMPTOMVALUE , SYMPTOMOTHER , ISUSEDRUG , NOUSEDRUGREASONCODE , NOUSEDRUGREASONVALUE , NOUSEDRUGSIDEEFFECTS , OTHERNOUSEDRUGREASON , NOUSEDRUGLAW , NOUSEDRUGLAWREASON , LAWSIDEEFFECTSFLAG , LAWSIDEEFFECTS , OTHERLAWREASON , TREATMENTMEASURES , CLINICALINFO , AUXILIARYCHECK , INTERVENENUM , BEFOREINTERVENEDATE , ISINTERVENE , SYNDROME , INTERVENEMEASURES , MEASURESCONTENT , OTHERINTERVENEMEASURES , OTHERMEASURESCONTENT , PROPOSAL , ACCEPTABILITY , ISACCEPTHEALTHEDU , HEALTHEDUTYPE , VISITTYPE , REFERRALREASON , REFERRALORGDEPT , SYNSTATUS , EMPIGUID , ISGOVERNANCE ) VALUES (newid(),'001', NULL, NULL, NULL, '0000001', '2023-08-01 10:51:23.000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '140', '90', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, " + str(varParam1) + ", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '5001', '0')"
        # Sqlserver_PO.execute(sql)
        # Color_PO.consoleColor("31", "33", sql, "")
        # log = log + sql + "\n"
        #
        # # 2，删除"评估表"中对应身份证的记录
        # Sqlserver_PO.execute("delete from T_ASSESS_INFO where ID_CARD = '%s'" % (varIdcard))
        # sql = "delete from T_ASSESS_INFO where ID_CARD ='" + str(varIdcard) + "'"
        # Color_PO.consoleColor("31", "33", sql, "")
        # log = log + sql + "\n"
        #
        # # 3，新增评估
        # i_i_newAssessResult, log1 = self.i_newAssess(varIdcard, TOKEN)
        # log = log + log1 + "\n"
        # sleep(2)
        # if i_i_newAssessResult == 200:
        #
        #     # 4，获取"评估表"中评估id
        #     l_var = Sqlserver_PO.execQuery("select ID from T_ASSESS_INFO where ID_CARD = '%s' " % (varIdcard))
        #     # print(l_var[0]['ID'])
        #     varID = l_var[0]['ID']
        #     sql = "select ID from T_ASSESS_INFO where ID_CARD = '" + str(varIdcard) + "'"
        #     Color_PO.consoleColor("31", "33", sql, "")
        #     log = log + sql + "\n"
        #
        #     # 5，跑规则
        #     i_i_AssessRuleRecordStatus, log2 = self.i_AssessRuleRecord(varID, TOKEN)
        #     log = log + log2 + "\n"
        #     if i_i_AssessRuleRecordStatus == 200:
        #
        #         # 6，
        #         Sqlserver_PO.execute("update T_ASSESS_INFO set %s where ID_CARD = '%s'" % (varParam2, varIdcard))
        #         sql = "update T_ASSESS_INFO set " + str(varParam2) + " where ID_CARD ='" + str(varIdcard) + "'"
        #         Color_PO.consoleColor("31", "33", sql, "")
        #         log = log + sql + "\n"
        #
        #         # 7，检查"评估规则结果表"
        #         l_result = Sqlserver_PO.execQuery("select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = %s and RULE_CODE = '%s' " % (varID, varRuleCode))
        #         sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "' => " + str(l_result[0]['NO']) + "条"
        #         Color_PO.consoleColor("31", "33", sql, "")
        #         log = log + sql + "\n"
        #         if l_result[0]['NO'] == 1:
        #             return 1
        #         else:
        #             return log
        #
        # else:
        #     return log


    def r1(self, d, Openpyxl_PO, TOKEN):

        # {'result': None, 'testRuleName': 'r1', 'testRuleParam': 'AGE=55', 'ruleCode': 'PG_Age001'}
        # {'result': None, 'testRuleName': 'r2', 'testRuleParam': "'I10'", 'ruleCode': 'GY_YH001001', 'diseaseRuleCode': 'YH_JB001', 'varIdcard': '310101202308070001'}

        log = ""
        varQTY = ""

        # 1，遍历所有列得到列值
        l_all = Openpyxl_PO.getColValue("testRule")
        # print(l_all)

        i_newAssessStatus = 0
        for i in range(len(l_all)):
            if d['testRuleName'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:
                        # print(command)

                        if 'varIdcard' in d:
                            command = str(command).replace("{身份证}", d['varIdcard'])
                        if 'testRuleParam1' in d:
                            command = str(command).replace("{测试规则参数1}", d['testRuleParam1'])
                            command = str(command).replace("{测试规则参数2}", d['testRuleParam2'])
                        if 'testRuleParam' in d:
                            command = str(command).replace("{测试规则参数}", d['testRuleParam'])
                        if 'ruleCode' in d:
                            # print(d)
                            command = str(command).replace("{规则编码}", d['ruleCode'])
                        if "{随机数}" in command:
                            command = str(command).replace("{随机数}", Data_PO.getPhone())

                        varID = Openpyxl_PO.getCellValue(21, 1, "testRule")
                        varIdcard = Openpyxl_PO.getCellValue(22, 1, "testRule")
                        varQTY = Openpyxl_PO.getCellValue(23, 1, "testRule")
                        varRunRule = Openpyxl_PO.getCellValue(24, 1, "testRule")
                        varNewAssess = Openpyxl_PO.getCellValue(25, 1, "testRule")
                        varGUID = Openpyxl_PO.getCellValue(26, 1, "testRule")

                        if varID != None:
                            if "varID=" in varID:
                                varID = varID.split("varID=")[1].split(")")[0]
                                # print(varID)
                                command = str(command).replace("{varID}", varID)
                        if varIdcard != None:
                            if "varIdcard" in varIdcard:
                                varIdcard = varIdcard.split("varIdcard=")[1].split(")")[0]
                                # print(varIdcard)
                                command = str(command).replace("{varIdcard}", varIdcard)
                        if varQTY != None:
                            if "varQTY" in varQTY:
                                varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                                # print(varQTY)
                                command = str(command).replace("{varQTY}", varQTY)
                        if varRunRule != None:
                            # print(type(varRunRule))
                            # varRunRule = varRunRule.split("varRunRule=")[1].split(")")[0]
                            log = log + "\n" + varRunRule
                        if varNewAssess != None:
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            log = log + "\n" + varNewAssess
                        if varGUID != None:
                            if "varGUID" in varGUID:
                                varGUID = varGUID.split("varGUID=")[1].split(")")[0]
                                # print(varGUID)
                                command = str(command).replace("{varGUID}", varGUID)
                        Color_PO.consoleColor("31", "33", command, "")

                        # 步骤日志
                        log = log + "\n" + command
                        a = eval(command)
                        # print(a)
                        if a != None:
                            if isinstance(a, list):
                                if isinstance(a[0], dict):
                                    # print(a[0])
                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        # print(varID)
                                        Openpyxl_PO.setCellValue(21, 1, "varID=" + str(varID), "testRule")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        # print(varIdcard)
                                        Openpyxl_PO.setCellValue(22, 1, "varIdcard=" + str(varIdcard), "testRule")
                                    if "QTY" in a[0]:
                                        varQTY = a[0]['QTY']
                                        # print(varQTY)
                                        Openpyxl_PO.setCellValue(23, 1, "varQTY=" + str(varQTY), "testRule")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        # print(varGUID)
                                        Openpyxl_PO.setCellValue(26, 1, "varGUID=" + str(varGUID), "testRule")
                            if isinstance(a, tuple):
                                if "跑规则" in a[0]:
                                    varRunRule = a[1]
                                    Openpyxl_PO.setCellValue(24, 1, "varRunRule=" + str(varRunRule), "testRule")
                                if "新增评估" in a[0]:
                                    varNewAssess = a[1]
                                    Openpyxl_PO.setCellValue(25, 1, "varNewAssess=" + str(varNewAssess), "testRule")


                    else:
                        break
        Openpyxl_PO.setCellValue(21, 1, "", "testRule")
        Openpyxl_PO.setCellValue(22, 1, "", "testRule")
        Openpyxl_PO.setCellValue(23, 1, "", "testRule")
        Openpyxl_PO.setCellValue(24, 1, "", "testRule")
        Openpyxl_PO.setCellValue(25, 1, "", "testRule")
        Openpyxl_PO.setCellValue(26, 1, "", "testRule")


        return varQTY, log


    def gw(self, d, Openpyxl_PO, TOKEN):

        # self.outResultGW(varQty, varLog, k, varSheetName, Openpyxl_PO)

        # {'result': None, 'diseaseRuleCode': 'GW_JB004',
        # 'ruleCode': "('GW_JB004','PG_AGE003','PG_JWS001','PG_JWS007','PG_JWS012','PG_JZS004','PG_JZS005','PG_JYZB006','PG_JYZB007','PG_JYZB008','PG_JYZB009')"}

        # print(d)

        # {'GW_JB004':1234}   // 1234是GW_JB004的varID

        d_all = {}
        log = ""
        varQTY = ""

        # 1，遍历所有列得到列值
        l_all = Openpyxl_PO.getColValue("GW")
        # print(l_all)


        i_newAssessStatus = 0
        for i in range(len(l_all)):
            if d['diseaseRuleCode'] == l_all[i][0]:
                for j in range(1, len(l_all[i])):
                    command = l_all[i][j]
                    if command != None:

                        print(d_all)
                        # print(command)

                        if command == "exit":
                            Openpyxl_PO.setCellValue(21, 1, "", "testRule")
                            Openpyxl_PO.setCellValue(22, 1, "", "testRule")
                            Openpyxl_PO.setCellValue(23, 1, "", "testRule")
                            Openpyxl_PO.setCellValue(24, 1, "", "testRule")
                            Openpyxl_PO.setCellValue(25, 1, "", "testRule")
                            Openpyxl_PO.setCellValue(26, 1, "", "testRule")
                            Openpyxl_PO.setCellValue(27, 1, "", "testRule")
                            return d_all, log

                        if 'varIdcard' in d:
                            command = str(command).replace("{身份证}", d['varIdcard'])
                        # if 'testRuleParam1' in d:
                        #     command = str(command).replace("{测试规则参数1}", d['testRuleParam1'])
                        #     command = str(command).replace("{测试规则参数2}", d['testRuleParam2'])
                        # if 'testRuleParam' in d:
                        #     command = str(command).replace("{测试规则参数}", d['testRuleParam'])

                        if 'ruleCode' in d:
                            command = str(command).replace("{规则编码}", d['ruleCode'])

                        command = str(command).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

                        # command = str(command).replace("{随机数}", Data_PO.getPhone())

                        varID = Openpyxl_PO.getCellValue(21, 1, "testRule")
                        varIdcard = Openpyxl_PO.getCellValue(22, 1, "testRule")
                        # varQTY = Openpyxl_PO.getCellValue(23, 1, "testRule")
                        varRunRule = Openpyxl_PO.getCellValue(24, 1, "testRule")
                        varNewAssess = Openpyxl_PO.getCellValue(25, 1, "testRule")
                        varGUID = Openpyxl_PO.getCellValue(26, 1, "testRule")
                        # varQTY0 = Openpyxl_PO.getCellValue(27, 1, "testRule")


                        if varID != None:
                            if "varID=" in varID:
                                varID = varID.split("varID=")[1].split(")")[0]
                                # print(varID)
                                command = str(command).replace("{varID}", varID)
                        if varIdcard != None:
                            if "varIdcard" in varIdcard:
                                varIdcard = varIdcard.split("varIdcard=")[1].split(")")[0]
                                # print(varIdcard)
                                command = str(command).replace("{varIdcard}", varIdcard)
                        # if varQTY != None:
                        #     if "varQTY" in varQTY:
                        #         varQTY = varQTY.split("varQTY=")[1].split(")")[0]
                        #         # print(varQTY)
                        #         command = str(command).replace("{varQTY}", varQTY)
                        if varRunRule != None:
                            # print(type(varRunRule))
                            # varRunRule = varRunRule.split("varRunRule=")[1].split(")")[0]
                            log = log + "\n" + varRunRule
                        if varNewAssess != None:
                            # print(type(varNewAssess))
                            # varNewAssess = varNewAssess.split("varNewAssess=")[1].split(")")[0]
                            log = log + "\n" + varNewAssess
                        if varGUID != None:
                            if "varGUID" in varGUID:
                                varGUID = varGUID.split("varGUID=")[1].split(")")[0]
                                # print(varGUID)
                                command = str(command).replace("{varGUID}", varGUID)
                        # if varQTY0 != None:
                        #     if "varQTY0" in varQTY0:
                        #         varQTY0 = varQTY0.split("varQTY0=")[1].split(")")[0]
                        #         print(varQTY0)
                        #         command = str(command).replace("{varQTY0}", varQTY0)
                        Color_PO.consoleColor("31", "33", command, "")

                        # 步骤日志
                        log = log + "\n" + command
                        a = eval(command)
                        # print(a)
                        if a != None:
                            if isinstance(a, list):
                                if isinstance(a[0], dict):
                                    # print(a[0])
                                    if "ID" in a[0]:
                                        varID = a[0]['ID']
                                        # print(varID)
                                        Openpyxl_PO.setCellValue(21, 1, "varID=" + str(varID), "testRule")
                                        Openpyxl_PO.setCellValue(33, 1, str(varID), "testRule")
                                    if "ID_CARD" in a[0]:
                                        varIdcard = a[0]['ID_CARD']
                                        # print(varIdcard)
                                        Openpyxl_PO.setCellValue(22, 1, "varIdcard=" + str(varIdcard), "testRule")
                                    if "QTY" in a[0]:
                                        varQTY = a[0]['QTY']
                                        # print(varQTY)
                                        Openpyxl_PO.setCellValue(23, 1, "varQTY=" + str(varQTY), "testRule")
                                    if "GUID" in a[0]:
                                        varGUID = a[0]['GUID']
                                        # print(varGUID)
                                        Openpyxl_PO.setCellValue(26, 1, "varGUID=" + str(varGUID), "testRule")
                                    if "QTY0" in a[0]:
                                        # varQTY0 = a[0]['QTY0']
                                        d_all['QTY0'] = str(a[0]['QTY0'])
                                        # print(varQTY0)
                                        # Openpyxl_PO.setCellValue(27, 1, "varQTY0=" + str(varQTY0), "testRule")

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
                                        if "PG_Age004" in a[0]: d_all['PG_Age004'] = str(a[0]['PG_Age004'])
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

                            if isinstance(a, tuple):
                                if "跑规则" in a[0]:
                                    varRunRule = a[1]
                                    Openpyxl_PO.setCellValue(24, 1, "varRunRule=" + str(varRunRule), "testRule")
                                if "新增评估" in a[0]:
                                    varNewAssess = a[1]
                                    Openpyxl_PO.setCellValue(25, 1, "varNewAssess=" + str(varNewAssess), "testRule")




                    else:
                        break
        Openpyxl_PO.setCellValue(21, 1, "", "testRule")
        Openpyxl_PO.setCellValue(22, 1, "", "testRule")
        Openpyxl_PO.setCellValue(23, 1, "", "testRule")
        Openpyxl_PO.setCellValue(24, 1, "", "testRule")
        Openpyxl_PO.setCellValue(25, 1, "", "testRule")
        Openpyxl_PO.setCellValue(26, 1, "", "testRule")
        Openpyxl_PO.setCellValue(27, 1, "", "testRule")

        # self.outResultGW(varQty, log, k, varSheetName, Openpyxl_PO)

        log = log + "\n" + str(d_all)

        return d_all, log

        # {'QTY0':"0", "PG_AGE003":"1", "PG_JWS001":"1"}

