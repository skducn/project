# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 @pytest.fixture() 与 @pytest.mark.usefixtures()

# ********************************************************************************************************************
import pytest

# 实例1：被测函数将fixture作为参数调用，如返回值。
# 分析：fixtureFunc 这个函数就是一个fixture，fixture函数内部可以实现一些初始化操作，支持return返回值。
# 注意：可定义多个相同的fixture，但只处理最后一个fixture
@pytest.fixture()
def fixtureFunc1():
    print("我优先执行")
    return '---------share'

def test_fixture1(fixtureFunc1):
    print('a100 {}'.format(fixtureFunc1))

class TestFixture1(object):
    def test_fixture_class(self, fixtureFunc1):
        print('b200 "{}"'.format(fixtureFunc1))


# # ******************************************
# 实例2：被测函数或者类前使用@pytest.mark.usefixtures('fixture')装饰器装饰
# fixture函数内部可以实现一些初始化操作，但不支持return返回值。
@pytest.fixture()
def fixtureFunc2():
    print('---------share2')

@pytest.mark.usefixtures('fixtureFunc2')
def test_fixture2():
    print('a1')

@pytest.mark.usefixtures('fixtureFunc2')
class TestFixture2(object):
    def test_fixture_class(self):
        print('a2')


if __name__ =='__main__':
    pytest.main(['-s', 'test_fixture.py'])