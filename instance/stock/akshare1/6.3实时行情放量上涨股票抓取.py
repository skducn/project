# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  6.3 数据处理与分析 实时行情放量上涨股票抓取
# www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# *****************************************************************

import pandas as pd
import numpy as np
import akshare as ak
import os
pd.set_option('display.width', None)

from time import strftime, localtime
year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
getDate = year + mon + day


# 6.3.1 获取实时行情数据
def get_stock_zh_a_spot_em(file_name):
    data = ak.stock_zh_a_spot_em()
    data.to_csv(file_name, encoding='gbk', index=False)
    print(data)
# get_stock_zh_a_spot_em('实时行情数据.csv')

# 6.3.2 通过map将涨跌幅列转百分比
data = ak.stock_zh_a_spot_em()
# data['涨跌幅(%)'] = data['涨跌幅'].map(lambda x:'{}%'.format(x))
# print(data['涨跌幅(%)'] )

# 6.3.3 添加标签'是否放量'，量比>10的为是
data['是否放量'] = data['量比'].map(lambda x:'是' if x>10 else '否')
print(data['是否放量'].value_counts())

# 6.3.4 添加标签'是否上涨'，涨跌幅>5%的为是
data['是否上涨'] = data['涨跌幅'].map(lambda x:'是' if x>5 else '否')
print(data['是否上涨'].value_counts())

# 6.3.5 筛选'是否放量' 和'是否上涨'都为是的股票存储到'yymmdd放量上涨股票清单.csv'
s_data = data.loc[(data['是否放量']=='是') & (data['是否上涨']=='是'),:].copy()
print(s_data)
s_data.to_csv(getDate + '_放量上涨股票清单.csv')





