# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-8-1
# Description:
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import re, subprocess, requests, os, psutil, json
import sys

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "peopleHospital", "utf8")  # 测试环境
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



class PlatformRulePO():

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

        command = "curl -X POST \"http://192.168.0.201:28801/auth/login\" -H \"accept: */*\" -H \"Content-Type: application/json\" -d \"{ \\\"password\\\": \\\"" + str(
            varPass) + "\\\", \\\"userNo\\\": \\\"" + str(varUser) + "\\\"}\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)
        return (d_r['data']['token'])


    # 查询机构规则配置列表
    def getDatabaseRuleConfigList(self, ratioCategory, tableName, fieldName, TOKEN):

        # ("准确性", "TB_HIS_MZ_Reg", "GHBM", TOKEN)

        d_ratioCategory = {"准确性": 1, "完整性": 2, "一致性": 3, "及时性": 4}

        command = "curl -X GET \"http://192.168.0.201:28801/regional-dqc/ruleConfig/getDatabaseRuleConfigList?keyWord=" + str(tableName) + "&ratioCategory=" + str(d_ratioCategory[ratioCategory]) + "\" -H  \"token:" + str(TOKEN) + "\" -H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\""
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)
        return d_r
        # for i in range(len(d_r['data'])):
        #     if d_r['data'][i]['fieldName'] == fieldName:
        #         # print(d_r['data'][i])
        #         return d_r['data'][i]['id']

    # 校验测试(前端使用，拼接时分秒)
    def webTest(self, category, endTime, orgGroup, ruleIds, startTime, TOKEN):

        # PlatformRule_PO.webTest("非空", "2023-9-18", "B", id, "2023-09-18", TOKEN)

        d_category = {"非空": 1, "身份证": 2, "日期": 3, "数字范围": 4, "值阈": 5, "关联表": 6}
        command = "curl -X GET \"http://192.168.0.201:28801/regional-dqc/dataQualityController/webTest?category=" + \
                  str(d_category[category]) + "&endTime=" + str(endTime) + "&orgGroup=" + str(orgGroup) + \
                  "&ruleIds=" + str(ruleIds) + "&startTime=" + str(startTime) + \
                  "\" -H  \"token:" + str(TOKEN) + "\" -H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\""
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        return(d_r)
        # if d_r['data'] != []:
        #     print(d_r['data'][0]['errorDesc'])

    # 测试-汇总测试
    def testStatistics(self, startTime, endTime, TOKEN):
        command = "curl -X GET \"http://192.168.0.201:28801/regional-dqc/dataQualityController/test-statistics\" " \
                  "-H  \"token:" + str(TOKEN) + "\" -H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\" " \
                     "-d \"endTime=2023-9-21 00:00:00\" -d \"startTime=2023-9-21 23:45:45\""

        print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        print(d_r)
        return (d_r)




    def result(self, k, varSign, varInfo, varSheet, Openpyxl_PO):

        # self.result(i + 2, 1, varInfo, varSheet, Openpyxl_PO)

        if varSign == 1 or varSign == True:
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheet)
            Color_PO.consoleColor("31", "36", varSheet + " => " + str(k) + " => OK\n", "")
            Openpyxl_PO.setCellValue(k, 2, varInfo, varSheet)
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheet)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheet)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheet)
            Color_PO.consoleColor("31", "31", varSheet + " => " + str(k) + " => ERROR => " + str(varInfo), "")
            Openpyxl_PO.setCellValue(k, 2, varInfo, varSheet)
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheet)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheet)

    def result2(self, k, varSign, varInfo, varSheet, Openpyxl_PO):

        if varSign == 1 or varSign == True:
            Openpyxl_PO.setCellValue(k, 3, "OK", varSheet)
            Color_PO.consoleColor("31", "36", varSheet + " => " + str(k) + " => OK", "")
            Openpyxl_PO.setCellValue(k, 4, varInfo, varSheet)
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheet)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheet)
        else:
            Openpyxl_PO.setCellValue(k, 3, "ERROR", varSheet)
            Color_PO.consoleColor("31", "31", varSheet + " => " + str(k) + " => ERROR => " + str(varInfo), "")
            Openpyxl_PO.setCellValue(k, 4, varInfo, varSheet)
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheet)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheet)



    # 非空
    def feikong(self, varSheet, Openpyxl_PO, TOKEN):

        # 校验非空

        # # 1，对空表自动插入一条记录
        self.genRecord(varSheet, Openpyxl_PO)

        # 2，获取测试表与字段
        list = Openpyxl_PO.getRowValueByCol([4, 6], varSheet)
        list.pop(0)
        # print(list)  # [['TB_HIS_MZ_Reg ', 'GHRQ'], ['TB_HIS_MZ_Reg', 'GTHSJ']...]

        # 3，遍历表格
        for i in range(len(list)):
        # for i in range(25):
        # for i in range(105, 121):
            # print(i+2, list[i])
            # print(list[i][0], list[i][1])  # "TB_HIS_MZ_Reg", "GHBM"

            # 2, 执行"查询机构规则配置列表"接口，获取测试字段的id （如 "TB_HIS_MZ_Reg", "GHBM"）
            id = self.getDatabaseRuleConfigList("完整性", list[i][0], list[i][1], TOKEN)
            # print(id)

            # 3, 更新测试字段值为空
            # Sqlserver_PO.updtRecord('TB_HIS_MZ_Reg', "GHBM=444,CREATETIMEDQC='2020-12-12'", Top=1)
            Sqlserver_PO.updtRecord(list[i][0], list[i][1] + "=null,CREATETIMEDQC='2020-12-12 00:00:01'", Top=1)

            # # 4，执行"校验测试（前端使用，拼接时分秒）"接口，获取返回值
            d_result = self.webTest("非空", "2020-12-12", id, TOKEN)  # category, startTime,orgGroup,ruleIds
            # print(d_result)
            if d_result['data'] == []:
                # print(d_result)
                # 5，结果
                self.result(i + 2, 0, "返回[]", varSheet, Openpyxl_PO)
            else:
                print(d_result['data'])
                # 5，结果
                self.result(i + 2, 1, d_result['data'][0]['errorDesc'], varSheet, Openpyxl_PO)

            # # 获取数据库表必填项字段及类型
            # d_NotNullNameType = Sqlserver_PO.getNotNullNameType(list[i][0])
            # # print(d_NotNullNameType)  # # {'ID': 'int', 'NAME': 'text', 'AGE': 'int'}
            # # 不验证数据库表必填项
            # if list[i][1] not in d_NotNullNameType:
            #     Sqlserver_PO.updtRecord(list[i][0], list[i][1] + "=''")
            #     # 接口断言
            #     # ???
            #
            # else:
            #     self.result(i + 2, 1, varSheet, Openpyxl_PO)
    # 日期
    def riqi(self, varSheet, Openpyxl_PO, TOKEN):

        # 校验日期

        # # 1，对空表自动插入一条记录
        self.genRecord(varSheet, Openpyxl_PO)

        # 2，获取测试表与字段
        list = Openpyxl_PO.getRowValueByCol([4, 6, 7], varSheet)
        list.pop(0)
        # print(list)  # [['TB_HIS_MZ_Reg ', 'GHRQ', '日期校验'], ['TB_HIS_MZ_Reg', 'GTHSJ', '日期时间校验'],]

        # for i in range(len(list)):
        for i in range(0, 2):
        # for i in range(20, len(list)):

            # 2, 执行"查询机构规则配置列表"接口，获取测试字段的id （如 "TB_HIS_MZ_Reg", "GHBM"）
            id = self.getDatabaseRuleConfigList("准确性", list[i][0], list[i][1], TOKEN)
            # print(id)

            # 3, 更新测试字段值为空
            # Sqlserver_PO.updtRecord('TB_HIS_MZ_Reg', "GHBM=444,CREATETIMEDQC='2020-12-12'", Top=1)
            if list[i][2] == "日期校验":
                Sqlserver_PO.updtRecord(list[i][0], list[i][1] + " = 20221212", Top=1)
            elif list[i][2] == "日期时间校验":
                Sqlserver_PO.updtRecord(list[i][0], list[i][1] + " = '20221212 121212'", Top=1)

            # # 4，执行"校验测试（前端使用，拼接时分秒）"接口，获取返回值
            d_result = self.webTest("日期", "2020-12-12", id, TOKEN)  # category, startTime,orgGroup,ruleIds
            # print(d_result)
            if d_result['data'] == []:
                # print(d_result)
                # 5，结果
                self.result(i + 2, 0, "返回[]", varSheet, Openpyxl_PO)
            else:
                # print(d_result['data'])
                # 5，结果
                self.result(i + 2, 1, d_result['data'][0]['errorDesc'], varSheet, Openpyxl_PO)

            # # 获取字段的类型
            # s_type = Sqlserver_PO.getFieldType(list[i][0], list[i][1])
            # # print(s_type)
            # if s_type == list[i][2]:
            #     self.result(i + 2, 1, varSheet, Openpyxl_PO)
            # else:
            #     self.result(i + 2, 0, varSheet, Openpyxl_PO)
    # 数字范围
    def shuzifanwei(self, varSheet, Openpyxl_PO, TOKEN):

        # 数字范围
        self.genRecord(varSheet, Openpyxl_PO)

        list = Openpyxl_PO.getRowValueByCol([4, 6, 10, 11], varSheet)
        list.pop(0)
        print(list)  # [['TB_YL_MZ_Medical_Record_Exam', 'AGE', 0, 200], ['TB_YL_MZ_Medical_Record_Exam', 'AGE_MONTH', 0, 11], ]

        for i in range(len(list)):
        # for i in range(0,1):


            # 2, 执行"查询机构规则配置列表"接口，获取测试字段的id （如 "TB_HIS_MZ_Reg", "GHBM"）
            id = self.getDatabaseRuleConfigList("准确性", list[i][0], list[i][1], TOKEN)
            # print(id)

            # 获取表中所有字段的大小
            l_size = Sqlserver_PO.execQuery(
                "SELECT B.name as Name, B.max_length as Size FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc" % (
                list[i][0]))
            # print(l_size)  # [{'Name': 'ID', 'Size': 4}, {'Name': 'NAME', 'Size': 16}, {'Name': 'AGE', 'Size': 4}]
            # 遍历所有字段
            varSign = 0
            for j in range(len(l_size)):
                # print(l_size[i])
                if l_size[j]['Name'] == list[i][1]:
                    # print(l_size[j]['Size'])
                    if list[i][3] == l_size[j]['Size']:
                        varSign = 1
                        print(list[i][1], l_size[j]['Size'])
                        break
                    else:
                        print(list[i][1], l_size[j]['Size'])


            # # 3, 更新测试字段值为空
            # # Sqlserver_PO.updtRecord('TB_HIS_MZ_Reg', "GHBM=444,CREATETIMEDQC='2020-12-12'", Top=1)
            # if list[i][2] == "日期校验":
            #     Sqlserver_PO.updtRecord(list[i][0], list[i][1] + " = 20221212", Top=1)
            # elif list[i][2] == "日期时间校验":
            #     Sqlserver_PO.updtRecord(list[i][0], list[i][1] + " = '20221212 121212'", Top=1)

            # # # 4，执行"校验测试（前端使用，拼接时分秒）"接口，获取返回值
            # d_result = self.webTest("数字范围", "2020-12-12", id, TOKEN)  # category, startTime,orgGroup,ruleIds
            # # print(d_result)
            # if d_result['data'] == []:
            #     # print(d_result)
            #     # 5，结果
            #     self.result(i + 2, 0, "返回[]", varSheet, Openpyxl_PO)
            # else:
            #     # print(d_result['data'])
            #     # 5，结果
            #     self.result(i + 2, 1, d_result['data'][0]['errorDesc'], varSheet, Openpyxl_PO)


    # 值阈
    def zhiyu(self, varSheet, startTime, endTime, Openpyxl_PO, TOKEN):

        # 校验值域
        # 【腾讯文档】区域平台值域校验
        # https://docs.qq.com/doc/DS1NkRkNMVnRIaFdL

        # 1，获取表格测试值
        list = Openpyxl_PO.getRowValueByCol([6, 8, 13, 14, 1,3], varSheet)
        list.pop(0)
        # print(list)  # [['TB_HIS_MZ_Reg', 'GTHBZ', '1,2', '0,3'], ['TB_HIS_MZ_Reg', 'GHLB', '100,101,102,103,104,200,600,601,999', None], ...]


        # 遍历所有行
        for i in range(38, 45):
        # for i in range(len(list)):
            if list[i][4] == "ERROR" or list[i][5] == "ERROR":
                if list[i][2] != None:

                    # todo 正确字典代码
                    print("\n" + varSheet + " => " + str(i+2) + " => 字典代码[" + str(list[i][2]) + "]")

                    l_testZhiyu = list[i][2].split(",")  # ['01', '02', '03', '04', '05', '06', '07', '99']
                    varSign = 0
                    l_errorZhiyu = []
                    # 遍历所有的值域
                    for zy in range(len(l_testZhiyu)):
                        # 1, 初始化第一条测试数据
                        sql = "update top(1) " + str(list[i][0]) + " set CREATETIMEDQC='" + str(startTime) + " 11:11:11', " + list[i][1] + "='" + str(l_testZhiyu[zy] + "'")
                        Color_PO.consoleColor("31", "36", sql, "")
                        status = Sqlserver_PO.execute(list[i][0], sql)
                        sleep(1)
                        if status != "ok":
                            self.result(i + 2, 0, status, varSheet, Openpyxl_PO)
                            break

                        # 2, 执行"查询机构规则配置列表"接口，获取id
                        # print(list[i][0], list[i][1])
                        d_r = self.getDatabaseRuleConfigList("准确性", list[i][0], list[i][1], TOKEN)  # ("准确性", "TB_HIS_MZ_Reg", "GHBM", TOKEN)
                        # print(d_r)
                        for j in range(len(d_r['data'])):
                            if d_r['data'][j]['fieldName'] == list[i][1] and d_r['data'][j]['errorDesc'] == '数据项上传内容与值域要求不一致':
                                id = d_r['data'][j]['id']
                                break
                        # print(id)

                        # 3, 校验测试(前端使用，拼接时分秒) category, endTime, orgGroup, ruleIds, startTime, TOKEN)
                        d_r = self.webTest(varSheet, endTime, "B", id, startTime, TOKEN)
                        # print(len(d_r['data']))

                        # 多条不符合值域的记录
                        for l in range(len(d_r['data'])):
                            l_errorZhiyu.append(d_r['data'][l]['fieldValue'])
                        # print(list3)

                        list1 = []
                        # print(d_r['data'])
                        if d_r['data'] == []:
                            varSign = varSign + 0
                        else:
                            varSign = 1
                            print(d_r['data'])
                            for k, v in d_r['data'][0].items():
                                if v == None:
                                    list1.append(k)
                            # print(list1)
                    if varSign == 0:
                        self.result(i + 2, 1, "", varSheet, Openpyxl_PO)
                    else:
                        self.result(i + 2, 0, str(l_errorZhiyu), varSheet, Openpyxl_PO)

                    # todo 错误字典代码
                    print(varSheet + " => " + str(i + 2) + " => 错误字典代码[" + str(list[i][3]) + "]")

                    if list[i][3] != None:
                        l_testZhiyu = list[i][3].split(",")  # ['01', '02', '03', '04', '05', '06', '07', '99']
                        varSign = 0
                        l_errorZhiyu = []
                        # 遍历所有的值域
                        for zy in range(len(l_testZhiyu)):
                            # 1, 初始化第一条测试数据
                            sql = "update top(1) " + str(list[i][0]) + " set CREATETIMEDQC='" + str(startTime) + " 11:11:11', " + list[i][1] + "='" + str(l_testZhiyu[zy] + "'")
                            Color_PO.consoleColor("31", "36", sql, "")
                            Sqlserver_PO.execute(list[i][0], sql)
                            sleep(1)

                            # 2, 执行"查询机构规则配置列表"接口，获取id
                            d_r = self.getDatabaseRuleConfigList("准确性", list[i][0], list[i][1], TOKEN)
                            for j in range(len(d_r['data'])):
                                if d_r['data'][j]['fieldName'] == list[i][1] and d_r['data'][j][
                                    'errorDesc'] == '数据项上传内容与值域要求不一致':
                                    id = d_r['data'][j]['id']
                                    break
                            # print(id)

                            # 3, 校验测试(前端使用，拼接时分秒) category, endTime, orgGroup, ruleIds, startTime, TOKEN)
                            d_r = self.webTest(varSheet, endTime, "B", id, startTime, TOKEN)
                            # print(d_r['data'])

                            # 多条不符合值域的记录
                            for l in range(len(d_r['data'])):
                                l_errorZhiyu.append(d_r['data'][l]['fieldValue'])
                            # print(list3)

                            list1 = []
                            # print(d_r['data'])
                            if d_r['data'] == []:
                                varSign = 0
                            else:
                                varSign = 1
                                # print(d_r['data'])
                                for k, v in d_r['data'][0].items():
                                    if v == None:
                                        list1.append(k)
                                # print(list1)

                        if varSign == 0:
                            self.result2(i + 2, 0, str(List_PO.twoListGetLeftNotContainRight(l_testZhiyu, l_errorZhiyu)), varSheet, Openpyxl_PO)
                        else:
                            self.result2(i + 2, 1, "", varSheet, Openpyxl_PO)
                    else:
                        self.result2(i + 2, 0, "None", varSheet, Openpyxl_PO)


    # 身份证
    def shenfenzheng(self, varSheet, Openpyxl_PO):

        # 校验身份证
        self.genRecord(varSheet, Openpyxl_PO)
        list = Openpyxl_PO.getRowValueByCol([4, 6], varSheet)
        list.pop(0)
        print(list)  # [['TB_YL_Patient_Information', 'ZJHM'], ['TB_LIS_Report_Exam', 'ZJHM'],】
        # PlatformRule_PO.shenfenzheng(2, ['jh2', 'AGE'], Openpyxl_PO)
        for i in range(len(list)):
            a = Sqlserver_PO.execQuery('select top(1) ' + list[i][1] + ' from ' + list[i][0])
            idcard = a[0][list[i][1]]
            # print(idcard)  # 310101198004110014
            self.result(i + 2, Data_PO.isIdCard(idcard), varSheet, Openpyxl_PO)


    def genRecord123(self, varSheet, Openpyxl_PO):

        # 对空表生成记录

        # 1, 获取所有表名
        l_tables = Openpyxl_PO.getOneColValue(3, varSheet)
        l_tables.pop(0)
        l_tables = [x for i, x in enumerate(l_tables) if x not in l_tables[:i]]  # 去重
        print(l_tables)  # ['TB_HIS_MZ_Reg', 'TB_HIS_MZ_Charge', ]

        # 2, 遍历所有表，对空表生成记录
        for i in range(len(l_tables)):
            # 直接从系统表中查询表的总记录数（特别适合大数据）
            # print(l_tables[i])
            a = Sqlserver_PO.execQuery("SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + l_tables[i] + "') AND indid < 2")
            # print(l_tables[i], a[0]['rows'])
            # print(a)
            if a[0]['rows'] == 0:
                d_NotNullNameType = Sqlserver_PO.getNotNullNameType(l_tables[i])
                # print(d_NotNullNameType)
                if d_NotNullNameType != {} :
                    Sqlserver_PO.instRecordByNotNull(l_tables[i])
                else:
                    Sqlserver_PO.instRecord(l_tables[i])








