# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-06-15
# Description: tushare
# pip3.9 install tushare --upgrade
# 官网 http://tushare.org/
# 量化投资分析师（Quant）
# 对金融市场进行大数据分析的企业和个人
# 开发以证券为基础的金融类产品和解决方案的公司
# 正在学习利用python进行数据分析的人
# *****************************************************************

import tushare as ts
# print(ts.__version__)


# df = ts.get_hist_data('603439')
# #直接保存

ts.set_token('894e80b70503f5cda0d86f75820c5871ff391cf7344e55931169bb2a')
pro = ts.pro_api()


# df = pro.daily(ts_code='603439.SH', start_date='20220119', end_date='20220120')
# print(df)

df = pro.top_inst(trade_date='20220120')
print(df)


# df = ts.get_realtime_quotes('603439')
# print(df)
# df = ts.get_realtime_quotes('603439')[['name','price','pre_close','date','time']]
# print(df)


