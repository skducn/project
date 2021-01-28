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