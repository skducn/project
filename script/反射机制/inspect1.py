#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 内置的inspect模块来获取函数的签名
#****************************************************************

import inspect


# getmembers：获取对象的所有成员。
class Test:
    def method(self):
        pass

t = Test()
for member in inspect.getmembers(t):
    print(member)
# ('__class__', <class '__main__.Test'>)
# ('__delattr__', <method-wrapper '__delattr__' of Test object at 0x7fb52826fd30>)
# ('__dict__', {})
# ('__dir__', <built-in method __dir__ of Test object at 0x7fb52826fd30>)
# ('__doc__', None)
# ('__eq__', <method-wrapper '__eq__' of Test object at 0x7fb52826fd30>)
# ('__format__', <built-in method __format__ of Test object at 0x7fb52826fd30>)
# ('__ge__', <method-wrapper '__ge__' of Test object at 0x7fb52826fd30>)
# ('__getattribute__', <method-wrapper '__getattribute__' of Test object at 0x7fb52826fd30>)
# ('__gt__', <method-wrapper '__gt__' of Test object at 0x7fb52826fd30>)
# ('__hash__', <method-wrapper '__hash__' of Test object at 0x7fb52826fd30>)
# ('__init__', <method-wrapper '__init__' of Test object at 0x7fb52826fd30>)
# ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x7fb528523020>)
# ('__le__', <method-wrapper '__le__' of Test object at 0x7fb52826fd30>)
# ('__lt__', <method-wrapper '__lt__' of Test object at 0x7fb52826fd30>)
# ('__module__', '__main__')
# ('__ne__', <method-wrapper '__ne__' of Test object at 0x7fb52826fd30>)
# ('__new__', <built-in method __new__ of type object at 0x1034442f8>)
# ('__reduce__', <built-in method __reduce__ of Test object at 0x7fb52826fd30>)
# ('__reduce_ex__', <built-in method __reduce_ex__ of Test object at 0x7fb52826fd30>)
# ('__repr__', <method-wrapper '__repr__' of Test object at 0x7fb52826fd30>)
# ('__setattr__', <method-wrapper '__setattr__' of Test object at 0x7fb52826fd30>)
# ('__sizeof__', <built-in method __sizeof__ of Test object at 0x7fb52826fd30>)
# ('__str__', <method-wrapper '__str__' of Test object at 0x7fb52826fd30>)
# ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x7fb528523020>)
# ('__weakref__', None)
# ('method', <bound method Test.method of <__main__.Test object at 0x7fb52826fd30>>)


# todo ismodule: 检查对象是否是模块。
import os
print(inspect.ismodule(os))  # True


# todo isclass: 检查对象是否是类。
import inspect
class Test:
    pass
print(inspect.isclass(Test))  # True
print(inspect.isclass(inspect.isclass))  # False


# todo ismethod: 检查对象是否是方法。
class Test:
    def method(self):
        pass
t = Test()
print(inspect.ismethod(t.method))  # True



# todo isfunction: 检查对象是否是函数。
def func():
    pass
print(inspect.isfunction(func))  # True



# todo stack: 获取当前的调用栈。
def func():
    print(inspect.stack())
    print(inspect.stack()[0])
    print(inspect.stack()[0][1])  # /Users/linghuchong/Downloads/51/Python/project/script/反射机制/inspect1.py
    print(inspect.stack()[1])
func()


# todo getsource: 获取对象的源码。
def func():
    pass
source = inspect.getsource(func)
print(source)
# def func():
#     pass


# todo getfile: 获取对象所在的文件路径。
import os,redis
file_path = inspect.getfile(os)
print(file_path)  # /Users/linghuchong/miniconda3/envs/py308/lib/python3.8/os.py
file_path = inspect.getfile(redis)
print(file_path)  # /Users/linghuchong/miniconda3/envs/py308/lib/python3.8/site-packages/redis/__init__.py


# todo currentframe: 获取当前的帧。
frame = inspect.currentframe()
print(frame)  # <frame at 0x7fdc080e3a40, file '/Users/linghuchong/Downloads/51/Python/project/script/反射机制/inspect1.py', line 105, code <module>>
