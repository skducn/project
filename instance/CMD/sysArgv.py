# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-10-20
# Description: CMD命令行参数化之 sys.argv
# sys.argv 入参是一个有序的列表，命令行中必须按照脚本规定的顺序去输入参数，这种方法比较适合脚本中需要的参数个数很少且参数固定的脚本。
# 1，如果输入的参数比函数要求的多，多余的参数忽略
# 2，如果输入的参数比函数要求的少，则报错，一般需要设置异常捕获。
#***************************************************************
# 如：python dycmd.py --url https://v.douyin.com/2c6fEbw/
# click（）
# 参考：https://blog.csdn.net/weixin_33506900/article/details/112187887


import sys

def test_for_sys(year, name, body):
    print('the year is', year)  # 写实现功能
    print('the name is', name)
    print('the body is', body)

try:
    year, name, body = sys.argv[1:4]  # 将三个变量传入列表
    test_for_sys(year, name, body)  # 调用上面的函数来执行操作
except Exception as e:
    print(sys.argv)

# python sysArgv.py 1 2 3
# the year is 1
# the name is 2
# the body is 3

# python sysArgv.py 1 2
# ['sysArgv.py', '1', '2']  //输出异常捕获

