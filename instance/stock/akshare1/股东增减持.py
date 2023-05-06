# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# *****************************************************************

import pandas as pd
import akshare as ak
import os,platform
pd.set_option('display.width', None)

# '初始化数据'
folder_name = '股东增减持'
file_name = folder_name + '.xlsx'

# 股东增减持
def get_stock_ggcg_em(var):
    current_dir = os.getcwd()
    file_dir = '{}/{}'.format(current_dir, folder_name)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    file_dir_name = '{}/{}'.format(file_dir, file_name)
    if os.path.isfile(file_dir_name):
        data = pd.read_excel(file_dir_name, sheet_name=var)
    else:
        data = ak.stock_ggcg_em(symbol=var)
        data.to_excel(file_dir_name, folder_name, index=False)
        # data.to_excel(file_dir_name, folder_name, encoding='gbk', index=False)
        # 注意：如果excel文件名包含中文，需要参数 encoding='GBK'，否则追加时会报错 File is not a ZIP file！
    return file_dir_name

file_dir_name = get_stock_ggcg_em('全部')
# file_dir_name = get_stock_ggcg_em('股东增持')
# get_stock_ggcg_em('股东减持')


if platform.system() == "Darwin":
    os.system("open " + file_dir_name)


