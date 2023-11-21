# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-6-10
# Description: orjson 序列化
# orjson 支持3.7到3.10 所有版本64位的Python
# pip install orjson
# 可以将datetime、date和time实例序列化为RFC 3339格式，例如:"2022-06-12T00:00:00+00:00"
# 序列化numpy.ndarray实例的速度比其他库快4-12倍，但使用的内存更少，约为其他库的1/3左右
# 输出速度是标准库的10到20倍
# 序列化的结果是bytes类型，而不是str
# 序列化str时，不会将unicode转义为ASCII
# 序列化float的速度是其他库的10倍，反序列化的速度是其他库的两倍,不会损失精度。当序列化NaN,Infinity,-Infinity时，会返回null。
# 可以直接序列化str、int、list和dict的子类
# 不提供load( )和dump( )方法，在原生JSON库中，load( )方法可以把json格式的文件转换成python对象
# 功能丰富的高性能 Python JSON 库 https://weibo.com/ttarticle/p/show?id=2309634846250649583640
# *****************************************************************

import orjson,sys,json

print(orjson.dumps([float('NaN'), float('Infinity'), float('-Infinity')]))  # b'[null,null,null]'
str = json.dumps([float('NaN'), float('Infinity'), float('-Infinity')])
print(str)  # [NaN, Infinity, -Infinity]

sys.exit(0)

print("1，序列化, 将Python对象序列化为JSON数据,结果bytes类型".center(100, "-"))
b = orjson.dumps({"a":1, "b":2})
print(type(b))  # <类与实例 'bytes'>
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
print(orjson.dumps({1:"a", 2:3},option=orjson.OPT_NON_STR_KEYS))  # b'{"1":"a","2":3}'
b = (orjson.dumps({1:"a", 2:3},option=orjson.OPT_NON_STR_KEYS))
d = orjson.loads(b)  # {'1': 'a', '2': 3}
print(d)

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