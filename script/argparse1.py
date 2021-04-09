# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-9-24
# Description   : argparse 是一个命令行参数解析模块，它运行在命令行下。
# 官网资料：https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
# *********************************************************************

# import argparse
# parser = argparse.ArgumentParser()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)


# # 使用1：使用echo输出内容。
# 如 python argparse1.py john ，结果输出 john
# parser.description = '使用echo输出信息'    # 描述信息
# parser.add_argument("echo")
# args = parser.parse_args()
# print(args.echo)


# 使用2：输入2个整数进行乘法计算。
# 如： python argparse1.py -h
# 如： python argparse1.py 4 5
# 结果： 4 * 5 = 20
# parser.description = '输入2个整数输出乘法结果'
# parser.add_argument("ParA", help="我是A", type=int)
# parser.add_argument("ParB", help="我是B", type=int)
# args = parser.parse_args()
# print(str(args.ParA) + " * " + str(args.ParB) + " = ", args.ParA * args.ParB)

