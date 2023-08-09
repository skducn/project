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
            log = str(d_r) + " 跑规则, http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var)
            print(log)
            return (d_r['code'], log)
        else:
            log = "[" + str(d_r['code']) + "] 跑规则, http://192.168.0.243:8011/rules/tAssessRuleRecord/testExecuteRule/" + str(var)
            print(log)
            return (d_r['code'], log)

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
        if d_r['code'] != 200:
            log = str(d_r) + "新增评估, http://192.168.0.243:8011/server/qyyh/addAssess/" + str(varIdcard)
            print(log)
            return (d_r['code'], log)
        else:
            log = "[" + str(d_r['code']) + "] 新增评估, http://192.168.0.243:8011/server/qyyh/addAssess/" + str(varIdcard)
            print(log)
            return (d_r['code'], log)



    def outResult(self, l_result, k, varSheetName, Openpyxl_PO):

        if l_result == 1:
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheetName)
            Color_PO.consoleColor("31", "36", str(k) + " => OK\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheetName)  # 更新测试时间
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheetName)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheetName)
            Color_PO.consoleColor("31", "31", str(k) + " => ERROR\n", "")
            Openpyxl_PO.setCellValue(k, 2, l_result, varSheetName)
            Openpyxl_PO.setCellFont(k, "A", color="ff0000", varSheet=varSheetName)
            Openpyxl_PO.setCellFont(k, "B", color="ff0000", varSheet=varSheetName)

    def runRule_result(self, varResult, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # 3，遍历每条规则
        for k, v in d_paramCode.items():

            if varResult == v[0] and v[1] != None:

                varRuleCode = v[2]  # GY_YH001001
                try:
                    l_v1 = Str_PO.str2list(v[1])
                except:
                    # l_v1 = []
                    print("error, 测试规则 " + str(v[1]) + " 格式错误！")

                if l_v1[0] == "r1":
                    # 实例：r1,DIAGNOSIS_CODE='I10'
                    varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
                    varParam = varParam.replace(".and.", ',')
                    print(str(k) + " => (" + l_v1[0] + ")")  # r2
                    varSort = v[3]  # 家族史
                    l_result = self.r1(varSort, varRuleCode, varParam, TOKEN)  # 家族史, PG_JZS001, IAGNOSIS_CODE='I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r2":
                    # 实例： r2, 'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")  # r2
                    varIdcard = None
                    if varSheetName == "健康干预":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    elif varSheetName == "疾病评估规则（已患和高风险）":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    l_result = self.r2(varIdcard, varRuleCode, varParam, TOKEN)  # {身份证自动匹配} , GY_YH001001, 'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r7":
                    # 实例："r7,"I10","N03"
                    varParam1 = l_v1[1]  # 'I10'
                    varParam2 = l_v1[2]  # "N03"
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r7(varRuleCode, varParam1, varParam2, TOKEN)  # GY_YH001001，"I10","N03"
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r3":
                    # 实例："r3,'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r3(varRuleCode, varParam, TOKEN)  # GY_YH001001，'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r4":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    varParam2 = l_v1[2]  # job002
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r4(varRuleCode, varParam1, varParam2, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r6":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r6(varRuleCode, varParam1, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)



    def runRule_resultNull(self, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # 3，遍历每条规则
        for k, v in d_paramCode.items():
            # print(v)
            if v[0] == None and v[1] != None:

                varRuleCode = v[2]  # GY_YH001001
                try:
                    l_v1 = Str_PO.str2list(v[1])
                except:
                    # l_v1 = []
                    print("error, 测试规则 " + str(v[1]) + " 格式错误！")

                if l_v1[0] == "r1":
                    # 实例：r1,DIAGNOSIS_CODE='I10'
                    varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
                    varParam = varParam.replace(".and.", ',')
                    print(str(k) + " => (" + l_v1[0] + ")")  # r2
                    varSort = v[3]  # 家族史
                    l_result = self.r1(varSort, varRuleCode, varParam, TOKEN)  # 家族史, PG_JZS001, IAGNOSIS_CODE='I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r2":
                    # 实例： r2, 'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")  # r2
                    varIdcard = None
                    if varSheetName == "健康干预":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    elif varSheetName == "疾病评估规则（已患和高风险）":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    l_result = self.r2(varIdcard, varRuleCode, varParam, TOKEN)  # {身份证自动匹配} , GY_YH001001, 'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r7":
                    # 实例："r7,"I10","N03"
                    varParam1 = l_v1[1]  # 'I10'
                    varParam2 = l_v1[2]  # "N03"
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r7(varRuleCode, varParam1, varParam2, TOKEN)  # GY_YH001001，"I10","N03"
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r3":
                    # 实例："r3,'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r3(varRuleCode, varParam, TOKEN)  # GY_YH001001，'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r4":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    varParam2 = l_v1[2]  # job002
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r4(varRuleCode, varParam1, varParam2, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r6":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r6(varRuleCode, varParam1, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)



    def runRule_param(self, varRuleParam, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # 遍历每条规则
        for k, v in d_paramCode.items():

                varRuleCode = v[2]  # GY_YH001001
                try:
                    l_v1 = Str_PO.str2list(v[1])
                except:
                    # l_v1 = []
                    print("error, 测试规则 " + str(v[1]) + " 格式错误！")

                # ruleQty = len(varRuleParam.split(","))
                # if ruleQty == 1:


                if l_v1[0] == "r1" and varRuleParam == "r1":
                    # 实例：r1,DIAGNOSIS_CODE='I10'
                    varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
                    varParam = varParam.replace(".and.", ',')
                    print(str(k) + " => (" + l_v1[0] + ")")
                    varSort = v[3]  # 家族史
                    l_result = self.r1(varSort, varRuleCode, varParam, TOKEN)  # 家族史, PG_JZS001, IAGNOSIS_CODE='I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r2" and varRuleParam == "r2":
                    # 实例： r2, 'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")  # r2
                    varIdcard = None
                    if varSheetName == "健康干预":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    elif varSheetName == "疾病评估规则（已患和高风险）":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    l_result = self.r2(varIdcard, varRuleCode, varParam, TOKEN)  # {身份证自动匹配} , GY_YH001001, 'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r7" and varRuleParam == "r7":
                    # 实例："r7,"I10","N03"
                    varParam1 = l_v1[1]  # 'I10'
                    varParam2 = l_v1[2]  # "N03"
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r7(varRuleCode, varParam1, varParam2, TOKEN)  # GY_YH001001，"I10","N03"
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r3" and varRuleParam == "r3":
                    # 实例："r3,'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r3(varRuleCode, varParam, TOKEN)  # GY_YH001001，'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r4" and varRuleParam == "r4":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    varParam2 = l_v1[2]  # job002
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r4(varRuleCode, varParam1, varParam2, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

                elif l_v1[0] == "r6" and varRuleParam == "r6":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r6(varRuleCode, varParam1, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)





    def runRule_Resultparam(self, varResult, varRuleParam, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # 遍历每条规则
        for k, v in d_paramCode.items():

            if varResult == v[0] and v[1] != None:
                varRuleCode = v[2]  # GY_YH001001
                try:
                    l_v1 = Str_PO.str2list(v[1])
                except:
                    # l_v1 = []
                    print("error, 测试规则 " + str(v[1]) + " 格式错误！")

                # ruleQty = len(varRuleParam.split(","))
                # if ruleQty == 1:


                if l_v1[0] == "r1" and varRuleParam == "r1":
                    # 实例：r1,DIAGNOSIS_CODE='I10'
                    varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
                    varParam = varParam.replace(".and.", ',')
                    print(str(k) + " => (" + l_v1[0] + ")")
                    varSort = v[3]  # 家族史
                    l_result = self.r1(varSort, varRuleCode, varParam, TOKEN)  # 家族史, PG_JZS001, IAGNOSIS_CODE='I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)
                elif l_v1[0] == "r2" and varRuleParam == "r2":
                    # 实例： r2, 'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")  # r2
                    varIdcard = None
                    if varSheetName == "健康干预":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    elif varSheetName == "疾病评估规则（已患和高风险）":
                        diseaseCode = v[3]  # YH_JB001
                        # 获取疾病身份证表对应code：idcard
                        d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                        for k1, v1 in d_code_Idcard.items():
                            if k1 == diseaseCode:
                                varIdcard = v1
                                break
                    l_result = self.r2(varIdcard, varRuleCode, varParam, TOKEN)  # {身份证自动匹配} , GY_YH001001, 'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)
                elif l_v1[0] == "r7" and varRuleParam == "r7":
                    # 实例："r7,"I10","N03"
                    varParam1 = l_v1[1]  # 'I10'
                    varParam2 = l_v1[2]  # "N03"
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r7(varRuleCode, varParam1, varParam2, TOKEN)  # GY_YH001001，"I10","N03"
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)
                elif l_v1[0] == "r3" and varRuleParam == "r3":
                    # 实例："r3,'I10'
                    varParam = l_v1[1]  # 'I10'
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r3(varRuleCode, varParam, TOKEN)  # GY_YH001001，'I10'
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)
                elif l_v1[0] == "r4" and varRuleParam == "r4":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    varParam2 = l_v1[2]  # job002
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r4(varRuleCode, varParam1, varParam2, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)
                elif l_v1[0] == "r6" and varRuleParam == "r6":
                    # 分解 "r4,  '01','JB002'
                    varParam1 = l_v1[1]  # 01
                    print(str(k) + " => (" + l_v1[0] + ")")
                    l_result = self.r6(varRuleCode, varParam1, TOKEN)
                    self.outResult(l_result, k, varSheetName, Openpyxl_PO)

    def runRule(self, varSheetName, d_paramCode, Openpyxl_PO, TOKEN):

        # 3，遍历每条规则
        for k, v in d_paramCode.items():
            varRuleCode = v[2]  # GY_YH001001
            try:
                l_v1 = Str_PO.str2list(v[1])
            except:
                # l_v1 = []
                print("error, 测试规则 " + str(v[1]) + " 格式错误！")

            if l_v1[0] == "r1":
                # 实例：r1,DIAGNOSIS_CODE='I10'
                varParam = l_v1[1]  # IAGNOSIS_CODE='I10'
                varParam = varParam.replace(".and.", ',')
                print(str(k) + " => (" + l_v1[0] + ")")  # r2
                varSort = v[3]  # 家族史
                l_result = self.r1(varSort, varRuleCode, varParam, TOKEN)  # 家族史, PG_JZS001, IAGNOSIS_CODE='I10'
                self.outResult(l_result, k, varSheetName, Openpyxl_PO)

            elif l_v1[0] == "r2":
                # 实例： r2, 'I10'
                varParam = l_v1[1]  # 'I10'
                print(str(k) + " => (" + l_v1[0] + ")")  # r2
                varIdcard = None
                if varSheetName == "健康干预":
                    diseaseCode = v[3]  # YH_JB001
                    # 获取疾病身份证表对应code：idcard
                    d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                    for k1, v1 in d_code_Idcard.items():
                        if k1 == diseaseCode:
                            varIdcard = v1
                            break
                elif varSheetName == "疾病评估规则（已患和高风险）":
                    diseaseCode = v[3]  # YH_JB001
                    # 获取疾病身份证表对应code：idcard
                    d_code_Idcard = self.getDiseaseIdcard(Openpyxl_PO)
                    for k1, v1 in d_code_Idcard.items():
                        if k1 == diseaseCode:
                            varIdcard = v1
                            break
                l_result = self.r2(varIdcard, varRuleCode, varParam, TOKEN)  # {身份证自动匹配} , GY_YH001001, 'I10'
                self.outResult(l_result, k, varSheetName, Openpyxl_PO)

            elif l_v1[0] == "r7":
                # 实例："r7,"I10","N03"
                varParam1 = l_v1[1]  # 'I10'
                varParam2 = l_v1[2]  # "N03"
                print(str(k) + " => (" + l_v1[0] + ")")
                l_result = self.r7(varRuleCode, varParam1, varParam2, TOKEN)  # GY_YH001001，"I10","N03"
                self.outResult(l_result, k, varSheetName, Openpyxl_PO)

            elif l_v1[0] == "r3":
                # 实例："r3,'I10'
                varParam = l_v1[1]  # 'I10'
                print(str(k) + " => (" + l_v1[0] + ")")
                l_result = self.r3(varRuleCode, varParam, TOKEN)  # GY_YH001001，'I10'
                self.outResult(l_result, k, varSheetName, Openpyxl_PO)

            elif l_v1[0] == "r4":
                # 分解 "r4,  '01','JB002'
                varParam1 = l_v1[1]  # 01
                varParam2 = l_v1[2]  # job002
                print(str(k) + " => (" + l_v1[0] + ")")
                l_result = self.r4(varRuleCode, varParam1, varParam2, TOKEN)
                self.outResult(l_result, k, varSheetName, Openpyxl_PO)

            elif l_v1[0] == "r6":
                # 分解 "r4,  '01','JB002'
                varParam1 = l_v1[1]  # 01
                print(str(k) + " => (" + l_v1[0] + ")")
                l_result = self.r6(varRuleCode, varParam1, TOKEN)
                self.outResult(l_result, k, varSheetName, Openpyxl_PO)




    def run(self, varSheetName, varResult, varRuleParam, Openpyxl_PO, TOKEN):

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
            # print(l_paramCode[2])  # PG_JWS013  //健康评估规则库编码
            # print(l_paramCode[3])  # YH_JB008  //疾病评估规则编码


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


        if varResult == "ALL" :
            if varRuleParam == "":
                # 遍历所有记录
                # ChcRule_PO.run('健康评估', "ALL", "", Openpyxl_PO, TOKEN)
                self.runRule(varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
            else:
                # 遍历所有及指定测试规则的记录，如只执行r1
                # ChcRule_PO.run('健康评估', "ALL", "r1", Openpyxl_PO, TOKEN)
                self.runRule_param(varRuleParam, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
        else:
            if varResult == "" :
                if varRuleParam == "":
                    # ChcRule_PO.run('健康评估', "", "", Openpyxl_PO, TOKEN)
                    self.runRule_resultNull(varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
                else:
                    # 遍历指定结果及指定测试规则的记录，如所有的r1
                    # ChcRule_PO.run('健康评估', "", "r1", Openpyxl_PO, TOKEN)
                    self.runRule_param(varRuleParam, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
            else:
                if varRuleParam == "":
                    # 遍历指定结果的记录，如OK
                    # ChcRule_PO.run('健康评估', "ERROR", "", Openpyxl_PO, TOKEN)
                    # ChcRule_PO.run('健康评估', "OK", "", Openpyxl_PO, TOKEN)
                    self.runRule_result(varResult, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)
                else:
                    # 遍历指定结果及指定测试规则的记录，如ok，r1
                    # ChcRule_PO.run('健康评估', "OK", "r1", Openpyxl_PO, TOKEN)
                    # ChcRule_PO.run('健康评估', "ERROR", "r1", Openpyxl_PO, TOKEN)
                    self.runRule_Resultparam(varResult, varRuleParam, varSheetName, d_paramCode, Openpyxl_PO, TOKEN)




    def r1(self, varSort, varRuleCode, varParam, TOKEN):

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
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
                Color_PO.consoleColor("31", "33", sql, "")
                Color_PO.consoleColor("31", "36", "记录数：" + str(l_result[0]['NO']) + "条", "")

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
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
                sql1 = "\n" + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                Color_PO.consoleColor("31", "36", "记录数：" + str(l_result[0]['NO']) + "条", "")
                log = log + sql + sql1 + "\n"
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
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
                sql1 = "\n" + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                Color_PO.consoleColor("31", "36", "记录数：" + str(l_result[0]['NO']) + "条", "")
                log = log + sql + sql1 + "\n"
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
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varASSESS_ID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
                sql1 = "\n" + str(l_result[0]['NO']) + "条"
                Color_PO.consoleColor("31", "33", sql, "")
                Color_PO.consoleColor("31", "36", "记录数：" + str(l_result[0]['NO']) + "条", "")
                log = log + sql + sql1 + "\n"
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
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE= '" + str(varRuleCode) + "'"
                Color_PO.consoleColor("31", "33", sql, "")
                Color_PO.consoleColor("31", "36", "记录数：" + str(l_result[0]['NO']) + "条", "")
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
                sql = "select count(*) NO from T_ASSESS_RULE_RECORD where ASSESS_ID = " + str(varID) + " and RULE_CODE = '" + str(varRuleCode) + "'"
                Color_PO.consoleColor("31", "33", sql, "")
                Color_PO.consoleColor("31", "36", "记录数：" + str(l_result[0]['NO']) + "条", "")
                log = log + sql + "\n"
                if l_result[0]['NO'] == 1:
                    return 1
                else:
                    return log

        else:
            return log










    # def healthAssessment(self, Openpyxl_PO: object, TOKEN: object) -> object:
    #
    #     '''
    #     健康评估规则库
    #     :param Openpyxl_PO:
    #     :param TOKEN:
    #     :return:
    #     '''
    #
    #     # 获取"健康评估规则库"的规则编码和自动化规则
    #     l_codeParam = (Openpyxl_PO.getColValueByCol([5, 7], [1], '健康评估规则库'))  # 获取第5、7列值，忽略第一行数据
    #     d_paramCode = dict(zip(l_codeParam[1], l_codeParam[0]))
    #     print(d_paramCode)
    #     No = 2
    #     for k, v in d_paramCode.items():
    #         k = Str_PO.str2list(k)
    #
    #         if k != None:
    #             if k[0] == 'r1':
    #                 print(No, k, v)
    #                 varTbl = k[1]  # T_ASSESS_INFO
    #                 varParam = k[3]  # AGE=55
    #                 varParam = varParam.replace(".and.", ',')
    #
    #                 # 1,获取数据id
    #                 l_value = Sqlserver_PO.execQuery("select top 1 %s from %s" % (k[2], varTbl))  # 获取表中第一条记录的id
    #                 varId = l_value[0][k[2]]
    #                 # print(v[2] + " = " + str(varId))  # ID = 1
    #
    #                 # 2，修改数据
    #                 # print("update " + varTbl + " set " + varParam + " where " + v[2] + "=" + str(varId))
    #                 Color_PO.consoleColor("31", "33",
    #                                       "update " + varTbl + " set " + varParam + " where " + k[2] + "=" + str(varId),
    #                                       "")
    #                 Sqlserver_PO.execute("update %s set %s where %s='%s'" % (varTbl, varParam, k[2], varId))
    #
    #                 # 3，跑规则
    #                 self.i_AssessRuleRecord(varId, TOKEN)
    #
    #                 # 4，检查"评估规则结果表"
    #                 l_result = (self.getResult(varId, v))
    #
    #                 if l_result != []:
    #                     # print(l_result)  # [{'ID': 26162}]
    #                     # print(No, " = > OK\n")
    #                     Color_PO.consoleColor("31", "36", str(No) + " => OK\n", "")
    #                     Openpyxl_PO.setCellValue(No, 8, "OK", "健康评估规则库")
    #                 else:
    #                     # print(No, " = > ERROR\n")
    #                     Color_PO.consoleColor("31", "31", str(No) + " => ERROR\n", "")
    #                     Openpyxl_PO.setCellValue(No, 8, "ERROR", "健康评估规则库")
    #                 Openpyxl_PO.setCellValue(No, 9, Time_PO.getDateTimeByDivide(), "健康评估规则库")
    #                 Openpyxl_PO.setCellValue(1, 8, "自动化测试结果", "健康评估规则库")
    #
    #         No = No + 1
    #     Openpyxl_PO.open()


    # def healthInterposal123(self, Openpyxl_PO, TOKEN):
    #
    #     '''
    #     健康干预规则库
    #     :param Openpyxl_PO:
    #     :param TOKEN:
    #     :return:
    #     '''
    #
    #     # 获取"健康评估规则库"的规则编码和自动化规则
    #     l_codeParam = (Openpyxl_PO.getColValueByCol([2, 8], [1], '健康干预规则库'))  # 获取第2、9列值，忽略第一行数据
    #     d_paramCode = dict(zip(l_codeParam[1], l_codeParam[0]))
    #     print(d_paramCode)
    #     No = 2
    #     for k, v in d_paramCode.items():
    #         k = Str_PO.str2list(k)
    #         if k != None:
    #
    #             if k[0] == 'r2':
    #                 print(No, k, v)
    #                 varTbl = k[1]  # T_ASSESS_INFO
    #                 varParam = k[3]  # AGE=55
    #                 varParam = varParam.replace(".and.", ',')
    #
    #                 # 1，修改数据
    #                 # print("update " + varTbl + " set " + varParam + " where id=1")
    #                 Color_PO.consoleColor("31", "33", "update " + varTbl + " set " + varParam + " where id=1", "")
    #                 Sqlserver_PO.execute("update %s set %s where id=1" % (varTbl, varParam))
    #                 l_var = Sqlserver_PO.execQuery("select %s from %s where id=1" % (k[2], varTbl))
    #                 # print("select " + v[2] + " from " + varTbl + " where id=1")
    #                 varIDcard = l_var[0]['IDCARD']
    #                 print("身份证：" + str(varIDcard))
    #
    #                 # 2,新增评估
    #                 self.i_newAssess(varIDcard, TOKEN)
    #
    #                 # 3, 获取评估表id
    #                 l_var = Sqlserver_PO.execQuery("select id from T_ASSESS_INFO where ID_CARD='%s'" % (varIDcard))
    #                 # print(l_var)
    #                 varId = l_var[0]['id']
    #                 # print(varId)
    #
    #                 # 4，跑规则
    #                 self.i_AssessRuleRecord(varId, TOKEN)
    #
    #                 # 5，检查"评估规则结果表"
    #                 l_result = (self.getResult(varId, v))
    #                 if l_result != []:
    #                     # print(No, " = > OK\n")
    #                     Color_PO.consoleColor("31", "36", str(No) + " => OK\n", "")
    #                     Openpyxl_PO.setCellValue(No, 9, "OK", "健康干预规则库")
    #                 else:
    #                     # print(No, " = > ERROR\n")
    #                     Color_PO.consoleColor("31", "31", str(No) + " => ERROR\n", "")
    #                     Openpyxl_PO.setCellValue(No, 9, "ERROR", "健康干预规则库")
    #                 Openpyxl_PO.setCellValue(No, 10, Time_PO.getDateTimeByDivide(), "健康干预规则库")
    #                 # Openpyxl_PO.setCellValue(1, 8, "自动化测试结果", "健康干预规则库")
    #         No = No + 1
    #     Openpyxl_PO.open()