# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2020-12-8
# Description: 健康档案质控报告V2
# *****************************************************************

from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ExcelPO import *
from PO.BasePO import *
Base_PO = BasePO(object)


Excel_PO = ExcelPO("v2.xlsx")

print("表1 = 1.常住人口电子健康档案工作指标 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" )
tbl1 = Excel_PO.l_getRowData("表1")
tbl1.pop(0)
print("[表1_c1_电子健康档案建档率]")
for i in range(len(tbl1)):
    if round((tbl1[i][3])/(tbl1[i][2]) * 100, 2) == round(tbl1[i][4], 2):
        # print("[ok] " + str(i+2))
        Excel_PO.setCellColor(i + 2, 5, "00E400", "表1")
    else:
        print("[error] No." + str(i+2) + "，表格值" + str(round(tbl1[i][4], 2)) + "，测试值" + str(round(tbl1[i][3] / tbl1[i][2] * 100, 2)))
        Excel_PO.setCellColor(i + 2, 5, "FF0000", "表1")

print("\n[表1_c2_目标签约人数]")
for i in range(len(tbl1)):
    if (int(tbl1[i][2] * 0.3)) == tbl1[i][5]:
        # print("[ok] " + str(i+2))
        Excel_PO.setCellColor(i + 2, 6, "00E400", "表1")
    else:
        print("[error] No." + str(i + 2) + "，表格值" + str(round(tbl1[i][5], 2)) + "，测试值" + str(round(tbl1[i][2] * 0.3, 2)))
        Excel_PO.setCellColor(i + 2, 6, "FF0000", "表1")

print("\n[表1_c3_签约完成率]")
for i in range(len(tbl1)):
    if round(tbl1[i][6] / tbl1[i][5] * 100, 2) == round(tbl1[i][7], 2):
        # print("[ok] " + str(i+2))
        Excel_PO.setCellColor(i + 2, 8, "00E400", "表1")
    else:
        print("[error] No." + str(i + 2) + "，表格值" + str(round(tbl1[i][7], 2)) + "，测试值" + str(round(tbl1[i][6] / tbl1[i][5] * 100, 2)))
        Excel_PO.setCellColor(i + 2, 8, "FF0000", "表1")

Excel_PO.save()