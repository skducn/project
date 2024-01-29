# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-1-26
# Description: 利用 python 进行数据分析.pdf
# 1.USA.gov Data Archives  http://1usagov.measuredvoice.com/2013/
# *****************************************************************
# usagov_bitly_data2013-05-17-1368832207


import pandas as pd
import json

path = 'usagov_bitly_data2013-05-17-1368832207'
# print(open(path).readline())
# { "a": "Mozilla\/5.0 (Linux; U; Android 4.1.2; en-us; HTC_PN071 Build\/JZO54K) AppleWebKit\/534.30 (KHTML, like Gecko) Version\/4.0 Mobile Safari\/534.30",
# "c": "US",
# "nk": 0,
# "tz": "America\/Los_Angeles",
# "gr": "CA",
# "g": "15r91",
# "h": "10OBm3W",
# "l": "pontifier",
# "al": "en-US",
# "hh": "j.mp",
# "r": "direct",
# "u": "http:\/\/www.nsa.gov\/",
# "t": 1368832205,
# "hc": 1365701422,
# "cy": "Anaheim",
# "ll": [ 33.816101, -117.979401 ] }

# 在一个打开 的文件句柄上进行迭代即可获得一个由行组成的序列
records = [json.loads(line) for line in open(path)]
print(records[0]['tz'])  # America/Los_Angeles

time_zones = [rec['tz'] for rec in records if 'tz' in rec]
print(time_zones)  # ['America/Los_Angeles', '', 'America/Phoenix', 'America/Chicago', '',...]
print(time_zones[:10])  # ['America/Los_Angeles', '', 'America/Phoenix', 'America/Chicago', '', 'America/Indianapolis', 'America/Chicago', '', 'Australia/NSW', '']

from collections import defaultdict
from collections import Counter


def get_counts2(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] +=1
    return counts

# 统计时区出现的次数
counts = get_counts2(time_zones[:10])
print(counts)  # defaultdict(<class 'int'>, {'America/Los_Angeles': 1, '': 4, 'America/Phoenix': 1, 'America/Chicago': 2, 'America/Indianapolis': 1, 'Australia/NSW': 1})
print(counts['America/Chicago'])  # 2

counts = Counter(time_zones)
print(counts.most_common(5))  # [('America/New_York', 903), ('America/Chicago', 686), ('', 636), ('America/Los_Angeles', 421), ('America/Puerto_Rico', 184)]

frame = pd.DataFrame(records)
# print(frame)
print(frame['tz'][:5])
# [3959 rows x 18 columns]
# 0    America/Los_Angeles
# 1
# 2        America/Phoenix
# 3        America/Chicago
# 4
# Name: tz, dtype: object

# frame['tz']所返回的Series对象有一个value_counts 方法，该方法输出一个按值出现的次数进行排序的Series对象
# 等同于 counts.most_common(5)
tz_counts = frame['tz'].value_counts()
print(tz_counts[:5])
# Name: tz, dtype: object
# America/New_York       903
# America/Chicago        686
#                        636
# America/Los_Angeles    421
# America/Puerto_Rico    184
# Name: tz, dtype: int64

print("``````````````")
clean_tz = frame['tz'].fillna('missing')  # 替换缺失值（NA）
clean_tz[clean_tz == ''] = 'Unknow'   # 替换未知值（空字符串）
tz_counts = clean_tz.value_counts()
print(tz_counts[:5])
# ``````````````
# America/New_York       903
# America/Chicago        686
# Unknow                 636
# America/Los_Angeles    421
# America/Puerto_Rico    184
# Name: tz, dtype: int64

# # 要以pylab模式打开，否则这条代码没效果
# tz_counts[:5].plot(kind='barh', rot=0)



print(frame['a'][:10])
# 0    Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; H...
# 1    Mozilla/4.0 (compatible; MSIE 7.0; Windows NT ...
# 2    Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20...
# 3    Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; S...
# 4    Opera/9.80 (Android; Opera Mini/7.5.33286/29.3...
# 5    Mozilla/5.0 (compatible; MSIE 10.0; Windows NT...
# 6    Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) G...
# 7    Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_5 li...
# 8    Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like ...
# 9    Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKi...
# Name: a, dtype: object


from pandas import Series
results = Series([x.split()[0] for x in frame.a.dropna()])
print(results[:10])
# 0    Mozilla/5.0
# 1    Mozilla/4.0
# 2    Mozilla/5.0
# 3    Mozilla/5.0
# 4     Opera/9.80
# 5    Mozilla/5.0
# 6    Mozilla/5.0
# 7    Mozilla/5.0
# 8    Mozilla/5.0
# 9    Mozilla/5.0
# dtype: object

print(results.value_counts()[:5])
# Mozilla/5.0           3251
# Mozilla/4.0            322
# CakePHP                 38
# ShortLinkTranslate      36
# TVersity                30
# dtype: int64

print(frame.a.notnull())
# 0       True
# 1       True
# 2       True
# 3       True
# 4       True
#         ...
# 3954    True
# 3955    True
# 3956    True
# 3957    True
# 3958    True
# Name: a, Length: 3959, dtype: bool

import numpy as np
cframe = frame[frame['a'].notnull()]  # 去掉缺失的数据

operating_system = np.where(cframe['a'].str.contains('Opera'))
print(operating_system)
# (array([   4,  292,  371,  373,  427,  565,  690,  694, 1106, 1134, 1227,
#        1233, 1326, 1327, 1486, 1487, 1549, 2231, 2848, 2858, 2940, 2956,
#        3014, 3069, 3124, 3160, 3197, 3445, 3464, 3774]),)


# # 根据时区和新得到的操作系统列表对数据进行分 组了:
# by_tz_os = cframe.groupby(['tz', operating_system])
# agg_counts = by_tz_os.size().unstack().fillna(0)
# print(agg_counts[:10])
