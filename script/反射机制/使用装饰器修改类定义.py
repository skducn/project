#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 使用装饰器修改类定义
#****************************************************************

def add_attribute(attr_name, attr_value):
    def decorator(cls):
        setattr(cls, attr_name, attr_value)
        return cls
    return decorator

@add_attribute('my_attr', 'My Value')
class MyClass:
    pass

print(MyClass.my_attr)  # My Value
