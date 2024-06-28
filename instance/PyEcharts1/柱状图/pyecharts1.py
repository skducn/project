# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-3-3
# Description: pyEcharts
# pip install pyecharts

# ta-lib 安装
# brew install ta-lib
# pip install ta-lib   //https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# 安装ta-lib报错 https://zhuanlan.zhihu.com/p/647474788
# https://github.com/cgohlke/talib-build/releases 下载安装whl
# ta-lib-0.4.0.jar # https://sourceforge.net/projects/ta-lib/files/latest/download

# pip3.9 install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# 首先用 YahooFinancials API 来下载若干外汇和加密货币的三年半历史数据，安装该 API 用一行代码 pip3.9 install yahoofinancials
# 起始日：2016-01-01
# 终止日：2019-05-13
# 四个外汇：欧元美元、美元日元、美元人民币，英镑美元
# 三个加密货币：比特币、以太币、瑞波币
# 参考：https://blog.csdn.net/weixin_42232219/article/details/90631442
#***************************************************************

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# matplotlib inline
from datetime import datetime
import talib as ta
# from pyecharts import Line, Kline, Pie, Grid, Overlap, Timeline, WordCloud


r_hex = '#dc2624'     # red,       RGB = 220,38,36
dt_hex = '#2b4750'    # dark teal, RGB = 43,71,80
tl_hex = '#45a0a2'    # teal,      RGB = 69,160,162
r1_hex = '#e87a59'    # red,       RGB = 232,122,89
tl1_hex = '#7dcaa9'   # teal,      RGB = 125,202,169
g_hex = '#649E7D'     # green,     RGB = 100,158,125
o_hex = '#dc8018'     # orange,    RGB = 220,128,24
tn_hex = '#C89F91'    # tan,       RGB = 200,159,145
g50_hex = '#6c6d6c'   # grey-50,   RGB = 108,109,108
bg_hex = '#4f6268'    # blue grey, RGB = 79,98,104
g25_hex = '#c7cccf'   # grey-25,   RGB = 199,204,207


# from yahoofinancials import YahooFinancials
# start_date = "2016-01-01"
# end_date = "2016-01-03"
#
# currencies = ["EURUSD=X","JPY=X","CNY=X","GBPUSD=X"]
# # cryptocurrencies = ["BTC-USD","ETH-USD","XRP-USD"]
#
# Fx_obj = YahooFinancials(currencies)
# # CRX_obj = YahooFinancials(cryptocurrencies)
#
# FX_daily = Fx_obj.get_historical_price_data(start_date,end_date,"daily")
# # CFX_daily = CRX_obj.get_historical_price_data(start_date,end_date,"daily")
#
# print(FX_daily)

from yahoofinancials import YahooFinancials
yahoo_financials = YahooFinancials('AAPL')
print(yahoo_financials.get_financial_stmts('annual', 'income'))