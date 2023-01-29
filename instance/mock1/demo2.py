# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: mock应用示例
# pip3.90 install mock
# pip3.9 install appium-python-client
# 步骤：
# 1，确定替换对象，如 visit_ustack函数中的send_request。(此接口开发还未完成)
# 2，实例化mock一个对象，设置mock对象的行为，模拟send_request返回值成功200或失败404
# 3，使用mock对象替换掉 client.send_request
# 4，设置检查点，调用client.visit_ustack(), 查看期望值与返回值是否一样。
# 实际情况，可以替换标准库和第三方模块对象，先import，然后替换指定对象。
# *****************************************************************

import mock
import requests
import unittest
import client

def send_request(url):
    r = requests.get(url)
    return r.status_code

def visit_ustack():
    return send_request('http://www.ustack.com')


# 外部模块调用visit_ustack()来访问官网。下面我们使用mock对象在单元测试中分别测试访问正常和访问不正常的情况。

class TestClient(unittest.TestCase):

    def test_success_request(self):
        success_send = mock.Mock(return_value='200')
        client.send_request = success_send      # mock对象，替换 send_request
        self.assertEqual(client.visit_ustack(), '200')  # 检查期望值与返回值是200
        
    def test_fail_request(self):
        fail_send = mock.Mock(return_value='404')
        client.send_request = fail_send
        self.assertEqual(client.visit_ustack(), '404')








