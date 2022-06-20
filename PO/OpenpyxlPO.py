# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-12-8
# Description   : openpyxl 对象层
# openpyxl 官网：http://openpyxl.readthedocs.org/en/latest/
# openpyxl 只支持【.xlsx / .xlsm / .xltx / .xltm】格式的文件
# openpyxl 的首行、首列 是 （1,1）而不是（0,0）
# openpyxl 的NULL空值对应于python中的None，表示这个cell里面没有数据。
# openpyxl 的numberic数字型，统一按照浮点数来进行处理，对应于python中的float
# openpyxl 的string字符串型，对应于python中的unicode
# openpyxl 会将整个xlsx读入到内存中，方便处理。
# openpyxl 操作大文件时可使用 Optimized reader 和 Optimized writer 两种模式，它们提供了流式的接口，速度更快，使我们可以用常量级的内存消耗来读取和写入无限量的数据。
#   Optimized reader，打开文件使用use_iterators=True参数，如：wb = load_workbook(filename = 'haggle.xlsx',use_iterators=True)
# openpyxl 读取大数据的效率没有 xlrd 高
# openpyxl 与 xlsxwriter xlrd xlwt xlutils 的比较，这些库都不支持 excel 写操作，一般只能将原excel中的内容读出、做完处理后，再写入一个新的excel文件。
# openpyxl常用模块用法：https://www.debug8.com/python/t_41519.html
# todo: 使用方法
# 基础使用方法：https://blog.csdn.net/four91/article/details/106141274
# 高级使用方法：https://blog.csdn.net/m0_47590417/article/details/119082064
# todo: 安装包
# pip3 install openpyxl == 3.0.0
# 注意！：其他版本（如3.0.2使用中会报错）如有报错，请安装3.0.0
# todo: 报错
# 如：File "src\lxml\serializer.pxi", line 1652, in lxml.etree._IncrementalFileWriter.write TypeError: got invalid input value of type <class 'xml.etree.ElementTree.Element'>, expected string or Element
# 解决方法: pip uninstall lxml   及更新 openpyxl 版本，3.0.7以上
# todo: 乱码
# gb2312 文字编码，在读取后会显示乱码，需转换成 Unicode
# todo: 颜色
# 颜色码对照表（RGB与十六进制颜色码互转） https://www.sioe.cn/yingyong/yanse-rgb-16/
# 绿色 = 00E400，黄色 = FFFF00，橙色 = FF7E00，红色 = FF0000，粉色 = 99004C，褐色 =7E0023,'c6efce = 淡绿', '006100 = 深绿'，'ffffff=白色', '000000=黑色'，'ffeb9c'= 橙色
# todo: 表格列 A，B，C 与 1，2，3 互转
# from openpyxl.utils import get_column_letter,column_index_from_string
# get_column_letter(2)  # 'B'
# column_index_from_string('B')  # 2
# *********************************************************************

from openpyxl import load_workbook
import openpyxl, sys, platform, os
import openpyxl.styles
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, Protection, Alignment
from openpyxl.utils import get_column_letter,column_index_from_string
from datetime import date
from time import sleep
import psutil
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.CharPO import *
Char_PO = CharPO()
from PO.SysPO import *
Sys_PO = SysPO()
from PO.MysqlPO import *

'''
1.1 新建excel  newExcel()
1.2 添加保留工作表  addSheet()
1.3 添加覆盖工作表 addSheetCover()
1.4 删除工作表  delSheet()
1.5 切换工作表 switchSheet() 
1.6 获取所有工作表 getSheet()

2.1 初始化数据 initData()
2.2 设置单元格行高与列宽 setCellDimensions()
2.3 设置工作表所有单元格的行高与列宽 setSheetDimensions()
2.4.1 设置字体类（字体颜色） setFont()
2.4.2 设置填充类（背景色） setFille()
2.4.3 设置边框类 setBorder()
2.4.4 设置位置类 setAlignment()
2.4 设置单元格值 setCellValue()
2.5 设置整行值  setRowValue()
2.6 设置整列值  setColValue()
2.7 设置工作表背景颜色 setSheetColor()
2.8 设置单元格背景色 setCellColor()
2.9 设置整行(可间隔)背景色  setRowColor()
2.10 设置整列(可间隔)背景色  setColColor()
2.11 设置固定单元格  setFreezeCell()
2.12 设置筛选列  setFilterCol()

3.1 获取总行数和总列数 l_getTotalRowCol()
3.2 获取单元格的值 getCellValue()
3.3 获取每行数据 l_getRowValue()
3.4 获取每列数据 l_getColValue()
3.5 获取指定列的行数据 l_getRowValueByPartCol()
3.6 获取某些列的列数据，可忽略多行 l_getColValueByPartCol()
3.7 获取单元格的坐标 getCoordinate()
3.8 获取工作表数据的坐标 getdimensions()

4.1 清空行 clsRow()
4.2 清空列 clsCol()
4.3 删除行 delRow()
4.4 删除列 delCol()

5.1 输出两表差异部分 getDiffValueByXlsxs()
5.2 对一张表的两个sheet进行数据比对，差异数据标注颜色  setCellColorByCmpSheets()

6 将excel表格导入数据库 xlsx2db()
'''

class OpenpyxlPO():

    def __init__(self, file):

        self.file = file
        self.wb = openpyxl.load_workbook(self.file)
        self.wb.sheetnames  # 工作表名称，如 ['北京', 'mySheet1', '上海']
        # self.wb.active  # 获取当前活跃的Worksheet对象
        # print(self.wb.active)  # <Worksheet "北京">
        # self.wb.worksheets  # 以列表的形式返回所有的Worksheet对象，如：[<Worksheet "北京">, <Worksheet "mySheet1">, <Worksheet "上海">]
        # sh2 = self.wb['上海']
        # print(sh2)
        # self.wb.encoding  # 获取文档的字符集编码
        # self.wb.properties  # 获取文档的元数据，如标题，创建者，创建日期等
        # self.wb.active = 0  # 通过索引值设置当前活跃的worksheet

    def getSheets(self):
        return self.wb.sheetnames

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
    def ws(self, active_row):
        '''
        # 废弃
        :param active_row:
        :return:
        '''
        worksheet = self.wb.get_sheet_by_name(self.sh)
        coords = "A" + str(active_row)
        print(coords)
        # worksheet.cell(row=active_row, column=1)
        worksheet.sheet_view.selection[0].activeCell = coords
        worksheet.sheet_view.selection[0].sqref = coords
    def save(self):
        '''
        保存
        '''
        self.wb.save(self.file)
    def open(self, otherFile=0):
        if platform.system() == 'Darwin':
            if otherFile != 0:
                os.system("open " + otherFile)
            else:
                os.system("open " + self.file)
        if platform.system() == 'Windows':
            if otherFile != 0 :
                os.system("start " + otherFile)
            else:
                os.system("start " + self.file)

    def newExcel(self, varFileName, *varSheetName):
        '''
        1.1 新建excel(覆盖)
        :param varFileName: 文件名
        :param varSheetName: N个工作表
        # Openpyxl_PO.newExcel("d:\\444.xlsx")  # 新建excel默认一个Sheet1工作表
        # Openpyxl_PO.newExcel("d:\\444.xlsx", "mySheet1", "mySheet2","mySheet3")  # 新建excel生成三个工作表，默认在第一个mySheet1表。
        # 注意：如果文件已存在则会先删除后再新建！
        '''

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
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


    def addSheet(self, varSheetName, varIndex=0):
        '''
        1.2 添加保留工作表  addSheet()
        :param varSheetName:
        :param varIndex:
        :return:
        # Openpyxl_PO.addSheet("mysheet1")  # 默认在第一个位置上添加工作表
        # Openpyxl_PO.addSheet("mysheet1", 99)   # 当index足够大时，则在最后一个位置添加工作表
        # Openpyxl_PO.addSheet("mysheet1", -1)   # 倒数第二个位置添加工作表
        # 注意：如果工作表名已存在，则保留原工作表。
        '''

        try:
            sign = 0
            for i in self.wb.sheetnames:
                if i == varSheetName:
                    sign = 1
                    break
            if sign == 0:
                self.wb.create_sheet(title=varSheetName, index=varIndex)
                self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def addSheetCover(self, varSheetName, varIndex=0):
        '''
        1.3 添加覆盖工作表 addSheetCover
        :param varSheetName:
        :param varIndex:
        :return:
        # Openpyxl_PO.addSheet("mySheet1")
        # Openpyxl_PO.addSheet("mySheet1", 0 )  # 在第一个工作表前添加工作表
        # Openpyxl_PO.addSheet("mySheet2",99)   # 在第99个位置添加工作表
         Openpyxl_PO.addSheet("mySheet3", -1)   # 在倒数第二个位置添加工作表。
        '''

        try:
            for i in self.wb.sheetnames:
                if i == varSheetName:
                    del self.wb[i]
                    break
            self.wb.create_sheet(title=varSheetName, index=varIndex)
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def delSheet(self, varSheetName):
        '''
        1.4 删除工作表
        :param varSheetName:
        :return:
        # Openpyxl_PO.delSheet("mySheet1")
        # 注意:如果工作表只有1个，则不能删除。
        '''

        try:
            if len(self.wb.sheetnames) > 1:
                for i in self.wb.sheetnames:
                    if i == varSheetName:
                        del self.wb[i]
                        self.save()
            else:
                print("[warning], excel必须保留1个工作表！")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


     # 1.5 qiehua切换工作表
    def switchSheet(self, varSheet):

        varSheet = self.wb[varSheet]
        sh = self.sh(varSheet)



    def initData(self, data, varSheet=0):
        '''
        2.1 初始化保留数据
        :param data:
        :param varSheet:
        :return:
        '''

        try:
            sh = self.sh(varSheet)
            for r in range(len(data)):
                sh.append(data[r])
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setCellDimensions(self, row, rowQty, col, colQty, varSheet=0):
        '''
        2.2 设置单元格行高与列宽
        :param row:
        :param rowQty:
        :param col:
        :param colQty:
        :param varSheet:
        :return:
                # Openpyxl_PO.setCellDimensions(3, 30, 'f', 50)  ， 设置第三行行高30，第f列列宽50
        '''

        try:
            sh = self.sh(varSheet)
            sh.row_dimensions[row].height = rowQty  # 行高
            sh.column_dimensions[col].width = colQty  # 列宽
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setSheetDimensions(self, rowQty, colQty, varSheet=0):
        '''
        2.3 设置工作表所有单元格的行高与列宽
        :param rowQty:
        :param colQty:
        :param varSheet:
        :return:
        '''

        try:
            sh = self.sh(varSheet)
            rows = sh.max_row
            columns = sh.max_column
            for i in range(1, rows+1):
                sh.row_dimensions[i].height = rowQty  # 行高
            for i in range(1, columns+1):
                sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


    def setFont(self, size, color):
        '''
        2.4.1 设置字体类 (字体，字号，粗体，斜体，？，下划线，？，字体颜色)
        :param size:
        :param color:
        :return:
        '''

        try:
            return Font(name=u'微软雅黑', size='' + size + '', bold=False, italic=False, vertAlign='baseline', underline='none',strike=False, color='' + color + '')
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setFille(self, patternType, fgColor):
        '''
        2.4.2 设置填充类，可设置单元格填充颜色等
        :param patternType:
        :param fgColor:
        :return:
         # patternType = {'lightVertical', 'mediumGray', 'lightGrid', 'darkGrid', 'gray125', 'lightHorizontal', 'gray0625','lightTrellis', 'darkUp', 'lightGray', 'darkVertical', 'darkGray', 'solid', 'darkTrellis', 'lightUp','darkHorizontal', 'darkDown', 'lightDown'}
         # return PatternFill(patternType='solid', fgColor='006100')  # 背景色
        '''

        try:
            return PatternFill(patternType='' + patternType + '', fgColor='' + fgColor + '')  # 背景色
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setBorder(self):
        '''
        2.4.3 设置边框类，可以设置单元格各种类型的边框
        # 设置边框样式，上下左右边框
        :return:
        '''

        try:
            return Border(left=Side(style='medium', color='FF000000'), right=Side(style='medium', color='FF000000'),
                          top=Side(style='medium', color='FF000000'), bottom=Side(style='medium', color='FF000000'),
                          diagonal=Side(style='medium', color='FF000000'), diagonal_direction=0,
                          outline=Side(style='medium', color='FF000000'),
                          vertical=Side(style='medium', color='FF000000'),
                          horizontal=Side(style='medium', color='FF000000'))
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setAlignment(self, l_var):
        '''
        2.4.4 设置位置类，可以设置单元格内数据各种对齐方式
        :param l_var:
        :return:
        horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous","distributed",)
        vertical = ("top", "center", "bottom", "justify", "distributed")
        setALignment(['center','top'])
        '''

        try:
            return Alignment(horizontal=l_var[0], vertical=l_var[1])
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setCellValue(self, varRow, varCol, varContent, font, fill, border, alignment, number_format, protection, varSheet=0):
        '''
        2.4 设置单元格值
        :param varRow:  行
        :param varCol:  列
        :param varContent:  值
        :param font: 字体类 (字体，字号，粗体，斜体，？，下划线，？，字体颜色)
        :param fill: 填充类，可设置单元格填充颜色等
        :param border: 边框类，可以设置单元格各种类型的边框
        :param alignment: 位置类、可以设置单元格内数据各种对齐方式
        :param number_format: 格式类，可以设置单元格内各种类型的数据格式
        :param protection: 保护类，可以设置单元格写保护等
        :param varSheet:
        :return:
        '''

        try:
            sh = self.sh(varSheet)
            if font == "" and fill == "" and border == "" and alignment == "" and number_format == "" and protection == "":
                sh.cell(row=varRow, column=varCol, value=varContent)
            else:
                if alignment != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).alignment = alignment
                if font != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).font = font
                if fill != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).fill = fill
                if border != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).border = border
                if alignment != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).alignment = alignment
                if number_format != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).number_format = number_format
                if protection != "":
                    sh.cell(row=varRow, column=varCol, value=varContent).protection = protection
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setRowValue(self, d_var, varSheet=0):
        '''
        2.5 设置整行值
        :param d_var: 字典
        :param varSheet:
        :return:
        # Openpyxl_PO.setRowValue({7:[1,2,3],8:["44",66]})  # 对第7行第9行分别写入内容
        # Openpyxl_PO.setRowValue({7: ["你好", 12345, "7777"], 8: ["44", None, "777777777"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
        '''

        sh = self.sh(varSheet)
        for k, v in d_var.items():
            for i in range(len(v)):
                if v[i] != None:
                    sh.cell(row=k, column=i + 1, value=str(v[i]))
        # self.save()


    def setColValue(self, d_var, varSheet=0):
        '''
        2.6 设置整列值
        :param d_var:
        :param varSheet:
        :return:
        #   Openpyxl_PO.setColValue({"A": ["k1", 666, "777"], "F": ["name", None, "888"]}, -1)
        '''

        try:
            sh = self.sh(varSheet)
            for k, v in d_var.items():
                for i in range(len(v)):
                    if v[i] != None:
                        sh.cell(row=i+1, column=column_index_from_string(k), value=v[i])
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setSheetColor(self, varColor, varSheet=0):
        '''
        2.7 设置工作表背景颜色
        :param varColor:
        :param varSheet:
        :return:
        # Openpyxl_PO.setSheetColor("FF0000")
        '''

        try:
            sh = self.sh(varSheet)
            sh.sheet_properties.tabColor = varColor
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setCellColor(self, row, col, varFillType, varColor, varSheet=0):
        '''
        2.8 设置单元格背景色
        :param row:
        :param col:
        :param varColor:
        :param varSheet:
        :return:
        Openpyxl_PO.setCellColor(6, 7, "solid", "FF0000")   将单元格第6行第7列的背景色设置为红色（FF0000）
        Openpyxl_PO.setCellColor(6, 7, None, "")  消除单元格颜色
        '''

        try:
            sh = self.sh(varSheet)
            rows = sh.max_row
            cols = sh.max_column

            # 清除表格里所有单元格的背景色
            if row == None and col == None:
                style = PatternFill(fill_type=None)
                for i in range(1, rows + 1):
                    for j in range(1, cols + 1):
                        sh.cell(i, j).fill = style
            else:
                if varFillType == None:
                    style = PatternFill(fill_type=None)  # 消除单元格颜色
                else:
                    style = PatternFill(varFillType, fgColor=varColor)
                sh.cell(row, col).fill = style
            self.save()
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setRowColor(self, row, varSkip, varColor, varSheet=0):
        '''
        2.9 设置整行(可间隔)背景色
        :param row:
        :param varColor:
        :param varSheet:
        :return:
        Openpyxl_PO.setRowColor(6, 1, "FF0000")
        '''

        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column

        # 清除表格里所有单元格的背景色
        style = PatternFill(fill_type=None)
        for i in range(1, rows+1):
            for j in range(1, cols+1):
                sh.cell(i, j).fill = style

        style = PatternFill("solid", fgColor=varColor)
        for i in range(row, rows+1, varSkip):
            for j in range(1, cols+1):
                sh.cell(i, j).fill = style
        self.save()


    def setColColor(self, col, varSkip, varColor, varSheet=0):
        '''
        2.9 设置整列(可间隔)背景色
        :param row:
        :param varColor:
        :param varSheet:
        :return:
            Openpyxl_PO.setColColor(6, 1, "FF0000")
        '''

        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column

        style = PatternFill(fill_type=None)  # 消除单元格颜色
        for i in range(1, rows+1):
            for j in range(1, cols+1):
                sh.cell(i, j).fill = style

        style = PatternFill("solid", fgColor=varColor)
        for i in range(1, rows+1):
            for j in range(col, cols+1, varSkip):
                sh.cell(i, j).fill = style
        self.save()




    def setFreezeCell(self, varCell, varSheet=0):
        '''
        2.11 设置固定单元格
        :param varCell:
        :param varSheet:
        :return:
         # 冻结单元格 sheet.freeze_panes
        # 如:Openpyxl_PO.freeze("h2") 表示将a1-h2区间固定（不移动）
        '''

        sh = self.sh(varSheet)
        sh.freeze_panes = varCell

        #
        # coords = "W48"
        # # sh.sheet_view.selection[0].activeCell = coords
        # # sh.sheet_view.selection[0].sqref = coords
        # sh.sheet_view.topLeftCell = coords
        self.save()

    def setFilterCol(self, varCell="all", varSheet=0):
        '''
        2.12 设置筛选列
        :param varCell:
        :param varSheet:
        :return:
        '''
        # .auto_filter.ref = sheet.dimensions 给所有字段添加筛选器；
        #  .auto_filter.ref = "A1" 给 A1 这个格子添加“筛选器”，就是给第一列添加“筛选器
        sh = self.sh(varSheet)
        if varCell == "all":
            sh.auto_filter.ref = sh.dimensions
        else:
            sh.auto_filter.ref = varCell
        self.save()



    def l_getTotalRowCol(self, varSheet=0):
        '''
        3.1 获取总行数和总列数
        :param varSheet:
        :return:
        # print(Openpyxl_PO.l_getTotalRowCol())  # [4,3] //返回第1个工作表的总行数和总列数
        # print(Openpyxl_PO.l_getTotalRowCol(1))  # [4,3] //返回第2个工作表的总行数和总列数
        # print(Openpyxl_PO.l_getTotalRowCol("python"))  # [4,3] //返回python工作表的总行数和总列数
        '''

        try:
            sh = self.sh(varSheet)
            rows = sh.max_row
            cols = sh.max_column
            return [rows, cols]
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def getCellValue(self, varRow, varCol, varSheet=0):
        '''
        3.2 获取单元格的值
        :param varRow:
        :param varCol:
        :param varSheet:
        :return:
        '''
        try:
            sh = self.sh(varSheet)
            cell_value = sh.cell(row=varRow, column=varCol).value
            return cell_value
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def l_getEachRow(self, varSheet=0):
        '''
        3.3 获取每行数据
        :param varSheet:
        :return:
         # print(Openpyxl_PO.l_getEachRow())
        # print(Openpyxl_PO.l_getEachRow("python"))
        '''

        try:
            l_rowData = []  # 每行数据
            l_allData = []  # 所有行数据
            sh = self.sh(varSheet)
            for cases in list(sh.rows):
                for i in range(len(cases)):
                    l_rowData.append(cases[i].value)
                l_allData.append(l_rowData)
                l_rowData = []
            return (l_allData)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def l_getEachCol(self, varSheet=0):
        '''
        3.4 获取每列数据
        :param varSheet:
        :return:
        # print(Openpyxl_PO.l_getEachCol())
        # print(Openpyxl_PO.l_getEachCol("python"))
        '''

        try:
            l_colData = []  # 每列数据
            l_allData = []  # 所有行数据
            sh = self.sh(varSheet)
            for cases in list(sh.columns):
                for i in range(len(cases)):
                    l_colData.append(cases[i].value)
                l_allData.append(l_colData)
                l_colData = []
            return (l_allData)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def l_getRowValueByPartCol(self, l_varCol, varSheet=0):
        '''
        3.5 获取指定列的行数据
        :param l_varCol:
        :param varSheet:
        :return:
        # print(Openpyxl_PO.l_getRowValueByPartCol([1, 2, 4]))  # 获取第1，2，4列的行数据
        # print(Openpyxl_PO.l_getRowValueByPartCol([1, 2, 4], -1))  # 获取最后一个工作表的第1，2，4列的行数据
        '''

        try:
            l_rowData = []  # 每行的数据
            l_allData = []  # 所有的数据
            sh = self.sh(varSheet)
            for row in range(1, sh.max_row + 1):
                for column in l_varCol:
                    l_rowData.append(sh.cell(row, column).value)
                l_allData.append(l_rowData)
                l_rowData = []
            return l_allData
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def l_getColValueByPartCol(self, l_varCol, l_varIgnoreRowNum, varSheet=0):
        '''
        3.6 获取某些列的列数据，可忽略多行
        :param l_varCol:
        :param l_varIgnoreRowNum:
        :param varSheet:
        :return:
        # print(Openpyxl_PO.l_getColValueByPartCol([1, 3], [1, 2]))  # 获取第二列和第四列的列值，并忽略第1，2行的行值。
        # print(Openpyxl_PO.l_getColValueByPartCol([2], [], "python"))  # 获取第2列所有值。
        '''


        l_colData = []  # 每列的数据
        l_allData = []  # 所有的数据
        try:
            sh = self.sh(varSheet)
        except:
            print("[Error], " + varSheet + "不存在！")
            sys.exit(0)
        for col in l_varCol:
            for row in range(1, sh.max_row+1):
                if row not in l_varIgnoreRowNum:
                    l_colData.append(sh.cell(row, col).value)
            l_allData.append(l_colData)
            l_colData = []
        return l_allData


    def getCoordinate(self, varRow, varCol, varSheet=0):
        '''
        3.7 获取单元格的坐标
        :return:
        '''
        try:
            sh = self.sh(varSheet)
            print(sh.dimensions)
            return sh.cell(row=varRow, column=varCol).coordinate

        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def getdimensions(self, varSheet=0):
        '''
        3.8 获取工作表数据的坐标
        :return:
        '''
        try:
            sh = self.sh(varSheet)
            return (sh.dimensions)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(
                sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def l_getOneRow(self, varRow, varSheet=0):
        '''
        3.9 获取某一行数据
        :param varSheet:
        :return:
         # print(Openpyxl_PO.l_getOneRow(1))
        # print(Openpyxl_PO.l_getOneRow("sheet"))
        '''

        list1 = []

        sh = self.sh(varSheet)
        row = [val for val in sh.rows][varRow]  # 获取第一行
        for cel in row:
            list1.append(cel.value)
        return list1




    def clsRow(self, varNums, varSheet=0):
        '''
        4.1 清空行
        :param varNums:
        :param varSheet:
        :return:
           # Openpyxl_PO.clsRow(2)  # 清空第2行
        '''

        try:
            sh = self.sh(varSheet)
            for i in range(sh.max_row):
                sh.cell(row=varNums, column=i + 1, value="")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def clsCol(self, varCol, varSheet=0):
        '''
        4.2 清空列
        :param varCol:
        :param varSheet:
        :return:
        '''
        # 注意：保留标题，从第二行开始清空
        # Openpyxl_PO.clsCol(2)  # 清空第2列
        # Openpyxl_PO.clsCol(1, "python")  # 清空第1列
        try:
            sh = self.sh(varSheet)
            for i in range(sh.max_row-1):
                sh.cell(row=i + 2, column=varCol).value = None
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def delRow(self, varFrom, varSeries=1, varSheet=0):
        '''
        4.3 删除行
        :param varFrom:
        :param varSeries:
        :param varSheet:
        :return:
         # Openpyxl_PO.delRow(2, 3)  # 删除第2行之连续3行（删除2，3，4行）
        '''

        try:
            sh = self.sh(varSheet)
            sh.delete_rows(varFrom, varSeries)  # 删除从某行开始连续varSeries行
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")
            exit(0)

    def delCol(self, varFrom, varSeries=1, varSheet=0):
        '''
        4.4 删除列
        :param varFrom:
        :param varSeries:
        :param varSheet:
        :return:
         # Openpyxl_PO.delCol(1, 2)  # 删除第1列之连续2列（删除1，2列）
        # Openpyxl_PO.delCol(2, 1, "python")  # 删除第2列之连续1列（删除2列）
        '''

        try:
            sh = self.sh(varSheet)
            sh.delete_cols(varFrom, varSeries)  # 删除从某列开始连续varSeries行
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


    def getDiffValueByXlsxs(self, l_file1row, l_file2row):
        '''
        5.1 输出两表差异部分
        :param l_file1row:
        :param l_file2row:
        :return:
            print(Openpyxl_PO.getDiffValueByXlsxs(Openpyxl_PO.l_getRowValue(), Openpyxl_PO2.l_getRowValue()))
            {5: {'loan_amnt': 5000}, 6: {'loan_amnt': 200, 'term': '36 months'}}   表示 第五行，loan_amnt 列的值 5000

        '''

        dictAll = {}
        dict1 = {}
        try:

            if len(l_file1row) == len(l_file2row):
                for i in range(len(l_file1row)):
                    if l_file1row[i] != l_file2row[i]:
                        for j in range(len(l_file1row[i])):
                            if l_file1row[i][j] != l_file2row[i][j]:
                                dict1[l_file1row[0][j]] = l_file1row[i][j]
                                dictAll[i + 1] = dict1
                        dict1 = {}

                if dictAll != []:
                    print(dictAll)
                else:
                    print("[ok], 两列表比对结果一致")
            else:
                print("[warning], 两列表数量不一致！")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def getDiffValueByXlsxs1(self, l_file1row, l_file2row):
        '''
        5.1 输出两表差异部分
        :param l_file1row:
        :param l_file2row:
        :return:
            print(Openpyxl_PO.getDiffValueByXlsxs(Openpyxl_PO.l_getRowValue(), Openpyxl_PO2.l_getRowValue()))
            [[5, 'member_id', 1311441], [7, 'loan_amnt', 5600]]   表示 第五行，member_id列的值1311441
            [[5, 'member_id', 5555], [7, 'loan_amnt', 1200]]
        '''

        list1 = []
        list2 = []
        list11 = []
        list22 = []
        try:
            if len(l_file1row) == len(l_file2row):
                for i in range(len(l_file1row)):
                    if l_file1row[i] != l_file2row[i]:
                        for j in range(len(l_file1row[i])):
                            if l_file1row[i][j] != l_file2row[i][j]:
                                list1.append(i+1)
                                list1.append(l_file1row[0][j])
                                list1.append(l_file1row[i][j])
                                list2.append(i + 1)
                                list2.append(l_file2row[0][j])
                                list2.append(l_file2row[i][j])
                        list11.append(list1)
                        list22.append(list2)
                        list1 = []
                        list2 = []
                if list11 != []:
                    print(list11)
                    print(list22)
                else:
                    print("[ok], 两列表比对结果一致")
            else:
                print("[warning], 两列表数量不一致！")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def setCellColorByCmpSheets(self, varSheet1, varSheet2):
        '''
        5.2 对一张表的两个sheet进行数据比对，差异数据标注颜色
        :param l_file1row:
        :param l_file2row:
        :return:
            前提条件，两sheet表的行列数一致
            Openpyxl_PO.setCellColorByCmpSheets("Sheet1", "Sheet2")

        '''

        l_sheetOneRow = self.l_getRowValue(varSheet1)
        l_sheetTwoRow = self.l_getRowValue(varSheet2)
        try:
            if len(l_sheetOneRow) == len(l_sheetTwoRow):
                for i in range(len(l_sheetOneRow)):
                    if l_sheetOneRow[i] != l_sheetTwoRow[i]:
                        for j in range(len(l_sheetOneRow[i])):
                            if l_sheetOneRow[i][j] != l_sheetTwoRow[i][j]:
                                self.setCellColor(i+1, j+1, "solid", "FF0000")
                                self.setCellColor(i+1, j+1, "solid", "ffeb9c", "Sheet2")
                            else:
                                self.setCellColor(i+1, j+1, None, "", "Sheet1")
                                self.setCellColor(i+1, j+1, None, "", "Sheet2")
                    else:
                        for j in range(len(l_sheetOneRow[i])):
                            self.setCellColor(i + 1, j + 1, None, "", "Sheet1")
                            self.setCellColor(i + 1, j + 1, None, "", "Sheet2")
                self.save()
            else:
                print("[warning], 比对的Sheet中行列数不一致！")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


if __name__ == "__main__":

    # Sys_PO.killPid('EXCEL.EXE')

    Openpyxl_PO = OpenpyxlPO("ExcelPO/fold.xlsx")
    # Openpyxl_PO.delSheet("南京")
    # Openpyxl_PO.addSheetCover("mySheet1", 1)   # 当index足够大时，则在最后一个位置添加工作表

    # print(Openpyxl_PO.getSheets())

    # x= Openpyxl_PO.l_getOneRow(2,"北京")
    # print(x)

    # print("1.1 新建excel ".center(100, "-"))
    # Openpyxl_PO.newExcel("./OpenpyxlPO/newfile2.xlsx", "mySheet1", "mySheet2", "mySheet3")  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。

    # print("1.2 添加保留工作表".center(100, "-"))
    # Openpyxl_PO.addSheet("mySheet1")

    # print("1.3 添加覆盖工作表".center(100, "-"))
    # Openpyxl_PO.addSheetCover("mySheet1", 99)   # 当index足够大时，则在最后一个位置添加工作表

    # print("1.4 删除工作表".center(100, "-"))
    # Openpyxl_PO.delSheet("Sheet1")
    # Openpyxl_PO.delSheet("mySheet1")


    # print("2.1 初始化保留数据".center(100, "-"))
    # Openpyxl_PO.initData([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])   # 保留原有数据，在原数据下生成数据。
    # # Openpyxl_PO.initData([['姓名', '电话', '成绩', '学科'], ['金浩', 13816109050, 119, '语文'], ['Marry', 15201062191, 28, '数学']], "haha")  # 在haha工作表中初始化数据

    # print("2.2 设置单元格行高与列宽".center(100, "-"))
    # Openpyxl_PO.setCellDimensions(3, 30, 'f', 30)

    # print("2.3 设置工作表所有单元格的行高与列宽".center(100, "-"))
    # Openpyxl_PO.setSheetDimensions(30, 20)
    # Openpyxl_PO.open()


    # print("2.4.1 设置字体类（字体颜色）".center(100, "-"))
    # font = Openpyxl_PO.setFont('16', '000000')  # 16号字体颜色
    #
    # print("2.4.2 设置填充类（背景色）".center(100, "-"))
    # fille = Openpyxl_PO.setFille('solid', '006100')  # 单元格背景色
    #
    # print("2.4.3 设置边框类".center(100, "-"))
    # border = Openpyxl_PO.setBorder()  # 黑色直线边框
    #
    # print("2.4.4 设置位置类".center(100, "-"))
    # alignment = Openpyxl_PO.setAlignment(['center', 'top'])  # 文字左右居中，位置在上
    #
    # print("2.4 设置单元格值".center(100, "-"))
    # Openpyxl_PO.setCellValue(1, 6, "jinhao", font, fille, border, "", "", "")  # 引用font和fille对2行6列写入值
    # Openpyxl_PO.setCellValue(1, 6, "jinhao", font, fille, "", "", "", "")  # 引用font和fille对2行6列写入值
    # Openpyxl_PO.setCellValue(2, 4, "upup", font, "", border, "", "", "")
    # Openpyxl_PO.setCellValue(3, 4, "upup", "", "", border, "", "", "")
    # Openpyxl_PO.setCellValue(4, 4, "upup", "", "", "", alignment, "", "")
    # Openpyxl_PO.setCellValue(4, 4, "upup", "", "", "", "", "", "")

    # print("2.5 设置整行值".center(100, "-"))
    # Openpyxl_PO.setRowValue({7: ["你好", 12345, "7777"], 8: ["44", None, "777777777"]})  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
    # Openpyxl_PO.setRowValue({7: ["你好", 12345, "7777"], 8: ["44", "None", "777777777"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容
    # Openpyxl_PO.open()

    # print("2.6 设置整列值".center(100, "-"))
    # Openpyxl_PO.setColValue({"A": ["k1", 666, "777"], "F": ["4456", None, "888"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
    # Openpyxl_PO.open()

    # print("2.7 设置工作表标题选项卡背景颜色".center(100, "-"))
    # Openpyxl_PO.setSheetColor("FF0000")
    # Openpyxl_PO.open()

    # print("2.8 设置单元格背景色".center(100, "-"))
    # Openpyxl_PO.setCellColor(4, 1, None, "", "Sheet1")  # 清除第四行第1列的背景色
    # Openpyxl_PO.setCellColor(5, 1, "solid", "ff0000", "Sheet1")  # 第五行第一列设置红色
    # Openpyxl_PO.setCellColor(None, None, "", "", "Sheet1")  # 清除表格里所有背景色
    # Openpyxl_PO.open()

    # print("2.9 设置整行(可间隔)背景色".center(100, "-"))
    # Openpyxl_PO.setRowColor(5, 1, "ff0000")  # 从第五行开始不间隔地设置每行颜色为红色
    # Openpyxl_PO.setRowColor(3, 2, "ff0000")  # 从第3行开始每隔1行设置每行颜色为红色

    # print("2.10 设置整列(可间隔)背景色".center(100, "-"))
    # Openpyxl_PO.setColColor(2, 1, "ff0000")  # 从第2列开始不间隔地设置每列颜色为红色
    # Openpyxl_PO.setColColor(2, 2, "ff0000")  # 从第2行开始每隔1列设置颜色为红色



    # print("3.1 获取总行数和总列数".center(100, "-"))
    # print(Openpyxl_PO.l_getTotalRowCol())  # [4,3] //返回第1个工作表的总行数和总列数
    # # print(Openpyxl_PO.l_getTotalRowCol(1))  # [4,3] //返回第2个工作表的总行数和总列数
    # # print(Openpyxl_PO.l_getTotalRowCol("python"))  # [4,3] //返回python工作表的总行数和总列数

    # print("3.2 获取单元格值".center(100, "-"))
    # print(Openpyxl_PO.getCellValue(3, 2))  # 获取第3行第2列的值


    # print("3.3 获取每行数据".center(100, "-"))
    # print(Openpyxl_PO.l_getEachRow())
    # # print(Openpyxl_PO.l_getEachRow("python"))
    #
    # print("3.4 获取每列数据".center(100, "-"))
    # print(Openpyxl_PO.l_getEachCol())
    # # print(Openpyxl_PO.l_getEachCol("python"))
    #
    # print("3.5 获取指定列的行数据".center(100, "-"))
    # print(Openpyxl_PO.l_getRowValueByPartCol([2]))   # 获取第1，2，4列的行数据
    # # print(Openpyxl_PO.l_getRowValueByPartCol([1, 2, 4], -1))   # 获取最后一个工作表的第1，2，4列的行数据
    #
    # print("3.6 获取某些列的列数据，可忽略多行".center(100, "-"))
    # print(Openpyxl_PO.l_getColValueByPartCol([1, 3], [1, 2]))   # 获取第二列和第四列的列值，并忽略第1，2行的行值。
    print(Openpyxl_PO.l_getColValueByPartCol([2], [], "上海"))  # 获取第2列所有值。

    # print("3.7 获取单元格的坐标".center(100, "-"))
    # print(Openpyxl_PO.getCoordinate(2, 5))   # E2

    # print("3.8 获取工作表数据的坐标".center(100, "-"))
    # print(Openpyxl_PO.getdimensions())  # A1:E17


    # print("4.1 清空行".center(100, "-"))
    # # Openpyxl_PO.clsRow(2)  # 清空第2行
    # Openpyxl_PO.save()
    #
    # print("4.2 清空列".center(100, "-"))
    # # Openpyxl_PO.clsCol(2)  # 清空第2列
    # # Openpyxl_PO.clsCol(1, "python")  # 清空第2列
    # # Openpyxl_PO.save()

    # print("4.3 删除行".center(100, "-"))
    # # Openpyxl_PO.delRow(2, 3)  # 删除第2行之连续3行（删除2，3，4行）
    # # Openpyxl_PO.save()
    #
    # print("4.4 删除列".center(100, "-"))
    # # Openpyxl_PO.delCol(1, 2)  # 删除第1列之连续2列（删除1，2列）
    # # Openpyxl_PO.delCol(2, 1, "python")  # 删除第2列之连续1列（删除2列）
    # # Openpyxl_PO.save()


    # print("5.1 输出两表差异部分 ".center(100, "-"))
    # Openpyxl_PO = OpenpyxlPO("./data/loanStats.xlsx")
    # Openpyxl_PO2 = OpenpyxlPO("./data/loanStats2.xlsx")
    # Openpyxl_PO.getDiffValueByXlsxs(Openpyxl_PO.l_getRowValue(), Openpyxl_PO2.l_getRowValue("Sheet2"))
    # Openpyxl_PO.open()
    
    # print("5.2 对一张表的两个sheet进行数据比对，差异数据标注颜色 ".center(100, "-"))
    # Openpyxl_PO.setCellColorByCmpSheets("Sheet1", "Sheet2")
    # Openpyxl_PO.open()

