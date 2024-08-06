#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 反射机制
# 反射机制就是在运行时，动态的确定对象的类型，并可以通过字符串调用对象属性、方法、导入模块，是一种基于字符串的事件驱动。
# python是一门解释型语言，因此对于反射机制支持很好。
# 在python中支持反射机制的函数有 eval()、exec()、hasattr()、getattr()、setattr()、delattr()、__import__，这些函数都可以执行字符串。
# python反射机制: http://www.imooc.com/article/details/id/287771
# Python 反射与元编程 http://www.51testing.com/?action-viewnews-itemid-7802037
#****************************************************************

'''
1，eval() 简单表达式，有返回值。

2.1，exec() 复杂表达式，无返回值
2.2，exec() 赋值语句，无返回值
2.3，exec() 导入模块，一般用于临时导入
2.4，exec() 调用类
2.5，exec() 调用类中方法
2.6，exec() 调用方法

3.1，hasattr判断对象t中有没有name属性
3.2，hasattr判断对象t中有没有do方法

4，getattr获取对象的属性值
5，setattr新增或修改对象的属性
6，delattr删除对象的属性

7，__import__(module) 动态加载类和函数

8，动态函数名
'''

# print("1，eval() 简单表达式，有返回值。".center(100, "-"))
# r = eval("12 + 43")
# print(r)  # 55
#
# print("2.1，exec() 复杂表达式，无返回值".center(100, "-"))
# a = '''l_1 = []
# for i in range(10):
#     l_1.append(i)'''
# exec(a)
# print(l_1)   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# print("2.2，exec() 赋值语句，无返回值".center(100, "-"))
# exec("aa = 21")
# print(aa)    # 21  //exec执行了赋值语句，并定义了aa变量

# # 2.3，exec() 导入模块，一般用于临时导入
# print("2.3，exec() 导入模块，一般用于临时导入".center(100, "-"))
# exec("import reflect2")  # index
# print(reflect2.KEYWORD)   # john
# reflect2.sayHello()  # hello yoyo

# print("2.4，exec() 调用类".center(100, "-"))
# class Animal():
#     def __init__(self):
#         print("hello123")
# a = "Animal"
# exec(a + "()")  # # hello123   //相当于执行 Animal()
# exec("Animal()")  # # hello123
# Animal()  # hello123

# print("2.5，exec() 调用类中方法".center(100, "-"))
# class Base2:
#     def __init__(self):
#         self.name = "测试"
#     def func2(self, abc):
#         print("百度")
#         print(abc + 10)
#         return "淘宝"
# a = Base2()
# b = eval("a.func2(5)")
# # 百度
# # 15
# print(b)   # 淘宝
# exec("a.func2(7)")
# # 百度
# # 17
#
# print("2.6，exec() 调用方法".center(100, "-"))
# def test():
#     print("123")
# exec('test()')  # 123



class Teacher:
    def __init__(self):
        self.name = "张老师"

    def do(self, test):
        print("报名")
        print(test + 10)
        return "备课"
t = Teacher()


print("3.1，hasattr判断对象t中有没有name属性".center(100, "-"))
print(hasattr(t, "name"))  # True
if hasattr(t, "name"):
    print(t.name)   # 张老师

print("3.2，hasattr判断对象t中有没有do方法".center(100, "-"))
print(hasattr(t, "do"))  # True
if hasattr(t, "do"):
    func = getattr(t, "do")
    b = func(3)
    # 报名
    # 13
    print(b)  # 备课

print("4，getattr获取对象的属性值".center(100, "-"))
print(getattr(t, "name"))  # 张老师
print(getattr(t, "age", 34))  # 34  //t对象中没有age属性，这里设置了default默认值34 , 没什么意义。

print("5，setattr新增或修改对象的属性".center(100, "-"))
setattr(t, "sex", "女")  # 新增属性与值
print(t.sex)  # 女
setattr(t, "name", "王助理")  # 修改name属性的值
print(t.name)  # 王助理
t = Teacher()
# print(t.sex)  # AttributeError: 'Teacher' object has no attribute 'sex' //报错，因为重新实例化后，t对象已重置。


print("6，delattr删除对象的属性".center(100, "-"))
delattr(t, 'name')
# print(t.name)  # AttributeError: 'Teacher' object has no attribute 'name' //报错，因为name已被删除。



print("7，__import__(module) 动态加载类和函数".center(100, "-"))
# 通过实例化对象方式调用
# 使用场景：如果一个模块经常变化，主要用于反射或者延迟加载模块.
a = __import__("reflect2")
a.sayHello()  # hello yoyo
a.sayHelloZhCn()  # 你好 peter
print(a.KEYWORD)  # john
print(a.__name__)  # reflect2


print("7，__import__(module) 参数fromlist".center(100, "-"))

# reflectTest = __import__('reflect2',fromlist = ('user',))
reflectTest = __import__('reflect2', fromlist = True)
reflectTest.sayHello()  # hello yoyo
print(reflectTest.sayHello)  # <function sayHello at 0x000001BC6705A670>
print(reflectTest.__name__)  # reflect2





