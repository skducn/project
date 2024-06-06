# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-12-8
# Description   : openpyxl 应用层
# https://pypi.org/project/openpyxl/#files
# https://foss.heptapod.net/openpyxl/openpyxl/-/issues

# *********************************************************************

from PO.OpenpyxlPO import *

# todo 文件，工作表
# 打开文件（文件不存在则创建文件，默认Sheet1）
# Openpyxl_PO = OpenpyxlPO("/Users/linghuchong/Downloads/51/Python/project/PO/data/7.xlsx")
Openpyxl_PO = OpenpyxlPO("./data/7.xlsx")
# Openpyxl_PO = OpenpyxlPO(r"/Users/linghuchong/Downloads/51/Python/project/PO/data/11.xlsx",['Sheet2','Sheet3'])

# Openpyxl_PO.sh("Sheet2")
# Openpyxl_PO.switchSheet("Sheet2")

# Openpyxl_PO.setCell(12, 'B', "hello")
Openpyxl_PO.save()

# df = pd.DataFrame(pd.read_excel("./data/7.xlsx"))
# df.to_excel("./data/7.xlsx", index=False, header=None)


# Openpyxl_PO.renameSheet("Sheet1", "444")
# Openpyxl_PO.addCoverSheet("mysheet1")
# Openpyxl_PO.open('Sheet3')
# Openpyxl_PO.open()


# print("1.1 新建".center(100, "-"))
# Openpyxl_PO.newExcel("./OpenpyxlPO/newfile2.xlsx", ["mySheet1", "mySheet2", "mySheet3"])  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。
# Openpyxl_PO.newExcel("d://t44.xlsx", ["mySheet661", "mySheet552", "mySheet32"])  # 新建excel，生成三个工作表（mySheet1,mySheet2,mySheet3），默认定位在第一个mySheet1表。

# print("1.2 打开".center(100, "-"))
# Openpyxl_PO.open(1)  # 打开第二个工作表
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
# Openpyxl_PO.insertNullRows(5)  # 在第5行前插入一行空白

# print("2.0.2 在第N列前插入多列空白".center(100, "-"))
# Openpyxl_PO.insertCols(3)  # 在第3列前插入1列空白， 等同于 insertCols(3, 1)
# Openpyxl_PO.insertCols(3, 2)  # 在第3列前插入2列空白， 等同于 insertCols(3, 1)

# print("2.1 更新单元格值".center(100, "-"))
# Openpyxl_PO.setCell(1, 'B', "hello")
# Openpyxl_PO.setCell(1, 3, "hello")

# print("2.2 插入行数据".center(100, "-"))
# Openpyxl_PO.insertRows({2: ["金浩", "101", "102"]}, "Sheet1")

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
# Openpyxl_PO.appendCols([["test", "张三", "李四"], ["dev", "55", "34"]], 2)

# todo 样式

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
# Openpyxl_PO.setFreeze('A2', "Sheet1")

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
# Openpyxl_PO.setRowColColor(7, "all", "ff0000")  # 设置第7行所有列背景色

# print("2.15.3 设置所有单元格背景色".center(100, "-"))
# Openpyxl_PO.setAllCellColor("ff0000")  # 设置所有单元格背景色
# Openpyxl_PO.setAllCellColor(None)  # 清除所有单元格背景色

# print("2.16 设置整行(可间隔)背景色".center(100, "-"))
# Openpyxl_PO.setRowColor(5, 0, "ff0000")  # 从第5行开始每行颜色标红色
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