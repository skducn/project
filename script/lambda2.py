# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-12-19
# Description: 匿名函数 lambda：是指一类无需定义标识符（函数名）的函数或子程序。
# lambda 函数可以接收任意多个参数 (包括可选参数) 并且返回单个表达式的值。
# 要点：
# 1，lambda 函数不能包含命令，
# 2，包含的表达式不能超过一个。
# 格式： 函数对象地址 = lambda 参数列表 : 表达式 ， lambda返回值是一个函数的地址，也就是函数对象。
# 用途：一般将它用在需要封装特殊的、非重用代码上，避免令代码充斥着大量单行函数。

# 参数列表如：
# a,b
# a=1,b=2
# *args
# **kwargs
# a,b=1,*args
# 空
# ....

# 参数表达式如：
# 1
# None
# a+b
# sum(a)
# 1 if a >10 else 0
# ......
# ********************************************************************************************************************


p = lambda x, y: x+y
p(1, 4)     # 注意：这样是可以执行的，不会报错，只是没有print的话不会输出结果。
print(p(1, 4))   # 5

a = lambda x, y, z: (x+8) * y - z
print(a(5, 6, 8))   # 70
print(a)  # <function <lambda> at 0x000001F75FE0E160>

# 在匿名函数后面直接传递实参
print((lambda x: x**2)(3))  # 9

# 将lambda函数作为参数传递给其他函数比如说结合map、filter、sorted、reduce等一些Python内置函数使用
# filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
x = filter(lambda x: x % 3 == 0, [1, 2, 3, 4, 5, 6])
print(list(x))  # [3, 6]

# https://www.cnblogs.com/lincappu/p/8179475.html
# map() 会根据提供的函数对指定序列做映射。
# 当seq只有一个时，将函数func作用于这个seq的每个元素上，并得到一个新的seq
squares = map(lambda x: x ** 2, range(5))
print(list(squares)) # [0,1,4,9,16]
# 当seq多于一个时，map可以并行（注意是并行）地对每个seq执行
x = map(lambda s:s[0:1].upper()+s[1:].lower(),['adam', 'LISA', 'barT'])
print(list(x))  # ['Adam', 'Lisa', 'Bart']





# # 输入编号，返回相应内容
# '''
# 输入1，计算10+2，返回12
# 输入2，计算10-2，返回8
# 输入3，计算10*2，返回20
# 输入其他数字，退出程序，否则循环提示输入信息
# '''
#
# tips = "1 : +\n2 : -\n3 : *\nother to quit\n"
#
# d1 = {
#     '1': lambda x, y: x + y,
#     '2': lambda x, y: x - y,
#     '3': lambda x, y: x * y}
#
# if __name__ == '__main__':
#     while True:
#         print(tips)
#         inputInfo = input('Input : ')
#         if inputInfo not in d1:
#             break
#         print(d1[inputInfo](10, 2), "\n")

