# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-11-13
# Description: pandas 学习
# pandas是基于NumPy数组构建的，使数据预处理、清洗、分析工作变得更快更简单。
# pandas是专门为处理表格和混杂数据设计的，而NumPy更适合处理统一的数值数组数据。
# pandas有两个主要数据结构：Series和DataFrame。
# Python利用pandas处理Excel数据的应用 https://www.cnblogs.com/liulinghua90/p/9935642.html
# ********************************************************************************************************************

import pandas as pd, numpy as np

# todo Series类型
arr1 = np.arange(10)
print(arr1)  # [0 1 2 3 4 5 6 7 8 9]
print(type(arr1))  # <class 'numpy.ndarray'>
for i in arr1:
    print(i)

s1 = pd.Series(arr1)
print(s1)   # 第一列是索引，第二列是列表值
# 0    0
# 1    1
# 2    2
# 3    3
# 4    4
# 5    5
# 6    6
# 7    7
# 8    8
# 9    9

# Series和ndarray之间的主要区别在于Series之间的操作会根据索引自动对齐数据。


# todo DataFrame类型
# DataFrame是一个表格型的数据类型，每列值类型可以不同，是最常用的pandas对象。
# DataFrame既有行索引也有列索引，它可以被看做由Series组成的字典（共用同一个索引）。
# DataFrame中的数据是以一个或多个二维块存放的（而不是列表、字典或别的一维数据结构）。

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

# 输出指定列（columns） , 及指定索引号（index）#，不存在的列debt则输出NaN
df2 = pd.DataFrame(data, columns=['year', 'state', 'pop', 'debt'], index=['one', 'two', 'three', 'four', 'five', 'six'])
print(df2)
#        year   state  pop debt
# one    2000    Ohio  1.5  NaN
# two    2001    Ohio  1.7  NaN
# three  2002    Ohio  3.6  NaN
# four   2001  Nevada  2.4  NaN
# five   2002  Nevada  2.9  NaN
# six    2003  Nevada  3.2  NaN

print(df2.columns)
# Index(['year', 'state', 'pop', 'debt'], dtype='object')

print(df2['state'])
# one        Ohio
# two        Ohio
# three      Ohio
# four     Nevada
# five     Nevada
# six      Nevada
# Name: state, dtype: object

#列可以通过赋值的方式进行修改。例如，我们可以给那个空的"debt"列赋上一个标量值或一组值
df2['debt'] = 16.5
print(df2)
#        year   state  pop  debt
# one    2000    Ohio  1.5  16.5
# two    2001    Ohio  1.7  16.5
# three  2002    Ohio  3.6  16.5
# four   2001  Nevada  2.4  16.5
# five   2002  Nevada  2.9  16.5
# six    2003  Nevada  3.2  16.5



# DataFrame方式是可以使用嵌套字典，如果嵌套字典传给DataFrame，pandas就会被解释为外层字典的键作为列，内层字典键则作为行索引：
pop = {'Nevada': {2001: 2.4, 2002: 2.9},'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
df3 = pd.DataFrame(pop)
print(df3)
#       Nevada  Ohio
# 2001     2.4   1.7
# 2002     2.9   3.6
# 2000     NaN   1.5



# 读取数据
data = pd.read_csv('test.csv')
print(data)
data = pd.read_csv('test.csv', sep=';',  nrows=20, skiprows=[2, 5])    # 读取前 20 行数据，并移除第 2 行和第 5 行
print(data)

# 保存数据
data.to_csv('test.csv', index=None)
# data.to_csv('test.csv')   # 如果没有Index=None 则每次保存后会多一列序号。

# 查看前三行数据
print(data.head(3))

# print(data.loc[1,"level"])
#
# df = pd.read_excel('d:\\cases.xlsx') #这个会直接默认读取到这个Excel的第一个表单
# data = df.head()#默认读取前5行的数据
# print(data)
#
# # print("获取到所有的值:\n{0}".format(data))#格式化输出
#
# df=pd.read_excel('d:\\cases.xlsx',sheet_name='test_case')#可以通过sheet_name来指定读取的表单
# data=df.head()#默认读取前5行的数据
# print("获取到所有的值:\n{0}".format(data))#格式化输出
#
#
# data=df.iloc[0].values#0表示第一行 这里读取数据并不包含表头，要注意哦！
# # .ix is deprecated. Please use
# # .loc for label based indexing or
# # .iloc for positional indexing
# print("读取指定行的数据：\n{0}".format(data))
#
# data=df.iloc[[1,2]].values#读取指定多行的话，就要在ix[]里面嵌套列表指定行数
# print("读取指定行的数据：\n{0}".format(data))
#
# data=df.iloc[1,1]#读取第一行第1列的值，这里不需要嵌套列表
# print("读取指定行的数据：\n{0}".format(data))
#
#
# data=df.loc[[1,2],['年龄','金额']].values#读取第一行第二行的title以及data列的值，这里需要嵌套列表
# print("读取指定行的数据：\n{0}".format(data))
