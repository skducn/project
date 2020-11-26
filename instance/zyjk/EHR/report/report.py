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


Excel_PO = ExcelPO("r2.xlsx")

print(Excel_PO.l_getSheet())
l_data = Excel_PO.l_getRowData()
print(l_data)

l_data = Excel_PO.l_getRowData(1)
print(l_data)

l_data = Excel_PO.l_getRowData(6)
print(l_data)


# 两表单元格比较('1.常住人口电子健康档案工指标',1,0, '2.签约居民人群分类',2,1)
# 一个表某一列的合计（忽略第一行） 合计（"7.家庭医生电子健康建档率",2,ignore0）
# 一个表某一行的合计（忽略第一列）
# 一个表里（A列/B列*100%）两值比率统计。

