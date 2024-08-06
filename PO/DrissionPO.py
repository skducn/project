# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2024-8-6
# Description   : drissionPage 浏览器封装 控制浏览器或收发数据包。
# https://www.drissionpage.cn/get_start/installation
# pip install DrissionPage
# pip install DrissionPage --upgrade
# pip install DrissionPage==4.0.0b17
# 导入 https://www.drissionpage.cn/get_start/import
# *********************************************************************
# 控制浏览器
from DrissionPage import ChromiumPage
# 动作链，用于执行一系列动作。
# 在浏览器页面对象中已有内置，无如特殊需要无需主动导入。
from DrissionPage.common import Actions

# 只要收发数据包，导入SessionPage。
from DrissionPage import SessionPage

# 既可控制浏览器，也可收发数据包。
from DrissionPage import WebPage

# 键盘按键类，用于键入 ctrl、alt 等按键。
from DrissionPage.common import Keys

# 与 selenium 一致的By类，便于项目迁移。
from DrissionPage.common import By

# wait_until：可等待传入的方法结果为真
# make_session_ele：从 html 文本生成ChromiumElement对象
# configs_to_here：把配置文件复制到当前路径
# get_blob：获取指定的 blob 资源
# tree：用于打印页面对象或元素对象结构
# from_selenium：用于对接 selenium 代码
# from_playwright：用于对接 playwright 代码
from DrissionPage.common import wait_until
from DrissionPage.common import make_session_ele
from DrissionPage.common import configs_to_here


class DrissionPO:

    def open(self, varUrl):
        self.page = ChromiumPage()
        self.page.get(varUrl)

    def set(self, varId, varValue):
        ele = self.page.ele(varId)
        ele.input(varValue)

    def clk(self, varId):
        self.page.ele(varId).click()




if __name__ == "__main__":

    Drission_PO = DrissionPO()

    # Drission_PO.open('https://gitee.com/login')
    # Drission_PO.set('#user_login', '您的账号')
    # Drission_PO.set('#user_password', '您的账号')
    # Drission_PO.clk('@value=登 录')


    # page = SessionPage()

    # # 爬取3页
    # for i in range(1, 3):
    #     # 访问某一页的网页
    #     page.get(f'https://gitee.com/explore/all?page={i}')
    #     # 获取所有开源库<a>元素列表
    #     links = page.eles('.title project-namespace-path')
    #     # 遍历所有<a>元素
    #     for link in links:
    #         # 打印链接信息
    #         # .text获取元素的文本，.link获取元素的href或src属性。
    #         print(link.text, link.link)

    # 创建页面对象
    page = WebPage()
    # 访问网址
    page.get('https://gitee.com/explore')
    page('#q').input('DrissionPage')
    page('t:button@tx():搜索').click()
    page.wait.load_start()
    # 切换到收发数据包模式
    page.change_mode()
    items = page.ele('.results mt-3').eles('.card border-1 mb-3')
    # from DrissionPage.common import By
    #
    #
    #
    # # 按 xpath 查找
    # loc2 = (By.XPATH, '//a[@class="p_cls"]')
    # ele = page.ele(loc2)
    #
    # # 获取所有行元素
    # items = page.ele('.results mt-3').eles('.card-body')

    # 遍历获取到的元素
    for item in items:
        # 打印元素文本
        print(item('.gvp').text)
        # print(item('.project-desc mb-1').text)
        print()