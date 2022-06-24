# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2022-6-24
# Description: 自动操作 GUI 神器——PyAutoGUI
# http://www.51testing.com/html/08/n-7789608.html
# ***************************************************************


import pyautogui

# pyautogui.moveTo(200,400,duration=0.5)
#
# pyautogui.moveRel(200,500,duration=2)
# print(pyautogui.position())  # Point(x=400, y=900)

pyautogui.click(100,300,button='right')


# class DataPO():
#
#
#     def getRandomInt(self, varEndInt, varNum):
#         # random.sample()生成不相同的随机数
#         return random.sample(range(1, varEndInt), varNum)
#
#
# if __name__ == '__main__':
#
#     Data_PO = DataPO()
#
#     # print("1 随机生成中文用户名".center(100, "-"))
#     # print(Data_PO.getChineseName())  # 陈恋柏
