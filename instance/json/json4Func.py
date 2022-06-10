# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: json库的4个方法 json.dumps(), json.loads(), json.dump() ,json.load()
# json.dumps()	将python对象编码成Json字符串（结果生成的时字符串）
# json.loads()	将Json字符串解码成python对象
# json.dump()	将python中的对象转化成json储存到文件 （结果生成一个fp的文件流和文件相关）
# json.load()	将文件中的json的格式转化成python对象提取出来

''' 语法：
# json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
obj:转化成json的对象。
skipkeys：默认值是False，如果dict的keys内的数据不是python的基本类型(str,unicode,int,long,float,bool,None)，设置为False时，就会报TypeError的错误。此时设置成True，则会跳过这类key 。
ensure_ascii=True：默认输出ASCLL码，如果把这个该成False,就可以输出中文。
check_circular：如果check_circular为false，则跳过对容器类型的循环引用检查，循环引用将导致溢出错误(或更糟的情况)。
allow_nan：如果allow_nan为假，则ValueError将序列化超出范围的浮点值(nan、inf、-inf)，严格遵守JSON规范，而不是使用JavaScript等价值(nan、Infinity、-Infinity)。
indent:参数根据数据格式缩进显示，读起来更加清晰。
separators:是分隔符的意思，参数意思分别为不同dict项之间的分隔符和dict项内key和value之间的分隔符，把：和，后面的空格都除去了。
default：default(obj)是一个函数，它应该返回一个可序列化的obj版本或引发类型错误。默认值只会引发类型错误。
sort_keys =True:是告诉编码器按照字典排序(a到z)输出。如果是字典类型的python对象，就把关键字按照字典排序。

def dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):
'''
# ********************************************************************************************************************

import json


print("1，json.dumps() 将Python对象编码成json格式的字符串（字典转字符串）".center(100, "-"))
dict1 = {'name': '你猜', 'age': 19, 'city':'四川'}
print(json.dumps(dict1))  # {"name": "\u4f60\u731c", "age": 19, "city": "\u56db\u5ddd"}
print(json.dumps(dict1, separators=(',', ':')))  # {"name":"\u4f60\u731c","age":19,"city":"\u56db\u5ddd"}  # 把：和，后面的空格都除去了
print(json.dumps(dict1, separators=(',', ':'), ensure_ascii=False))  # {"name":"你猜","age":19,"city":"四川"}
print(json.dumps(dict1, separators=(',', ':'), ensure_ascii=False, sort_keys=True))  # {"age":19,"city":"四川","name":"你猜"}
print(json.dumps(dict1, separators=(',', ':'), ensure_ascii=False, indent=1))
# {
#  "name":"你猜",
#  "age":19,
#  "city":"四川"
# }


print("2，json.loads() 将Json字符串解码成python对象（字符串转字典）".center(100, "-"))
str1 = json.dumps(dict1, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
print(json.loads(str1))  # {'age': 19, 'city': '四川', 'name': '你猜'}



print("3，json.dump() 将python中的对象转化成json储存到文件".center(100, "-"))
# 注意：python中的对象可以是str或dict，但文件里保存的是str字符串
json_str = {'age': 19, 'city': '四川', 'name': '你猜'}
# json.dump(json_str,  open('d:\\json1.txt', 'w', encoding='utf-8'))  # "{'age': 19, 'city': '\u56db\u5ddd', 'name': '\u4f60\u731c'}"
# json.dump(json_str, open('d:\\json1.txt', 'w'), ensure_ascii=False)  # {"age": 19, "city": "四川", "name": "你猜"}


print("3，json.load() 将文件中的json的格式转化成python对象提取出来".center(100, "-"))
json_str = open('d:\\json1.txt', 'r')
dict4 = json.load(json_str)
print(dict4)  # {'age': 19, 'city': '四川', 'name': '你猜'}
print(type(dict4))  # <class 'dict'>