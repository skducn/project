# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-18
# Description: ...对象，获取矩阵第二列的值，解压迭代对象，展开的艺术，异常处理中巧用else，迭代器切片slice获取区间项
# Python编程进阶，常用八大技巧！ http://www.51testing.com/html/11/n-6391311.html
# ********************************************************************************************************************

'''
1，空函数占位符的三种方法 ... pass Ellipsis

'''


print("1，空函数占位符的三种方法 ... pass Ellipsis ".center(100, "-"))
#以下三个函数功能是一样的
def func():
    ...
def func():
    Ellipsis
def func():
    pass



# todo 字符串转函数之 eval

def function2(name, age):
    print("name: %s, age: %s" % (name, age))
    return 2

# eval 用于动态地执行字符串中的Python表达式或语句。它可以将一个字符串转为Python代码并执行。
func = "function2"
x = eval(func)("Alice", 11)
print(x)


