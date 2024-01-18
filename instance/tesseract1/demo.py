# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-1-16
# Description: # 图片识别文字
# https://blog.csdn.net/hhy321/article/details/125122480
# 官网下载语言包 https://tesseract-ocr.github.io/tessdoc/Data-Files 下 chi_sim.traineddata
# 将文件放在 /usr/local/share/tessdata 下
# *****************************************************************

import pytesseract
from PIL import Image

# todo 图转文字

# from PIL import Image
# im = Image.open('merged_image.png')
# string = pytesseract.image_to_string(im, lang='chi_sim')
# print(string)



# todo 图片合并

# img1 = Image.open('1.jpg')
# img2 = Image.open('3.jpg')
# w1, h1 = img1.size
# w2, h2 = img2.size
# # 创建新的图像
# new_img = Image.new('RGB', (w1+w2, h1))
# # 合并图像
# new_img.paste(img1, (0, 0))
# new_img.paste(img2, (w1, 0))
# # 保存新的图像
# new_img.save('merged_image.png')


