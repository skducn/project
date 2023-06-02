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


# 生成目录结构
current_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = '{}/{}'.format(current_dir, folder_name)
if not os.path.isdir(file_dir):
    os.makedirs(file_dir)
file_dir_name = '{}/{}'.format(file_dir, file_name)

# apply
# data['流通股本占比'] = data.apply(lambda x: x['A股流通股本']/x['A股总股本'], axis='columns')
# data['板块行业'] = data.apply(lambda x: '{}{}'.format(x['板块'], x['所属行业']), axis='columns')
# data['行业平均流通股本'] = data.apply(lambda x: data.loc[data['所属行业'] == x['所属行业'], 'A股流通股本'].mean(), axis='columns')

# 格式化百分比，单位
def formatData():
    # print(list(data.loc[0:]))  # 标题
    # print(list(data.loc[0]))   # 第一条数据
    d_data = dict(zip(list(data.loc[0:]), list(data.loc[0])))
    for k, v in d_data.items():
        if '%' in str(v):
            data[k] = data[k].astype(str)
            data[k] = data[k].map(lambda x:x.replace('%', ''))
            data[k] = data[k].astype(np.float64)
        elif '亿' in str(v) or '万' in str(v):
            # print(k)
            data[k] = data[k].map(lambda x:float(x.replace('亿', ''))*10000 if '亿' in x else float(x.replace('万', '')))
            data[k] = data[k].astype(np.float64)
    return data
data = formatData()
if os.path.isfile(file_dir_name_jishi):
    with pd.ExcelWriter(file_dir_name_jishi, engine='openpyxl', mode='a') as writer:
        data.to_excel(writer, sheet_name=time.strftime("%H%M%S"), index=False)
else:
    with pd.ExcelWriter(file_dir_name_jishi, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=time.strftime("%H%M%S"), index=False)

# 1，格式化千分位
data['A股流通股本'] = data['A股流通股本'].map(lambda x: x.replace(',', ''))

# 2，格式化数据类型转换
data[['A股流通股本', 'A股总股本']] = data[['A股流通股本', 'A股总股本']].astype(np.float64)

# 3，公式计算，流通股本占比=A股流通股本/A股总股本
data['流通股本占比'] = data.apply(lambda x: x['A股流通股本']/x['A股总股本'], axis='columns')

# 4，按条件生成新列
data['是否放量'] = data['量比'].map(lambda x: '是' if x > int(qrr) else '否')

# 5，符合条件输出
s_data = data.loc[(data['是否放量'] == '是') & (data['是否上涨'] == '是'),:].copy()
# 6，输出指定的列
s_data = s_data[['代码', '名称', '最新价', '换手率', '市盈率-动态', '量比', '涨跌幅']]

# 7,列排序
s_data.sort_values('换手率', inplace=True, ascending=False)
s_data.sort_values(['最新公告日期', '每股净资产'], inplace=True, ascending=[False, True])  # 最新公告日期升序，每股净资产降序

# 8,保留表格里数据类型，如代码列数据是字符串00123，如果不使用converters则读取表格后得到的是123，但我们要获取是00123
original_data = pd.read_excel(file_dir_name, converters={'代码': str})