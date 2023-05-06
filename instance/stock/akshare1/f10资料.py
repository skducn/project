# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# 使用方法： zl 300795
# *****************************************************************

import pandas as pd
import akshare as ak
import os, platform, sys
pd.set_option('display.width', None)

# stock_id = '300795'
stock_id = sys.argv[1]  # 300795

# 通过股票简称找到股票代码？？未做
# stock_id = '四川黄金'
# if stock_id.isnumeric() == False:
# # 获取沪股票
# sh = ak.stock_info_sh_name_code(symbol="主板A股")
# # 获取深股票
# sz = ak.stock_info_sz_name_code(indicator="A股列表")


# '初始化数据'
folder_name = 'F10资料'
# 个股信息查询接口，获取股票简称
data = ak.stock_individual_info_em(symbol=stock_id)
d_data = dict(zip(list(data['item']), list(data['value'])))
# print(d_data['股票简称'])
file_name = d_data['股票简称'] + '_' + stock_id + '.xlsx'



# 生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)



def getF10():
    print('{}({})下载中...'.format(d_data['股票简称'], stock_id))

    # 1,个股信息查询
    data = ak.stock_individual_info_em(symbol=stock_id)
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name='个股信息查询', index=False)

    # 2,财务指标
    data = ak.stock_financial_analysis_indicator(symbol=stock_id)
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
        data.to_excel(writer, sheet_name='财务指标', index=False)

    # 3,十大流通股东
    if int(stock_id) < 400000 :
        s_data = ak.stock_gdfx_top_10_em(symbol='sz' + stock_id, date="20230331")
    else:
        s_data = ak.stock_gdfx_top_10_em(symbol='sh' + stock_id, date="20230331")
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
        s_data.to_excel(writer, sheet_name='十大流通股东', index=False)

    # 4,股东户数
    data = ak.stock_zh_a_gdhs_detail_em(symbol=stock_id)
    with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
        data.to_excel(writer, sheet_name='股东户数', index=False)

    if platform.system() == "Darwin":
        os.system("open " + file_dir_name)

# 生成数据
if os.path.isfile(file_dir_name):
    os.remove(file_dir_name)
    getF10()
else:
    getF10()