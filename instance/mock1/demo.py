# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: mock应用示例
# pip3.90 install mock
# *****************************************************************

import mock
import requests
import unittest

url = "www.baidu.com/login"
data = {
    "user_id": "001",
    "password": "caichen"
}

def post_request(url, data):
    """登陆百度账号"""
    res = requests.post(url, data).json()
    return res

class TestLogin(unittest.TestCase):

    """单元测试"""
    def setUp(self) -> None:
        print("case开始执行")
    def tearDown(self) -> None:
        print("case执行结束")

    def test_01(self):
        """模拟数据判断是否正确"""
        # url = "www.baidu.com/login/tieba"
        data = {
            "user_id": "001"
        }
        sucess_test = mock.Mock(return_value=url)
        post_request = sucess_test
        res = post_request
        # self.assertEqual("654321", res())
        self.assertEqual("www.baidu.com/login" ,res())

if __name__ == '__main__':
    unittest.main()












