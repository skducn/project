# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-5-2
# Description: # StringIO在内存中读写字符串
# https://blog.csdn.net/weixin_42133116/article/details/134535449
# *****************************************************************
'''
从内存中读取字符串转化为df

'''
from io import StringIO
import pandas as pd

# 创建StringIO对象
s = StringIO()

# 向对象写入内容
s.write("jinhao")

# 将对象指针移动到开始位置
s.seek(0)

# 读取字符串
c = s.read()
print(c)  # jinhao

# 获取对象的长度
p = s.tell()
print(p)  # 6

# 关闭对象
s.close()


# 从内存中读取字符串转化为df
data=('col1,col2,col3\n''a,b,1\n''c,d,3')
df = pd.read_csv(StringIO(data))
print(df)
#   col1 col2  col3
# 0    a    b     1
# 1    c    d     3

df = pd.read_csv(StringIO(data), dtype=object)
print(df)
#   col1 col2 col3
# 0    a    b    1
# 1    c    d    3
