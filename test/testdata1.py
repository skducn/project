# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-9-18
# Description: 使用Hypothesis生成测试数据
# http://www.51testing.com/html/51/n-4462451.html
# pip install hypothesis
# *****************************************************************

import unittest
from random import randint
from hypothesis import given, settings
import hypothesis.strategies as st

def add(a, b):
    return a + b

# @setting()装饰器中通过 max_examples 管理随机数的个数
# @given() 装饰测试用例，调用strategies 模块下面的 integers() 方法生成随机的测试数。
class Testdata1(unittest.TestCase):
    @settings(max_examples=10)
    @given(a=st.integers(), b=st.integers())
    def test_case(self, a, b):
        print("a->", a)
        print("b->", b)
        c1 = a + b
        c2 = add(a, b)
        self.assertEqual(c1, c2)
if __name__ == '__main__':
    unittest.main()


# # 通过调用 randint() 函数生成随机数。循环10次（也可以是100次，1000次），用更少的代码做更多的测试，测试的数据越多，发现bug的可能性越大。
# class AddTest(unittest.TestCase):
#     def test_case(self):
#         for i in range(10):
#             a = randint(-32768, 32767)
#             b = randint(-32768, 32767)
#             print("a->", a)
#             print("b->", b)
#             c1 = a + b
#             c2 = add(a, b)
#             self.assertEqual(c1, c2)
#
# if __name__ == '__main__':
#     unittest.main()

