# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-6-25
# Description: 公卫 清洗数据，实例 a_upload
# *****************************************************************
import numpy as np
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")
engine = Sqlserver_PO.getEngine_pymssql()
df = pd.read_sql(text('SELECT * FROM a_upload'), con=engine.connect())
# print(df)


# todo 将空值填充为零1
df.replace('', '零1', inplace=True)

# todo 将o_value列的缺失值填充为 vanilla
df.replace({'o_value':{np.nan:'vanilla'}}, inplace=True)

# todo 将缺失值填充为零
df.fillna('零', inplace=True)

df.to_sql('a_upload2', con=engine, if_exists='replace', index=False)
