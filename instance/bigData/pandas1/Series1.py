# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-7
# Description: Series 学习
# 官网api  https://pandas.pydata.org/docs/reference/series.html
# *****************************************************************

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
a = Sqlserver_PO.selectParam("select * from a_test where id=%s", 3)
print(a)

# import pandas as pd
# import numpy as np
#
# # Constructor
# # DataFrame([data, index, dtype, name, copy,...])
# # One-dimensional ndarray with axis lables (including time series) .
#
# # Attributes
# # Axes
#
# # Series.index
# # The index(axis labels) of the Series.
# # 轴标签（索引）
#
# # Series.array
# print(pd.Series([1, 2, 3]).array)
# # <PandasArray>
# # [1, 2, 3]
# # Length: 3, dtype: int64
#
# ser = pd.Series(pd.Categorical(['a', 'b', 'a']))
# print(ser.array)
# # ['a', 'b', 'a']
# # Categories (2, object): ['a', 'b']
#
# # Series.values
# # Return Series as ndarray or ndarray-like depending on the dtype.
#
# print(pd.Series([1, 2, 3]).values)  # [1 2 3]    //是array不是列表
# print(pd.Series(list('aabc')).values)  # ['a' 'a' 'b' 'c']
# print(pd.Series(list('aabc')).astype('category').values)
#
# # Series.dtype
# # 正数强制转化成浮点数
# print(pd.Series([1, 2, 3, 4, 5, 6.0]))
# # 0    1.0
# # 1    2.0
# # 2    3.0
# # 3    4.0
# # 4    5.0
# # 5    6.0
# # dtype: float64
#
# # 如有字符串则强制转换成 object 类型
# print(pd.Series([1, 2, 3, 6.0, "foo"]))
# # 0      1
# # 1      2
# # 2      3
# # 3    6.0
# # 4    foo
# # dtype: object