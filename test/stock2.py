# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-6-4
# Description: stock
# ********************************************************************************************************************


# import tushare as ts
# d = ts.get_tick_data('300658',date='2020-06-04')
# print(d)
# e = ts.get_hist_data('300658',start='2020-06-01',end='2020-06-03')
# print(d)

import tushare as ts
d = ts.get_hist_data('300658') #一次性获取全部日k线数据
print(d)
e = ts.get_hist_data('300658',start='2020-05-01',end='2020-06-04')
print(d)