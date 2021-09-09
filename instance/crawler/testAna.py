# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-7-1
# Description: 爬取 去哪儿 大连景区数据,分析数据
#***************************************************************

import pandas as pd
import numpy as np
df = pd.read_excel('d:\\test.xlsx', names=['景点名称','星级', '城区','热度','地址','价格','月销量'])
# print(df.head())
# df = df.drop_duplicates()
# # print(df)
# print(df.info())

# d = {'one' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
#      'two' : pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])}
#
# df = pd.DataFrame(d)
# print(df)
df = pd.DataFrame([[1, 2], [3, 4]], columns = ['a','b'])
df2 = pd.DataFrame([[5, 6], [7, 8]], columns = ['a','b'])

df = df.append(df2)

print(df)

df = df.drop(0)

print(df)
# print(df.loc[0].reset_index())
# print("~~~~~~~~~~~~~~")
# df = df.loc[0].reset_index()
# print(df.iloc[1])
# print(df.iloc[1]["a"])


