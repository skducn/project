#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Created on : 2024-8-5
# Description: 使用exec()动态执行代码字符串
#****************************************************************

code = """
class MyClass:
    def say_hello(self):
        print("Hello from MyClass")
        """

exec(code)
my_instance = MyClass()
my_instance.say_hello()  # Hello from MyClass