# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-7-19
# Description: 爬取盛蕴erp管理平台报表数据
# 192.168.0.65
# 预发布：
# 接口文档：http://192.168.0.245:8080/doc.html
# 数据库：192.168.0.244
#***************************************************************

import os, sys

from ErpPO import *
Erp_PO = ErpPO()

from PO.StrPO import *
Str_PO = StrPO()
from PO.TimePO import *
Time_PO = TimePO()
from PO.DataPO import *
Data_PO = DataPO()
from PO.ListPO import *
List_PO = ListPO()
from PO.OpenpyxlPO import *


Sys_PO.killPid('EXCEL.EXE')

def checkBrowser():
    Openpyxl_PO = OpenpyxlPO("../statisticalReturns/i_erp_reportField_case.xlsx")

    # 生成临时sheet
    varSheet = "browser"
    Openpyxl_PO.delSheet(varSheet)
    Openpyxl_PO.addSheetCover(varSheet, 99)


    # oa
    Erp_PO.login("http://192.168.0.65", "liuting", "")
    Erp_PO.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
    Erp_PO.maxBrowser(1)  # 全屏
    Erp_PO.clickMemuERP("统计报表", "拜访分析报表")
    Erp_PO.zoom("20")  # 缩小页面20%便于抓取元素
    list1 = Erp_PO.Web_PO.getXpathsText("//tr")  # 获取数据
    list1 = List_PO.listBatchDel(list1, "明细")
    list1 = List_PO.listBatchDel(list1, "总计")
    list1 = List_PO.listBatchDel(list1, "操作")
    list1 = List_PO.listBatchDel(list1, "")
    # print(list1)


    # 更新区域和代表
    list7 = List_PO.sliceList(list1, '区域\n代表', 0)
    list2 = List_PO.sliceList(list1, '区域\n代表', 1)
    list2.insert(0, '区域\n代表')
    list2.append('总计\n')
    # print(list2)

    # 将字段与值写入表格
    for i in range(len(list7)):
        list3 = str(list7[i]).split("\n")
        Openpyxl_PO.setRowValue({i+1: list3}, "browser")

    # 将区域和代表插入表格
    Openpyxl_PO.insertCols(1, 2, "browser")
    for i in range(len(list2)):
        list4 = str(list2[i]).split("\n")
        Openpyxl_PO.setRowValue({i+1: list4}, "browser")


    l_title = Openpyxl_PO.getOneRowValue(0, "browser")
    # print(l_title)
    for i in range(len(l_title)):
        if l_title[i] == '拜访定位匹配人次':
            # print(i)
            Openpyxl_PO.delSeriesCol(i+1, 10, "browser")  # 删除第“拜访定位匹配人次”列及之后的所有列
            break

    Openpyxl_PO.save()
    Erp_PO.close()

