# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-19
# Description: fire模块 用来自动生成命令行接口（CLI）
# ********************************************************************************************************************

import fire

fire.Fire([lambda: 'Hello World!', lambda: 'Hello Python!'])
# (py308) localhost-2:命令行 linghuchong$ python 获取对象属性和方法.py 0
# Hello World!
# (py308) localhost-2:命令行 linghuchong$ python 获取对象属性和方法.py 1
# Hello Python!

fire.Fire({'hello': lambda: 'Hello World!'})
# (py308) localhost-2:命令行 linghuchong$ python 获取对象属性和方法.py hello
# Hello World!
