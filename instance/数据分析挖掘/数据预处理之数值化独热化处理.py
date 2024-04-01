# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-3-20
# Description: 数据分析与可视化
# https://pandas.pydata.org/docs/user_guide/io.html
# ********************************************************************************************************************

import pandas as pd
import numpy as np

df = pd.read_csv('sales_data.csv')


# todo 查看数据的详细信息，指标类型统计，数据大小，内存占用信息
# print(df.info())
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

# print(df.dtypes.index)
# Index(['ORDERNUMBER', 'QUANTITYORDERED', 'PRICEEACH', 'ORDERLINENUMBER',
#        'SALES', 'ORDERDATE', 'STATUS', 'QTR_ID', 'MONTH_ID', 'YEAR_ID',
#        'PRODUCTLINE', 'MSRP', 'PRODUCTCODE', 'CUSTOMERNAME', 'PHONE',
#        'ADDRESSLINE1', 'ADDRESSLINE2', 'CITY', 'STATE', 'POSTALCODE',
#        'COUNTRY', 'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME'],
#       dtype='object')

# print(df.dtypes)
# ORDERNUMBER           int64
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

# # todo 某一列是否为空
# print(df['ADDRESSLINE2'].isnull())
#
# # todo 某一列值的统计
# print(df['ADDRESSLINE2'].value_counts())

print(df['ORDERDATE'].isnull().values)
# print(np.unique(df['ADDRESSLINE2']))

# # todo 将字符串类型的数字转化为浮点型
# df['POSTALCODE'] = pd.to_numeric(df['POSTALCODE'], errors='coerce')
# print(df.info())

# # 查看字符串类型数据的具体数据类别
df_dtypes = df.dtypes
for col in df_dtypes.index:
    if df_dtypes[col] == 'object':
        print('*' * 50)
        print(col + ":")
        print(len(np.unique(df[col].astype(str))))
        print((np.unique(df[col].astype(str))))

print(df.describe().T)
