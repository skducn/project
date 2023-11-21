# # coding: utf-8
# # ********************************************************************************************************************
# # Author     : John
# # Date       : 2020-10-27
# # Description: pytest
# # 显示安装包版本，pip3 show pytest , 6.1.1
# # https://www.jianshu.com/p/b07d897cb10c  Pytest基础使用教程
# # Full pytest documentation   https://docs.pytest.org/en/stable/contents.html#toc
# # pytest参数列表，https://www.cnblogs.com/wtfm/p/10824461.html
# # https://www.pythonf.cn/read/21629   构建pytest+allure环境并记录问题,搭建,pytestallure
# # https://pan.baidu.com/s/1YkgYpvfmH_I26ZPAJ1OF0A#list/path=%2Fallure%E5%91%BD%E4%BB%A4%E8%A1%8C%E5%B7%A5%E5%85%B7   allure-commandline-2.12.1.zip
# # 安装allure命令行工具
# # pip3 install pytest-allure
# # 下载地址：https://pan.baidu.com/s/1YkgYpvfmH_I26ZPAJ1OF0A
# # 把解压后的allure文件夹放到根目录，并添加到环境变量，把allure文件下的bin目录添加到系统环境变量的PATH下。
# # 检查allure是否安装成功
# # 在DOS窗口输入allure --version，如果能正确展示安装版本即为安装成功。
# # ********************************************************************************************************************
# import pytest
#
# @pytest.fixture(scope="session",autouse=True)
# def login():
#
#
# # @pytest.fixture(scope='function')
# # def setup_function(request):
# #     def teardown_function():
# #         print("teardown_function called!")
# #     request.addfinalizer(teardown_function)
# #     print("\nsetup_function called!")
# #
# # @pytest.fixture(scope='module')
# # def setup_module(request):
# #     def teardown_module():
# #         print("teardown_module called!")
# #     request.addfinalizer(teardown_module)
# #     print("setup_module called!")
#
# # def test_1(setup_function):
# #     print("test_1 called!")
# #
# # def test_2(setup_module):
# #     print("test_2 called!")
# #
# # def test_3(setup_module):
# #     print("test_3 called!")
# #
# # def test_4(setup_function):
# #     print("test_4 called!")
# #
# # def func(x):
# #     return x+1
# #
# # def test_func():
# #     assert func(3) == 5
#
#
# # @pytest.fixture()
# # def user(x=100):
# #     print(123+x)
# #     return 88
# #
# # def test_user(user):
# #     print(user)
#
# # names = ["羡鱼", "abc123", "admin@123.com"]
# # @pytest.mark.parametrize("name", names)
# # def test_user_reg(name): # 接收的变量名要和parametrize的"name"一致
# #     print(name)
#
# # 类与实例 TestClass:
# #     def test_one(self):
# #         x = "this"
# #         assert 'h' in x
# #
# #     def test_two(self):
# #         x = "hello"
# #         assert hasattr(x,"check")
#
#     # def test1():
# #     print('test_numbers_3_4  <============================ actual test code')
# #     assert 3 * 4 == 12
# #
# # def test4():
# #     print('test_strings_a_3  <============================ actual test code')
# #     assert 4 == 44
# #
# # def test2():
# #     print('test_strings_a_3  <============================ actual test code')
# #     assert 4 == 4
# #
# # def test3():
# #     print( 'test_strings_a_3  <============================ actual test code')
# #     assert 4 == 4
# #
# # if __name__ == '__main__':
# #     pytest.main(["-s","test_1.py"])