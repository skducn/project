# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-1-2
# Description: LEGB规则, 决定变量和函数的作用域解析。
# 作用：在给定环境中查找和访问变量和函数的顺序。
# 局部作用域 Local、闭包函数外的函数Enclosing、全局作用域Global和内置作用域Built-in
# http://www.51testing.com/html/71/n-7799171.html
# *****************************************************************


# todo 局部作用域 Local
# def abc():
#     x =10
#     print(x)
# abc()   # 10

# todo 闭包函数外的函数Enclosing
def enclosing_scope_example():
    x =11
    def inner():
        print(x)
    inner()
enclosing_scope_example()  # 11


# todo 全局作用域Global
x =12
def global_score_example():
    print(x)
global_score_example()  # 12



# todo 内置作用域Built-in
import math
def built_in_scope_example():
    print(math.pi) # 输出内置变量math.pi的值
built_in_scope_example()  # 3.141592653589793








