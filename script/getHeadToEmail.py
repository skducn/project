# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-9-18
# Description: 调用笔记本摄像头进行拍照，并发送邮件
# *****************************************************************

from PO.netPO import *
from PO.devicePO import *
from PO.timePO import *
device_PO = DevicePO()
net_PO = NetPO()
time_PO = TimePO()


# 调用摄像头拍照
varPathFile = "d:\\51\\" + time_PO.getDatetime() + ".jpg"
device_PO.callCamera(varPathFile)

# 发邮件
net_PO.sendEmail('skducn@163.com', "skducn@163.com", "笔记本于" + time_PO.getDatetimeEditHour(0) + "调用摄像头拍照",
          "您好！\n\n调用摄像头笔记本的mac地址：" + device_PO.getMAC() + " , IP地址：" + device_PO.getLocalIP() + "\n\n这是一封自动产生的email，请勿回复\n\nBest Regards",
          varPathFile, "", "", "")
