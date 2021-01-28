# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2021-1-28
# Description: 类装饰器 decorate
# *******************************************************************************************************************************

# todo: 类装饰器基本语
print("类装饰器基本语".center(100, "-"))
def decorator(cls):    # 装饰器函数,cls是一个类，返回也是一个类 , 等同于 Model = decorator(Model)
    print("888888")
    return cls
@decorator
class Model(object):
    def __init__(self):
        print("model created")

Model()
# 888888
# model created
# 分析：由于装饰器是在加载该模块时运行的，因此上文代码中装饰器输出的"888888"只会在加载该模块时输出一次。



# todo: 类装饰器悄悄地返回其他类的对象
print("类装饰器悄悄地返回其他类的对象".center(100, "-"))
class A():
    def __init__(self):
        print("77777")
def decorator(cls):
    return A
@decorator
class Model(object):
    def __init__(self):
        print("model created")

model = Model()  # 77777
# print(model)  # <__main__.A object at 0x000001F011CEDF10>
# 分析：返回的是A类对象



# todo: 类装饰器可以修改类对象
print("类装饰器可以修改类对象".center(100, "-"))
def decorator(cls):
    cls.test_val = 1
    return cls
@decorator
class Model(object):
    test_val = 0
    def __init__(self):
        pass

model = Model()
print(model.test_val)  # 1
# 分析：原本类 Model 中test_val=0 ，经过类装饰器的修饰，Model类的test_val值已经被改成了1。



# todo: 多层级继承，装饰器只修饰当前类
# 对于继承关系，若f装饰了类A，类B继承了A，则产生B的对象时仍然会调用装饰器f，但装饰器f只会修饰类A。
print("多层级继承，装饰器只修饰当前类".center(100, "-"))
def decorator(num):
    print(num)   # 100
    def dec2(cls):
        print(cls)   # <class '__main__.Model'>
        return cls
    return dec2
def decorator2(cls):
    print(cls)   # <class '__main__.SubModel'>
    return cls
@decorator(100)
class Model(object):
    test_val = 0
    def __init__(self):
        pass
@decorator2
class SubModel(Model):
    def __init__(self):
        pass

model = SubModel()
# 100
# <class '__main__.Model'>
# <class '__main__.SubModel'>





print("装饰器1".center(100, "-"))
# decorator装饰funB，funB作为参数引入到decorator中，同时funA返回值就是修饰后的返回值
def decorator(funB):
    print("A")
    funB()
    return "最终修饰结果"
def funB():
    print("B")
# funB()  # B
# decorator(funB())  # B A   //先执行了funB(), 再执行decorator()
# decorator(funB)  # A B    //先执行funA(), 再调用decorator()
@decorator
def funB():
    print("B")
# A  B  //先执行装饰器@decorator , 再调用funB()
print(type(funB)) #<class 'str'>   //被修饰的函数名变为了字符串
print(funB)  # 最终修饰结果  //被修饰的函数funB总是被替换成＠符号所引用的函数funA的返回值




print("装饰器2".center(100, "-"))
def foo(fn):
    #定义一个嵌套函数
    def bar(*args):
        print("===1===",args)
        n = args[0]
        print("===2===",n * (n -1))
        #查看传递给foo函数的fn函数
        print(fn.__name__)
        fn(n * (n -1))
        print("*" * 15)
        return fn(n * (n -1))
    return bar

@foo
def my_test(a):
    print("===my_test函数===", a)
print(my_test)  #返回值是bar函数<function foo.<locals>.bar at 0x032C3D20>
my_test(10)  #意思就是my_test函数被bar函数替换，调用my_test函数就是调用bar函数
# ===1=== (10,)
# ===2=== 90
# my_test
# ===my_test函数=== 90
# ***************
# ===my_test函数=== 90

my_test(6, 45)
# ===1=== (6, 45)
# ===2=== 30
# my_test
# ===my_test函数=== 30
# ***************
# ===my_test函数=== 30



print("装饰器3".center(100, "-"))
def auth(fn):
    def auth_fn(*args):
        print("----模拟执行权限检查-----")
        #回调被修饰的目标函数
        fn(*args) #作为函数参数时前面必须有*，如果在函数里面的参数则为args
    return auth_fn
@auth
def bedecorated(a,b):
    print("执行bedecotated函数，参数a:%s,参数b:%s" % (a, b))
#调用bedecorated函数，其实就是调用修饰后返回的auth_fn函数
bedecorated(4,5)
# ----模拟执行权限检查-----
# 执行bedecotated函数，参数a:4,参数b:5



