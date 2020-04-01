# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: CMS配置文件
# *****************************************************************

from selenium import webdriver
from Public.PageObject.LevelPO import *
from Public.PageObject.ThirdPO import *

from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(5)
Level_PO = LevelPO(driver)

varURL = "http://172.21.200.54/index.html"   # 登录页

