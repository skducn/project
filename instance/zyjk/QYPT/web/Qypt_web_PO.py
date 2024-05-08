# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2024-5-8
# Description: https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.WebPO import *
Web_PO = WebPO("chrome")


class Qypt_web_PO():

    def clsApp(self, varApp):

        '''
        关闭应用程序
        :param varApp:
        :return:
         # clsApp("chrome.exe")
         clsApp("Google Chrome")
        '''

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def login(self, varUrl, varUser, varPass):

        # 登录
        Web_PO.openURL(varUrl)
        Web_PO.setText("/html/body/div[1]/div/div/div[1]/div[2]/form/div/div[1]/label/div/div/div[1]/input", varUser)
        Web_PO.setText("/html/body/div[1]/div/div/div[1]/div[2]/form/div/div[2]/label/div/div/div/input", varPass)
        Web_PO.clk("/html/body/div[1]/div/div/div[1]/div[2]/form/div/button", 2)

    def clkApp(self, varAppName):

        # 打开应用并获取菜单和url

        # 遍历获取应用
        l_appname = Web_PO.getTexts("/html/body/div/section/section/main/div[2]/div[2]/div/div[2]/div[1]")
        l_appcode = Web_PO.getValuesByAttr("/html/body/div/section/section/main/div[2]/div[2]/div", "id")
        d_applist = dict(zip(l_appname, l_appcode))
        # print(d_applist)
        for k, v in d_applist.items():
            if k == varAppName:

                # 进入应用并切换新页面
                Web_PO.clkById(v, 2)
                Web_PO.swhLabel(1)

                # 获取菜单链接
                l_memuUrl = Web_PO.getValuesByAttr("//a", "href")
                # print(l_memuUrl)
                # 展开所有菜单（去掉display：none）
                Web_PO.jsDisplayByTagName("ul", len(l_memuUrl))

                # 获取菜单名称
                l_menu = Web_PO.getTexts("//a/li/span")
                # print(l_menu)

                # 合并菜单与URL
                d_menuUrl = dict(zip(l_menu, l_memuUrl))

                return d_menuUrl
