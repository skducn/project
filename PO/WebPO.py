# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2018-7-2
# Description: webdriverPO 对象层
# geckodriver 0.14.0 for selenium3.0 下载地址：https://github.com/mozilla/geckodriver/releases
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases

# chromedriver驱动，下载地址：https://npm.taobao.org/mirrors/chromedriver
# 查看Chrome浏览器版本，chrome://version/
# chrome浏览器的options参数，https://blog.csdn.net/xc_zhou/article/details/82415870
# Q1：WebDriverException:Message:'geckodriver'executable needs to be in Path
# A1：geckodriver是原生态的第三方浏览器，对于selenium3.x版本使用geckodriver来驱动firefox，需下载geckodriver.exe,下载地址：https://github.com/mozilla/geckodriver/releases
# 将 geckodriver 放在 C:\Python38\Scripts

# Q2：MAC 移动chromedriver时报错，如 sudo mv chromedriver /usr/bin 提示： Operation not permitted
# A2: 重启按住command + R,进入恢复模式，实用工具 - 终端，输入 csrutil disable , 重启电脑。
# *******************************************************************************************************************************

'''

1.1，打开网站
1.2，关闭网站

2，获取当前全屏浏览器分辨率

3.1，截取全屏
3.2，截取浏览器内屏幕
3.3，截屏指定图片中某一区域

4.1，屏幕左移
4.2，屏幕上移
4.3，屏幕下移
4.4，元素拖动到可见的元素
4.5，内嵌窗口中滚动条操作

5，获取验证码

6，弹出框(未测试)

7，切换窗口
8，多浏览器窗口切换（不指定那个网址的）


'''


from PO.BasePO import *
from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageGrab
import cv2,requests
from pytesseract import *
from PIL import Image, ImageDraw, ImageGrab
from PO.DataPO import *
Data_PO = DataPO()

class WebPO(BasePO):


    # 1.1 打开
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
            # option.add_argument('--ignore-certificate-errors')
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            # option.add_argument("user-data-dir = C:\Python37\profile")
            self.driver = webdriver.Chrome(options=option)
            self.driver.get(varURL)
        return self.driver
    def openURL(self, varURL):
        self._openURL(varURL)

    # 1.2 关闭（当前窗口）
    def closeURL(self):
        self.driver.close()

    # 1.3 关闭所有窗口（退出驱动）
    def quitURL(self):
        self.driver.quit()

    # todo [screen]

    # 2.1 获取当前全屏浏览器宽高
    def getBrowserSize(self):
        self.driver.maximize_window()  # 全屏
        size_Dict = self.driver.get_window_size()
        return(size_Dict['width']-16, size_Dict['height']-16)

    # 2.2 获取当前屏幕分辨率
    def getScreenWidthHeight(self):
        js = 'var winW = window.screen.width;var winH = window.screen.height;alert(winW+","+winH)'
        self.driver.execute_script(js)
        line = self.driver.switch_to.alert.text
        self.driver.switch_to.alert.accept()
        size = line.split(',')
        return int(size[0]), int(size[1])

    # 2.3 截取全屏
    def captureScreen(self, varImageFile):
        # self.Web_PO.captureScreen('d:\\allscreen.png')
        im = ImageGrab.grab()
        im.save(varImageFile)

    # 2.4 截取浏览器屏幕
    def captureBrowser(self, varImageFile):
        # 前置条件：先openURL打开浏览器后才能截屏，否则报错，如：Web_PO.openURL('https://www.baidu.com/')
        # self.Web_PO.captureBrowser("d:\\screenshot.png")
        self.driver.get_screenshot_as_file(varImageFile)

    # 2.5 截屏指定图片中某一区域
    def capturePicturePart(self, varSourceImageFile, varTargetImageFile, varHighStart, varHighEnd, varWidthStart, varWidthEnd):
        # 截指定图片中某一区域
        # img = cv2.imread(varSourceImageFile, 0)  # 截图后灰色
        img = cv2.imread(varSourceImageFile)  # 截图后原色
        crop_img = img[varHighStart:varHighEnd, varWidthStart:varWidthEnd]
        cv2.imwrite(varTargetImageFile, crop_img)
        # cv2.imshow("image", crop_img)
        # cv2.waitKey(0)

    # 2.6 屏幕左移
    def scrollLeft(self, location, t):
        # 如：Web_PO.scrollLeft('1000', 2)  # 屏幕向左移动1000个像素
        self.driver.execute_script("var q=document.documentElement.scrollLeft=" + location)
        sleep(t)

    # 2.7 屏幕上移
    def scrollTop(self, location, t):
        # 屏幕上移 self.Web_PO.scrollTop("10000",2)
        # js = "var q=document.body.scrollTop=" + location
        self.driver.execute_script("var q=document.documentElement.scrollTop=" + location)
        sleep(t)

    # 2.8 屏幕下移
    def scrollDown(self, location, t):
        # 屏幕下移
        self.driver.execute_script("var q=document.documentElement.scrollDown=" + location)
        sleep(t)


    # 3 元素拖动到可见的元素
    def scrollIntoView(self, varXpath, t):
        # 元素拖动到可见的元素
        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)


    # 4 内嵌窗口中滚动条操作
    def scrollTopById(self, varId, t):
        # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
        # self.screenTopId("zy.android.healthstatisticssystem:id/vp_content",2)
        js = "var q=document.getElementById('" + varId +"').scrollTop=100000"
        self.driver.execute_script(js)
        sleep(t)


    # 5 获取验证码
    def getCode(self, capScrnPic, xStart, yStart, xEnd, yEnd):
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


    # 6 弹出框(未测试)
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


    # todo [browser]

    # 7 浏览器中多个标签页切换（同时打开2个标签页）
    def openSwitchLabel(self, varURL1, varURL2, varSwitch):
        # 如：先打开 varURL1，再打开 varURL2，且激活第一个标签页
        # Web_PO.switchWindow("http://www.baidu.com", "http://www.taobao.com", 0)   # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页
        self.openURL(varURL1)
        self.driver.execute_script('window.open("' + varURL2 + '");')  # 新建标签2
        all_handles = self.driver.window_handles
        sleep(2)
        self.driver.switch_to.window(all_handles[varSwitch])
        # Web_PO.driver.close()  # 关闭当前窗口
        # Web_PO.driver.switch_to.window(all_handles[1])  # 切换回url2
        # sleep(5)
        # Web_PO.driver.quit() # 关闭所有窗口


    # 8 浏览器中新建标签页（激活状态）
    def openNewLabel(self, varURL):
        self.openURL(varURL)
        self.driver.execute_script('window.open("' + varURL + '");')


    # 9 浏览器中多个标签页切换
    def switchLabel(self, varSwitch):
        # self.Web_PO.switchLabel(0) # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页 , 以此类推。
        all_handles = self.driver.window_handles
        sleep(2)
        self.driver.switch_to.window(all_handles[varSwitch])



if __name__ == '__main__':

    Web_PO = WebPO("chrome")
    # Web_PO = WebPO("firefox")

    # Web_PO.driver.set_window_size(1366, 768)  # 按分辨率1366*768打开浏览器


    # print("1.1，打开网站".center(100, "-"))
    # Web_PO.openURL('https://www.baidu.com/')
    #
    # print("2，获取当前全屏浏览器分辨率".center(100, "-"))
    # print(Web_PO.getBrowserSize())  # (1920, 1040)
    #
    # print("3.1，截取全屏".center(100, "-"))
    # Web_PO.captureScreen('d:\\fullScreen.jpg')  # 1920,1080
    #
    # print("3.2，截取浏览器内屏幕".center(100, "-"))
    # Web_PO.openURL('https://www.baidu.com/')
    # Web_PO.captureBrowser(u"d:\\browserScreen.png")  # 1920,926

    # print("3.3，截屏指定图片中某一区域".center(100, "-"))
    # Web_PO.capturePicturePart("d:\\fullScreen.jpg", "d:\\test.jpg", 500, 700, 750, 1050)



