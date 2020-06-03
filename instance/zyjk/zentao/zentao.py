# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-6-3
# Description: 从禅道中导出测试组所有人任务
# *****************************************************************

import os, sys
# sys.path.append("../../../../")
# from instance.zyjk.BI.PageObject.BiPO import *

from PO.TimePO import *
Time_PO = TimePO()
from PO.FilePO import *
File_PO = FilePO()
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.201", "root1", "123456", "zentao", 3306)  # 测试数据库
row, col = Excel_PO.getRowCol("zentao.xlsx", "daily")
# print(row, col)


varStartDate = str(Time_PO.get_day_of_day(-1))
varEndDate = varStartDate + " 23:59:59"
# print(varStartDate)
# print(varEndDate)


Mysql_PO.cur.execute("SELECT zt_user.realname AS '姓名', zt_project.`name` AS '项目', zt_module.`name` AS '模块', zt_task.`name` AS '任务', zt_task.desc AS '描述', zt_effort.consumed AS '工时', zt_task.finishedDate AS '完成时间' FROM zt_task INNER JOIN zt_project ON zt_task.project = zt_project.id INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story LEFT JOIN zt_module ON zt_task.module = zt_module.id LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id WHERE zt_task.finishedDate BETWEEN '%s' AND '%s' AND zt_effort.date BETWEEN  '%s' AND '%s' AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 AND realname IN ('胡小寒','赵云','陈晓东','舒阳阳')ORDER BY realname,finishedDate" % (varStartDate, varEndDate, varStartDate, varEndDate))
tmpTuple = Mysql_PO.cur.fetchall()
list1 = []
list2 = []
count = 1
for i in tmpTuple:
    # print(str(i[0]) + " , " + str(i[1]) + " ," + str(i[2]) + " , " + str(i[3]).replace("<p>","").replace("</p>","") + ", " + str(i[4]).replace("<p>","").replace("</p>","") + ", " + str(i[5]) + ", " + str(i[6]))
    list1.append(row+count)
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

# print(list2)
Excel_PO.writeXlsxByMore("zentao.xlsx", "daily", list2)
print("end")


