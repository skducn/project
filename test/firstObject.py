# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-1-27
# Description   : python函数是第一类对象（First-Class Object）
# http://www.360doc.com/content/17/1021/04/7210702_696800981.shtml
# 函数作为第一类对象是python函数的一大特性
# 在python中万物皆是对象，函数也不例外，函数可作为对象赋值给一个变量、可作为元素添加到集合对象中、可作为参数值传递给其他函数，还可以做函数返回值，这些特性就是第一类对象所特有的。
# *****************************************************************

# 一个简单函数实例
def foo(text):
    return len(text)
print(foo('zen of python'))


# 函数是对象，拥有对象模型的三个通用属性：id、类型、值
print(id(foo))   # 1632628305984
print(type(foo))  # <class 'function'>
print(foo)  # <function foo at 0x000001C3F7F8F040>



# 1，函数可作为对象赋值给一个变量
bar = foo     # 赋值给另一个变量时，函数不会被调用，仅仅是在函数对象上绑定了一个新的名字而已。
print(bar('zhiying'))   # 7
apple = bar   # 本质上这些变量最终指向的都是同一个函数对象
print(apple('苹果'))   # 2



# 2，函数作为元素存储在容器对象中（list、dict、set等）
funcs = [foo, str, len]
for f in funcs:
    print(f('hello'))
# 5
# hello
# 5
print(funcs[0])  # <function foo at 0x0000022349F5F040>
print(funcs[0]("test"))  # 4



# 3，函数可作为参数
def show(func):
    size = func('python')
    print('length of string is: %s' % size )
show(foo)  # length of string is: 6



# 4，函数可以作为返回值
def nick():
    return foo
print(nick())  # <function foo at 0x0000014962E9F040>
print(nick()("python"))    # 6



# 5，高阶函数map，map接受一个函数和一个迭代对象作为参数，调用时，一次迭代把迭代对象的元素作为参数条用该函数。
# map() 会根据提供的函数对指定序列做映射
lens = map(foo, ["the", "zen", "of", "python"])
print(id(lens))  # 2132248108528
print(type(lens))  # <class 'map'>
print(lens)  # <map object at 0x000001E327531DF0>  # 返回迭代器
print(list(lens))  # [3, 3, 2, 6]  # 使用 list() 转换为列表
# 等同于 链表推导式
print([foo(i) for i in ["the", "zen", "of", "python"]])  # [3, 3, 2, 6]
# 只不过 map的运行效率更快一点


# 6，函数可以嵌套，python允许函数中定义函数，这种函数叫嵌套函数
# 去除字符串第一个字符后再计算它的长度
def get_length(text):
    def clean(t):
        return t[1:]
    new_text = clean(text)
    return len(new_text)
print(get_length('python'))   # 5


# 7，实现了 __call__的类也可以作为函数
# 对于一个自定义的类，如果实现了 __call__ 方法，那么该类的实例对象的行为就是一个函数，是一个可以被调用（callable()）的对象
class Add:
    def __init__(self,n):
        self.n = n
    def __call__(self, x):
        return self.n + x

add = Add(1)
print(add(44))  # 45



# 8，判断对象是否为可调用对象，使用内置函数callable判断。
print(callable(foo))  # True
print(callable(1))  # false
print(callable(int))  # True
print(callable(add))  # True
print(callable(get_length))  # True
clean = get_length
print(callable(clean))  # True


