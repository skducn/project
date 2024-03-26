# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-3-20
# Description: 数据分析与可视化
# https://pandas.pydata.org/docs/user_guide/io.html
# ********************************************************************************************************************

import pandas as pd

df = pd.read_csv('sales_data.csv')


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

# print(df.head())


# todo 分类型数据统计
# 查看每个类别数据的数量
print(df['STATUS'].value_counts())
# STATUS
# Shipped       2617
# Cancelled       60
# Resolved        47
# On Hold         44
# In Process      41
# Disputed        14
# Name: count, dtype: int64

print(df['STATUS'].value_counts()['Disputed'])  # 14

# 查看每个类别数据的占比
print(df['STATUS'].value_counts(normalize=True))
# STATUS
# Shipped       0.927028
# Cancelled     0.021254
# Resolved      0.016649
# On Hold       0.015586
# In Process    0.014524
# Disputed      0.004959
# Name: proportion, dtype: float64

print("# ********************************************************************************************************************")

# todo 数值型类型统计
# 对数值型数据进行分箱处理
box = (pd.cut(df['SALES'], bins=[400, 500, 600, 700, 800, 900, 1000,
                                1100, 3400]))

print(box.value_counts(normalize=True))
# SALES
# (1100, 3400]    0.954926
# (1000, 1100]    0.012878
# (900, 1000]     0.012234
# (800, 900]      0.008371
# (700, 800]      0.005795
# (600, 700]      0.003220
# (500, 600]      0.001932
# (400, 500]      0.000644
# Name: proportion, dtype: float64
print(box.value_counts(normalize=True)[555])  # 0.0019317450096587251



print(pd.cut(range(10), bins=5))
# [(-0.009, 1.8], (-0.009, 1.8], (1.8, 3.6], (1.8, 3.6], (3.6, 5.4], (3.6, 5.4], (5.4, 7.2], (5.4, 7.2], (7.2, 9.0], (7.2, 9.0]]
# Categories (5, interval[float64, right]): [(-0.009, 1.8] < (1.8, 3.6] < (3.6, 5.4] < (5.4, 7.2] < (7.2, 9.0]]

print(pd.cut(range(10), bins=5, right=False))
# [[0.0, 1.8), [0.0, 1.8), [1.8, 3.6), [1.8, 3.6), [3.6, 5.4), [3.6, 5.4), [5.4, 7.2), [5.4, 7.2), [7.2, 9.009), [7.2, 9.009)]
# Categories (5, interval[float64, left]): [[0.0, 1.8) < [1.8, 3.6) < [3.6, 5.4) < [5.4, 7.2) < [7.2, 9.009)]

print(pd.cut(range(10), bins=[0, 2, 4, 6, 8, 10], right=False))
# [[0, 2), [0, 2), [2, 4), [2, 4), [4, 6), [4, 6), [6, 8), [6, 8), [8, 10), [8, 10)]
# Categories (5, interval[int64, left]): [[0, 2) < [2, 4) < [4, 6) < [6, 8) < [8, 10)]
print(pd.cut(range(10), bins=[0, 2, 4, 6, 8, 10], right=False)[0])  # [0, 2)

print(pd.cut(range(10), bins=[0, 2, 4, 6, 8, 10], right=True))
# [NaN, (0.0, 2.0], (0.0, 2.0], (2.0, 4.0], (2.0, 4.0], (4.0, 6.0], (4.0, 6.0], (6.0, 8.0], (6.0, 8.0], (8.0, 10.0]]
# Categories (5, interval[int64, right]): [(0, 2] < (2, 4] < (4, 6] < (6, 8] < (8, 10]]

