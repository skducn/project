# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2017-11-10
# Description: selenium & geckodriver 安装、用法、常见问题
#****************************************************************


from selenium import webdriver
driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
assert "百度一下" in driver.title
browser.close()

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
inputElement = driver.find_element_by_id("kw")
inputElement.send_keys("beyond")
inputElement.submit()
print(driver.title)
try:
   WebDriverWait(driver, 10).until(lambda driver : driver.title.lower().startswith("beyond"))
   print(driver.title)
finally:
  pass