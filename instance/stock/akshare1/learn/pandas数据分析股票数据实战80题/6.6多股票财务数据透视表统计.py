# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  6.6 数据处理与分析 - 6.6多股票财务数据透视表统计
# www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/5835909/106048134#taid=13742048517098629&vid=387702306337923316
# *****************************************************************

import pandas as pd
import numpy as np
import akshare as ak
import time
import os,sys
pd.set_option('display.width', None)
import time, platform, sys

file_name = '多股票财务数据透视表统计.xlsx'

d = ak.stock_financial_abstract(symbol='300310')
print(d)

# 6.6 将多个股票的财务数据进行拼接，如 ['300310', '300795']
data = pd.DataFrame()
l_stock = ['300310', '300795']
for stock in l_stock:
    print('{}财务数据获取中。。。'.format(stock))
    data1 = ak.stock_financial_abstract(symbol=stock)
    data1['股票名称'] = [stock]*data1.shape[0]
    # 如果总表为空就替换，否则拼接
    if data.shape[0] == 0:
        data = data1.copy()
    else:
        data = pd.concat([data, data1])
    time.sleep(1)
print(data)

# # 计算每只股票"净利润占比" = "净利润"/"资产总计"
# l_col = ['净利润', '资产总计']
# for col in l_col:
#     data[col].fillna(0, inplace=True)
#     data[col] = data[col].astype(str)
#     data[col] = data[col].map(lambda x: x.repalce(',', ''))
#     data[col] = data[col].map(lambda x: x.repalce('元', ''))
#     data[col] = data[col].astype(np.float64)
# data['净利润占比'] = data['净利润'] / data['资产总计']
# print(data)
