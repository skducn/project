# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 输入输出美化
# https://www.runoob.com/python3/python3-inputoutput.html
# str()： 函数返回一个用户易读的表达形式。
# repr()： 产生一个解释器易读的表达形式，可以转义字符串中的特殊字符
# ********************************************************************************************************************

s = "heloo,john"
print(str(s))  # heloo,john
print(repr(s))  # 'heloo,john'

# repr()函数可以转义字符串中的特殊字符
hello = 'hello, runoob\n123'
print(repr(hello))  # 'hello, runoob\n123'
print(str(hello))
# hello, runoob
# 123

# repr() 的参数可以是 Python 的任何对象
x = 100
y = 200
print(repr((x, y, ('Google', 'Runoob'))))  # (100, 200, ('Google', 'Runoob'))


# 实例，输出一个平方与立方的表:
# 方法1：
for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    print(repr(x*x*x).rjust(4))
# 字符串对象的 rjust() 方法, 它可以将字符串靠右, 并在左边填充空格。
# 还有类似的方法, 如 ljust() 和 center()。 这些方法并不会写任何东西, 它们仅仅返回新的字符串。

# 方法2：
for x in range(1, 11):
    print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))

#  1   1    1
#  2   4    8
#  3   9   27
#  4  16   64
#  5  25  125
#  6  36  216
#  7  49  343
#  8  64  512
#  9  81  729
# 10 100 1000


# 实例： zfill(), 它会在数字的左边填充 0，如下所示：
print('12'.zfill(5))  # 00012
print( '-3.14'.zfill(7))  # -003.14
print('3.14159265359'.zfill(5))   # 3.14159265359


# 实例：str.format(), {}、{数字}、关键字进行替换
print('{}网址： "{}!"'.format('菜鸟教程', 'www.runoob.com'))  # 菜鸟教程网址： "www.runoob.com!"
print('{0} 和 {1}'.format('Google', 'Runoob'))   # Google 和 Runoob
print('{1} 和 {0}'.format('Google', 'Runoob'))   # Runoob 和 Google
print('{name}网址： {site}'.format(name='菜鸟教程', site='www.runoob.com'))  # 菜鸟教程网址： www.runoob.com
print('站点列表 {0}, {1}, 和 {other}。'.format('Google', 'Runoob', other='Taobao'))  # 站点列表 Google, Runoob, 和 Taobao。
import math
print('常量 PI 的值近似为 {0:.3f}。'.format(math.pi))  # 常量 PI 的值近似为 3.142。  //可选项 : 和格式标识符可以跟着字段名
# 在 : 后传入一个整数, 可以保证该域至少有这么多的宽度。 用于美化表格时很有用。
table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
for name, number in table.items():
   print('{0:10} ==> {1:10d}'.format(name, number))
# Google     ==>          1
# Runoob     ==>          2
# Taobao     ==>          3
table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
print('Runoob: {Runoob:d}; Google: {Google:d}; Taobao: {Taobao:d}'.format(**table))  # Runoob: 2; Google: 1; Taobao: 3

