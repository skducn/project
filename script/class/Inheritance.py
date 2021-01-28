# -*- coding: utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2021-1-28
# Description: 继承 Inheritance  及 重写 override
# 继承：实现代码的重用，减少代码冗余，提高重用性。
# 继承的概念：子类拥有父类的所有方法和属性，继承是类与类之间的关系
# 继承的传递性：C 类从 B 类继承，B 类又从 A 类继承，那么 C 类就具有 B 类和 A 类的所有属性和方法，子类拥有父类以及父类的父类中封装的所有属性和方法。
# 如何继承：单继承、多继承、其他对象继承、顺序继承、组合（除了继承之外的一种高重用性的方式）
#****************************************************************

# todo: 单继承
class GrandFather():
    print('爷爷')
class Parent(GrandFather):
    print('爸爸')
class Me(Parent):
    print('我')
me = Me()
# 爷爷
# 爸爸
# 我
print(Me.__bases__)  # (<class '__main__.Parent'>,)  //继承了哪些类



# todo: 多继承
class Fruit:
    def info(self, weight):
        self.weight = weight
        print("水果的重量: %s" % (self.weight))
class Food:
    def taste(self):
        print("不同食物，口味不同")
class Apple(Fruit, Food):
    pass
a = Apple()
a.info(25)  # 水果的重量: 25
a.taste()  # 不同食物，口味不同
print(Apple.__bases__)  # (<class '__main__.Fruit'>, <class '__main__.Food'>)   //继承了哪些类，从左到右。



# todo: 多继承，如多个类的父类方法名字重名时，只获取第一个父类的方法
class Item:
    def info(self):
        print("这是一个商品")
class Product:
    def info(self):
        print('这是一个工艺')
class Mouse(Product,Item): #父类顺序，如果有相同的方法，先调用一个参数
    pass
m = Mouse()
m.info()  # 这是一个工艺

# 内置属性 __mro__ 可以查看类方法搜索顺序
# MRO 是 method resolution order，主要用于在多继承时判断方法、属性的调用路径
print(Mouse.__mro__)  # (<class '__main__.Mouse'>, <class '__main__.Product'>, <class '__main__.Item'>, <class 'object'>)



# todo: 其他对象继承，如 dict，list，tuple等
class Mylist(list):
    pass
list2 = Mylist()  # Mylist类继承了list，因此实例化的list2具有list的特性。
list2.append(5)
list2.append(6)
print(list2)  # [5, 6]



# todo: 继承顺序，方法解析顺序MRO（Method Resolution Order）
# 新式类的MRO：object

class A:
    def show(self):
        print("A.show()")
class B(A):
    pass
class C(A):
    def show(self):
        print("C.show()")
class D(B, C):
    pass

print(D.__mro__)  # (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
# 分析：d b a object c a object,重复的保留最后一个，最后结果： d b c a object
x = D()
x.show()  # C.show()


# 复杂继承，新式类的MRO：object
class X(object):
    pass
class Y(object):
    pass
class A(X, Y):
    print("aaa")
class B(Y):
    print("bbb")
class C(A, B):
    pass

print(C.__mro__)  # (<class '__main__.C'>, <class '__main__.A'>, <class '__main__.X'>, <class '__main__.B'>, <class '__main__.Y'>, <class 'object'>)
# 分析：c a x object y object b y object, 重复的保留最后一个，最后结果： c a x b y object



# todo: 组合，除了继承之外的一种高重用性的方式
# 组合是将两个无继承关系的类进行关联。如：人和手机是两个不同的类，没法互相继承，但组合在一起可以是“人用手机打电话”。
class Mobile():
    def call(self):
        return("打电话")

class People():
    def __init__(self, name, mobile):
        self.name = name
        self.mobile = mobile
    def call(self):
        print(self.name + self.mobile)

people = People('小白', Mobile().call())
people.call()  # 小白打电话



# todo: 子类重写父类方法，调用子类的方法
class Bird:
    def fly(self):
        print("我在天空里自由自在地飞翔")
class Ostrich(Bird):
    def fly(self):  #重写Bird类的fly()方法
        print("我只能在地上奔跑")
os = Ostrich()
os.fly()  # 我只能在地上奔跑



# todo: 子类重写父类方法，调用父类的方法
class BaseClass:
    def foo(self):
        print("父类中定义的foo方法")
class SubClass(BaseClass):
    def foo(self):
        print("子类中定义的foo方法")
    def bar(self):
        self.foo()   # 调用子类的 foo
        # BaseClass.foo(self)  # 调用父类的 foo ,通过类名调用父类被重写的方法（不推荐，因为如果使用当前子类名调用方法，会形成递归调用，出现死循环）
        super().foo()  # # 调用父类的 foo ,通过super().父类方法
sc = SubClass()
sc.bar()
# 子类中定义的foo方法
# 父类中定义的foo方法


# todo: 继承之重写构造函数
import random as r
class Fish:
    def __init__(self):
        self.x = r.randint(0, 10)
        self.y = r.randint(0, 10)
    def move(self):
        self.x -= 1
        print('我的位置是：', self.x, self.y)
class Goldfish(Fish):
    pass
class Carp(Fish):
    pass
class Shark(Fish):
    def __init__(self):
        # super().__init__()
        self.hungry = True
    def eat(self):
        if self.hungry:
            print('饿了，要进食')
            self.hungry = False
        else:
            print("吃饱了")

fish = Fish()
fish.move()  # 我的位置是： 2 8
goldfish = Goldfish()
goldfish.move()  # 我的位置是： 9 0
shark = Shark()
shark.eat()  # 饿了，要进食
shark.eat()  # 吃饱了   // __init__构造函数只执行一次。
# shark.move()  # 报错，AttributeError: 'Shark' object has no attribute 'x', 原因是shark中__init__()覆盖了父类fish的__init__()）

# 解决方法：在shark的__init__构造函数中第一行设置 super().__init__() 或 Fish.__init__(self)
# super().__init__()， 表示执行父类的__init__，说白了就是将父类覆盖了子类的__init__
# Fish.__init__(self) ，表示执行Fish的__init__(), 这里要写上self，这个方式不推荐。



# todo: 使用super函数调用父类构造方法1
class Fooparent:
    def __init__(self):
        self.parents = '5 I\'m the parent'
        print("1 Parent11")
    def bar(self,message):
        print("3 %s from Parent"% message)
class FooChild(Fooparent):
    def __init__(self):
        super().__init__()   # 等同于 super(FooChild,self).__init__()
        print("2 child22")
        # self.parents = '66 I\'m the parent'
    def bar(self,message):
        super().bar(message)   # 等同于 super(FooChild,self).bar(message)
        print("4 Child bar function")
        print(self.parents)

foochild = FooChild()
foochild.bar("jinhao")
# 1 Parent11
# 2 child22
# 3 jinhao from Parent
# 4 Child bar function
# 5 I'm the parent
# 分析：执行FooChild的构造函数，先执行父类构造函数，再执行子类构造函数，完成了1，2； 继续持续bar方法中父类bar，再执行子类bar，完成了3，4，
# 关于print(self.parents)，先搜索子类构造函数中是否存在这个成员变量，如果存在则输出，否则查早父类中的这个变量，这里是输出了父类的这个变量。



# todo: 使用super函数调用父类构造方法2
class  Employee:
    def __init__(self,salary):
        self.salary = salary
    def work(self):
        print("普通员工正在写代码，工资是：",self.salary)
class Customer(Employee):
    def __init__(self, favorite, address,salary):
        self.favorite = favorite
        self.address = address
        self.salary = salary
    def info(self):
        print("我是一个顾客，我的爱好是：%s,地址是%s" % (self.favorite,self.address))
        super().__init__(self.salary)
        #manager 继承了Employee,Customer
class Manager(Customer):
    def __init__(self, favorite, address,salary):
        print("manager的构造方法")
        super().__init__(favorite, address,salary)  # 等同于 super(Manager, self).__init__(favorite, address)  # super函数调用父类的构造方法

m = Manager("IT","beijing",10330)
m.info()
m.work()
# manager的构造方法
# 我是一个顾客，我的爱好是：IT,地址是beijing
# 普通员工正在写代码，工资是： 10330


