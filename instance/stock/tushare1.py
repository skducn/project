# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-06-15
# Description: http://tushare.org/
# pip3 install tushare
# *****************************************************************

import tushare as ts

# df = ts.get_hist_data('003026')
#直接保存
ts.set_token('894e80b70503f5cda0d86f75820c5871ff391cf7344e55931169bb2a')
pro = ts.pro_api()
df = pro.bak_daily('daily', ts_code='000625.SZ', start_date='20210101', end_date='20210615')

df.to_csv('c:/00062511111.csv')
