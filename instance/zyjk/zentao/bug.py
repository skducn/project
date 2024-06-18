# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-6-11
# Description: bug统计
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import pandas as pd

df = pd.read_csv('123.csv', encoding='ISO-8859-1')
# print(df.head())

import chardet

# # 假设file_path是你要读取的文件路径
# with open('123.csv', 'rb') as f:
#     data = f.read()
#     encoding = chardet.detect(data)['encoding']
#     print(encoding)  # ISO-8859-1
#
# with open('123.csv', 'r', encoding=encoding) as f:
#     content = f.read()
#     print(content)

# a = df.groupby(['product', df.resolvedBy.isin(['liuxia'])]).count()
# print(a)

d={'yangwenqing':'杨文庆','fanbingchuan':'范冰川','wangxu':'王旭','zhangtao1':'章涛','fanyi':'樊易','sunzhuangzhuang':'孙壮壮',
   'jiangweijian':'江伟健','dingxianhui':'丁先辉','yuanlixuan':'袁立宣','sunwenbo':'孙文博','caoyang':'曹阳',

   'renyangyin':'任杨寅','miqinglin':'米庆林','wangshuaishuai':'王帅帅','quhanlin':'曲翰林','tangkunchao':'唐坤超','huangchuanjun':'黄传军',
   'yangkuang':'杨框','zhaoyangzhou':'赵炀周','liucong':'刘聪','fengzhenglong':'冯正龙','qinpengfei':'覃鹏飞','wumin':'吴敏',
   'liyunfei':'李云飞','zhengdongsheng':'郑东升','maxinjie':'马鑫洁','wangshuai':'王帅','sunmin':'孙敏','zhaoxingyu':'赵星宇'}

p = {'29': '智赢CRM',
     '40': 'OA智能办公系统',
     '48': '妇幼保健院实施产品',
     '53': '电子健康档案数据管理平台产品',
     '56': '区域平台应用',
     '59': '区域HIS',
     '61':'区域公共卫生管理系统',
     '62':'社区健康管理中心系统',
     '65': '智赢健康俱乐部'}

def x(id):
    for k, v in d.items():
        data1 = df.where(df['product'] == id).where(df['assignedTo'] == k).sort_values(by=['id']).count()[0]
        data2 = df.where(df['product'] == id).where(df['resolvedBy'] == k).sort_values(by=['id']).count()[0]
        if data1 > 0 or data2 > 0 :
            data = data1 + data2
            print(id, p[str(id)], v, data)
        # print("--------------")

# for i in range(100):
#     x(i)
    #

