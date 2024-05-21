# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2024-5-21
# Description: pandas 读取
# PySpark，它是Spark的python api接口。
# PySpark处理大数据的好处是它是一个分布式计算机系统，可以将数据和计算分布到多个节点上，能突破你的单机内存限制。
# Pandas的拓展库 modin、dask、polars等，它们提供了类似pandas的数据类型和函数接口，但使用多进程、分布式等方式来处理大数据集。
# ***************************************************************

'''
1, 使用chunksize参数分块读取CSV文件
2, pyspark


'''

import pandas as pd


# # 1, 使用chunksize参数分块读取CSV文件
# # 优点：chunking分块读取，用多少读取多少，占用内存小
# # 缺点：不要在循环内部进行大量计算或内存密集型的操作，否则可能会消耗过多的内存或降低性能。
# chunksize = 10
# # 每次读取csv中10行
# for chunk in pd.read_csv('https://www.gairuo.com/file/data/dataset/GDP-China.csv', chunksize=chunksize):
#     print(chunk.head())
#     # 处理每个 chunk，例如，你可以将每个 chunk 写入不同的文件


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

