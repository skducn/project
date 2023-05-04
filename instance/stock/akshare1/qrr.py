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
import os, sys, platform
from time import strftime, localtime
year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
getDate = year + mon + day

pd.set_option('display.width', None)

# 量比qrr
# qrr = sys.argv[1]
# 涨跌幅chg
# chg = sys.argv[2]
qrr = 5
chg = 3

# 获取实时行情数据
data = ak.stock_zh_a_spot_em()

# 将实时行情数据保存到文件
def get_stock_zh_a_spot_em(file_name):
    if os.path.isfile(file_name):
        data = pd.read_csv(file_name, encoding='gbk')
    else:
        data = ak.stock_zh_a_spot_em()
        data.to_csv(file_name, encoding='gbk', index=False)
    return data
data = get_stock_zh_a_spot_em(getDate + '_实时行情数据.csv')


# 量比 > query1 的为是
data['是否放量'] = data['量比'].map(lambda x:'是' if x > int(qrr) else '否')
# 涨跌幅 < query2 的为是
data['是否上涨'] = data['涨跌幅'].map(lambda x:'是' if x < int(chg) and x > 0 else '否')
# 市盈率-动态
data['市盈率-动态正数'] = data['市盈率-动态'].map(lambda x:'是' if x > 0 else '否')
# 排除科创板
data['是否科创'] = data['代码'].map(lambda x:'是' if int(x) > 680000 else '否')


# 同时满足 量比 > query1 和 涨跌幅 < query2 股票存储到放量上涨股票清单.csv
s_data = data.loc[(data['是否放量'] == '是') & (data['是否上涨'] == '是') & (data['市盈率-动态正数'] == '是') & (data['是否科创'] == '否'), :].copy()
s_data = s_data[['代码', '名称', '最新价', '涨跌幅', '量比', '换手率', '市盈率-动态']]
s_data.sort_values('换手率', inplace=True, ascending=False)

# print(s_data.sorted('量比',))

pathFile = os.getcwd() + '/' + getDate + '_量比大' + str(qrr) + '_涨跌幅小' + str(chg) + '.csv'
s_data.to_csv(pathFile)
#
if platform.system() == "Darwin":
    os.system("open " + pathFile)



