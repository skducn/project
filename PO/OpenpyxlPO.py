# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-12-8
# Description   : openpyxl 对象层
# openpyxl 官网：http://openpyxl.readthedocs.org/en/latest/
# 支持.xlsx / .xlsm / .xltx / .xltm格式的文件
# 首行、首列 是 （1,1）而不是（0,0）
# NULL空值 = python中的None，表示这个cell里面没有数据。
# numberic数字型 = python中的float
# string字符串型 = python中的unicode
# openpyxl 会将整个xlsx读入到内存中，方便处理。
# openpyxl 操作大文件时可使用 Optimized reader 和 Optimized writer 两种模式，它们提供了流式的接口，速度更快，使我们可以用常量级的内存消耗来读取和写入无限量的数据。
# Optimized reader 可用 use_iterators=True参数打开，如：wb = load_workbook(filename = 'haggle.xlsx',use_iterators=True)
# openpyxl 读取大数据的效率没有 xlrd 高。
# xlsxwriter xlrd xlwt xlutils 这些库都不支持 excel 写操作，一般只能将原excel中的内容读出、做完处理后，再写入一个新的excel文件。
# 扩展学习 xlwings https://blog.csdn.net/qfxietian/article/details/123822358

# todo: 使用方法
# 参考：openpyxl常用模块用法 https://www.debug8.com/python/t_41519.html
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
from openpyxl.utils import get_column_letter, column_index_from_string
# get_column_letter(2)  # 'B'
# a = column_index_from_string('B')  # 2
# *********************************************************************

from openpyxl import load_workbook
import openpyxl, sys, platform, os
import openpyxl.styles
from openpyxl.styles import (
    Font,
    PatternFill,
    GradientFill,
    Border,
    Side,
    Alignment,
    Protection,
    Alignment,
)
from openpyxl.utils import get_column_letter, column_index_from_string
from datetime import date
from time import sleep
import psutil
import xlwings as xw

from PO.ColorPO import *
Color_PO = ColorPO()
from PO.CharPO import *
Char_PO = CharPO()
from PO.SysPO import *
Sys_PO = SysPO()
from PO.ListPO import *
List_PO = ListPO()

from PO.MysqlPO import *


"""
1.1 新建 newExcel("./OpenpyxlPO/newfile2.xlsx", "mySheet1", "mySheet2", "mySheet3") 
1.2 打开 open()
1.3 获取所有工作表 getSheets()
1.4 操作工作表 sh()
1.5 切换工作表 switchSheet("Sheet2") 
1.6 添加不覆盖工作表 addSheet("Sheet1")
1.7 添加覆盖工作表 addCoverSheet("Sheet1", 1) 
1.8 删除工作表 delSheet("Sheet1")
1.9 保存 save()

2.0.1 在第N行前插入多行空白 insertNullRows(3, 5) 在第3行前插入5行空白
2.0.2 在第N列前插入多列空白 insertNullCols(3) 在第3列前插入1列空白
2.1 更新单元格值 setCell(1, 2, "hello") 等同于 Openpyxl_PO.setCell(1, 'B', "hello")

2.2 插入行数据 insertRows({1: ["100", 101, "102"], 5: ["444", "123", "666"]})
2.3 更新行数据 setRows({7: ["200", 222, "555"], 8: ["777", "345", "888"]})
2.4 追加行数据 appendRows([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])

2.5 插入列数据 insertCols({"a": ["姓名", "张三", "李四"], "c": ["年龄", "55", "34"]})
2.6 更新列数据 setCols({"A": ["公司", "百度", "天猫"], "F": ["学校", "清华大学", "北京大学"]})
2.7 追加列数据 appendCols([["姓名", "张三", "李四"], ["年龄", "55", "34"]])

2.5 设置单元格行高与列宽 setCellDimensions(3, 30, 'f', 30) //设置第三行行高30，第f列列宽50
2.6 设置工作表所有单元格的行高与列宽 setAllCellDimensions(30, 20) //设置所有单元格高30，宽50
2.7 设置所有单元格自动换行 setAllWordWrap()
2.8 设置冻结首行 setFreeze('A2'）
2.9 设置单元格对齐样式  setCellAlignment(5, 4, 'center', 'center')
2.9.2 设置单行多列对齐样式 setRowColAlignment(5, [1,4], 'center', 'center')
2.9.3 设置所有单元格对齐样式 setAllCellAlignment('center', 'center')
2.10 设置筛选列  setFilterCol("all") # 全部筛选, setFilterCol("") # 取消筛选 , setFilterCol("A2") # 对A2筛选 
2.11 设置单元格字体（字体、字号、粗斜体、下划线、颜色） setCellFont(1, 1, name=u'微软雅黑', size=16, bold=True, italic=True, color="000000")
2.11.2 设置单行多列字体  setRowColFont(1, [1, 5])
2.11.3 设置所有单元格字体  setAllCellFont(color="000000")
2.12 设置单元格边框 setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])
2.13 设置单元格填充背景色 setPatternFill(2, 2, 'solid', '006100')
2.14 设置单元格填充渐变色 setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])
2.15 设置单元格背景色 setCellColor(1, 1, "ff0000")  # 第1行第一列设置红色
2.15.2 设置单行多列背景色 setRowColColor(5, ['b', 'd'], "ff0000")
2.15.3 设置所有单元格背景色 setAllCellColor("ff0000")
2.16 设置整行(可间隔)背景色  setRowColor(3, 1, "ff0000")  # 从第3行开始每隔1行颜色标红色
2.17 设置整列(可间隔)背景色  setColColor(2, 1, "ff0000")  # 从第2列开始每隔1列设置颜色为红色
2.18 设置工作表背景颜色 setSheetColor("FF0000")

3.1 获取总行列数 getTotalRowCol()  # [5,10]
3.2 获取单元格的值 getCell(3,2)
3.3 获取一行数据 getOneRow(2) # 获取第2行值
3.4 获取一列数据 getOneCol(2) 或 getOneCol('B') # 获取第2列值
3.5.1 获取行数据 getRow()  # [['状态', '名字'],['ok', 'jinhao']...]
3.5.2 获取带行号的行数据 getRowBySeq()  # { 2 : ['状态', '名字'], 3 : ['ok', 'jinhao']...}
3.5.3 获取部分列的行数据 getRowByCol([1, 3])  # 获取第1，3列的行数据 [['Number具体数', 'jinhaoyoyo'], [2, 30], [3, 25]...]
    支持序号与字母混搭 getRowByCol(["A", "C"])， getRowByCol([2, "C"])
    支持去重 getRowByCol([1, 3, 2, "a", "C", "B"])
3.5.4 获取带行号的部分列的行数据 getRowByColSeq([1, 3])  # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25]...}
     getRowByColSeq([1, 'c']) 同上  

3.6.1 获取每列数据 getCol()
3.6.2 获取带列序号的每列数据 getColBySeq()  # { 2 : ['状态', '名字'], 3 : ['ok', 'jinhao']...}
3.6.3 获取带列字母的每列数据 getColByLetter()  # { 'a' : ['状态', '名字'], 'b' : ['ok', 'jinhao']...}

	
3.8.1 获取标题的序号 getTitleColSeq(['测试'，‘开发’])  # [2，4]
3.8.2 获取标题的字母 getTitleColLetter(['测试'，‘开发’])  # ['A', 'C']
3.8.3 将标题转列字典序列 title2dictSeq（['测试'，‘开发’]）# {2: '姓名', 5: '性别'}
3.8.4 将标题转列字典字母 title2dictLetter（['测试'，‘开发’]）# {'B': '姓名', 'E': '性别'}

3.9 获取部分列的列值(可忽略多行) getColByPartialColByUnwantedRow([1, 3], [1, 2]))   # 获取第二列和第四列的列值，并忽略第1，2行的行值。
3.10 获取单元格的坐标 getCellCoordinate(2, 5))   # E2
3.11 获取所有数据的坐标 getDimensions())  # A1:E17


4.1 清空行 clsRow(2)  # 清空第2行
4.2 清空列 clsCol(2)  # 清空第2列
4.2.1 清空列保留标题 clsColRetainTitle(2)  # 清空第2列
4.3 删除连续行 delSeriesRow(2, 3)  # 删除从第二行开始连续三行数据 （即删除2，3，4行）
4.4 删除连续列 delSeriesCol(2, 3)  # 删除从第二列开始连续三列数据 （即删除2，3，4列）
4.

5.1 两表比较，获取差异内容（两表标题与行数必须一致）getDiffValueByCmp(Openpyxl_PO.getRow("Sheet2"), Openpyxl_PO2.getRow("Sheet2"))
5.2 两工作表比较，对差异内容标注颜色 setColorByDiff("Sheet1", "Sheet2")
 
6 移动范围数据 moveValue(rows, cols, 'C1:D2')

7 将excel中标题（第一行字段）排序（从小打大）sortFields()

"""


class OpenpyxlPO:

    def __init__(self, file):

        self.file = file
        if self.file != "":
            self.wb = openpyxl.load_workbook(self.file)
        # self.wb.sheetnames
        # self.wb.active  # 获取当前活跃的Worksheet对象
        # print(self.wb.active)  # <Worksheet "北京">
        # self.wb.worksheets  # 以列表的形式返回所有的Worksheet对象，如：[<Worksheet "北京">, <Worksheet "mySheet1">, <Worksheet "上海">]
        # sh2 = self.wb['上海']
        # print(sh2)
        # self.wb.encoding  # 获取文档的字符集编码
        # self.wb.properties  # 获取文档的元数据，如标题，创建者，创建日期等
        # self.wb.active = 0  # 通过索引值设置当前活跃的worksheet

    # todo [工作表]

    # def newExcel(self, varFileName, *varSheetName):
    # 
    #     # 1.1 新建excel(覆盖)
    #     # Openpyxl_PO.newExcel("d:\\444.xlsx")  # 新建excel默认一个Sheet1工作表
    #     # Openpyxl_PO.newExcel("d:\\444.xlsx", "mySheet1", "mySheet2","mySheet3")  # 新建excel生成三个工作表，默认在第一个mySheet1表。
    #     # 注意：如果文件已存在则会先删除后再新建。
    #     wb = openpyxl.Workbook()
    #     ws = wb.active
    #     if len(varSheetName) == 0:
    #         ws.title = "Sheet1"
    #     else:
    #         ws.title = varSheetName[0]
    #     for i in range(1, len(varSheetName)):
    #         wb.create_sheet(varSheetName[i])
    #     wb.save(varFileName)

    def newExcel(self, varFileName, l_sheetName):

        '''
        1.1 新建excel(覆盖)
        :param varFileName: 
        :param l_sheetName: 
        :return: 
        # Openpyxl_PO.newExcel("d:\\444.xlsx")  # 新建excel默认一个Sheet1工作表
        # Openpyxl_PO.newExcel("d:\\444.xlsx", ["mySheet1", "mySheet2","mySheet3"])  # 新建excel生成三个工作表，默认在第一个mySheet1表。
        # 注意：如果文件已存在则会先删除后再新建。
        '''

        wb = openpyxl.Workbook()
        ws = wb.active
        if len(l_sheetName) == 1:
            ws.title = "Sheet1"
        else:
            ws.title = l_sheetName[0]
        for i in range(1, len(l_sheetName)):
            wb.create_sheet(l_sheetName[i])
        wb.save(varFileName)

    def open(self, varSheet=0):

        '''
        1.2 打开
        :param otherFile: 
        :return:
            # Openpyxl_PO.open(1) # 打开第二个工作表
            # Openpyxl_PO.open() # 打开第一个工作表
            # Openpyxl_PO.open('test')  # 打开test工作表
        '''

        self.switchSheet(varSheet)
        if platform.system() == "Darwin":
            os.system("open " + self.file)
        if platform.system() == "Windows":
            os.system("start " + self.file)


    def getSheets(self):

        '''
        1.3 获取所有工作表
        如 ['mySheet1', 'mySheet2', 'mySheet3']
        :return: 
        '''
        return self.wb.sheetnames

    def sh(self, varSheet):

        '''
        1.4 操作工作表
        :param varSheet: 
        :return: 
        '''
        
        if isinstance(varSheet, int):
            sh = self.wb[self.wb.sheetnames[varSheet]]
            return sh
        elif isinstance(varSheet, str):
            sh = self.wb[varSheet]
            return sh
        else:
            exit(0)

    def switchSheet(self, varSheet=0):
        
        '''
        1.5 切换工作表
        # switchSheet("Sheet2")
        :param varSheet: 
        :return: 
        '''

        # self.wb[varSheet]
        self.wb.active = self.sh(varSheet)
        for sheet in self.wb:
            if sheet.title == varSheet:
                sheet.sheet_view.tabSelected = True
            else:
                sheet.sheet_view.tabSelected = False
        self.save()

        # return self.wb[varSheet]

    def addSheet(self, varSheetName, varIndex=0):
    
        '''
        1.6 添加不覆盖工作表
        # Openpyxl_PO.addSheet("mysheet1")  # 默认在第一个位置上添加工作表
        # Openpyxl_PO.addSheet("mysheet1", 99)   # 当index足够大时，则在最后一个位置添加工作表
        # Openpyxl_PO.addSheet("mysheet1", -1)   # 倒数第二个位置添加工作表
        # 注意：如果工作表名已存在，则不添加工作表，即保留原工作表。
        :param varSheetName: 
        :param varIndex: 
        :return: 
        '''
        
        sign = 0
        for i in self.wb.sheetnames:
            if i == varSheetName:
                sign = 1
                break
        if sign == 0:
            self.wb.create_sheet(title=varSheetName, index=varIndex)
            self.save()

    def addCoverSheet(self, varSheetName, varIndex=0):
        
        '''
        # 1.7 添加工作表(覆盖)
        # Openpyxl_PO.addCoverSheet("mySheet1")
        # Openpyxl_PO.addCoverSheet("mySheet1", 0 )  # 在第一个工作表前添加工作表
        # Openpyxl_PO.addCoverSheet("mySheet2",99)   # 在第99个位置添加工作表
        # Openpyxl_PO.addCoverSheet("mySheet3", -1)   # 在倒数第二个位置添加工作表。
        :param varSheetName: 
        :param varIndex: 
        :return: 
        '''
        
        for i in self.wb.sheetnames:
            if i == varSheetName:
                del self.wb[i]
                break
        self.wb.create_sheet(title=varSheetName, index=varIndex)
        self.save()

    def delSheet(self, varSheetName):

        '''
        # 1.8 删除工作表
        # Openpyxl_PO.delSheet("mySheet1")
        # 注意:如果工作表只有1个，则不能删除。
        :param varSheetName:
        :return:
        '''

        if len(self.wb.sheetnames) > 1:
            for i in self.wb.sheetnames:
                if i == varSheetName:
                    del self.wb[i]
                    self.save()
        else:
            print("[warning], excel必须保留1个工作表！")

    def save(self):

        '''
        1.9 保存
        :return:
        '''
        self.wb.save(self.file)



    # todo [设置]

    def insertNullRows(self, seq, moreRow=1, varSheet=0):

        '''
        2.0.1 在第N行前插入多行空白
        :param seq:
        :param moreRow:
        :param varSheet:
        :return:
        insertNullRows(3)  在第3行前插入1行空白
        insertNullRows(3，5)  在第3行前插入5行空白
        '''

        sh = self.sh(varSheet)
        sh.insert_rows(idx=seq, amount=moreRow)
        self.save()

    def insertNullCols(self, varCol, moreCol=1, varSheet=0):

        '''
        2.0.2 在第N列前插入多列空白
        :param seq:
        :param moreRow:
        :param varSheet:
        :return:
        insertNullCols(3)  在第3列前插入1列空白
        insertNullCols(3，5)  在第3列前插入5列空白
        '''

        sh = self.sh(varSheet)
        if isinstance(varCol, int):
            sh.insert_cols(idx=varCol, amount=moreCol)
        else:
            sh.insert_cols(idx=column_index_from_string(varCol), amount=moreCol)
        self.save()

    def setCell(self, varRow, varCol, varContent, varSheet=0):

        # 2.1 设置单元格值
        # e.g.setCell(2,"b","123")  # 将第二行B列的值改为123
        sh = self.sh(varSheet)
        if isinstance(varCol, str):
            varCol = column_index_from_string(varCol)  # 将'B'转换成2
        sh.cell(row=varRow, column=varCol, value=varContent)
        self.save()


    def insertRows(self, d_var, varSheet=0):

        '''2.2 插入行数据'''

        for k, v in d_var.items():
            self.insertNullRows(int(k), varSheet=varSheet)
        self.setRows(d_var, varSheet=varSheet)

    def setRows(self, d_var, varSheet=0):

        '''
        # 2.3 更新行数据
        # Openpyxl_PO.setRows({7:[1,2,3],8:["44",66]})  # 更新第7、8行内容
        # Openpyxl_PO.setRows({7: ["你好", 12345, "7777"], 8: ["44", None, "777777777"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
        :param d_var:
        :param varSheet:
        :return:
        '''

        sh = self.sh(varSheet)
        for k, v in d_var.items():
            for i in range(len(v)):
                if v[i] != None:
                    sh.cell(row=k, column=i + 1, value=str(v[i]))
        self.save()

    def appendRows(self, l_l_rows, varSheet=0):

        '''
        2.4 追加行数据
        appendRows([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])
        :param l_l_rows:
        :param varSheet:
        :return:
        '''

        sh = self.sh(varSheet)
        for r in range(len(l_l_rows)):
            sh.append(l_l_rows[r])
        self.save()


    def insertCols(self, d_var, varSheet=0):

        '''
        2.5 插入列数据".center(100, "-"))
        Openpyxl_PO.insertCols({1: ["姓名", "张三", "李四"], 5: ["年龄", "55", "34"]})
        :param d_var:
        :param varSheet:
        :return:
        '''

        for k, v in d_var.items():
            self.insertNullCols(k, varSheet=varSheet)
        self.setCols(d_var, varSheet=varSheet)

    def setCols(self, d_var, varSheet=0):

        # 2.3 设置整列值
        # Openpyxl_PO.setCols({"A": ["k1", 666, "777"], "F": ["name", None, "888"]}, -1)
        # Openpyxl_PO.setCols({3: ["k1", 666, "777"], 4: ["name", None, "888"]}, -1)
        sh = self.sh(varSheet)
        for k, v in d_var.items():
            for i in range(len(v)):
                if v[i] != None and k.isalpha():
                    sh.cell(row=i + 1, column=column_index_from_string(k), value=v[i])
                elif v[i] != None and k.isdigit():
                    sh.cell(row=i + 1, column=int(k), value=v[i])
        self.save()

    def appendCols(self, l_l_cols, varSheet=0):

        '''
        2.7 追加列数据
        :param l_l_cols:
        :param varSheet:
        :return:
        '''
        l_colLetter = []
        l_row_col = self.getTotalRowCol(varSheet=varSheet)
        totalCol = l_row_col[1]
        for i in range(len(l_l_cols)):
            l_colLetter.append(get_column_letter(totalCol+i+1))
        # print(l_colLetter)
        d = List_PO.twoList2dict(l_colLetter, l_l_cols)
        self.setCols(d)

    def setCellDimensions(self, row, rowQty, col, colQty, varSheet=0):

        # 2.5 设置单元格行高与列宽
        # Openpyxl_PO.setCellDimensions(3, 30, 'f', 50) //第三行行高30，第f列列宽50
        sh = self.sh(varSheet)
        sh.row_dimensions[row].height = rowQty  # 行高
        sh.column_dimensions[col].width = colQty  # 列宽
        self.save()

    def setRowColDimensions(self, row, rowQty, l_col, colQty, varSheet=0):

        # 2.5.2 设置单行多列行高与列宽
        # Openpyxl_PO.setRowColDimensions(5, 30, ['f', 'h'], 30)  #
        sh = self.sh(varSheet)
        cols = sh.max_column
        sh.row_dimensions[row].height = rowQty  # 行高
        if l_col == "all":
            for i in range(1, cols + 1):
                sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
        else:
            # print(column_index_from_string(l_col[0]))  # 6
            # print(column_index_from_string(l_col[1]))  # 8
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
        self.save()

    def setAllCellDimensions(self, rowQty, colQty, varSheet=0):

        # 2.6 设置所有单元格的行高与列宽
        sh = self.sh(varSheet)
        rows = sh.max_row
        columns = sh.max_column
        for i in range(1, rows + 1):
            sh.row_dimensions[i].height = rowQty  # 行高
        for i in range(1, columns + 1):
            sh.column_dimensions[get_column_letter(i)].width = colQty  # 列宽
        self.save()

    def setAllCellDimensionsHeight(self, rowQty, varSheet=0):

        # 2.6 设置所有单元格的行高与列宽
        sh = self.sh(varSheet)
        rows = sh.max_row
        columns = sh.max_column
        for i in range(1, rows + 1):
            sh.row_dimensions[i].height = rowQty  # 行高
        self.save()

    def setAllWordWrap(self, varSheet=0):

        # 2.7 设置所有单元格自动换行
        sh = self.sh(varSheet)
        # print(list(sh._cells.keys())) # [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 1), (6, 2), (6, 3), (7, 1), (7, 2), (7, 3)]
        for key in list(sh._cells.keys()):
            sh._cells[key].alignment = Alignment(wrapText=True)
        self.save()

    def setFreeze(self, coordinate, varSheet=0):

        # 2.8 冻结窗口
        # setFreeze('A2'）
        sh = self.sh(varSheet)
        sh.freeze_panes = coordinate
        self.save()

    def setCellAlignment(
        self,
        row,
        col,
        horizontal="center",
        vertical="center",
        text_rotation=0,
        wrap_text=False,
        varSheet=0,
    ):

        # 2.9 设置单元格对齐样式
        # Openpyxl_PO.setCellAlignment(5, 4, 'center', 'top')
        # Openpyxl_PO.setCellAlignment(5, "f", 'center', 'top')
        # Alignment(horizonta水平对齐模式, vertical=垂直对齐模式, text_rotation=旋转角度, wrap_text=是否自动换行)
        # horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed",)
        # vertical = ("top", "center", "bottom", "justify", "distributed")
        sh = self.sh(varSheet)
        if isinstance(col, int):
            sh.cell(row=row, column=col).alignment = Alignment(
                horizontal=horizontal,
                vertical=vertical,
                text_rotation=text_rotation,
                wrap_text=wrap_text,
            )
        else:
            sh.cell(row, column_index_from_string(col)).alignment = Alignment(
                horizontal=horizontal,
                vertical=vertical,
                text_rotation=text_rotation,
                wrap_text=wrap_text,
            )
        self.save()

    def setRowColAlignment(
        self,
        row,
        l_col,
        horizontal="center",
        vertical="center",
        text_rotation=0,
        wrap_text=False,
        varSheet=0,
    ):

        # 2.9.2 设置单行多列对齐样式
        # Openpyxl_PO.setRowColAlignment(1, [4, 6], 'center', 'center')  # 第一行第四五六列居中
        # Openpyxl_PO.setRowColAlignment(9, "all", 'center', 'center')  # 第九行全部居中
        # Alignment(horizonta水平对齐模式, vertical=垂直对齐模式, text_rotation=旋转角度, wrap_text=是否自动换行)
        # horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed",)
        # vertical = ("top", "center", "bottom", "justify", "distributed")
        sh = self.sh(varSheet)
        cols = sh.max_column
        if l_col == "all":
            for i in range((cols)):
                sh.cell(row=row, column=i + 1).alignment = Alignment(
                    horizontal=horizontal,
                    vertical=vertical,
                    text_rotation=text_rotation,
                    wrap_text=wrap_text,
                )
        else:
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.cell(row=row, column=i).alignment = Alignment(
                    horizontal=horizontal,
                    vertical=vertical,
                    text_rotation=text_rotation,
                    wrap_text=wrap_text,
                )
        self.save()

    def setAllCellAlignment(
        self,
        horizontal="center",
        vertical="center",
        text_rotation=0,
        wrap_text=False,
        varSheet=0,
    ):

        # 2.9.3 设置所有单元格对齐样式
        # Openpyxl_PO.setAllCellAlignment('center', 'center')
        # Alignment(horizonta水平对齐模式, vertical=垂直对齐模式, text_rotation=旋转角度, wrap_text=是否自动换行)
        # horizontal = ("general", "left", "center", "right", "fill", "justify", "centerContinuous", "distributed",)
        # vertical = ("top", "center", "bottom", "justify", "distributed")
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        for r in range(rows):
            for c in range(cols):
                sh.cell(row=r + 1, column=c + 1).alignment = Alignment(
                    horizontal=horizontal,
                    vertical=vertical,
                    text_rotation=text_rotation,
                    wrap_text=wrap_text,
                )
        self.save()

    def setFilterCol(self, varCell="all", varSheet=0):

        # 2.10 设置筛选列
        # setFilterCol("all")  # 全部筛选
        # setFilterCol("")  # 取消筛选
        # setFilterCol("A2") # 对A2筛选
        sh = self.sh(varSheet)
        if varCell == "all":
            sh.auto_filter.ref = sh.dimensions
        elif varCell == "":
            sh.auto_filter.ref = None
        else:
            sh.auto_filter.ref = varCell
        self.save()

    def setCellFont(
        self,
        row,
        col,
        name="微软雅黑",
        size=10,
        bold=False,
        italic=False,
        color=None,
        varSheet=0,
    ):

        # 2.11 设置单元格字体（字体、字号、粗斜体、下划线、颜色）
        # setCellFont(1, 1)
        # setCellFont(1, "f")
        # setCellFont(1, "f", size=16, bold=True, color="ff0000")
        sh = self.sh(varSheet)
        if isinstance(col, int):
            sh.cell(row, col).font = Font(
                name=name, size=size, bold=bold, italic=italic, color=color
            )
        else:
            sh.cell(row, column_index_from_string(col)).font = Font(
                name=name, size=size, bold=bold, italic=italic, color=color
            )
        self.save()

    def setRowColFont(
        self,
        row,
        l_col,
        name="微软雅黑",
        size=16,
        bold=False,
        italic=False,
        color="000000",
        varSheet=0,
    ):

        # 2.11.2 设置单行多列字体（字体、字号、粗斜体、下划线、颜色）
        # setRowColFont(1, ["e", "h"])
        # setRowColFont(1, "all", color="000000")
        sh = self.sh(varSheet)
        cols = sh.max_column
        if l_col == "all":
            for i in range((cols)):
                sh.cell(row=row, column=i + 1).font = Font(
                    name=name, size=size, bold=bold, italic=italic, color=color
                )
        else:
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.cell(row=row, column=i).font = Font(
                    name=name, size=size, bold=bold, italic=italic, color=color
                )
        self.save()

    def setAllCellFont(
        self, name="微软雅黑", size=16, bold=False, italic=False, color="000000", varSheet=0
    ):

        # 2.11.2 设置所有单元格字体（字体、字号、粗斜体、下划线、颜色）
        # setAllCellFont()
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column

        for r in range(rows):
            for c in range(cols):
                sh.cell(row=r + 1, column=c + 1).font = Font(
                    name=name, size=size, bold=bold, italic=italic, color=color
                )
        self.save()

    def setBorder(
        self,
        row,
        col,
        left=["thin", "ff0000"],
        right=["thick", "ff0000"],
        top=["thin", "ff0000"],
        bottom=["thick", "ff0000"],
        varSheet=0,
    ):

        """
        2.12 设置单元格边框
        # 设置边框样式，上下左右边框
        Side(style=边线样式，color=边线颜色)
         * style 参数的种类： 'double, 'mediumDashDotDot', 'slantDashDot','dashDotDot','dotted','hair', 'mediumDashed, 'dashed', 'dashDot', 'thin','mediumDashDot','medium', 'thick'

        setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])
        """

        sh = self.sh(varSheet)
        border = Border(
            left=Side(style=left[0], color=left[1]),
            right=Side(style=right[0], color=right[1]),
            top=Side(style=top[0], color=top[1]),
            bottom=Side(style=bottom[0], color=bottom[1]),
        )
        sh.cell(row=row, column=col).border = border
        self.save()

    def setPatternFill(self, row, col, fill_type="solid", fgColor="99ccff", varSheet=0):

        """
        2.13 设置单元格填充背景色
        patternType = {'lightVertical', 'mediumGray', 'lightGrid', 'darkGrid', 'gray125', 'lightHorizontal', 'gray0625','lightTrellis', 'darkUp', 'lightGray', 'darkVertical', 'darkGray', 'solid', 'darkTrellis', 'lightUp','darkHorizontal', 'darkDown', 'lightDown'}
        PatternFill(fill_type=填充样式，fgColor=填充颜色）
        setPatternFill(2, 2, 'solid', '006100')
        """

        sh = self.sh(varSheet)
        pattern_fill = PatternFill(fill_type=fill_type, fgColor=fgColor)
        sh.cell(row=row, column=col).fill = pattern_fill
        self.save()
        # return PatternFill(patternType='' + patternType + '', fgColor='' + fgColor + '')  # 背景色

    def setGradientFill(
        self, row, col, stop=["FFFFFF", "99ccff", "000000"], varSheet=0
    ):

        # 2.14 设置单元格填充渐变色
        # GradientFill(stop=(渐变颜色 1，渐变颜色 2……))
        # setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])
        sh = self.sh(varSheet)
        gradient_fill = GradientFill(stop=(stop[0], stop[1], stop[2]))
        sh.cell(row=row, column=col).fill = gradient_fill
        self.save()

    def setCellColor(self, row, col, varColor=None, varSheet=0):

        # 2.15 设置单元格背景色
        # Openpyxl_PO.setCellColor(5, 1)  # 清除第5行第1列的背景色
        # Openpyxl_PO.setCellColor(5, "d")  # 清除第5行d列的背景色
        # Openpyxl_PO.setCellColor(5, 1, "ff0000")  # 设置第五行第1列设置红色
        # Openpyxl_PO.setCellColor(5, "e", "ff0000")  # 设置第五行e列设置红色
        # Openpyxl_PO.setCellColor(None, None)  # 清除所有背景色
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
            if varColor == None:
                style = PatternFill(fill_type=None)  # 消除单元格颜色
            else:
                style = PatternFill("solid", fgColor=varColor)
            if isinstance(col, int):
                sh.cell(row, col).fill = style
            else:
                sh.cell(row, column_index_from_string(col)).fill = style
        self.save()

    def setRowColColor(self, row, l_col, varColor, varSheet=0):

        # 2.15.2 设置单行多列背景色
        # Openpyxl_PO.setRowColColor(5, ['b', 'd'], "ff0000")
        # Openpyxl_PO.setRowColColor(5, "all", "ff0000")
        sh = self.sh(varSheet)
        cols = sh.max_column
        style = PatternFill("solid", fgColor=varColor)

        if l_col == "all":
            for i in range((cols)):
                sh.cell(row=row, column=i + 1).fill = style
        else:
            for i in range(
                column_index_from_string(l_col[0]),
                int(column_index_from_string(l_col[1])) + 1,
            ):
                sh.cell(row=row, column=i).fill = style
        self.save()

    def setAllCellColor(self, varColor=None, varSheet=0):

        # 2.15.3 设置所有单元格背景色
        # setAllCellColor("ff0000")
        # setAllCellColor()
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        if varColor == None:
            style = PatternFill(fill_type=None)  # 消除单元格颜色
        else:
            style = PatternFill("solid", fgColor=varColor)

        for r in range(rows):
            for c in range(cols):
                sh.cell(row=r + 1, column=c + 1).fill = style
        self.save()

    def setRowColor(self, row, varSkip, varColor, varSheet=0):

        # 2.16 设置整行(可间隔)背景色
        # Openpyxl_PO.setRowColor(6, 1, "FF0000")
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        # 清除表格里所有单元格的背景色
        style = PatternFill(fill_type=None)
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                sh.cell(i, j).fill = style
        style = PatternFill("solid", fgColor=varColor)
        for i in range(row, rows + 1, varSkip + 1):
            for j in range(1, cols + 1):
                sh.cell(i, j).fill = style
        self.save()

    def setColColor(self, col, varSkip, varColor, varSheet=0):

        # 2.17 设置整列(可间隔)背景色
        # Openpyxl_PO.setColColor(6, 1, "FF0000")
        sh = self.sh(varSheet)
        rows = sh.max_row
        cols = sh.max_column
        style = PatternFill(fill_type=None)  # 消除单元格颜色
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                sh.cell(i, j).fill = style
        style = PatternFill("solid", fgColor=varColor)
        for i in range(1, rows + 1):
            for j in range(col, cols + 1, varSkip + 1):
                sh.cell(i, j).fill = style
        self.save()

    def setSheetColor(self, varColor, varSheet=0):

        # 2.18 设置工作表背景颜色
        # Openpyxl_PO.setSheetColor("FF0000")
        sh = self.sh(varSheet)
        sh.sheet_properties.tabColor = varColor
        self.save()


    # todo [获取]

    def getTotalRowCol(self, varSheet=0):

        # 3.1 获取总行列数
        # Openpyxl_PO.getTotalRowCol()  # [4,3] //返回第1个工作表的总行数和总列数

        sh = self.sh(varSheet)
        return [sh.max_row, sh.max_column]

    def getCell(self, varRow, varCol, varSheet=0):

        # 3.2 获取单元格的值

        sh = self.sh(varSheet)
        return sh.cell(row=varRow, column=varCol).value


    def getOneRow(self, varSeq, varSheet=0):

        # 3.3 获取一行数据

        l_row = []
        sh = self.sh(varSheet)
        t_row = [r for r in sh.rows][varSeq-1]  # 获取此行的单元格值
        # print((t_row))  # (<Cell 'Sheet'.A3>, <Cell 'Sheet'.B3>, <Cell 'Sheet'.C3>)
        for cell in t_row:
            l_row.append(cell.value)
        return l_row  #  [10, 5, 10]

    def getOneCol(self, varCol, varSheet=0):

        # 3.4 获取一列的值

        l_col = []
        sh = self.sh(varSheet)
        if isinstance(varCol, str):
            varCol = column_index_from_string(varCol)  # 2
        t_col = [c for c in sh.columns][int(varCol)-1]  # 获取此列的单元格值
        # print(t_col)  # (<Cell 'Sheet'.C1>, <Cell 'Sheet'.C2>, ...)
        for cell in t_col:
            l_col.append(cell.value)
        return l_col  # ['山丘', 30, 25, 30, 10, 5, 10]

    def getRow(self, varSheet=0):

        # 3.5.1 获取每行数据

        l_row = []  # 每行值
        l_l_row = []  # 所有行值
        sh = self.sh(varSheet)
        # print(sh.rows)  # (<Cell 'Sheet'.A1>, <Cell 'Sheet'.B1>, <Cell 'Sheet'.C1>), (<Cell 'Sheet'.A2>, <Cell 'Sheet'.B2>, <Cell 'Sheet'.C2>), ...)
        for row in list(sh.rows):
            for i in range(len(row)):
                l_row.append(row[i].value)
            l_l_row.append(l_row)
            l_row = []
        return l_l_row

    def getRowBySeq(self, varSheet=0):

        # 3.5.2 获取带行号的每行数据

        d_seq_row = {}
        l_l_row = self.getRow(varSheet)
        for i in range(len(l_l_row)):
            d_seq_row[i + 1] = l_l_row[i]
        return d_seq_row

    def getRowByCol(self, l_col, varSheet=0):

        # 3.5.3 获取部分列的行数据
        #   获取部分列的行数据 getRowByCol([1, 2, 4])  # 获取第1，2，4列的行数据
        # 	获取部分列的行数据 getRowByCol(["A", "C"])
        # 	获取部分列的行数据 getRowByCol([2, "C"])
        # 	获取部分列的行数据 getRowByCol([1, 3, 2, "a", "C", "B"])

        l_row = []  # 每行的数据
        l_l_row = []  # 所有的数据

        for i in range(len(l_col)):
            if isinstance(l_col[i], int):
                pass
            else:
                l_col[i] = column_index_from_string(l_col[i])

        # 去重(先入为主，保留排前面的值，后面重复的值忽略，如 [1, 3, 5, 2, 1, 7, 27, 3] => [1, 3, 5, 2, 7, 27])
        l_col = sorted(set(l_col), key=l_col.index)

        sh = self.sh(varSheet)
        for row in range(1, sh.max_row + 1):
            for col in l_col:
                l_row.append(sh.cell(row, col).value)
            l_l_row.append(l_row)
            l_row = []
        return l_l_row

    def getRowByColSeq(self, l_col, varSheet=0):

        # 3.5.4 获取带行号的部分列的行数据

        d_seq_row = {}
        l_l_col = self.getRowByCol(l_col, varSheet)
        for i in range(len(l_l_col)):
            d_seq_row[i + 1] = l_l_col[i]
        return d_seq_row



    def getCol(self, varSheet=0):

        # 3.6.1 获取每列数据
        # print(Openpyxl_PO.getCol())

        l_col = []  # 每列值
        l_l_col = []  # 所有数据
        sh = self.sh(varSheet)
        # print(sh.columns)  # <generator object Worksheet._cells_by_col at 0x7ff4849f6970>
        for col in list(sh.columns):
            for i in range(len(col)):
                l_col.append(col[i].value)
            l_l_col.append(l_col)
            l_col = []
        return l_l_col

    def getColBySeq(self, varSheet=0):

        # 3.6.2 获取带列序号的每列数据

        d_seq_col = {}
        l_l_col = self.getCol(varSheet)
        for i in range(len(l_l_col)):
            d_seq_col[i + 1] = l_l_col[i]
        return d_seq_col

    def getColByLetter(self, varSheet=0):

        # 3.6.3 获取带列字母的每列数据

        d_seq_col = {}
        l_l_col = self.getCol(varSheet)
        for i in range(len(l_l_col)):
            d_seq_col[get_column_letter(i + 1)] = l_l_col[i]
        return d_seq_col





    def getTitleColSeq(self, l_partialTitle, varSheet=0):

        # 3.8.1 获取标题的序号
        # getTitleColSeq(['姓名', '性别'])  => [1, 3]
        # 标题是表格中第一行数据

        l_title = self.getOneRow(1, varSheet)  # ['姓名', '年龄', '性别', '地址']
        for i in range(len(l_partialTitle)):
            for j in range(len(l_title)):
                if l_partialTitle[i] == l_title[j]:
                    l_partialTitle[i] = j + 1
        return l_partialTitle  # [1, 3]

    def getTitleColLetter(self, l_partialTitle, varSheet=0):

        # 3.8.2 获取标题的字母
        # getTitleColSeq(['姓名', '性别'])  => ['A', 'C']
        # 标题是表格中第一行数据

        l_title = self.getOneRow(1, varSheet)  # ['姓名', '年龄', '性别', '地址']
        for i in range(len(l_partialTitle)):
            for j in range(len(l_title)):
                if l_partialTitle[i] == l_title[j]:
                    l_partialTitle[i] = get_column_letter(j + 1)
        return l_partialTitle  # ['A', 'C']

    def title2dictSeq(self, l_partialTitle, varSheet=0):

        # 3.8.3 将标题转列字典序列
        # title2dictSeq(['姓名', '性别'])  => {"1":'姓名'，“2”：“性别“}

        # 标题是表格中第一行数据
        l_title = self.getOneRow(1, varSheet)
        l_letter = []
        for i in range(len(l_partialTitle)):
            for j in range(len(l_title)):
                if l_partialTitle[i] == l_title[j]:
                    l_letter.append(j + 1)
        return dict(zip(l_letter, l_partialTitle))

    def title2dictLetter(self, l_partialTitle, varSheet=0):

        # 3.8.4 将标题转列字典字母
        # title2dictLetter(['姓名', '性别'])  => {'B': '姓名', 'E': '性别'}

        # 标题是表格中第一行数据
        l_title = self.getOneRow(1, varSheet)
        l_seq = []
        for i in range(len(l_partialTitle)):
            for j in range(len(l_title)):
                if l_partialTitle[i] == l_title[j]:
                    l_seq.append(get_column_letter(j + 1))
        return dict(zip(l_seq, l_partialTitle))  # {'B': '姓名', 'E': '性别'}



    def getColByPartialColByUnwantedRow(self, l_varCol, l_varIgnoreRowNum, varSheet=0):

        # 3.9 获取部分列的列值(可忽略多行)
        # print(Openpyxl_PO.getColByPartialColByUnwantedRow([1, 3], [1, 2]))  # 获取第二列和第四列的列值，并忽略第1，2行的行值。
        # print(Openpyxl_PO.getColByPartialColByUnwantedRow([2], [], "python"))  # 获取第2列所有值。

        l_col = []  # 每列值
        l_l_col = []  # 所有列的值
        sh = self.sh(varSheet)
        for col in l_varCol:
            for row in range(1, sh.max_row + 1):
                if row not in l_varIgnoreRowNum:
                    l_col.append(sh.cell(row, col).value)
            l_l_col.append(l_col)
            l_col = []
        return l_l_col

    def getCellCoordinate(self, varRow, varCol, varSheet=0):

        # 3.10 获取单元格的坐标
        sh = self.sh(varSheet)
        return sh.cell(row=varRow, column=varCol).coordinate

    def getDimensions(self, varSheet=0):

        # 3.11 获取所有数据的坐标
        sh = self.sh(varSheet)
        return sh.dimensions

    # todo [清除]

    def clsRow(self, varNums, varSheet=0):

        # 4.1 清空行
        # Openpyxl_PO.clsRow(2)  # 清空第2行
        sh = self.sh(varSheet)
        for i in range(1, sh.max_row):
            sh.cell(row=varNums, column=i, value="")
        self.save()

    def clsCol(self, varCol, varSheet=0):

        # 4.2 清空列
        # Openpyxl_PO.clsCol(2)  # 清空第2列
        sh = self.sh(varSheet)
        for i in range(1, sh.max_row + 1):
            sh.cell(row=i, column=varCol).value = None
        self.save()

    def clsColRetainTitle(self, varCol, varSheet=0):

        # 4.2.1 清空列保留标题
        sh = self.sh(varSheet)
        for i in range(sh.max_row - 1):
            sh.cell(row=i + 2, column=varCol).value = None
        self.save()

    def delSeriesRow(self, varFrom, varSeries=1, varSheet=0):

        # 4.3 删除连续行
        # Openpyxl_PO.delSeriesRow(2, 3)  # 删除从第二行开始连续三行数据 （即删除2，3，4行）
        sh = self.sh(varSheet)
        sh.delete_rows(idx=varFrom, amount=varSeries)
        self.save()

    def delSeriesCol(self, varFrom, varSeries=1, varSheet=0):

        # 4.4 删除连续列
        # Openpyxl_PO.delSeriesCol(2, 3)  # 删除从第二列开始连续三列数据 （即删除2，3，4列）
        # Openpyxl_PO.delSeriesCol('U', 1)  # 删除从第U列开始连续1列数据 （即删除U列）
        sh = self.sh(varSheet)
        if isinstance(varFrom, int):
            sh.delete_cols(idx=varFrom, amount=varSeries)
        else:
            sh.delete_cols(idx=column_index_from_string(varFrom), amount=varSeries)
        self.save()

    # todo [多表]

    def getDiffValueByCmp(self, l_file1row, l_file2row):

        """
        5.2 两工作表比较，对差异内容标注颜色
        :param l_file1row:
        :param l_file2row:
        :return:
            print(Openpyxl_PO.getDiffValueByLeft(Openpyxl_PO.getRow(), Openpyxl_PO2.getRow()))
            [[5, 'member_id', 1311441], [7, 'loan_amnt', 5600]]   表示 第五行，member_id列的值1311441
            [[5, 'member_id', 5555], [7, 'loan_amnt', 1200]]
        """

        d_left = {}
        d_left_sub = {}
        d_right = {}
        d_right_sub = {}
        d_all = {}

        if len(l_file1row) == len(l_file2row):
            for i in range(len(l_file1row)):
                if l_file1row[i] != l_file2row[i]:
                    for j in range(len(l_file1row[i])):
                        if l_file1row[i][j] != l_file2row[i][j]:
                            d_left_sub[l_file1row[0][j]] = l_file1row[i][j]
                            d_right_sub[l_file2row[0][j]] = l_file2row[i][j]
                    d_left[i + 1] = d_left_sub
                    d_right[i + 1] = d_right_sub
                    d_left_sub = {}
                    d_right_sub = {}

            if d_left != {} or d_right != {}:
                d_all["left"] = d_left
                d_all["right"] = d_right
                return d_all
            else:
                print("[ok], 两列表比对结果一致")
        else:
            print("[warning], 两列表数量不一致！")

    def setColorByDiff(self, varSheet1, varSheet2):

        # 5.2 两工作表比较，对差异内容标注颜色
        # 前提条件，两sheet表的行列数一致
        # Openpyxl_PO.setColorByDiff("Sheet1", "Sheet2")

        l_sheetOneRow = self.getRow(varSheet1)
        l_sheetTwoRow = self.getRow(varSheet2)

        if l_sheetOneRow == None or l_sheetTwoRow == None:
            print("[Error], " + varSheet1 + " 或 " + varSheet2 + " 不存在！")
            sys.exit(0)

        if len(l_sheetOneRow) == len(l_sheetTwoRow):
            for i in range(len(l_sheetOneRow)):
                for j in range(len(l_sheetOneRow[i])):
                    if l_sheetOneRow[i][j] != l_sheetTwoRow[i][j]:
                        self.setCellColor(i + 1, j + 1, "FF0000", varSheet1)
                        self.setCellColor(i + 1, j + 1, "ffeb9c", varSheet2)
                print("检查第" + str(i + 1) + "行")

            self.save()
        else:
            print("[warning], 两sheet的行数不一致！")
            sys.exit(0)

    def setSheetByDiff(self, varSheet1, varSheet2):

        # 5.3 两工作表比较，生成新表Sheet1%Sheet2，对差异内容标注颜色
        # 前提条件，两sheet表的行列数一致
        # Openpyxl_PO.setSheetByDiff("Sheet1", "Sheet2")

        l_sheetOneRow = self.getRow(varSheet1)
        l_sheetTwoRow = self.getRow(varSheet2)

        if l_sheetOneRow == None or l_sheetTwoRow == None:
            print("[Error], " + varSheet1 + " 或 " + varSheet2 + " 不存在！")
            sys.exit(0)

        if len(l_sheetOneRow) == len(l_sheetTwoRow):

            # 生成临时sheet
            varSheet = varSheet1 + "%" + varSheet2
            self.delSheet(varSheet)
            self.addCoverSheet(varSheet, 99)

            for i in range(len(l_sheetOneRow)):
                for j in range(len(l_sheetOneRow[i])):
                    if l_sheetOneRow[i][j] == "" and l_sheetTwoRow[i][j] == "":
                        pass
                    elif l_sheetOneRow[i][j] != l_sheetTwoRow[i][j]:
                        print(l_sheetOneRow[i][j], l_sheetTwoRow[i][j])
                        self.setCell(
                            i + 1,
                            j + 1,
                            str(l_sheetOneRow[i][j]) + "/" + str(l_sheetTwoRow[i][j]),
                            varSheet,
                        )
                        self.setCellColor(i + 1, j + 1, "FF0000", varSheet)
                    else:
                        self.setCell(
                            i + 1, j + 1, str(l_sheetOneRow[i][j]), varSheet
                        )
            self.save()
            return varSheet
        else:
            print("[warning], 两sheet的行数不一致！")
            sys.exit(0)

    def moveValue(self, varFrom, varRows, varCols, varSheet=0):

        # 6 移动范围数据
        sh = self.sh(varSheet)
        sh.move_range(varFrom, rows=varRows, cols=varCols)
        self.save()

    def sortFields(self, varSheet1):

        # 7 将excel中标题（第一行字段）排序（从小打大）

        l_sortAsc = []
        l_title = self.getOneRow(1)
        for k in range(len(l_title)):
            x = "z"
            for i in range(len(l_title)):
                if x > l_title[i]:
                    x = l_title[i]
            l_sortAsc.append(x)
            l_title.remove(x)
        # print(l_sortAsc)

        self.addSheet("sortAsc")
        self.setRows({1: l_sortAsc}, "sortAsc")
        col = self.getCol(varSheet1)
        # print(col)
        for i in range(len(col)):
            for j in range(len(l_sortAsc)):
                if col[i][0] == l_sortAsc[j]:
                    self.setCols({str(j + 1): col[i]}, "sortAsc")

        self.save()


if __name__ == "__main__":

    Sys_PO.clsApp("Microsoft Excel")
    Openpyxl_PO = OpenpyxlPO("./data/area.xlsx")


    # print("1.1 新建".center(100, "-"))
    # Openpyxl_PO.newExcel("./OpenpyxlPO/newfile2.xlsx", ["mySheet1", "mySheet2", "mySheet3"])  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。
    # Openpyxl_PO.newExcel("d://t44.xlsx", ["mySheet661", "mySheet552", "mySheet32"])  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。

    # print("1.2 打开".center(100, "-"))
    Openpyxl_PO.open(1)  # 打开第二个工作表
    # Openpyxl_PO.open() # 打开第一个工作表
    # Openpyxl_PO.open('test')  # 打开test工作表

    # print("1.6 添加工作表(不覆盖)".center(100, "-"))
    # Openpyxl_PO.addSheet("saasuser1")

    # print("1.7 添加工作表(覆盖)".center(100, "-"))
    # Openpyxl_PO.addCoverSheet("Sheet0", 0)    # 第一个位置添加工作表
    # Openpyxl_PO.addCoverSheet("Sheet100", 100)    # 第100个位置添加工作表  //当index足够大时，则在最后一个位置添加工作表
    # Openpyxl_PO.open()

    # print("1.8 删除工作表".center(100, "-"))
    # Openpyxl_PO.delSheet("Sheet1")
    # Openpyxl_PO.delSheet("mySheet1")



    # print("2.0.1 在第N行前插入多行空白".center(100, "-"))
    # Openpyxl_PO.insertNullRows(1)  # 在第三行前插入一行空白， 等同于 insertRows(3, 1)
    # Openpyxl_PO.insertNullRows(5)  # 在第三行前插入一行空白， 等同于 insertRows(3, 1)
    # Openpyxl_PO.insertRows(3, 5)  # 在第三行前插入五行空白

    # print("2.0.2 在第N列前插入多列空白".center(100, "-"))
    # Openpyxl_PO.insertCols(3)  # 在第3列前插入1列空白， 等同于 insertCols(3, 1)
    # Openpyxl_PO.insertCols(3, 2)  # 在第3列前插入2列空白， 等同于 insertCols(3, 1)

    # print("2.1 更新单元格值".center(100, "-"))
    # Openpyxl_PO.setCell(1, 'B', "hello")
    # Openpyxl_PO.setCell(1, 3, "hello")

    # print("2.2 插入行数据".center(100, "-"))
    # Openpyxl_PO.insertRows({2: ["金浩", "101", "102"], 5: ["yoyo", "123", "666"]})

    # print("2.3 更新行数据".center(100, "-"))
    # Openpyxl_PO.setRows({2: ["金浩", "101", "102"], 5: ["yoyo", "123", "666"]})
    # Openpyxl_PO.setRows({7: ["你好", 12345, "7777"], 8: ["44", None, "777777777"]})  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格
    # Openpyxl_PO.setRows({7: ["你好", 12345, "7777"], 8: ["44", "None", "777777777"]}, -1)  # 对最后一个sheet表，对第7，8行分别写入内容
    # Openpyxl_PO.open()

    # print("2.4 追加行数据".center(100, "-"))
    # Openpyxl_PO.appendRows([['姓名', '电话', '成绩', '学科'], ['毛泽东', 15266606298, 14, '化学'], ['周恩来', 15201077791, 78, '美术']])


    # print("2.5 插入列数据".center(100, "-"))
    # Openpyxl_PO.insertCols({"a": ["姓名", "张三", "李四"], "c": ["年龄", "55", "34"]})

    # print("2.6 更新列数据".center(100, "-"))
    # Openpyxl_PO.setCols({"A": [None, "k1", 666, "777"], "C": [None, "888", None, "999"]})  # 对最后一个sheet表，对第7，8行分别写入内容，如遇None则跳过该单元格

    # print("2.7 追加列数据".center(100, "-"))
    # Openpyxl_PO.appendCols([["test", "张三", "李四"], ["dev", "55", "34"]])



    # print("2.5 设置单元格行高与列宽".center(100, "-"))
    # Openpyxl_PO.setCellDimensions(3, 30, 'f', 34)  # 设置第三行行高30，第f列宽34

    # print("2.5.2 设置单行多列行高与列宽".center(100, "-"))
    # Openpyxl_PO.setRowColDimensions(5, 30, ['f', 'h'], 33)  # 设置第五行行高30，f - h列宽33

    # print("2.6 设置所有单元格的行高与列宽".center(100, "-"))
    # Openpyxl_PO.setAllCellDimensions(30, 20)

    # print("2.7 设置所有单元格自动换行".center(100, "-"))
    # Openpyxl_PO.setAllWordWrap()
    # Openpyxl_PO.setAllWordWrap("Sheet1")

    # print("2.8 设置冻结首行".center(100, "-"))
    # Openpyxl_PO.setFreeze('A2', "saasuser")

    # print("2.9 设置单元格对齐样式".center(100, "-"))
    # Openpyxl_PO.setCellAlignment(5, 4, 'center', 'top')
    # Openpyxl_PO.setCellAlignment(1, "e", 'center', 'top', 45)
    # Openpyxl_PO.setCellAlignment(1, 1, 'center', 'top', 45, True)
    # Openpyxl_PO.setCellAlignment(5, 4, 'center', 'center', "saasuser1")

    # print("2.9.2 设置单行多列对齐样式".center(100, "-"))
    # Openpyxl_PO.setRowColAlignment(1, ["c", "e"], 'center', 'center')  # 第一行第c,d,e列居中
    # Openpyxl_PO.setRowColAlignment(9, "all", 'center', 'center')  # 第九行全部居中

    # print("2.9.3 设置所有单元格对齐样式".center(100, "-"))
    # Openpyxl_PO.setAllCellAlignment('center', 'center')

    # print("2.10 设置筛选列".center(100, "-"))
    # Openpyxl_PO.setFilterCol("all")  # 全部筛选
    # Openpyxl_PO.setFilterCol("") # 取消筛选
    # Openpyxl_PO.setFilterCol("A2") # 对A2筛选

    # print("2.11 设置单元格字体（字体、字号、粗斜体、下划线、颜色）".center(100, "-"))
    # Openpyxl_PO.setCellFont(1, 6)  # 设置第一行第六列字体（默认微软雅黑字号16粗体）
    # Openpyxl_PO.setCellFont(2, "f")  # 设置第一行第f列字体（默认微软雅黑字号16粗体）
    # Openpyxl_PO.setCellFont(5, "f", size=14, bold=True, color="red")
    # Openpyxl_PO.setCellFont(5, "f", size=14, bold=True)

    # print("2.11.2 设置单行多列字体".center(100, "-"))
    # Openpyxl_PO.setRowColFont(1, ["b", "h"])  # 第一行第b-h列
    # Openpyxl_PO.setRowColFont(9, "all")  # 第九行

    # print("2.11.3 设置所有单元格字体".center(100, "-"))
    # Openpyxl_PO.setAllCellFont()

    # print("2.12 设置单元格边框".center(100, "-"))
    # Openpyxl_PO.setBorder(1, 2, left = ['thin','ff0000'], right = ['thick','ff0000'], top = ['thin','ff0000'],bottom = ['thick','ff0000'])

    # print("2.13 设置单元格填充背景色".center(100, "-"))
    # Openpyxl_PO.setPatternFill(2, 2, 'solid', '006100')  # 单元格背景色

    # print("2.14 设置单元格填充渐变色".center(100, "-"))
    # Openpyxl_PO.setGradientFill(3, 3, stop=["FFFFFF", "99ccff", "000000"])

    # print("2.15 设置单元格背景色".center(100, "-"))
    # Openpyxl_PO.setCellColor(5, 1)  # 清除第5行第1列的背景色
    # Openpyxl_PO.setCellColor(5, "d")  # 清除第5行d列的背景色
    # Openpyxl_PO.setCellColor(5, 1, "ff0000", "Sheet2")  # 设置第五行第1列设置红色
    # Openpyxl_PO.setCellColor(5, "e", "ff0000")  # 设置第五行e列设置红色
    # Openpyxl_PO.setCellColor(None, None)  # 清除所有背景色

    # print("2.15.2 设置单行多列背景色".center(100, "-"))
    # Openpyxl_PO.setRowColColor(5, ['b', 'd'], "ff0000") # 设置第五行第b，c，d列背景色
    # Openpyxl_PO.setRowColColor(7, "all", "ff0000")  # 设置第五行所有列背景色

    # print("2.15.3 设置所有单元格背景色".center(100, "-"))
    # Openpyxl_PO.setAllCellColor("ff0000")  # 设置所有单元格背景色
    # Openpyxl_PO.setAllCellColor(None)  # 清除所有单元格背景色

    # print("2.16 设置整行(可间隔)背景色".center(100, "-"))
    # Openpyxl_PO.setRowColor(5, 0, "ff0000")  # 从第3行开始每行颜色标红色
    # Openpyxl_PO.setRowColor(3, 1, "ff0000")  # 从第3行开始每隔1行颜色标红色

    # print("2.17 设置整列(可间隔)背景色".center(100, "-"))
    # Openpyxl_PO.setColColor(2, 0, "ff0000")  # 从第2列开始每列颜色为红色
    # Openpyxl_PO.setColColor(2, 1, "ff0000")  # 从第2列开始每隔1列设置颜色为红色

    # print("2.18 设置工作表背景颜色".center(100, "-"))
    # Openpyxl_PO.setSheetColor("FF0000")



    # print("3.1 获取总行列数".center(100, "-"))
    # print(Openpyxl_PO.getTotalRowCol())  # [7,5]

    # print("3.2 获取单元格值".center(100, "-"))
    # print(Openpyxl_PO.getCell(3, 2))  # 获取第3行第2列的值

    # print("3.3 获取一行数据".center(100, "-"))
    # print(Openpyxl_PO.getOneRow(1))  # ['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字']
    #
    # print("3.4 获取一列数据".center(100, "-"))
    # print(Openpyxl_PO.getOneCol(2))  # ['高地', 40, 44, 50, 30, 25, 150]
    # print(Openpyxl_PO.getOneCol('B'))  # ['高地', 40, 44, 50, 30, 25, 150]

    # print("3.5.1 获取每行数据".center(100, "-"))
    # print(Openpyxl_PO.getRow())  # [['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字'], [2, 40, 30, 'ok', 'jinhao'],...]
    #
    # print("3.5.2 获取带行号的每行数据".center(100, "-"))
    # print(Openpyxl_PO.getRowBySeq())  # {1: ['Number具体数', '高地', 'jinhaoyoyo', '状态', '名字'], 2: [2, 40, 30, 'ok', 'jinhao'],...}

    # print("3.5.3 获取部分列的行数据".center(100, "-"))
    # print(Openpyxl_PO.getRowByCol([1, 3]))   # [['Number具体数', 'jinhaoyoyo'], [2, 30], [3, 25], [4, 30], [5, 10], [6, 5], [7, 10]] //获取1和3列的行数据
    # print(Openpyxl_PO.getRowByCol(['a', 'C']))  # 同上
    # print(Openpyxl_PO.getRowByCol(["A", 3]))   # 同上
    # print(Openpyxl_PO.getRowByCol([1, 3, 2, "a", "C", "B"]))   # [['Number具体数', '山丘', '高地'], [2, 30, 40], [3, 25, 44], [4, 30, 50], [5, 10, 30], [6, 5, 25], [7, 10, 150]] //获第1，3，2列的行数据，"a", "C", "B"忽略
    #
    # print("3.5.4 获取带行号的部分列的行数据".center(100, "-"))
    # print(Openpyxl_PO.getRowByColSeq([1, 3]))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
    # print(Openpyxl_PO.getRowByColSeq([1, 'C']))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}
    # print(Openpyxl_PO.getRowByColSeq(['a', 'C']))   # {1: ['Number具体数', 'jinhaoyoyo'], 2: [2, 30], 3: [3, 25], 4: [4, 30], 5: [5, 10], 6: [6, 5], 7: [7, 10]}



    # print("3.6.1 获取每列数据".center(100, "-"))
    # print(Openpyxl_PO.getCol())  # [['Number具体数', 2, 3, 4, 5, 6, 7], ['高地', 40, 44, 50, 30, 25, 150],...]
    #
    # print("3.6.2 获取带列序号的每列数据".center(100, "-"))
    # d_seq_row = Openpyxl_PO.getColBySeq()
    # print(d_seq_row)  # {1: ['Number具体数', 2, 3, 4, 5, 6, 7], 2: ['高地', 40, 44, 50, 30, 25, 150],,...}
    # del d_seq_row[1]  # 删除第一行，一般用于去掉标题
    # print(d_seq_row)  # {2: ['高地', 40, 44, 50, 30, 25, 150], 3: ['jinhaoyoyo', 30, 25, 30, 10, 5, 10],...}
    #
    # print("3.6.3 获取带列字母的每列数据".center(100, "-"))
    # d_letter_row = Openpyxl_PO.getColByLetter()
    # print(d_letter_row)  # {'A': ['Number具体数', 2, 3, 4, 5, 6, 7], 'B': ['高地', 40, 44, 50, 30, 25, 150],...}
    # del d_letter_row['A']  # 删除第一行，一般用于去掉标题
    # print(d_letter_row)  # {'B': ['高地', 40, 44, 50, 30, 25, 150], 'C': ['jinhaoyoyo', 30, 25, 30, 10, 5, 10]...}


    # print("3.8.1 获取标题的序号".center(100, "-"))
    # print(Openpyxl_PO.getTitleColSeq(["高地", "名字"]))  # [2, 5]
    #
    # print("3.8.2 获取标题的字母".center(100, "-"))
    # print(Openpyxl_PO.getTitleColLetter(["高地", "名字"]))  # ['B', 'E']

    # print("3.8.3 将标题转列字典序列".center(100, "-"))
    # print(Openpyxl_PO.title2dictSeq(["高地", "名字"]))  # {2: '高地', 5: '名字'}
    #
    # print("3.8.4 将标题转列字典字母".center(100, "-"))
    # print(Openpyxl_PO.title2dictLetter(["高地", "名字"]))  # {'A': '高地', 'C': '名字'}

    # l_colSeq = (Openpyxl_PO.title2colSeq(["高地", "名字"]))
    # print(l_colSeq)  # [2, 5]
    # print(Openpyxl_PO.getRowByCol(l_colSeq)) # [['高地', '名字'], [40, 'jinhao'], [44, 'yoyo'], [50, 'titi'], [30, 'mama'], [25, 'baba'], [150, 'yeye']]
    #
    # l_colSeq = (Openpyxl_PO.getTitleCol(["高地", "名字"]))
    # print(l_colSeq)  # [2, 5]

    # print("3.9 获取部分列的列值(可忽略多行)".center(100, "-"))
    # print(Openpyxl_PO.getColByPartialColByUnwantedRow([1, 3], [1, 4]))   # 获取第二列和第四列的列值，并忽略第1，2行的行值。
    # print(Openpyxl_PO.getColByPartialColByUnwantedRow([2], [], "上海"))  # 获取第2列所有值。

    # print("3.10 获取单元格的坐标".center(100, "-"))
    # print(Openpyxl_PO.getCellCoordinate(2, 5))   # E2

    # print("3.11 获取工作表数据的坐标".center(100, "-"))
    # print(Openpyxl_PO.getDimensions())  # A1:E17



    # print("4.1 清空行".center(100, "-"))
    # Openpyxl_PO.clsRow(2)  # 清空第2行
    #
    # print("4.2 清空列".center(100, "-"))
    # Openpyxl_PO.clsCol(2)  # 清空第2列
    # print("4.2.1 清空列保留标题".center(100, "-"))
    # Openpyxl_PO.clsColRetainTitle(2)  # 清空第2列保留标题

    # print("4.3 删除行".center(100, "-"))
    # # Openpyxl_PO.delSeriesRow(2, 3)  # 删除第2行之连续3行（删除2，3，4行）
    #
    # print("4.4 删除列".center(100, "-"))
    # # Openpyxl_PO.delSeriesCol(1, 2)  # 删除第1列之连续2列（删除1，2列）
    # # Openpyxl_PO.delSeriesCol(2, 1, "python")  # 删除第2列之连续1列（删除2列）
    # Openpyxl_PO.delSeriesCol('D', 1)  # 删除第D列之连续1列（删除D列）

    # print("5.1 两表比较获取差异内容（两表标题与行数必须一致） ".center(100, "-"))
    # Openpyxl_PO = OpenpyxlPO("./data/loanStats.xlsx")
    # Openpyxl_PO2 = OpenpyxlPO("./data/loanStats2.xlsx")
    # print(Openpyxl_PO.getDiffValueByCmp(Openpyxl_PO.getRow("Sheet2"), Openpyxl_PO2.getRow("Sheet2")))

    # # print("5.2 对一张表的两个sheet进行数据比对，差异数据标注颜色 ".center(100, "-"))
    # Openpyxl_PO = OpenpyxlPO("./data/loanStats.xlsx")
    # Openpyxl_PO.setColorByDiff("Sheet1", "Sheet2")

    # # print("5.3 对一张表的两个sheet进行数据比对，将结果写入第一个sheet ".center(100, "-"))
    # Openpyxl_PO.setSheetByDiff("browser", "interface")

    # # print("6 移动范围数据".center(100, "-"))
    # Openpyxl_PO.moveValue('C1:D2', 3, -2)  # 把'C1:D2'区域移动到 下三行左二列
    # Openpyxl_PO.moveValue('A1:C14', 0, 3)  # 把'A1:C14'区域向右移动3列

    # # print("7 将excel中标题（第一行字段）排序（从小打大）".center(100, "-"))
    # Openpyxl_PO.sortFields("Sheet1")


    # Openpyxl_PO.open()