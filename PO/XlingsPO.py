# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-12-8
# Description   : xlwings 对象层
# https://docs.xlwings.org/en/stable/installation.html
# https://docs.xlwings.org/en/stable/quickstart.html

# https://blog.csdn.net/weixin_42146296/article/details/103647940
# https://www.cnblogs.com/Teyisang/p/14729307.html
# https://zhuanlan.zhihu.com/p/348393559

# https://github.com/xlwings/xlwings/issues/934
# pip install appscript
# *********************************************************************

import xlwings as xw
import sys
# app = xw.App(visible=True, add_book=False)  # 属性visible表示工作簿是否可见，属性          add_book表示是否新增工作簿
#
# app.display_alerts = False  # 关闭一些提示信息，可以加快运行速度，默认为True
#
# app.screen_updating = False  # 更新显示工作表的内容，默认为 True，关闭它可以提升运行速度。

# print(xw.__version__)


# 创建文件

# wb = xw.Book()
# wb.save('1.xlsx')
# wb.close()

# app = xw.App(visible=True, add_book=False)
# wb = app.books.add()
# wb.save('111.xlsx')
# wb.close()
# # app.quit()


# wb =xw.Book()
# sh = wb.sheets['Sheet1']
# wb.save(f'111.xlsx')
# wb.close()

# 打开表
# app = xw.App(visible=False, add_book=False)
# wb = app.books('./data/kill.xlsx')


# 打开表
wb = xw.Book('./data/kill.xlsx')


# todo 工作表

# 所有工作表名
print(wb.sheet_names)  # ['hello34', 'abc', 'Sheet1', 'Sheet2', 'Sheet3']

# 工作表数量
# print(wb.sheets.count)  # 5

# 新建工作表
# wb.sheets.add("jinhao")

# 在工作表jinhao前新增工作表titi
# wb.sheets.add(name="titi", before='jinhao')

# 在工作表jinhao后新增工作表yoyo
# wb.sheets.add(name="yoyo2", after='jinhao')
# 并激活yoyo工作表
# sh = wb.sheets.active

# 删除工作表（如不存在也不会报错）
# wb.sheets["yoyo"].delete()

# 激活指定的工作表
wb.sheets['Sheet2'].activate()
sht = wb.sheets["Sheet2"]   # sht = wb.sheets[3]

# 查看指定索引的工作表名
# print(wb.sheets[1].name)

# 重命名表格sheet
# wb.sheets[1].name='abc'



# todo 工作表格式化

# 获取总行数
# print(sht.used_range.last_cell.row)  # 5
# print(sht.used_range.last_cell.column)  # 6

# 获取高度与宽度
# print(xw.Range('a1:c2').height) # 66.0  返回range的高度
# print(xw.Range('a1:b3').width)  # 341.0  返回range的宽度

# # 设置A1行高度
# sht.range("A1").row_height = 33
# # 设置A1-A5行高度
# sht.range("A1:A5").row_height = 33

# 设置宽度
# sht.range("B1").column_width = 33  # 设置B列宽度
# sht.range("B1:D3").column_width = 33  # 设置BCD列宽度

# 设置单元格填充色（背景色）
# sht.range('B3').color= 255,200,255 # 粉色
# 删除背景色
# sht.range('B3').color = None

#在整个工作表上自动调整宽度,可传参数
# sht.autofit(axis='c')
# xw.Range('a1').autofit()
# 自动调整列宽
# sht.range('A1:B2').columns.autofit()
# 自动调整行高
# sht.range('A1:B2').rows.autofit()

# 清空内容和格式
# sht.clear()
# 清除内容，但保留格式
# sht.clear_contents()

# 返回表示范围参考的字符串值，输出为$a$2
# print(xw.Range('A2').address)  # $A$2
# print(sht.range('A2').address)  # 同上
# print(xw.Range('A2:C4').address)  # $A$2:$C$4


# ？返回对应sheet的索引值，从0计数
# print(sht.index())

# sht.range("B3").options(expand='table').api.Font.Color = 0xFF0000 #

# 设置单元格格式
# xw.Range('A1:C3').number_format = '0.00%'

# # 清除单元格内容
# sht.range('A1').clear()
# # 清除单元格内容，但保留格式
# sht.range('A2').clear_contents()



# todo 单元格

# # 获取坐标的值
# print(sht.cells(1,2).value)  # 1  //相当于B1
#
# # 获取A2单元格值
# print(sht.range("A2").value)
#
# # 获取A3-C3单元格值（列表）
# print(sht["A3:C3"].value)
#
# # 获取第二行第四列的值。
# print(sht[1,3].value)

# # 获取区间行列
# print(xw.Range('B2:C4').shape)  # （3，2）
#
# # 获取区间列表值
# print(xw.Range('B2:C4').options(ndim=2).value)  # [[5.0, 11.0], [100.0, '测试'], [2.0, '呃呃']]

# # 获取超链接
# print(xw.Range ('A1').hyperlink)  # http://www.baidu.com
# # 获取值
# print(xw.Range ('A1').value)  # www.baidu.com

# --------------

# 更新公式
# xw.Range('A2').formula = '=sum(c1:c2)'
# # 输出公式
# print(xw.Range('A2').formula)   # =SUM(C1:C2)

# 更新A1值（超链接）
# xw.Range('A1').add_hyperlink(address = 'www.baidu.com')

# # 从单元格开始更新行值，更新A3，B3，C3
# sht.range("A3").value=['a',100, "测试"]
# # 从单元格开始更新多行值
# sht.range('A4').options(expand='table').value = [[1, 2], [3, 4]]
#
# # 从单元格开始更新列值，更新A3，A4，A5
# sht.range("A3").options(transpose=True).value = ["行133", "行2", "行3"]
# # 从单元格开始更新列多列值
# sht.range('B6').options(expand='table',transpose=True).value = [[1,2,3,4] ,[11,12,13,14]]

# --------------

# 删除B2值，下方值自动上移
# sht.range('B2').delete()

# 删除第二行
# sht.range('2:2').delete()

# --------------

# ？插入
# sht.api.row('A2').insert()
# sht.range("a1").insert()
# sht.api.Rows("2:1").Insert()
sht.api.Rows(2).Insert()

# 插入单元格，从A2开始往右边移动。
# sht.range("A2").insert(shift='right')

# --------------


sys.exit(0)

wb.save()
# wb.close()





# sh = wb.sheets[0]
# value = sh.range('A3').value
# sh.range('A3').value = 'jinhao'
#
# wb.save()
# wb.close()


# 新建excel文件
# app = xw.App(visible=True, add_book=True)

# 添加一个新的工作薄
# wb = app.books.add()

# # 保存文件
# wb.save('a2.xlsx')
# wb.close()
# # app.quit()


# wb = xw.Book('./data/test99.xlsx')  # 打开已有excel文件
# # print(xw.apps.keys())
# # wb = xw.apps[3625].books['area2.xlsx']
# wb.close()
# ws = wb.sheets["sheet1"]  # 获取sheet表

# rows = ws.api.UsedRange.Rows.Formula  # 获取所有行数据内容
#
# row_count = ws.used_range.last_cell.row  # 获取最大行数
# print(row_count)
#
# col_count = ws.used_range.last_cell.col  # 获取最大列数
# print(col_count)

