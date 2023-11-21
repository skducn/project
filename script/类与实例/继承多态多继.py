# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-7-7
# Description: 继承，多态，多重继承
# ********************************************************************************************************************

# 1，继承是子类自动共享父类之间数据和方法的机制

class Mylist(list):
    pass
    def test(self):
        pass
def func():
    pass

list2 = Mylist()
print(list2)
list2.append(5)
list2.append(6)
print(list2)



class A:
    def foo(self):
        print('called A.foo()')

class B(A):
    pass

class C(A):
    def foo(self):
        print('called C.foo()')

class D(B, C):
    pass

if __name__ == '__main__':
    d = D()
    d.foo()


class Person():

    name = '小义'

    __alise = '小wang'

    def getname(self):

        return self.__alise

p = Person()

print(p.name)  # '小义'

# print(p.__alise)  # 报错，AttributeError: 'Person' object has no attribute '__alise'，因为不能用这种方式访问私有变量。

print(p._Person__alise)  # 小wang , 通过函数self方式调用私有变量。

print(p.getname())  # 小wang, 通过函数self方式调用私有变量。




# 类与实例 GrandFather():
#     print('我是爷爷')
#
# 类与实例 Parent(GrandFather):
#     print('我是父类')
#
# 类与实例 SubClass(Parent):
#     print('我是子类')
#
# # sub = SubClass()
# SubClass()
# #注意：类在定义的时候就执行类体代码，执行顺序是从上到下

#
class Parent2():
    print('干爹')

class Parent():
    print('亲爹')

class Me(Parent, Parent2):
    print('我')
Me()

print(Me.__bases__)  # (<类与实例 '__main__.Parent'>, <类与实例 '__main__.Parent2'>)

#注意：类在定义的时候就执行类体代码，执行顺序是从上到下
#
# print(SubClass.__bases__)
# #注意，如果sub = SubClass(),sub是没有__bases__方法的

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
people.call()



class Parent:
    def hello(self):
        print('父类的方法')

class Child(Parent):
    pass

p = Parent()
p.hello()  # 父类的方法
c = Child()
c.hello()  # 父类的方法


class Child(Parent):

    def __init__(self):
        super(Child, self).__init__()

    def hello(self):
        print('子类的方法')



c = Child()
c.hello()  # 子类的方法
p.hello()  # 父类的方法

# 「方法解析顺序」（Method Resolution Order，或MRO
print(Child.mro())  # [<类与实例 '__main__.Child'>, <类与实例 '__main__.Parent'>, <类与实例 'object'>]


# 经典类的 MRO
import inspect
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

print(inspect.getmro(D))
# (<类与实例 '__main__.D'>, <类与实例 '__main__.B'>, <类与实例 '__main__.C'>, <类与实例 '__main__.A'>, <类与实例 'object'>)

print(D.__mro__)
# (<类与实例 '__main__.D'>, <类与实例 '__main__.B'>, <类与实例 '__main__.C'>, <类与实例 '__main__.A'>, <类与实例 'object'>)

x = D()
x.show()

# 菱形继承
# 按照深度遍历,重复类只保留最后一个
# 按照深度遍历，其顺序为 [D, B, A, object, C, A, object]，重复类只保留最后一个，因此变为 [D, B, C, A, object]


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

print(C.__mro__)
# (<类与实例 '__main__.C'>, <类与实例 '__main__.A'>, <类与实例 '__main__.X'>, <类与实例 '__main__.B'>, <类与实例 '__main__.Y'>, <类与实例 'object'>)
c = C()


# c a x b y object






class Parent:
   def myMethod(self):
      print('父类方法')

class Child(Parent):
   def myMethod(self):
      print('子类方法')

c = Child()          # 子类实例
c.myMethod()         # 子类调用重写方法



class Person(object):
    def __init__(self,name,sex):
        self.name = name
        self.sex = sex

    def print_title(self):
        if self.sex == "male":
            print("man")
        elif self.sex == "female":
            print("woman")

class Child(Person):
    def print_title(self):
        if self.sex == "male":
            print("boy")
        elif self.sex == "female":
            print("girl")

May = Child("May","female")
Peter = Person("Peter","male")

print(May.name,May.sex,Peter.name,Peter.sex)
May.print_title()
Peter.print_title()