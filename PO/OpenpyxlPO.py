# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 202-12-8
# Description   : openpyxl 对象层, 可读写excel for xlsx
# 注意事项：请安装 openpyxl 3.0.0，其他版本如3.0.2使用中会报错。 pip3 install openpyxl == 3.0.0

# Python library to read/write Excel 2007 2010 xlsx/xlsm files
# openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files
# http://openpyxl.readthedocs.org/en/latest/
# https://openpyxl.readthedocs.io/en/stable/usage.html#write-a-workbook
# openpyxl（可读写excel表）专门处理Excel2007及以上版本产生的xlsx文件，xls和xlsx之间转换容易
# 注意：如果文字编码是“gb2312” 读取后就会显示乱码，请先转成Unicode
# openpyxl 的首行、首列 是 （1,1）而不是（0,0）
# NULL空值：对应于python中的None，表示这个cell里面没有数据。
# numberic： 数字型，统一按照浮点数来进行处理。对应于python中的float。
# string： 字符串型，对应于python中的unicode。
# 在默认情况下，openpyxl会将整个xlsx都读入到内存中，方便处理。
# 操作大文件的时候，速度较慢，可以使用Optimized reader和Optimized writer。它们提供了流式的接口，速度更快。
# xlrd 读取大数据的效率比 openpyxl高
# openpyxl , xlsxwriter xlrd xlwt xlutils 下载地址：http://www.python-excel.org/
# 以上这些库都没有提供修改 excel 表格内容功能，一般只能将原excel中的内容读出、做完处理后，再写入一个新的excel文件。
# https://www.debug8.com/python/t_41519.html 常用模块openpyxl
# *********************************************************************

from openpyxl import load_workbook
import openpyxl
import openpyxl.styles
from openpyxl.styles import PatternFill
from datetime import date

from PO.ColorPO import *
Color_PO = ColorPO()
from PO.CharPO import *
Char_PO = CharPO()

'''
1 新建excel newExcel()
2 获取总行数和总列数 l_getTotalRowCol()
3 设置单元格的值 setCellValue()
4 批量设置单元格的值  setMoreCellValue()
5 获取每行数据 l_getRowData()
6 获取每列数据 l_getColData()
7 获取N列的行数据 l_getRowDataByPartCol()
8 获取N列的列数据，可忽略多行 l_getColDataByPartCol()
9 设置单元格背景色 setCellColor()
10 删除行 delRowData()
11 删除列 delColData()
12 清空行 clsRowData()
13 清空列 clsColData()
14 两表比较，输出差异 cmpExcel()
15 获取单元格的值 getCellValue()
'''

class OpenpyxlPO():

    def __init__(self, file):
        self.file = file
        self.wb = openpyxl.load_workbook(self.file)
        # self.wb.sheetnames  # 获取所有的工作表名称
        # # self.nameSizeColor = openpyxl.styles.Font(name="宋体", size=33, color="00CCFF")

    def save(self):
        self.wb.save(self.file)

    def sh(self, varSheet):
        if isinstance(varSheet, int):
            sh = self.wb[self.wb.sheetnames[varSheet]]
            return sh
        elif isinstance(varSheet, str):
            sh = self.wb[varSheet]
            return sh
        else:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")
            exit(0)


    # 1 新建excel（ok）
    def newExcel(self, varFileName, *varSheetName):
        # 新建excel，生成N个工作表（默认一个Sheet1）
        # 注意：如果文件已存在则会先删除后再新建！
        # Openpyxl_PO.newExcel("d:\\444.xlsx")  # 新建excel，默认生成一个工作表Sheet1
        # Openpyxl_PO.newExcel("d:\\444.xlsx", "mySheet1", "mySheet2","mySheet3")  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            if len(varSheetName) == 0:
                ws.title = "Sheet1"
            else:
                ws.title = varSheetName[0]
            for i in range(1, len(varSheetName)):
                wb.create_sheet(varSheetName[i])
            wb.save(varFileName)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    # 2 获取总行数和总列数(ok)
    def l_getTotalRowCol(self, varSheet=0):
        # print(Openpyxl_PO.l_getTotalRowCol())  # [4,3] //返回第1个工作表的总行数和总列数
        # print(Openpyxl_PO.l_getTotalRowCol(1))  # [4,3] //返回第2个工作表的总行数和总列数
        # print(Openpyxl_PO.l_getTotalRowCol("python"))  # [4,3] //返回python工作表的总行数和总列数
        sh = self.sh(varSheet)
        rows = sh.max_row
        columns = sh.max_column
        return [rows, columns]

    # 3 设置单元格的值(ok)
    def setCellValue(self, varRow, varCol, varContent, varSheet=0):
        # Openpyxl_PO.wrtCellValue(5, 3, "777777")  # 对第一个sheet表的第5行第3列写入数据
        # Openpyxl_PO.wrtCellValue(5, 3, "12345678", "python")  # 对python工作表的的第5行第3列写入数据
        try:
            sh = self.sh(varSheet)
            sh.cell(row=varRow, column=varCol, value=varContent)
            # self.wb.save(self.file)
        except:
            Color_PO.consoleColor("31", "31", "[ERROR] ", "call " + sys._getframe(1).f_code.co_name + " (line " + str(
                sys._getframe(1).f_lineno) + ", call " + sys._getframe(
                0).f_code.co_name + " from '" + sys._getframe().f_code.co_filename + "')")

    # 4 批量设置单元格的值(ok)
    def setMoreCellValue(self, varList_Row_Col_Content, varSheet=0):
        # Openpyxl_PO.wrtMoreCellValue([[7, "你好", "测试", "报告"], [9, "再见", "", "好了"]])  # 对第7行第9行分别写入内容
        # Openpyxl_PO.wrtMoreCellValue([[2, "a", "b", "c"], [3, "d", "", "f"]], -1)  # 对最后一个sheet表第2行第3行分别写入内容

        try:
            sh = self.sh(varSheet)
            for i in range(len(varList_Row_Col_Content)):
                for j in range(1, len(varList_Row_Col_Content[i])):
                    sh.cell(row=varList_Row_Col_Content[i][0], column=j, value=varList_Row_Col_Content[i][j])
            # self.wb.save(self.file)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    # 5 获取每行数据(ok)
    def l_getRowData(self, varSheet=0):
        # print(Openpyxl_PO.l_getRowData())
        # print(Openpyxl_PO.l_getRowData("python"))

        l_rowData = []  # 每行数据
        l_allData = []  # 所有行数据
        sh = self.sh(varSheet)
        for cases in list(sh.rows):
            for i in range(len(cases)):
                l_rowData.append(cases[i].value)
            l_allData.append(l_rowData)
            l_rowData = []
        return (l_allData)

    # 6 获取每列数据(ok)
    def l_getColData(self, varSheet=0):
        # print(Openpyxl_PO.l_getColData())
        # print(Openpyxl_PO.l_getColData("python"))

        l_colData = []  # 每列数据
        l_allData = []  # 所有行数据
        sh = self.sh(varSheet)
        for cases in list(sh.columns):
            for i in range(len(cases)):
                l_colData.append(cases[i].value)
            l_allData.append(l_colData)
            l_colData = []
        return (l_allData)

    # 7 获取N列的行数据（ok）
    def l_getRowDataByPartCol(self, l_varCol, varSheet=0):
        # print(Openpyxl_PO.l_getRowDataByPartCol([1, 2, 4]))  # 获取第1，2，4列的行数据
        # print(Openpyxl_PO.l_getRowDataByPartCol([1, 2, 4], -1))  # 获取最后一个工作表的第1，2，4列的行数据

        l_rowData = []  # 每行的数据
        l_allData = []  # 所有的数据
        sh = self.sh(varSheet)
        for row in range(1, sh.max_row + 1):
            try:
                for column in l_varCol:
                    l_rowData.append(sh.cell(row, column).value)
                l_allData.append(l_rowData)
                l_rowData = []
            except:
                print("errorrrrrrrrrr, line " + str(
                    sys._getframe(1).f_lineno) + ", in " + sys._getframe().f_code.co_name + "() ")
                print("建议：参数列表元素不能是0或负数")
                exit(0)

        return l_allData

    # 8 获取N列的列数据，可忽略多行(ok)
    def l_getColDataByPartCol(self, l_varCol, l_varIgnoreRowNum, varSheet=0):
        # print(Openpyxl_PO.l_getColDataByPartCol([1, 3], [1, 2]))  # 获取第二列和第四列的列值，并忽略第1，2行的行值。
        # print(Openpyxl_PO.l_getColDataByPartCol([2], [], "python"))  # 获取第2列所有值。

        l_colData = []  # 每列的数据
        l_allData = []  # 所有的数据
        sh = self.sh(varSheet)
        for col in l_varCol:
            try:
                for row in range(1, sh.max_row):
                    if row not in l_varIgnoreRowNum:
                        l_colData.append(sh.cell(row, col).value)
                l_allData.append(l_colData)
                l_colData = []
            except:
                print("errorrrrrrrrrr, line " + str(
                    sys._getframe(1).f_lineno) + ", in " + sys._getframe().f_code.co_name + "() ")
                print("建议：参数列表元素不能是0或负数")
                exit(0)

        return l_allData

    # 9 设置单元格背景色(ok)
    def setCellColor(self, row, col, varColor, varSheet=0):
        # Openpyxl_PO.setCellColor(6, 7, "FF0000")   将单元格第6行第7列的背景色设置为红色（FF0000）
        # 绿色 = 00E400，黄色 = FFFF00，橙色 = FF7E00，红色 = FF0000，粉色 = 99004C，褐色 =7E0023

        sh = self.sh(varSheet)
        style = PatternFill("solid", fgColor=varColor)
        sh.cell(row, col).fill = style

    # 10 删除行(ok)
    def delRowData(self, varFrom, varSeries=1, varSheet=0):
        # Openpyxl_PO.delRowData(2, 3)  # 删除第2行之连续3行（删除2，3，4行）

        try:
            sh = self.sh(varSheet)
            sh.delete_rows(varFrom, varSeries)  # 删除从某行开始连续varSeries行
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")
            exit(0)

    # 11 删除列(ok)
    def delColData(self, varFrom, varSeries=1, varSheet=0):
        # Openpyxl_PO.delColData(1, 2)  # 删除第1列之连续2列（删除1，2列）
        # Openpyxl_PO.delColData(2, 1, "python")  # 删除第2列之连续1列（删除2列）

        try:
            sh = self.sh(varSheet)
            sh.delete_cols(varFrom, varSeries)  # 删除从某列开始连续varSeries行
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    # 12 清空行(ok)
    def clsRowData(self, varNums, varSheet=0):
        # Openpyxl_PO.clsRowData(2)  # 清空第2行

        try:
            sh = self.sh(varSheet)
            for i in range(sh.max_row):
                sh.cell(row=varNums, column=i + 1, value="")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    # 13 清空列(ok)
    def clsColData(self, varNums, varSheet=0):
        # Openpyxl_PO.clsColData(2)  # 清空第2列
        # Openpyxl_PO.clsColData(1, "python")  # 清空第2列

        try:
            sh = self.sh(varSheet)
            for i in range(sh.max_row):
                sh.cell(row=i + 1, column=varNums, value="")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    # 14 两表比较，输出差异
    def cmpExcel(self, file1, file1Sheet, file2, file2Sheet):
        # 输出的列表中，第一个元素是序号。
        try:
            list1 = self.l_getRowColNums(file1, file1Sheet)
            list2 = self.l_getRowColNums(file2, file2Sheet)
            tmpList1 = []
            tmpList2 = []
            mainList1 = []
            mainList2 = []
            wb = load_workbook(file1)
            wk_sheet = wb[file1Sheet]
            for i in range(1, list1[0] + 1):
                tmpList1.append(i)
                for j in range(1, list1[1] + 1):
                    tmpList1.append(wk_sheet.cell(row=i, column=j).value)
                mainList1.append(tmpList1)
                tmpList1 = []
            # print(mainList1)

            wb = load_workbook(file2)
            wk_sheet = wb[file2Sheet]
            for i in range(1, list2[0] + 1):
                tmpList2.append(i)
                for j in range(1, list1[1] + 1):
                    tmpList2.append(wk_sheet.cell(row=i, column=j).value)
                mainList2.append(tmpList2)
                tmpList2 = []
            # print(mainList2)

            a = [x for x in mainList1 if x in mainList2]  # 两个列表中都存在
            b = [y for y in (mainList1) if y not in a]  # 两个列表中的不同元素，输出 mainList1 中差异部分
            c = [y for y in (mainList2) if y not in a]  # 两个列表中的不同元素，输出 mainList2 中差异部分

            if b == []:
                print("ok，两表一致")
            else:
                return file1, b, file2, c
                # print(file1 + " => " + str(b))
                # print(file2 + " => " + str(c))

        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    # 15 获取单元格值
    def getCellValue(self, varRow, varCol, varSheet=0):
        sh = self.sh(varSheet)
        cell_value = sh.cell(row=varRow, column=varCol).value
        return cell_value


if __name__ == "__main__":

    Openpyxl_PO = OpenpyxlPO("d:\\1.xlsx")


    print("1，新建excel".center(100, "-"))
    # Openpyxl_PO.newExcel("d:\\444.xlsx")  # 新建excel，默认生成一个工作表Sheet1
    # Openpyxl_PO.newExcel("d:\\444.xlsx", "mySheet1", "mySheet2", "mySheet3")  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。

    print("2 获取总行数和总列数".center(100, "-"))
    # print(Openpyxl_PO.l_getTotalRowCol())  # [4,3] //返回第1个工作表的总行数和总列数
    # print(Openpyxl_PO.l_getTotalRowCol(1))  # [4,3] //返回第2个工作表的总行数和总列数
    # print(Openpyxl_PO.l_getTotalRowCol("python"))  # [4,3] //返回python工作表的总行数和总列数

    print("3 设置单元格的值".center(100, "-"))
    # Openpyxl_PO.setCellValue(5, 3, "jinhao")  # 对第一个sheet表的第5行第3列写入数据
    # Openpyxl_PO.setCellValue(5, 3, "12345678", "python")  # 对python工作表的的第5行第3列写入数据
    # Openpyxl_PO.save()

    print("4 批量设置单元格的值".center(100, "-"))
    # Openpyxl_PO.setMoreCellValue([[7, "你好", "测试", "报告"], [9, "再见", "", "好了"]])  # 对第7行第9行分别写入内容
    # Openpyxl_PO.setMoreCellValue([[2, "a", "b", "c"], [3, "d", "", "f"]], -1)  # 对最后一个sheet表第2行第3行分别写入内容
    # Openpyxl_PO.save()

    print("5 获取每行数据".center(100, "-"))
    # print(Openpyxl_PO.l_getRowData())
    # print(Openpyxl_PO.l_getRowData("python"))

    print("6 获取每列数据".center(100, "-"))
    # print(Openpyxl_PO.l_getColData())
    # print(Openpyxl_PO.l_getColData("python"))

    print("7 获取指定列的行数据".center(100, "-"))
    # print(Openpyxl_PO.l_getRowDataByPartCol([1, 2, 4]))   # 获取第1，2，4列的行数据
    # print(Openpyxl_PO.l_getRowDataByPartCol([1, 2, 4], -1))   # 获取最后一个工作表的第1，2，4列的行数据

    print("8 获取某些列的列数据，可忽略多行".center(100, "-"))
    # print(Openpyxl_PO.l_getColDataByPartCol([1, 3], [1, 2]))   # 获取第二列和第四列的列值，并忽略第1，2行的行值。
    # print(Openpyxl_PO.l_getColDataByPartCol([2], [], "python"))  # 获取第2列所有值。

    print("9 设置单元格背景色".center(100, "-"))
    # Openpyxl_PO.setCellColor(11, 1, "00E400")
    # Openpyxl_PO.save()

    print("10 删除行".center(100, "-"))
    # Openpyxl_PO.delRowData(2, 3)  # 删除第2行之连续3行（删除2，3，4行）
    # Openpyxl_PO.save()

    print("11 删除列".center(100, "-"))
    # Openpyxl_PO.delColData(1, 2)  # 删除第1列之连续2列（删除1，2列）
    # Openpyxl_PO.delColData(2, 1, "python")  # 删除第2列之连续1列（删除2列）
    # Openpyxl_PO.save()

    print("12 清空行".center(100, "-"))
    # Openpyxl_PO.clsRowData(2)  # 清空第2行
    # Openpyxl_PO.save()

    print("13 清空列".center(100, "-"))
    # Openpyxl_PO.clsColData(2)  # 清空第2列
    # Openpyxl_PO.clsColData(1, "python")  # 清空第2列
    # Openpyxl_PO.save()

    print("14 两表比较，输出差异".center(100, "-"))
    # file1,list1,file2,list2 = Openpyxl_PO.cmpExcel("d:\\test1.xlsx", "mySheet1", "d:\\test2.xlsx", "mySheet1")
    # print(file1 + ">"*50)
    # for l in list1:
    #     print(l)
    # print("\n" + file2 + ">"*50)
    # for l in list2:
    #     print(l)

    print("15 获取单元格值".center(100, "-"))
    # print(Openpyxl_PO.getCellValue(3, 2))  # 获取第3行第2列的值