# -*- coding: utf-8 -*-

# 导入依赖包
import scrapy
from selenium import webdriver
import time
import json


# 构建spider自动生成的基本配置
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    # 模拟请求的headers，非常重要，不设置也可能知乎不让你访问请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "HOST": "www.zhihu.com"
    }

    # 第一步：使用selenium登录知乎并获取登录后的cookies，cookies没失效时，只要初次请求执行一次
    def loginZhihu(self):
        # 登录网址
        loginurl = 'https://www.zhihu.com/signin'
        # 加载webdriver驱动，用于获取登录页面标签属性
        driver = webdriver.Chrome()

        # driver = webdriver.Firefox(executable_path='C:\Python37\Scripts\geckodriver', firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, firefox_options=None)

        driver.get(loginurl)

        # 方式1 通过填充用户名和密码
        driver.find_element_by_name('username').clear()  # 获取用户名框
        driver.find_element_by_name('username').send_keys(u'13816109050')  # 填充用户名
        driver.find_element_by_name('password').clear()  # 获取密码框
        driver.find_element_by_name('password').send_keys(u'jinhao80')  # 填充密码
        time.sleep(3)  # 执行休眠10s等待浏览器的加载
        # input("检查网页是否有验证码要输入，有就在网页输入验证码，输入完后在编辑器中回车；如果无验证码，则直接回车")
        # 非常关键，有时候知乎会在输入密码后弹出验证码，这一步可将代码执行暂时停滞
        # driver.find_element_by_css_selector("button[class='Button SignFlow-submitButton Button--primary Button--blue']").click()    # 点击登录按钮

        # # 方式2 直接通过扫描二维码，如果不是要求全自动化，建议用这个，非常直接
        # # 毕竟我们这一步只是想保存登录后的cookies，至于用何种方式登录，可以不必过于计较
        # time.sleep(10)  # 同样休眠10s等待页面
        # input("请页面二维码，并确认登录后，点击回车：")  # 点击二维码手机扫描登录

        # 通过上述的方式实现登录后，其实我们的cookies在浏览器中已经有了，我们要做的就是获取
        cookies = driver.get_cookies()  # Selenium为我们提供了get_cookies来获取登录cookies
        driver.close()  # 获取cookies便可以关闭浏览器
        # 然后的关键就是保存cookies，之后请求从文件中读取cookies就可以省去每次都要登录一次的
        # 当然可以把cookies返回回去，但是之后的每次请求都要先执行一次login没有发挥cookies的作用
        jsonCookies = json.dumps(cookies)  # 通过json将cookies写入文件
        with open('zhihuCookies.json', 'w') as f:
            f.write(jsonCookies)
        print(cookies)
        # return cookies

    # Scrapy使用保存ookies请求发现模块，看是否是登录之后的状态
    def question(self, response):
        with open('zhihu_find.html', 'w', encoding='utf-8') as f:
            f.write(response.text)  # 写入文件，保存成.html文件
        pass

    def parse(self, response):
        pass

    # scrapy请求的开始时start_request
    def start_requests(self):
        zhihu_findUrl = 'https://www.zhihu.com/explore'
        self.loginZhihu()  # 首次使用，先执行login，保存cookies之后便可以注释，
        # 毕竟每次执行都要登录还是挺麻烦的，我们要充分利用cookies的作用
        # 从文件中获取保存的cookies
        with open('zhihuCookies.json', 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())  # 获取cookies
        # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']
        print(cookies_dict)
        # Scrapy发起其他页面请求时，带上cookies=cookies_dict即可，同时记得带上header值，
        yield scrapy.Request(url=zhihu_findUrl, cookies=cookies_dict, callback=self.question, headers=self.headers)

if __name__=='__mai__':
    x =ZhihuSpider
    x.loginZhihu()