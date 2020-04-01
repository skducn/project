#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2020-3-5
# Description: 类与对象（继承，多态，公有私有，多重继承）
# https://blog.csdn.net/weixin_42994525/article/details/86654983
#****************************************************************

class Person:
    hair = 'black'
    def __init__(self, name="Will", age=8):
        self.name = name
        self.age = age
    def say(self, content):
        print(content)


p = Person()
p.skills = ['programming']  # 在__init__中增加成员变量，如 skills = ['programming']
print(p.name)  # Will
print(p.age)  # 8
print(p.hair)  # black
print(p.skills)  # ['programming']
del p.name  # 删除p对象的name成员变量，
# print(p.name)  # 报错，因为已经被删除了。
# 注意：不影响其他对象对name的调用，再新建一个x对象时，name实例变量任然会被构造。
x = Person()
print(x.name)  # Will

# *************************************************************************************

# 继承，子类共享父类数据和方法的机制
# 继承列表属性的类
class Mylist(list):
    pass
    # // Mylist类继承了list，因此实例化的list2具有list的特性。

list2 = Mylist()
print(list2)   # []
list2.append(5)
list2.append(6)
print(list2)  # [5, 6]

# *************************************************************************************

# 多态，多态指的是父类的引用指向子类的对象

class Animal(object):
    pass

class Cat(Animal):
    pass

class Pig(Animal):
    pass

a = list()
b = Animal()
c = Cat()

# isinstance(变量,类型)
print(isinstance(a, list))  # True
print(isinstance(b, Animal))  # True
print(isinstance(c, Cat))  # True
print(isinstance(c, Animal))  # True
print(isinstance(b, Pig))  # false

# *************************************************************************************

# 使用多态，不同的子类对象可以共用一个函数
# 需求：饲养员喂养猫和老鼠，老虎等动物
# 分析：
# 定义饲养员的类和动物的类
# 定义老鼠类，猫类等继承动物类
# 在饲养员中定义类成员函数，喂养

class Person(object):
    '''
    def feedCat(self,cat):
        print("喂养" + cat.name)
    def feedMouse(self,mouse):
        print("喂养" + mouse.name)
    def feedTiger(self,tiger):
        print("喂养" + tiger.name)
    '''

    def feedAnimal(self, ani):
        print("喂养" + ani.name)


class Animal(object):
    def __init__(self, name):
        self.name = name

    def eat(self):
        print("eating")


class Mouse(Animal):
    def __init__(self, name):
        super(Mouse, self).__init__(name)


# 1.创建一个饲养员的对象
p = Person()
# 2.创建Mouse的对象
m = Mouse("Tom")
# 3.饲养员执行自己的行为
p.feedAnimal(m)  # 喂养To


# *************************************************************************************#

# 公有变量，私有变量
# 1，默认情况对象的属性和方法都是公有的
# 2，Python内部给出了一个name mangling（名字改编，名字重整）的机制
# 在python中定义私有变量只需要在变量名或函数名前加上‘’__‘’两个下划线
class Person():
    name = '小义'
    __alise = '小wang'
    def getname(self):
        return self.__alise

p = Person()
print(p.name)  # '小义'
# print(p.__alise)  # 报错，AttributeError: 'Person' object has no attribute '__alise'，不能用这种方式访问私有变量。
print(p._Person__alise)  # 小wang
print(p.getname())  # 小wang  //通过函数调用私有变量。

# # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
# # 继承，子类继承父类的属性和方法，如果子类调用的函数与父类同名，则优先调用子类自己的函数。
#
# # 继承一般函数，如：hello()
# class Parent:
#     def hello(self):
#         print('正在调用父类的方法')
# class Child(Parent):
#     pass
# p = Parent()
# p.hello()  # 正在调用父类的方法
# c = Child()
# c.hello()  # 正在调用父类的方法
#
# class Child(Parent):
#     def hello(self):
#         print('子类的方法')
# c = Child()
# c.hello()  # 子类的方法
# p.hello()  # 正在调用父类的方法
#
# # 继承构造函数,__init__()
# import random as r
# class Fish:
#     def __init__(self):
#         self.x = r.randint(0, 10)
#         self.y = r.randint(0, 10)
#     def move(self):
#         self.x -= 1
#         print('我的位置是：', self.x, self.y)
#
# class Goldfish(Fish):
#     pass
# class Carp(Fish):
#     pass
# class Shark(Fish):
#     def __init__(self):
#         self.hungry = True
#
#     def eat(self):
#         if self.hungry:
#             print('饿了，要进食')
#             self.hungry = False
#         else:
#             print("吃饱了")
#
# fish = Fish()
# fish.move()  # 我的位置是： 2 8
# goldfish = Goldfish()
# goldfish.move()  # 我的位置是： 9 0
# shark = Shark()
# shark.eat()  # 饿了，要进食
# shark.eat()  # 吃饱了  , 因为__init__构造函数只执行一次。
# # shark.move()  # 报错，AttributeError: 'Shark' object has no attribute 'x'， 因为子类shark中新定义的__init__()覆盖了父类fish的方法和属性（__init__()）
# # 解决方法是在shark的__init__()中第一行添加 Fish.__init__(self) 或 super().__init__()
# # Fish.__init__(self) ，表示执行Fish的__init__(), 这里要写上self。
# # super().__init__()， 表示执行父类的__init__，说白了就是将父类覆盖了子类的__init__。
#
# # 》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
# # 多重继承：一个子类可以继承多个父类的属性和方法
#
# class Base1:
#     def fool1(self):
#         print('我是fool1')
# class Base2:
#     def fool2(self):
#         print('我是fool2')
#
# class C(Base1, Base2):
#     pass
# c = C()
# c.fool1()  # 我是fool1
# c.fool2()  # 我是fool2
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
