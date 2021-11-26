# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: 微信小程序自动化测试 python + uiautomator2 + weditor
# 微信小程序自动化测试-----python+weditor的使用 https://blog.csdn.net/weixin_44062468/article/details/95202814
# pip3 install --pre uiautomator2
# 连接手机后安装atx-agent, python -m uiautomator2 init  , 显示 Successfully init AdbDevice(serial=ff6183750321) 表示成功，ff6183750321这是手机设备。
# pip3 install --pre weditor
# shttps://github.com/openatx/uiautomator2#xpath

# TBX调用
# debugmm.qq.com/?forcex5=true
#***************************************************************


import uiautomator2 as u2
import os
import time

#d = u2.connect('172.16.0.7')
# d = u2.connect_usb('ff6183750321')
d = u2.connect_usb('5LM7N16315006543')
# print(d.info)
# print(d.info['currentPackageName'])

# 启动微信

# d.app_info("com.tencent.mm")
# img = d.app_icon("com.tencent.mm")
# img.save("icon.png")

d.unlock()
d.app_start("com.tencent.mm")
d.swipe_ext("down",scale=0.9)

# LCM
# d.xpath('//*[@content-desc="LCMclub,"]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]').click()

# 金桥国际
d.xpath('//*[@resource-id="com.tencent.mm:id/dix"]/android.widget.RelativeLayout[3]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]').click()
# d.click(0.944, 0.168)

# u2.set_fail_prompt(True) # 填写False可以关闭这个功能
#
# d = u2.connect()
# d(text="Search").click(timeout=2)



#
# d(resourceId="com.huawei.android.launcher", text=u"微信").click()
# time.sleep(5)

# #进入应用列表
# d(resourceId="com.android.launcher3:id/all_apps_handle").click()
# time.sleep(5)
#
# # 启动AppWWW
# d(resourceId="com.android.launcher3:id/icon", text=u"骁龙相机").click()
# time.sleep(5)
#
# # 拍照
# d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()
# time.sleep(5)
#
# # 切换摄像图
# d(resourceId="org.codeaurora.snapcam:id/front_back_switcher").click()
# time.sleep(5)
#
# #拍照
# d(resourceId="org.codeaurora.snapcam:id/shutter_button").click()
# time.sleep(5)
#
#
# #点击预览按钮
# d(resourceId="org.codeaurora.snapcam:id/preview_thumb").click()
#
# time.sleep(5)
#
# #按返回键
# for i in range(2):
#     os.system("adb shell input keyevent 4")
#     time.sleep(3)
