# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 调用当前笔记本摄像头拍照  callCamera()
# 调用笔记本摄像头，需安装opencv包(cv2)，pip install opencv-python
# ***************************************************************

import cv2
from time import strftime, localtime, sleep

def callCamera():

    """调用当前笔记本摄像头拍照"""
    tmp = strftime("%Y", localtime()) + strftime("%m", localtime()) +strftime("%d", localtime()) +strftime("%H", localtime()) +strftime("%M", localtime()) + strftime("%S", localtime())
    varSaveFile = "camera" + str(tmp) + ".jpg"
    cap = cv2.VideoCapture(0)
    cap.set(3, 700)
    cap.set(4, 500)
    cap.set(5, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 99)
    cap.set(cv2.CAP_PROP_CONTRAST, 20)
    cap.set(cv2.CAP_PROP_EXPOSURE, 3000)
    ret, frame = cap.read()
    cv2.waitKey(2)
    cv2.imwrite(varSaveFile, frame)
    cap.release()
    cv2.destroyAllWindows()


callCamera()   # 无参数，则默认保存在当前路径，文件名为 callCamera当前日期时间，如 callCamera20200312121012.jpp

