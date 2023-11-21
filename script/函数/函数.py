# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-18
# Description: ...对象，获取矩阵第二列的值，解压迭代对象，展开的艺术，异常处理中巧用else，迭代器切片slice获取区间项
# Python编程进阶，常用八大技巧！ http://www.51testing.com/html/11/n-6391311.html
# ********************************************************************************************************************

'''
1，空函数占位符的三种方法 ... pass Ellipsis
2，eval调用字符串函数
3，创建动态函数
'''

# todo 空函数占位符的三种方法 ... pass Ellipsis
#以下三个函数功能是一样的
def func():
    ...
def func():
    Ellipsis
def func():
    pass


# todo eval调用字符串函数
# eval 用于动态地执行字符串中的Python表达式或语句。它可以将一个字符串转为Python代码并执行。

def function2(name, age):
    print("name: %s, age: %s" % (name, age))
    return 2

x = eval("function2")("Alice", 11)  # 相当于 function2("alice", 11)
print(x)
# name: Alice, age: 11
# 2


# todo 创建动态函数
for i in range(5):
    func = 'test' + str(i)
    param = 'hello'

    a = '''def ''' + str(func) + '''(''' + str(param) + '''):
        name = '张三'
        print("I'm ''' + str(func) + ''', ''' + param + '''")'''
    exec(a)
    exec(func + "('" + param + "')")
# # 相当于函数
# def test1(param):
#     name = '张三'
#     print("I'm test1, hello")

# I'm test0, hello
# I'm test1, hello
# I'm test2, hello
# I'm test3, hello
# I'm test4, hello