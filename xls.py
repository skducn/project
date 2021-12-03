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



class XLS:

    def __init__(self):

        pass

    def getCaseParam(self):

        ''' 遍历获取 excelNo、名称、路径、方法、参数、检查key、检查value、全局变量、sql语句 '''

        print(555555)
        # l_case = []
        # l_casesuit = []
        # sh = self.Openpyxl_PO.sh(self.sheetCase)
        # # 从第二行开始遍历
        #
        # for i in range(sh.max_row-1):
        #     if sh.cell(row=i+2, column=1).value == "N" or sh.cell(row=i+2, column=1).value == "n":
        #         pass
        #     else:
        #         l_case.append(i+2)  # excelNO
        #         l_case.append(sh.cell(row=i+2, column=4).value)  # 类型
        #         l_case.append(sh.cell(row=i+2, column=5).value)  # 大类
        #         l_case.append(sh.cell(row=i+2, column=6).value)  # 名称
        #         l_case.append(sh.cell(row=i+2, column=7).value)  # 路径
        #         l_case.append(sh.cell(row=i+2, column=8).value)  # 方法
        #         l_case.append(sh.cell(row=i+2, column=9).value)  # 参数
        #         l_case.append(sh.cell(row=i+2, column=11).value)  # 检查返回值
        #         l_case.append(sh.cell(row=i+2, column=12).value)  # 全局变量
        #         l_case.append(sh.cell(row=i+2, column=13).value)  # sql语句
        #         l_case.append(sh.cell(row=i+2, column=16).value)  # 担当者
        #         l_case.append(sh.max_row-1)  # 用例总数
        #         l_casesuit.append(l_case)
        #         l_case = []
        #
        # print(l_casesuit)
        # return l_casesuit

    def result(self, excelNo, iType, iSort, iName, iPath, iMethod, iParam, iCheckResponse,  globalVar, sql, tester, caseQty):

        ''' 替换参数，解析接口，检查 iCheckResponse '''

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
            sql_var = str(sql).split("=|||")[0]
            sql_command = len(str(sql).split("=|||")[1].split("|||"))
            # 只有1条sql语句
            if sql_command == 1:
                sql = str(sql).split("=|||")[1]
                sql_before = self.Mysql_PO.execQuery(sql)
                self.d_tmp[sql_var] = sql_before[0][0]
                print("\n【sql语句】：" + str(sql_var) + " = " + str(sql))
            else:
                # 多条sql语句
                for m in range(sql_command):
                    tmp = str(sql).split("=|||")[1].split("|||")[m]
                    sql_before = self.Mysql_PO.execQuery(tmp)
                    self.d_tmp[sql_var+str(m)] = sql_before[0][0]
                    print("\n【sql语句" + str(m+1) + "】：" + str(sql_var) + str(m) + " = " + str(tmp))


            # sql_before = self.Mysql_PO.execQuery(sql)
            # print("\n【接口前sql（" + str(sql) + "）查询值】：" + str(sql_before[0][0]))

        res, d_globalVar = reflection.run([iName, iPath, iMethod, iParam, globalVar])
        if d_globalVar != None:
            self.d_tmp = Dict_PO.getMergeDict2(self.d_tmp, d_globalVar)
        print("\n<font color='purple'>【全局变量】：" + str(self.d_tmp) + "</font>")
        d_res = json.loads(res)


        # # sql更新后
        # if sql != None:
        #     if "{{" in sql:
        #         for k in self.d_tmp:
        #             if "{{" + k + "}}" in sql:
        #                 sql = str(sql).replace("{{" + k + "}}", str(self.d_tmp[k]))
        #     sql_after = self.Mysql_PO.execQuery(sql)
            # print("\n【sql语句】：" + str(sql))
            # print("\n【接口前sql值】：" + str(sql_before[0][0]))
            # print("\n【接口前sql值】：" + str(sql_after[0][0]))


        # 检查返回值 iCheckResponse（如 $.code=200）
        try:
            # $.code: 200
            if len(iCheckResponse.split(",")) == 1:
                iResValue = jsonpath.jsonpath(d_res, expr=iCheckResponse.split(":")[0])
                iResValue = str(iResValue[0])  # 200

                # 检查返回值中有变量，如 $.code:{{var}}
                if "{{" in iCheckResponse.split(":")[1]:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in iCheckResponse.split(":")[1]:
                            testResponse = str(iCheckResponse.split(":")[1]).replace("{{" + k + "}}", str(self.d_tmp[k]))
                            if iResValue != testResponse:
                                self.setCaseParam(excelNo, "Fail", d_res, sql_before, sql_after)
                                assert iResValue == iCheckResponse.split(":")[1], "预期值: " + iCheckResponse.split(":")[1] + "，实测值: " + iResValue + ""
                            else:
                                print("\n<font color='green'>【检查返回值】：" + str(iCheckResponse) + " = " + str(iResValue) + " </font>")
                                self.setCaseParam(excelNo, "OK", d_res, sql_before, sql_after)
                # 检查返回值中是明确的值，如 $.code:200
                elif iResValue != iCheckResponse.split(":")[1]:
                    self.setCaseParam(excelNo, "Fail", d_res, sql_before, sql_after)
                    assert iResValue == iCheckResponse.split(":")[1], "预期值: " + iCheckResponse.split(":")[1] + "，实测值: " + iResValue + ""
                else:
                    print("\n<font color='green'>【检查返回值】：" + str(iCheckResponse) + " </font>")
                    self.setCaseParam(excelNo, "OK", d_res, sql_before, sql_after)
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
                                testResponse = str(iCheckResponse.split(",")[i].split(":")[1]).replace("{{" + k + "}}", str(self.d_tmp[k]))
                                if iResValue != testResponse:
                                    sign = 1
                                else:
                                    sign = 0
                if sign == 1:
                    self.setCaseParam(excelNo, "Fail", d_res, sql_before, sql_after)
                    assert iResValue == iCheckResponse.split(",")[i].split(":")[1], "预期值: " + iCheckResponse.split(",")[i].split(":")[1] + "，实测值: " + iResValue + ""
                else:
                    print("\n<font color='green'>【检查返回值】：" + str(iCheckResponse) + " </font>")
                    self.setCaseParam(excelNo, "OK", d_res, sql_before, sql_after)

        except Exception as e:
            print(e.__traceback__)
            self.setCaseParam(excelNo, "Fail", d_res, sql_before, sql_after)
            assert 1 == 0, "返回值中未找到 " + str(iCheckResponse)




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
        self.Openpyxl_PO.setCellValue(excelNo, 10, str(d_res), ['c6efce', '006100'], self.sheetCase)
        # sql更新前值
        # self.Openpyxl_PO.setCellValue(excelNo, 14, str(sql_before), ['c6efce', '006100'], self.sheetCase)
        # sql更新后值
        # self.Openpyxl_PO.setCellValue(excelNo, 15, str(sql_after), ['c6efce', '006100'], self.sheetCase)

        self.Openpyxl_PO.wb.save(self.varExcel)

if __name__ == '__main__':
    xls = XLS()
