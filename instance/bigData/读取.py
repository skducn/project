# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2024-5-21
# Description: pandas 读取
# PySpark，它是Spark的python api接口。
# PySpark处理大数据的好处是它是一个分布式计算机系统，可以将数据和计算分布到多个节点上，能突破你的单机内存限制。
# Pandas的拓展库 modin、dask、polars等，它们提供了类似pandas的数据类型和函数接口，但使用多进程、分布式等方式来处理大数据集。
# read_csv参数详解

# ***************************************************************

'''
header（表头）
参数header=None，即无表头
无参数header，即默认第一行是表头
多表头

【索引】
默认索引，即0，1，2，3...
单索引，参数index_col指定列索引号或列名
多索引，参数index_col指定列列表

【行列显示】
显示所有行和列
显示前N行
显示指定列
显示指定列和指定索引
对指定列进行显示与排序

【shuju1数据转换】
将 1.0 转换成 TRUE， 0.0 转换成 False (数据类型变成了object)
将 True 转换成 1.0， False 转换成 2.0
单列，将 NaN 转为 0 (object时，NaN 转换成 0,float64时，NaN 转换成 0.0)
所有列，将 NaN 转为 0(object时，NaN 转换成 0,float64时，NaN 转换成 0.0)

[修改]
将year列的值加100
将name列的值最后加上s
真假值转换 true_values false_values


'''

import pandas as pd
import numpy as np
import sys

print(pd.__version__)

# # 1, chunksize 分块读取
# # 优点：分块读取，用多少读取多少，占用内存小
# # 缺点：不建议在循环内部进行大量计算或内存密集型的操作，否则可能会消耗过多的内存或降低性能。
# # 每次读取10行数据
# 应用：可以将每个 chunk 写入不同的文件
# for chunk in pd.read_csv('https://www.gairuo.com/file/data/dataset/GDP-China.csv', chunksize=10):
#     print(chunk.head())

# # 2, pyspark
# from pyspark.sql import SparkSession
# # 2.1 创建一个 SparkSession 对象
# spark = SparkSession.builder.appName("Big Data Processing with PySpark").getOrCreate()
# df = spark.read.csv("GDP-China.csv", header=True, inferSchema=True)
#
# print(df.show(5))
# # +----+--------+------------------+-----------------------+-----------------------+-----------------------+---------+
# # |year|  income|total_output_value|industrial_added_value1|industrial_added_value2|industrial_added_value3|avg_value|
# # +----+--------+------------------+-----------------------+-----------------------+-----------------------+---------+
# # |2018|896915.6|          900309.5|                64734.0|               366000.9|               469574.6|    64644|
# # |2017|820099.5|          820754.3|                62099.5|               332742.7|               425912.1|    59201|
# # |2016|737074.0|          740060.8|                60139.2|               296547.7|               383373.9|    53680|
# # |2015|683390.5|          685992.9|                57774.6|               282040.3|               346178.0|    50028|
# # |2014|642097.6|          641280.6|                55626.3|               277571.8|               308082.5|    47005|
# # +----+--------+------------------+-----------------------+-----------------------+-----------------------+---------+
# # only showing top 5 rows
#
# # 新增一列year2，将year*10
# df_transformed = df.withColumn("year2", df["year"] * 10)
# print(df_transformed.show(5))
# # +----+--------+------------------+-----------------------+-----------------------+-----------------------+---------+-----+
# # |year|  income|total_output_value|industrial_added_value1|industrial_added_value2|industrial_added_value3|avg_value|year2|
# # +----+--------+------------------+-----------------------+-----------------------+-----------------------+---------+-----+
# # |2018|896915.6|          900309.5|                64734.0|               366000.9|               469574.6|    64644|20180|
# # |2017|820099.5|          820754.3|                62099.5|               332742.7|               425912.1|    59201|20170|
# # |2016|737074.0|          740060.8|                60139.2|               296547.7|               383373.9|    53680|20160|
# # |2015|683390.5|          685992.9|                57774.6|               282040.3|               346178.0|    50028|20150|
# # |2014|642097.6|          641280.6|                55626.3|               277571.8|               308082.5|    47005|20140|
# # +----+--------+------------------+-----------------------+-----------------------+-----------------------+---------+-----+
# # only showing top 5 rows
#
# # 2.2 将结果保存到新的 CSV 文件中
# # 注意：Spark 默认不会保存表头到 CSV，你可能需要手动处理这个问题
# df_transformed.write.csv("GDP-China_transformed", header=True)  # 保存到此目录GDP-China_transformed下
#
# # 2.3 停止 SparkSession
# spark.stop()


# 3,modin(报错)
# import modin.pandas as pd
# df = pd.read_csv('GDP-China.csv')
# print(df.head())

# # 4,dask
# import dask.dataframe as dd
# df = dd.read_csv('GDP-China.csv')
# print(df.head())

# 5,polars
# import polars as pl
# df = pl.read_csv('GDP-China.csv')
# print(df.head())
# print(df.count())



# todo 表头

# # 第一行表头
# # 注意：由于文档中有一行空白，所以整数型列变成float64，如year；字符型列变成object，如memo
# df = pd.read_csv('test.csv', header=0, encoding='gb2312')  # 中文编码使用gb2312
# # df = pd.read_csv('test.csv', encoding='gb2312') # 同上
# print(df)
# #      year    income  ...  industrial_added_value3  memo
# # 0  2018.0  896915.6  ...                 469574.6    测试
# # 1     NaN       NaN  ...                      NaN   NaN
# # 2  2015.0  683390.5  ...                 346178.0    44
# # 3  2014.0  642097.6  ...                 308082.5    腾讯
# # 4  2013.0  588141.2  ...                 277979.1    阿里
# # 5  2012.0  537329.0  ...                 244852.2    抖音
# # 6  2011.0  483392.8  ...                 216120.0    美团
# print(df['year'].dtypes)  # float64
# print(df['memo'].dtypes)  # object

#
# df = pd.read_csv('test2.csv', header=0)
# # df = pd.read_csv('test.csv') # 同上
# print(df)
# #    name  year  ...  industrial_added_value3  avg_value
# # 0  john  2018  ...                 469574.6      64644
# # 1  yoyo  2017  ...                 425912.1      59201
# # 2  titi  2016  ...                 383373.9      53680
# # 3  baba  2015  ...                 346178.0      50028
# # 4  mama  2014  ...                 308082.5      47005
# print(df['year'].dtypes)  # int64
#
# print("---"*33)

# # # 没有表头
# # # 注意：与header=0的区别，除了没有表头（序号0、1、2...表示）之外，数据也都是原值，且无法获取某列的数据类型，如df['year'].dtypes) 报错。
# df = pd.read_csv('test.csv', header=None, encoding='gb2312')
# print(df.head())
# #       0         1  ...                        5     6
# # 0  year    income  ...  industrial_added_value3  memo
# # 1  2018  896915.6  ...                 469574.6    测试
# # 2   NaN       NaN  ...                      NaN   NaN
# # 3  2015  683390.5  ...                   346178    44
# # 4  2014  642097.6  ...                 308082.5    腾讯
# # print(df['0'].dtypes)  # 报错



# # # 多层索引 multiIndex (多个标题)
# # 数据从第三行开始
# df = pd.read_csv('test.csv', header=[0, 1], encoding='gb2312')
# print(df)
# #      year    income  ... industrial_added_value3 memo
# #      2018  896915.6  ...                469574.6   测试
# # 0     NaN       NaN  ...                     NaN  NaN
# # 1  2015.0  683390.5  ...                346178.0   44
# # 2  2014.0  642097.6  ...                308082.5   腾讯
# # 3  2013.0  588141.2  ...                277979.1   阿里
# # 4  2012.0  537329.0  ...                244852.2   抖音
# # 5  2011.0  483392.8  ...                216120.0   美团

# # 数据从第5行开始（介于中间的行将被忽略掉，本例中的数据0，1,3行将被作为多级标题出现，第3行数据将被丢弃，dataframe的数据从第5行开始）
# df = pd.read_csv('test.csv', header=[0, 1, 3], encoding='gb2312')
# print(df)
# #    year    income  ... industrial_added_value3 memo
# #    2018  896915.6  ...                469574.6   测试
# #    2015  683390.5  ...                  346178   44
# # 0  2014  642097.6  ...                308082.5   腾讯
# # 1  2013  588141.2  ...                277979.1   阿里
# # 2  2012  537329.0  ...                244852.2   抖音
# # 3  2011  483392.8  ...                216120.0   美团


# # 指定列名 names
# df = pd.read_csv('test.csv', encoding='gb2312',names=['列1','列2'])
# print(df.head())
# #                                                                                                        列1    列2
# # year income   total_output_value industrial_added_value1 industrial_added_value2  industrial_added_value3  memo
# # 2018 896915.6 900309.5           64734                   366000.9                                469574.6    测试
# # NaN  NaN      NaN                NaN                     NaN                                          NaN   NaN
# # 2015 683390.5 NaN                57774.6                 282040.3                                  346178    44
# # 2014 642097.6 1                  55626.3                 277571.8                                308082.5    腾讯






# todo 索引列

# # # 默认索引，即0，1，2，3...
# # df = pd.read_csv('test.csv', encoding='gb2312')
# df = pd.read_csv('test.csv', index_col=False, encoding='gb2312')  # 同上
# print(df.head())
# #      year    income  ...  industrial_added_value3  memo
# # 0  2018.0  896915.6  ...                 469574.6    测试
# # 1     NaN       NaN  ...                      NaN   NaN
# # 2  2015.0  683390.5  ...                 346178.0    44
# # 3  2014.0  642097.6  ...                 308082.5    腾讯
# # 4  2013.0  588141.2  ...                 277979.1    阿里


# # # 单索引，参数index_col指定列索引号或列名
# df = pd.read_csv('test.csv', index_col=1, encoding='gb2312')
# # df = pd.read_csv('test.csv', index_col='income', encoding='gb2312')  # 同上
# print(df.head())
# #             year  total_output_value  ...  industrial_added_value3  memo
# # income                                ...
# # 896915.6  2018.0            900309.5  ...                 469574.6    测试
# # NaN          NaN                 NaN  ...                      NaN   NaN
# # 683390.5  2015.0                 NaN  ...                 346178.0    44
# # 642097.6  2014.0                 1.0  ...                 308082.5    腾讯
# # 588141.2  2013.0                 0.0  ...                 277979.1    阿里


# # # 多索引，参数index_col指定列列表
# df = pd.read_csv('test.csv', index_col=[0, 1], encoding='gb2312')
# # # df = pd.read_csv('test.csv', index_col=['income', 'year'], encoding='gb2312')  # 同上
# print(df.head())
# #                  total_output_value  ...  memo
# # year   income                        ...
# # 2018.0 896915.6            900309.5  ...    测试
# # NaN    NaN                      NaN  ...   NaN
# # 2015.0 683390.5                 NaN  ...    44
# # 2014.0 642097.6                 1.0  ...    腾讯
# # 2013.0 588141.2                 0.0  ...    阿里



# todo 行列显示

# 显示所有行和列
# pd.set_option('display.max_rows', None)  # 显示所有行
# pd.set_option('display.max_columns', None)  # 显示所有列
# df = pd.read_csv('test.csv', encoding='gb2312')
# print(df)


# # # 显示前N行
# # df = pd.read_csv('test.csv', nrows=4, encoding='gb2312')
# # print(df)
# # #      year    income  ...  industrial_added_value3  memo
# # # 0  2018.0  896915.6  ...                 469574.6    测试
# # # 1     NaN       NaN  ...                      NaN   NaN
# # # 2  2015.0  683390.5  ...                 346178.0    44
# # # 3  2014.0  642097.6  ...                 308082.5    腾讯
#
# df = pd.read_csv('test.csv', encoding='gb2312')
# print(df)
# #      year    income  ...  industrial_added_value3  memo
# # 0  2018.0  896915.6  ...                 469574.6    测试
# # 1     NaN       NaN  ...                      NaN   NaN
# # 2  2015.0  683390.5  ...                 346178.0    44
# # 3  2014.0  642097.6  ...                 308082.5    腾讯
# # 4  2013.0  588141.2  ...                 277979.1    阿里
# # 5  2012.0  537329.0  ...                 244852.2    抖音
# # 6  2011.0  483392.8  ...                 216120.0    美团
#
# # 跳过前N行
# # 注意表头
# # df = pd.read_csv('test.csv', skiprows=2, encoding='gb2312')
# df = pd.read_csv('test.csv', skiprows=range(2), encoding='gb2312')  # 同上
# print(df)
# #    Unnamed: 0  Unnamed: 1  Unnamed: 2  ...  Unnamed: 4  Unnamed: 5  Unnamed: 6
# # 0        2015    683390.5         NaN  ...    282040.3    346178.0          44
# # 1        2014    642097.6         1.0  ...    277571.8    308082.5          腾讯
# # 2        2013    588141.2         0.0  ...    261956.1    277979.1          阿里
# # 3        2012    537329.0         NaN  ...    244643.3    244852.2          抖音
# # 4        2011    483392.8         NaN  ...    227038.8    216120.0          美团
#
# # 跳过指定行，之后第一行数据为表头
# # df = pd.read_csv('test.csv', skiprows=[0, 2], encoding='gb2312')
# df = pd.read_csv('test.csv', skiprows=np.array([0, 2]), encoding='gb2312')  # 同上
# print(df)
# #    2018  896915.6  900309.5    64734  366000.9  469574.6  测试
# # 0  2015  683390.5       NaN  57774.6  282040.3  346178.0  44
# # 1  2014  642097.6       1.0  55626.3  277571.8  308082.5  腾讯
# # 2  2013  588141.2       0.0  53028.1  261956.1  277979.1  阿里
# # 3  2012  537329.0       NaN  49084.5  244643.3  244852.2  抖音
# # 4  2011  483392.8       NaN  44781.4  227038.8  216120.0  美团
#
# # 隔行跳过
# df = pd.read_csv('test.csv', skiprows=lambda x: x % 2 !=0, encoding='gb2312')
# print(df)
# #      year    income  ...  industrial_added_value3  memo
# # 0     NaN       NaN  ...                      NaN   NaN
# # 1  2014.0  642097.6  ...                 308082.5    腾讯
# # 2  2012.0  537329.0  ...                 244852.2    抖音

# # 显示指定列
# df = pd.read_csv('test.csv', usecols=[0, 1, 2], encoding='gb2312')
# # df = pd.read_csv('test.csv', usecols=['year', 'income', 'total_output_value'], encoding='gb2312') # 同上
# df = pd.read_csv('test.csv', usecols=[0, 1, 2],  encoding='gb2312').squeeze("columns")  # 同上

# print(df)
# #      year    income  total_output_value
# # 0  2018.0  896915.6            900309.5
# # 1     NaN       NaN                 NaN
# # 2  2015.0  683390.5                 NaN
# # 3  2014.0  642097.6                 1.0
# # 4  2013.0  588141.2                 0.0
# # 5  2012.0  537329.0                 NaN
# # 6  2011.0  483392.8                 NaN


# # 显示指定列和指定索引
# df = pd.read_csv('test.csv', usecols=[0, 1, 2], index_col=1, encoding='gb2312')
# print(df.head())
# #             year  total_output_value
# # income
# # 896915.6  2018.0            900309.5
# # NaN          NaN                 NaN
# # 683390.5  2015.0                 NaN
# # 642097.6  2014.0                 1.0
# # 588141.2  2013.0                 0.0


# # # 对指定列进行显示与排序
# df = pd.read_csv('test.csv', usecols=[0, 1, 2], encoding='gb2312')[['total_output_value', 'year', 'income']]
# print(df.head(8))
# #    total_output_value    year    income
# # 0            900309.5  2018.0  896915.6
# # 1                 NaN     NaN       NaN
# # 2                 NaN  2015.0  683390.5
# # 3                 1.0  2014.0  642097.6
# # 4                 0.0  2013.0  588141.2
# # 5                 NaN  2012.0  537329.0
# # 6                 NaN  2011.0  483392.8
# print(df['total_output_value'].dtypes)  # float64

# # 返回序列，如果是一列，返回Series
# df = pd.read_csv('test.csv', usecols=[0],  encoding='gb2312').squeeze("columns")
# print(df)
# # 0    2018.0
# # 1       NaN
# # 2    2015.0
# # 3    2014.0
# # 4    2013.0
# # 5    2012.0
# # 6    2011.0
# # Name: year, dtype: float64
# print(df[4])  # 2013.0

# # 返回序列，如果是多列，返回DataFrame
# df = pd.read_csv('test.csv', usecols=[0,2],  encoding='gb2312').squeeze("columns")
# print(df)
# #      year  total_output_value
# # 0  2018.0            900309.5
# # 1     NaN                 NaN
# # 2  2015.0                 NaN
# # 3  2014.0                 1.0
# # 4  2013.0                 0.0
# # 5  2012.0                 NaN
# # 6  2011.0                 NaN


# # 2.11 dtype(数据类型)
# # 所有数据均为此数据类型（报错，因为name是object）
# # df = pd.read_csv('test2.csv', dtype=np.float64, encoding='gb2312')
# # 指定字段类型
# df = pd.read_csv('test2.csv', dtype={'name':str, 'year':np.float64}, encoding='gb2312')
# # 依次指定（没成功？？？）
# # df = pd.read_csv('test2.csv', dtype=[str,float,float,float,float,float,float,float], encoding='gb2312')
# print(df)
# #    name    year  ...  industrial_added_value3  avg_value
# # 0  john  2018.0  ...                 469574.6      64644
# # 1  yoyo  2017.0  ...                 425912.1      59201
# # 2  titi  2016.0  ...                 383373.9      53680
# # 3  baba  2015.0  ...                 346178.0      50028
# # 4  mama  2014.0  ...                 308082.5      47005
# print(df['name'].dtypes)  # object
# print(df['year'].dtypes)  # float64




# todo 类型转换


# # # 将 1.0 转换成 TRUE， 0.0 转换成 FALSE
# # 注意：转换成布尔值后，数据类型变成了object
# df['total_output_value'] = df['total_output_value'].replace({1.0:True, 0.0:False})
# print(df.head(8))
# #   total_output_value    year    income
# # 0           900309.5  2018.0  896915.6
# # 1           820754.3  2017.0       NaN
# # 2           740060.8  2016.0       NaN
# # 3                NaN  2015.0  683390.5
# # 4               True  2014.0  642097.6
# # 5              False  2013.0  588141.2
# # 6                NaN  2012.0  537329.0
# # 7                NaN  2011.0  483392.8
# print(df['total_output_value'].dtypes)  # object

# # # 将 True 转换成 1.0， False 转换成 2.0
# df['total_output_value'] = df['total_output_value'].replace({True:1, False:2})
# print(df.head(8))
# #    total_output_value    year    income
# # 0            900309.5  2018.0  896915.6
# # 1            820754.3  2017.0       NaN
# # 2            740060.8  2016.0       NaN
# # 3                 NaN  2015.0  683390.5
# # 4                 1.0  2014.0  642097.6
# # 5                 2.0  2013.0  588141.2
# # 6                 NaN  2012.0  537329.0
# # 7                 NaN  2011.0  483392.8
# print(df['total_output_value'].dtypes)  # float64

# print("---"*33)
# # 将 NaN 转为 0
# # 注意：total_output_value是object时，NaN 转换成 0
# # 注意：total_output_value是float64时，NaN 转换成 0.0
# # 单列，将 NaN 转为 0
# df['total_output_value'] = df['total_output_value'].replace({np.nan:0})
# print(df.head(8))
# #   total_output_value    year    income
# # 0           900309.5  2018.0  896915.6
# # 1           820754.3  2017.0       NaN
# # 2           740060.8  2016.0       NaN
# # 3                  0  2015.0  683390.5
# # 4               True  2014.0  642097.6
# # 5              False  2013.0  588141.2
# # 6                  0  2012.0  537329.0
# # 7                  0  2011.0  483392.8

# # 所有列，将 NaN 转为 0
# df.fillna(0, inplace=True)
# print(df.head(8))
# #   total_output_value    year    income
# # 0           900309.5  2018.0  896915.6
# # 1           820754.3  2017.0       0.0
# # 2           740060.8  2016.0       0.0
# # 3                  0  2015.0  683390.5
# # 4               True  2014.0  642097.6
# # 5              False  2013.0  588141.2
# # 6                  0  2012.0  537329.0
# # 7                  0  2011.0  483392.8

# # 将 total_output_value 转为 int
# df['total_output_value'] = df['total_output_value'].astype(int)
# print(df.head(8))
# #    total_output_value    year    income
# # 0              900309  2018.0  896915.6
# # 1              820754  2017.0       0.0
# # 2              740060  2016.0       0.0
# # 3                   0  2015.0  683390.5
# # 4                   1  2014.0  642097.6
# # 5                   0  2013.0  588141.2
# # 6                   0  2012.0  537329.0
# # 7                   0  2011.0  483392.8


# todo 修改

# df = pd.read_csv('test.csv', usecols=[0,1,2])
# print(df.head())
# #      year    income  total_output_value
# # 0  2018.0  896915.6            900309.5
# # 1  2017.0       NaN            820754.3
# # 2  2016.0       NaN            740060.8
# # 3  2015.0  683390.5                 NaN
# # 4  2014.0  642097.6                 1.0
#
# # 将1 或1.0 改为 NaN
# df = pd.read_csv('test.csv', usecols=[0,1,2], na_values='1.0')
# print(df.head())
# #      year    income  total_output_value
# # 0  2018.0  896915.6            900309.5
# # 1  2017.0       NaN            820754.3
# # 2  2016.0       NaN            740060.8
# # 3  2015.0  683390.5                 NaN
# # 4  2014.0  642097.6                 NaN
#
# df = pd.read_csv('test.csv', usecols=[0,1,2], encoding='gb2312')
# print(df.head())

# df = pd.read_csv('test.csv', usecols=[0,1,2], na_values={4:2}, encoding='gb2312')
# print(df.head())

# print("---"*33)
#
# # 将year列的值加100
# df = pd.read_csv('test2.csv',converters={'year': lambda x: int(x)+100})
# print(df.head())
# #    name  year  ...  industrial_added_value3  avg_value
# # 0  john  2118  ...                 469574.6      64644
# # 1  yoyo  2117  ...                 425912.1      59201
# # 2  titi  2116  ...                 383373.9      53680
# # 3  baba  2115  ...                 346178.0      50028
# # 4  mama  2114  ...                 308082.5      47005
#
#
# # 将name列的值最后加上s
# def foo(p):
#     return p + 's'
# df = pd.read_csv('test2.csv',converters={'name': foo})
# # df = pd.read_csv('test2.csv',converters={0: foo}) # 同上，因为name的索引号是0
# print(df.head())
# #     name  year  ...  industrial_added_value3  avg_value
# # 0  johns  2018  ...                 469574.6      64644
# # 1  yoyos  2017  ...                 425912.1      59201
# # 2  titis  2016  ...                 383373.9      53680
# # 3  babas  2015  ...                 346178.0      50028
# # 4  mamas  2014  ...                 308082.5      47005
#
#
# # 真假值转换 true_values false_values
# from io import StringIO
# data= ('a,b,c\n1,yoyo,2\n3,No,4')
# df = pd.read_csv(StringIO(data),true_values=['yoyo'], false_values=['No'])
# print(df.head())
# #    a      b  c
# # 0  1   True  2
# # 1  3  False  4




df = pd.read_csv('test2.csv')
# print(df)


from PO.TimePO import *
Time_PO = TimePO()


title = "工作日志"
filePrefix = "abc"

pd.set_option('colheader_justify', 'center')  # 对其方式居中
html = '''<html><head><title>''' + str(title) + '''</title></head>
  <body><b><caption>''' + str(title) + '''_''' + str(
    Time_PO.getDate()) + '''</caption></b><br><br>{table}</body></html>'''
style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;border-collapse: collapse;border: 1px solid silver;}.mystyle td, 
th {padding: 5px;}.mystyle tr:nth-child(even) {background: #E0E0E0;}.mystyle tr:hover {background: silver;cursor:pointer;}</style>'''
rptNameDate = "report/" + str(filePrefix) + str(Time_PO.getDate()) + ".html"
with open(rptNameDate, 'w') as f:
    f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
    # f.write(html.format(table=df.to_html(classes="mystyle", col_space=50)))