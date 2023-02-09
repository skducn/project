# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-3
# Description: 统计禅道中测试人员某个时间段的记录，如统计 2023-2-1 到 2023-2-8 所有人的记录，生成 zentao_daily.xlsx文档。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


import sys, platform,os
sys.path.append("../../../")

from time import sleep

from PO.TimePO import *
Time_PO = TimePO()

from PO.FilePO import *
File_PO = FilePO()

from PO.StrPO import *
Str_PO = StrPO()

from PO.SysPO import *
Sys_PO = SysPO()
Sys_PO.closeApp('EXCEL.EXE')

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)

from PO.OpenpyxlPO import *

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# todo 配置参数

# 统计人员
varJinhao = '金浩'
varShuyangyang = '舒阳阳'
varWanggang = '汪刚'
varChenxiaodong = '陈晓东'
varGuohaojie = '郭浩杰'
varGuofei = '郭斐'
varLiubinlong = '刘斌龙'

# 统计日期
# varStartDate = "2023-02-01"
varStartDate = Time_PO.getDateByMinusPeriod(-1)
# varEndDate = "2023-02-08  23:59:59"
varEndDate = Time_PO.getDateByMinus() + " 23:59:59"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

excelName = "zentao_daily.xlsx"
excelSheet = str(varStartDate) + "_" + Time_PO.getDateByMinus()


# 如果文档不存在，自动创建
if os.path.isfile(os.getcwd() + "\\" + excelName):
    Openpyxl_PO = OpenpyxlPO(excelName)
    Openpyxl_PO.addSheetCover(excelSheet, 0)
else:
    Openpyxl_PO = OpenpyxlPO('')
    Openpyxl_PO.newExcel(excelName, excelSheet)


# 获取人员的禅道日报记录，并保存到文档
Mysql_PO.cur.execute("SELECT zt_user.realname AS '姓名', zt_project.`name` AS '项目', zt_module.`name` AS '模块', zt_task.`name` AS '任务', zt_task.desc AS '描述', zt_effort.consumed AS '工时', zt_task.finishedDate AS '完成时间' FROM zt_task INNER JOIN zt_project ON zt_task.project = zt_project.id INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story LEFT JOIN zt_module ON zt_task.module = zt_module.id LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id WHERE zt_task.finishedDate BETWEEN '%s' AND '%s' AND zt_effort.date BETWEEN  '%s' AND '%s' AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 AND realname IN ('%s','%s','%s','%s','%s','%s','%s')ORDER BY realname,finishedDate" % (varStartDate, varEndDate, varStartDate, varEndDate, varJinhao,varShuyangyang,varWanggang,varChenxiaodong,varGuohaojie,varGuofei,varLiubinlong))
tmpTuple = Mysql_PO.cur.fetchall()
list1 = []
list2 = []
count = 1
# l_rowcol = Openpyxl_PO.getRowCol(excelSheet)
for i in tmpTuple:
    # print(str(i[0]) + " , " + str(i[1]) + " ," + str(i[2]) + " , " + str(i[3]).replace("<p>","").replace("</p>","") + ", " + str(i[4]).replace("<p>","").replace("</p>","") + ", " + str(i[5]) + ", " + str(i[6]))
    # list1.append(l_rowcol[0]+count)
    list1.append(str(i[0]))
    list1.append(str(i[1]))
    list1.append(str(i[2]))
    list1.append(str(i[3]).replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<span>","").replace("</span>","").replace("<br />",""))
    list1.append(str(i[4]).replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<span>","").replace("</span>","").replace("<br />",""))
    list1.append(str(i[5]))
    list1.append(str(i[6]))
    list2.append(list1)
    list1 = []
    count = count + 1

Openpyxl_PO.setRowValue({1: ["姓名", "项目", "模块", "标题", "描述", "工时", "完成日期", "评审意见"]}, excelSheet)
Openpyxl_PO.addOnRowValue(list2, excelSheet)
Openpyxl_PO.save()



print("\n文档 " + excelName + " 打开中，请稍等...")
if platform.system() == 'Darwin':
    os.system("open " + excelName)
if platform.system() == 'Windows':
    os.system("start " + excelName)

