# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2018-7-2
# Description: webdriverPO 对象层

# pip install opencv_python    // cv2

# chromedriver驱动
# 下载：https://npm.taobao.org/mirrors/chromedriver
# 下载：http://chromedriver.storage.googleapis.com/index.html
# 存放路径：C:\Python38\Scripts\chromedrive.exe
# 查看Chrome浏览器版本，chrome://version/

# chrome的options参数
# https://blog.csdn.net/xc_zhou/article/details/82415870
# https://blog.csdn.net/amberom/article/details/107980370

# geckodriver 0.14.0 for selenium3.0
# 下载地址：https://github.com/mozilla/geckodriver/releases
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases

# Q1：WebDriverException:Message:'geckodriver'executable needs to be in Path
# A1：geckodriver是原生态的第三方浏览器，对于selenium3.x版本使用geckodriver来驱动firefox，需下载geckodriver.exe,下载地址：https://github.com/mozilla/geckodriver/releases
# 将 geckodriver 放在 C:\Python38\Scripts

# Q2：MAC 移动chromedriver时报错，如 sudo mv chromedriver /usr/bin 提示： Operation not permitted
# A2: 重启按住command + R,进入恢复模式，实用工具 - 终端，输入 csrutil disable , 重启电脑。
# *******************************************************************************************************************************

"""

1.1 打开网站 open()
1.2 打开标签页 openLabel("http://www.jd.com")
1.3 切换标签页 switchLabel(0)
1.4 获取当前浏览器宽高 getBrowserSize()
1.5 截取浏览器内屏幕 getBrowserScreen()

2.1 全屏浏览器 maxBrowser(0)
2.2 缩放页面比率 zoom(20)
2.3 动态加载页面滚动到底部（加载所有数据） dynamicLoadToEnd()
2.4 页面滚动条到底部 scrollToEnd()
2.5 app屏幕左移 scrollLeft('1000',9)
2.6 app屏幕右移 scrollRight('1000', 5)
2.7 app屏幕上移 scrollTop('1000', 5)
2.8 app屏幕下移 scrollDown('1000', 5)
2.9 元素拖动到可见的元素 scrollIntoView(varXpath)
2.10 内嵌窗口中滚动条操作 scrollTopById(varId)

3.1 弹出框 popupAlert()
3.2 确认弹出框 confirmAlert("accept", 2)

4.1 关闭当前窗口 close()
4.2 退出浏览器应用 quit()

获取验证码？？

"""


from PO.BasePO import *
from selenium import webdriver

# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from PIL import ImageGrab
import cv2, requests, bs4
from pytesseract import *
from PIL import Image, ImageDraw, ImageGrab
import pyautogui


class WebPO(BasePO):
    def _openURL(self, varURL):

        """1.1 打开"""

        if self.driver == "firefox":
            if platform.system() == "Windows":
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
            elif platform.system() == "Darwin":
                self.driver = webdriver.Firefox(
                    firefox_profile=None,
                    firefox_binary=None,
                    timeout=30,
                    capabilities=None,
                    proxy=None,
                    executable_path="/usr/local/bin/geckodriver",
                    firefox_options=None,
                    log_path="geckodriver.log",
                )
                self.driver._is_remote = False  # 解决mac电脑上传图片问题
                self.driver.implicitly_wait(10)  # 隐性等待
                self.driver.get(varURL)
            return self.driver

        if self.driver == "chrome":
            option = webdriver.ChromeOptions()
            option.add_argument("--start-maximized")  # 最大化
            # driver_width, driver_height = pyautogui.size()  # 通过pyautogui方法获得屏幕尺寸
            # print(driver_width, driver_height)
            # option.add_argument('--window-size=%sx%s' % (driver_width, driver_height))

            option.add_argument(
                "--disable-blink-features=AutomationControlled"
            )  # 禁止浏览器出现验证滑块
            option.add_argument(
                r"--user-data-dir=c:\selenium_user_data"
            )  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题
            # option.add_argument('--incognito')  # 无痕隐身模式
            # option.add_argument('disable-infobars')  # 不显示 Chrome正在受到自动软件的控制的提示（已废弃，替代者excludeSwitches）
            # option.add_argument("disable-cache")  # 禁用缓存
            # option.add_argument('--ignore-certificate-errors')
            # option.add_argument("--disable-extensions")  # 禁用扩展插件的设置参数项
            # option.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
            option.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )  # 不显示 chrome正受到自动测试软件的控制的提示
            # option.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            # option.headless = True  # 无界面模式
            self.driver = webdriver.Chrome(options=option)
            # self.driver = webdriver.Chrome(executable_path="d:\\chromedriver", chrome_options=option) # 启动带有自定义设置的Chrome浏览器
            self.driver.get(varURL)
            return self.driver

        if self.driver == "chromeHeadless":
            option = webdriver.ChromeOptions()
            option.add_argument(
                "--disable-blink-features=AutomationControlled"
            )  # 禁止浏览器出现验证滑块
            option.add_argument(
                r"--user-data-dir=c:\selenium_user_data"
            )  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题
            option.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )  # 不显示 chrome正受到自动测试软件的控制的提示
            option.add_experimental_option(
                "excludeSwitches", ["enable-logging"]
            )  # 禁止打印日志
            option.headless = True  # 无界面模式
            self.driver = webdriver.Chrome(options=option)
            self.driver.get(varURL)
            return self.driver

    def openURL(self, varURL):
        self._openURL(varURL)

    def openLabel(self, varURL):

        """1.2 打开标签页"""

        self.openURL(varURL)
        self.driver.execute_script('window.open("' + varURL + '");')

    def switchLabel(self, varSwitch, t=1):

        """1.3 切换标签页"""

        # self.Web_PO.switchLabel(0) # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页 , 以此类推。

        all_handles = self.driver.window_handles
        sleep(t)
        self.driver.switch_to.window(all_handles[varSwitch])

    def getBrowserSize(self):

        """1.4 获取当前浏览器宽高"""

        d_size = self.driver.get_window_size()  # {'width': 1936, 'height': 1056}
        return (d_size["width"] - 16, d_size["height"] + 24)

    def getBrowserScreen(self, varImageFile):

        """1.5 截取浏览器内屏幕"""

        # 前置条件：先打开浏览器后才能截屏.
        # self.Web_PO.getBrowserScreen("d:\\screenshot.png")
        self.driver.get_screenshot_as_file(varImageFile)

    def setBrowser(self, width, height):

        """2.0 指定分辨率浏览器"""

        # Web_PO.setBrowser(1366, 768) # 按分辨率1366*768打开浏览器
        self.driver.set_window_size(width, height)

    def maxBrowser(self, t=1):

        """2.1 全屏浏览器"""

        # self.switchLabel(varWhichWindows)  # 切换句柄
        self.driver.maximize_window()  # 全屏
        sleep(t)

    def zoom(self, percent):

        """2.2 缩放页面比率"""

        js = "document.body.style.zoom='" + str(percent) + "%'"
        self.driver.execute_script(js)

    def dynamicLoadToEnd(self, varClassValue):

        """2.3 动态加载页面滚动到底部（加载所有数据）

        varClassValue 参数是所需加载数据，如list中class值
        Web_PO.driver.find_elements(By.CLASS_NAME, "Eie04v01")
        return: 返回所需加载数据的数量
        """

        # dynamicLoadToEnd('Eie04v01')
        num, len_now = 0, 0
        _input = self.driver.find_element(By.TAG_NAME, "body")
        while True:
            _input.send_keys(Keys.PAGE_DOWN)
            self.driver.implicitly_wait(2)
            elem = self.driver.find_elements(By.CLASS_NAME, varClassValue)
            len_cur = len(elem)
            # print(len_now, len_cur)
            if len_now != len_cur:
                len_now = len_cur
                num = 0
            elif len_now == len_cur and num <= 2:
                num = num + 1
                sleep(0.5)
            else:
                sleep(2)
                break
        return len_cur

    def scrollToEnd(self, t):

        """2.4 页面滚动条到底部
        :return:
        """

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(t)

    def scrollLeft(self, location, t=1):

        """2.5 app屏幕左移"""

        # Web_PO.scrollLeft('1000', 2)  # 屏幕向左移动1000个像素
        self.driver.execute_script(
            "var q=document.documentElement.scrollLeft=" + location
        )
        sleep(t)

    def scrollRight(self, location, t=1):

        """2.6 app屏幕右移"""

        # Web_PO.scrollRight('1000', 2)  # 屏幕向右移动1000个像素
        self.driver.execute_script(
            "var q=document.documentElement.scrollRight=" + location
        )
        sleep(t)

    def scrollTop(self, location, t=1):

        """2.7 app屏幕上移"""

        # self.Web_PO.scrollTop("10000",2) # 屏幕向上移动1000个像素
        # self.driver.execute_script("var q=document.body.scrollTop=" + location)
        self.driver.execute_script(
            "var q=document.documentElement.scrollTop=" + location
        )
        sleep(t)

    def scrollDown(self, location, t=1):

        """2.8 app屏幕下移"""

        # self.Web_PO.scrollDown("10000",2) # 屏幕向下移动1000个像素
        self.driver.execute_script(
            "var q=document.documentElement.scrollDown=" + location
        )
        sleep(t)

    def scrollIntoView(self, varXpath, t=1):

        """2.9 元素拖动到可见的元素"""

        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)

    def scrollTopById(self, varId, t=1):

        """2.10 内嵌窗口中滚动条操作"""

        # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
        # self.screenTopId("zy.android.healthstatisticssystem:id/vp_content",2)
        js = "var q=document.getElementById('" + varId + "').scrollTop=100000"
        self.driver.execute_script(js)
        sleep(t)

    def popupAlert(self, text, t=1):

        """3.1 弹出框"""

        # 注意这里需要转义引号
        js = "alert('" + text + "');"
        self.driver.execute_script(js)
        sleep(t)

    def confirmAlert(self, operate, t=1):

        """3.2 确认弹出框"""

        if operate == "accept":
            self.driver.switch_to.alert.accept()
            sleep(t)
        if operate == "dismiss":
            self.driver.switch_to.alert.dismiss()
            sleep(t)
        if operate == "text":
            x = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            return x

    def close(self):

        """4.1 关闭当前窗口"""

        self.driver.close()

    def quit(self):

        """4.2 退出浏览器应用"""

        self.driver.quit()

    def getCode(self, capScrnPic, xStart, yStart, xEnd, yEnd):

        """8 获取验证码 ？？"""

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
        img = img.convert("RGBA")
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


if __name__ == "__main__":

    Web_PO = WebPO("chrome")
    # Web_PO = WebPO("chromeHeadless")
    # Web_PO = WebPO("firefox")

    # # print("1.1 打开网站".center(100, "-"))
    Web_PO.openURL(
        "https://baijiahao.baidu.com/s?id=1753450036624046728&wfr=spider&for=pc"
    )

    # # print("1.2 打开标签页".center(100, "-"))
    # Web_PO.openLabel("http://www.jd.com")

    # # print("1.3 切换标签页".center(100, "-"))
    # Web_PO.switchLabel(0)

    # print("1.4 获取当前浏览器宽高".center(100, "-"))
    # print(Web_PO.getBrowserSize())  # (1536, 824)

    # print("1.5 截取浏览器内屏幕".center(100, "-"))
    # Web_PO.getBrowserScreen("d:/222333browserScreen.png")

    # # print("2.0 指定分辨率浏览器".center(100, "-"))
    Web_PO.setBrowser(1366, 768)

    # # print("2.1 全屏浏览器".center(100, "-"))
    # Web_PO.maxBrowser()

    # # print("2.2 缩放页面比率".center(100, "-"))
    # Web_PO.zoom(20)
    # Web_PO.zoom(220)

    # print("2.3 动态加载页面滚动到底部（加载所有数据）".center(100, "-"))
    # Web_PO.openURL('https://www.douyin.com/user/MS4wLjABAAAARzph2dTaIfZG4w_8czG9Yf5YiqHqc7RGXrqUM3fHtBU?vid=7180299495916326181')
    # qty = Web_PO.dynamicLoadToEnd('Eie04v01')  # 动态加载页面直到最后一个 class=Eie04v01 ,并返回加载的数量。
    # print(qty)
    # text = Web_PO.driver.page_source
    # text = bs4.BeautifulSoup(text, 'lxml')
    # link = text.find_all('a')
    # for a in link:
    #     href = a['href']
    #     if "/video" in href:
    #         print("https://www.douyin.com" + href)

    # # print("2.4 页面滚动条到底部".center(100, "-"))
    # Web_PO.openURL('https://baijiahao.baidu.com/s?id=1753450036624046728&wfr=spider&for=pc')
    # sleep(2)
    # Web_PO.scrollToEnd(2)

    # print("2.5 app屏幕左移".center(100, "-"))
    # Web_PO.scrollLeft('1000',9)

    # print("2.6 app屏幕右移".center(100, "-"))
    # Web_PO.scrollRight('1000', 5)

    # print("2.7 app屏幕上移".center(100, "-"))
    # Web_PO.scrollTop('1000', 5)

    # print("2.8 app屏幕下移".center(100, "-"))
    # Web_PO.scrollDown('1000', 5)

    # print("2.9 元素拖动到可见的元素".center(100, "-"))
    # Web_PO.scrollIntoView(varXpath)

    # print("2.10 内嵌窗口中滚动条操作".center(100, "-"))
    # Web_PO.scrollTopById(varId)

    # # print("3.1 弹出框".center(100, "-"))
    # Web_PO.popupAlert("你好吗？")

    # # print("3.2 确认弹出框".center(100, "-"))
    # Web_PO.confirmAlert("accept", 2)
    # Web_PO.confirmAlert("dismiss", 2)
    # print(Web_PO.confirmAlert("text", 2))

    # print("4.1 关闭当前窗口".center(100, "-"))
    # Web_PO.close()
    #
    # print("4.2 退出浏览器应用".center(100, "-"))
    # Web_PO.quit()
