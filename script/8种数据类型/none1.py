# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2021-1-18
# Description: None是一个特殊常量，表示空值；
# None与False不同，None不是0，也不是空字符串。
# *******************************************************************

print(type(None))  # <类与实例 'NoneType'> 有自己的数据类型

x = None
if x:
    print(True)
else:
    print(False)  # # False
