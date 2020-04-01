# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: python  if __name__ == '__main__': 的解析
# ********************************************************************************************************************

# 当你打开一个.py文件时, 经常会在代码的最下面看到if __name__ == '__main__'
# 模块是对象，并且所有的模块都有一个内置属性__name__。一个模块的__name__的值取决于您如何应用模块。如果
# import 一个模块，那么模块__name__的值通常为模块文件名，不带路径或者文件扩展名。但是您也可以像一个标准的程序样直接运行模块，在这
# 种情况下, __name__的值将是一个特别缺省"__main__"。


# 1，在cmd中直接运行.py文件, 则__name__的值是 '__main__';
# 2，而在import 一个.py文件后, __name__的值就不是'__main__'

# 从而用if __name__ == '__main__' 来判断是否是在直接运行该.py文件

# Test.py
class Test:
    def __init(self): pass
    def f(self):
        print('Hello, World!')

if __name__ == '__main__':
    Test().f()


# 在cmd中输入:
# C: > python Test.py
# Hello, World!
# 说明: "__name__ == '__main__'" 是成立的

# 你再在cmd中输入:
# C: > python
# >> > import Test
# >> > Test.__name__  # Test模块的__name__
# 'Test'
# >> > __name__  # 当前程序的__name__
# '__main__'
# 无论怎样, Test.py中的 "__name__ == '__main__'"都不会成立的!




