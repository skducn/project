# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 字典对象直接序列化为 JSON的{}  https://www.jb51.net/article/65101.htm
# dumps参数方法 https://docs.python.org/2/library/json.html#json.dumps
# Python语言特定的序列化模块是pickle
# ********************************************************************************************************************
import json

# Python的dict对象可以直接序列化为JSON的{}

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
# print(json.dumps(s))  报错，因为Student对象不是一个可序列化为JSON的对象，默认情况下，dumps()方法不知道如何将Student实例变为一个JSON的{}对象。
# 可选参数default就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为Student专门写一个转换函数，再把函数传进去即可，如 student2dict()
# 这样，Student实例首先被student2dict()函数转换成dict，然后再被顺利序列化为JSON。
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

# print(json.dumps(s, default=student2dict))  # {"name": "Bob", "age": 20, "score": 88}

# 更好的方法，写一个通用序列化json，无需以上转换函数。
# 因为通常class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量。
x = json.dumps(s, default=lambda obj: obj.__dict__)
print(x) # {"name": "Bob", "age": 20, "score": 88}


# 同样的道理，如果我们要把JSON反序列化为一个Student对象实例，loads()方法首先转换出一个dict对象，然后，我们传入的object_hook函数负责把dict转换为Student实例：
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=dict2student))  # <__main__.Student object at 0x000002B83AF54970>  //反序列化的Student实例对象




