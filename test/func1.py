# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-31
# Description   : __init__，__new__，__call__
# https://www.jb51.net/article/49375.htm

# 对象生命周期的基础是创建、初始化和销毁。

# *****************************************************************
# 1.__new__(cls, *args, **kwargs)  创建对象时调用，返回当前对象的一个实例;注意：这里的第一个参数是cls即class本身
# 2.__init__(self, *args, **kwargs) 创建完对象后调用，对当前对象的实例的一些初始化，无返回值,即在调用__new__之后，根据返回的实例初始化；注意，这里的第一个参数是self即对象本身
# 3.__call__(self,  *args, **kwargs) 如果类实现了这个方法，相当于把这个类型的对象当作函数来使用，相当于 重载了括号运算符

class A(object):

    def __new__(cls, *args, **kwargs):
        print("new")
        return super(A, cls).__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        print("init")
        super(A, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('call')


a = A()
# new
# init
print(a())
# call
# None



class Person(object):
    """Silly Person"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return '<Person: %s(%s)>' % (self.name, self.age)

if __name__ == '__main__':
    piglei = Person('piglei', 24)
    print(piglei) # <Person: piglei(24)>




class PositiveInteger(int):
    def __new__(cls, value):
        return super(PositiveInteger, cls).__new__(cls, abs(value))

i = PositiveInteger(-3)
print(i)  # 3


class Singleton(object):
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
obj1 = Singleton()
obj2 = Singleton()

obj1.attr1 = 'value1'
print(obj1.attr1, obj2.attr1)  # value1 value1
print(obj1 is obj2)


# class Foo():
#     c = 1
#     def __init__(self,name):
#         self.name = name
#
#     def __getattr__(self, item):
#         return(item)
#
#     def sing(self):
#         print("sing")
#
# foo = Foo("safly")
# print(foo.__dict__)
# print(foo.a)


# class Foo():
#     c = 1
#     def __init__(self,name):
#         self.name = name
#
#     def __getattr__(self, item):
#         return("__getattr__")
#
#
#     def __getattribute__(self, item):
#         return("__getattribute__")
#
#
#     def sing(self):
#         print("sing")
#
# foo = Foo("safly")
# print(foo.__dict__)
# print(foo.a)


# class Foo():
#     def __init__(self,name):
#         self.name = name
#
#     def __getattr__(self, item):
#         print("__getattr__", item)
#
#     def __getattribute__(self, item):
#         print("__getattribute__",item)
#         raise AttributeError()
#
# foo = Foo("safly")
# foo.a

# try:
#     s = None
#     if s is None:
#         print("s 是空对象")
#         raise NameError  # 如果引发NameError异常，后面的代码将不能执行,如 print("111111")
#     print("111111")  # 这句不会执行，但是后面的except还是会走到
# except NameError:
#     print("空对象没有长度")

# s = None
# if s is None:
#     raise Exception("Invalid level!", s) # 触发异常后，后面的代码就不会再执行
# print('is here?')  # 如果不使用try..except，不会执行到这里




# class Networkerror(RuntimeError):
#     def __init__(self, arg):
#         self.args = arg
#
# try:
#     raise Networkerror("123")
# except Networkerror as e:
#     print (e.args)


