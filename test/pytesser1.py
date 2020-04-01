# coding=utf-8

import pytesseract
from PIL import Image

image = Image.open("6.jpg")
code = pytesseract.image_to_string(image)
print(code)



#
# import PIL
# # import sys
# # print sys.path
#
# from pytesseract import *
# from PIL import Image
# # from pytesser import *
# # import Image
#
# # 获取此元素在页面中的位置及尺寸
# # checkcodeimg = Level_PO.getXPATH("//img[@onclick=\"doChangeCaptcha(this)\"]", 2)
# # # x1 = checkcodeimg.location['x']
# # # y1 = checkcodeimg.location['y']
# # # x2 = x1 + checkcodeimg.size['width']
# # # y2 = y1 + checkcodeimg.size['height']
# # # box = (int(x1), int(y1), int(x2), int(y2))
#
# im = Image.open('kaptcha.jpg')
# imgry = im.convert('L')
# print(image_to_string(imgry))
#
#
# Level_PO.getCode(u"test.jpg", 2060, 850, 2187, 900)