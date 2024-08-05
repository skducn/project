#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 使用inspect模块获取函数签名
# param_name, 参数名
# param.default, 参数默认值
# param.annotation, 注释
# param.kind 参数种类，例如POSITIONAL_OR_KEYWORD表示位置或关键字参数，KEYWORD_ONLY表示仅关键字参数等
# 参考：https://www.jb51.net/python/285751rwz.htm
#****************************************************************

import inspect

# todo 1 获取方法的签名
def example_function(a, c=1, *args, **kwargs):
    pass
signature = inspect.signature(example_function)

# 输出将会是这个函数的签名，包括它的参数名和默认值：
print(signature)  # (a, c=1, *args, **kwargs)

# 如果你想要以可读的方式获取参数的名字和默认值，你可以遍历signature.parameters：
for param_name, param in signature.parameters.items():
    print(param_name, param.default, param.annotation, param.kind)
# a <class 'inspect._empty'> <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
# c 1 <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
# args <class 'inspect._empty'> <class 'inspect._empty'> VAR_POSITIONAL
# kwargs <class 'inspect._empty'> <class 'inspect._empty'> VAR_KEYWORD


# todo 2 获取类中__init__的签名
class MyClass:
    def __init__(self, arg1, arg2="default", *, kwarg1=None):
        pass
sig = inspect.signature(MyClass.__init__)
for param_name, param in sig.parameters.items():
    print(param_name, param.default, param.annotation, param.kind)

# self <class 'inspect._empty'> <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
# arg1 <class 'inspect._empty'> <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
# arg2 default <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
# kwarg1 None <class 'inspect._empty'> KEYWORD_ONLY


