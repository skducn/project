# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-26
# Description: CRM 商务管理 - 销售分析（PC端）
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import datetime,numpy
from time import sleep

from PO.timePO import *
from PO.mysqlPO import *
from PO.excelPO import *
from decimal import Decimal
from PO.listPO import *

mysql_PO = MysqlPO("192.168.0.65", "ceshi", "123456", "TD_APP")  # 盛蕴CRM小程序 测试环境
time_PO = TimePO()
excel_PO = ExcelPO()
list_PO = ListPO()

# ===================================================================================================================================================
# 净销售分析报表（代表）
def netSale_representative(varMenu, varName):
    print("~" * 100)
    starttime = datetime.datetime.now()
    varYesterday = time_PO.get_day_of_day(-1)
    varFirstday_of_month = time_PO.get_firstday_of_month(str(varYesterday).split("-")[0],str(varYesterday).split("-")[1])

    if varMenu == "日销售金额":
        print("净销售分析报表（代表） => " + str(varYesterday) + " 日销售金额（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,client_name,stock from purchase_sale where diqu_uid<>0 and time="%s"' % (varYesterday))
    elif varMenu == "当月累计销售金额":
        print("净销售分析报表（代表） => " + str(varFirstday_of_month) + " 至 " + str(varYesterday) + " 当月累计销售金额（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,client_name,stock from purchase_sale where diqu_uid<>0 and time BETWEEN "%s" AND "%s"' % (varFirstday_of_month, varYesterday))
    elif varMenu == "月销售指标":
        print("净销售分析报表（代表） => " + str(varFirstday_of_month) + " 至 " + str(varYesterday) + " 月销售指标金额（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,client_name,stock from purchase_sale where diqu_uid<>0 and time BETWEEN "%s" AND "%s"' % (varFirstday_of_month, varYesterday))
    elif varMenu == "当年累计销售金额":
        varTime_firstday_of_year = time_PO.get_firstday_of_month(str(varYesterday).split("-")[0], 1)
        print("净销售分析报表（代表） => " + str(varTime_firstday_of_year) + " 至 " + str(varYesterday) + " 当年累计销售金额（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,client_name,stock from purchase_sale where diqu_uid<>0 and time BETWEEN "%s" AND "%s"' % (varTime_firstday_of_year, varYesterday))
    else:
        exit()
    database = mysql_PO.cur.fetchall()
    l_src = []
    l_optimize = []
    for i in range(tblCount):
        l_src.append(list(database[i]))
    # print("database原始 => " + str(l_src))
    l_merger = l_src
    for i in range(len(l_merger)):
        for j in range(i + 1, len(l_merger)):
            if l_merger[i][0] == l_merger[j][0] and l_merger[i][1] == l_merger[j][1]:
                l_merger[i][2] = str(int(l_merger[i][2]) + int(l_merger[j][2]))
    # print("database合并 => " + str(l_merger))
    if l_optimize == []:
        l_optimize.append(l_merger[0])
    for i in range(len(l_merger)):
        varTmp = 0
        for j in range(len(l_optimize)):
            if l_merger[i][0] == l_optimize[j][0] and l_merger[i][1] == l_optimize[j][1]:
                varTmp = varTmp + 1
        if varTmp == 0:
            l_optimize.append(l_merger[i])
    # print("database去重 => " + str(l_optimize))
    # print("databsse => ")
    # for i in range(len(l_optimize)):
    #     print(l_optimize[i])

    allRecord = excel_PO.readAllrows("sale_201912.xls")
    excel_PO.writeXls("sale_201912.xls", "*", 9, "", "sheet1")  # 数量

    sum = 0
    varSign = 0
    l_calc = []
    for i in range(1, allRecord):
        l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
        for j in range(len(l_optimize)):
            if l_optimize[j][0] == l_excel[0] and l_optimize[j][1] == l_excel[7] and l_excel[3] == varName:   # 药品名称0,医院名称7
                excel_PO.writeXls("sale_201912.xls", i, 9, l_optimize[j][2], "sheet1")   # 数量9

    if varMenu == "月销售指标":
        for i in range(1, allRecord):
            l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
            if l_excel[3] == varName:
                varSign = 1
                unitCost = Decimal(str(l_excel[8])).quantize(Decimal('0.00'))  # 单价
                varAmount = float(unitCost) * float(l_excel[11]) * 0.0001  #  金额 = 单价 * 12月指标
                # excel_PO.writeXls("sale_201912.xls", i, 12, varAmount, "sheet1")  # 写入12月销售指标金额
                l_calc.append(l_excel[7])  # 医院名
                l_calc.append(varAmount)  # 月销售指标
                l_calc.append(l_excel[4])  # 姓名
    else:
        excel_PO.writeXls("sale_201912.xls", "*", 10, "", "sheet1")  # 金额 = 单价 * 数量
        for i in range(1, allRecord):
            l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
            if l_excel[3] == varName and l_excel[9] != "":  # 地区经理3,数量9
                varSign = 1
                unitCost = Decimal(str(l_excel[8])).quantize(Decimal('0.00'))  # 单价
                varAmount = float(unitCost) * float(l_excel[9]) * 0.0001  # 金额 = 单价 * 数量
                excel_PO.writeXls("sale_201912.xls", i, 10, varAmount, "sheet1")  # 写入日销售金额
                l_calc.append(l_excel[7])  # 医院名称7
                l_calc.append(varAmount)  # 金额
                l_calc.append(l_excel[4])  # 姓名4

    if varSign == 1:
        # excel原始数据 ,(excel 单价*数量计算后的数据)
        # print(l_calc)
        l_src = list_PO.oneSplitGroupList(l_calc, 3)
        # print("excel原始数据 => " + str(l_src))

        # excel医院金额合并
        l_merger = l_src
        for i in range(len(l_merger)):
            for j in range(i + 1, len(l_merger)):
                if l_merger[i][0] == l_merger[j][0] and l_merger[i][2] == l_merger[j][2]:
                    l_merger[i][1] = l_merger[i][1] + l_merger[j][1]
        # print("excel医院合并 => " + str(l_merger))

        # excel医院去重
        l_optimize2 = []
        if l_optimize2 == []:
            l_optimize2.append(l_merger[0])
        for i in range(len(l_merger)):
            varTmp = 0
            for j in range(len(l_optimize2)):
                if l_merger[i][0] == l_optimize2[j][0] and l_merger[i][2] == l_optimize2[j][2]:
                    varTmp = varTmp + 1
            if varTmp == 0:
                l_optimize2.append(l_merger[i])
        # print("excel医院去重 => " + str(l_optimize2))

        # excel人员合并
        l_merger = l_optimize2
        for i in range(len(l_merger)):
            for j in range(i + 1, len(l_merger)):
                if l_merger[i][2] == l_merger[j][2] :
                    l_merger[i][1] = l_merger[i][1] + l_merger[j][1]
        # print("excel人员合并 => " + str(l_merger))

        # 人员去重
        l_optimize2 = []
        if l_optimize2 == []:
            l_optimize2.append(l_merger[0])
        for i in range(len(l_merger)):
            varTmp = 0
            for j in range(len(l_optimize2)):
                if l_merger[i][2] == l_optimize2[j][2]:
                    varTmp = varTmp + 1
            if varTmp == 0:
                l_optimize2.append(l_merger[i])
        # print("人员去重 => " + str(l_optimize2))

        for i in range(len(l_optimize2)):
            sum = sum + round(l_optimize2[i][1], 2)
        print("区域：" + varName + "（" + str(round(sum, 2)) + "）")
        sum = 0
        for i in range(len(l_optimize2)):
            sum = sum + round(l_optimize2[i][1], 2)
            print("- " + str(l_optimize2[i][2]) + "（" + str(round(l_optimize2[i][1], 2)) + "）")
        # return round(sum, 2)
        # print(round(sum, 2))
    else:
        return []

    endtime = datetime.datetime.now()
    print("执行了 " + str((endtime - starttime).seconds) + " 秒")

netSale_representative("日销售金额", "刘挺")
netSale_representative("当月累计销售金额", "刘挺")
netSale_representative("月销售指标", "刘挺")

netSale_representative("日销售金额", "饶顺荣")
netSale_representative("当月累计销售金额", "饶顺荣")
netSale_representative("月销售指标", "饶顺荣")

netSale_representative("日销售金额", "张慧涛")
netSale_representative("当月累计销售金额", "张慧涛")
netSale_representative("月销售指标", "张慧涛")

netSale_representative("日销售金额", "薛伟")
netSale_representative("当月累计销售金额", "薛伟")
netSale_representative("月销售指标", "薛伟")

netSale_representative("日销售金额", "钮学彬")
netSale_representative("当月累计销售金额", "钮学彬")
netSale_representative("月销售指标", "钮学彬")

netSale_representative("日销售金额", "黄新晖")
netSale_representative("当月累计销售金额", "黄新晖")
netSale_representative("月销售指标", "黄新晖")

netSale_representative("日销售金额", "周夙")
netSale_representative("当月累计销售金额", "周夙")
netSale_representative("月销售指标", "周夙")

netSale_representative("日销售金额", "邓向阳")
netSale_representative("当月累计销售金额", "邓向阳")
netSale_representative("月销售指标", "邓向阳")



# ===================================================================================================================================================
# 净销售分析报表（医院）
def netSale_hospital(varMenu, varName):
    starttime = datetime.datetime.now()
    print("~" * 100)
    allRecord = excel_PO.readAllrows("sale_201912.xls")
    excel_PO.writeXls("sale_201912.xls", "*", 13, "", "sheet1")
    excel_PO.writeXls("sale_201912.xls", "*", 14, "", "sheet1")

    # 获取医院名称列表
    l_merger = []
    for i in range(1, allRecord):
        l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
        if l_excel[3] == varName:
            l_merger.append(l_excel[7])
    # 医院去重
    l_optimize7 = []
    if l_optimize7 == []:
        l_optimize7.append(l_merger[0])
    for i in range(len(l_merger)):
        varTmp = 0
        for j in range(len(l_optimize7)):
            if l_merger[i] == l_optimize7[j]:
                varTmp = varTmp + 1
        if varTmp == 0:
            l_optimize7.append(l_merger[i])
    # print("excel医院去重 => " + str(l_optimize7))
    # print(len(l_optimize7))
    # for i in range(len(l_optimize7)):
    #     print(l_optimize7[i])

    varYesterday = time_PO.get_day_of_day(-1)
    varFirstday_of_month = time_PO.get_firstday_of_month(str(varYesterday).split("-")[0], str(varYesterday).split("-")[1])
    sum = 0
    l_optimize2 = []
    if varMenu == "日销售金额":
        print("净销售分析报表（医院） => " + str(varYesterday) + " 日销售金额（" + varName + "）")
    elif varMenu == "当月累计销售金额":
        print("净销售分析报表（医院） => " + str(varFirstday_of_month) + " 至 " + str(varYesterday) + " 当月累计销售金额（" + varName + "）")
    elif varMenu == "月销售指标金额":
        print("净销售分析报表（医院） => " + str(varFirstday_of_month) + " 至 " + str(varYesterday) + " 月销售指标金额（" + varName + "）")

    l_calc = []
    if varMenu == "月销售指标金额":
        for i in range(1, allRecord):
            l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
            if l_excel[3] == varName:
                unitCost = Decimal(str(l_excel[8])).quantize(Decimal('0.00'))  # 单价
                varAmount = float(unitCost) * float(l_excel[11]) * 0.0001  # 金额 = 单价 * 12月指标
                # excel_PO.writeXls("sale_201912.xls", i, 12, varAmount, "sheet1")  # 写入12月销售指标金额
                l_calc.append(l_excel[7])  # 医院名
                l_calc.append(varAmount)  # 月销售指标
    else:
        for a in range(len(l_optimize7)):
            if varMenu == "日销售金额":
                tblCount = mysql_PO.cur.execute('select product,client_name,stock,daibiao from purchase_sale where diqu_uid<>0 and client_name="%s" and time="%s"' % (l_optimize7[a], varYesterday))
            elif varMenu == "当月累计销售金额":
                tblCount = mysql_PO.cur.execute('select product,client_name,stock,daibiao from purchase_sale where diqu_uid<>0 and client_name="%s" and time BETWEEN "%s" AND "%s"' % (l_optimize7[a], varFirstday_of_month, varYesterday))

            if tblCount != 0 :
                database = mysql_PO.cur.fetchall()
                l_src = []
                l_optimize = []

                for i in range(tblCount):
                    l_src.append(list(database[i]))
                # print("database原始 => " + str(l_src))
                l_merger = l_src
                for i in range(len(l_merger)):
                    for j in range(i + 1, len(l_merger)):
                        if l_merger[i][0] == l_merger[j][0] and l_merger[i][1] == l_merger[j][1] and l_merger[i][3] == l_merger[j][3]:
                            l_merger[i][2] = str(int(l_merger[i][2]) + int(l_merger[j][2]))
                # print("database合并数量 => " + str(l_merger))
                if l_optimize == []:
                    l_optimize.append(l_merger[0])
                for i in range(len(l_merger)):
                    varTmp = 0
                    for j in range(len(l_optimize)):
                        if l_merger[i][0] == l_optimize[j][0] and l_merger[i][1] == l_optimize[j][1] and l_merger[i][3] == l_merger[j][3]:
                            varTmp = varTmp + 1
                    if varTmp == 0:
                        l_optimize.append(l_merger[i])
                # print("database去重 => " + str(l_optimize))
                #
                # print("databsse => ")
                # for i in range(len(l_optimize)):
                #     print(l_optimize[i])

                for i in range(1, allRecord):
                    l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
                    for j in range(len(l_optimize)):
                        if l_optimize[j][0] == l_excel[0] and l_optimize[j][1] == l_excel[7] and l_optimize[j][3] == l_excel[4]:  # 药品名称0,医院名称7,姓名4
                            excel_PO.writeXls("sale_201912.xls", i, 13, l_optimize[j][2], "sheet1")  # 医院（数量）13
                for i in range(1, allRecord):
                    l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
                    if l_excel[7] == l_optimize7[a] and l_excel[13] != "":  # 医院名称7，医院（数量）13
                        varPrice = Decimal(str(l_excel[8])).quantize(Decimal('0.00'))  # 单价
                        varAmount = float(varPrice) * float(l_excel[13]) * 0.0001  # 金额 = 单价 * 医院数量
                        # excel_PO.writeXls("sale_201912.xls", i, 14, varAmount, "sheet1")  # 医院金额
                        l_calc.append(l_excel[7])
                        l_calc.append(varAmount)


    l_src = list_PO.oneSplitGroupList(l_calc, 2)
    # print("excel原始数据 => " + str(l_src))

    # excel医院金额合并
    l_merger = []
    l_merger = l_src
    for i in range(len(l_merger)):
        for j in range(i + 1, len(l_merger)):
            if l_merger[i][0] == l_merger[j][0]:
                l_merger[i][1] = l_merger[i][1] + l_merger[j][1]
    l_merger[0][1] = round(l_merger[0][1], 2)
    # print("excel医院金额合并 => " + str(l_merger))

    # excel医院去重
    if l_optimize2 == []:
        l_optimize2.append(l_merger[0])
    for i in range(len(l_merger)):
        varTmp = 0
        for j in range(len(l_optimize2)):
            if l_merger[i][0] == l_optimize2[j][0] :
                varTmp = varTmp + 1
        if varTmp == 0:
            l_optimize2.append(l_merger[i])
    # print("excel医院去重 => " + str(l_optimize2))

    for i in range(len(l_optimize2)):
        if l_optimize2[i][1] == 0.0 or l_optimize2[i][1] == 0:
            pass
        else:
            print(l_optimize2[i])
        sum = sum + round(l_optimize2[i][1], 2)

    print("合计:" + str(round(sum, 2)))

    endtime = datetime.datetime.now()
    print("执行了 " + str((endtime - starttime).seconds) + " 秒")

# netSale_hospital("日销售金额", "刘挺")
# netSale_hospital("当月累计销售金额", "刘挺")
# netSale_hospital("月销售指标金额", "刘挺")
#
# netSale_hospital("日销售金额", "饶顺荣")
# netSale_hospital("当月累计销售金额", "饶顺荣")
# netSale_hospital("月销售指标金额", "饶顺荣")
#
# netSale_hospital("日销售金额", "张慧涛")
# netSale_hospital("当月累计销售金额", "张慧涛")
# netSale_hospital("月销售指标金额", "张慧涛")
#
# netSale_hospital("日销售金额", "薛伟")
# netSale_hospital("当月累计销售金额", "薛伟")
# netSale_hospital("月销售指标金额", "薛伟")
# #
# netSale_hospital("日销售金额", "钮学彬")
# netSale_hospital("当月累计销售金额", "钮学彬")
# netSale_hospital("月销售指标金额", "钮学彬")
# #
# netSale_hospital("日销售金额", "黄新晖")
# netSale_hospital("当月累计销售金额", "黄新晖")
# netSale_hospital("月销售指标金额", "黄新晖")
# #
# netSale_hospital("日销售金额", "周夙")
# netSale_hospital("当月累计销售金额", "周夙")
# netSale_hospital("月销售指标金额", "周夙")
# #
# netSale_hospital("日销售金额", "邓向阳")
# netSale_hospital("当月累计销售金额", "邓向阳")
# netSale_hospital("月销售指标金额", "邓向阳")

# ===================================================================================================================================================
# 产品销售分析报表
def productSale_representative(varProduct, varMenu, varName):
    print("~" * 100)
    starttime = datetime.datetime.now()
    varYesterday = time_PO.get_day_of_day(-1)
    varFirstday_of_month = time_PO.get_firstday_of_month(str(varYesterday).split("-")[0],str(varYesterday).split("-")[1])

    if varMenu == "日销售数量":
        print("产品销售分析报表（代表） => " + varProduct + " " + str(varYesterday) + " 日销售数量（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,daibiao,stock from purchase_sale where diqu_uid<>0 and time="%s" and diqu="%s" and product="%s"' % (varYesterday, varName, varProduct))
        database = mysql_PO.cur.fetchall()
        l_src = []
        for i in range(tblCount):
            l_src.append(list(database[i]))
        # print("database原始 => " + str(l_src))
        l_merger = l_src
        sum = 0
        for i in range(len(l_merger)):
            print(l_merger[i])
            sum = sum + int(l_merger[i][2])
        print("合计:" + str(sum))

    elif varMenu == "当月累计销售数量":
        print("产品销售分析报表（代表） => " + varProduct + " " + str(varFirstday_of_month) + " 至 " + str(varYesterday) + " 当月累计销售数量（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,daibiao,stock from purchase_sale where diqu_uid<>0 and time BETWEEN "%s" AND "%s" and diqu="%s" and product="%s"' % (varFirstday_of_month, varYesterday, varName, varProduct))
        database = mysql_PO.cur.fetchall()
        # 原始
        l_src = []
        for i in range(tblCount):
            l_src.append(list(database[i]))
        # print("原始 => " + str(l_src))

        # 合并
        l_merger = []
        l_merger = l_src
        for i in range(len(l_merger)):
            for j in range(i + 1, len(l_merger)):
                if l_merger[i][1] == l_merger[j][1]:
                    l_merger[i][2] = int(l_merger[i][2]) + int(l_merger[j][2])
        # print("合并 => " + str(l_merger))

        # 去重
        l_optimize2 = []
        if l_optimize2 == []:
            l_optimize2.append(l_merger[0])
        for i in range(len(l_merger)):
            varTmp = 0
            for j in range(len(l_optimize2)):
                if l_merger[i][1] == l_optimize2[j][1]:
                    varTmp = varTmp + 1
            if varTmp == 0:
                l_optimize2.append(l_merger[i])
        # print("去重 => " + str(l_optimize2))

        l_result = l_optimize2
        sum = 0
        for i in range(len(l_result)):
            print(l_result[i])
            sum = sum + int(l_result[i][2])
        print("合计:" + str(sum))

    elif varMenu == "月销售指标数量":
        print("产品销售分析报表（代表） => " + str(varFirstday_of_month) + " 至 " + str(varYesterday) + " 月销售指标数量（" + varName + "）")
        sum = 0
        allRecord = excel_PO.readAllrows("sale_201912.xls")
        l_result = []
        for i in range(1, allRecord):
            l_excel = excel_PO.readRowValue("sale_201912.xls", i, "sheet1")
            if l_excel[3] == varName and l_excel[0] == varProduct :
                 sum = sum + int(l_excel[11])
                 l_result.append(l_excel[0])
                 l_result.append(l_excel[4])
                 l_result.append(l_excel[11])

        l_src = list_PO.oneSplitGroupList(l_result, 3)
        print(l_src)

        # 合并
        l_merger = []
        l_merger = l_src
        for i in range(len(l_merger)):
            for j in range(i + 1, len(l_merger)):
                if l_merger[i][1] == l_merger[j][1]:
                    l_merger[i][2] = int(l_merger[i][2]) + int(l_merger[j][2])
        print("合并 => " + str(l_merger))

        # 去重
        l_optimize2 = []
        if l_optimize2 == []:
            l_optimize2.append(l_merger[0])
        for i in range(len(l_merger)):
            varTmp = 0
            for j in range(len(l_optimize2)):
                if l_merger[i][1] == l_optimize2[j][1]:
                    varTmp = varTmp + 1
            if varTmp == 0:
                l_optimize2.append(l_merger[i])
        print("去重 => " + str(l_optimize2))

        l_result = l_optimize2
        sum = 0
        for i in range(len(l_result)):
            print(l_result[i])
            sum = sum + int(l_result[i][2])
        print("合计:" + str(sum))

    elif varMenu == "当年累计销售数量":
        varTime_firstday_of_year = time_PO.get_firstday_of_month(str(varYesterday).split("-")[0], 1)
        print("产品销售分析报表（代表） => " + varProduct + " " + str(varTime_firstday_of_year) + " 至 " + str(varYesterday) + " 当年累计销售数量（" + varName + "）")
        tblCount = mysql_PO.cur.execute('select product,daibiao,stock from purchase_sale where diqu_uid<>0 and time BETWEEN "%s" AND "%s" and diqu="%s" and product="%s"' % (varTime_firstday_of_year, varYesterday, varName, varProduct))
        database = mysql_PO.cur.fetchall()
        # 原始
        l_src = []
        for i in range(tblCount):
            l_src.append(list(database[i]))
        # print("原始 => " + str(l_src))

        # 合并
        l_merger = []
        l_merger = l_src
        for i in range(len(l_merger)):
            for j in range(i + 1, len(l_merger)):
                if l_merger[i][1] == l_merger[j][1]:
                    l_merger[i][2] = int(l_merger[i][2]) + int(l_merger[j][2])
        # print("合并 => " + str(l_merger))

        # 去重
        l_optimize2 = []
        if l_optimize2 == []:
            l_optimize2.append(l_merger[0])
        for i in range(len(l_merger)):
            varTmp = 0
            for j in range(len(l_optimize2)):
                if l_merger[i][1] == l_optimize2[j][1]:
                    varTmp = varTmp + 1
            if varTmp == 0:
                l_optimize2.append(l_merger[i])
        # print("去重 => " + str(l_optimize2))

        l_result = l_optimize2
        sum = 0
        for i in range(len(l_result)):
            print(l_result[i])
            sum = sum + int(l_result[i][2])
        print("合计:" + str(sum))

    else:
        exit()


    endtime = datetime.datetime.now()
    print("执行了 " + str((endtime - starttime).seconds) + " 秒")

# productSale_representative("依叶", "日销售数量", "刘挺")
# productSale_representative("依叶", "当月累计销售数量", "刘挺")
# productSale_representative("依叶", "月销售指标数量", "刘挺")
# productSale_representative("依叶", "当年累计销售数量", "刘挺")

print("done")
sleep(1212)
# ===================================================================================================================================================
# PC端销售分析报表数据遍历
from instance.zyjk.CRM.PageObject.CrmPO import *
Crm_PO = CrmPO()

# 登录
Crm_PO.login()

# 选择 商务管理 - 销售分析
Level_PO.clickXpath("//div[@类与实例='menu-scroll scroll-down']", 1)
Level_PO.clickXpath("//div[@类与实例='menu-scroll scroll-down']", 1)
Level_PO.clickXpath("//div[@类与实例='menu-scroll scroll-down']", 1)
Level_PO.clickXpath("//div[@类与实例='menu-scroll scroll-down']", 1)
Level_PO.clickXpath("//div[@类与实例='menu-scroll scroll-down']", 1)
Level_PO.clickXpath("//div[@id='m9321']/span", 2)  # 商务管理
Level_PO.clickXpath("//ul[@id='third-menulist-f15881']/li/a", 2)  # 销售分析

# # 净销售分析报表
# print("--------------------------------------  净销售分析报表 --------------------------------------")
# l_net, l_netSale_representativeName = Crm_PO.saleAnalysisReport("净销售分析报表", "")
# print(l_net[1][0])  # 饶顺荣
# print(l_net[1][1])  # {日销售金额}
# print(l_net[1][2])  # {当月累计销售金额}
# print(l_net[1][3])  # {月销售指标金额}
# print(l_net[1][4])  # {月进度}
#
# # 净销售分析报表 之 代表
# l_representative, varTemp = Crm_PO.optRepresentative(l_netSale_representativeName, "净销售分析报表", "饶顺荣", "孙华江")  # 最后一个饶顺荣是代表页里饶顺荣
# print(l_representative[varTemp][0])  # 饶顺荣
# print(l_representative[varTemp][1])  # {日销售金额}
# print(l_representative[varTemp][2])  # {当月累计销售金额}
# print(l_representative[varTemp][3])  # {月销售指标金额}
# print(l_representative[varTemp][4])  # {月进度}
#
# # 净销售分析报表 之 医院
# l_hospital, varTemp = Crm_PO.optHospital(l_netSale_representativeName, "净销售分析报表", "饶顺荣", "上海市第一人民医院-总院")  # 最后一个饶顺荣是医院页里饶顺荣
# print(l_hospital[varTemp][0])  # 饶顺荣
# print(l_hospital[varTemp][1])  # {日销售金额}
# print(l_hospital[varTemp][2])  # {当月累计销售金额}
# print(l_hospital[varTemp][3])  # {月销售指标金额}
# print(l_hospital[varTemp][4])  # {月进度}

def quyu(l_productList, varQuyu):
    for i in range(len(l_productList)):
        if l_productList[i][0] == varQuyu:
            return l_productList[i]


# 产品销售分析报表
print("--------------------------------------  产品销售分析报表 --------------------------------------")
l_productList, l_quyu = Crm_PO.saleAnalysisReport("产品销售分析报表", "依叶")
print(quyu(l_productList, "饶顺荣"))

# print(l_productList[1][0])  # 饶顺荣
# print(l_productList[1][1])  # {日销售金额}
# print(l_productList[1][2])  # {当月累计销售金额}
# print(l_productList[1][3])  # {月销售指标金额}
# print(l_productList[1][4])  # {月进度}

# 净销售分析报表 之 代表
l_representative, varTemp1 = Crm_PO.optRepresentative(l_quyu, "产品销售分析报表", "饶顺荣", "饶顺荣")  # 最后一个饶顺荣是代表页里饶顺荣
print(l_representative[varTemp1])
# print(l_representative[varTemp][0])  # 饶顺荣
# print(l_representative[varTemp][1])  # {日销售金额}
# print(l_representative[varTemp][2])  # {当月累计销售金额}
# print(l_representative[varTemp][3])  # {月销售指标金额}
# print(l_representative[varTemp][4])  # {月进度}

# 净销售分析报表 之 医院
l_hospital, varTemp2 = Crm_PO.optHospital(l_quyu, "产品销售分析报表", "饶顺荣", "饶顺荣")  # 最后一个饶顺荣是医院页里饶顺荣
print(l_hospital[varTemp2])
# print(l_hospital[varTemp][0])  # 饶顺荣
# print(l_hospital[varTemp][1])  # {日销售金额}
# print(l_hospital[varTemp][2])  # {当月累计销售金额}
# print(l_hospital[varTemp][3])  # {月销售指标金额}
# print(l_hospital[varTemp][4])  # {月进度}

if quyu(l_productList, "饶顺荣") == l_representative[varTemp1]  == l_hospital[varTemp2] :
    print("ok")
else:
    print("error")



