# -*- coding: utf-8 -*-

def singleton(cls):
    _instance = {}    # 不建议外部调用
    def _singleton(*args, **kargs):
            if cls not in _instance:
                    _instance[cls] = cls(*args, **kargs)
            return _instance[cls]
    return _singleton


@singleton
class A(object):
        a = 1
        def __init__(self, x = 0):
                self.x = x

a1 = A(2)
a2 = A(3)

print(id(a1))
print (id(a2))
print (a1.x)
print (a2.x)


# # 1、类中私有变量或私有方法不能被实例引用
# # 2、实例引用时通过_类__私有变量直接init中私有变量，类似地，实例引用可通过_类_私有方法直接访问
# # 3、私有方法可以重写init的self.x值
#
# 类与实例 A(object):
#     def __init__(self, x):
#         self.__a = 5  # 私有变量
#         self.x = x
#     def __func(self):
#         # 私有方法
#         self.x = 3
#         print("1212121221")
#
# a = A(2)
# print(a.x) # 2 , init中构造了self.x,所以才能print a.x
#
# # print(a.__a) 报错，私有变量不能被实例引用，"AttributeError: 'A' object has no attribute '__a'"
# # print(a.__func) # 报错，私有方法不能被实例引用，AttributeError: 'A' object has no attribute '__b'
#
# print(a._A__a)#  5 ， 通过_类名__变量，直接访问
# a._A__func()  # 通过_类名__方法，初始化ini中self.x
# print(a.x) # 3
#
