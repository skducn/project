# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-9-24
# Description   : argparse 是一个命令行参数解析模块，它运行在命令行下。
# 官网资料：https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
# 一个“-”的是指令，两个“--”的是接收指令内容的变量。
# python argparse1.py -h  //查看参数说明
# Python命令行参数解析包argparse的使用详解 https://www.jb51.net/article/262574.htm
# *********************************************************************

import argparse

def test_for_sys(year, name, body):
    print('the year is', year)
    print('the name is', name)
    print('the body is', body)  # 同上 定义函数功能

parser = argparse.ArgumentParser(usage="程序用途描述", description='帮助文档的描述', epilog="额外说明")
parser.add_argument('--name', '-n', help='name 属性，非必要参数', choices=['ok','error'])
parser.add_argument('--year', '-y', help='year 属性，非必要参数，但是有默认值', default=2017)  # 此处定义每个参数的必要性
parser.add_argument('--body', '-b', help='body 属性，必要参数', required=True)  # "-b"是"--body"的简写
args = parser.parse_args()

if __name__ == '__main__':
    try:
        test_for_sys(args.year, args.name, args.body)  # 此处调参即可
    except Exception as e:
        print("error")


# 使用2：输入2个整数进行乘法计算。
# 如： python argparse1.py -h
# 如： python argparse1.py 4 5
# 结果： 4 * 5 = 20
# parser.description = '输入2个整数输出乘法结果'
# parser.add_argument("ParA", help="我是A", type=int)
# parser.add_argument("ParB", help="我是B", type=int)
# args = parser.parse_args()
# print(str(args.ParA) + " * " + str(args.ParB) + " = ", args.ParA * args.ParB)

