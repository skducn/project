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

