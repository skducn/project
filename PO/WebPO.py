# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John12121212,2222222
# Date       : 2018-7-2
# Description: webdriverPO 对象层
# geckodriver 0.14.0 for selenium3.0 下载地址：https://github.com/mozilla/geckodriver/releases
# chromedriver驱动，下载地址：https://npm.taobao.org/mirrors/chromedriver
# 查看Chrome浏览器版本，chrome://version/
# chrome浏览器的options参数，https://blog.csdn.net/xc_zhou/article/details/82415870
# Q1：WebDriverException:Message:'geckodriver'executable needs to be in Path
# A1：geckodriver是原生态的第三方浏览器，对于selenium3.x版本使用geckodriver来驱动firefox，需下载geckodriver.exe,下载地址：https://github.com/mozilla/geckodriver/releases
# 将 geckodriver 放在 C:\Python38\Scripts
# Q2：MAC 移动chromedriver时报错，如 sudo mv chromedriver /usr/bin 提示： Operation not permitted
# A2: 重启按住command + R,进入恢复模式，实用工具 - 终端，输入 csrutil disable , 重启电脑。
# *******************************************************************************************************************************

from PO.BasePO import *
from selenium import webdriver
from PIL import ImageGrab
import cv2
from pytesseract import *
from PIL import Image, ImageDraw, ImageGrab

class WebPO(BasePO):

    def _openURL(self, varURL):
        if self.driver == "firefox" :
            if platform.system() == 'Windows':
                # profile = webdriver.FirefoxProfile()
                # # profile = FirefoxProfile()
                # profile.native_events_enabled = True
                # # self.driver = Firefox(profile)
                # profile.set_preference("browser.startup.homepage", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
                # profile.set_preference("startup.homepage_welcome_url", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
                # profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
                # profile.assume_untrusted_cert_issuer = True  # 访问没有证书的https站点
                # accept_untrusted_certs = True  # 访问没有证书的https站点
                # profile.set_preference('permissions.default.image', 2)  # 不加载的图片，加快显示速度
                # profile.set_preference('browser.migration.version', 9001)  # 不加载过多的图片，加快显示速度
                # self.driver = webdriver.Firefox(profile)
                self.driver = webdriver.Firefox()
                self.driver.implicitly_wait(10)  # 隐性等待
                self.driver.get(varURL)
            elif platform.system() == 'Darwin':
                self.driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver.log')
                self.driver._is_remote = False  # 解决mac电脑上传图片问题
                self.driver.implicitly_wait(10)   # 隐性等待
                self.driver.get(varURL)
            return self.driver

        if self.driver == "chrome" :
            option = webdriver.ChromeOptions()
            option.add_argument('disable-infobars')
            # option.add_argument("user-data-dir = C:\Python37\profile")
            self.driver = webdriver.Chrome(chrome_options=option)
            self.driver.get(varURL)

        return self.driver

    def openURL(self, varURL):
        self._openURL(varURL)

    def closeURL(self):
        self.driver.quit()

    def getScreenWidthHeight(self):
        # 获取当前屏幕分辨率
        js = 'var winW = window.screen.width;var winH = window.screen.height;alert(winW+","+winH)'
        self.driver.execute_script(js)
        line = self.driver.switch_to.alert.text
        self.driver.switch_to.alert.accept()
        size = line.split(',')
        Screen = {}
        Screen['width'] = int(size[0])
        Screen['height'] = int(size[1])
        return Screen

    def getFullScreen(self, varImageFile):
        # 截取全屏
        # self.Web_PO.getFullScreen('d:\\allscreen.png')
        im = ImageGrab.grab()
        im.save(varImageFile)

    def getBrowserScreen(self, varImageFile):
        # # 截取浏览器内屏幕(因此要打开浏览器后才能截图)
        # self.Web_PO.getBrowserScreen("d:\\screenshot.jpg")
        try:
            self.driver.get_screenshot_as_file(varImageFile)
        except:
            pass

    def getPartScreen(self, varSourceImageFile, varTargetImageFile):
        # 截屏指定图片中某一区域，并另存为。？测试未通过
        # self.Web_PO.getPartScreen("d://123", "d:/444", 452, 40, 1480, 130)
        img = cv2.imread(varSourceImageFile)
        # h、w为想要截取的图片大小
        h = 40
        w = 130
        cropImg = img[(452):(452 + h), (1480):(1480 + w)]
        cv2.imwrite(varTargetImageFile, cropImg)

    def scrollLeft(self, location, t):
        # 屏幕左移
        # 如：Web_PO.scrollLeft('1000', 2)  # 屏幕向左移动1000个像素
        self.driver.execute_script("var q=document.documentElement.scrollLeft=" + location)
        sleep(t)

    def scrollTop(self, t):
        # 屏幕上移 screenTop("10000",2)
        # js = "var q=document.body.scrollTop=" + location
        self.driver.execute_script("var q=document.documentElement.scrollTop=100000")
        sleep(t)

    def scrollDown(self, location, t):
        # 屏幕下移
        self.driver.execute_script("var q=document.documentElement.scrollDown=" + location)
        sleep(t)

    def scrollIntoView(self, varXpath, t):
        # 元素取悦拖动到可见的元素
        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)

    def scrollTopById(self, varId, t):
        # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
        # self.screenTopId("zy.android.healthstatisticssystem:id/vp_content",2)
        js = "var q=document.getElementById('" + varId +"').scrollTop=100000"
        self.driver.execute_script(js)
        sleep(t)

    def getCode(self, capScrnPic, xStart, yStart, xEnd, yEnd):
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

    def popupAlert(self, operate, t):
        # 弹出框 (未测试)
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

if __name__ == '__main__':

    Web_PO = WebPO("chrome")
    # Web_PO = WebPO("firefox")
    Web_PO.openURL('https://www.baidu.com/')
    Web_PO.driver.maximize_window()  # 全屏
    # sleep(2)
    # print(Web_PO.getScreenWidthHeight())
    # Web_PO.getFullScreen('d:\\allscreen.png')
    # Web_PO.getBrowserScreen("d:\\screenshot.jpg")


