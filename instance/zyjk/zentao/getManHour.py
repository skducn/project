# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-4-1
# Description: 统计测试组 云his、公卫、区域平台 3个平台的每月工时
# 【腾讯文档】项目工作量评估汇总表
# https://docs.qq.com/sheet/DYlBzQ0pnc0JySm9j?tab=7x18g7
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Color_PO.consoleColor2(
#     {"31": "30red", "31": "31red", "32": "32green", "33": "33yellow", "34": "34blue", "35": "35purple", "36": "36azure",
#      "37": "37grep", "38": "38white", "39": "39white",
#      "40": "40redBlack", "41": "41redred", "42": "42redGreen", "43": "43redYellow", "44": "44redBlue",
#      "45": "45redPurple", "46": "46redAzure", "47": "44redGrey"})


import calendar

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.211", "readonly", "benetech123", "zentaoep", 3306)

def getManHour(varYear, varMonth, varProject, var_l_who):
    sum = 0.0
    l1 = []

    # 获取月份最后一天
    s_lastDay = calendar.monthrange(varYear, varMonth)[1]
    varStartDate = str(varYear) + "-" + str(varMonth) + "-1"
    varEndDate = str(varYear) + "-" + str(varMonth) + "-" + str(s_lastDay)

    for i in range(len(var_l_who)):
        sql = "select sum(a.工时) as manHour " \
                "from ( SELECT zt_user.realname AS '姓名', zt_project.`name` AS '项目', zt_module.`name` AS '模块', " \
                "zt_task.`name` AS '任务', zt_task.desc AS '描述', zt_effort.consumed   AS '工时', zt_task.finishedDate AS '完成时间' "\
                "FROM zt_task "\
                "INNER JOIN zt_project ON zt_task.project = zt_project.id "\
                "INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story "\
                "LEFT JOIN zt_module ON zt_task.module = zt_module.id "\
                "LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id "\
                "WHERE zt_task.finishedDate BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' AND zt_effort.date BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' "\
                "AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 "\
                "AND zt_project.`name` = '" + varProject + "' "\
                "AND realname IN ('" + var_l_who[i] + "') "\
                "ORDER BY realname, finishedDate) as a"

        r = Mysql_PO.execQuery(sql)
        if r[0][0] != None:
            sum = sum + r[0][0]
        l1.append(var_l_who[i] + "(" + str(r[0][0]) + ")")
    # print(str(varMonth) + "月工时(" + varProject + ")" + "=> " + str(sum) + str(l1) + " => " + str((sum/8)) + "天 ")
    r = Color_PO.getColor({"31": str(varMonth) + "月工时(" + varProject + ")"}) + "=> " + str(sum) + str(l1) + " => " + Color_PO.getColor({"34": str((sum/8)) + "天 "})
    print(r)

def _getManHour(varYear, varMonth, varProject, var_l_who):
    sum = 0.0
    l1 = []
    sum2 = 0.0
    # 获取月份最后一天
    s_lastDay = calendar.monthrange(varYear, varMonth)[1]
    varStartDate = str(varYear) + "-" + str(varMonth) + "-1"
    varEndDate = str(varYear) + "-" + str(varMonth) + "-" + str(s_lastDay)

    for i in range(len(var_l_who)):
        sql = "select sum(a.工时) as manHour " \
                "from ( SELECT zt_user.realname AS '姓名', zt_project.`name` AS '项目', zt_module.`name` AS '模块', " \
                "zt_task.`name` AS '任务', zt_task.desc AS '描述', zt_effort.consumed   AS '工时', zt_task.finishedDate AS '完成时间' "\
                "FROM zt_task "\
                "INNER JOIN zt_project ON zt_task.project = zt_project.id "\
                "INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story "\
                "LEFT JOIN zt_module ON zt_task.module = zt_module.id "\
                "LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id "\
                "WHERE zt_task.finishedDate BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' AND zt_effort.date BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' "\
                "AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 "\
                "AND zt_project.`name` = '" + varProject + "' "\
                "AND realname IN ('" + var_l_who[i] + "') "\
                "ORDER BY realname, finishedDate) as a"

        r = Mysql_PO.execQuery(sql)
        if r[0][0] != None:
            sum = sum + r[0][0]
    r = Color_PO.getColor({"31": varProject}) + "=> " + str(sum) + Color_PO.getColor({"34": " (" + str((sum/8)) + "天" + ")"} )
    print(r)
    return sum



def getProject(varYear, varMonth, var_l_who):

    sum2 = 0
    # 获取月份最后一天
    s_lastDay = calendar.monthrange(varYear, varMonth)[1]
    varStartDate = str(varYear) + "-" + str(varMonth) + "-1"
    varEndDate = str(varYear) + "-" + str(varMonth) + "-" + str(s_lastDay)
    # todo print 2024-3-1 ~ 2024-3-31
    print(str(varMonth) + "月(" + varStartDate + " ~ " + varEndDate + ")工时明细")

    for i in range(len(var_l_who)):
        sql="SELECT DISTINCT zt_project.`name` FROM " \
            "zt_task INNER JOIN zt_project ON zt_task.project = zt_project.id INNER JOIN zt_user ON zt_task.finishedBy = zt_user.account AND zt_user.account = zt_task.story " \
            "LEFT JOIN zt_module ON zt_task.module = zt_module.id LEFT JOIN zt_effort ON zt_effort.objectID = zt_task.id " \
            "WHERE zt_task.finishedDate BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' AND zt_effort.date BETWEEN '" + varStartDate + "' AND '" + varEndDate + "' " \
            "AND zt_effort.objectType = 'task' AND zt_effort.account != 'admin' AND zt_effort.consumed > 0 AND realname IN ('" + var_l_who[i] + "') " \
            "group by zt_project.`name`" \
            "ORDER By realname, finishedDate"
        p = Mysql_PO.execQuery(sql)
        # print(str(var_l_who[i]) + " => " + str(p))
        # todo print 3月XXX
        print("-----------------------------------")
        print(str(var_l_who[i]))
        for j in range(len(p)):
            sum = _getManHour(varYear, varMonth, p[j][0], [var_l_who[i]])
            sum2 = sum2 + sum
        print("总工时：" + str(sum2))
        sum2 = 0


# todo 获取区域HIS的总工时
# getManHour(2024, 3, '区域HIS', ['郭浩杰', '陈晓东'])
# # 3月工时(区域HIS) => 324.0['郭浩杰(205.0)', '陈晓东(119.0)'] => 40.5天
#
#
# todo 获取3区域公共卫生管理系统的总工时
# getManHour(2024, 3, '区域公共卫生管理系统', ['郭浩杰', '陈晓东', '郭斐', '刘斌龙', '舒阳阳'])
# # 3月工时(区域公共卫生管理系统) => 409.0['郭浩杰(None)', '陈晓东(118.0)', '郭斐(113.0)', '刘斌龙(103.0)', '舒阳阳(75.0)'] => 51.125天


# todo 获取所有项目明细工时与总工时
getProject(2024, 4, ['郭浩杰', '陈晓东', '郭斐', '刘斌龙', '舒阳阳', '金浩'])
# 3月工时(电子健康档案数据管理平台产品研发项目2.0) => 3.0['刘斌龙(3.0)'] => 0.375天
# 3月工时(社区健康管理中心) => 52.0['刘斌龙(52.0)'] => 6.5天
# 3月工时(区域公共卫生管理系统) => 103.0['刘斌龙(103.0)'] => 12.875天
# 3月工时(智赢健康俱乐部) => 20.0['刘斌龙(20.0)'] => 2.5天

