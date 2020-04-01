# -*- coding: utf-8 -*-
# https://blog.csdn.net/Z_shoushow/article/details/80363330

class A:
    member = "this is a test."
    name = "john"

    def __init__(self, name, title):
        self.name = name
        self.title = title

    @staticmethod
    def foo1():
        # @staticmethod 修饰的函数是静态方法，该方法不强制要求传递参数（自身对象self，自身类cls参数）
        # @staticmethod 修饰器 只能调用类的属性，无法调用类中其他方法，如 A.foo4()
        # 可以直接使用 类.方法 A.foo1()调用 或 实例化 a.foo1()调用
        print(A.name)
        # print(A.foo4())  # 报错 TypeError: foo4() missing 1 required positional argument: 'self'

    @classmethod
    def foo2(cls):
        # @classmethod 修饰的函数是类方法， 第一参数必须是cls 或 self 参数 ， cls表示这个类本身，<class '__main__.A'>
        # @classmethod 修饰器 可调用类的属性及其他方法，如 cls.member，cls().fii3()
        # 可以直接使用 类.方法 A.foo2()调用 或 实例化 a.foo2()调用
        print("foo2: ", cls.member)
        cls('123','444').foo3()
        print(cls)  # <class '__main__.A'>

    @classmethod
    def foo3(self):
        print("foo3: ", self.name)
        self('123','444').foo1()
        print(self)  # <class '__main__.A'>

    def foo4(self):
        # self : 表示一个具体的实例本身，是实例化类后的地址id，如  # <__main__.A object at 0x0000024E30629F28>
        # 实例化方法（必须实例化类之后才能被调用），如 a.foo4()
        print("foo4: ", self.member)
        print(self)  # <__main__.A object at 0x0000024E30629F28>
        print(A)  # <class '__main__.A'> 表示类的本身 与 cls 结果一致。
        print(self.title)  # 获取类属性


# @classmethod 不需要self参数，但第一个参数需要是表示自身类的cls参数。


a = A('1','2')
A.foo1()  # 等同于 A().foo1() ， a.foo1()

print("--------------------------")
a.foo2()
A.foo2()
print("--------------------------")
a.foo3()
A.foo3()
print("--------------------------")
a.foo4()
# A.foo4()   报错，TypeError: foo3() missing 1 required positional argument: 'self'
