# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-9-11
# Description: 区域平台 - 数据交换规则
#***************************************************************
import sys

from PO.OpenpyxlPO import *
from PlatformRulePO import *
PlatformRule_PO = PlatformRulePO()
PlatformRule_PO.clsApp("Microsoft Excel")
Openpyxl_PO = OpenpyxlPO("数据交换规则.xlsx")

# todo 1，非空
PlatformRule_PO.genRecord('非空', Openpyxl_PO)
PlatformRule_PO.feikong('非空', Openpyxl_PO)


# todo 2，日期
PlatformRule_PO.genRecord('日期', Openpyxl_PO)
PlatformRule_PO.riqi('日期', Openpyxl_PO)


# todo 3,数字范围
PlatformRule_PO.genRecord('数字范围', Openpyxl_PO)
PlatformRule_PO.shuzifanwei('数字范围', Openpyxl_PO)


# todo 4，值域
PlatformRule_PO.genRecord('值域', Openpyxl_PO)
PlatformRule_PO.zhiyu('值域', Openpyxl_PO)


# todo 5，身份证
PlatformRule_PO.genRecord('身份证', Openpyxl_PO)
PlatformRule_PO.shenfenzheng('身份证', Openpyxl_PO)



# todo 6，关联表
# list = Openpyxl_PO.getRowValueByCol([4, 6, 10, 11], '关联表')
# list.pop(0)
# print(list)




Openpyxl_PO.open()

