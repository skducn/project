# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2018-7-18
# Description: android自动化测试框架
# config.py 配置文件，负责启动appium
# AndroidPO.py 函数封装包
# selenium 3.13    sudo pip install selenium -U / pip show selenium
# appium-desktop 1.8.2 对应的包 Appium-1.6.2.dmg   from https://github.com/appium/appium-desktop/releases
# 命令方式启动appium 1.8.2
# os.system("node /Applications/Appium.app/Contents/Resources/app/node_modules/appium/build/lib/main.js ")
#***************************************************************
import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,random,webbrowser,platform,string,datetime,redis,subprocess,re,smtplib,pytesseract
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
from time import sleep
sys.path.append("..")
from appium import webdriver
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from Public.PageObject.LevelPO import *

# from Public.PageObject.ThirdPO import *
# Third_PO = ThirdPO()
# 获取包的Package 和 LaunchActivityName
# appLocation ='/Users/linghuchong/Desktop/cetchealth1.0.1_test_20180709.apk'
# appLocation = 'ehr_dmp_release_ttest_v1.3.0.apk'
# devicesinfo1 = subprocess.Popen("aapt dump badging {}".format(appLocation),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# print(devicesinfo1)
# devicesinfo2 = devicesinfo1.stdout.read()
# print(devicesinfo2)
# PackageName = devicesinfo2.split(" versionCode")[0].replace("package: name=","").replace("'","")
# LaunchActivityName = devicesinfo2.split("launchable-activity: name='")[1].split("'")[0]
# androidVersion = subprocess.getoutput('adb shell getprop ro.build.version.release')
# androidSerialno = subprocess.getoutput('adb shell getprop ro.serialno')
# android
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'  # '4.4'   # str(float(androidVersion[0:3]))
desired_caps['deviceName'] = '13123'
# desired_caps['app'] = '/Users/linghuchong/Downloads/51/android/dangjian/PartyBuilding1.0.0_prod.apk'
desired_caps['appPackage'] = 'zy.android.healthstatisticssystem'
desired_caps['appActivity'] = 'zy.android.healthstatisticssystem.mvp.ui.activity.SplashActivity'
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# print(androidVersion)

# # 手机信息定义与输出 , 定义手机分辨率的宽,高
# screenX = driver.get_window_size()['width']
# screenY = driver.get_window_size()['height']
# tmpProductmodel = commands.getoutput('adb shell getprop ro.product.model')
# tmpProductdevice = commands.getoutput('adb shell getprop ro.product.device')
# tmpSdk = commands.getoutput('adb shell getprop ro.build.version.sdk')
# tmpAbi = commands.getoutput('adb shell getprop ro.product.cpu.abi')
# tmpSerialno = commands.getoutput('adb shell getprop ro.serialno')
# productmodel = tmpProductmodel.strip()
# print u"型号 = " + str(tmpProductmodel.strip()) + u"\n" \
#      u"分辨率 = " + str(screenX) + u" x " + str(screenY) + u"\n" \
#      u"Android版本 = " + str(androidVersion.strip()) + u" , SDK = " + str(tmpSdk.strip())