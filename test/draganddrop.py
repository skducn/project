# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-6-29
# Description: drag and drop for HTML5
# https://stackoverflow.com/questions/29982072/how-to-implement-the-selenium-html5-drag-and-drop-workaround-in-python
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, os, unittest, time, xlwt, xlrd, MySQLdb, json, xlwt, datetime, platform
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
driver = webdriver.Firefox()

# for HTML5 way1 （测试成功）
driver.get('http://the-internet.herokuapp.com/drag_and_drop')
with open("D:\\51\\python\\project\\PO\\js\\drag_and_drop_helper.js") as f:
    js = f.read()
driver.execute_script(js + "$('#column-a').simulateDragDrop({ dropTarget: '#column-b'});")


# # for HTML5 way2 (未测试成功)
# jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"
# driver.get("http://html5demos.com/drag")
# driver.set_script_timeout(30)
# jquery_file = "D:\\51\\js\\jquery_load_helper.js"
# drag_file = "D:\\51\\js\\drag_and_drop_helper.js"
# # load jquery helper
# with open(jquery_file) as f:
#     load_jquery_js = f.read()
# # load drag and drop helper
# with open(drag_file) as f:
#     drag_and_drop_js = f.read()
# # load jquery
# driver.execute_script(load_jquery_js, jquery_url)
# # perform drag&drop
# driver.execute_script(drag_and_drop_js + "$('#one').simulateDragDrop({ dropTarget: '#bin'});")



# for no HTML5 way that using JS （测试成功）
driver.get('http://sahitest.com/demo/dragDropMooTools.htm')
dragger = driver.find_element_by_id('area')  # 被拖拽元素
item1 = driver.find_element_by_xpath('//div[text()="Item 1"]')  # 目标元素1
item2 = driver.find_element_by_xpath('//div[text()="Item 2"]')  # 目标2
item3 = driver.find_element_by_xpath('//div[text()="Item 3"]')  # 目标3
item4 = driver.find_element_by_xpath('//div[text()="Item 4"]')  # 目标4
action = ActionChains(driver)
action.drag_and_drop(dragger, item1).perform()  # 1.移动dragger到目标1
sleep(2)
action.click_and_hold(dragger).release(item2).perform()  # 2.效果与上句相同，也能起到移动效果aaaa
sleep(2)
action.click_and_hold(dragger).move_to_element(item3).release().perform()  # 3.效果与上两句相同，也能起到移动的效果
sleep(2)
# action.drag_and_drop_by_offset(dragger, 361, 207).perform()  # 4.移动到指定坐标
action.click_and_hold(dragger).move_by_offset(361, 207).release().perform()  # 5.与上一句相同，移动到指定坐标

