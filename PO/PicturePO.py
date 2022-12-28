# coding: utf-8
# ***************************************************************
# Author     : John
# Date       : 2022-12-29
# Description: 图片处理库
# ***************************************************************

'''

1 裁剪图片中的区域（画中画）
2 设置图片灰色
3 下载图片
'''

import cv2, requests
from PIL import Image, ImageDraw, ImageGrab

class PicturePO():


    def PIP(self, varSourceImageFile, varTargetImageFile, varWidthStart, varWidthEnd, varHighStart, varHighEnd, ):

        '''1 裁剪图片中的区域（画中画）'''

        # img = cv2.imread(varSourceImageFile, 0)  # 截图后灰色
        img = cv2.imread(varSourceImageFile)  # 截图后原色
        crop_img = img[varHighStart:varHighEnd, varWidthStart:varWidthEnd]
        cv2.imwrite(varTargetImageFile, crop_img)
        # cv2.imshow("image", crop_img)
        # cv2.waitKey(0)


    def setGrey(self, varSourceImageFile, varTargetImageFile):

        '''2 设置图片灰色 '''

        img = cv2.imread(varSourceImageFile, 0)  # 设置图片灰色
        cv2.imwrite(varTargetImageFile, img)


    def downPic(self, picUrl, toSave):

        '''3 下载图片'''

        img = requests.get(picUrl)
        with open(toSave, 'ab') as f:
            f.write(img.content)
            f.close()



if __name__ == '__main__':

    Picture_PO = PicturePO()

    # print("1 裁剪图片中的区域（画中画）".center(100, "-"))
    # Picture_PO.PIP("d:/11/6/12.jpg", "d:/11/6/revise12.jpg", 0, 400, 0, 800)


    # print("2 设置图片灰色".center(100, "-"))
    Picture_PO.setGrey("d:/11/6/12.jpg", "d:/11/6/back.jpg")

   # print('3 下载图片'.center(100, "-"))
    Picture_PO.downPic('https://imgsa.baidu.com/forum/w%3D580/sign=b2310eb7be389b5038ffe05ab534e5f1/680c676d55fbb2fbc7f64cbb484a20a44423dc98.jpg', "d:/11/6/123.jpg")



