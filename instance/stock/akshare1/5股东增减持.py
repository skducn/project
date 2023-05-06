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
import os, sys, platform
pd.set_option('display.width', None)
from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())

# 1, 初始化数据
folder_name = '5股东增减持'
file_name = today + '_' + folder_name + '.xlsx'

# 2, 生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)


def main():
    data = ak.stock_ggcg_em(symbol='股东增持')
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name='股东增持', index=False)

    data = ak.stock_ggcg_em(symbol='股东减持')
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
        data.to_excel(writer, sheet_name='股东减持', index=False)

# 3,生成数据(# 股东增减持)
if os.path.isfile(file_dir_name):
    os.remove(file_dir_name)
main()

# 4，打开文档
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)


