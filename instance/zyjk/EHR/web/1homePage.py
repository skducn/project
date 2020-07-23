# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-7-23
# Description: 电子健康档案数据监控中心（PC端）之 首页
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# https://npm.taobao.org/mirrors/chromedriver  chrome驱动 , C:\Python38\Scripts\chromedrive.exe
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

dataMonitor_PO.login("test", "Qa@123456")
dataMonitor_PO.clickMenu("首页")
l_text = dataMonitor_PO.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容


overallIndex = "[总体指标分布]"
l_overallIndex = l_text[0].split("总体指标分布\n")[1].split("\n更新档案总数(份)")[0]
l_overallIndex = l_overallIndex.split('\n')
Color_PO.consoleColor("31", "36", l_overallIndex.pop(0), "\n")  # 数据更新截止至时间：2020年07月15日
l_overallIndex.append("更新档案总数(份)")
d_overallIndex = (List_PO.list2dictBySerial(l_overallIndex))
d_overallIndex = {value: key for key, value in d_overallIndex.items()}
Color_PO.consoleColor("31", "31", overallIndex, "")  # [总体指标分布]
print(d_overallIndex)  # {'常住人口(人)': '111111', '户籍人口(人)': '1212', '目标建档总数(份)': '83334', '问题档案数量(份)': '20000', '更新档案总数(份)': '0'}
l_overallIndex2 = l_text[0].split("更新档案总数(份)\n")[1].split("\n电子健康档案分布图")[0]
l_overallIndex2 = l_overallIndex2.split('\n')
d_overallIndex2 = (List_PO.list2dictBySerial(l_overallIndex2))
del d_overallIndex2["标准"]
d_overallIndex2 = {value: key for key, value in d_overallIndex2.items()}
print(d_overallIndex2)  # {'户籍人口占比': '1.09%', '实际建档率': '18%', '问题档案占比': '100%', '档案更新率': '0%'}


ehrMap = "\n[电子健康档案分布图]"
Color_PO.consoleColor("31", "31", ehrMap, "")  # [电子健康档案分布图]
l_ehrMap = l_text[0].split("家庭医生团队分布\n")[1].split("\n前往页")[0]
l_ehrMap = l_ehrMap.split('\n')
l_ehrMap.pop(-1)
print(List_PO.listSplitSubList(l_ehrMap, 4)) # [['团队', '建档数量(份)', '问题档案数量(份）', '问题档案占比'], ['王敬丽团队', '1959', '1959', '100.00%'], ['周坤团队', '1754', '1754', '100.00%'], ['中心团队', '1116', '1116', '100.00%'], ['郁红娟团队', '955', '955', '100.00%'], ['严慧艳团队', '945', '945', '100.00%'], ['12']]


signDoctor = "\n[签约医生分布]"
Color_PO.consoleColor("31", "31", signDoctor, "")  # [签约医生分布]
l_signDoctor = l_text[0].split("问题统计列表\n")[1].split("\n前往页")[0]
l_signDoctor = l_signDoctor.split('\n')
l_signDoctor.pop(-1)
print(List_PO.listSplitSubList(l_signDoctor, 6))


age = "\n[年龄分布]"
Color_PO.consoleColor("31", "31", age, "")  # [年龄分布]
l_age = l_text[0].split("年龄分布\n")[1].split("\n前往页")[0]
l_age = l_age.split('\n')
l_age.pop(-1)
print(List_PO.listSplitSubList(l_age, 4))  # [['年龄', '建档数量(份)', '问题档案数量(份)', '问题档案占比'], ['7-64岁', '12727', '12727', '100.00%'], ['65岁以上', '4496', '4496', '100.00%'], ['0-6岁', '2776', '2776', '100.00%']]


sickness = "\n[疾病分布]"
Color_PO.consoleColor("31", "31", sickness, "")  # [疾病分布]
l_sickness = l_text[0].split("疾病分布\n")[1].split("\n前往页")[0]
l_sickness = l_sickness.split('\n')
l_sickness.pop(-1)
print(List_PO.listSplitSubList(l_sickness, 4))  # [['疾病', '建档数量(份)', '问题档案数量(份)', '问题档案占比']]


particularPersons = "\n[特殊人群分布]"
Color_PO.consoleColor("31", "31", particularPersons, "")  # [特殊人群分布]
l_particularPersons = l_text[0].split("特殊人群分布\n")[1].split("\n前往页")[0]
l_particularPersons = l_particularPersons.split('\n')
l_particularPersons.pop(-1)
print(List_PO.listSplitSubList(l_particularPersons, 4))  # [['疾病', '建档数量(份)', '问题档案数量(份)', '问题档案占比']]

