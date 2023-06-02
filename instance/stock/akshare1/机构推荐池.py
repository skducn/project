# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-9
# Description:
# https://www.akshare.xyz/data/stock/stock.html#id228
# *****************************************************************

import pandas as pd
import numpy as np
import akshare as ak
import os, sys, platform
pd.set_option('display.width', None)
from time import strftime, localtime
today = strftime("%Y", localtime()) + strftime("%m", localtime()) + strftime("%d", localtime())
import time

# 1，初始化数据
folder_name = '机构推荐池'
file_name = today + '_' + folder_name + '.xlsx'

# 2，生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)


# 3, 机构推荐池
# symbol="行业关注度"; choice of {'最新投资评级', '上调评级股票', '下调评级股票', '股票综合评级', '首次评级股票', '目标涨幅排名', '机构关注度', '行业关注度', '投资评级选股'}

data = ak.stock_institute_recommend_detail(symbol="301058")
# data = ak.stock_institute_recommend(symbol="投资评级选股")
print(data)
with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
    data.to_excel(writer, sheet_name='301058', index=False)

# def formatData():
#     # print(list(data.loc[0:]))  # 标题
#     # print(list(data.loc[0]))   # 第一条数据
#     d_data = dict(zip(list(data.loc[0:]), list(data.loc[0])))
#     for k, v in d_data.items():
#         if '%' in str(v):
#             data[k] = data[k].astype(str)
#             data[k] = data[k].map(lambda x:x.replace('%', ''))
#             data[k] = data[k].astype(np.float64)
#         elif '亿' in str(v) or '万' in str(v):
#             data[k] = data[k].map(lambda x:float(x.replace('亿', ''))*10000 if '亿' in x else float(x.replace('万', '')))
#             data[k] = data[k].astype(np.float64)
#     return data
# data = formatData()
# data.sort_values('净额', inplace=True, ascending=False)
#
# # 4，按条件生成新列
# data['股票代码'] = data['股票代码'].astype(np.int64)
# data['股票代码1'] = data['股票代码'].map(lambda x: '是' if x < 680000 else '否')
# data['涨跌幅1'] = data['涨跌幅'].map(lambda x: '是' if x < 3 and x>0 else '否')
# data['换手率1'] = data['换手率'].map(lambda x: '是' if x > 3 else '否')
# data['净额1'] = data['净额'].map(lambda x: '是' if x > 3000 else '否')
# # 5，符合条件输出
# data = data.loc[(data['涨跌幅1'] == '是') & (data['换手率1'] == '是') & (data['净额1'] == '是') & (data['股票代码1'] == '是'), ['股票代码', '股票简称', '最新价', '涨跌幅', '换手率', '净额']]
#
# if os.path.isfile(file_dir_name_jishi):
#     with pd.ExcelWriter(file_dir_name_jishi, engine='openpyxl', mode='a') as writer:
#         data.to_excel(writer, sheet_name=time.strftime("%H%M"), index=False)
# else:
#     with pd.ExcelWriter(file_dir_name_jishi, engine='openpyxl', mode='w') as writer:
#         data.to_excel(writer, sheet_name=time.strftime("%H%M"), index=False)

# 4，打开文档
if platform.system() == "Darwin":
    os.system("open " + file_dir_name)

# data['x'] = data['x'].apply(lambda x: if x['流入资金'])

# def getData(var1):
#
#     if os.path.isfile(file_dir_name):
#         data = pd.read_excel(file_dir_name, sheet_name=var1)
#     else:
#         # print('即时')
#         # data = ak.stock_fund_flow_individual(symbol='即时')
#         data = ak.stock_fund_flow_individual(symbol="即时")
#         with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
#             data.to_excel(writer, sheet_name='即时', index=False)
#
#         # print('3日排行')
#         data = ak.stock_fund_flow_individual(symbol='3日排行')
#         with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
#             data.to_excel(writer, sheet_name='3日排行', index=False)
#
#         # print('5日排行')
#         data = ak.stock_fund_flow_individual(symbol='5日排行')
#         with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
#             data.to_excel(writer, sheet_name='5日排行', index=False)
#
#         # print('10日排行')
#         data = ak.stock_fund_flow_individual(symbol='10日排行')
#         with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
#             data.to_excel(writer, sheet_name='10日排行', index=False)
#
#         # print('20日排行')
#         data = ak.stock_fund_flow_individual(symbol='20日排行')
#         with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
#             data.to_excel(writer, sheet_name='20日排行', index=False)
#     return data
#
# # # 3，生成数据
# # if os.path.isfile(file_dir_name):
# #     os.remove(file_dir_name)
# data = getData('即时')
#
# file_dir_name_today = '{}/{}'.format(file_dir, today + '_即时.xlsx')
# with pd.ExcelWriter(file_dir_name_today, engine='openpyxl', mode='w') as writer:
#     data.to_excel(writer, sheet_name='即时', index=False)




# 6.2.1 获取资金流入流出数据
# def get_stock_fund_flow_individual():
#     current_dir = os.getcwd()
#     file_dir = '{}/{}'.format(current_dir, folder_name)
#     if not os.path.isdir(file_dir):
#         os.makedirs(file_dir)
#     file_dir_name = '{}/{}'.format(file_dir, file_name)
#     if os.path.isfile(file_dir_name):
#         data = pd.read_excel(file_dir_name, sheet_name='source')
#     else:
#         # data = ak.stock_fund_flow_individual(symbol='即时')
#         data = ak.stock_fund_flow_individual(symbol='3日排行')
#         data.to_excel(file_dir_name, 'source', index=False)
#         # data.to_excel(file_dir_name, 'source', encoding='GBK', index=False)
#         # 注意：如果excel文件名包含中文，需要参数 encoding='GBK'，否则追加时会报错 File is not a ZIP file！
#     return data, file_dir_name
#
# data, file_dir_name = get_stock_fund_flow_individual()


# 6.2.2 清洗数据（格式化数据，去掉涨跌幅和换手率的百分比，将单位亿转换成万）
# def formatData():
#     # print(list(data.loc[0:]))  # 标题
#     # print(list(data.loc[0]))   # 第一条数据
#     d_data = dict(zip(list(data.loc[0:]), list(data.loc[0])))
#     for k, v in d_data.items():
#         if '%' in str(v):
#             data[k] = data[k].astype(str)
#             data[k] = data[k].map(lambda x:x.replace('%', ''))
#             data[k] = data[k].astype(np.float64)
#         elif '亿' in str(v) or '万' in str(v):
#             # print(k)
#             data[k] = data[k].map(lambda x:float(x.replace('亿', ''))*10000 if '亿' in x else float(x.replace('万', '')))
#             data[k] = data[k].astype(np.float64)
#     with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='w') as writer:
#         data.to_excel(writer, sheet_name='format', index=False)
#     dataFormat = pd.read_excel(file_dir_name, sheet_name='format')
#     return dataFormat
# dataFormat = formatData()




# 检查重复值
# 检查指定列重复值的数量
# print(dataFormat.duplicated(['最新价'], keep=False).sum())
# # 检查行记录重复值的数量
# print(dataFormat.duplicated(keep=False).sum())
# 删除指定列的重复数据，保留重复行的最后一行
# dataFormat.drop_duplicates(['最新价'],keep='last')
# 直接删除，保留一个副本
# dataFormat = dataFormat.drop_duplicates(['最新价'], inplace=False)
# sys.exit(0)

# # # 检查是否有空置
# print(dataFormat.isnull().sum())
# 序号      0
# 股票代码    0
# 股票简称    0
# 最新价     3
# 涨跌幅     2
# 换手率     0
# 流入资金    0
# 流出资金    0
# 净额      0
# 成交额     0
# dtype: int64

# 将'最新价'的空值替换成0
# dataFormat['最新价'].fillna(0, inplace=True)

# 获取标题
# print(list(dataFormat.loc[0:]))  # ['序号', '股票代码', '股票简称', '最新价', '涨跌幅', '换手率', '流入资金', '流出资金', '净额', '成交额']

# 获取记录中包含空值的行数据
# print(dataFormat.loc[dataFormat.isnull().values])
#     序号    股票代码  股票简称    最新价  涨跌幅    换手率      流入资金      流出资金       净额       成交额
# 11  12  300540  蜀道装备   0.00  NaN   9.14   13400.0    7336.1  6110.97   20800.0
# 13  14  300678  中科信息  61.67  NaN  21.31  117900.0  113000.0  4862.90  230800.0

# 获取记录中包含空值的索引值
# print(dataFormat.loc[dataFormat.isnull().values].index)  # Index([11, 13], dtype='int64')
# print(list(dataFormat.loc[dataFormat.isnull().values].index))  # [11, 13]
# print(list(dataFormat.loc[dataFormat.isnull().values].index)[0])  # 11


# 获取记录中包含空值的序号
# print(dataFormat.loc[dataFormat.isnull().values, '序号'])
# 11    12
# 13    14
# Name: 序号, dtype: int64
# print(list(dataFormat.loc[dataFormat.isnull().values, '序号']))  # [12, 14]
# print(list(dataFormat.loc[dataFormat.isnull().values, '序号'])[1])  # 14
# print(len(dataFormat.loc[dataFormat.isnull().values]))  # 2

# 删除包含缺失值的行记录
# dataFormat.dropna(inplace=True)
# print(dataFormat.head(20))
# dataFormat.sort_values('流入资金', inplace=True, ascending=False)
# print(dataFormat.head(20))

# print(dataFormat.isnull().sum())
# # print(dataFormat['最新价'].head(10))

# sheet_name不能修改已经存在的sheet，必须新的sheet
# with pd.ExcelWriter(file_dir_name, engine='openpyxl', mode='a') as writer:
#     dataFormat.to_excel(writer, sheet_name='formatFillna', index=False)


# # 6.2.3 统计全是流入资金，流出资金，净额，成交额 用字典形式返回。
# data_sum = data.sum()
# target_list = ['流入资金','流出资金','净额','成交额']
# value_list = list(data_sum[target_list])
# market_overall_dict = dict(zip(target_list, value_list))
# print(market_overall_dict)
#
# # 6.2.4 构建 净额占比 = 净额/成交额，找到 净额占比 最小值和最大值对应的股票，形成字典。
# data['净额占比'] = data['净额']/data['成交额']
# print(data.loc[data['净额占比'].idxmax(), '股票简称'])
# print(data.loc[data['净额占比'].idxmin(), '股票简称'])
#
# # 6.2.5 构建"是否st" 标签，有st的股票标记为是
# data['是否ST'] = data['股票简称'].map(lambda x:'是' if 'ST' in x else '否')
# print(data['是否ST'].value_counts())
#
# # 6.2.6 将 净额占比排名前50的数据，按换手率降序
# s_data = data.copy()
# s_data.sort_values('净额占比', inplace=True, ascending=False)
# s_data = s_data.head(5)
# s_data.sort_values('换手率', inplace=True, ascending=False)
# print(s_data)
#
#
# # 6.2.7 将 净额占比排名后50的数据，按涨跌幅降序
# s_data = data.copy()
# s_data.sort_values('净额占比', inplace=True, ascending=False)
# s_data = s_data.tail(5)
# s_data.sort_values('涨跌幅', inplace=True, ascending=False)
# print(s_data)