# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2023-7-22
# Description: demo
# pyinstaller -F main.py -p /Users/linghuchong/Downloads/51/Python/project/instance/web
# ***************************************************************

from DemoPO import *
Demo_PO = DemoPO()

Demo_PO.open("http://www.baidu.com")

# import PyQt5.QtWidgets
#
# desktop = PyQt5.QtWidgets.QApplication.desktop()
# screenRect = desktop.screenGeometry()
# width, height = screenRect.width(), screenRect.height()
#
# print("屏幕长：", width)
# print("屏幕宽：", height)


# Web_PO.open("http://www.163.com")
# # Web_PO.openLabel("http://www.jd.com")
# # Web_PO.switchLabel(0)
# # x = Web_PO.getTextsAndAttrs("//div[@id='s-top-left']/a","href")
# # print(x)
#
# x = Web_PO.getBrowserSize()
# print(x)
# print(a)


# Web_PO.close()

