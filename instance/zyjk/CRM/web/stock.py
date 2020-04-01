# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-11-19
# Description: CRM 销售业绩报表与 65数据库匹配
# 依据：2019.11月销售业绩报表(2).xlsx
# https://blog.csdn.net/firehood_/article/details/8433077  Tesseract-OCR 字符识别---样本训练
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../../..")))

from PO.mysqlPO import *
mysql_PO = MysqlPO("192.168.0.65", "ceshi", "123456", "TD_APP")

from PO.excelPO import *
excel_PO = ExcelPO()

allRecord = excel_PO.readAllrows("sale.xls")

for i in range(1, allRecord):
    x = excel_PO.readRowValue("sale.xls", i, "sheet1")
    if x[1] == "国药":
        company = "国药%"
    elif x[1] == "沪中":
        company = "上药%"
    else:
        company = str(x[1]).strip()
    saleDate = str(x[0]).strip()
    product = str(x[2]).strip()
    address = str(x[8]).strip()

    mysql_PO.cur.execute('select stock,daibiao from purchase_sale where business like "%s" and product like "%s" and  time="%s"  and  client_name="%s"' % (company,product,saleDate,address))
    s1 = mysql_PO.cur.fetchall()

    if len(s1) == 0 :
        address = str(x[15]).strip()
        mysql_PO.cur.execute(
            'select stock,daibiao from purchase_sale where business like "%s" and product like "%s" and  time="%s"  and  client_name="%s"' % (
            company, product, saleDate, address))
        s1 = mysql_PO.cur.fetchall()
        print(str(i + 1) + "," + str(s1))
    else:
        print(str(i + 1) + "," + str(s1))

    b = 0
    if len(s1) == 1 :
        # if int(x[10]) != int(s1[0][0]) or s1[0][1] == "":
        if int(x[10]) != int(s1[0][0]):
            excel_PO.writeExcel("sale.xls", "sheet1", i, 11, s1.__str__())
    else:
        for j in range(len(s1)):
            if int(x[10]) == int(s1[j][0]):
                b = 1
        if b != 1:
            excel_PO.writeExcel("sale.xls", "sheet1", i, 11, s1.__str__())



