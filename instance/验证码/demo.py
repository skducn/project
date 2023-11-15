# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-11-14
# Description: 验证码
# https://blog.csdn.net/Cameback_Tang/article/details/124247948 Python使用pytesseract进行验证码图像识别
# https://blog.csdn.net/u010698107/article/details/121736386
# *****************************************************************

import pytesseract
from PIL import Image
from pylab import *
from numpy import *
from PIL import ImageFilter
import cv2
import pytesseract

from PO.CaptchaPO import *
Captcha_PO = CaptchaPO()
Captcha_PO.genCaptcha("1.jpg")

# 加载验证码图片
image_path = "1.jpg"  # 替换为实际的图片路径
image = cv2.imread(image_path)

# 将图像转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 对图像进行二值化处理
_, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 去除干扰线
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
clean_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
cv2.imwrite("1.jpg", clean_image)

code = pytesseract.image_to_string("1.jpg")
print("验证码识别结果：", code)

# img = cv.imread('2.gif')
# blur = cv.pyrMeanShiftFiltering(img, sp=10, sr=50)  # sp :定义的漂移物理空间半径大小  sr：定义的漂移色彩空间半径大小
# gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
# ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)  # 1.全局阈值法   THRESH_BINARY：表示小于阈值置0，大于阈值置填充色
# # binary.save('binary.jpg')
# ret.save('ret.jpg')


# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# from PIL import Image,ImageEnhance,ImageFilter
#
# img_name = '2.gif'
# #去除干扰线
# im = Image.open(img_name)
# #图像二值化
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
# data = im.getdata()
# w,h = im.size
# #im.show()
# black_point = 0
# for x in range(1,w-1):
#     for y in range(1,h-1):
#         mid_pixel = data[w*y+x] #中央像素点像素值
#         if mid_pixel == 0: #找出上下左右四个方向像素点像素值
#             top_pixel = data[w*(y-1)+x]
#             left_pixel = data[w*y+(x-1)]
#             down_pixel = data[w*(y+1)+x]
#             right_pixel = data[w*y+(x+1)]
#
#             #判断上下左右的黑色像素点总个数
#             if top_pixel == 0:
#                 black_point += 1
#             if left_pixel == 0:
#                 black_point += 1
#             if down_pixel == 0:
#                 black_point += 1
#             if right_pixel == 0:
#                 black_point += 1
#             if black_point >= 3:
#                 im.putpixel((x,y),0)
#             #print black_point
#             black_point = 0
# # im.show()
# im.save('222.jpg')


# # 加载验证码图片
# image_path = "1.jpg"  # 替换为实际的图片路径
# image = cv2.imread(image_path)
#
# # 将图像转换为灰度图像
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # 对图像进行预处理：去噪、边缘检测和二值化处理
# processed_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
# processed_image = cv2.Canny(processed_image, 50, 150)
# _, processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# # processed_image.s
# cv2.imwrite("222.jpg", processed_image)
#
# # 使用 Tesseract OCR 进行数字识别
# code = pytesseract.image_to_string("666.jpg", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')



# import cv2
# import pytesseract
#
# # 加载验证码图片
# image_path = "2.gif"  # 替换为实际的图片路径
# image = cv2.imread(image_path)
#
# # 将图像转换为灰度图像
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # 对图像进行二值化处理
# _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#
# # 去除干扰线
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# clean_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
# cv2.imwrite("333.jpg", clean_image)
#
# # 使用 Tesseract OCR 进行数字识别
# code = pytesseract.image_to_string(clean_image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
#
# print("验证码识别结果：", code)

# im = array(Image.open("jfvbjpg.jpg").convert('L'))
# for i in range(30):
#     for j in range(70):
#         if 30<=im[i][j]<=110:
#             im[i][j] = 1
#         else:
#             im[i][j] = 0
# gray()
# contour(im, origin='image')
# axis('equal')
# axis('off')
# # print(show())
# savefig("jfvb.jpg")

# image = Image.open("3.gif")
# gray_image = image.convert('L')
# #
# # # 对图像进行二值化处理
# threshold = 150
# # binary_image = gray_image.point(lambda x: 0 if x< threshold else 255, '1')
# binary_image = gray_image.point(lambda p: p > threshold and 255)
# #
# from scipy.ndimage.filters import median_filter
# im = median_filter(binary_image, size=5)
# im.show()


# blurred_image = binary_image.filter(ImageFilter.SMOOTH_MORE)
# blurred_image.save("333.jpg")
#
# # 使用 Tesseract OCR 进行数字识别
# code = pytesseract.image_to_string("222.jpg", config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
#
# print("验证码识别结果：", code)


# # 进行验证码识别
# img = Image.open("5.gif")
# result = pytesseract.image_to_string(img,)  # 接口默认返回的是字符串
# print(result)
# # # ''.join(result.split())  # 去掉全部空格和\n\t等
# # result = ''.join(list(filter(str.isalnum, result)))  # 只保留字母和数字
# # print(result)




