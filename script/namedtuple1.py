# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-7-17
# Description: collections - namedtuple
# https://blog.csdn.net/june_young_fan/article/details/91359194
# typename：实际上就是你通过namedtuple创建的一个元组的子类的类名，通过这样的方式我们可以初始化各种各样的实例化元组对象。
# ********************************************************************************************************************

from collections import namedtuple

Point1 = namedtuple('Point', ['x', 'y'])
p = Point1(11, y=22)   # 创建的一个元组的子类，并实例化元组对象p
print(p)    # Point(x=11, y=22)
print(p[0], p[1])
print(type(p))  # <class '__main__.Point'>

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
