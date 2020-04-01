# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2019-1-16
# Description: 反射机制
# 在运行中,对于任意一个实体类,都知道这个类的所有属性和方法/
# 对于任意一个对象,都能够调用它的任意方法和属性;
# 这种动态获取信息以及动态调用对象方法的功能称为面向对象语言的反射机制.
#****************************************************************

import Math, inspect

# func = getattr(Math, 'say')
# print(func())  # hello
#
# func = getattr(Math, 'add')
# print(func(1, 3))  # 4


# 反射获取函数
def run(line):
    func = getattr(Math, line[1])
    args = inspect.getfullargspec(func).__str__()
    args = args[args.find('args=') + 5:args.find(', varargs')]
    args = eval(args)
    l = len(args)  # 2 , 因为add有2个参数.
    if l == 0:
        return func()
    elif l == 2:
        return func(line[2],line[3])




