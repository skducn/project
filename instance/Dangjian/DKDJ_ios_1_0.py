# # -*- coding:utf-8 -*-
# import unittest
# import os
# from appium import webdriver
# from appium.webdriver.common.touch_action import TouchAction
# from time import sleep
# import datetime
# import random
#
# class MyIOSTests(unittest.TestCase):
#     #开启猫宁3.0
#     def setUp(self):
#
#         self.driver = webdriver.Remote(
#             command_executor='http://127.0.0.1:4723/wd/hub',
#             desired_capabilities={
#                 'platformName': 'iOS',
#                 'platformVersion': '9.3',
#                 'deviceName': 'iPhone 6 plus'
#             })



# -*- coding: utf-8 -*-
# 步骤：
# 1、打开appium2
# 2、xcodebuild -project WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination 'id=405537558ee589296b8180e4d6312a1582fe9179' test

from time import sleep
from appium import webdriver

desired_caps = {}
desired_caps['automationName'] = 'XCUITest'  # Xcode8.2以上无UIAutomation,需使用XCUITest
desired_caps['platformName'] = 'iOS'
desired_caps['platformVersion'] = '10.3.3'
desired_caps['deviceName'] = 'SKiPhone'
desired_caps['bundleId'] = 'com.cetc.partybuilding'             #'需要启动的bundle id, 去问开发者'
# desired_caps['bundleId'] = 'com.cetc.Community.Patient'             #'需要启动的bundle id, 去问开发者'


desired_caps['udid'] = '405537558ee589296b8180e4d6312a1582fe9179'   #真机的udid 可在Xcode或iTunes里查看'
# desired_caps['newCommandTimeout'] = 3600  # 1 hour

# 打开Appium服务器，start server后，尝试启动被测App
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
print "121212121"
sleep(4)
# 学习计划
driver.find_element_by_id("com.cetc.partybuilding:id/learn_plan").click()
sleep(12)

driver.quit()