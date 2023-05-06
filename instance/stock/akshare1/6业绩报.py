# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# 使用方法： yjb
# *****************************************************************

import pandas as pd
import akshare as ak
import os, sys, platform
pd.set_option('display.width', None)
from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())


# 1，初始化数据
folder_name = '6业绩报'
file_name = today + '_业绩报.xlsx'  # 20120321_业绩报.xlsx

# 3, 生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)

# 4, 获取业绩报
def main():
    data = ak.stock_yjbb_em(date="20230331")
    # 过滤每股收益 < 0
    data['是否每股收益'] = data['每股收益'].map(lambda x: '正' if x > 0 else '负')
    # 过滤科创板、B股
    data['是否科创'] = data['股票代码'].map(lambda x: '是' if int(x) > 620000 else '否')

    # 符合条件输出，换手率降序
    s_data = data.loc[(data['是否每股收益'] == '正') & (data['是否科创'] == '否'),:].copy()
    s_data.sort_values(['最新公告日期', '每股净资产'], inplace=True, ascending=[False, False])
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
        s_data.to_excel(writer, sheet_name='20230331业绩报', index=False)


# 5,生成数据
if os.path.isfile(file_dir_name):
    os.remove(file_dir_name)
main()

# 6，打开文档
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)