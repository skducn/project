# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-11-13
# Description: pandas 学习
# https://www.cnblogs.com/liulinghua90/p/9935642.html
# ********************************************************************************************************************

import  pandas  as pd

df = pd.read_excel('d:\\cases.xlsx') #这个会直接默认读取到这个Excel的第一个表单
data = df.head()#默认读取前5行的数据
print(data)

# print("获取到所有的值:\n{0}".format(data))#格式化输出

df=pd.read_excel('d:\\cases.xlsx',sheet_name='test_case')#可以通过sheet_name来指定读取的表单
data=df.head()#默认读取前5行的数据
print("获取到所有的值:\n{0}".format(data))#格式化输出


data=df.iloc[0].values#0表示第一行 这里读取数据并不包含表头，要注意哦！
# .ix is deprecated. Please use
# .loc for label based indexing or
# .iloc for positional indexing
print("读取指定行的数据：\n{0}".format(data))

data=df.iloc[[1,2]].values#读取指定多行的话，就要在ix[]里面嵌套列表指定行数
print("读取指定行的数据：\n{0}".format(data))

data=df.iloc[1,1]#读取第一行第1列的值，这里不需要嵌套列表
print("读取指定行的数据：\n{0}".format(data))


data=df.loc[[1,2],['年龄','金额']].values#读取第一行第二行的title以及data列的值，这里需要嵌套列表
print("读取指定行的数据：\n{0}".format(data))
