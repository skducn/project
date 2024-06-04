# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-3
# Description: 统计禅道工作日志
# 如统计 2023-2-1 到 2023-2-8 所有人的工作日志，生成zentao_daily.xlsx文档。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, platform, os

import pandas as pd

sys.path.append("../../../")

from PO.TimePO import *
Time_PO = TimePO()

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)

from PO.OpenpyxlPO import *


def getRecord(varStartDate, varEndDate, l_varWho):

    varEndDate = varEndDate + " 23:59:59"
    excelName = "zentao_daily.xlsx"
    sheetName = "禅道日报"

    # 创建文档
    if os.path.isfile(os.getcwd() + "/" + excelName):
        Openpyxl_PO = OpenpyxlPO(excelName)
        Openpyxl_PO.addCoverSheet(sheetName, 0)
    else:
        Openpyxl_PO = NewexcelPO(excelName,sheetName)

    # 获取人员的禅道日报记录，并保存到文档

    listall = []
    for j in range(len(l_varWho)):
        sql = "SELECT zt_user.realname AS '姓名', zt_project.`name` AS '项目', zt_module.`name` AS '模块', zt_task.`name` AS '任务', zt_task.desc AS '描述', " \
              "zt_effort.consumed AS '工时', zt_task.finishedDate AS '完成时间' FROM zt_task INNER JOIN zt_project ON zt_task.project = zt_project.id INNER JOIN " \
              "zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story LEFT JOIN zt_module ON zt_task.module = zt_module.id " \
              "LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id WHERE zt_task.finishedDate BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' AND zt_effort.date BETWEEN  " \
              "'" + varStartDate + "' AND '" + varEndDate + "' AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 AND realname IN ('" + l_varWho[j] + "') ORDER BY " \
              "realname,finishedDate"
        # print(sql)
        tmpTuple = Mysql_PO.execQuery(sql)
        # print(tmpTuple)
        list1 = []
        list2 = []
        count = 1
        for i in tmpTuple:
            list1.append(str(i[0]))
            # list1.append(str(i[1]))
            list1.append(str(i[2]))
            list1.append(str(i[3]).replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<span>","").replace("</span>","").replace("<br />",""))
            list1.append(str(i[4]).replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<span>","").replace("</span>","").replace("\n\t","  ").
                         replace("\n\n","").replace("\n","").replace("<div>"," ").replace("</div>"," ")
                         .replace("</div>", "").replace('<span style="background-color:#FFFFFF;">', "")
                         .replace('<p class="MsoNormal">', "").replace('<p class="MsoNormal" style="margin-left:0pt;text-indent:0pt;background:#FFFFFF;">', "")
                         .replace('<p class="MsoNormal" style="text-indent:27pt;">', "")
                         .replace('<p class="MsoNormal" style="text-indent:36pt;">', "")
                         .replace('<p class="p" style="margin-left:0pt;text-indent:0pt;background:#FFFFFF;">', "")
                         .replace('<p class="MsoNormal" style="text-indent:40pt;">', "")
                         .replace('<p class="MsoNormal" style="text-indent:45pt;">', "")
                         .replace('<p class="MsoNormal" style="margin-left:0pt;text-indent:36pt;background:#FFFFFF;">',
                                  "")
                         .replace('<p class="MsoNormal" style="text-indent:72pt;">', "")
                         .replace('<p class="MsoNormal" style="text-indent:36pt;background:#FFFFFF;">', "")
                         .replace('<p class="MsoNormal" style="text-indent:72pt;background:#FFFFFF;">', "")
                         .replace('<p style="background-color:#FFFFFF;">', "")
                         )
            list1.append(str(i[5]))
            list1.append(str(i[6]))
            list2.append(list1)
            list1 = []
            count = count + 1
        # print(list2)
        for k in range(len(list2)):
            listall.append(list2[k])
    # print(listall)
    # sys.exit(0)
    d2 = dict(enumerate(listall, start=2))
    # print(d2)
    for k, v in d2.items():
        print(v[0], v[1], v[3], v[4].replace("<div>", "").replace("\n\n", "").replace("\n\n\n", "")
              .replace("</div>", "").replace('<span style="background-color:#FFFFFF;">', "")
              .replace('<p class="MsoNormal">', "").replace('<p class="MsoNormal" style="margin-left:0pt;text-indent:0pt;background:#FFFFFF;">',"")
              .replace('<p class="MsoNormal" style="text-indent:27pt;">',"")
              .replace('<p class="MsoNormal" style="text-indent:36pt;">',"")
              .replace('<p class="p" style="margin-left:0pt;text-indent:0pt;background:#FFFFFF;">',"")
              .replace('<p class="MsoNormal" style="text-indent:40pt;">',"")
              .replace('<p class="MsoNormal" style="text-indent:45pt;">',"")
              .replace('<p class="MsoNormal" style="margin-left:0pt;text-indent:36pt;background:#FFFFFF;">',"")
              .replace('<p class="MsoNormal" style="text-indent:72pt;">',"")
              .replace('<p class="MsoNormal" style="text-indent:36pt;background:#FFFFFF;">',"")
              .replace('<p class="MsoNormal" style="text-indent:72pt;background:#FFFFFF;">',"")
              .replace('<p style="background-color:#FFFFFF;">',"")
              .replace('\n\t\n\t',"")
              .replace('<div>\n\t', ""))
        # print(v)

    # Openpyxl_PO.insertRows({1: ["姓名", "项目", "模块", "标题", "描述", "工时", "完成日期"]}, sheetName)
    Openpyxl_PO.insertRows({1: ["姓名", "项目", "标题", "描述", "工时", "完成日期"]}, sheetName)
    Openpyxl_PO.setRows(d2, sheetName)
    Openpyxl_PO.save()

    df = pd.read_excel(excelName)

    # print(excelName + " 生成中，请稍等...")
    # if platform.system() == 'Darwin':
    #     os.system("open " + excelName)
    # if platform.system() == 'Windows':
    #     os.system("start " + excelName)

    return df


# 生成4-7到4-8两天的工作日志
# df = getRecord("2024-5-24", "2024-5-30", ['金浩'])
# getRecord("2024-5-24", "2024-5-30", ['郭斐'])
# getRecord("2024-5-24", "2024-5-30", ['陈晓东'])
# getRecord("2024-5-24", "2024-5-30", ['舒阳阳'])
df = getRecord("2024-5-1", "2024-5-30", ['郭斐','刘炳龙','舒阳阳'])


title = "工作日志"
filePrefix = "abc"
pd.set_option('colheader_justify', 'center')  # 对其方式居中
html = '''<html><head><title>''' + str(title) + '''</title></head>
  <body><b><caption>''' + str(title) + '''_''' + str(
    Time_PO.getDate()) + '''</caption></b><br><br>{table}</body></html>'''
style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;border-collapse: collapse;border: 1px solid silver;}.mystyle td, 
th {padding: 5px;}.mystyle tr:nth-child(even) {background: #E0E0E0;}.mystyle tr:hover {background: silver;cursor:pointer;}</style>'''
rptNameDate = "report/" + str(filePrefix) + str(Time_PO.getDate()) + ".html"
with open(rptNameDate, 'w') as f:
    f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
