# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: mock 应用示例
# pip install mock
# 为什么要使用Mock？
# 之所以使用mock测试，是因为真实场景很难实现或者短期实现起来很困难。主要场景有：
# 真实对象可能还不存在（接口还没有完成开发）
# 真实对象很难搭建起来（第三方支付联调）
# 真实对象的行为很难触发（例如网络错误）
# 真实对象速度很慢（例如一个完整的数据库，在测试之前可能需要初始化）
# 真实对象可能包含不能用作测试（而不是为实际工作）的信息和方法
# 真实的对象是用户界面，或包括用户页面在内
# 真实的对象使用了回调机制
# 真实对象的行为是不确定的（例如当前的时间或当前的温度）

# 如何使用Mock？
# 通过代码制造假的输出（结果）

# todo 执行以下代码前，先开启服务Mock（Mock Server），执行：mock_server.py
# https://blog.csdn.net/qq_73332379/article/details/137682973


# *****************************************************************

from mock import Mock
import unittest,requests

# login接口（假设这个函数开发还没有完成）
def login(url, data):
    """登陆百度账号"""
    res = requests.post(url, data).json()
    print(res)
    return res

class TestLogin(unittest.TestCase):

    """单元测试"""
    def setUp(self) -> None:
        print("case开始执行")
    def tearDown(self) -> None:
        print("case执行结束")


    # 使用mock模拟login接口
    def test_01(self):

        # 1，接口访问的数据
        # 测试数据
        url = "http://127.0.0.1:5000/member/register"
        data = {
            "username": "momo",
            "password": "123456"
        }

        # 2，调用接口login（这里使用Mock）
        # login = Mock(return_value="123") # 模拟返回实际值123 ,当接口开发完成时，把这行代码注释掉即可
        actual = login(url,data)

        # 3，断言（预期值，实际值）
        self.assertEqual({'code': 1, 'msg': 'success'} , actual)

if __name__ == '__main__':
    unittest.main()












