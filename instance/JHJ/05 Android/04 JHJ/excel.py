#http://www.cnblogs.com/lhj588/archive/2012/01/06/2314181.html
#链表推到，结果[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
info = [2*x for x in range(10)]
print info

#在输出的结果左面添加0 ，如以下结果是 00012
s='12'.zfill(5)
print (s)

#format格式化输出 str.format()
print('We are the {} who say "{}!"'.format('knights', 'Ni'))
print('{0} and {1}'.format('spam', 'eggs'))
print('{1} and {0}'.format('spam', 'eggs'))
print('This {food} is {adjective}.'.format(food='spam', adjective='absolutely horrible'))
print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred',other='Georg'))


x = 2 # this gets overwritten
print [x**3 for x in range(5)]

vec1 = [2, 4, 6]
vec2 = [4, 3, -9]
print [x*y for x in vec1 for y in vec2]

# 写EXCEL，pyExcelerator 0.6.4a， https://pypi.python.org/pypi/pyExcelerator/
# 读EXCEL，xlrd 0.9.4，https://pypi.python.org/pypi/xlrd

#pyExcelerator 写Excel
from pyExcelerator import *
w = Workbook()     #创建一个工作簿
ws = w.add_sheet('sheet1')     #创建一个工作表
# ws.write(0,0,'bit')    #在1行1列写入bit
# ws.write(0,1,'huang')  #在1行2列写入huang
# ws.write(1,0,'xuan')   #在2行1列写入xuan
# w.save('mini.xls')     #保存

#xlwt 写EXCEL2003 ，可对EXCEL进行格式化、字体颜色等控制
import xlwt
from datetime import datetime
wbk = xlwt.Workbook()
sheet = wbk.add_sheet("sheet1")
style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='YYYY-MM-DD')
wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')
ws.write(0, 0, 1234.56, style0)
ws.write(1, 0, datetime.now(), style1)
ws.write(2, 0, 1)
ws.write(2, 1, 1)
ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('example.xls')

#xlrd 读Excel
import xlrd
fname = "test.xls"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    #获取一个工作表
    #sh = bk.sheet_by_index(0)  #通过索引顺序获取
    #sh = bk.sheets()[0]        #通过索引顺序获取
    sh = bk.sheet_by_name("Sheet1") #通过名称获取
    #sh = bk.sheet_by_name(u'Sheet1') #通过名称获取
except:
    print "no sheet in %s named Sheet1" % fname
nrows = sh.nrows #获取行数
ncols = sh.ncols #获取列数
# print "nrows %d, ncols %d" % (nrows,ncols)
#获取第一行第一列数据
cell_value0 = sh.cell_value(0,0)
# print cell_value0
cell_value = sh.cell_value(1,1)
# print cell_value

#获取各行数据，拆分原数据并保持到其他文档中，如
#原单元格C1数据：123,456,789
#目标单元格A1=123，B1=456,C1=789
row_list = []
mydata = []
for i in range(1,nrows): #1,2,3,4
    row_data = sh.row_values(i) #每行的信息
    col_data = sh.col_values(1) #每列的信息
    cella = sh.cell(i,1).value #某个单元值
    #cellb = sh.cell(rowx=0,colx=1).value
    #cell_A1 = bk.row(0)[0].value#使用行列索引
    print cella

    pkgdatas = row_data[2].split(',')
    x=0
    for pkgdata in pkgdatas:
        ws.write(i,x,pkgdata)
        x=x+1
w.save('mini.xls')

#将文件复制到指定目录
import os
import shutil
filepath="test.xls"
if os.path.exists(filepath):
    shutil.copy(filepath,"./folder1/")