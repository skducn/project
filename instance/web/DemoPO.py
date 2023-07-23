# coding=utf-8
# # ***************************************************************
# Author :John
# Created on : 2023-7-19
# Description: demo
# https://chromedriver.storage.googleapis.com/index.html
# # ***************************************************************


# from PO.SysPO import *
# Sys_PO = SysPO()
# Sys_PO.closeApp("Google Chrome")
import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
options = Options()
options.add_argument("--start-maximized")
# screen_width, screen_height = pyautogui.size()  # 通过pyautogui方法获得屏幕尺寸
# print(screen_width, screen_height)
# options.add_argument('--window-size=%sx%s' % (screen_width, screen_height))
# options.add_argument('--incognito')  # 无痕隐身模式
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 不显示 chrome正受到自动测试软件的控制的提示
options.add_argument("disable-cache")  # 禁用缓存
# options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块
# options.add_argument(r"--user-data-dir=.\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--disable-extensions")  # 禁用扩展插件的设置参数项
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
# options.headless = True  # 无界面模式
options.add_argument('--no-sandbox')  # 解决文件不存咋的报错
options.add_argument('-disable-dev-shm-usage')  # 解决DevToolsActivePort文件不存咋的报错
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条，因对一些特殊页面
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升速度
driver = webdriver.Chrome(service=Service("/Users/linghuchong/Downloads/51/Python/project/instance/web/chromedriver"), options=options)
# print(driver.capabilities['browserVersion'])  # 浏览器版本
# print(driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # chrome驱动版本
from PO.WebPO import *
Web_PO = WebPO(driver)

class DemoPO():

    def open(self, url):
        Web_PO.opn(url)
        x = Web_PO.getTextsAndAttrs("//div[@id='s-top-left']/a","href")
        print(x)

