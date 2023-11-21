# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: Pickle
# Pickle 是Python的内置模块，用于将Python对象序列化为二进制数据。可以处理几乎所有Python对象，但仅适用于Python。
# 使用Pickle进行序列化与反序列化
# ********************************************************************************************************************

import pickle

data = {'name': "Carol", 'age': 35}

# 将对象序列化为二进制数据
with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)

# 将二进制数据反序列化为对象
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)  # {'name': 'Carol', 'age': 35}

