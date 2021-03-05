# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-3-5
# Description: # 二维码生成和识别
# 参考：https://www.bilibili.com/read/cv7761473/
# pip install pyzbar
# pip install pillow
# *****************************************************************

from pyzbar.pyzbar import decode
from PIL import Image

path = "1.png"   # 二维码图
img = Image.open(path)
bar = decode(img)[0]
result = bar.data.decode()
print(result)

