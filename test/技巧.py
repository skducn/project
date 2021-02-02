# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-1-27
# Description   : python技巧
# *****************************************************************
# todo:  python技巧

# 1，unbound变量，选择性赋值
x = 0
mult = 1024 if x else 500
print(mult)

# 2，print不换行
print("123", end="")
print("456")

# 3，python区分大小写（变量名，函数名，类名，模块名称，异常名称）
an=1
# print(An)


# 4，运算符
print(11/2)   # 5.5   / 浮点除法运算符
print(11//2)    # 5    //整数除法运算符
print(-11//2)  # -6    //带负数的四舍五入取整。
print(11.0//2)  # 5.0

# 5，分数
import fractions
x = fractions.Fraction(1, 3)
print(x)  # 1/3
print(type(x))  # <class 'fractions.Fraction'>
print(x*2)  # 2/3



# 6，零值是false， 非零值是true
x = 0.0   # 为假，false
if 0.0 == 0: print("0.0=0")
# x = fractions.Fraction(0, 3)  # 为假
# x = fractions.Fraction(10, 0)  # 报错，分母不能为0
# x = 0.0000000000000000000000000000001   # 为真
if x:
    print("true")
else:
    print("false")



# 7，列表
l_test = ['a']
l_test = l_test + [2.0, 3]   # 连接+赋值，这会消耗大量内存。 所以应该用 list.append() 添加元素
print(l_test)  # ['a', 2.0, 3]
l_test.insert(0, "tt")
print(l_test)  # ['tt', 'a', 2.0, 3]
l_test.extend("abc")
print(l_test)  # ['tt', 'a', 2.0, 3, 'a', 'b', 'c']
l_test.extend(["abc"])
print(l_test)  # ['tt', 'a', 2.0, 3, 'a', 'b', 'c', 'abc']

# 检索列表中元素出现的次数
print(l_test.count("a"))  # 2



# 7，元组是不可变的，元组的速度比列表快，如定义了一系列常量值，只需对他进行遍历，那么请使用元组替代列表。
a, b, c = ("a", 2, True)
print(a)  # a
print(b)  # 2
print(c)  # True

# 内建的range()函数构造了一个整数序列。
(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)
print(SATURDAY)  # 5


# 8,set()返回一个集合
l_test2 = ['a', 'b', 'mpilgrim', True, False, 42]
print(set(l_test2))  # {False, True, 'mpilgrim', 42, 'a', 'b'}   # 列表转集合

l_test3 = (9, 6, 'baidu', True)
print(set(l_test3))  # {9, 'baidu', 6, True}  # 元组转集合

l_test4 = "123"
print(set(l_test4))  # {'1', '2', '3'}  # 字符串打散转集合

l_test5 = {"a": 111, "b": 222}
print(set(l_test5))  # {'b', 'a'}  # 字典key转集合

# 9，子集与超集的关系
a_set= {1, 2, 3}
b_set= {1, 2, 3, 4}
print(a_set.issubset(b_set))   # True        判断b_set是不是a_set的子集
print(b_set.issuperset(a_set))  # True      判断a_set是不是b_set的超集


# 10, None是一个特殊常量，表示空值；None与False不同，None不是0，也不是空字符串。
print(type(None))  # <class 'NoneType'> 有自己的数据类型
# None = None
x = None
if x:
    print(True)
else:
    print(False)
# False










