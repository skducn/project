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
import os
pd.set_option('display.width', None)

stock_id = '300795'

def get_stock_financial_analysis_indicator(stock_id):
    current_dir = os.getcwd()
    file_name = '{}/{}.csv'.format(current_dir, stock_id)

    if not os.path.isfile(file_name):
        print('{}下载中...'.format(stock_id))
        data = ak.stock_financial_analysis_indicator(stock_id)
        data.to_csv(file_name, index=True, encoding='gbk')

# stock_list=['300058']
# for stock_id in stock_list:
#     get_stock_financial_analysis_indicator(stock_id)

# stock_individual_info_em_df = ak.stock_individual_info_em(symbol="300795")
# print(stock_individual_info_em_df)

# # 历史行情数据-不复权
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="300795", period="daily", start_date="20230420", end_date='20230428', adjust="")
# print(stock_zh_a_hist_df)
#
# # 历史行情数据-前复权
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="300795", period="daily", start_date="20230420", end_date='20230428', adjust="qfq")
# print(stock_zh_a_hist_df)
#
# # 历史行情数据-后复权
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="300795", period="daily", start_date="20230420", end_date='20230428', adjust="hfq")
# print(stock_zh_a_hist_df)

# 股东增减持
# stock_ggcg_em_df = ak.stock_ggcg_em(symbol="股东增持")
# # print(stock_ggcg_em_df)
# stock_ggcg_em_df.to_csv('股东增持.csv', index=True)

# 十大流通股东
# stock_gdfx_top_10_em_df = ak.stock_gdfx_top_10_em(symbol="sz002236", date="20230331")
# print(stock_gdfx_top_10_em_df)

# 股东户数
# stock_zh_a_gdhs_detail_em_df = ak.stock_zh_a_gdhs_detail_em(symbol="300795")
# print(stock_zh_a_gdhs_detail_em_df)

# 个股排行
# choice of {"北向", "沪股通", "深股通"}
# choice of {"今日排行", "3日排行", "5日排行", "10日排行", "月排行",
stock_em_hsgt_hold_stock_df = ak.stock_hsgt_hold_stock_em(market="北向", indicator="今日排行")
# stock_em_hsgt_hold_stock_df = ak.stock_hsgt_hold_stock_em(market="北向", indicator="5日排行")
print(stock_em_hsgt_hold_stock_df)
stock_em_hsgt_hold_stock_df.to_csv('今日北向个股排行.csv', index=True)

# 业绩报
# stock_yjbb_em_df = ak.stock_yjbb_em(date="20230331")
# print(stock_yjbb_em_df)
# stock_yjbb_em_df.to_csv('业绩报.csv', index=True)

