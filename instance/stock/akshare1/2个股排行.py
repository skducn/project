# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description: 获取个股排行中 北向 沪股通 深股通 增持股票
# www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# 使用方法： ggph b|sh|sz
# *****************************************************************

import pandas as pd
import akshare as ak
import os, sys, platform
pd.set_option('display.width', None)
from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())

# 1，参数化
# varAddress = '沪股通'
varAddress = sys.argv[1]
if varAddress == 'b':varAddress = '北向'
if varAddress == 'sh':varAddress = '沪股通'
if varAddress == 'sz':varAddress = '深股通'

# 2，初始化数据
folder_name = '2个股排行'
file_name = today + '_' + varAddress + '.xlsx'

# 3, 生成目录结构
# 个股排行
def get_stock_hsgt_hold_stock_em():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = '{}/{}/{}'.format(current_dir, folder_name, today)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    file_dir_name = '{}/{}'.format(file_dir, file_name)
    if os.path.isfile(file_dir_name):
        data = pd.read_excel(file_dir_name, sheet_name=None)
        l_sheetName = list(data)
        l_all = ['今日排行', "3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"]
        l_data = [x for x in l_all if x not in l_sheetName]
        for i in range(len(l_data)):
                data = ak.stock_hsgt_hold_stock_em(market=varAddress, indicator=l_data[i])
                with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
                    data.to_excel(writer, sheet_name=l_data[i], index=False)
    else:
        data = ak.stock_hsgt_hold_stock_em(market=varAddress, indicator='今日排行')
        data.to_excel(file_dir_name, '今日排行', index=False)
        l_data = ["3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"]
        for i in range(len(l_data)):
            data = ak.stock_hsgt_hold_stock_em(market=varAddress, indicator=l_data[i])
            with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
                data.to_excel(writer, sheet_name=l_data[i], index=False)
        # data.to_excel(file_dir_name, folder_name, encoding='gbk', index=False)
        # 注意：如果excel文件名包含中文，需要参数 encoding='GBK'，否则追加时会报错 File is not a ZIP file！
    return file_dir_name
file_dir_name = get_stock_hsgt_hold_stock_em()

# 4，打开文档
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)
