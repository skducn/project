# coding:utf-8
# import unittest
# from macaca import WebDriver
# import time
# 
# desired_caps = {
#     'browserName': 'Chrome', #Chrome', # Electon, Safari(iOS).
#     'platformName': 'Desktop', # iOS, Android.
#     # 'platformVersion': '*',
#     'autoAcceptAlerts': True
# }
# 
# server_url = 'https://www.baidu.com/'
# driver = WebDriver(desired_caps)
# driver.init()
# driver.maximize_window()
# driver.get(server_url)
# driver.element_by_id("kw")
# driver.send_keys("macaca")
# driver.element_by_id("su").click()
# print driver.title
# driver.wait_for_element('id','head')
# driver.close()


from macaca import WebDriver, WebElement

# Configure the desired capabilities.
desired_caps = {
    'autoAcceptAlerts': True,
    'browserName': 'Electon',
    'platformName': 'desktop'
}

driver = WebDriver(desired_caps)

# Start the WebDriver session
driver.init()

# Support fluent API
driver.set_window_size(1280, 800).get("https://www.google.com")

# Get WebElement instance through element_by_* APIs.
web_element = driver.element_by_id("lst-ib")
print(type(web_element))
# macaca.webelement.WebElement

# WebElement include methods such as send_keys, click, get_attribute and etc.
web_element.send_keys("macaca")
web_element = driver.element_by_name("btnK")
web_element.click()

# WebDriver also has some properties like source, title and current_url.
html = driver.source
print('Does Macaca exist: ', 'macaca' in html)
# Does Macaca exist: True
title = driver.title
print(title)