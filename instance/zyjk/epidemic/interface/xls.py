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
        self.Openpyxl_PO.clsColData(13, self.sheetCase)  # 清空返回值
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
                l_case.append(sh.cell(row=i+2, column=10).value)  # 检查key
                l_case.append(sh.cell(row=i+2, column=11).value)  # 检查value
                l_case.append(sh.cell(row=i+2, column=12).value)  # 全局变量
                l_case.append(sh.cell(row=i+2, column=14).value)  # sql语句
                l_casesuit.append(l_case)
                l_case = []
        # print(l_casesuit)
        return l_casesuit

    def result(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iKey, iValue, globalVar, sql):

        ''' 替换参数，解析接口，检查iKey、iValue '''

        sql_before = ""
        sql_after = ""

        # 替换参数中的变量
        if iParam != None:
            if "{{" in iParam:
                for k in self.d_tmp :
                    if "{{" + k + "}}" in iParam:
                        iParam = str(iParam).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')

        if "{{" in iPath:
            for k in self.d_tmp:
                if "{{" + k + "}}" in iPath:
                    iPath = str(iPath).replace("{{" + k + "}}", str(self.d_tmp[k]))

        # 华丽分割线
        # print("\n" + (str(excelNo) + "，" + iName).center(100, "-"))

        # sql更新前
        if sql != None:
            if "{{" in sql:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in sql:
                        sql = str(sql).replace("{{" + k + "}}", str(self.d_tmp[k]))
            sql_before = self.Mysql_PO.execQuery(sql)
            print("\nsql更新前的值 => " + str(sql) + " => " + str(sql_before[0][0]))

        res, d_globalVar = reflection.run([iName, iPath, iMethod, iParam, globalVar])

        if d_globalVar != None:
            self.d_tmp = Dict_PO.getMergeDict2(self.d_tmp, d_globalVar)
        print("\n全局变量 => " + str(self.d_tmp))
        d_res = json.loads(res)

        # sql更新后
        if sql != None:
            if "{{" in sql:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in sql:
                        sql = str(sql).replace("{{" + k + "}}", str(self.d_tmp[k]))
            sql_after = self.Mysql_PO.execQuery(sql)
            print("\nsql更新后的值 => " + str(sql) + " => " + str(sql_after[0][0]))

        # 验证检查key和value（如 $.code=200）、sql更新前和更新后
        try:
            iResValue = jsonpath.jsonpath(d_res, expr=iKey)
            iResValue = str(iResValue[0])  # 200
            if iResValue != iValue:
                self.setCaseParam(excelNo, "Fail", d_res, sql_before, sql_after)
                assert iResValue == iValue, "预期值是<" + iValue + ">，而实测值是<" + iResValue + ">"
            else:
                self.setCaseParam(excelNo, "OK", d_res, sql_before, sql_after)
        except Exception as e:
            print(e.__traceback__)
            self.setCaseParam(excelNo, "Fail", d_res, sql_before, sql_after)
            assert 1 == 0, "返回字典中未找到：" + str(iKey) + " = " + str(iValue)




    def setCaseParam(self, excelNo, result, d_res, sql_before, sql_after):

        ''' 更新表格数据 '''

        # 结果
        if result == "OK":
            self.Openpyxl_PO.setCellValue(excelNo, 2, "OK", ['c6efce', '006100'], self.sheetCase)
        else:
            self.Openpyxl_PO.setCellValue(excelNo, 2, "Fail", ['ffeb9c', '000000'], self.sheetCase)
        # 日期
        self.Openpyxl_PO.setCellValue(excelNo, 3, str(datetime.now().strftime("%Y-%m-%d")), ['ffffff', '000000'], self.sheetCase)
        # 返回值
        self.Openpyxl_PO.setCellValue(excelNo, 13, str(d_res), ['c6efce', '006100'], self.sheetCase)
        # sql更新前值
        self.Openpyxl_PO.setCellValue(excelNo, 15, str(sql_before), ['c6efce', '006100'], self.sheetCase)
        # sql更新后值
        self.Openpyxl_PO.setCellValue(excelNo, 16, str(sql_after), ['c6efce', '006100'], self.sheetCase)

        self.Openpyxl_PO.wb.save(self.varExcel)

if __name__ == '__main__':
    xls = XLS()
