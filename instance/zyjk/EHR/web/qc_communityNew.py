# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2021-10-11
# Description: EHR 质量管理系统 (质控结果分析 - 社区签约居民New)
# chrome版本：94.0.4606.81
# webdriver驱动：https://npm.taobao.org/mirrors/chromedriver
# 本地路径：C:\Python39\Scripts
# *****************************************************************

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
dataMonitor_PO = DataMonitorPO()

# *****************************************************************
# 登录
dataMonitor_PO.login("test", "Qa@123456")

# 菜单
dataMonitor_PO.clickMenu("质控结果分析", "(社区)签约居民-新")

# *****************************************************************
a,b,c,d,e,f,g,h,i,j,k,l,m = dataMonitor_PO.getCommunityNew()
print("签约居民中重点人群：" + str(a))
print("签约未建档人数：" + str(b))
# print(c)
print("老年人:" + c[0])
print("糖尿病:" + c[1])
print("高血压:" + c[2])
print("老年人与糖尿病:" + c[3])
print("既是老年人又是高血压与糖尿病:" + c[4])
print("老年人与高血压:" + c[5])
print("糖尿病与高血压:" + c[6])
print("60岁以上签约居民：" + str(d))
print("60岁以上签约居民 - 签约率：" + str(e) + "%")
print("60岁以上签约居民 - 签约建档率：" + str(f) + "%")
print("签约居民中非重点人群：" + str(g))
print("签约未建档人数：" + str(h))
print("签约居民中非重点人群 - 签约率：" + str(i) + "%")
print("签约居民中非重点人群 - 签约建档率：" + str(j) + "%")
print("规范建档占比：" + str(k) + "%")
print("更新率：" + str(l) + "%")
print("利用率：" + str(m) + "%")

# 检查点

dataMonitor_PO.checkDigitalborder(" c1，签约居民中重点人群不能小于0", int(a), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c2，签约未建档人数不能小于0", int(b), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c3，60岁以上签约居民不能小于0", int(d), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c4，60岁以上签约居民 - 签约率不能小于0", float(e), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c5，60岁以上签约居民 - 签约率不能大于0", float(e), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c6，60岁以上签约居民 - 签约建档率不能小于0", float(f), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c7，60岁以上签约居民 - 签约建档率不能大于0", float(f), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c8，签约居民中非重点人群不能小于0", int(g), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c9，签约居民中非重点人群 - 签约率不能小于0", float(i), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c10，签约居民中非重点人群 - 签约率不能大于0", float(i), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c11，签约居民中非重点人群 - 签约建档率不能小于0", float(j), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c12，签约居民中非重点人群 - 签约建档率不能大于0", float(j), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c13，规范建档占比不能小于0", float(k), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c14，规范建档占比不能大于0", float(k), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c15，更新率比不能小于0", float(l), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c16，更新率不能大于0", float(l), "<=", 100)
dataMonitor_PO.checkDigitalborder(" c17，利用率比不能小于0", float(m), ">=", 0)
dataMonitor_PO.checkDigitalborder(" c18，利用率比不能大于0", float(m), "<=", 100)