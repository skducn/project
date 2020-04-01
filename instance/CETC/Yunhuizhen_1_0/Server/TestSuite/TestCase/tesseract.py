# coding: utf-8
# PyTesser 官方下载地址：http://code.google.com/p/pytesser/downloads/list
# PIL库资源地址： http://www.pythonware.com/products/pil/
# ocr https://zh.wikipedia.org/wiki/%E5%85%89%E5%AD%A6%E5%AD%97%E7%AC%A6%E8%AF%86%E5%88%AB
#
# tesseract https://code.google.com/p/tesseract-ocr/
#
# pytesseract https://pypi.python.org/pypi/pytesseract

import pytesseract
from PIL import Image

image = Image.open('/Users/linghuchong/Downloads/51/test2.png')
# image.load()
# image.split()
# vcode1=pytesseract.image_to_string(image, lang='fra')
# print vcode1


vcode1=pytesseract.image_to_string(image,lang="eng", config="-psm 7")
print vcode1
vcode = pytesseract.image_to_string(image)
print vcode


   # def screenWidthHeight(self,rightCornerPicID):
   #      # self.screenWidthHeight("com.mowin.tsz:id/my_tab")
   #      # 获取屏幕右下角图片的长度和高度, 一般是屏幕的长度和高度(1440,2392)
   #      location =  self.driver.find_element_by_id('captcha').location
   #      size = self.driver.find_element_by_id('captcha').size
   #      varWidth = int(location["x"] + size["width"])
   #      varHeight = int(location["y"] + size["height"])
   #      return varWidth,varHeight
   #
   #
   # def captureCustomScreen(self,imageName,startX, startY, endX, endY):
   #  # 功能:截取屏幕(自定义范围)   # 如: captureCustomScreen("test.png",0,1080,1,1920)
   #  self.driver.save_screenshot(imageName)
   #  box=(startX, startY, endX, endY)
   #  i = Image.open(imageName)
   #  newImage = i.crop(box)
   #  newImage.save(imageName)