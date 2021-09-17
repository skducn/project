# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 conftest.py 测试用例的前置条件可以使用fixture实现

# 问题：如果我们在编写测试用的时候，每一个测试文件里面的用例都需要先登录后才能完成后面的操作，那么们该如何实现呢？

# conftest 应用中需要结合fixture，即fixture中参数scope也适用conftest中fixture的特性：
# 1.@pytest.fixture(scope="session")，参数为session时，则先执行一次，再执行所有的测试文件。
# 2.@pytest.fixture(scope="module")，参数为module时，则在每个测试文件前执行一次
# 3.@pytest.fixture(scope="class")，参数为class时，则在每个测试文件中的类前执行一次，如果没有类则执行scope=function
# 4.@pytest.fixture(scope="function")，参数为function时，则在每个测试文件的函数前执行一次

# 总结：
# 1.conftest.py文件名字是固定的，不可以做任何修改
# 2.文件和用例文件在同一个目录下，那么conftest.py作用于整个目录
# 3.conftest.py文件所在目录必须存在__init__.py文件
# 4.conftest.py文件不能被其他文件导入
# 5.所有同目录测试文件运行前都会执行conftest.py文件
# ********************************************************************************************************************

import pytest

@pytest.fixture(scope="class")
def login():
    print('\n login in conftest.py -----------')

@pytest.fixture()
def user(x=100):
    print(123+x)
    return 88

def test_user(user):
    print(user)


if __name__ == '__main__':
    pytest.main(["-vs"])

# 或在命令行执行： pytest -vs
