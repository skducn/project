# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-3-20
# Description: 查询数据
# https://pandas.pydata.org/docs/user_guide/io.html
# ********************************************************************************************************************

import pandas as pd

# 设置界面显示的最大行列数据量
pd.options.display.max_columns = None  # 显示所有列数据
# pd.options.display.max_rows = None   # 显示所有行数据（谨慎，容易导致内存溢出）

df = pd.read_csv('sales_data.csv', usecols=range(1, 24))

# 查看数据量、数据指标
print(df.shape)  # (2823, 23)

# 查看数据尺寸
print(df.size)  # 64929

# 查看数据纬度
print(df.ndim)  # 2

# # 查看前N条数据
print(df.head(10))
# # 查看后N条数据
# print(df.tail(10))

# 查看指定条件的数据
print(df[df['SALES'] > 5000].shape)  # (549, 23)
# 多条件与过滤，销售大于5000，且州为CA的数据量
a = df[df['SALES'] > 5000]
print(a[a['STATE'] == 'CA'].shape)  # (80, 23)
# 等同于 print(df[df['SALES'] > 5000][df['STATE'] == 'CA'].shape)  # (80, 23)  //UserWarning: Boolean Series key will be reindexed to match DataFrame index.


# 查看指定列(区分大小写)
print(df[['SALES', 'ORDERDATE']].head())
#      SALES        ORDERDATE
# 0  2871.00   2/24/2003 0:00
# 1  2765.90    5/7/2003 0:00
# 2  3884.34    7/1/2003 0:00
# 3  3746.70   8/25/2003 0:00
# 4  5205.27  10/10/2003 0:00

# 查看指定行
# print(df[1:3])

# 查看指定行（指定索引）和列(指定名称)
print(df.loc[3:5, ['SALES', 'ORDERDATE']])  # 显示SALES和ORDERDATE列的第三四五行数据
#      SALES        ORDERDATE
# 3  3746.70   8/25/2003 0:00
# 4  5205.27  10/10/2003 0:00
# 5  3479.76  10/28/2003 0:00

# 查看指定行（指定索引）和列（指定索引）
print(df.iloc[3:5, :5])  # 显示前5列的第三四行数据
#     QUANTITYORDERED  PRICEEACH  ORDERLINENUMBER    SALES        ORDERDATE
# 3               45      83.26                6  3746.70   8/25/2003 0:00
# 4               49     100.00               14  5205.27  10/10/2003 0:00

# 查看指定行（指定索引）和列（指定索引）
print(df.iat[3, 4])  # 8/25/2003 0:00   //第三行第四列的值
# 等同于  print(df.loc[3, 'ORDERDATE'])


# 查看数据的详细信息和数据指标的类型
# object 包含字符串的复合型
print(df.dtypes)
# QUANTITYORDERED       int64
# PRICEEACH           float64
# ORDERLINENUMBER       int64
# SALES               float64
# ORDERDATE            object
# STATUS               object
# QTR_ID                int64
# MONTH_ID              int64
# YEAR_ID               int64
# PRODUCTLINE          object
# MSRP                  int64
# PRODUCTCODE          object
# CUSTOMERNAME         object
# PHONE                object
# ADDRESSLINE1         object
# ADDRESSLINE2         object
# CITY                 object
# STATE                object
# POSTALCODE           object
# COUNTRY              object
# TERRITORY            object
# CONTACTLASTNAME      object
# CONTACTFIRSTNAME     object
# dtype: object

# 统计不同类型数据指标的数量
from collections import Counter
print(Counter(df.dtypes.values))  # Counter({dtype('O'): 15, dtype('int64'): 6, dtype('float64'): 2})

# 查看数据的详细信息，指标类型统计，数据大小，内存占用信息
print(df.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2823 entries, 0 to 2822
# Data columns (total 23 columns):
#  #   Column            Non-Null Count  Dtype
# ---  ------            --------------  -----
#  0   QUANTITYORDERED   2823 non-null   int64
#  1   PRICEEACH         2823 non-null   float64
#  2   ORDERLINENUMBER   2823 non-null   int64
#  3   SALES             2823 non-null   float64
#  4   ORDERDATE         2823 non-null   object
#  5   STATUS            2823 non-null   object
#  6   QTR_ID            2823 non-null   int64
#  7   MONTH_ID          2823 non-null   int64
#  8   YEAR_ID           2823 non-null   int64
#  9   PRODUCTLINE       2823 non-null   object
#  10  MSRP              2823 non-null   int64
#  11  PRODUCTCODE       2823 non-null   object
#  12  CUSTOMERNAME      2823 non-null   object
#  13  PHONE             2823 non-null   object
#  14  ADDRESSLINE1      2823 non-null   object
#  15  ADDRESSLINE2      302 non-null    object
#  16  CITY              2823 non-null   object
#  17  STATE             1337 non-null   object
#  18  POSTALCODE        2747 non-null   object
#  19  COUNTRY           2823 non-null   object
#  20  TERRITORY         1749 non-null   object
#  21  CONTACTLASTNAME   2823 non-null   object
#  22  CONTACTFIRSTNAME  2823 non-null   object
# dtypes: float64(2), int64(6), object(15)
# memory usage: 507.4+ KB
# None
