# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest 之 conftest.py
# 问题：如果我们在编写测试用的时候，每一个测试文件里面的用例都需要先登录后才能完成后面的操作，那么们该如何实现呢？这就需要我们掌握conftest.py文件的使用
# conftest文件实际应用中需要结合fixture来使用，那么fixture中参数scope也适用conftest中fixture的特性，这里再说明一下
# 1.conftest中fixture的scope参数为session，那么所有的测试文件执行前执行一次
# 2.conftest中fixture的scope参数为module，那么每一个测试文件执行前都会执行一次conftest文件中的fixture
# 3.conftest中fixture的scope参数为class，那么每一个测试文件中的测试类执行前都会执行一次conftest文件中的fixture
# 4.conftest中fixture的scope参数为function，那么所有文件的测试用例执行前都会执行一次conftest文件中的fixture
# 总结：实际工作中不仅仅只有函数使用，也往往不仅存在一个conftest.py文件
# 1.conftest.py文件名字是固定的，不可以做任何修改
# 2.文件和用例文件在同一个目录下，那么conftest.py作用于整个目录
# 3.conftest.py文件所在目录必须存在__init__.py文件
# 4.conftest.py文件不能被其他文件导入
# 5.所有同目录测试文件运行前都会执行conftest.py文件
# ********************************************************************************************************************

import pytest

@pytest.fixture()
def login():
    print('\n login in conftest.py -----------')

