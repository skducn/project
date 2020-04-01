# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2019-1-16
# Description: 使用json模块操作文件 common/io/json1.py
#****************************************************************

import json

# json 文件中存储的数据结构为 列表 或 字典。

# json.dump(list,f_obj) 用来存储数据到json文件中
# 则number.json文件中的内容的格式与python中一样，为列表[1, 2, 3, 4, 5, 6]
numbers = [1, 2, 3, 4, 5, 6]
with open('number.json', 'w') as f_obj:
    json.dump(numbers, f_obj)

# json.load(f_obj) 用来从json文件读取数据到内存中
with open('number.json', 'r') as f_obj:
    numbers = json.load(f_obj)
print(numbers)  # 则numbers为列表[1, 2, 3, 4, 5, 6]
