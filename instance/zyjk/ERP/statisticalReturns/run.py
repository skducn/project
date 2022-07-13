# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-6-30
# Description: erp - 统计报表 - 拜访分析报表
# 接口文档：http://192.168.0.238:8090/doc.html
#***************************************************************


import requests, json
import urllib3, math
urllib3.disable_warnings()

from PO.StrPO import *
Str_PO = StrPO()

from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
Data_PO = DataPO()

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


# 所有地区经理和代表的id
db_t_userId_userName = Mysql_PO_OA.execQuery("select BYNAME, UID, USER_NAME from `user` where NOT_LOGIN=0 AND USER_PRIV_NAME='地区经理' or USER_PRIV_NAME='医药代表'")
print(db_t_userId_userName)  # (('niuxuebin', 81, '钮学彬'), ('huangxinhui', 84, '黄新晖'),


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
# print(token)
# sys.exit(0)

d = {}
d_field = {}


def reportAnalysis(tbl_report, tblField, iResField, sql, d_tbl_param):

    # visitAnalysis( "计划拜访人次", "plannedVisitsNumber", "sql", {"endTime": "2022-06-30  23:59:59", "startTime": "2022-06-01", "uid": 0})
    sign = 0

    l_rowcol= Openpyxl_PO.getRowCol(varSheet)
    currCol = l_rowcol[1]+1
    currRow = 2
    Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)

    print(tblField)


    if iResField != None and sql == None:
        pass

    elif iResField != None and "%s" in sql:

        # 遍历所有人的字段值
        s = 0
        for i in range(len(res_visitAnalysis['data']['detail'])):
            # print(res_visitAnalysis['data']['detail'][i]) # {'delegateId': 84, 'managerName': '廖荣平', 'representativeName': '黄新晖', 'plannedVisitsNumber': 0, 'actualVisitsNumber': 0, 'actualVisitsPersonNumber': 0, 'actualVisitRate': 0, 'twoACustomerVisitNumber': 0, 'twoACustomerVisitRate': 0, 'highPotentialCustomerVisitNumber': 0, 'highPotentialCustomerVisitRate': 0, 'newAddCustomerNumber': 0, 'allNumber': 0, 'actualVisitCoverRate': 0, 'doubleTotal': 0, 'potentialityTotal': 0, 'plannedMeetingFollowNumber': 0, 'actualMeetingFollowNumber': 0, 'actualConcludeMeetingFollowNumber': 0, 'actualConcludeDoubleANumber': 0, 'actualConcludePotentialityNumber': 0, 'doubleARatioRate': 0, 'doubleAFrequencyRate': 0, 'highRatioRate': 0, 'highFrequencyRate': 0, 'meetingFollowRate': 0, 'locationMatchNumber': 0}

            if tbl_report == "拜访分析报表":
                if Str_PO.getRepeatCount(sql, "%s") == 1:
                    sql_value = Mysql_PO.execQuery(sql % (res_visitAnalysis['data']['detail'][i]['delegateId']))
                elif Str_PO.getRepeatCount(sql, "%s") == 3:
                    sql_value = Mysql_PO.execQuery(sql % (res_visitAnalysis['data']['detail'][i]['delegateId'], d_tbl_param["starTime"], d_tbl_param["endTime"]))
                    # print(sql_value)
                if len(sql_value) == 0:
                # if sql_value[0][0] == None:
                    sql_value = 0
                else:
                    sql_value = sql_value[0][0]

                # 接口和sql比对
                if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                    s = s + sql_value

                    Openpyxl_PO.setCellValue(currRow, 2, res_visitAnalysis['data']['detail'][i]['representativeName'] + "(" + str(res_visitAnalysis['data']['detail'][i]['delegateId']) + ")", varSheet)  # 第二列代表名字
                    Openpyxl_PO.setCellValue(currRow, currCol, sql_value, varSheet)  # 指标值
                else:
                    Openpyxl_PO.setCellValue(currRow, 2, res_visitAnalysis['data']['detail'][i]['representativeName'] + "(" + str(res_visitAnalysis['data']['detail'][i]['delegateId']) + ")", varSheet)
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                    sign = 1


            elif tbl_report == "协访分析":
                sql_value = Mysql_PO.execQuery(sql % (res_visitAnalysis['data']['detail'][i]['uid'], d_tbl_param["startTime"], d_tbl_param["endTime"]))
                # print(sql_value)
                if sql_value[0][0] == None:
                    sql_value = 0
                else:
                    sql_value = sql_value[0][0]

                # 接口和sql比对
                if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                    Openpyxl_PO.setCellValue(currRow, 2, res_visitAnalysis['data']['detail'][i]['userName'] + "(" + str(res_visitAnalysis['data']['detail'][i]['uid']) + ")", varSheet)
                    Openpyxl_PO.setCellValue(currRow, currCol, sql_value, varSheet)  # 指标值
                else:
                    Openpyxl_PO.setCellValue(currRow, 2, res_visitAnalysis['data']['detail'][i]['userName'] + "(" + str(res_visitAnalysis['data']['detail'][i]['uid']) + ")", varSheet)
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                    sign = 1

            if sign == 1:
                Openpyxl_PO.setCellValue(currRow, 1, "error", varSheet)
                Openpyxl_PO.setCellColor(currRow, 1, "ff0000", varSheet)
                sign = 0

            currRow = currRow + 1
            d[iResField] = s
        Openpyxl_PO.save()

        # print(d)

    else:
        # 各比率的计算

        for i in range(len(res_visitAnalysis['data']['detail'])):
            if res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0 :
                Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
            else:
                tmp1 = Data_PO.newRound(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] / res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100)
                if tmp1 == int(res_visitAnalysis['data']['detail'][i][iResField]):
                    Openpyxl_PO.setCellValue(currRow, currCol, str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

            currRow = currRow + 1
        Openpyxl_PO.save()

    # 合计
    # print(res_visitAnalysis['data']['total'])
    Openpyxl_PO.setCellValue(currRow, 2, "总计", varSheet)  # 第二列代表名字

    if iResField in d:
        if d[iResField] == res_visitAnalysis['data']['total'][iResField]:
            Openpyxl_PO.setCellValue(currRow, currCol, res_visitAnalysis['data']['total'][iResField], varSheet)
        else:
            Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算)/" + str(res_visitAnalysis['data']['total'][iResField]), varSheet)
            Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
    else:
        if sql != None:
            if res_visitAnalysis['data']['total'][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['total'][sql.split("/")[0]] == 0:
                Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
            else:
                tmp = Data_PO.newRound(res_visitAnalysis['data']['total'][sql.split("/")[0]] / res_visitAnalysis['data']['total'][sql.split("/")[1]] * 100)
                # print(tmp)
                if tmp == int(res_visitAnalysis['data']['total'][iResField]):
                    Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%", varSheet)
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%(计算)/" + str(int(res_visitAnalysis['data']['total'][iResField])) + "%", varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
    Openpyxl_PO.save()
# ------------------------------------------------------------------------------------------------------------------------

# 加载表格数据，读取测试用例
from PO.OpenpyxlPO import *
Sys_PO.killPid('EXCEL.EXE')
Openpyxl_PO = OpenpyxlPO("i_erp_reportField_case.xlsx")
l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))

# 生成临时sheet
varSheet = "temp"
Openpyxl_PO.delSheet(varSheet)
Openpyxl_PO.addSheetCover(varSheet, 99)
Openpyxl_PO.setRowValue({1: ["结果", "代表（id）"]}, varSheet)

# 获取default（接口）
l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))

for i in range(1, len(l_getRowValue_case)):
    if l_getRowValue_case[i][0] != "N":
        tbl_report = l_getRowValue_case[i][1]  # 报表
        d_tbl_param = Str_PO.str2dict(l_getRowValue_case[i][2])  # 参数2字典

        # 遍历参数
        varSign1 = 0
        for j in range(1, len(l_getRowValue_i)):
            # summary
            if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                # paths
                r = requests.post("http://192.168.0.238:8090" + l_getRowValue_i[j][2],
                                       headers={"content-type": "application/json", "token" : token, "traceId" : "123"},
                                       json=d_tbl_param, verify=False)
                str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                res_visitAnalysis = json.loads(str1)
                l_getRowValue = (Openpyxl_PO.getRowValue(tbl_report))
                varSign1 = 1
                break

        if varSign1 == 0:
            print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
            sys.exit(0)

        # print(l_getRowValue)
        print(("erp_" + tbl_report + str(l_getRowValue_case[i][4])).center(100, "-"))

        for j in range(1, len(l_getRowValue)):
            if l_getRowValue[j][0] != "N":
                reportAnalysis(tbl_report, l_getRowValue[j][1], l_getRowValue[j][2], l_getRowValue[j][3], d_tbl_param)


        # excel导入数据库表
        Mysql_PO.xlsx2db("i_erp_reportField_case.xlsx", "12345", sheet_name="temp", index=True)


        # 生成report.html
        df = pd.read_sql(sql="select * from `12345`", con=Mysql_PO.getPymysqlEngine())
        pd.set_option('colheader_justify', 'center')  # 对其方式居中
        html = '''<html><head><title>''' + str("erp_" + tbl_report) + '''</title></head>
        <body><b><caption>''' + str("erp_" + tbl_report) + '''(''' + str(l_getRowValue_case[i][4])  + ''') 更新于 ''' + str(Time_PO.getDateTimeByDivide()) + '''</caption></b><br><br>{table}</body></html>'''
        style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
        rptNameDate = "report/" + str("erp_" + tbl_report) + "_" + str(l_getRowValue_case[i][4]) + ".html"
        with open(rptNameDate, 'w') as f:
            f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        from bs4 import BeautifulSoup
        # 优化report.html, 去掉None、修改颜色
        html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
        html_text = str(html_text).replace("<td>None</td>", "<td></td>").replace("<td>error</td>", '<td bgcolor="#ed1941">error</td>')

        # 另存为report.html
        tf = open(rptNameDate, 'w', encoding='utf-8')
        tf.write(str(html_text))
        tf.close()

        # Openpyxl_PO.delSheet(varSheet)
        print("[done], " + str(rptNameDate))

        Sys_PO.openFile(rptNameDate)

Openpyxl_PO.open()