# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-3
# Description: 统计禅道中测试人员上一工作日的任务。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, platform,os
sys.path.append("../../../")
from time import sleep
from PO.TimePO import *
Time_PO = TimePO()
from PO.FilePO import *
File_PO = FilePO()
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)


from PO.OpenpyxlPO import *
excelName = "禅道每日审查_测试.xlsx"
excelSheet = "每日禅道审查"
Openpyxl_PO = OpenpyxlPO(excelName)
Openpyxl_PO.closeExcelPid('EXCEL.EXE')   # 关闭所有打开的excel


# 获取上一工作日
l_rowcol = Openpyxl_PO.l_getTotalRowCol(excelSheet)
for i in range(11):
    varStartDate = str(Time_PO.get_day_of_day(-1-i))
    if cal.is_working_day(date(int(varStartDate.split("-")[0]), int(varStartDate.split("-")[1]), int(varStartDate.split("-")[2]))):
        break
varEndDate = varStartDate + " 23:59:59"


# 获取人员的任务清单
Mysql_PO.cur.execute("SELECT zt_user.realname AS '姓名', zt_project.`name` AS '项目', zt_module.`name` AS '模块', zt_task.`name` AS '任务', zt_task.desc AS '描述', zt_effort.consumed AS '工时', zt_task.finishedDate AS '完成时间' FROM zt_task INNER JOIN zt_project ON zt_task.project = zt_project.id INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story LEFT JOIN zt_module ON zt_task.module = zt_module.id LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id WHERE zt_task.finishedDate BETWEEN '%s' AND '%s' AND zt_effort.date BETWEEN  '%s' AND '%s' AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 AND realname IN ('金浩','赵云','陈晓东','舒阳阳')ORDER BY realname,finishedDate" % (varStartDate, varEndDate, varStartDate, varEndDate))
tmpTuple = Mysql_PO.cur.fetchall()
list1 = []
list2 = []
count = 1
for i in tmpTuple:
    # print(str(i[0]) + " , " + str(i[1]) + " ," + str(i[2]) + " , " + str(i[3]).replace("<p>","").replace("</p>","") + ", " + str(i[4]).replace("<p>","").replace("</p>","") + ", " + str(i[5]) + ", " + str(i[6]))
    list1.append(l_rowcol[0]+count)
    list1.append(str(i[0]))
    list1.append(str(i[1]))
    list1.append(str(i[2]))
    list1.append(str(i[3]).replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<span>","").replace("</span>","").replace("<br />",""))
    list1.append(str(i[4]).replace("<p>","").replace("</p>","").replace("&nbsp;","").replace("<span>","").replace("</span>","").replace("<br />",""))
    list1.append(str(i[5]))
    list1.append(str(i[6]))
    list1.append("正常")
    list2.append(list1)
    list1 = []
    count = count + 1


Openpyxl_PO.setMoreCellValue(list2, excelSheet)
Openpyxl_PO.save()
print("\n成功导出" + str(varStartDate) + "的任务清单，请稍等...")

if platform.system() == 'Darwin':
    os.system("open " + excelName)
if platform.system() == 'Windows':
    os.system("start " + excelName)

