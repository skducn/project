# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-12-9
# Description:  质控报告 EHR对象库
# *****************************************************************

from PO.OpenpyxlPO import *
import sys,os
from PO.StrPO import *
Str_PO = StrPO()
from PO.ColorPO import *
Color_PO = ColorPO()

class ReportPO():

    def __init__(self):
        self.Openpyxl_PO = OpenpyxlPO("v2.xlsx")

    def colResult(self, l_param, varDot):

        ''' 表格列表达式 '''
        # colResult(["表1.电子健康档案建档率", "=", "辖区内常住人口建立电子健康档案人数", "/", "辖区内常住人口数"])

        print(l_param[0] + "(done)")
        # 目标列
        try:
            destSheetName = str(l_param[0]).split(".")[0]
            destTestResult = str(l_param[0]).split(".")[1]  # 电子健康档案建档率
            allData = self.Openpyxl_PO.l_getRowData(destSheetName)  # 表1
            for i in range(len(allData[0])):
                if allData[0][i] == destTestResult:
                    destTestResult = i
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")
            exit(0)

        # 逻辑列
        sum = ""
        l_param.pop(0)
        l_param.pop(0)
        # print(l_param)  # ['辖区内常住人口建立电子健康档案人数', '/', '辖区内常住人口数', '*100']  =》 "allData[i][3]/allData[i][2]*100"
        for i in range(len(l_param)):
            if "." in str(l_param[i]) and Str_PO.isContainChinese(l_param[i]):
                srcSheetName = str(l_param[i]).split(".")[0]  # 表1
                src1 = str(l_param[i]).split(".")[1]  # 辖区内常住人口建立电子健康档案人数
            else:
                src1 = l_param[i]  # 辖区内常住人口建立电子健康档案人数
                for j in range(len(allData[0])):
                    if allData[0][j] == src1:
                        src1 = "allData[i][" + str(j) + "]"
                        break
            sum = sum + src1
            src1 = ""
        # print(sum)  # allData[i][3]/allData[i][2]*100

        # 测试
        for i in range(1, len(allData)):
            # if round((allData[i][3])/(allData[i][2]) * 100, 2) == round(allData[i][4], 2):
            if varDot == "取整":
                if round(allData[i][destTestResult], 2) == int(eval(sum)):
                    # print("[ok] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)))
                    self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "00E400", destSheetName)
                else:
                    Color_PO.consoleColor("31", "31", "[ERROR] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(int(eval(sum))), "")
                    # print("[error] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(int(eval(sum))))
                    self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "FF0000", destSheetName)
            else:
                if round(allData[i][destTestResult], 2) == round(eval(sum), 2):
                    # print("[ok] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)))
                    self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "00E400", destSheetName)
                else:
                    Color_PO.consoleColor("31", "31", "[ERROR] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(round(eval(sum), 2)),"")
                    # print("[error] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(round(eval(sum), 2)))
                    self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "FF0000", destSheetName)


    def save(self):
        self.Openpyxl_PO.save()