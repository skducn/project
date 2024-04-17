# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Created on : 2018-7-2
# Description: Web 对象层 （selenium 4.4.3）
# pip install opencv_python    // cv2
# ***************************************************************

"""
1.1 打开网站 open()
1.2 打开标签页 openLabel("http://www.jd.com")
1.3 切换标签页 switchLabel(1)
1.4 关闭当前窗口 close()

2.1 获取当前浏览器宽高 getBrowserSize()
2.2 设置浏览器分辨率 setBrowserSize()
2.3 设置浏览器全屏 setBrowserMax()
2.4 缩放页面比率 zoom(20)
2.5 截取浏览器内屏幕 getBrowserScreen()
2.6 页面滚动条到底部 scrollBottom()

3.1 弹出框 popupAlert()
3.2 确认弹出框 confirmAlert("accept", 2)

4.1 关闭浏览器应用 quit()

5.1 app屏幕左移 scrollLeftByApp('1000',9)
5.2 app屏幕右移 scrollRightByApp('1000', 5)
5.3 app屏幕上移 scrollUpByApp('1000', 5)
5.4 app屏幕下移 scrollDownByApp('1000', 5)

元素拖动到可见的元素 scrollIntoView(varXpath)
内嵌窗口中滚动条操作 scrollTopById(varId)
动态加载页面滚动到底部（加载所有数据） dynamicLoadToEnd()
获取验证码 getCode()
"""


from PO.WebPO import *
Web_PO = WebPO("chrome")


# # print("1.1 打开网站".center(100, "-"))
# Web_PO.openURL("https://baijiahao.baidu.com/s?id=1753450036624046728&wfr=spider&for=pc")
Web_PO.openURL("https://kyfw.12306.cn/otn/resources/login.html")
# Web_PO.openURL("https://www.xvideos.com/video76932809/_")
# Xvideos_PO.getInfo("https://www.xvideos.com/video76932809/_")

# # print("1.2 打开标签页".center(100, "-"))
# Web_PO.openLabel("http://www.jd.com")

# # print("1.3 切换标签页".center(100, "-"))
# Web_PO.switchLabel(0)

# print("1.4 获取当前浏览器宽高".center(100, "-"))
# print(Web_PO.getBrowserSize())  # (1536, 824)

# print("1.5 截取浏览器内屏幕".center(100, "-"))
# Web_PO.getBrowserScreen("d:/222333browserScreen.png")

# # print("2.0 指定分辨率浏览器".center(100, "-"))
# Web_PO.setBrowser(1366, 768)

# # print("2.1 全屏浏览器".center(100, "-"))
# Web_PO.maxBrowser()

# # print("2.2 缩放页面比率".center(100, "-"))
# Web_PO.zoom(20)
# Web_PO.zoom(220)

# print("2.3 动态加载页面滚动到底部（加载所有数据）".center(100, "-"))
# Web_PO.openURL('https://www.douyin.com/user/MS4wLjABAAAARzph2dTaIfZG4w_8czG9Yf5YiqHqc7RGXrqUM3fHtBU?vid=7180299495916326181')
# qty = Web_PO.dynamicLoadToEnd('Eie04v01')  # 动态加载页面直到最后一个 类与实例=Eie04v01 ,并返回加载的数量。
# print(qty)
# text = Web_PO.driver.page_source
# text = bs4.BeautifulSoup(text, 'lxml')
# link = text.find_all('a')
# for a in link:
#     href = a['href']
#     if "/video" in href:
#         print("https://www.douyin.com" + href)

# # print("2.4 页面滚动条到底部".center(100, "-"))
# Web_PO.openURL('https://baijiahao.baidu.com/s?id=1753450036624046728&wfr=spider&for=pc')
# sleep(2)
# Web_PO.scrollToEnd(2)

# print("2.5 app屏幕左移".center(100, "-"))
# Web_PO.scrollLeft('1000',9)

# print("2.6 app屏幕右移".center(100, "-"))
# Web_PO.scrollRight('1000', 5)

# print("2.7 app屏幕上移".center(100, "-"))
# Web_PO.scrollTop('1000', 5)

# print("2.8 app屏幕下移".center(100, "-"))
# Web_PO.scrollDown('1000', 5)

# print("2.9 元素拖动到可见的元素".center(100, "-"))
# Web_PO.scrollIntoView(varXpath)

# print("2.10 内嵌窗口中滚动条操作".center(100, "-"))
# Web_PO.scrollTopById(varId)

# # print("3.1 弹出框".center(100, "-"))
# Web_PO.popupAlert("你好吗？")

# # print("3.2 确认弹出框".center(100, "-"))
# Web_PO.confirmAlert("accept", 2)
# Web_PO.confirmAlert("dismiss", 2)
# print(Web_PO.confirmAlert("text", 2))

# print("4.1 关闭当前窗口".center(100, "-"))
# Web_PO.close()
#
# print("4.2 退出浏览器应用".center(100, "-"))
# Web_PO.quit()
