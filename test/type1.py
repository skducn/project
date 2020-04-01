# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2020-3-3
# Description: type（）动态创建类
#***************************************************************

# 1,type（）函数可以查看变量的类型，如下：

a = "123"
print(type(a))   # <class 'str'>

class Animal():
    pass
a = Animal()
print(type(a))  # <class '__main__.Animal'>
print(type(Animal))  # <class 'type'>  ，定义的Animal类本身的类型是 type

# 因此，当使用 class 定义 Animal 类时，可理解为定义了一个特殊的对象（type 类的对象），并将该对象赋值给 Animal 变量。也就是使用 class 定义的所有类都是 type 类的实例。
# 总结，Python 完全允许使用 type() 函数（相当于 type 类的构造器函数）来创建 type 对象，又由于 type 类的实例就是类，因此 Python 可以使用 type() 函数来动态创建类。

# 一般创建类及实例化调用
class Test():
    name = "Test"
    def hello(self):
        print("hello world")

t = Test()
t.hello()  # hello world  ，等同于 Test.hello(t)
print(t.name)  # Test

# 使用type()动态创建类
def hello(self):
    self.name = 10
    print("hello world")

t = type("hello",(),{"a":1,"hello":hello})
print(t)  # <class '__main__.hello'>
T = t()
print(T.a)  # 1
T.hello()  # hello world
print(T.name)  # 10

# 其实python中一切都是对象，类也是对象；只不过是一种特殊的对象，是type的对象

# python中类创建的本质：
# 我们使用class创建类，当你使用class关键字时，Python解释器自动创建这个对象。而底层其实使用的是type函数(type函数也可以查看实例所属类型)来创建类的。所以我们可以直接使用type()函数来手动实现动态创建类。

# 当ype（）只有一个参数时，其作用就是返回变量或对象的类型
# 当type（）有三个参数时，其作用就是创建类对象：
#   第一个参数：name表示类名称，字符串类型
#   第二个参数：bases表示继承对象（父类），元组类型，单元素使用逗号
#   第三个参数：attr表示属性，这里可以填写类属性、类方式、静态方法，采用字典格式，key为属性名，value为属性值

# 总结：
# 通过type添加的属性是类属性，并不是实例属性
#
# 通过type可以给类添加普通方法，静态方法，类方法，效果跟class一样
#
# type创建类的效果，包括继承等的使用性质和class创建的类一样。本质class创建类的本质就是用type创建。所以可以说python中所有类都是type创建的。

# 对元类的理解与注意事项
#
# 元类就是类的类，python中函数type实际上是一个元类。type就是Python在背后用来创建所有类的元类。
# Python中所有的东西都是对象。这包括整数、字符串、函数以及类。
# 它们全部都是对象，而且它们都是从一个类创建而来，这个类就是type。type就是Python的内建元类，当然了，也可以创建自己的元类。
#
#
# python查看对象所属类型既可以用type函数，也可以用对象自带的__class__属性。
# 以下代码验证：任何对象最终的所属类都是type。 type是所有类的创造者。

num = 1
print(num.__class__)  # <class 'int'>
print(num.__class__.__class__)  # <class 'type'>



def function2(name, age):
    print("name: %s, age: %s" % (name, age))
    return 2

x = eval("function2")("Alice", 11)
print(x)










