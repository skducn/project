# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-11-19
# Description:
#
# hasattr(object, name)
# 定义：该实参是一个对象和一个字符串。如果字符串是对象的属性之一的名称，则返回 True，否则返回 False。
# （此功能是通过调用 getattr(object, name) 看是否有 AttributeError 异常来实现的。）

# getattr(object, name[, default])
# 定义：返回对象命名属性的值。
# name 必须是字符串。如果该字符串是对象的属性之一，则返回该属性的值。例如， getattr(x, 'foobar') 等同于 x.foobar。
# 如果指定的属性不存在，且提供了 default 值，则返回它，否则触发 AttributeError。

# setattr(object, name, value)
# 定义：此函数与 getattr() 两相对应。 其参数为一个对象、一个字符串和一个任意值。
# 字符串指定一个现有属性或者新增属性。 函数会将值赋给该属性，只要对象允许这种操作。 例如，setattr(x, 'foobar', 123) 等价于 x.foobar = 123。

# delattr(object, name)
# 定义：实参是一个对象和一个字符串。该字符串必须是对象的某个属性。如果对象允许，该函数将删除指定的属性。例如 delattr(x, 'foobar') 等价于 del x.foobar 。

# 标准库：https://docs.python.org/zh-cn/3.7/library/functions.html#hasattr
# https://docs.python.org/zh-cn/3.7/library/functions.html#getattr
# https://docs.python.org/zh-cn/3.7/library/functions.html#setattr
# *****************************************************************

class Teacher:
    def __init__(self):
        self.name = "张老师"

    def do(self, test):
        print("报名")
        print(test + 10)
        return "备课"
t = Teacher()


print("1.1，判断对象t中有没有name属性".center(100, "-"))
print(hasattr(t, "name"))  # True
if hasattr(t, "name"):
    print(t.name)   # 张老师

print("1.2，判断对象t中有没有do方法".center(100, "-"))
print(hasattr(t, "do"))  # True
if hasattr(t, "do"):
    func = getattr(t, "do")
    b = func(3)
    # 报名
    # 13
    print(b)  # 备课


print("2，获取对象的属性值".center(100, "-"))
print(getattr(t, "name"))  # 张老师
print(getattr(t, "age", 34))  # 34  //t对象中没有age属性，这里设置了default默认值34 , 没什么意义。



print("3，新增或修改对象的属性".center(100, "-"))
setattr(t, "sex", "女")  # 新增属性与值
print(t.sex)  # 女

setattr(t, "name", "王助理")  # 修改name属性的值
print(t.name)  # 王助理

t = Teacher()
# print(t.sex)  # AttributeError: 'Teacher' object has no attribute 'sex' //报错，因为重新实例化后，t对象已重置。


print("4，删除对象的属性".center(100, "-"))
delattr(t, 'name')
# print(t.name)  # AttributeError: 'Teacher' object has no attribute 'name' //报错，因为name已被删除。