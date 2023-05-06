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
import time, platform, sys
from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())

# '初始化数据'
folder_name = '量比涨幅'
# 量比qrr
qrr = sys.argv[1]
# qrr = 5
# 涨跌幅chg
chg = sys.argv[2]
# chg = 4
# file_name = today + '_' + folder_name + '.xlsx'
file_name = today + '_量比大于' + str(qrr) + '_涨跌幅小于' + str(chg) + '.xlsx'
# pathFile = os.getcwd() + '/' + getDate + '_量比大于' + str(qrr) + '_涨跌幅小于' + str(chg) + '.xlsx'


# 生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)

# 6.3.1 获取实时行情数据
data = ak.stock_zh_a_spot_em()


# 6.3.2 通过map将涨跌幅列转百分比
# data = ak.stock_zh_a_spot_em()
# data['涨跌幅(%)'] = data['涨跌幅'].map(lambda x:'{}%'.format(x))
# print(data['涨跌幅(%)'] )

def getData():
    # 筛选条件
    # # 6.3.3 添加标签'是否放量'，量比>10的为是
    data['是否放量'] = data['量比'].map(lambda x:'是' if x > int(qrr) else '否')
    # 6.3.4 添加标签'是否上涨'，涨跌幅>5%的为是
    data['是否上涨'] = data['涨跌幅'].map(lambda x:'是' if x < int(chg) and x > 0 else '否')
    # 市盈率-动态 > 0
    data['市盈率-动态正数'] = data['市盈率-动态'].map(lambda x:'是' if x > 0 else '否')
    # 去掉科创板
    data['是否科创'] = data['代码'].map(lambda x:'是' if int(x) > 680000 else '否')

    # 6.3.5 筛选'是否放量' 和'是否上涨'都为是的股票存储到'yymmdd放量上涨股票清单.csv'
    # 符合条件输出，换手率降序
    s_data = data.loc[(data['是否放量'] == '是') & (data['是否上涨'] == '是') & (data['市盈率-动态正数'] == '是') & (data['是否科创'] == '否'), :].copy()
    s_data = s_data[['代码', '名称', '最新价', '换手率', '市盈率-动态', '量比', '涨跌幅']]
    s_data.sort_values('换手率', inplace=True, ascending=False)
    return s_data



# 生成数据
if os.path.isfile(file_dir_name):
    s_data = getData()
    # 当前时分秒
    current_time = time.strftime("%H%M%S")
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
        s_data.to_excel(writer, sheet_name=current_time, index=False)
else:
    s_data = getData()
    # 当前时分秒
    current_time = time.strftime("%H%M%S")
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
        s_data.to_excel(writer, sheet_name=current_time, index=False)


if platform.system() == "Darwin":
    os.system("open " + file_dir_name)