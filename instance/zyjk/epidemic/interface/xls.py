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

        self.Openpyxl_PO.clsColData(2, self.sheetCase)  # 清空结果
        self.Openpyxl_PO.clsColData(3, self.sheetCase)  # 清空日期
        self.Openpyxl_PO.clsColData(10, self.sheetCase)  # 清空返回值
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
        # 从第二行开始遍历
        #
        for i in range(sh.max_row-1):
            if sh.cell(row=i+2, column=1).value == "N" or sh.cell(row=i+2, column=1).value == "n":
                pass
            else:
                l_case.append(i+2)  # excelNO
                l_case.append(sh.cell(row=i+2, column=4).value)  # 类型
                l_case.append(sh.cell(row=i+2, column=5).value)  # 大类
                l_case.append(sh.cell(row=i+2, column=6).value)  # 名称
                l_case.append(sh.cell(row=i+2, column=7).value)  # 路径
                l_case.append(sh.cell(row=i+2, column=8).value)  # 方法
                l_case.append(sh.cell(row=i+2, column=9).value)  # 参数
                l_case.append(sh.cell(row=i+2, column=11).value)  # 检查返回值
                l_case.append(sh.cell(row=i+2, column=12).value)  # 全局字典变量
                l_case.append(sh.cell(row=i+2, column=13).value)  # 全局sql
                l_case.append(sh.cell(row=i+2, column=14).value)  # 全局脚本变量
                l_case.append(sh.cell(row=i+2, column=15).value)  # 断言条件
                l_case.append(sh.cell(row=i+2, column=17).value)  # 担当者
                l_case.append(sh.max_row-1)  # 用例总数
                l_casesuit.append(l_case)
                l_case = []

        return l_casesuit

    def result(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iCheckResponse,  g_dict, s_sql, g_script, iAssert, tester, caseQty):

        ''' 替换参数，解析接口，检查 iCheckResponse '''

        # 路径
        if "{{" in iPath:
            for k in self.d_tmp:
                if "{{" + k + "}}" in iPath:
                    iPath = str(iPath).replace("{{" + k + "}}", str(self.d_tmp[k]))

        # 参数
        if iParam != None:
            if "{{" in iParam:
                for k in self.d_tmp :
                    if "{{" + k + "}}" in iParam:
                        iParam = str(iParam).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')

        # 变量(g)
        if g_dict != None:
            if "{{" in g_dict:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in g_dict:
                        g_dict = str(g_dict).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')

        # 返回值
        res, d_g_dict = reflection.run([iName, iPath, iMethod, iParam, g_dict])
        # 用于downFile情况
        if res == None:
            d_res = None
        else:
            d_res = json.loads(res)
        # 更新变量(g)（合并字典）
        if d_g_dict != None:
            self.d_tmp = dict(self.d_tmp, **d_g_dict)  # 合并字典，如key重复，则前面字典key值被后面字典所替换


        # 检查返回值 iCheckResponse（如 $.code=200）
        try:
            if d_res != None:
                # $.code: 200
                if len(iCheckResponse.split(",")) == 1:
                    iResValue = jsonpath.jsonpath(d_res, expr=iCheckResponse.split(":")[0])
                    iResValue = str(iResValue[0])  # 200

                    # 检查返回值中有变量，如 $.code:{{var}}
                    if "{{" in iCheckResponse.split(":")[1]:
                        for k in self.d_tmp:
                            if "{{" + k + "}}" in iCheckResponse.split(":")[1]:
                                testResponse = str(iCheckResponse.split(":")[1]).replace("{{" + k + "}}",
                                                                                         str(self.d_tmp[k]))
                                if iResValue != testResponse:
                                    self.setCaseParam(excelNo, "Fail", d_res)
                                    assert iResValue == iCheckResponse.split(":")[1], "预期值: " + \
                                                                                      iCheckResponse.split(":")[
                                                                                          1] + "，实测值: " + iResValue + ""
                                else:
                                    print("\n<font color='green'>【检查返回值】：" + str(iCheckResponse) + " = " + str(
                                        iResValue) + " </font>")
                                    self.setCaseParam(excelNo, "Ok", d_res)
                    # 检查返回值中是明确的值，如 $.code:200
                    elif iResValue != iCheckResponse.split(":")[1]:
                        self.setCaseParam(excelNo, "Fail", d_res)
                        assert iResValue == iCheckResponse.split(":")[1], "预期值: " + iCheckResponse.split(":")[
                            1] + "，实测值: " + iResValue + ""
                    else:
                        print("\n<font color='green'>【检查返回值】：" + str(iCheckResponse) + " </font>")
                        self.setCaseParam(excelNo, "Ok", d_res)
                else:
                    # $.code: 200, $.msg: success}
                    sign = 0
                    for i in range(len(iCheckResponse.split(","))):
                        iResValue = jsonpath.jsonpath(d_res, expr=iCheckResponse.split(",")[i].split(":")[0])
                        iResValue = str(iResValue[0])  # 200

                        # 检查返回值中有变量，如 $.code:{{var}}
                        if "{{" in iCheckResponse.split(",")[i].split(":")[1]:
                            for k in self.d_tmp:
                                if "{{" + k + "}}" in iCheckResponse.split(",")[i].split(":")[1]:
                                    testResponse = str(iCheckResponse.split(",")[i].split(":")[1]).replace(
                                        "{{" + k + "}}", str(self.d_tmp[k]))
                                    if iResValue != testResponse:
                                        sign = 1
                                    else:
                                        sign = 0
                    if sign == 1:
                        self.setCaseParam(excelNo, "Fail", d_res)
                        assert iResValue == iCheckResponse.split(",")[i].split(":")[1], "预期值: " + \
                                                                                        iCheckResponse.split(",")[
                                                                                            i].split(":")[
                                                                                            1] + "，实测值: " + iResValue + ""
                    else:
                        print("\n<font color='green'>【检查返回值】：" + str(iCheckResponse) + " </font>")
                        self.setCaseParam(excelNo, "Ok", d_res)
            else:
                pass
        except Exception as e:
            print(e.__traceback__)
            self.setCaseParam(excelNo, "Fail", d_res)
            assert 1 == 0, "返回值中未找到 " + str(iCheckResponse)

        # sql变量（g）
        if s_sql != None:
            if "{{" in s_sql:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in s_sql:
                        s_sql = str(s_sql).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # 转变量（g）
            d_sql = json.loads(s_sql)
            for k, v in d_sql.items():
                sql_value = self.Mysql_PO.execQuery(v)
                self.d_tmp[k] = sql_value[0][0]
                print("\n【全局sql】：" + str(k) + " = (" + str(sql_value[0][0] ) + ")")

        # 自定义变量（g）
        if g_script != None and "=" in g_script:
            g_script_name = str(g_script).split("=")[0]
            self.d_tmp[g_script_name] = eval(str(g_script).split("=")[1])


        # 输出变量（g）
        print("\n<font color='purple'>【全局字典变量】：" + str(self.d_tmp) + "</font>")

        # 断言变量
        if iAssert != None:

            # 断言下载文件
            if str(iAssert).split("=")[0] == "file":
                # 判断文件是否存在
                # print(str(iAssert).split("=")[1])
                if (os.path.isfile(str(iAssert).split("=")[1])):
                    self.setCaseParam(excelNo, "Ok", d_res, "True")
                else:
                    self.setCaseParam(excelNo, "Fail", d_res, "False")
            else:
                # 断言变量(g)
                if isinstance(self.d_tmp[str(iAssert).split("=")[0]], int):
                    if self.d_tmp[str(iAssert).split("=")[0]] == int(str(iAssert).split("=")[1]):
                        self.setCaseParam(excelNo, "Ok", d_res, "True")
                    else:
                        self.setCaseParam(excelNo, "Fail", d_res, "False")
                elif isinstance(self.d_tmp[str(iAssert).split("=")[0]], str):
                    if self.d_tmp[str(iAssert).split("=")[0]] == str(iAssert).split("=")[1]:
                        self.setCaseParam(excelNo, "Ok", d_res, "True")
                    else:
                        self.setCaseParam(excelNo, "Fail", d_res, "False")




    def setCaseParam(self, excelNo, result, d_res, result_assert=""):

        ''' 更新表格数据 '''

        # 结果
        if result == "Ok":
            self.Openpyxl_PO.setCellValue(excelNo, 2, "Ok", ['c6efce', '006100'], self.sheetCase)
        else:
            self.Openpyxl_PO.setCellValue(excelNo, 2, "Fail", ['ffeb9c', '000000'], self.sheetCase)

        # 日期
        self.Openpyxl_PO.setCellValue(excelNo, 3, str(datetime.now().strftime("%Y-%m-%d")), ['ffffff', '000000'], self.sheetCase)

        # 返回值
        self.Openpyxl_PO.setCellValue(excelNo, 10, str(d_res), ['c6efce', '006100'], self.sheetCase)

        # 断言结果
        if result_assert == "True":
            self.Openpyxl_PO.setCellValue(excelNo, 16, "True", ['c6efce', '006100'], self.sheetCase)
        if result_assert == "False":
            self.Openpyxl_PO.setCellValue(excelNo, 16, "False", ['ffeb9c', '000000'], self.sheetCase)

        self.Openpyxl_PO.wb.save(self.varExcel)

if __name__ == '__main__':
    xls = XLS()
