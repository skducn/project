# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2021-5-18
# Description: pivot_table 透视表的应用
# *****************************************************************


import pandas as pd
import numpy as np

data = pd.read_csv("BlackFriday.csv")
print(data.head())


print(data.isna().sum())

gender_purchase = data.pivot_table(index=["User_ID"], values="Purchase", aggfunc="sum")
# gender_purchase = data.pivot_table(index=["Gender","User_ID"],values="Purchase",aggfunc="sum")
gender_purchase = gender_purchase.reset_index()
print(gender_purchase.head(10))



top10 = data.pivot_table(index=["Product_ID"],values=['Purchase'],aggfunc="count").reset_index().sort_values(by="Purchase",ascending=False).head(10)
print(top10)





df = pd.DataFrame({'student': ['小红', '小红', '李华', '李华', '小天', '小天'],
                    'class': ['001','001','001','001','002','002'],
                   'subject': ['C', 'Java', 'Python', 'C', 'C', 'Python'],
                   'grades': [80,  90, 78, 90, 80, 78]})
print(df)
#   student class subject  grades
# 0      小红   001       C      80
# 1      小红   001    Java      90
# 2      李华   001  Python      78
# 3      李华   001       C      90
# 4      小天   002       C      80
# 5      小天   002  Python      78
print(df.pivot_table(index='subject'))
#             grades
# subject
# C        83.333333
# Java     90.000000
# Python   78.000000
print(df.pivot_table(columns='subject'))
# subject          C  Java  Python
# grades   83.333333  90.0    78.0

print(df.pivot_table(index='subject', aggfunc=lambda x: type(x)))
#                                          class  ...                                student
# subject                                         ...
# C        <class 'pandas.core.frame.DataFrame'>  ...  <class 'pandas.core.frame.DataFrame'>
# Java     <class 'pandas.core.frame.DataFrame'>  ...  <class 'pandas.core.frame.DataFrame'>
# Python   <class 'pandas.core.frame.DataFrame'>  ...  <class 'pandas.core.frame.DataFrame'>

print(df.pivot_table(index='subject', aggfunc=lambda x: x.tolist()))
#                    class        grades       student
# subject
# C        [001, 001, 002]  [80, 90, 80]  [小红, 李华, 小天]
# Java               [001]          [90]          [小红]
# Python        [001, 002]      [78, 78]      [李华, 小天]

# 原来就是通过指定维度后透视得到的值的列表，或者你可以理解是通过lookup来得到的一列值。所以mean函数在作用于class、student这两列是字符串元素的列表肯定是不对的，所以被过滤掉了。

# 统计各个班级(class)的平均分以及班级学生人数
print(df.pivot_table(index='class', aggfunc={'grades': np.mean, 'student': lambda x: len(x.unique())}))
#        grades  student
# class
# 001      84.5        2
# 002      79.0        1

# 统计各个班级(class)的各个科目(subject)的平均分
print(df.pivot_table(index='class', columns='subject',  values='grades'))
# subject     C  Java  Python
# class
# 001      85.0  90.0    78.0
# 002      80.0   NaN    78.0


# 统计各个班级(class)的各个科目(subject)的最高分,并且将空值填充为0
print(df.pivot_table(index='class', columns='subject',  values='grades', aggfunc=max, fill_value=0))
# class
# 001      90    90      78
# 002      80     0      78

# 统计各个班级(class)的各个科目(subject)的人数
print(df.pivot_table(index='class', columns='subject',  values='grades', aggfunc='count', fill_value=0))
# subject  C  Java  Python
# class
# 001      2     1       1
# 002      1     0       1

# 统计各个学生(student)的最高分,最低分,平均分
print(df.pivot_table(index='student', values='grades', aggfunc=[np.max, np.min, np.mean]))
# max = np.max , min = np.min
#            max    min   mean
#         grades grades grades
# student
# 小天          80     78     79
# 小红          90     80     85
# 李华          90     78     84

# 上面是多级索引,可能你想去掉grades这一级, 可以参考下面方法
# stack()是行转列, 把grades从column变成了index, 再reset_index去掉grades
#
print(df.pivot_table(index='student', values='grades', aggfunc=[max, min, np.mean]).stack().reset_index(level=-1, drop=True))
#          max  min  mean
# student
# 小天        80   78    79
# 小红        90   80    85
# 李华        90   78    84



