# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-11-14
# Description: 验证码
# https://blog.csdn.net/Cameback_Tang/article/details/124247948 Python使用pytesseract进行验证码图像识别
# https://blog.csdn.net/u010698107/article/details/121736386 Python OCR工具pytesseract详解
# ddddocr库目前支持的版本为Python3.9以下
# pip install ddddocr
# pip install ddddocr -i https://pypi.tuna.tsinghua.edu.cn/simple/
# https://weibo.com/ttarticle/p/show?id=2309404947288748326957
# 训练验证码之ddddocr一个图文视频教学 https://blog.csdn.net/weixin_43411585/article/details/136559397#_1
# *****************************************************************

import ddddocr
import cv2

# 数字字母混合的验证码、纯字母验证码
ocr = ddddocr.DdddOcr()
f = open("3766.jpg", mode='rb')
# f = open("jfvb.jpg", mode='rb')
cpatcha = ocr.classification(f.read())
print(cpatcha)  # 3766


# 滑块验证码
# import ddddocr  det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)  with open('target.png', 'rb') as f:     target_bytes = f.read()  with open('background.png', 'rb') as f:     background_bytes = f.read()  res = det.slide_match(target_bytes, background_bytes, simple_target=True) print(res)  ------------------------------------------ 输出结果如下: {'target_y': 0, 'target': [184, 58, 246, 120]}


# 中文验证码识别
det = ddddocr.DdddOcr(det=True)
with open("chinese.jpg", 'rb') as f:
    image = f.read()
    poses = det.detection(image)
    im = cv2.imread("chinese.jpg")
    for box in poses:
        x1, y1, x2, y2 = box
        im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
        cv2.imwrite("result.jpg", im)

