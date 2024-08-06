#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 使用functools.wraps保持装饰器中的元数据
#****************************************************************


from functools import wraps
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper
@my_decorator
def say_hello(name):
    """Says hello to the given name."""
    # print(f"Hello, {name}!")

print(say_hello.__name__)  # say_hello
print(say_hello.__doc__)  # Says hello to the given name.
