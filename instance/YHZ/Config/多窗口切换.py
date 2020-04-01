# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2017-6-14
# Description: 浏览器多窗口切换
#***************************************************************

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
from time import sleep

# 【Webdriver驱动】
driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver5.log')
driver.implicitly_wait(10)

# 第一个窗口 baidu
driver.get("http://www.baidu.com")

# 获得百度搜索窗口句柄
sreach_windows = driver.current_window_handle

# 第二个窗口 taobao
js = 'window.open("http://www.taobao.com");'
driver.execute_script(js)

# 第三个窗口 jd
js = 'window.open("http://www.jd.com");'
driver.execute_script(js)

# 获得所有打开的窗口句柄
all_handles = driver.window_handles
print all_handles   # [u'2147483649', u'2147483653', u'2147483656']


# 切换到最近打开的窗口 jd
driver.switch_to_window(all_handles[-1])
sleep(5)

# 切换到中间打开的窗口 taobao
driver.switch_to_window(all_handles[1])
sleep(5)

# 切换到第一个打开的窗口 baidu
driver.switch_to_window(all_handles[0])
sleep(6)

print "end "

# #进入注册窗口
# for handle in all_handles:
#     if handle !=sreach_windows:
#         driver.switch_to_window(handle)
#         print ('now register window!')
#         # driver.find_element_by_name("phone").send_keys('15143049892')
#         # driver.find_element_by_name("password").send_keys('password')

# #回到搜索窗口
# for handle in all_handles:
#     if handle==sreach_windows:
#         driver.switch_to_window(handle)
#         print ('no sreach window!')
#         # driver.find_element_by_id('TANGRAM__PSP_2__closeBtn').click()
#         # driver.find_element_by_id("kw").send_keys("selenium")
#         # driver.find_element_by_id("su").click()
#         time.sleep(2)
#
# driver.quit()