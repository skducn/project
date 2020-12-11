# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-11-26
# Description: 电子健康档案数报表
# *****************************************************************


from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ExcelPO import *
from PO.BasePO import *
Base_PO = BasePO(object)


Excel_PO = ExcelPO("r2.xlsx")

# print(Excel_PO.l_getSheet())
# l_data = Excel_PO.l_getRowData()
# print(l_data)
#
# l_data = Excel_PO.l_getRowData(1)
# print(l_data)
#
# l_data = Excel_PO.l_getRowData(6)
# print(l_data)


s1 = "1.常住人口电子健康档案工指标"
s2 = "2.签约居民人群分类"
s4 = "4.电子健康档案规范建档率"
s3 = "3.电子健康档案建档率"
s5 = "5.电子健康档案动态更新率"
s6 = "6.电子健康档案利用率"
s7 = "7.家庭医生电子健康建档率"
s8 = "8.家庭医生电子健康档案规范建档率"

# 获取签约居民人数
signResidentNums = (Excel_PO.l_getRowValues(1, "3.电子健康档案建档率")[0])
print(signResidentNums)
# 签约居民中建立电子健康档案的人数
createdSignResidentNums = (Excel_PO.l_getRowValues(1, "3.电子健康档案建档率")[1])
print(createdSignResidentNums)


title = "1.c2 电子健康档案建档率"
value = (str(round((Excel_PO.l_getRowValues(1, s1)[1])/(Excel_PO.l_getRowValues(1, s1)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s1)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s1)[2]) + " <> " + str(value))
title = "1.f2 签约完成率"
value = (str(round((Excel_PO.l_getRowValues(1, s1)[4])/(Excel_PO.l_getRowValues(1, s1)[3])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s1)[5], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s1)[5]) + " <> " + str(value))



title = "2.b2 签约居民中老年人占比"
value = (str(round((Excel_PO.l_getRowValues(1, s2)[0])/(Excel_PO.l_getRowValues(1, s4)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s2)[1], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s2)[1]) + " <> " + str(value))
title = "2.d2 签约居民中高血压患者占比"
value = (str(round((Excel_PO.l_getRowValues(1, s2)[2])/(Excel_PO.l_getRowValues(1, s4)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s2)[3], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s2)[3]) + " <> " + str(value))
titel = "2.f2 签约居民中糖尿病患者占比"
value = (str(round((Excel_PO.l_getRowValues(1, s2)[4])/(Excel_PO.l_getRowValues(1, s4)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s2)[5], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s2)[5]) + " <> " + str(value))



title = "3.c2 建档率"
value = (str(round((Excel_PO.l_getRowValues(1, s3)[1])/(Excel_PO.l_getRowValues(1, s3)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s3)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s3)[2]) + " <> " + str(value))



title = "5.c2 档案动态更新率"
value = (str(round((Excel_PO.l_getRowValues(1, s5)[1])/(Excel_PO.l_getRowValues(1, s5)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s5)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s5)[2]) + " <> " + str(value))



title = "6.c2 档案利用率"
value = (str(round((Excel_PO.l_getRowValues(1, s6)[1])/(Excel_PO.l_getRowValues(1, s5)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s6)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s6)[2]) + " <> " + str(value))



title = "7.E 建档率"
# 计算表中建档率（签约居民中建立电子健康档案的人数/签约居民人数*100%），四舍五入保留1位小数。
l_actual = (Excel_PO.l_getColDataByPartCol([2, 3], [0], s7))
l_all = []
for i in range(len(l_actual[0])):
    l_all.append(str(round(l_actual[1][i]/l_actual[0][i]*100, 1)) + "%")
# print(l_all)
l_expect = (Excel_PO.l_getColDataByPartCol([4], [0], s7))
# print(l_expect[0])
Base_PO.assertEqual(List_PO.compare2ListsGetIndex(l_all,l_expect[0]), None, "[ok] " + title, "[error] " + title + ", " + str(List_PO.compare2ListsGetIndex(l_all, l_expect[0])))



title = "8.C 全部签约人数统计"
l_actual = (Excel_PO.l_getColDataByPartCol([2], [0], s8))
s = 0
for i in l_actual[0]:
    s = s + i
Base_PO.assertEqual(signResidentNums, s, "[ok] " + title, "[error] " + title + ", " + str(s) + " <> " + str(signResidentNums))

title = "8.D 签约居民中建立电子健康档案的人数"
l_actual = (Excel_PO.l_getColDataByPartCol([3], [0], s8))
s = 0
for i in l_actual[0]:
    s = s + i
Base_PO.assertEqual(createdSignResidentNums, s, "[ok] " + title, "[error] " + title + ", " + str(s) + " <> " + str(createdSignResidentNums))
