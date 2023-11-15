# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-11-14
# Description: 验证码
# https://blog.csdn.net/Cameback_Tang/article/details/124247948 Python使用pytesseract进行验证码图像识别
# https://blog.csdn.net/u010698107/article/details/121736386 Python OCR工具pytesseract详解
# *****************************************************************

import ddddocr

ocr = ddddocr.DdddOcr()
f = open("1.jpg", mode='rb')
img = f.read()
result = ocr.classification(img)
print(result)  # 2345




