#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2019-10-28
# Description: 反射机制
# 反射机制就是在运行时，动态的确定对象的类型，并可以通过字符串调用对象属性、方法、导入模块，是一种基于字符串的事件驱动。
# python是一门解释型语言，因此对于反射机制支持很好。在python中支持反射机制的函数有 eval()、exec()、getattr()、setattr()、delattr()、__import__，这些函数都可以执行字符串。
# python反射机制: http://www.imooc.com/article/details/id/287771
#****************************************************************


print("1，eval() 执行单个表达式，且有返回值。".center(100, "-"))
b = eval("12 + 43")
print(b)  # 55


print("2.1，exec() 赋值语句，且无返回值".center(100, "-"))
# # 2.1，简单赋值
b = exec("aa = 21")
print(b)      # None   //因为exec无返回值
print(aa)    # 21  //exec执行了赋值语句，并定义了aa变量


print("2.2，exec() 执行字符串跨行之复杂表达式".center(100, "-"))
a = '''ret = [] 
for i in range(10):
    ret.append(i)'''
exec(a)
print(ret)   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


print("2.3，exec() 导入模块，一般用于临时导入".center(100, "-"))
exec("import reflect2")  # index
print(reflect2.KEYWORD)   # john
reflect2.sayHello()  # hello yoyo


print("2.4，exec() 执行动态类".center(100, "-"))
class Animal():
    def __init__(self):
        print("hello123")
a = "Animal"
exec(a + "()")  # # hello123   //相当于执行 Animal()
Animal()  # hello123


print("2.5，exec() 执行动态类".center(100, "-"))
class Base2:
    def __init__(self):
        self.name = "测试"
    def func2(self, abc):
        print("百度")
        print(abc + 10)
        return "淘宝"
a = Base2()
b = eval("a.func2(5)")
# 百度
# 15
print(b)   # 淘宝

exec("a.func2(7)")
# 百度
# 17



print("3，hasattr 判断对象是否包含对应的属性".center(100, "-"))
if hasattr(a, "name"):
    print(a.name)   # 测试

if hasattr(a, "func2"):
    func = getattr(a, "func2")
    b = func(3)
    # 百度
    # 13
    print(b)  # 淘宝

print("4，setattr() 设置属性值".center(100, "-"))
# 将 name="name123" 改为 name="jinhao"
setattr(a, "name", "jinhao")
print(a.name)  # jinhao
a = Base2()
print(a.name)  # 测试

print("5，getattr() 返回一个对象属性值".center(100, "-"))
# 新增属性并赋值，如 : age=33
setattr(a, "age", "33")
print(getattr(a, "age"))  # 33
print(a.age)  # 33
a = Base2()
# print(a.age)  # 报错，因为重新创建对象后，setattr设置的值就不存在了，所以它是不安全的。



print("6，__import__(module) 动态加载类和函数".center(100, "-"))
# 通过对象方式调用，参数 formlist
# 使用场景：如果一个模块经常变化。主要用于反射或者延迟加载模块.
a = __import__("reflect2")
a.sayHello()  # hello index
a.sayHelloZhCn()  # 你好 index
print(a.KEYWORD)  # john
print(a.__name__)  # reflect2

# reflectTest = __import__('reflectTest.user',fromlist = ('user',))
# reflectTest.sayHello()
# print(reflectTest.user)