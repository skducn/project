# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest练习
# 显示安装包版本，pip3 show pytest , 目前是5.3.5
# https://www.jianshu.com/p/b07d897cb10c
# Full pytest documentation   https://docs.pytest.org/en/stable/contents.html#toc
# ********************************************************************************************************************
# 生效范围
#
# session: 会话级, 所有执行的用例 , 只执行1次。
# package: 包级, 当前包所有执行的用例
# module: 模块级，
# class: 类级，方法与类前执行1次
# function: 方法级，所有方法前执行1次。

import pytest

@pytest.fixture(scope="function")
def start():
    print("\n-----start-----")

# 1，当单个用例需要调用fixture时，可直接在用例里加fixture参数，如 def test_a(start)
def test_a(start):
    print("执行a")

# 2，也可以给class中每一个用例加各自的fixture参数。
class Test_aaa():
    def test_01(self, start):
        print("用例01")

    def test_02(self, start):
        print("用例02")

if __name__ == '__main__':
    pytest.main(["-s","test_3.py"])