# coding=utf-8
# # ***************************************************************
# Author :John
# Created on : 2023-7-19
# Description: demo
# https://chromedriver.storage.googleapis.com/index.html
# # ***************************************************************

# from PO.SysPO import *
# Sys_PO = SysPO()
# Sys_PO.clsApp("Google Chrome")


import re, subprocess, requests, os
from webdriver_manager.chrome import ChromeDriverManager
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

chromeBrowserVer = subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version", shell=True)
chromeBrowserVer = bytes.decode(chromeBrowserVer)
# print(chromeBrowserVer)  # Google Chrome 114.0.5735.198
chromeBrowserFirstVersion = (chromeBrowserVer.split('Google Chrome ')[1].split(".")[0])  # 114
resp = requests.get(url="https://chromedriver.storage.googleapis.com/")
content = resp.text
if os.name == "nt":
    chromeDriverVer = re.search(f"<Contents><Key>({chromeBrowserFirstVersion}\.\d+\.\d+\.\d+)/chromedriver_win32\.zip</Key>.*?", content, re.S)
    chrome_driver_path = ChromeDriverManager(driver_version=chromeDriverVer.group(1)).install()  # 自动下载与之匹配的chromedriver驱动
    print(chrome_driver_path)
    if os.path.isfile('??/Users/linghuchong/.wdm/drivers/chromedriver/win32/' + chromeDriverVer.group(1) + '/chromedriver'):
        chrome_driver_path = '??/Users/linghuchong/.wdm/drivers/chromedriver/win32/' + chromeDriverVer.group(1) + '/chromedriver'
    else:
        print('download chromedriver ...')
        chrome_driver_path = ChromeDriverManager(driver_version=chromeDriverVer.group(1)).install()  # 自动下载与之匹配的chromedriver驱动
elif os.name == 'posix':
    chromeDriverVer = re.search(f"<Contents><Key>({chromeBrowserFirstVersion}\.\d+\.\d+\.\d+)/chromedriver_mac64\.zip</Key>.*?", content, re.S)
    # print(chromeDriverVer.group(1))  # 114.0.5735.16
    if os.path.isfile('/Users/linghuchong/.wdm/drivers/chromedriver/mac64/' + chromeDriverVer.group(1) + '/chromedriver'):
        chrome_driver_path = '/Users/linghuchong/.wdm/drivers/chromedriver/mac64/' + chromeDriverVer.group(1) + '/chromedriver'
    else:
        print('download chromedriver ...')
        chrome_driver_path = ChromeDriverManager(driver_version=chromeDriverVer.group(1)).install()  # 自动下载与之匹配的chromedriver驱动

driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
<<<<<<< HEAD
from WebPO import *
=======
from PO.WebPO import *
>>>>>>> origin/master
Web_PO = WebPO(driver)

class DemoPO():

    def open(self, url):
        Web_PO.opn(url)
        # x = Web_PO.getTextsAndAttrs("//div[@id='s-top-left']/a","href")
        # print(x)


if __name__ == "__main__":
    D = DemoPO()
    D.open("http://www.baidu.com")