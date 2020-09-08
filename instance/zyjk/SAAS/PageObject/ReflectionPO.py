#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2020-8-27
# Description: 反射机制
# 在运行中,对于任意一个实体类,都知道这个类的所有属性和方法/
# 对于任意一个对象,都能够调用它的任意方法和属性;
# 这种动态获取信息以及动态调用对象方法的功能称为面向对象语言的反射机制.
#****************************************************************

import inspect

from instance.zyjk.SAAS.PageObject.HttpPO import *
Http_PO = HttpPO()

def run(line):

    global Http_PO
    func = getattr(Http_PO, line[1])  # line[1]=method   # post,get,pull
    args = inspect.getfullargspec(func).__str__()  # FullArgSpec(args=['self', 'interName', 'param'], varargs=None, varkw=None, defaults=('',), kwonlyargs=[], kwonlydefaults=None, annotations={})
    print(args)
    args = args[args.find('args=') + 5:args.find(', varargs')]  # ['self', 'interName', 'param']
    args = eval(args)  # ['self', 'interName', 'param']
    print(args)
    args.pop(0)  # ['interName', 'param']
    l = len(args)  #  依据xls - result函数中 jsonres = reflection.run([caseName, method, interName, param])  line2=interName ,line3=param
    if l == 0:
        return func()
    elif l == 2:
        return func(line[2], line[3])
    elif l == 3:
        return func(line[1],line[2],line[3])
    elif l == 4:
        return func(line[0],line[1],line[2],line[3])




