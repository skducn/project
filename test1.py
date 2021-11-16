# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# *****************************************************************

d_var = '{"var11":"$.code","var12":"$.msg","var13":"$.data.list[0].name"}'
for a in range(1, len(d_var.split("$."))):
  var = d_var.split("$.")[a].split('"')[0]
  var = "$." + var
  print(var)
  # x = jsonpath.jsonpath(d_response, expr=var)
  # print(str(a) + ", " + str(x))
  # d_var = d_var.replace(var, str(x[0]))


# x = ['老', '空', '老 糖', '糖\n1', '老', '空', '糖', '糖\n1', '糖', '空', '老 高', '高\n2', '老', '空', '老 高', '高\n2', '老 高 糖', '高\n1\n糖\n1', '老 高', '高\n2']
# list1 = []
# for i in range(len(x)):
#  list1.append(x[i].replace("\n", ""))
# print(list1)



# x = ['老', '', '老 糖', '糖\n1', '老', '', '糖', '糖\n1', '糖', '', '老 高', '高\n2', '老', '', '老 高', '高\n2', '老 高 糖', '高\n1\n糖\n1', '老 高', '高\n2',"",""]
# tmp = []
# for i in range(20):
#  if x[i] == '':
#   tmp.append("空")
#  else:
#   tmp.append(x[i])
#
#
# print(tmp)

#
# l_33= ['13764376490', '孙*祥', '其他', '-', '87.8%', '4', '2', '-', '-', '-', '聂*亮', '老', '未发现档案', '0.0%', '-', '-', '-', '-', '-', '范*利', '糖', '未发现档案', '0.0%', '-', '-', '-', '-', '-', '忻*强', '老', '-', '69.3%', '6', '25', '28', '-', '-', '65025814', '张*中', '其他', '-', '42.9%', '4', '24', '-', '-', '-', '13020143988', '张*梅', '其他', '-', '42.9%', '4', '24', '-', '-', '-', '18001908015', '管*航', '其他', '-', '42.9%', '4', '24', '-', '-', '-', '13062737935', '庞*勇', '糖', '-', '82.3%', '5', '24', '5', '-', '-', '13661684669', '钱*国', '其他', '-', '42.9%', '4', '24', '-', '-', '-', '65103710', '马*龙', '老', '-', '70.3%', '5', '24', '28', '-', '-']
# l4 = []
# for i in range(len(l_33)):
#  if "*" in l_33[i] and i == 0:
#   l4.append("空")
#  elif "*" in l_33[i]:
#   print(i)
#   if len(l_33[i - 1]) < 7:
#    l4.append("空1")
#   else:
#    l4.append(l_33[i-1])
#   l4.append(l_33[i])
#   l4.append(l_33[i+1])
#   l4.append(l_33[i+2])
#   l4.append(l_33[i+3])
#   l4.append(l_33[i+4])
#   l4.append(l_33[i+5])
#   l4.append(l_33[i+6])
#   l4.append(l_33[i+7])
#   l4.append(l_33[i+8])
#
# print(l_33)
# print(l4)
#
#
# from PO.ListPO import *
# List_PO = ListPO()
#
# a = ['古*尔', '000000000000000000', '戴*星', '110108195005133414']
# b = ['13764376490', '孙*祥', '其他', '-', '87.8%', '4', '2', '-', '-', '-', '空1', '聂*亮', '老', '未发现档案', '0.0%', '-', '-', '-', '-', '-']
# print(List_PO.listSplitSubList(a, 2))
# print(List_PO.listSplitSubList(b, 10))
# x = List_PO.listSplitSubList(a, 2)[1] + List_PO.listSplitSubList(b, 10)[1]
# print(x)
#
# d = {
#  "diastolicBloodPressure": 91,
#  "heartRate": 66,
#  "measurementDate": "2021-03-23 17:01",
#  "systolicPressure": 121,
#  "id": ""
# }
#
# print(d)
#
# import textwrap
#
# text = """abcdefg
# hijklmn
# opqrstuvwxyz
# """
#
# print(text)
#
# # # # todo: fill() 调整换行符,每行显示给定宽度，注意下一行前会有空格
# print("fill() 调整换行符,每行显示给定宽度".center(100, "-"))
# print(textwrap.fill(text, width=6))
# # abcdef
# # g hijk
# # lmn op
# # qrstuv
# # wxyz
#
# # # # todo:dedent() 去除缩进
# print("dedent()去除缩进".center(100, "-"))
# sample_text = '''    aaabbb    cccddd'''
# print(textwrap.dedent(sample_text))
# # # # aaabbb    cccddd
#
# # # # todo:indent() 给定前缀
# print(":indent() 给定前缀".center(100, "-"))
# print(textwrap.indent(text, prefix='----'))
# # ----abcdefg
# # ----hijklmn
# # ----opqrstuvwxyz
#
#
# s = 'hello\n\n \nworld'
#
# # # 默认忽略空白符（包括任何行结束符）组成的行（\n）
# print(textwrap.indent(s, '+ '))
# # + hello
#
# # + world
#
#
# # # 函数对象 = lambda 参数：表达式
# print(textwrap.indent(s, '+ ', lambda line: True))
# # + hello
# # +
# # +
# # + world
#
# #
# # # todo:首行缩进，其余行添加前缀22，每行限制字符10个。
# # print("首行缩进，其余行添加前缀22，每行限制字符10个。".center(100, "-"))
# # # subsequent_indent:初始化除了第一行的所有行
# # detent_text = textwrap.dedent(text).strip()
# # print(textwrap.fill(detent_text, initial_indent='  ', subsequent_indent='22', width=10))
# # #   abcdefg
# # # 22hijklmn
# # # 22opqrstuv
# # # 22wxyz
# #
# #
# # # todo:shorten() 多余的省略号
# # print("shorten() 多余的省略号".center(100, "-"))
# # print(textwrap.shorten(text, width=20))
# # # abcdefg [...]
# # print(textwrap.shorten("Hello world", width=10, placeholder="..."))
# # # Hello...
# #
# # # todo:wrap() 将一个字符串按照width的宽度进行切割，切割后返回list
# # print("wrap() 将一个字符串按照width的宽度进行切割，切割后返回list".center(100, "-"))
# # print(textwrap.wrap(text, width=10))
# # # ['abcdefg', 'hijklmn op', 'qrstuvwxyz']
# # # 分析：结果并不是保证了每个list元素都是按照width的，因为不但要考虑到width，也要考虑到空格（换行），也就是一个单词。
# #
# # sample_text = 'aaabbbcccdddeeeedddddfffffggggghhhhhhkkkkkkk'
# # print(textwrap.wrap(sample_text, width=5))
# # # ['aaabb', 'bcccd', 'ddeee', 'edddd', 'dffff', 'fgggg', 'ghhhh', 'hhkkk', 'kkkk']
# #
# #
# # print("定义 class textwrap.TextWrapper(…)".center(100, "-"))
# # # class textwrap.TextWrapper(…) # 这个类的构造函数接受一系列的关键字参数来初始化自己的属性信息
# # sample_text = '''aaa'''
# # textWrap = textwrap.TextWrapper()
# # textWrap.initial_indent = 'bbb'
# # print(textWrap.wrap(sample_text))
# # # ['bbbaaa']
# #
# # sample_text = '''aaa
# # kkk
# # jjj'''
# # textWrap = textwrap.TextWrapper(width = 2)
# # textWrap.initial_indent = 'bbb'
# # textWrap.subsequent_indent = 'ccc'
# # print(textWrap.wrap(sample_text))
# # # ['bbba', 'ccca', 'ccca', 'ccck', 'ccck', 'ccck', 'cccj', 'cccj', 'cccj']
# #
# #
# #
# # a = ["welcome,linuxmi.com,33"]
# # for i in a:
# #     print(i.count(',') + 1)
# #
# #
# # import numpy as np
# # #创建数组
# # a = np.array([2,1,0,5])
# # print(a)
# # print(a[:3])
# # print(a.min())
# # a.sort()
# # b = np.array([1,2,3],[4,5,6])
# print(b*b)