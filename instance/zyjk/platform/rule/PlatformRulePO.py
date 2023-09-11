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

    def genRecord(self, varSheet, Openpyxl_PO):

        # 生成记录(对空表生成记录)

        # 1, 获取所有表名
        l_tables = Openpyxl_PO.getOneColValue(3, varSheet)
        l_tables.pop(0)
        l_tables = [x for i, x in enumerate(l_tables) if x not in l_tables[:i]]  # 去重
        print(l_tables)  # ['TB_HIS_MZ_Reg', 'TB_HIS_MZ_Charge', ]

        # 2, 遍历所有表，对空表生成记录
        for i in range(len(l_tables)):
            # 直接从系统表中查询表的总记录数（特别适合大数据）
            a = Sqlserver_PO.execQuery("SELECT rows FROM sysindexes WHERE id = OBJECT_ID('" + l_tables[i] + "') AND indid < 2")
            # print(l_tables[i], a[0]['rows'])
            if a[0]['rows'] == 0:
                Sqlserver_PO.instRecordByNotNull(l_tables[i])

    def result(self, k, varSign, varSheet, Openpyxl_PO):

        if varSign == 1 or varSign == True:
            Openpyxl_PO.setCellValue(k, 1, "OK", varSheet)
            Color_PO.consoleColor("31", "36", varSheet + " => " + str(k) + " => OK\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheet)
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheet)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheet)
        else:
            Openpyxl_PO.setCellValue(k, 1, "ERROR", varSheet)
            Color_PO.consoleColor("31", "31", varSheet + " => " + str(k) + " => ERROR\n", "")
            Openpyxl_PO.setCellValue(k, 2, Time_PO.getDateTimeByDivide(), varSheet)
            Openpyxl_PO.setCellFont(k, "A", color="000000", varSheet=varSheet)
            Openpyxl_PO.setCellFont(k, "B", color="000000", varSheet=varSheet)


    def feikong(self, varSheet, Openpyxl_PO):

        # 校验非空

        list = Openpyxl_PO.getRowValueByCol([4, 6], varSheet)
        list.pop(0)
        # print(list)  # [['TB_HIS_MZ_Reg ', 'GHRQ'], ['TB_HIS_MZ_Reg', 'GTHSJ']...]
        for i in range(len(list)):
            # print(i+2, list[i])
            # 获取字段的类型，如果是必填项跳过不验证
            d_NotNullNameType = Sqlserver_PO.getNotNullNameType(list[i][0])
            # print(d_NotNullNameType)  # # {'ID': 'int', 'NAME': 'text', 'AGE': 'int'}
            if list[i][1] not in d_NotNullNameType:
                Sqlserver_PO.updtRecord(list[i][0], list[i][1] + "=''")
                # 接口断言
                # ???

            else:
                self.result(i + 2, 1, varSheet, Openpyxl_PO)



    def riqi(self, varSheet, Openpyxl_PO):

        # 校验日期

        list = Openpyxl_PO.getRowValueByCol([4, 6, 8], varSheet)
        list.pop(0)
        print(list)  # [['TB_HIS_MZ_Reg ', 'GHRQ', 'date'], ['TB_HIS_MZ_Reg', 'GTHSJ', 'datetime'],]
        for i in range(len(list)):
            print(i+2, list[i])
            # 获取字段的类型
            s_type = Sqlserver_PO.getFieldType(list[i][0], list[i][1])
            # print(s_type)
            if s_type == list[i][2]:
                self.result(i + 2, 1, varSheet, Openpyxl_PO)
            else:
                self.result(i + 2, 0, varSheet, Openpyxl_PO)


    def shuzifanwei(self, varSheet, Openpyxl_PO):

        # 数字范围

        list = Openpyxl_PO.getRowValueByCol([4, 6, 10, 11], varSheet)
        list.pop(0)
        print(list)  # [['TB_YL_MZ_Medical_Record_Exam', 'AGE', 0, 200], ['TB_YL_MZ_Medical_Record_Exam', 'AGE_MONTH', 0, 11], ]
        # PlatformRule_PO.shuzifanwei(2, ['jh2', 'AGE', 0, 200], Openpyxl_PO)
        for i in range(len(list)):

            # 获取表中所有字段的大小
            l_size = Sqlserver_PO.execQuery(
                "SELECT B.name as Name, B.max_length as Size FROM sys.tables A INNER JOIN sys.columns B ON B.object_id = A.object_id LEFT JOIN sys.extended_properties C ON C.major_id = B.object_id AND C.minor_id = B.column_id inner join systypes d on B.user_type_id=d.xusertype WHERE A.name ='%s' order by B.column_id asc"
                % (list[i][0])
            )

            # print(l_size)  # [{'Name': 'ID', 'Size': 4}, {'Name': 'NAME', 'Size': 16}, {'Name': 'AGE', 'Size': 4}]

            # 遍历所有字段
            varSign = 0
            for j in range(len(l_size)):
                # print(l_size[i])
                if l_size[j]['Name'] == list[i][1]:
                    # print(l_size[j]['Size'])
                    if list[i][3] == l_size[j]['Size']:
                        varSign = 1
                        break

            self.result(i + 2, varSign, varSheet, Openpyxl_PO)


    def zhiyu(self, varSheet, Openpyxl_PO):

        # 校验值域

        list = Openpyxl_PO.getRowValueByCol([4, 6, 11], varSheet)
        list.pop(0)
        # print(list)  # [['TB_HIS_MZ_Reg', 'GTHBZ', '1,2'], ['TB_HIS_MZ_Reg', 'GHLB', '100,101,102,103,104,200,600,601,999'],]
        for i in range(len(list)):
            # print(i+2,list[i])
            if list[i][2] != None:
                l_zhiyu = Str_PO.str2list(list[i][2])
                # print(varList[0], varList[1], l_zhiyu)  # TB_HIS_MZ_Reg GTHBZ ['1', '2']

                varSign = 0
                for j in range(len(l_zhiyu)):
                    a = Sqlserver_PO.execQuery('select top(1) ' + list[i][1] + ' from ' + list[i][0])
                    # print(a[0][varList[1]])
                    # 判断值域与字段值是否一致
                    if l_zhiyu[j] == a[0][list[i][1]]:
                        varSign = 1
                        break

                self.result(i + 2, varSign, varSheet, Openpyxl_PO)


    def shenfenzheng(self, varSheet, Openpyxl_PO):

        # 校验身份证

        list = Openpyxl_PO.getRowValueByCol([4, 6], varSheet)
        list.pop(0)
        print(list)  # [['TB_YL_Patient_Information', 'ZJHM'], ['TB_LIS_Report_Exam', 'ZJHM'],】
        # PlatformRule_PO.shenfenzheng(2, ['jh2', 'AGE'], Openpyxl_PO)
        for i in range(len(list)):
            a = Sqlserver_PO.execQuery('select top(1) ' + list[i][1] + ' from ' + list[i][0])
            idcard = a[0][list[i][1]]
            # print(idcard)  # 310101198004110014
            self.result(i + 2, Data_PO.isIdCard(idcard), varSheet, Openpyxl_PO)










