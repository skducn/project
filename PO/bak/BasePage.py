# coding: utf-8
#***************************************************************
# Author     : John
# Created on : 2016-7-29
# Description: 基础类封装，公用方法，例如driver, url ,FindElement等
# 定义open函数，重定义find_element，switch_frame，send_keys等函数。
#***************************************************************

import sys, os, datetime, xlrd, xlwt, smtplib, email, json, copy, random, MySQLdb, time
# import Image, ImageChops, mimetypes
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.abstract_event_listener	import *
from selenium.webdriver.support.event_firing_webdriver import *
from selenium.webdriver.support.expected_conditions	import *
from selenium.webdriver.common.action_chains import ActionChains
from xlutils.copy import copy
from pytesseract import *
from time import sleep
from PIL import Image, ImageDraw, ImageGrab
from pyquery import PyQuery as pg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase


class BasePage(object):

    def __init__(self, driver):
        # driver 是BasePage类的入参。
        self.driver = driver

    def _openURL(self, varURL, t):
        # 打开浏览器地址
        # 单下划线_开头的方法，在使用import * 时，该方法不会被导入，保证该方法为类私有的。
        self.driver.get(varURL)
        sleep(t)
        # self.driver.set_window_size(dimWidth, dimHigh)  # 指定窗口大小如 1920 * 1080
        # self.driver.maximize_window()  # 最大化浏览器 for win mac
    def openURL(self, varURL, t):
        self._openURL(varURL, t)

    def _openURLmore(self, varURL, varWidth, varHigh, t):
        # 打开多个浏览器地址
        self.driver.set_window_size(varWidth, varHigh)
        self.driver.get(varURL)
        sleep(t)
        # self.now_handle = self.driver.current_window_handle  # 获取当前窗口句柄
        # return self.now_handle
    def openURLmore(self, varURL, varWidth, varHigh, t):
        self._openURLmore(varURL, varWidth, varHigh, t)

    # def on_page(self, pagetitle):
    #     # 使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）
    #     return pagetitle in self.driver.title
    #
    # def _check_title(self, url, pagetitle):
    #     try:
    #         assert self.on_page(pagetitle), u"%s, expected=%s, actual=%s" % (url, self.driver.title, pagetitle)
    #     finally:
    #         pass
    #
    # def checkk_title(self):
    #     self._check_title(self.base_url, self.pagetitle)

    def find_element(self, *loc):
        # 重写元素定位方法
        try:
            # 注意：入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
            # WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下入参本身是元组，不需要加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            # print u"%s 页面中未能找到元素 %s "%(self, loc)
            print(u"页面中未找到元素 %s " %(loc))

    def find_elements(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except:
            print(u"页面中未找到元素 %s " %(loc))

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        # 重写定义send_keys方法
        try:
            loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            # print u"%s 页面中未能找到 %s 元素"%(self, loc)
            print(u"页面中未找到元素 %s " % (loc))

    def sendKeysId_mac(self, dimId, dimValue):
        self.driver.find_element_by_id(dimId).send_keys(dimValue)
    def sendKeysName_mac(self, dimName, dimValue):
        self.driver.find_element_by_name(dimName).send_keys(dimValue)
    def sendKeysXpath_mac(self, dimXpath, dimValue):
        self.driver.find_element_by_xpath(dimXpath).send_keys(dimValue)

    def close_driver(self):
        self.driver.close()
        # self.driver.quit()

    def popupAlert(self, operate, t):
        # 弹出框操作
        # self.Level_PO.popupAlert("accept", 2)
        # a = self.driver.switch_to_alert()
        # a.accept()  # 相当于点击确定，或者使用   driver.execute("acceptAlert")
        # a.dismiss()  # 相当于点击取消，或者使用   driver.execute("dismissAlert")
        # a.text  # 获取弹出框里的文字  或者使用  driver.execute("getAlertText")["value"]
        if operate == "accept":
            self.driver.switch_to_alert().accept()
            sleep(t)
        if operate == "dismiss":
            self.driver.switch_to_alert().dismiss()
            sleep(t)
        if operate == "text":
            return self.driver.switch_to_alert().text



    def getScreen(self, position, widthPercent, heightPercent):
        # 获取屏幕分辨率，并按比例返回 宽度和高度。
        # 如：getScreen(0.5, 1) 表示 宽度*0.5，高度*1
        js = 'var winW = window.screen.width;var winH = window.screen.height;alert(winW+","+winH)'
        self.driver.execute_script(js)
        line = self.driver.switch_to_alert().text
        self.driver.switch_to_alert().accept()
        size = line.split(',')
        if position == "left":
            width = int(size[0]) * widthPercent  # width
            height = int(size[1]) * heightPercent  # height
        if position == "right":
            width = int(size[0]) * widthPercent  # width
            height = int(size[1]) * heightPercent  # height
            x = int(size[0]) - width
            self.driver.set_window_position(x, y=0)
        return (width, height)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    '''[GET Database]'''

    def getTblRecordWhere1(self, cur, dimTable, dimWhereExpression):
        # 功能：查询表中记录是否存在，1个条件， 返回0=找到0条，1=找到1条，2=找到2条，以此类推）
        # print Level_PO.getTblRecordWhere1(curNCZ, "tm_doctor", "org_id=92")
        where = dimWhereExpression.split('=')
        x = cur.execute('select * from %s where %s="%s"' % (dimTable, where[0], where[1]))
        return x
    def getTblRecordWhere2(self, cur, dimTable, dimWhereExpression1, dimWhereExpression2):
        # 功能：查询表中记录是否存在，2个条件， 返回0=找到0条，1=找到1条，2=找到2条，以此类推）
        # print Level_PO.getTblRecordWhere2(curNCZ, "tm_doctor", "org_id=92", "office_id=262")
        where1 = dimWhereExpression1.split('=')
        where2 = dimWhereExpression2.split('=')
        x = cur.execute('select * from %s where %s="%s" and %s="%s"' % (dimTable, where1[0], where1[1], where2[0], where2[1]))
        return x
    def getTblValueWhere1(self, conn, cur, dimTable, dimField, dimWhereExpression):
        # 功能：查询表中某条件的字段值，1个条件
        # print Level_PO.getTblValueWhere1(connNCZ, curNCZ, "tm_doctor", "doctor_id", "job_number=lll520")
        where = dimWhereExpression.split('=')
        conn.commit()
        x = cur.execute('select %s from %s where %s="%s"' % (dimField, dimTable, where[0], where[1]))
        if x == 0 :
            return -1111111111
        else:
            t = cur.fetchone()
            return t[0]
    def getTblValueWhere2(self, conn, cur, dimTable, dimField, dimWhereExpression1, dimWhereExpression2):
        # 功能：查询表中某条件的字段值，1个条件
        # print Level_PO.getTblValueWhere2(connNCZ, curNCZ, "tm_doctor", "doctor_id", "org_id=92", "job_number=lll520")
        where1 = dimWhereExpression1.split('=')
        where2 = dimWhereExpression2.split('=')
        conn.commit()
        x = cur.execute('select %s from %s where %s="%s" and %s="%s"' % (dimField, dimTable, where1[0], where1[1], where2[0], where2[1]))
        if x == 0 :
            return -1111111111
        else:
            t = cur.fetchone()
            return t[0]



    '''[SCREEN]'''

    def captureScreenShot(self, varSavePath):
        # varSavePath = u'/Users/linghuchong/Downloads/51/screenshot.png'
        self.driver.save_screenshot(varSavePath)
    def screenLeft(self, location, t):
        # 屏幕左移
        # 如：Level_PO.screenLeft('1000', 2)  # 屏幕向左移动1000个像素
        self.driver.execute_script("var q=document.documentElement.scrollLeft=" + location)
        sleep(t)
    def screenTop(self, t):
        # 屏幕上移 screenTop("10000",2)
        # js = "var q=document.body.scrollTop=" + location
        self.driver.execute_script("var q=document.documentElement.scrollTop=100000")
        sleep(t)
    def screenDown(self, location, t):
        # 屏幕下移
        self.driver.execute_script("var q=document.documentElement.scrollDown=" + location)
        sleep(t)
    def screenTarget(self, varXpath, t):
        # 元素取悦拖动到可见的元素
        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)
    def screenTopId(self,id,t):
    # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
    # self.screenTopId("zy.android.healthstatisticssystem:id/vp_content",2)
        js = "var q=document.getElementById('" + id +"').scrollTop=100000"
        self.driver.execute_script(js)
        sleep(t)

    '''[图片降噪]'''

    def RGB2BlackWhite(self,filename):
        im = Image.open(filename)
        print("image info,", im.format, im.mode, im.size)
        (w, h) = im.size
        R = 0
        G = 0
        B = 0
        for x in range(w):
            for y in range(h):
                pos = (x, y)
                rgb = im.getpixel(pos)
                (r, g, b) = rgb
                R = R + r
                G = G + g
                B = B + b

        rate1 = R * 1000 / (R + G + B)
        rate2 = G * 1000 / (R + G + B)
        rate3 = B * 1000 / (R + G + B)

        print ("rate:", rate1, rate2, rate3)

        for x in range(w):
            for y in range(h):
                pos = (x, y)
                rgb = im.getpixel(pos)
                (r, g, b) = rgb
                n = r * rate1 / 1000 + g * rate2 / 1000 + b * rate3 / 1000
                # print "n:",n
                if n >= 60:
                    im.putpixel(pos, (255, 255, 255))
                else:
                    im.putpixel(pos, (0, 0, 0))

        im.save("blackwhite.bmp")
    def saveAsBmp(self,fname):
        pos1 = fname.rfind('.')
        fname1 = fname[0:pos1]
        fname1 = fname1 + '_2.bmp'
        im = Image.open(fname)
        new_im = Image.new("RGB", im.size)
        new_im.paste(im)
        new_im.save(fname1)
        return fname1

    # 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
    # 该函数也可以改成RGB判断的,具体看需求如何
    # # 打开图片
    # image = Image.open("yhzncz1.jpg")
    # # 将图片转换成灰度图片
    # image = image.convert("L")
    # # 去噪,G = 50,N = 4,Z = 4
    # Level_PO.clearNoise(image, 50, 4, 4)
    # # 保存图片
    # image.save("yhzncz123456789.jpg")

    def getPixel(self,image, x, y, G, N):
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0
        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            return image.getpixel((x, y - 1))
        else:
            return None

            # 降噪

    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # G: Integer 图像二值化阀值
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功
    #  1：降噪失败

    def clearNoise(self,image, G, N, Z):
        draw = ImageDraw.Draw(image)
        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = self.getPixel(image, x, y, G, N)
                    if color != None:
                        draw.point((x, y), color)

    '''[获取验证码]'''

    def getCode(self, capScrnPic,xStart, yStart, xEnd, yEnd):
        # 获取验证码
        # Level_PO.getCode(u"test.jpg",2060, 850, 2187, 900）
        # 注：地址是图片元素中的位置。
        self.driver.save_screenshot(capScrnPic)
        i = Image.open(capScrnPic)
        frame4 = i.crop((xStart, yStart, xEnd, yEnd))
        frame4.save(capScrnPic)
        # im = Image.open(capScrnPic)
        # imgry = im.convert('L')
        # # 去噪,G = 50,N = 4,Z = 4
        # self.clearNoise(imgry, 50, 0, 4)
        # # imgry.save(capScrnPic)
        # filename = self.saveAsBmp(capScrnPic)
        # self.RGB2BlackWhite(filename)
        # im = Image.open(capScrnPic)
        # imgry = im.convert('L')
        # ''''''''''''''''''''''''''''''''''''''
        img = Image.open(capScrnPic)
        img = img.convert('RGBA')
        pixdata = img.load()

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        img.save(capScrnPic)
        im = Image.open(capScrnPic)
        imgry = im.resize((1000, 500), Image.NEAREST)

        return image_to_string(imgry)


    '''[ASSERT]'''

    def assertTrue(self, expected, okMsg, errMsg):
        if expected == True :
            print (okMsg)
        else:
            print (errMsg)
    def assertEqual(self, expected, actual, okMsg, errMsg):
        if expected == actual:
            print (okMsg)
        else:
            print (errMsg)
    def assertContain(self, one, allcontain, okMsg, errMsg):
        if one in allcontain:
            print (okMsg)
        else:
            print (errMsg)

    '''[错误提示]'''

    def getError(self, varStatus, varErrorInfo, varErrorRow):
        # 功能：当函数返回值是error时，获取当前语句行号及错误提示。因此函数必须要有返回值
        # Level_PO.getError(Level_PO.inputId(u"officebundle_tmoffice_officeName", u"自动化科室123"), u"输入框定位错误！",sys._getframe().f_lineno)
        # errorrrrrrrrrrr, 101行, '获取科室文本与对应值的字典'。
        if varStatus == u"error":
            print (u"errorrrrrrrrrrr,", varErrorRow, u"行,", varErrorInfo)
            os._exit(0)





    # test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # def test(self):
    #     # 获取屏幕右下角图片的长度和高度, 一般是屏幕的长度和高度(1440,2392)
    #     sleep(5)
    #     self.driver.save_screenshot(u'/Users/linghuchong/Downloads/51/screenshot.png')
    #     # pic = ImageGrab.grab()
    #     # pic.save('/Users/linghuchong/Downloads/51/1.jpg')
    #     location = self.driver.find_element_by_id('code').location
    #     size = self.driver.find_element_by_id('code').size
    #     varWidth = int(location["x"] + size["width"])
    #     varHeight = int(location["y"] + size["height"])
    #
    #     a = location["x"]
    #     b = location["y"]
    #     print varWidth
    #     print varHeight
    #     print int(a)
    #     print int(b)
    #
    #     box = (int(a), int(b), varWidth, varHeight)
    #     im = Image.open(u'/Users/linghuchong/Downloads/51/screenshot.png')
    #     # im = im.crop(int(a), int(b), varWidth, varHeight)
    #     im = im.crop(box)
    #     im.save(u'/Users/linghuchong/Downloads/51/screenshot1.png')



    # def current_windows(self,now_handle):
    #     print now_handle
    #     self.driver.switch_to_window(now_handle)
        # now_handle = self.driver.current_window_handle #获取当前窗口句柄
        # print now_handle   #输出当前获取的窗口句柄
        # driver.find_element_by_id("kw1").send_keys("selenium")
        # driver.find_element_by_id("su1").click()
        # driver.find_element_by_xpath("//*[@id='1']/h3/a[1]").click()
        # time.sleep(2)
        # all_handles = self.now_handle  #获取所有窗口句柄
        # for handle in all_handles:
        # #
        # #     if handle != self.now_handle:
        # #         print handle    #输出待选择的窗口句柄
        #     self.driver.switch_to_window(handle)
        # self._current_windows(self.now_handle)
    #
    # def _current_windows(self, now_handle):
    #     self.driver.switch_to_window(now_handle)
    #     # all_handles = now_handle  #获取所有窗口句柄
    #     # for handle in all_handles:
    #     #     self.driver.switch_to_window(handle)

