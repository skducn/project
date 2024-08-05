#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 动态创建和调用方法
# 方法名是一个字符串
#****************************************************************


for i in range(5):
    func = 'test' + str(i)
    param = 'hello'

    a = '''def ''' + str(func) + '''(''' + str(param) + '''):
        name = '张三'
        print("I'm ''' + str(func) + ''', ''' + param + '''")'''

        # print("I'm ''' + str(func) + ''', ''' + param + '''" , name )'''
    exec(a)
    exec(func + "('" + param + "')")
# # 相当于函数
# def test1(param):
#     name = '张三'
#     print("I'm test1, hello", name)


# I'm test0, hello
# I'm test1, hello
# I'm test2, hello
# I'm test3, hello
# I'm test4, hello