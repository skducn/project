#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 使用元类进行类的自定义创建
#****************************************************************

class Meta(type):
    def __new__(cls, name, bases, attrs):
        attrs['class_name'] = name
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=Meta):
    pass
print(MyClass.class_name)