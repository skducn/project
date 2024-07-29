# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-7-29
# Description: saas
# pip install minium
#  基于unittest微信自己封装的框架
# https://minitest.weixin.qq.com/#/minium/Python/introduction/selector
# {
# "dev_tool_path": "/Applications/wechatwebdevtools.app/Contents/MacOS/cli",
# //"project_path": "/Users/linghuchong/Downloads/myGitLab/saas/doctor/test/saas-ecg-doctor-wechat"
# "project_path": "/Users/linghuchong/Downloads/myGitLab/SHthin/patient/test/saas-shthin-patient-wechat"
# }
# *****************************************************************

import minium

class TestMain(minium.MiniTest):
    # 每个测试用例，用一个方法单独的封装
    def test_01(self):
        a = self.page.get_element("text[class='iconfont icon-yuanquan1']")  # 阅读并同意
        a.click()
        b = self.page.get_element("button[@bindtap='bindGetUserInfo']")  # 微信登录
        b.click()
        c = self.page.get_element("button[@bindtap='getUserProfile']")  # 允许
        c.click()
        # self.page.get_element("input[placeholder='请输入密码']")
        # a = self.page.get_element("view#custom-class van-icon van-icon-success")
        # a.click()

