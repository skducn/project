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
# 序列化str时，不会将unicode转义为ASCII，只处理UTF-8格式的字符串，其他格式字符串会报错，如UTF-16
# 序列化float的速度是其他库的10倍，反序列化的速度是其他库的两倍,不会损失精度。当序列化NaN,Infinity,-Infinity时，会返回null。
# 可以直接序列化str、int、list和dict的子类
# 不提供load( )和dump( )方法，在原生JSON库中，load( )方法可以把json格式的文件转换成python对象
# 功能丰富的高性能 Python JSON 库 https://weibo.com/ttarticle/p/show?id=2309634846250649583640
# 库	耗时(s)
# orjson	0.78
# ujson	1.85
# simplejson	2.84
# json	2.21
# *****************************************************************

import orjson, sys, json, uuid
import numpy as np
from datetime import datetime

# todo 序列化 字典
b = orjson.dumps({"a": 1, "b": 2})
print(b)  # b'{"a":1,"b":2}'
print(b.decode())  # {"a":1,"b":2}
# todo 反序列化 字典
print(orjson.loads(b))  # {'a': 1, 'b': 2}


# todo 序列化 浮点数
print(orjson.dumps([float('NaN'), float('Infinity'), float('-Infinity')]))  # b'[null,null,null]'
str = json.dumps([float('NaN'), float('Infinity'), float('-Infinity')])
print(str)  # [NaN, Infinity, -Infinity]


# todo 序列化 整数（当值超过53-bit时会产生JSONEncodeError）
print(orjson.dumps(12345678901234567890))  # b'12345678901234567890'


# todo 序列化 字符串
# print(orjson.dumps("\ud800"))  # TypeError: str is not valid UTF-8: surrogates not allowed
print(orjson.dumps("金浩"))  # b'"\xe9\x87\x91\xe6\xb5\xa9"'


# todo 序列化 numpy（option=orjson.OPT_SERIALIZE_NUMPY）
print("将复杂数据对象转为字节".center(100, "-"))
d_np_dict = {'numpy-deme': np.random.randint(0,10,(3,5))}
print(d_np_dict)
# {'numpy-deme': array([[0, 3, 8, 1, 1],
#        [7, 0, 4, 8, 8],
#        [8, 5, 0, 8, 0]])}
print(orjson.dumps(d_np_dict, option=orjson.OPT_SERIALIZE_NUMPY))  # b'{"numpy-deme":[[6,3,7,7,9],[3,8,5,6,8],[7,0,4,5,4]]}'


# todo 序列化 UUID (OPT_SERIALIZE_UUID) 实例序列化为RFC 4122格式。
d_uuid = {'uuid_demo': uuid.uuid4()}
print(d_uuid)  # {'uuid_demo': UUID('1c3e8135-171a-4776-965d-acdaceb1b558')}
print(orjson.dumps(d_uuid))  # b'{"uuid_demo":"1c3e8135-171a-4776-965d-acdaceb1b558"}'
print(orjson.loads(orjson.dumps(d_uuid)))  # {'uuid_demo':'1c3e8135-171a-4776-965d-acdaceb1b558'}



# todo default 参数
import orjson, decimal
def default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
res = orjson.dumps(decimal.Decimal("0.0842389659712649442845"), default=default)
print(res)  # b'0.08423896597126494'



# todo option 参数
# 1 参数 OPT_APPEND_NEWLINE，结果添加换行符
print(orjson.dumps([], option=orjson.OPT_APPEND_NEWLINE))  # b'[]\n'


# 2 参数 OPT_OMIT_MICROSECONDS，可以设置datatime,time的实例的序列化结果没有微妙。
print(orjson.dumps({'now':datetime.now()}))  # b'{"now":"2022-06-10T14:05:38.413225"}'
print(orjson.dumps({'now':datetime.now()}, option=orjson.OPT_OMIT_MICROSECONDS))  # b'{"now":"2022-06-10T14:06:13"}'

# 3 参数 OPT_NON_STR_KEYS，将key（数值型）键转换为字符型".center(100, "-"))
print(orjson.dumps({1: "a", 2: 3}, option=orjson.OPT_NON_STR_KEYS))  # b'{"1":"a","2":3}'
b = (orjson.dumps({1: "a", 2: 3}, option=orjson.OPT_NON_STR_KEYS))
print(orjson.loads(b))  # {'1': 'a', '2': 3}

# 4 参数 OPT_INDENT_2，结果添加2个空格的缩进美化效果"
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

# 5 参数 OPT_SORT_KEYS，对键进行排序
print(orjson.dumps({"b":1, "c":2, "a":3}, option = orjson.OPT_SORT_KEYS))  # b'{"a":3,"b":1,"c":2}'

# 6 使用|运算符来组合多个option参数
d_orjson9 = {
    'c':np.random.randint(0,10,(2,2)),
    'd':np.random.randint(0,10,(2,2)),
    'a':np.random.randint(0,10,(2,2)),
}
print(orjson.dumps(d_orjson9, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SORT_KEYS))  # b'{"a":[[6,7],[2,2]],"c":[[2,2],[4,7]],"d":[[0,2],[9,6]]}'


sys.exit(0)

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