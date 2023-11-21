# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2020-3-3
# Description: type(object) & type(name, bases, dict)
# 定义：type函数有两种功能，即按照参数数量可实现 返回类型 或 创建动态对象类（如class）
# 1,type(object)  //传入一个参数时，返回 object 的类型。 返回值是一个 type 对象，通常与 object.__class__ 所返回的对象相同。
# 推荐使用 isinstance() 内置函数来检测对象的类型，因为它会考虑子类的情况。
# 2,type(name, bases, dict) //传入三个参数时，返回一个新的 type 对象。 这在本质上是 类与实例 语句的一种动态形式。
# name 字符串即类名并且会成为 __name__ 属性；
# bases 元组列出基类并且会成为 __bases__ 属性；
# dict 字典为包含类主体定义的命名空间并且会被复制到一个标准字典成为 __dict__ 属性；

# todo 关于对象、类、元类
# python中一切都是对象，类也是对象；只不过type是一种特殊的对象（元类）；
# python中类创建的本质，当使用 类与实例 创建类时，Python 底层其实使用的是type() 函数来创建，因此可以直接使用 type() 函数来实现动态创建类。
# 元类就是类的类，type() 实际上是一个元类，它创建所有的类，如下：
# 任何对象最终的所属类都是type
# num = 1
# print(num.__class__)  # <类与实例 'int'>  // num的类型是整数
# print(num.__class__.__class__)  # <类与实例 'type'>  //整数的类型是type

# 标准库：https://docs.python.org/zh-cn/3.7/library/functions.html#type
#***************************************************************


print("1，一般用class创建类".center(100, "-"))
# 分析，当使用 类与实例 创建类时其实是定义了一个特殊的对象（type 类的对象），并将该对象赋值给 Animal 变量，即 类与实例 定义的所有类都是 type 类的实例。
class Animal():

    speed = 100  # 类的属性

    def __init__(self):
        self.color = 'red'   # 实例属性，以self为前缀
        zone = "China"  # 局部变量

        self.__color2 = "blue"  # 定义一个私有属性，类的外部不能直接访问

    def getColor(self):  # 类方法
        print(self.__color2)  # 打印出私有变量

    def eat(self):
        print("meat")

tiger = Animal()
print(type(Animal))  # <类与实例 'type'>  //Animal类本身的类型就是type
print(type(tiger))  # <类与实例 '__main__.Animal'>  //tiger是从Animal类实例化

tiger.eat()  # meat   //等同于类名调用 Animal.eat('')
print(tiger.speed)  # 100
Animal.speed = Animal.speed + 20   # 修改类属性
print(Animal.speed)  # 120

sheep = Animal()
print(sheep.speed)  # 120





print("2，用type()动态创建类".center(100, "-"))
def Run(self):
    self.name = '张三'
    print("I like run")

Student = type("Student",(object,), {"age" : 13, "interest" : Run})
print(Student)  # <类与实例 '__main__.Student'>
s = Student()
print(s.age)  # 13   //类的属性，不是实例属性
s.interest()  # I like run
print(s.name)  # 张三



















