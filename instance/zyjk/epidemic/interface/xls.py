# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# pip3 install jsonpath for cmd
# pip3 install pymysql for cmd
# pip3 install mysqlclient  (MySQLdb) for cmd
# *****************************************************************
import json, jsonpath, platform, os
from datetime import datetime
import reflection
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from OpenpyxlPO import *
from MysqlPO import *
from DictPO import *
Dict_PO = DictPO()
from DataPO import *
Data_PO = DataPO()
from time import strftime, localtime
import time


class XLS:

    def __init__(self):

        # 初始化表格
        if platform.system() == 'Darwin':
            self.varExcel = os.path.dirname(os.path.abspath("__file__")) + u'/' + localReadConfig.get_system("xlsName")
        if platform.system() == 'Windows':
            self.varExcel = os.path.dirname(os.path.abspath("__file__")) + u'\\' + localReadConfig.get_system("xlsName")
        self.Openpyxl_PO = OpenpyxlPO(self.varExcel)
        self.Openpyxl_PO.closeExcelPid('EXCEL.EXE')   # 关闭excel进程
        l_sheetNames = (self.Openpyxl_PO.wb.sheetnames)   # 所有工作表名列表：如 ['inter', 'case']
        self.sheetInter = l_sheetNames[0]  # inter工作表
        self.sheetCase = l_sheetNames[1]  # case工作表
        self.d_inter = {}


        self.Openpyxl_PO.clsColData(9, self.sheetCase)  # 清空返回值
        self.Openpyxl_PO.clsColData(11, self.sheetCase)  # 清空返回值
        self.Openpyxl_PO.clsColData(14, self.sheetCase)  # 清空返回值
        self.Openpyxl_PO.clsColData(16, self.sheetCase)  # 清空返回值
        self.Openpyxl_PO.wb.save(self.varExcel)
        self.d_tmp = {}  # 临时字典

        if localReadConfig.get_env("switchENV") == "test":
            db_ip = localReadConfig.get_test("db_ip")
            db_username = localReadConfig.get_test("db_username")
            db_password = localReadConfig.get_test("db_password")
            db_port = localReadConfig.get_test("db_port")
            db_database = localReadConfig.get_test("db_database")
        else:
            db_ip = localReadConfig.get_dev("db_ip")
            db_username = localReadConfig.get_dev("db_username")
            db_password = localReadConfig.get_dev("db_password")
            db_port = localReadConfig.get_dev("db_port")
            db_database = localReadConfig.get_dev("db_database")
        self.Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)


    def getCaseParam(self):

        ''' 遍历获取 excelNo、名称、路径、方法、参数、检查key、检查value、全局变量、sql语句 '''

        l_case = []
        l_casesuit = []
        sh = self.Openpyxl_PO.sh(self.sheetCase)
        for i in range(sh.max_row-1):
            if sh.cell(row=i+2, column=1).value == "N" or sh.cell(row=i+2, column=1).value == "n":
                pass
            else:
                l_case.append(i+2)  # excelNo
                l_case.append(sh.cell(row=i+2, column=2).value)  # 类型
                l_case.append(sh.cell(row=i+2, column=3).value)  # 模块
                l_case.append(sh.cell(row=i+2, column=4).value)  # 名称
                l_case.append(sh.cell(row=i+2, column=5).value)  # 路径
                l_case.append(sh.cell(row=i+2, column=6).value)  # 方法
                l_case.append(sh.cell(row=i+2, column=7).value)  # 参数
                l_case.append(sh.cell(row=i+2, column=8).value)  # 担当者
                l_case.append(sh.cell(row=i+2, column=10).value)  # 检查返回值
                l_case.append(sh.cell(row=i+2, column=12).value)  # s表值
                l_case.append(sh.cell(row=i+2, column=13).value)  # s检查表值
                l_case.append(sh.cell(row=i+2, column=15).value)  # f检查文件位置
                l_case.append(sh.cell(row=i+2, column=17).value)  # 全局变量
                l_case.append(sh.max_row-1)  # 用例总数
                l_casesuit.append(l_case)
                l_case = []
        # print(l_casesuit)
        return l_casesuit

    # def result(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iCheckResponse,  g_dict, s_sql, g_userDefined, iAssert, tester, caseQty):

    def result(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, tester, responseCheck, selectSql, selectSqlCheck, fileLocation, g_var, caseQty):

        ''' 1替换参数，2解析接口，3检查值 '''

        # 1.1替换路径
        if "{{" in iPath:
            for k in self.d_tmp:
                if "{{" + k + "}}" in iPath:
                    iPath = str(iPath).replace("{{" + k + "}}", str(self.d_tmp[k]))
        # 1.2替换参数
        if iParam != None:
            if "{{" in iParam:
                for k in self.d_tmp :
                    if "{{" + k + "}}" in iParam:
                        iParam = str(iParam).replace("{{" + k + "}}", str(self.d_tmp[k]))

        # 1.3替换全局变量
        if g_var != None:
            if "{{" in g_var:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in g_var:
                        # g_var = str(g_var).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')
                        g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # d_var = json.loads(g_var)
            d_var = dict(eval(g_var))
            for k, v in d_var.items():
                if "str(" in str(v):
                    d_var[k] = eval(d_var[k])
        else:
            d_var ={}

        # 1.4替换检查返回值
        if responseCheck != None:
            if "{{" in responseCheck:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in responseCheck:
                        responseCheck = str(responseCheck).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')

        # 2解析接口 （返回值）
        res, d_var = reflection.run([iName, iPath, iMethod, iParam, d_var])
        # 用于downFile情况
        if res == None:
            d_res = None
        else:
            d_res = json.loads(res)


        # 3i检查返回值 iCheckResponse（如 $.code=200）
        try:
            if d_res != None:
                varSign = ""
                d_responseCheck = json.loads(responseCheck)
                if len(d_responseCheck) == 1:
                    for k, v in d_responseCheck.items():
                        iResValue = jsonpath.jsonpath(d_res, expr=k)

                        if v == iResValue[0]:
                            print("\n<font color='blue'>responseCheck => " + str(k) + " = " + str(v) + " </font>")
                            self.setCaseParam(excelNo, d_res, "Ok", None, None)
                        else:
                            self.setCaseParam(excelNo, d_res, "Fail", None, None)
                            assert v == iResValue[0], "预期值: " + str(v) + "，实测值: " + iResValue
                else:
                    for k, v in d_responseCheck.items():
                        iResValue = jsonpath.jsonpath(d_res, expr=k)
                        if v == iResValue[0]:
                            print("\n<font color='blue'>responseCheck => " + str(k) + " = " + str(v) + " </font>")
                        else:
                            print("\n<font color='red'>responseCheck => " + str(k) + " != " + str(v) + " </font>")
                            varSign = "error"
                    if varSign == "error":
                        self.setCaseParam(excelNo, d_res, "Fail", None, None)
                        assert v == iResValue[0], "预期值: " + str(v) + "，实测值: " + iResValue
                    else:
                        self.setCaseParam(excelNo, d_res, "Ok", None, None)

        except Exception as e:
            print(e.__traceback__)
            assert 1 == 0, "【i检查返回值】列有误，请检查参数或变量是否引用正确！"


        # s表值
        if selectSql != None:
            if "{{" in selectSql:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in selectSql:
                        selectSql = str(selectSql).replace("{{" + k + "}}", str(self.d_tmp[k]))
            try:
                # 转全局变量
                d_sql = json.loads(selectSql)
                for k, v in d_sql.items():
                    sql_value = self.Mysql_PO.execQuery(v)
                    self.d_tmp[k] = sql_value[0][0]
                    print("\n<font color='green'>selectSql => " + str(k) + " = " + str(sql_value[0][0]) + " </font>")
            except Exception as e:
                print(e.__traceback__)
                assert 1 == 0, "【s表值】有误，请检查参数或变量是否引用正确！"

        # s检查表值
        try:
            varSign = ""
            if selectSqlCheck != None:
                d_selectSqlCheck = json.loads(selectSqlCheck)
                if len(d_selectSqlCheck) == 1:
                    for k, v in d_selectSqlCheck.items():
                        if self.d_tmp[k] == v:
                            print("\n<font color='green'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                            self.setCaseParam(excelNo, d_res, None, "Ok", None)
                        else:
                            print("\n<font color='red'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                            self.setCaseParam(excelNo, d_res, None, "Fail", None)
                else:
                    for k, v in d_selectSqlCheck.items():
                        if self.d_tmp[k] == v:
                            print("\n<font color='green'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                        else:
                            print("\n<font color='red'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                            varSign = "error"
                    if varSign == "error":
                        self.setCaseParam(excelNo, d_res, None, "Fail", None)
                    else:
                        self.setCaseParam(excelNo, d_res, None, "Ok", None)
        except Exception as e:
            print(e.__traceback__)
            assert 1 == 0, "【s检查表值】列有误，请检查参数或变量是否引用正确！"
        # f检查文件位置



        # 当前变量
        print("\ncurrVar => " + str(d_var))

        # 全局变量
        self.d_tmp = dict(self.d_tmp, **d_var)  # 合并字典，如key重复，则前面字典key值被后面字典所替换
        print("\n<font color='purple'>globalVar => " + str(self.d_tmp) + "</font>")




    def setCaseParam(self, excelNo, d_res, responseCheckResult, selectSqlResult, fileLocationResult):

        ''' 更新表格数据 '''

        # i返回值
        self.Openpyxl_PO.setCellValue(excelNo, 9, str(d_res), ['c6efce', '006100'], self.sheetCase)

        # i结果
        if responseCheckResult != None:
            if responseCheckResult == "Ok":
                self.Openpyxl_PO.setCellValue(excelNo, 11, "Ok", ['c6efce', '006100'], self.sheetCase)
            else:
                self.Openpyxl_PO.setCellValue(excelNo, 11, "Fail", ['ffeb9c', '000000'], self.sheetCase)

        # s结果
        if selectSqlResult != None:
            if selectSqlResult == "Ok":
                self.Openpyxl_PO.setCellValue(excelNo, 14, "Ok", ['c6efce', '006100'], self.sheetCase)
            else:
                self.Openpyxl_PO.setCellValue(excelNo, 14, "Fail", ['ffeb9c', '000000'], self.sheetCase)

        # f结果
        if fileLocationResult != None:
            if fileLocationResult == "Ok":
                self.Openpyxl_PO.setCellValue(excelNo, 16, "Ok", ['c6efce', '006100'], self.sheetCase)
            else:
                self.Openpyxl_PO.setCellValue(excelNo, 16, "Fail", ['ffeb9c', '000000'], self.sheetCase)

        # # 日期
        # self.Openpyxl_PO.setCellValue(excelNo, 3, str(datetime.now().strftime("%Y-%m-%d")), ['ffffff', '000000'], self.sheetCase)


        self.Openpyxl_PO.wb.save(self.varExcel)

if __name__ == '__main__':
    xls = XLS()
