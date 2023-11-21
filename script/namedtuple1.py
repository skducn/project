# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-7-17
# Description: collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None) 命名元组的工厂函数

# 定义：命名元组赋予每个位置一个含义，提供可读性和自文档性。它们可以用于任何普通元组，并添加了通过名字获取值的能力，通过索引值也是可以的。
# namedtuple 命名元组应用于元组tuple数据，可读性更强、内存占用也不会太多。
# 一般我们会将从文件或者数据库中读取出来的数据使用namedtuple去进行转化，让原始数据代表的含义依然能在这样的数据结构中保留，增加数据的可读性和操作的便捷性。

# Collections之namedtuple: https://blog.csdn.net/june_young_fan/article/details/91359194

# 标准库：https://docs.python.org/zh-cn/3.7/library/collections.html?highlight=collections#collections.namedtuple
# 英文：https://docs.python.org/3.6/library/collections.html#collections.namedtuple
# ********************************************************************************************************************

from collections import namedtuple


print("8".center(100, "-"))

EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, birthday, score, sex')

import csv
count = 0
for emp in map(EmployeeRecord._make, csv.reader(open("namedtuple.csv", "r", encoding="gbk"))):
    print(emp.name, emp.score)
    print(emp._asdict())  # {'name': '张三', 'age': '30', 'birthday': '1990/12/12', 'score': '数学', 'sex': '男'}



# import sqlite3
# conn = sqlite3.connect('/companydata')
# cursor = conn.cursor()
# cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
# for emp in map(EmployeeRecord._make, cursor.fetchall()):
#     print(emp.name, emp.title)



Point1 = namedtuple('Point', ['x', 'y'])
p = Point1(11, y=22)   # 创建的一个元组的子类，并实例化元组对象p
print(p)    # Point(x=11, y=22)
print(p[0], p[1])
print(type(p))  # <类与实例 '__main__.Point'>

a, b = p
print(a+b)  # 33  ,但不能 print(p.a + p.b)
print(p.y + p.x)  # 33


# 替换所有的原来（必须是所有的值）
t = [100, 200]
a = Point1._make(t)
print(a)  # Point(x=100, y=200)


# 可以将原值转化成有序字典
print(a._asdict())  # {'x': 100, 'y': 200}

# 替换某一个原值
print(a._replace(x=55))  # Point(x=55, y=200)


print(p._fields)  #  ('x', 'y')
print(a._fields)  #  ('x', 'y')

Color = namedtuple('Color', 'red green blue')
Pixel = namedtuple('Pixel', Point1._fields + Color._fields)
print(Pixel(111, 22, 128, 255, 0))  # Pixel(x=11, y=22, red=128, green=255, blue=0)

print(getattr(p, 'x'))

# 将字典通过拆包的形式转换成namedtuple
d = {'x': 11, 'y': 2554}
print(Point1(**d))  # Point(x=11, y=2554)
p1 = Point1(**d)
print(p1[1])  # 2554



