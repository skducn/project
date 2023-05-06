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
import os, sys, platform, time
pd.set_option('display.width', None)

from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())

# '初始化数据'
folder_name = '放量涨幅'
file_name = today + '_' + folder_name + '.xlsx'
# 量比qrr
qrr = sys.argv[1]
# 涨跌幅chg
chg = sys.argv[2]
# qrr = 5
# chg = 8

# 获取实时行情数据
def get_stock_zh_a_spot_em():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # current_dir = os.getcwd()
    file_dir = '{}/{}'.format(current_dir, folder_name)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    file_dir_name = '{}/{}'.format(file_dir, file_name)
    if os.path.isfile(file_dir_name):
        data = pd.read_excel(file_dir_name, sheet_name='source')
    else:
        data = ak.stock_zh_a_spot_em()
        data.to_excel(file_dir_name, 'source', index=False)
        # data.to_excel(file_dir_name, 'source', encoding='gbk', index=False)
        # 注意：如果excel文件名包含中文，需要参数 encoding='GBK'，否则追加时会报错 File is not a ZIP file！
    return data, file_dir_name

data, file_dir_name = get_stock_zh_a_spot_em()

# 筛选条件
# 量比 > ？
data['是否放量'] = data['量比'].map(lambda x:'是' if x > int(qrr) else '否')
# 涨跌幅 < ？
data['是否上涨'] = data['涨跌幅'].map(lambda x:'是' if x < int(chg) and x > 0 else '否')
# 市盈率-动态 > 0
data['市盈率-动态正数'] = data['市盈率-动态'].map(lambda x:'是' if x > 0 else '否')
# 去掉科创板
data['是否科创'] = data['代码'].map(lambda x:'是' if int(x) > 680000 else '否')


# 符合条件输出，换手率降序
s_data = data.loc[(data['是否放量'] == '是') & (data['是否上涨'] == '是') & (data['市盈率-动态正数'] == '是') & (data['是否科创'] == '否'), :].copy()
s_data = s_data[['代码', '名称', '最新价', '涨跌幅', '量比', '换手率', '市盈率-动态']]
s_data.sort_values('换手率', inplace=True, ascending=False)
# print(s_data.sorted('量比',))

# 当前时分秒
current_time = time.strftime("%H%M%S")
with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
    s_data.to_excel(writer, sheet_name=current_time, index=False)

# pathFile = os.getcwd() + '/' + getDate + '_量比大' + str(qrr) + '_涨跌幅小' + str(chg) + '.csv'
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)



