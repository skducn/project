# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/4/13 12:30
# Description: tt.py.py
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# driver.get("http://www.baidu.com")


from selenium import webdriver
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=options)
url = "https://baidu.com"
browser.get(url)
