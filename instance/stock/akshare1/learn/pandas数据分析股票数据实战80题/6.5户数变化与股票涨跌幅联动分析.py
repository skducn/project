# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  6.4 数据处理与分析 - 户数变化与股票涨跌幅联动分析
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

file_name = '户数变化与股票涨跌幅联动分析.xlsx'

# 6.5.1 获取数据
def getData():
    if os.path.isfile(file_name):
        data = pd.read_excel(file_name, sheet_name='source')
    else:
        # data = ak.stock_zh_a_gdhs(symbol="20230330")
        data = ak.stock_zh_a_gdhs(symbol="最新")
        # data = ak.stock_zh_a_gdhs(symbol="每个季度末")
        with pd.ExcelWriter(file_name, engine='openpyxl', mode='w') as writer:
            data.to_excel(writer, sheet_name='最新', index=False)
    return data
# data = getData()
# print(data)

def updateData():
    if os.path.isfile(file_name):
        os.remove(file_name)
    return getData()
data = updateData()
print(data)

# data['股东户数-上次', '股东户数-增减'] = data['股东户数-上次', '股东户数-增减'].astype(np.int64)
data['户数变化率'] = data['股东户数-增减'] / data['股东户数-上次']

# 将"户数变化率"等频率分成8组，统计每组"区间涨跌幅"平均值
# cut：按照数值进行分割，等间隔
# qcut：按照数据分布进行分割，等频率
data['户数变化率分箱'] = pd.qcut(data['户数变化率'], 8, labels=np.arange(1, 9))
# print(data['户数变化率分箱'])
# sys.exit(0)
data['区间涨跌幅'].fillna(value=0, inplace=True)
data['区间涨跌幅'] = data['区间涨跌幅'].astype(np.float64)

print(data.groupby('户数变化率分箱')[['区间涨跌幅', '户数变化率']].mean())
print(data.pivot_table(index='户数变化率分箱', values=['区间涨跌幅', '户数变化率'], aggfunc='mean'))
#              区间涨跌幅     户数变化率
# 户数变化率分箱
# 1        15.194276 -0.222320
# 2         6.765393 -0.086002
# 3         3.520860 -0.046278
# 4         1.482626 -0.022580
# 5         1.504070 -0.005303
# 6         2.076762  0.019250
# 7         7.073165  0.075365
# 8        11.307596       NaN

if platform.system() == "Darwin":
    os.system("open " + file_name)