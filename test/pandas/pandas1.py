# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-11-13
# Description: pandas
# pandas是一个专注于数据处理的一个库，是基于NumPy构建的模块，使对数据预处理、清洗、分析工作变得更快更简单。
# pandas是专门为处理表格和混杂数据设计的，而NumPy更适合处理统一的数值数组数据。
# pandas有两种数据结构：Series（序列）和DataFrame（数据框），两者关系如下：
# 1，DataFrame的每一列或每一行都是一个序列（Series）。
# 2，DataFrame在操作每一行或每一列时都会转换为序列来处理。
# 3，序列Series是一维结构，数据框DataFrame是二维结构。
# Python利用pandas处理Excel数据的应用 https://www.cnblogs.com/liulinghua90/p/9935642.html
# ********************************************************************************************************************

import pandas as pd, numpy as np

'''

'''

# todo Series类型

print("1.1 series之列表数据输出索引和值".center(100, "-"))
sList = pd.Series([1, 2, 3])
print(sList)
# 0    1
# 1    2
# 2    3
# dtype: int64


print("1.2 series之字典数据输出索引和值".center(100, "-"))
sDict = pd.Series({"a":10, "b":20, "c":30})
print(sDict)
# a    10
# b    20
# c    30
# dtype: int64
print(sDict['a'])  # 10
print(sDict[0])  # 10
print(sDict.values)  # [10 20 30]


print("1.3 series之输出的相同的数据类型，全部转为浮点型。".center(100, "-"))
sFloat64 = pd.Series([1, 2, 3, np.nan])
print(sFloat64)
# 0    1.0
# 1    2.0
# 2    3.0
# 3    NaN
# dtype: float64
# // 由于np.nan是一个float类型的数据, 所以其他数据自动转为float类型输出，因为序列的数据类型必须相同。


print("2.1 series之设置index可自定义索引号。".center(100, "-"))
sIndex = pd.Series([1, 5.0, 1], index=["apple", "banana", "peal"])
print(sIndex)
# apple     1.0
# banana    5.0
# peal      2.0
# dtype: float64


print("2.2 series类型设置name。".center(100, "-"))
sName = pd.Series(data=['a', 'b', 'c'], name='Category')
print(sName)
# 0    a
# 1    b
# 2    c
# Name: Category, dtype: object
print(sName.name)  # Category
print(sName.index)  # RangeIndex(start=0, stop=3, step=1)
print(sName.dtype)  # object



print("3.1 series之输出每个值的重复数量".center(100, "-"))
s = pd.Series([1, 5.0, 1, 2, 1])
print(s.value_counts())
# 1.0    3
# 5.0    1
# 2.0    1
# dtype: int64

print("3.2 series之统计某个值的重复数量".center(100, "-"))
s = pd.Series([1, 5.0, 1, 2, 1])
print(s.value_counts()[1])  # 3





# todo DataFrame类型
# DataFrame既有行索引也有列索引，它可以被看做由Series组成的字典（共用同一个索引）。

print("4.1 DataFrame之输出标签（行的索引和列的名称）和值，数据字典中无内嵌字典。".center(100, "-"))
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002, 2003],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
df = pd.DataFrame(data)
print(df)
#     state  year  pop
# 0    Ohio  2000  1.5
# 1    Ohio  2001  1.7
# 2    Ohio  2002  3.6
# 3  Nevada  2001  2.4
# 4  Nevada  2002  2.9
# 5  Nevada  2003  3.2

print("4.2 DataFrame之输出标签（行的索引和列的名称）和值，数据字典中内嵌字典。".center(100, "-"))
# DataFrame方式是使用嵌套字典时，外层字典的键作为列名，内层字典的键作为行索引
df = pd.DataFrame({'Nevada': {2001: 2.4, 2002: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}})
print(df)
#       Nevada  Ohio
# 2001     2.4   1.7
# 2002     2.9   3.6
# 2000     NaN   1.5


print("4.3 DataFrame之自定义列（columns） 和索引号（index），不存在的列debt，会自动添加值为NaN".center(100, "-"))
df = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'], index=['one', 'two', 'three', 'four', 'five', 'six'])
print(df)
#        year   state  pop debt
# one    2000    Ohio  1.5  NaN
# two    2001    Ohio  1.7  NaN
# three  2002    Ohio  3.6  NaN
# four   2001  Nevada  2.4  NaN
# five   2002  Nevada  2.9  NaN
# six    2003  Nevada  3.2  NaN

print(df.columns)
# Index(['year', 'state', 'pop', 'debt'], dtype='object')


print("4.4.1 DataFrame之获某列取的所有值".center(100, "-"))
print(df['state'])
# one        Ohio
# two        Ohio
# three      Ohio
# four     Nevada
# five     Nevada
# six      Nevada
# Name: state, dtype: object


print("4.4.2 DataFrame之修改某列的所有制".center(100, "-"))
df['debt'] = 16.5
print(df)
#        year   state  pop  debt
# one    2000    Ohio  1.5  16.5
# two    2001    Ohio  1.7  16.5
# three  2002    Ohio  3.6  16.5
# four   2001  Nevada  2.4  16.5
# five   2002  Nevada  2.9  16.5
# six    2003  Nevada  3.2  16.5

print("4.5 DataFrame之格式化输出".center(100, "-"))
print("获取到所有的值:\n{0}".format(df))
# 获取到所有的值:
#        year   state  pop  debt
# one    2000    Ohio  1.5  16.5
# two    2001    Ohio  1.7  16.5
# three  2002    Ohio  3.6  16.5
# four   2001  Nevada  2.4  16.5
# five   2002  Nevada  2.9  16.5
# six    2003  Nevada  3.2  16.5


print("4.6 DataFrame之读取csv数据".center(100, "-"))
df = pd.read_csv('test.csv')
print(df)
#    姓名  age sex
# 0  张三   30   女
# 1  李四   28   1
# 2  王五   88   男


# print("4.7 DataFrame之读取部分csv数据（获取第1行数据，并移除第 3 行和第 5 行）".center(100, "-"))
# df = pd.read_csv('test.csv', sep=';',  nrows=1, skiprows=[3, 5])    # 读取前 1行数据，并移除第 3 行和第 5 行
# print(df)
# #   姓名,age,sex
# # 0    张三,30,女

# print("4.8 DataFrame之保存数据".center(100, "-"))
# df.to_csv('test.csv', index=None)
# df.to_csv('test.csv')   # 如果没有Index=None 则每次保存后会多一列序号。

print("4.9 DataFrame之输出前6条记录".center(100, "-"))
print(df.head(6))
# df.head() # 默认读取前5行的数据


print("4.10 DataFrame之获取第一条数据".center(100, "-"))
l_row = df.iloc[0].values  # 获取第二行数据，注意第一行是表头，数据从第二行开始，第二行是0，以此类推。
print(l_row)  # ['张三,30,女']


print("4.11 DataFrame之获取多行的数据".center(100, "-"))
l_row = df.iloc[[0, 2, 1]].values   # 注意输出的数据位置发生了变化
print(l_row)
# [['张三' 30 '女']
#  ['王五' 88 '男']
#  ['李四' 28 '1']]


print("4.12 DataFrame之 获取某行某列的值".center(100, "-"))
data = df.iloc[1, 1]  # 获取第三行第二列的值，注意第一行是表头，数据从第二行开始，第二行是0，以此类推。
print(data)  # 28


print("4.13 DataFrame之获取某行指定列的数据".center(100, "-"))
l_row = df.loc[[1, 2], ['sex','age']].values  # 获取第三四行sex和age列的值
print(l_row)
# [['1' 28]
#  ['男' 88]]