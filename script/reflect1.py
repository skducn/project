#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 反射机制
# 反射机制就是在运行时，动态的确定对象的类型，并可以通过字符串调用对象属性、方法、导入模块，是一种基于字符串的事件驱动。
# python是一门解释型语言，因此对于反射机制支持很好。在python中支持反射机制的函数有 eval()、exec()、getattr()、setattr()、delattr()、__import__，这些函数都可以执行字符串。
# http://www.imooc.com/article/details/id/287771
#****************************************************************


print("1，eval() 执行单个表达式获取值（有返回值）".center(100, "-"))
# 注意：不能是复杂的代码逻辑，不能是赋值表达式。
b = eval("12 + 43")
print(b)  # 55


print("2，eval() 执行复杂表达式（无返回值）".center(100, "-"))
# 2.1，简单赋值语句
b = exec("aa = 21")
print(b)      # None   //exec无返回值
print(aa)    # 21  //exec执行了赋值语句，并定义了aa变量

# 2.2，复杂表达式
a = '''ret = []
for i in range(10):
    ret.append(i)'''
exec(a)
print(ret)   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 2.3，导入模块
exec("import reflect1_test")
print(reflect1_test.KEYWORD)   # john


print("2.4，动态创建类".center(100, "-"))
class Base1:
    def __init__(self):
        print("base111")
a = "Base1"
exec(a + "()")  # 相当于执行 Base()


class Base2:
    def __init__(self):
        self.name = "name123"
    def test123(self, abc):
        print("test777")
        print(abc + 333)
        return "Base3::test4"

a = Base2()
# 通过字符串来调用a对象的test方法
b = eval("a.test123(111)")
# test777
# 444

print(b)  # Base3::test4

exec("a.test123(222)")
# test777
# 555


print("3，hasattr 判断属性是否存在".center(100, "-"))
if hasattr(a, "test123"):
    func = getattr(a, "test123")
    func(3)
    # test777
    # 336

print("4，setattr() 设置属性方法".center(100, "-"))
# 将 name="name123" 改为 name="jinhao"
setattr(a, "name", "jinhao")
print(a.name)  # jinhao //改变原有属性的值


print("5，getattr() 获取属性的方法".center(100, "-"))
# 新增属性并赋值，如 : age=33
setattr(a, "age", "33")
print(getattr(a, "age"))  # 33
print(a.age)  # 33


print("6，__import__() 动态导入一个对象".center(100, "-"))
# 通过对象方式调用，参数 formlist
a = __import__("reflect1_test", fromlist=True)
print(a.KEYWORD)  # john
a.comm_function()  # test_module
print(a.__name__)  # reflect1_test
