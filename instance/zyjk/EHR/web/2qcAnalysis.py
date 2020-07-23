# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-11
# Description: 电子健康档案数据监控中心（PC端）之 质控分析
# 技巧：去掉字符串两端的数字， astring.strip(string.digits) ,如 123姓名，输出：姓名
# 扩展：astring.lstrip(string.digits) 去掉左侧数字  , astring.rstrip(string.digits) 去掉右侧数字
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import numpy
from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()
from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.CharPO import *
char_PO = CharPO()

dataMonitor_PO.login("test", "Qa@123456")
dataMonitor_PO.clickMenu("档案质控分析")
l_text = dataMonitor_PO.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容


qcOverall = "\n[档案质控总体情况]"
Color_PO.consoleColor("31", "31", qcOverall, "")  # [档案质控总体情况]
l_qcOverall = l_text[0].split("重置\n")[1].split("\n本页")[0]
l_qcOverall = l_qcOverall.split('\n')
print(l_qcOverall.pop(0))  # '质控时间 质控档案总数量 问题档案数量 规范建档率 操作'
print(List_PO.listSplitSubList(l_qcOverall, 6))  # [['2020-07-15', '20000', '20000', '0.00%', '详情', '规范建档率提升分析']]


problemList = "\n[问题档案列表]"
Color_PO.consoleColor("31", "31", problemList, "")  # [问题档案列表]
dataMonitor_PO.Web_PO.clickXpath("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[5]/div/div/div/button", 2)  # 点击第一条记录详情
l_text = dataMonitor_PO.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
l_problemList = l_text[0].split("问题档案列表\n")[1].split("\n操作")[0]
l_problemList = l_problemList.split('\n')
print(l_problemList)  # ['规则类型:', '规范性 (93.74%)', '完整性 (100.00%)', '一致性 (0.50%)', '有效性 (95.74%)']
l_problemList = l_text[0].split("错误描述\n")[1].split("\n选择当前页数显示")[0]
l_problemList = l_problemList.split('\n')
print(List_PO.listSplitSubList(l_problemList, 8)) # [['详情', '321881198007198529', '王娟', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '321923200007074011', '徐鹏程', '宝山区大场镇大场社区卫生服务中心', '封面表', '建档日期', '有效性', '建档日期填写不规范'], ['详情', '32210119490127322X', '王琦', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '322109197702162322', '黄丽红', '宝山区大场镇大场社区卫生服务中心', '封面表', '村（居）委会名称', '完整性', '村（居）委会名称未填写'], ['详情', '322160196808063214', '蔡能姐', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '322501197307183227', '陈健蓉', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '322829195010062643', '陈红囡', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '323619198011280541', '周祈', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '32423119681220444X', '蒋余娟', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写'], ['详情', '325191196606052154', '宋云梯', '宝山区大场镇大场社区卫生服务中心', '封面表', '责任医生id', '完整性', '责任医生未填写']]


standardAnalysis = "\n[规范建档率提升分析]"
Color_PO.consoleColor("31", "31", standardAnalysis, "")  # [规范建档率提升分析]
dataMonitor_PO.Web_PO.clickXpath("//div[@class='el-table__body-wrapper is-scrolling-none']/table/tbody/tr/td[5]/div/div/div[2]/button", 2)  # 点击第一条记录规范建档率提升分析
l_text = dataMonitor_PO.Web_PO.getXpathsTextPart("//div", "Copyright © 2019上海智赢健康科技有限公司出品")  # 获取当前页全部内容
# print(l_text)
l_standardAnalysis = l_text[0].split("规范建档率提升分析\n序")[1].split("\n问题档案列表")[0]
l_standardAnalysis = l_standardAnalysis.split('\n')
print(l_standardAnalysis.pop(0))  # '质控时间 质控档案总数量 问题档案数量 规范建档率 操作'
print(List_PO.listSplitSubList(l_standardAnalysis, 4))





#
#
# # c1,查询档案质控分析选定一个日期
# Level_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
# Level_PO.clickXpath("//body/div[@class='el-select-dropdown el-popper is-multiple']/div[1]/div[1]/ul/li[1]", 2)  # 选择第1个  li[1]
# Level_PO.clickXpath("//button[@class='el-button el-button--primary']", 2)  # 查找
# Level_PO.clickXpath("//button[@class='el-button el-button--text el-button--small']", 2)  # 点击查询结果
# # 问题档案列表中的规则类型，勾选 “地址类数据问题 (24.10%)” 和 “电话数据类问题 (2.75%)”
# Level_PO.clickXpathsNum("//span[@aria-checked='mixed']", 1, 2)  # 勾选第1个 “地址类数据问题 (24.10%)”
# Level_PO.clickXpathsNum("//span[@aria-checked='mixed']", 3, 2)  # 勾选第3个  “电话数据类问题 (2.75%)”
#
# # 勾选规则后，页面自动匹配显示符合条件的问题档案列表，并点击第一条记录
# l_data = Level_PO.getXpathsText("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div")
# x = int(len(l_data)/9)
# l_record = numpy.array_split(l_data, x)
# print("[done],检查以下这条记录")
# l_title = ['操作:', '档案编号:', '姓名:', '社区医院:', '表单名称:', '字段名称:', '规则类型:', '错误描述:']
# l_merge = [i + j for i, j in zip(l_title, l_record[0])]
# # print(l_merge)
# list_PO.alignmentKey(l_merge, ":")
# Level_PO.clickXpathsNum("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 1, 2)  # 点击 第一条记录
# # Level_PO.clickXpathsNum("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 10, 2)  #  点击 第二条记录
# # Level_PO.clickXpathsNum("//div[@class='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 19, 2)  # 点击 第三条记录
#
#
#
# print("\n【健康档案封面】")
# Level_PO.clickId("tab-0", 2)   # 健康档案封面
# l_data = Level_PO.getXpathsText("//div[@id='pane-0']/div/div/div/div[1]/div/div/div")
# l_data.pop(0)
# list_PO.alignmentKey(l_data, ":\n")
#
#
#
# l_data = []
# Level_PO.clickId("tab-1", 2)   # 个人基本信息表
# l_data = Level_PO.getXpathsText("//div[@id='pane-1']/div/div/div/div[1]/div/div/div")
# l_data.pop(0)
# def printPersonBaseInfo(varTitle, varSplit):
#     print(varTitle)
#     if varTitle == "\n【个人基本信息表 - 生活环境】":
#         list_PO.alignmentKey(l_data, ":\n")
#     else:
#         # 合并
#         l_temp = []
#         for i in range(0, len(l_data)):
#             if varSplit != l_data[i]:
#                 l_temp.append(l_data[i])
#             else:
#                 for j in range(i):
#                     l_data.pop(0)
#                 l_data.pop(0)
#                 break
#         l_temp.pop()
#         if varSplit == "家族史" or varSplit == "遗传病史" or varSplit == "残疾情况" or varSplit == "生活环境" or varSplit == "反面":
#             list_PO.alignmentKey(l_temp, ":\n")
#         else:
#             l_temp = list_PO.elementMerge(l_temp, 3)
#             list_PO.alignmentKey(l_temp, ":")
# printPersonBaseInfo("\n【个人基本信息表 - 基础信息】", "个人其他信息")
# printPersonBaseInfo("\n【个人基本信息表 - 个人其他信息】", "医疗信息")
# printPersonBaseInfo("\n【个人基本信息表 - 医疗信息】", "既往史")
# printPersonBaseInfo("\n【个人基本信息表 - 既往史】", "家族史")
# printPersonBaseInfo("\n【个人基本信息表 - 家族史】", "遗传病史")
# printPersonBaseInfo("\n【个人基本信息表 - 遗传情况】", "残疾情况")
# printPersonBaseInfo("\n【个人基本信息表 - 残疾情况】", "生活环境")
# printPersonBaseInfo("\n【个人基本信息表 - 生活环境】", "")
#
#
# print("\n【档案信息卡 - 正面反面】")
# Level_PO.clickId("tab-3", 2)   # 档案信息卡
# list1 = Level_PO.getXpathsText("//div[@id='pane-3']/form/div/div[1]/div/div/div")
# # print(list1)
# l11 = []
# l22 = []
# l33 = []
# for i in range(len(list1)):
#     if list1[i].count(":\n") > 0 :
#         l11.append(list1[i].split("\n"))
# for i in range(len(l11)):
#     l22 = list_PO.elementMerge(l11[i],2)
#     l33 = l33 + l22
# list_PO.alignmentKey(l33, ":")
#
#
# print("\n【质控项目汇总 - 个人基本信息表】")
# l_person1 = Level_PO.getXpathText("//div[@class='main']/div[1]/div[2]/div[1]")
# l_person1Value = Level_PO.getXpathText("//div[@class='main']/div[1]/div[2]/div[2]")
# print(l_person1)
# print(l_person1Value)
#
#
#
#
#
#
#
#
#
#
#
# # print("2，按规则类型趋势分析，查看全部")
# # x = Level_PO.getXpathsText("//div[@class='container']/div[6]/div[3]/table/tbody/tr")
# # print(x)
#
#
#
#
# # print("1，档案数据质控分析 - 档案质控分析中查看全部，并点击第一条详情")
# # l_dataQcAnalysisTitle = Level_PO.getXpathsText("//div[@class='container']/div[3]/div[2]/table/thead/tr/th/div")
# # l_dataQcAnalysisTitle.pop()
# # print(" , ".join(l_dataQcAnalysisTitle))  # ['质控时间', '质控档案总数量', '问题档案数量', '合格率']
# # l_dataQcAnalysis = Level_PO.getXpathsText("//div[@class='container']/div[3]/div[3]/table/tbody/tr")
# # for i in range(len(l_dataQcAnalysis)):
# #     print(str(l_dataQcAnalysis[i]).replace("\n", " , ").replace("详情", ""))
# # Level_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
# # Level_PO.clickXpath("//body/div[@class='el-select-dropdown el-popper is-multiple']/div[1]/div[1]/ul/li[1]", 2)  # 选择第二个  li[1]
# # Level_PO.clickXpath("//button[@class='el-button el-button--primary']", 2)  # 查找
# # Level_PO.clickXpath("//button[@class='el-button el-button--text el-button--small']", 2)
# print("\n")