# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2017-6-14
# Description: 浏览器多窗口切换
#***************************************************************

from selenium import webdriver
from time import sleep
driver = webdriver.Firefox()
driver.implicitly_wait(2)

driver.get("http://www.baidu.com")
baidu_handle = driver.current_window_handle   # 2147483649
driver.execute_script('window.open("http://www.taobao.com");')  # 2147483656
driver.execute_script('window.open("http://www.jd.com");')  # 2147483653

# 获得所有打开的窗口句柄
all_handles = driver.window_handles

print(all_handles)   # [u'2147483649', u'2147483653', u'2147483656']
print(all_handles[0])  # 2147483649 baidu
print(all_handles[1])  # 2147483653 jd
print(all_handles[2])  # 2147483656 taobao

# 切换taobao
sleep(5)
driver.switch_to.window(all_handles[2])

# 切换到baidu
sleep(5)
driver.switch_to.window(all_handles[0])

# 切换到jd
sleep(5)
driver.switch_to.window(all_handles[1])
sleep(6)
