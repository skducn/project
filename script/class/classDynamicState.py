# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: 类的动态属性、slots、type函数定义类
# ********************************************************************************************************************

# todo: python动态属性、方法
class Cat:
    def __init__(self, name):
        self.name = name
def walk_func(self):
    print("%s慢慢走过每一片草地"% self.name)

d1 = Cat('Marry')
d2 = Cat('Kitty')
Cat.walk = walk_func   # 将一个方法在类外进行定义，就是动态方法。
d1.walk()  # Marry慢慢走过每一片草地
d2.walk()  # # Kitty慢慢走过每一片草地


# todo: __slot__限定动态添加的属性和方法
class Dog:
    __slots__ = ('walk', 'age', 'name')    # 限定这3个属性
    def __init__(self,name):
        self.name = name
    def bar(self):
        print("预先定义好的test方法")

d = Dog('Snoogy')
d.age = 5     #  添加age属性
print(d.age)  # 5
# d.weight = 24     #报错 ，因为slots 限定属性中没有 weight
Dog.walk = walk_func   # 定义动态方法
d.walk()   # Snoogy慢慢走过每一片草地
d.bar()  # 预先定义好的test方法
Dog.bar = lambda self: print("abc")  # 覆盖bar()方法
d.bar()   # abc



# todo: type函数定义类
def fn(self):
    print("fn函数")
Dog = type('Dog',(object,),dict(walk = fn,age = 6))  # 使用type函数定义Dog类

d = Dog()
print(type(d))  # <class '__main__.Dog'>
print(type(Dog))  # <class 'type'>
print(type(Dog()))  # <class '__main__.Dog'>
print(type(d.walk))  # <class 'method'>
d.walk()  # fn函数
print(d.age)  # 6