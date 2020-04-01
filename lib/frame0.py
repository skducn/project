# -*- coding: utf-8 -*-
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-12-20
# Description: python语法
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# python中,用双下划线定义的方式属于私有、隐藏方法，不能被实例化方式调用 。

# 同样，类中双下划线开头定义的属性属于私有属性，可采用 "_类__N" 的形式，如 A类中定义了 __N=78 ，则程序中用 A._A__N

class A:

    __N = 78

    def __init__(self):
        self.__x = 10
        print self.__x
        self.__y = 30

    def __foo(self):
        print 'from a'

    def bar(self):
        self.__foo()

    def fa(self):
        print 'from c'

    def test(self):
        self.fa()

# B类继承了A类的所有方法
class B(A):

    def __foo(self):
        print 'from B'

    def fa(self):
        print 'from d'

if __name__ == "__main__":
    print A._A__N  # 78
    print "@@@@@@@@@@@@@@@@@@@"

    a = A()  # 实例化a ， 执行__init__ ,输出 10
    print "@@@@@@@@@@@@@@@@@@@"

    print a._A__N  # 78
    print a._A__x  # 10
    print "@@@@@@@@@@@@@@@@@@@"

    # 以字典形式输出 __init__ 中属性的key和value
    print a.__dict__  # {'_A__y': 30, '_A__x': 10}

    # 新增属性 和 修改属性 ， 注意 __Y 与 __y 是两个不同属性
    a.__Y = 222; a._A__x = 90
    print a.__dict__  # {'__Y': 222, '_A__y': 30, '_A__x': 90}
    print "@@@@@@@@@@@@@@@@@@@"


    a.bar()  # from a
    # a.__foo()  # 报错，因为__foo是A类的私有隐藏属性，不能被实例化a调用。
    a._A__foo()  # from a  , 但可以通过 类名__foo()方式调用。
    print "@@@@@@@@@@@@@@@@@@@"

    b = B()
    b.bar()   # 先执行__init__ ,输出 10 ， 再输出 from a
    b.test()  # from d  , b调用A类中的test(), 但A、B类中都有相同的fa()方法，所以最终调用的还是B类自己的fa（）

    A.name = "john"  # A类中新增name属性并赋值。
    print A.name  # john
    print "@@@@@@@@@@@@@@@@@@@"

    del A.name  # 删除A.name 属性
    try:
       print A.name
    except:
        print "Errror, A.name is not defined "