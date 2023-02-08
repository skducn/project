# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-30
# Description: imutils包可以很简洁的调用opencv接口，轻松实现图像的平移，旋转，缩放，骨架化等操作
# *****************************************************************


# 2.1 图像平移

import numpy as np
import cv2 as cv
import imutils
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


img = cv.imread('test.jpg')  # 更改图片地址
translated = imutils.translate(img,10,10)  # 平移函数

plt.figure()
plt.subplot(121)
# plt.axis('off')  # 去掉坐标轴
plt.imshow(img[:,:,::-1])  # img[:,:,::-1]转换是为了转回RGB格式，这样才可以正常显示彩色图像
# plt.title('原图')

plt.subplot(122)
# plt.axis('off')  # 去掉坐标轴
plt.imshow(translated[:,:,::-1])
# plt.title('平移结果')
# plt.show()

plt.savefig("test100_50.jpg")# 保存图⽚完整







