# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:  滑动验证码
# *****************************************************************

from PO.WebPO import *
Web_PO = WebPO("chrome")

Web_PO.openURL("https://kyfw.12306.cn/otn/resources/login.html")
Web_PO.setTextById("J-userName", "18510000000")
Web_PO.setTextById("J-password", "123456")
Web_PO.clk('J-login')

# 定位滑块元素
h = Web_PO.find_element_by_css_selector(".slide-captcha-img")
action = ActionChains(Web_PO)
# 执行操作
action.click_and_hold(h).perform()  # 按住滑块
# 查看滑块的长度，如340 ， 340/4 = 85 ， 即向右滑动4次
action.move_by_offset(85,0)  # 向右移动85像素
action.move_by_offset(85,0)
action.move_by_offset(85,0)
action.move_by_offset(85,0)
# 释放
action.release().perform()







