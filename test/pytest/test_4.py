# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 use fixture
# 显示安装包版本，pip3 show pytest 6.1.1
# https://www.jianshu.com/p/b07d897cb10c
# Full pytest documentation   https://docs.pytest.org/en/stable/contents.html#toc
# ********************************************************************************************************************

'''
叠加fixture
如果class用例需要同时调用多个fixture，可以使用@pytest.mark.usefixtures()叠加。注意叠加顺序，先执行的放底层，后执行的放上层
'''

# usefixtures与传fixture区别
# 通过上面2个案例，对usefixtures使用基本方法已经掌握了，但是你会发现，我上面给的2个案例的fixture是没有返回值的。如果fixture有返回值，那么usefixtures就无法获取到返回值了，这个是它与用例直接传fixture参数的区别。
# 也就是说当fixture用return值需要使用时，只能在用例里面传fixture参数了。
# 当fixture没有return值的时候，两种方法都可以。

import time
import pytest

@pytest.fixture(scope="function")
def first():
    print("第一步：操作aaa")

@pytest.fixture(scope="function")
def second():
    print("第二步：操作bbb")

@pytest.mark.usefixtures("second")  # 后执行
@pytest.mark.usefixtures("first")  # 先执行
class TestFix():
    def test_1(self):
        print("用例1")
        assert 1==1

    def test_2(self):
        print("用例2")
        assert 2==2

if __name__ == '__main__':
    pytest.main(["-s","test_4.py"])