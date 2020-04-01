#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 反射机制
# 反射机制就是在运行时，动态的确定对象的类型，并可以通过字符串调用对象属性、方法、导入模块，是一种基于字符串的事件驱动。
# python是一门解释型语言，因此对于反射机制支持很好。在python中支持反射机制的函数有 eval()、exec()、getattr()、setattr()、delattr()、__import__，这些函数都可以执行字符串。
# http://www.imooc.com/article/details/id/287771
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# eval() 计算指定表达式的值。它只能执行单个表达式，而不能是复杂的代码逻辑，而且不能是赋值表达式。
# 通常我们使用eval的时候，主要是使用它的返回值，获取表达式计算出的值
a = "12 + 43"
b = eval(a)
print(b)

#****************************************************************

# exec() 执行复杂表达式，返回值是None
b = exec("aa = 21")
print(b)      # None，exec返回值为None
print(aa)    # 21，exec执行了赋值语句，并定义了aa变量

a = '''ret = []
for i in range(10):
    ret.append(i)'''
exec(a)
print(ret)   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# 导入模块
exec("import reflect1_test")
print(reflect1_test.KEYWORD)   # john

# 动态创建类
class Base1:
    def __init__(self):
        print("Base123")

a = "Base1"
exec(a + "()")  # 相当于执行 Base()

# eval()函数和exec()函数的区别：
# eval()函数只能计算单个表达式的值，而exec()函数可以动态运行代码段。
# eval()函数可以有返回值，而exec()函数返回值永远为None。

#****************************************************************
print("---------------------------------------------------------")
# hasattr 判断属性是否存在
# getattr() 获取属性的方法
# setattr() 设置属性方法

class Base2:
    def __init__(self):
        print("Base2")
        self.name = "name123"

    def test123(self, abc):
        print("test777")
        print(abc + 333)
        return "Base3::test4"

a = Base2()

b = eval("a.test123(111)")  # 通过字符串来调用a对象的test方法
print(b)  # 有返回值 Base3::test4

exec("a.test123(222)")  # 同eval，但返回值是None


print("///////////////////////")

if hasattr(a, "test123"):
    func = getattr(a, "test123")
    func(3)

setattr(a,"name","jinhao")
print(a.name)  # 改变原有属性的值

setattr(a,"age","33")
print(getattr(a,"age"))   # 新增属性，并设置值 同 # print(a.age)


#****************************************************************
# __import__() 动态导入一个对象，通过对象方式调用，重要参数 formlist

a = __import__("reflect1_test", fromlist=True)
print(a.KEYWORD)  # john
a.comm_function()  # test_module
print(a.__name__)  # reflect1_test
