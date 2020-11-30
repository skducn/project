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

# # 忽略第一行数据，求第三列所有值的和。
# l_data = Excel_PO.l_getColDataByPartCol([2], [1], "7.家庭医生电子健康建档率")
# print(l_data)
# s = 0
# for i in l_data[0]:
#     s = i + s
# print(s)

# # 获取表第2行第一个值
# signResidentNums = (Excel_PO.l_getRowValues(1, "4.电子健康档案规范建档率")[0])
# print(signResidentNums)

# # 统计所有行
l_data = Excel_PO.l_getRowData("4.电子健康档案规范建档率")
# print(l_data)







title = "1.c2 电子健康档案建档率"
s1 = "1.常住人口电子健康档案工指标"
value = (str(round((Excel_PO.l_getRowValues(1, s1)[1])/(Excel_PO.l_getRowValues(1, s1)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s1)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s1)[2]) + " <> " + str(value))
title = "1.f2 签约完成率"
s1 = "1.常住人口电子健康档案工指标"
value = (str(round((Excel_PO.l_getRowValues(1, s1)[4])/(Excel_PO.l_getRowValues(1, s1)[3])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s1)[5], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s1)[5]) + " <> " + str(value))
print("\n")


title = "2.b2 签约居民中老年人占比"
s2 = "2.签约居民人群分类"
s4 = "4.电子健康档案规范建档率"
value = (str(round((Excel_PO.l_getRowValues(1, s2)[0])/(Excel_PO.l_getRowValues(1, s4)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s2)[1], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s2)[1]) + " <> " + str(value))
title = "2.d2 签约居民中高血压患者占比"
value = (str(round((Excel_PO.l_getRowValues(1, s2)[2])/(Excel_PO.l_getRowValues(1, s4)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s2)[3], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s2)[3]) + " <> " + str(value))
titel = "2.f2 签约居民中糖尿病患者占比"
value = (str(round((Excel_PO.l_getRowValues(1, s2)[4])/(Excel_PO.l_getRowValues(1, s4)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s2)[5], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s2)[5]) + " <> " + str(value))
print("\n")


title = "3.c2 建档率"
s3 = "3.电子健康档案建档率"
value = (str(round((Excel_PO.l_getRowValues(1, s3)[1])/(Excel_PO.l_getRowValues(1, s3)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s3)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s3)[2]) + " <> " + str(value))
print("\n")


title = "5.c2 档案动态更新率"
s5 = "5.电子健康档案动态更新率"
value = (str(round((Excel_PO.l_getRowValues(1, s5)[1])/(Excel_PO.l_getRowValues(1, s5)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s5)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s5)[2]) + " <> " + str(value))
print("\n")


title = "6.c2 档案利用率"
s6 = "6.电子健康档案利用率"
value = (str(round((Excel_PO.l_getRowValues(1, s6)[1])/(Excel_PO.l_getRowValues(1, s5)[0])*100, 1)) + "%")
Base_PO.assertEqual(Excel_PO.l_getRowValues(1, s6)[2], value, "[ok] " + title, "[error] " + title + ", " + str(Excel_PO.l_getRowValues(1, s6)[2]) + " <> " + str(value))
print("\n")


s7 = "7.家庭医生电子健康建档率"
# 计算表中建档率（签约居民中建立电子健康档案的人数/签约居民人数*100%），四舍五入保留1位小数。
l_actual = (Excel_PO.l_getColDataByPartCol([2, 3], [0], s7))
l_all = []
for i in range(len(l_actual[0])):
    l_all.append(str(round(l_actual[1][i]/l_actual[0][i]*100, 1)) + "%")
print(l_all)
l_expect = (Excel_PO.l_getColDataByPartCol([4], [0], s7))
print(l_expect[0])


def compare(list1, list2):
    error_index = []
    if len(list1) == len(list2):
        for i in range(0, len(list1)):
        # 两个列表对应元素相同，则直接过
            if list1[i] == list2[i]:
                pass
            else:
                # 两个列表对应元素不同，则输出对应的索引
                error_index.append(i)
        if error_index == []:
            return None
        else:
            return (error_index)
    else:
        return("error, 两列表元素数量不一致")

print(compare(l_all,l_expect[0]))
