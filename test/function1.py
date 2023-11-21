# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-1-27
# Description   : 第一类对象（First-Class Object） - 函数
# 参考：http://www.360doc.com/content/17/1021/04/7210702_696800981.shtml
# 函数是第一类对象，对象模型的三个通用属性：id、类型和值
# 第一类对象的特征：
# 1，函数可赋值给一个变量
# 2，函数可作为元素添加到集合对象中,及所谓的容器对象（list\dict\set等）
# 3，函数可作为参数传递给其他函数
# 4，函数可以做函数返回值
# 高阶函数：函数接受一个或多个函数作为输入或输出（返回）的值是函数时，这样的函数成为高阶函数， 如python内置函数中，map函数接受一个函数和一个迭代对象为参数。
# 嵌套函数：函数可以嵌套函数，python允许函数中定义函数。
# 实现了 __call__的类也可以作为函数
# 判断对象是否为可调用对象，使用内置函数callable。
# *****************************************************************

# 一个计算参数text长度的简单函数
def foo(text):
    return len(text)
print(foo('zen of python'))   # 13


# todo:函数是对象，拥有对象模型的三个通用属性：id、类型、值
print(id(foo))   # 1632628305984
print(type(foo))  # <类与实例 'function'>
print(foo)  # <function foo at 0x000001C3F7F8F040>

# todo: 1，函数可赋值给一个变量
bar = foo     # 赋值给另一个变量时，函数不会被调用，仅仅是在函数对象上绑定了一个新的名字而已。
print(bar('zhiying'))   # 7
apple = bar   # 本质上这些变量最终指向的都是同一个函数对象
print(apple('苹果'))   # 2

# todo: 2，函数作为元素存储在容器对象中（list、dict、set等）
funcs = [foo, str, len]
for f in funcs:
    print(f('hello'))
# 5
# hello
# 5
print(funcs[0])  # <function foo at 0x0000022349F5F040>
print(funcs[0]("test"))  # 4

# todo: 3，函数可作为参数
# 高阶函数 show()
def show(func):
    size = func('python')
    print('length of string is: %s' % size )
show(foo)  # length of string is: 6

# todo :4，函数可以作为返回值
# 高阶函数 nick()
def nick():
    return foo
print(nick())  # <function foo at 0x0000014962E9F040>
a = nick()
print(a('python'))   # 6
print(nick()("python"))    # 6

# todo: 高阶函数map，map接受一个函数和一个迭代对象作为参数，调用时，一次迭代把迭代对象的元素作为参数条用该函数。
# map() 会根据提供的函数对指定序列做映射
lens = map(foo, ["the", "zen", "of", "python"])
print(id(lens))  # 2132248108528
print(type(lens))  # <类与实例 'map'>
print(lens)  # <map object at 0x000001E327531DF0>  # 返回迭代器
print(list(lens))  # [3, 3, 2, 6]  # 使用 list() 转换为列表
# 等同于 链表推导式，但 map 的运行效率更快一点
print([foo(i) for i in ["the", "zen", "of", "python"]])  # [3, 3, 2, 6]

# todo: 函数可以嵌套，python允许函数中定义函数，这种函数叫嵌套函数
# 函数目的：去除字符串第一个字符后再计算它的长度
def get_length(text):
    def clean(t):
        return t[1:]
    new_text = clean(text)
    return len(new_text)
print(get_length('python'))   # 5


# todo: 实现了 __call__的类也可以作为函数
# 对于一个自定义的类，如果实现了 __call__ 方法，那么该类的实例对象的行为就是一个函数，是一个可以被调用（callable()）的对象
class Add:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        return self.n + x

add = Add(1)
print(add(44))  # 45
print(Add(1)(4))  # 5

# todo: 判断对象是否为可调用对象，使用内置函数callable。
print(callable(foo))  # True
print(callable(1))  # False
print(callable(int))  # True
print(callable(add))  # True
print(callable(get_length))  # True
clean = get_length
print(callable(clean))  # True


