# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-11-11
# Description: 统计禅道人员上月的项目工时合计
# 思路：数据库里获取所有人所有项目工时合计，获取工时统计表项目与姓名，插入数据。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, platform,os
sys.path.append("../../../")
from time import sleep
from PO.TimePO import *
Time_PO = TimePO()
from PO.FilePO import *
File_PO = FilePO()
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)  # 测试数据库


l_project = Excel_PO.getRowValue("工时统计表.xlsx", 4)
# print(l_project)
for i in l_project:
    if i == "":
        l_project.remove(i)
l_project.pop(0)
l_project.pop(0)
# print(l_project)



# 获取上一工作日
for i in range(11):
    varStartDate = str(Time_PO.get_day_of_day(-1-i))
    if cal.is_working_day(date(int(varStartDate.split("-")[0]), int(varStartDate.split("-")[1]), int(varStartDate.split("-")[2]))):
        break
varEndDate = varStartDate + " 23:59:59"


# 获取人员名单位置
l_name = (Excel_PO.getColValue("工时统计表.xlsx", 1))
name = "赵云"
for k in range(len(l_name)):
    if name == l_name[k]:
        nameXY = k

# 获取人员的任务清单
Mysql_PO.cur.execute("select distinct(b.`项目`),sum(b.`工时`) as 工时 from (SELECT zt_project.`name` AS '项目', zt_effort.consumed AS '工时', zt_task.finishedDate AS '完成时间' FROM zt_task INNER JOIN zt_project ON zt_task.project = zt_project.id INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story LEFT JOIN zt_module ON zt_task.module = zt_module.id LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id WHERE zt_task.finishedDate BETWEEN '2020-10-1' AND '2020-10-31 23:59:59' AND zt_effort.date BETWEEN '2020-10-1' AND '2020-10-31 23:59:59' AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 AND realname IN ('%s') ORDER BY realname,finishedDate) as b group by b.`项目` " % (name))
tmpTuple = Mysql_PO.cur.fetchall()

for i in range(len(tmpTuple)):
    for j in range(len(l_project)):

            if tmpTuple[i][0] == "测试日常工作" and l_project[j] == "会议、学习、培训":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "电子健康档案数据管理平台产品研发项目" and l_project[j] == "电子健康档案产品研发":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "PIM-招远市妇幼" and l_project[j] == "招远妇幼保健":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] in l_project[j]:
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY+1, j+4, tmpTuple[i][1])

            if tmpTuple[i][0] == "PIM白茅岭产品迭代" and l_project[j] == "PIM-白茅岭":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "家床-金山石化社区" and l_project[j] == "金山石化家庭病床":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "普陀区中心医院远程心电项目" and l_project[j] == "普陀区中心医院心电项目":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "佛山家庭病床项目" and l_project[j] == "佛山第一人民医院家庭病床项目":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "家床-宝山7家家床" and l_project[j] == "家庭病床迭代":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "家庭病床产品研发项目" and l_project[j] == "家庭病床迭代":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])

            if tmpTuple[i][0] == "PIM军天湖项目" and l_project[j] == "PIM-白茅岭":
                Excel_PO.writeXlsx("工时统计表.xlsx", "工时统计", nameXY + 1, j + 4, tmpTuple[i][1])



if platform.system() == 'Darwin':
    os.system("open 工时统计表.xlsx")
if platform.system() == 'Windows':
    os.system("start 工时统计表.xlsx")

