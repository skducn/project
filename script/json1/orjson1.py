# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-6-10
# Description: 第三方JSON库, orjson
# orjson 支持3.7到3.10 所有版本64位的Python
# pip install orjson
# *****************************************************************

import orjson


print("1，序列化, 将Python对象序列化为JSON数据,结果bytes类型".center(100, "-"))
b = orjson.dumps({"a":1, "b":2})
print(type(b))  # <class 'bytes'>
print(b)  # b'{"a":1,"b":2}'

print("2，反序列化, 将JSON数据转换为Python对象，可以是str或bytes".center(100, "-"))
d = orjson.loads(b)
print(d)  # {'a': 1, 'b': 2}

print("3 参数 OPT_INDENT_2，结果添加2个空格的缩进美化效果".center(100, "-"))
print(orjson.dumps({"a":"b", "c":{"d":True},"e":[1,2]}).decode())  # {"a":"b","c":{"d":true},"e":[1,2]}
print(orjson.dumps({"a":"b", "c":{"d":True},"e":[1,2]}, option=orjson.OPT_INDENT_2).decode())
# {
#   "a": "b",
#   "c": {
#     "d": true
#   },
#   "e": [
#     1,
#     2
#   ]
# }

print("4 参数 OPT_OMIT_MICROSECONDS，可以将datatime,time转换结果后缀的毫秒部分省略掉".center(100, "-"))
from datetime import datetime
print(orjson.dumps({'now':datetime.now()})) # b'{"now":"2022-06-10T14:05:38.413225"}'
print(orjson.dumps({'now':datetime.now()}, option=orjson.OPT_OMIT_MICROSECONDS))  # b'{"now":"2022-06-10T14:06:13"}'

print("5 参数 OPT_NON_STR_KEYS，强制将非数值型键转换为字符型：".center(100, "-"))
print(orjson.dumps({1:"a", 2:"b"},option=orjson.OPT_NON_STR_KEYS)) # b'{"1":"a","2":"b"}'

print("6 参数 OPT_SERIALIZE_NUMPY，可以将包含numpy中数据结构对象的复杂对象，兼容性地转换为JSON中的数组".center(100, "-"))
import numpy as np
d_orjson3 = {
    'numpy-deme': np.random.randint(0,10,(3,5))
}
print(d_orjson3)
print(orjson.dumps(d_orjson3,option=orjson.OPT_SERIALIZE_NUMPY)) # b'{"numpy-deme":[[6,3,7,7,9],[3,8,5,6,8],[7,0,4,5,4]]}'


print("7 参数 OPT_SERIALIZE_UUID，对UUID对象进行转换".center(100, "-"))
import uuid
d_orjson6 = {'uuid_demo': uuid.uuid4()}
print(d_orjson6)  # {'uuid_demo': UUID('1c3e8135-171a-4776-965d-acdaceb1b558')}
print(orjson.dumps(d_orjson6))  # b'{"uuid_demo":"1c3e8135-171a-4776-965d-acdaceb1b558"}'
print(orjson.loads(orjson.dumps(d_orjson6)))  # {'uuid_demo':'1c3e8135-171a-4776-965d-acdaceb1b558'}

print("8 参数 OPT_SORT_KEYS，对键进行排序".center(100, "-"))
print(orjson.dumps({"b":1, "c":2, "a":3}, option = orjson.OPT_SORT_KEYS))  # b'{"a":3,"b":1,"c":2}'


print("9 使用|运算符来组合多个option参数".center(100, "-"))
d_orjson9 = {
    'c':np.random.randint(0,10,(2,2)),
    'd':np.random.randint(0,10,(2,2)),
    'a':np.random.randint(0,10,(2,2)),
}
print(orjson.dumps(d_orjson9, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SORT_KEYS))
# b'{"a":[[6,7],[2,2]],"c":[[2,2],[4,7]],"d":[[0,2],[9,6]]}'
# 分析：对key排序

print("10 针对dataclass、datetime添加自定义处理策略".center(100, "-"))
# 可以配合orjson.OPT_PASSTHROUGH_DATACLASS?，再通过对default参数传入自定义处理函数，来实现更为自由的数据转换逻辑，譬如下面简单的例子中，我们可以利用此特性进行原始数据的脱敏操作：

from dataclasses import dataclass

@dataclass
class User:
    id:str
    phone:int

def default(obj):
    if isinstance(obj,User):
        phone_str = str(obj.phone)
        return {
            'id': obj.id,
            'phone': f'{phone_str[:3]}XXXX{phone_str[-4:]}'
        }

    raise TypeError
d_orjson10 = {
    'user1':User(id=str(uuid.uuid4()), phone=13816109050)
}

print(orjson.dumps(d_orjson10,option=orjson.OPT_PASSTHROUGH_DATACLASS,default=default))
# b'{"user1":{"id":"222fa270-e54b-4fcc-8749-fa47d6be0976","phone":"138XXXX9050"}}'
x = orjson.loads(orjson.dumps(d_orjson10,option=orjson.OPT_PASSTHROUGH_DATACLASS,default=default))['user1']['phone']
print(x) # 138XXXX9050


print("11 参数 OPT_PASSTHROUGH_DATETIME，自定义default函数实现日期自定义格式化转换".center(100, "-"))
def default(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y%m%d')
    raise TypeError

print(orjson.dumps({'now': datetime.now()},option=orjson.OPT_PASSTHROUGH_DATETIME,default=default).decode())
# {"now":"20220610"}