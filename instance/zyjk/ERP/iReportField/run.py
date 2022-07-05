# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-6-30
# Description: erp - 统计报表 - 拜访分析报表
# 接口文档：http://192.168.0.238:8090/doc.html
#***************************************************************


import requests, json
import urllib3
urllib3.disable_warnings()

from PO.StrPO import *
Str_PO = StrPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.MysqlPO import *
db_ip = "192.168.0.238"
db_username = "root"
db_password = "ZAQ!2wsx"
db_port = 3306
db_database = "crmtest"
Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)
db_ip = "192.168.0.65"
db_username = "ceshi"
db_password = "123456"
db_port = 3336
db_database = "TD_OA"
Mysql_PO_OA = MysqlPO(db_ip, db_username, db_password, db_database, db_port)


# 所有地区经理和代表
db_t_userId_userName = Mysql_PO_OA.execQuery("select BYNAME, UID, USER_NAME from `user` where NOT_LOGIN=0 AND USER_PRIV_NAME='地区经理' or USER_PRIV_NAME='医药代表'")
# print(db_t_userId_userName)  # (('niuxuebin', 81, '钮学彬'), ('huangxinhui', 84, '黄新晖'),
# for i in range(len(db_t_userId_userName)):
#     print(db_t_userId_userName[i][0])  # niuxuebin
#     print(db_t_userId_userName[i][1])  # 81
#     print(db_t_userId_userName[i][2])  # 钮学彬



# 获取token
url = "http://192.168.0.65/logincheck.php"
header = {"content-type": "application/x-www-form-urlencoded"}
d_iParam = {'USERNAME':"niuxuebin"}
r = requests.post(url, headers=header, data=d_iParam, verify=False)
a = r.cookies.get_dict()
url = "http://192.168.0.65/general/appbuilder/web/business/product/crm"
r = requests.get(url, headers={"Cookie":"PHPSESSID=" + a["PHPSESSID"]}, verify=False)
# print(r.url)
token = str(r.url).split("token=")[1]


def visitAnalysis(tblField, iResField, sql):

    # visitAnalysis("计划拜访人次", "plannedVisitsNumber", "sql")
    sign = 0

    l_rowcol= Openpyxl_PO.getRowCol(varSheet)
    currCol = l_rowcol[1]+1
    currRow = 2
    Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)

    # 计划拜访人次
    # print(tblField, "--------------------------------------------------")
    # print(res_visitAnalysis['data'])

    for i in range(len(res_visitAnalysis['data'])):
        for k, v in res_visitAnalysis['data'][i].items():
            # 遍历报表上所有的人
            for j in range(len(db_t_userId_userName)):
                if k == "delegateId" and v == db_t_userId_userName[j][1]:
                    # print(res_visitAnalysis['data'][i])
                    # print(res_visitAnalysis['data'][i][iResField])


                    if iResField != None:

                        # sql = str(sql).replace("$id", str(db_t_userId_userName[j][1])).replace("$startTime", str(startTime)).replace("$endTime", str(endTime))
                        # print(str(sql))
                        # plannedVisitsNumber = Mysql_PO.execQuery(sql)
                        if Str_PO.getRepeatCount(sql, "%s") == 1:
                            plannedVisitsNumber = Mysql_PO.execQuery(sql % (db_t_userId_userName[j][1]))
                        elif Str_PO.getRepeatCount(sql, "%s") == 3:
                            plannedVisitsNumber = Mysql_PO.execQuery(sql % (db_t_userId_userName[j][1], startTime, endTime))
                        # print(plannedVisitsNumber[0][0])

                        if res_visitAnalysis['data'][i][iResField] == plannedVisitsNumber[0][0]:

                            # print("表格,写入每个用户")
                            # print(db_t_userId_userName[j][2])  # 钮学彬
                            Openpyxl_PO.setCellValue(currRow, 2, db_t_userId_userName[j][2], varSheet)  # 第一行第四列写入代表名字
                            Openpyxl_PO.setCellValue(currRow, currCol, plannedVisitsNumber[0][0], varSheet)
                        else:
                            Openpyxl_PO.setCellValue(currRow, 2, db_t_userId_userName[j][2], varSheet)  # 第一行第四列写入代表名字
                            Openpyxl_PO.setCellValue(currRow, currCol, str(plannedVisitsNumber[0][0]) + "(sql)/" + str(res_visitAnalysis['data'][i][iResField]) + "", varSheet)
                            Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                            sign = 1

                        if sign == 1:
                            Openpyxl_PO.setCellValue(currRow, 1, "error", varSheet)  # 第一行第四列写入代表名字
                            Openpyxl_PO.setCellColor(currRow, 1, "ff0000", varSheet)  # 错误标红色
                            sign = 0

                    currRow = currRow + 1
        Openpyxl_PO.save()



# 加载表格数据
from PO.OpenpyxlPO import *

Sys_PO.killPid('EXCEL.EXE')

Openpyxl_PO = OpenpyxlPO("i_erp_reportField_case.xlsx")
l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
for i in range(1, len(l_getRowValue_case)):
    if l_getRowValue_case[i][0] != "N":
        startTime = l_getRowValue_case[i][2]
        endTime = l_getRowValue_case[i][3]

        # 生成临时sheet
        varSheet = "temp"
        Openpyxl_PO.delSheet(varSheet)
        # varSheet = startTime[5:7] + startTime[8:10] + "-" + endTime[5:7] + endTime[8:10]
        Openpyxl_PO.addSheetCover(varSheet, 99)
        Openpyxl_PO.setRowValue({1: ["结果", "代表"]}, varSheet)


        # 获取拜访分析报表数据（接口）
        l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
        varSign1 = 0
        for j in range(1, len(l_getRowValue_i)):

            if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]: # "拜访分析报表":
                r = requests.post("http://192.168.0.238:8090" + l_getRowValue_i[j][2],
                                       headers={"content-type": "application/json", "token" : token, "traceId" : "123"},
                                       json={"endTime": endTime, "searchName": "", "starTime": startTime}, verify=False)
                str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                res_visitAnalysis = json.loads(str1)
                # print(res_visitAnalysis)
                l_getRowValue = (Openpyxl_PO.getRowValue(l_getRowValue_case[i][1]))


                varSign1 = 1
                break

        if varSign1 == 0:
            print("[warning], " + l_getRowValue_case[i][1] + " 没有对应的接口文档，程序已退出！")
            sys.exit(0)

        # print(l_getRowValue)
        for j in range(1, len(l_getRowValue)):
            if l_getRowValue[j][0] != "N":
                visitAnalysis(l_getRowValue[j][1], l_getRowValue[j][2], l_getRowValue[j][3])

        # excel导入数据库表
        Mysql_PO.xlsx2db("i_erp_reportField_case.xlsx", "12345", sheet_name="temp", index=True)

        # 生成report.html
        df = pd.read_sql(sql="select * from `12345`", con=Mysql_PO.getPymysqlEngine())
        pd.set_option('colheader_justify', 'center')  # 对其方式居中
        html = '''<html><head><title>''' + str("erp_" + l_getRowValue_case[i][1]) + '''</title></head>
        <body><b><caption>''' + str("erp_" + l_getRowValue_case[i][1]) + '''(''' + str(startTime) + ''' - ''' + str(endTime) +''')</caption></b><br><br>{table}</body></html>'''
        style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
        rptNameDate = "report/" + str("erp_" + l_getRowValue_case[i][1]) + str(startTime) + "_" + str(endTime) + ".html"
        with open(rptNameDate, 'w') as f:
            f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))

        from bs4 import BeautifulSoup
        # 优化report.html, 去掉None、修改颜色
        html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
        html_text = str(html_text).replace("<td>None</td>", "<td></td>").replace("<td>error</td>", '<td bgcolor="#ed1941">Error</td>')

        # 另存为report.html
        tf = open(rptNameDate, 'w', encoding='utf-8')
        tf.write(str(html_text))
        tf.close()

        Openpyxl_PO.delSheet(varSheet)
        print("[done], " + str(rptNameDate))

        Sys_PO.openFile(rptNameDate)

Openpyxl_PO.open()