# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest
# 显示安装包版本，pip3 show pytest , 6.1.1
# https://www.jianshu.com/p/b07d897cb10c
# Full pytest documentation   https://docs.pytest.org/en/stable/contents.html#toc
# pytest参数列表，https://www.cnblogs.com/wtfm/p/10824461.html
# https://www.pythonf.cn/read/21629   构建pytest+allure环境并记录问题,搭建,pytestallure
# https://pan.baidu.com/s/1YkgYpvfmH_I26ZPAJ1OF0A#list/path=%2Fallure%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7   allure-commandline-2.12.1.zip
# ********************************************************************************************************************

# 层级关系：
# 1.用例：setup/teardown
# 2.类套件：setup_class/teardown_class
# 3.模块套件：setup_module/teardown_module

import pytest


# def test_case01():
#     print("执行函数级第一条测试用例")
#     num = 1
#     assert 1 == num#进行用例结果判断
#
# def test_case02():
#     print("执行函数级第二条测试用例")


#类套件测试用例
class Test_login():
    #类套件初始化
    def setup_class(self):#只会在类执行前执行一次
        print("类初始化开始操作：打开浏览器")
    def teardown_class(self):
        print("类初始化清除操作：关闭浏览器")

    #函数初始化操作
    #pytest规则：入口写法：
    def setup(self):#每一条测试用例在执行的时候都会先执行一次这个
        print("窗口的打开")

    # pytest规则：结束写法：
    def teardown(self):
        print("窗口的关闭")

    #测试用例开始
    def test_case01(self):
        print("执行第01条登录测试用例")
        a = 3
        assert 3 == a

    def test_case02(self):
        print("执行第02条登录测试用例")

#用例的执行 -s 表示输出用例里面的打印，静默输出
#第一种方式：在DOS窗口移动到测试文件路径: pytest 文件名.py -s 来执行
#第二种方式：如果文件是以test开头，直接执行 pytest -s
#第三种方式：直接在代码里写执行入口:
# if __name__ == '__main__':
#     pytest.main(['test.py','-s'])


if __name__ == '__main__':
    pytest.main(['test_process.py','-s'])#代码内执行