# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: json 文件处理四个函数 json.dumps(), json.loads(), json.dump() ,json.load()
# ********************************************************************************************************************

import json

# 1,json.dumps()和json.loads()是json格式处理函数（json是字符串）
# json.dumps()函数是将一个Python数据类型列表进行json格式的编码（字典 转 字符串）
# json.loads()函数是将json格式数据转换为字典（字符串 转 字典）
dict1 = {"age": "12"}
json2str = json.dumps(dict1)
print("dict1的类型：" + repr(type(dict1)))
print("json2str的类型：" + str(type(json2str)))
str1 = '{"age": "12"}'
json2dict = json.loads(str1)
print("str1的类型：" + str(type(str1)))
print("json2dict的类型：" + str(type(json2dict)))


# 2,json.dump()和json.load() 读写json文件函数
# json.dump()函数的使用，将json信息写进文件
json_info = "{'age': '12'}"
file = open('d:\\json1.txt', 'w', encoding='utf-8')
json.dump(json_info, file)

# json.load()函数的使用，将读取json信息
file = open('d:\\json1.txt', 'r', encoding='utf-8')
info = json.load(file)
print(info)