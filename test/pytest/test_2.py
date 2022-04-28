# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 use fixture
# 显示安装包版本，pip3 show pytest , 目前是5.3.5
# https://www.jianshu.com/p/b07d897cb10c
# Full pytest documentation   https://docs.pytest.org/en/stable/contents.html#toc
# Pytest学习之use fixtures  https://www.cnblogs.com/nuonuozhou/p/10429846.html
# ********************************************************************************************************************

'''
1，当单个用例需要调用fixture时，可直接在用例里加fixture参数，如 def test_a(start)
2，也可以给class中每一个用例加各自的fixture参数。
3，如果class中所有用例都使用同一个fixture参数的话，最方便的是使用@pytest.mark.usefixtures()装饰器，让整个class都调用fixture
'''

import pytest

@pytest.fixture(scope="module")
def start():
    print("\n-----start-----")

@pytest.fixture(scope="function")
def end():
    print("\n-----end-----")

# 1，当单个用例需要调用fixture时，可直接在用例里加fixture参数，如 def test_a(start)
def test_a(start):
    print("执行a")

# 2，也可以给class中每一个用例加各自的fixture参数。
class Test_aaa():
    def test_01(self, end):
        print("用例01")

    def test_02(self, start):
        print("用例02")

# 3，如果class中所有用例都使用同一个fixture参数的话，最方便的是使用@pytest.mark.usefixtures()装饰器，让整个class都调用fixture
@pytest.mark.usefixtures("start")
class Test_bbb():
    def test_01(self):
        print("用例03")

    def test_02(self):
        print("用例04")

if __name__ == '__main__':
    pytest.main(["-s","test_2.py"])