# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  6.4 数据处理与分析 - 股票列表数据加工
# www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/5835909/106048134#taid=13742048517098629&vid=387702306337923316
# *****************************************************************

import pandas as pd
import numpy as np
import akshare as ak
import os,sys
pd.set_option('display.width', None)
import time, platform, sys

file_name = '股票列表数据加工.xlsx'

# 6.4.1 获取数据
def getData():
    if os.path.isfile(file_name):
        data = pd.read_excel(file_name, sheet_name='source')
    else:
        data = ak.stock_info_sz_name_code()
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='w') as writer:
            data.to_excel(writer, sheet_name='source', index=False)
    return data

# 3，生成数据
if os.path.isfile(file_name):
    os.remove(file_name)

# 6.4.2 计算 'A股流通股本/A股总股本'结算生成新的列 "流通股本占比'
data = getData()
# print(data)
data['A股流通股本'] = data['A股流通股本'].map(lambda x: x.replace(',', ''))
data['A股总股本'] = data['A股总股本'].map(lambda x: x.replace(',', ''))
data[['A股流通股本', 'A股总股本']] = data[['A股流通股本', 'A股总股本']].astype(np.float64)
data['流通股本占比'] = data.apply(lambda x: x['A股流通股本']/x['A股总股本'], axis='columns')
with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
    data.to_excel(writer, sheet_name='流通股本占比', index=False)

# 6.4.3 拼接字段，将 板块和所属行业拼接在一起，生成新列"板块行业"
data['板块行业'] = data.apply(lambda x: '{}{}'.format(x['板块'], x['所属行业']), axis='columns')
with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
    data.to_excel(writer, sheet_name='板块行业', index=False)

data['行业平均流通股本'] = data.apply(lambda x: data.loc[data['所属行业'] == x['所属行业'], 'A股流通股本'].mean(), axis='columns')
print(data)

def my_func(x):
    if x['所属行业'] =='J 金融业':
        return min(x['流通股本占比']*1.5, 1)
    elif x['所属行业'] =='C 制造业':
        return max(x['流通股本占比']*0.5, 0)
    elif x['所属行业'] =='K 房地产':
        return 0
    else:
        return x['流通股本占比']
data['行业调整流通股本占比'] = data.apply(lambda x:my_func(x), axis='columns')
print(data)



if platform.system() == "Darwin":
    os.system("open " + file_name)