# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  www.akshare.xyz
# conda activate py310
# pip install aksare
# https://www.cnblogs.com/hider/p/15494513.html?ivk_sa=1024320u
# 在机器学习中，经常会对数据进行分箱处理操作，即将一段连续的值切分为若干段，每一段的值当成一个分类。
# 这个将连续值转换成离散值的过程，就是分箱处理。

# Pandas 包中的 cut 和 qcut 都可以实现分箱操作，区别在于：
# cut：按照数值进行分割，等间隔
# qcut：按照数据分布进行分割，等频率
# *****************************************************************

import pandas as pd
import numpy as np

# ages = np.array([1,5,10,40,36,12,58,62,77,89,100,18,20,25,30,32])

# 平分为5个区间
# print(pd.cut(ages, 5))

# print(pd.cut(ages, 5).value_counts())
# (0.901, 20.8]    6
# (20.8, 40.6]     5
# (40.6, 60.4]     1
# (60.4, 80.2]     2
# (80.2, 100.0]    2
# Name: count, dtype: int64

# 平分指定labels
# print(pd.cut(ages, 5, labels=['婴儿', '青年', '中年', '壮年', '老年']))
# ['婴儿', '婴儿', '婴儿', '青年', '青年', ..., '婴儿', '婴儿', '青年', '青年', '青年']
# Length: 16
# Categories (5, object): ['婴儿' < '青年' < '中年' < '壮年' < '老年']


# pd.qcut 实现按数据的数量进行分割，尽量保证每个分组里变量的个数相同。
df = pd.DataFrame([x**2 for x in range(11)], columns=['number'])
# print(df)

# 按照数值由小到大 将数据分成4份
df['cut_group'] = pd.cut(df['number'], 4)
print(df)


# 分成四组 并且让每组变量的数量相同
df['qcut_group'] = pd.qcut(df['number'], 4)
print(df)

print(df['qcut_group'].value_counts()
)