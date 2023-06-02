# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-7
# Description: dataframe 学习
# 官网api  https://pandas.pydata.org/docs/reference/frame.html#constructor
# *****************************************************************

import pandas as pd

# Constructor
# DataFrame([data, index, columns, dtype, copy])
# Two-dimensional, size-mutable, potentially heterogeneous tabular data.

# Attributes and underlying data
# Axes

# DataFrame.index
# The index(row labels) of the DataFrame.
# 行标签（索引）

# DataFrame.columns
# The column labels of the DataFrame
# 列标签（列名）

# DataFrame.dtypes
# This returns a Series with the data type of each column.
# https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
df = pd.DataFrame({'float': [1.0],
                   'int': [1],
                   'datetime': [pd.Timestamp('20180310')],
                   'string': ['foo']})
print(df.dtypes)   # //返回的索引是列名，列名的混合型被存储为Object类型
# float              float64
# int                  int64
# datetime    datetime64[ns]
# string              object
# dtype: object

print(type(df.dtypes))  # <class 'pandas.core.series.Series'>
print(df['int'].dtype)  # int64

# 获取每个类型的数量
print(df.dtypes.value_counts())
# float64           1
# int64             1
# datetime64[ns]    1
# object            1
# Name: count, dtype: int64


# Indexing,iteration
# DataFrame.loc
# Access a group of rows and columns by labels or a boolean array



# ----------------------------------------------------------------------------
# # loc函数，即location，标签定位
# # 将第一行数据竖向排列输出
# print(data.loc[0])
#
# # 将第一行数据中所属行业竖向排列输出
# print(data.loc[0, ['所属行业']])  # 所属行业    J 金融业
# print(type(data.loc[0]))  # <class 'pandas.core.series.Series'>
#
# # 将第一行数据转换成列表
# print(list(data.loc[0])) # ['主板', '000001', '平安银行', '1991-04-03', 19405918198.0, 19405534450.0, 'J 金融业', 0.9999802252077905, '主板J 金融业', 4519580162.0, 1.0]
#
# # iloc函数，即index-location,索引定位
# print(data.iloc[0:3,1:4])
# #      A股代码   A股简称      A股上市日期
# # 0  000001   平安银行  1991-04-03
# # 1  000002  万  科Ａ  1991-01-29
# # 2  000004   ST国华  1990-12-01