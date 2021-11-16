#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2019-1-16
# Description: 反射机制
# 在运行中,对于任意一个实体类,都知道这个类的所有属性和方法/
# 对于任意一个对象,都能够调用它的任意方法和属性;
# 这种动态获取信息以及动态调用对象方法的功能称为面向对象语言的反射机制.
# getattr() 函数用于返回一个对象属性值。
#****************************************************************

import sys,inspect
# sys.path.append('E:\51\\Python\\09project\\common\\interface\\interFrame1')  # 如果要在cmd中执行python，需要加上路径，否则 public.PageObject.DatabasePO无法找到这个模块。

from instance.zyjk.epidemic.frame1.iDriven import *
http = HTTP()

def run(line):

    global http
    func = getattr(http, line[2])  # line[2]=method
    args = inspect.getfullargspec(func).__str__()
    # FullArgSpec(args=['self', 'interURL', 'param'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={})
    args = args[args.find('args=') + 5:args.find(', varargs')]
    args = eval(args)
    # print(args)  # ['self', 'interURL', 'param']
    args.pop(0)
    # print(args)
    l = len(args)  #  依据xls - result函数中 jsonres = reflection.run([caseName, interURL, method, param])
    if l == 0:
        return func()
    elif l == 2:
        return func(line[1], line[3])  # [interURL, param]
    elif l == 3:
        return func(line[1], line[3], line[4])  # [interURL, param, d_var]
    # elif l == 4:
    #     return func(line[2],line[3],line[4],line[5])




