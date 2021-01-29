# -*- coding: utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2021-1-28
# Description: 多态 Polymorphism
# 多态 不同的对象调用相同的方法，产生不同的执行结果，增加代码的灵活度
# 多态：多态指的是一类事物有多种形态
#****************************************************************


class Animal:
    def run(self):
        pass

class Person(Animal):
    def run(self):
        print("人跑")

class Dog(Animal):
    def run(self):
       print("狗跑")

class Pig(Animal):
    def run(self):
       print("猪跑")

person = Person()
dog = Dog()
pig = Pig()

person.run()  # 人跑
dog.run()  # 狗跑
pig.run()  # 猪跑
# 同属一个父类，但是他们在run这个方法上表现出不能的形态，这就是多态。
# 多态性是指当不同的对象收到相同的消息时，产生不同的动作。


#
# # 使用多态，不同的子类对象可以共用一个函数
# # 需求：饲养员喂养猫和老鼠，老虎等动物
# # 分析：
# # 定义饲养员的类和动物的类
# # 定义老鼠类，猫类等继承动物类
# # 在饲养员中定义类成员函数，喂养
#
# class Person(object):
#     '''
#     def feedCat(self,cat):
#         print("喂养" + cat.name)
#     def feedMouse(self,mouse):
#         print("喂养" + mouse.name)
#     def feedTiger(self,tiger):
#         print("喂养" + tiger.name)
#     '''
#
#     def feedAnimal(self, ani):
#         print("喂养" + ani.name)
#
#
# class Animal(object):
#     def __init__(self, name):
#         self.name = name
#
#     def eat(self):
#         print("eating")
#
#
# class Mouse(Animal):
#     def __init__(self, name):
#         super(Mouse, self).__init__(name)
#
#
# # 1.创建一个饲养员的对象
# p = Person()
# # 2.创建Mouse的对象
# m = Mouse("Tom")
# # 3.饲养员执行自己的行为
# p.feedAnimal(m)  # 喂养Tom