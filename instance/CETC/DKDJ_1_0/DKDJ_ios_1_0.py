# -*- coding:utf-8 -*-
import unittest
import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from time import sleep
import datetime
import random

class MyIOSTests(unittest.TestCase):
    #开启猫宁3.0
    def setUp(self):

        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'platformName': 'iOS',
                'platformVersion': '9.3',
                'deviceName': 'iPhone 6 plus'
            })