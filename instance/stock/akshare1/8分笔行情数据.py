# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:
# 接口: stock_zt_pool_em
# 目标地址: http://quote.eastmoney.com/ztb/detail#type=ztgc
# 描述: 东方财富网-行情中心-涨停板行情-涨停股池
# conda activate py310
# pip install aksare
# https://www.akshare.xyz/data/stock/stock.html#id352
#     https://gu.qq.com/sz300494/gp/detail
# *****************************************************************

import pandas as pd
import numpy as np
import akshare as ak
import os, sys, platform
pd.set_option('display.width', None)
from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())
import time

# 1，初始化数据
folder_name = '8分笔行情数据'
# varDate = '20230515'
file_name = today + '.xlsx'
# file_name = '20230515.xlsx'

# # 2，生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)

# 3, 获取涨停板数据
# data = ak.stock_bid_ask_em(symbol="300751")
# print(data)

data = ak.stock_zh_a_tick_tx_js(symbol="sz300751")
print(data)
# test = data.apply(lambda x: x['成交量'] if data['性质'] == '卖盘' else None, axis=0)
#
# print(test)


# data= pd.read_excel(file_dir_name)

# print(data['成交量'].map(lambda x: np.sum))
# def func(x):
#     if data['性质'] == '卖盘':

# x = (data[['成交量']].apply(np.sum, axis=0).values[0])
# def func(x):
#     return x.apply(lambda x: x if data['性质'] == '卖盘' else 0).sum()
# print(x)

# print(data[['成交量']].apply(func, axis=1))

print('外盘= ' + str(data.loc[data['性质'] =='卖盘', '成交量'].sum()))
print('内盘= ' + str(data.loc[data['性质'] =='买盘', '成交量'].sum()))
print('中性盘= ' + str(data.loc[data['性质'] =='中性盘', '成交量'].sum()))
# print(data.loc[data['性质'] =='卖盘', data['成交量']])



def condition(x):
    s = 0.00
    if x == '卖盘':
        # data['成交量'].astype(np.int)
        # print(type(data['成交量']))
        # print((data['成交量']))
        print(data['成交量'].to_list())
        # s = (data['成交量'].to_list())
        # s += data['成交量']
    return s
# data.apply(lambda x: x['成交量'] if data['性质'] == '卖盘' else None, axis=1)
# data['性质'].apply(condition)
# print(a)
# data['行业平均流通股本'] = data.apply(lambda x: data.loc[data['性质'] == x['卖盘'], '性质'].sum(), axis='columns')


if os.path.isfile(file_dir_name):
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        data.to_excel(writer, sheet_name=today, index=False)
else:
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=today, index=False)

# 4，打开文档
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)
