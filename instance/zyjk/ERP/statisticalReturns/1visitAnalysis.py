# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-6-30
# Description: erp - 统计报表 - 拜访分析报表
# 测试：
# 接口文档：http://192.168.0.238:8090/doc.html
# 数据库：192.168.0.238
# 预发布：
# 接口文档：http://192.168.0.245:8080/doc.html
# 数据库：192.168.0.244
#***************************************************************

import requests, json
import urllib3, math
urllib3.disable_warnings()
from ErpPO import *
Erp_PO = ErpPO()
from PO.StrPO import *
Str_PO = StrPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
Data_PO = DataPO()
from PO.ListPO import *
List_PO = ListPO()
from PO.MysqlPO import *
from PO.OpenpyxlPO import *
Sys_PO.killPid('EXCEL.EXE')

caseExcel = "i_erp_reportField_case.xlsx"

# 预发布接口文档ip
iUrl = "http://192.168.0.245:8080"

# 预发布数据库ip
db_ip = "192.168.0.244"
Mysql_PO = MysqlPO(db_ip, "root", "ZAQ!2wsx", "crm", 3306)
Mysql_PO_OA = MysqlPO("192.168.0.65", "ceshi", "123456", "TD_OA", 3336)

# 获取所有地区经理和代表的id
db_t_userId_userName = Mysql_PO_OA.execQuery("select BYNAME, UID, USER_NAME from `user` where NOT_LOGIN=0 AND USER_PRIV_NAME='地区经理' or USER_PRIV_NAME='医药代表'")
# (('niuxuebin', 81, '钮学彬'), ('huangxinhui', 84, '黄新晖'),

# 获取token
token = Erp_PO.getToken()

d = {}
d_field = {}


def reportAnalysis(tbl_report, tblField, iResField, sql, d_tbl_param):

    # visitAnalysis( '拜访分析报表', "计划拜访人次", "plannedVisitsNumber", "sql", {"endTime": "2022-06-30  23:59:59", "startTime": "2022-06-01", "uid": 0})
    sign = 0
    sign2 = 0
    l_result = []

    l_rowcol = Openpyxl_PO.getRowCol(varSheet)
    # print(l_rowcol)
    currCol = l_rowcol[1] + 1
    # print(currCol)
    currRow = 2
    Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)
    # print(tblField)

    if iResField != None and sql == None:
        pass

    elif iResField != None and "%s" in sql:

        # 遍历所有人的字段值
        s = 0
        for i in range(len(res_visitAnalysis['data']['detail'])):
            # print(res_visitAnalysis['data']['detail'][i]) # {'delegateId': 84, 'managerName': '廖荣平', 'representativeName': '黄新晖', 'plannedVisitsNumber': 0, 'actualVisitsNumber': 0, 'actualVisitsPersonNumber': 0, 'actualVisitRate': 0, 'twoACustomerVisitNumber': 0, 'twoACustomerVisitRate': 0, 'highPotentialCustomerVisitNumber': 0, 'highPotentialCustomerVisitRate': 0, 'newAddCustomerNumber': 0, 'allNumber': 0, 'actualVisitCoverRate': 0, 'doubleTotal': 0, 'potentialityTotal': 0, 'plannedMeetingFollowNumber': 0, 'actualMeetingFollowNumber': 0, 'actualConcludeMeetingFollowNumber': 0, 'actualConcludeDoubleANumber': 0, 'actualConcludePotentialityNumber': 0, 'doubleARatioRate': 0, 'doubleAFrequencyRate': 0, 'highRatioRate': 0, 'highFrequencyRate': 0, 'meetingFollowRate': 0, 'locationMatchNumber': 0}

            if tbl_report == "拜访分析报表":
                if Str_PO.getRepeatCount(sql, "%s") == 1:
                    sql1 = sql % (res_visitAnalysis['data']['detail'][i]['delegateId'])
                elif Str_PO.getRepeatCount(sql, "%s") == 3:
                    sql1 = sql % (res_visitAnalysis['data']['detail'][i]['delegateId'], d_tbl_param["starTime"], d_tbl_param["endTime"])
                sql_value = Mysql_PO.execQuery(sql1)

                if len(sql_value) == 0:
                    sql_value = 0
                else:
                    if sql_value[0][0] == None:
                        sql_value = 0
                    else:
                        sql_value = sql_value[0][0]

                # 接口和sql比对
                s = s + sql_value
                Openpyxl_PO.setCellValue(currRow, 1, res_visitAnalysis['data']['detail'][i]['managerName'], varSheet)  # 第1列区域
                Openpyxl_PO.setCellValue(currRow, 2, res_visitAnalysis['data']['detail'][i]['representativeName'], varSheet)  # 第二列代表名字


            if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value), varSheet)  # 指标值
            else:
                Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

            currRow = currRow + 1
            d[iResField] = s

        Openpyxl_PO.save()


    else:
        # 各比率的计算

        for i in range(len(res_visitAnalysis['data']['detail'])):
            if res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0 :
                Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
            else:
                tmp1 = Data_PO.newRound(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] / res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100)
                if tmp1 == int(res_visitAnalysis['data']['detail'][i][iResField]):
                    Openpyxl_PO.setCellValue(currRow, currCol, str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                    # Openpyxl_PO.setCellValue(currRow, 1, "ok", varSheet)
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
            currRow = currRow + 1
        Openpyxl_PO.save()

    # 合计
    Openpyxl_PO.setCellValue(currRow, 1, "总计", varSheet)
    Openpyxl_PO.setCellValue(currRow, 2, "None", varSheet)


    if iResField in d:
        if d[iResField] == res_visitAnalysis['data']['total'][iResField]:
            Openpyxl_PO.setCellValue(currRow, currCol, str(res_visitAnalysis['data']['total'][iResField]), varSheet)
            # print(res_visitAnalysis['data']['total'][iResField])
        else:
            Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算1)/" + str(res_visitAnalysis['data']['total'][iResField]), varSheet)
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

def getBrowserData(varSheet):

    # 获取浏览器页面数据

    # 1，打开oa
    Erp_PO.login("http://192.168.0.65", "liuting", "")
    Erp_PO.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
    Erp_PO.maxBrowser(1)  # 全屏

    # 2，获取协访分析表字段与值
    Erp_PO.clickMemuERP("统计报表", "拜访分析报表")
    Erp_PO.zoom("20")  # 缩小页面20%便于抓取元素
    l_fieldValueArea = Erp_PO.Web_PO.getXpathsText("//tr")  # 获取数据
    l_fieldValueArea = List_PO.listBatchDel(l_fieldValueArea, "明细")
    l_fieldValueArea = List_PO.listBatchDel(l_fieldValueArea, "总计")
    l_fieldValueArea = List_PO.listBatchDel(l_fieldValueArea, "操作")
    l_fieldValueArea = List_PO.listBatchDel(l_fieldValueArea, "")

    l_fieldValue = List_PO.sliceList(l_fieldValueArea, '区域\n代表', 0)
    l_area = List_PO.sliceList(l_fieldValueArea, '区域\n代表', 1)
    l_area.insert(0, '区域\n代表')
    l_area.append('总计\nNone')

    # 3, 新建sheet
    Openpyxl_PO.delSheet(varSheet)
    Openpyxl_PO.addSheetCover(varSheet, 99)

    # 4, 将字段与值写入表格
    for i in range(len(l_fieldValue)):
        list3 = str(l_fieldValue[i]).split("\n")
        Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

    # 5, 将区域和代表插入表格
    Openpyxl_PO.insertCols(1, 2, varSheet)
    for i in range(len(l_area)):
        list4 = str(l_area[i]).split("\n")
        Openpyxl_PO.setRowValue({i + 1: list4}, varSheet)

    l_title = Openpyxl_PO.getOneRowValue(0, varSheet)
    # print(l_title)
    for i in range(len(l_title)):
        if l_title[i] == '拜访定位匹配人次':
            # print(i)
            Openpyxl_PO.delSeriesCol(i + 1, 10, varSheet)  # 删除第“拜访定位匹配人次”列及之后的所有列
            break

    Erp_PO.close()

def getResult(varSheet):

    # 对新表生成结果状态

    r = Openpyxl_PO.getRowCol(varSheet)[0]
    c = Openpyxl_PO.getRowCol(varSheet)[1]

    varSign = 0
    list11 = []
    for i in range(r):
        for j in range(c):
            if "/" in Openpyxl_PO.getCellValue(i + 1, j + 1, varSheet):
                varSign = 1
        if varSign == 1:
            list11.append("error")
        else:
            list11.append("ok")
        varSign = 0

    Openpyxl_PO.insertCols(1, 1, varSheet)
    Openpyxl_PO.setColValue({"A": list11}, varSheet)
    Openpyxl_PO.setCellValue(1, 1, "结果", varSheet)


# ------------------------------------------------------------------------------------------------------------------------
# [main]

Openpyxl_PO = OpenpyxlPO(caseExcel)

print("1，获取协访分析表接口数据")
l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
for i in range(1, len(l_getRowValue_case)):
    if l_getRowValue_case[i][0] != "N":
        tbl_report = l_getRowValue_case[i][1]  # 报表
        d_tbl_param = Str_PO.str2dict(l_getRowValue_case[i][2])  # 参数2字典
        varNowTime = str(Time_PO.getDateTime())
        varTitle = "erp_" + tbl_report + "(" + str(l_getRowValue_case[i][4]) + ")_" + db_ip + "_" + varNowTime

        # 生成临时sheet
        varSheet = "i"
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)
        Openpyxl_PO.setRowValue({1: ["区域", "代表"]}, varSheet)

        # 遍历参数
        varSign1 = 0
        # 获取default（接口）
        l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
        for j in range(1, len(l_getRowValue_i)):
            # summary
            if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                # paths
                r = requests.post(iUrl + l_getRowValue_i[j][2],
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

        for j in range(1, len(l_getRowValue)):
            if l_getRowValue[j][0] != "N":
                reportAnalysis(tbl_report, l_getRowValue[j][1], l_getRowValue[j][2], l_getRowValue[j][3], d_tbl_param)


        # 忽略“拜访定位匹配人次”及之后的字段
        l_title = Openpyxl_PO.getOneRowValue(0, varSheet)
        # print(l_title)
        for i in range(len(l_title)):
            if l_title[i] == '拜访定位匹配人次':
                # print(i)
                Openpyxl_PO.delSeriesCol(i+1, 10, varSheet)  # 删除第“拜访定位匹配人次”列及之后的所有列
                break
        Openpyxl_PO.save()

print("2，获取浏览器前端页面数据")
getBrowserData('b')

print("3，将i接口sheet与b浏览器数据sheet比对,生成新表i%b")
varNewSheet = Openpyxl_PO.setSheetByDiff("i", "b")

print("4，对新表生成结果状态")
getResult(varNewSheet)

print("5，excel导入数据库表")
Mysql_PO.xlsx2db(caseExcel, "12345", sheet_name=varNewSheet, index=True)

print("6，生成report.html")
Erp_PO.getReport(Mysql_PO, varTitle)


Openpyxl_PO.open()