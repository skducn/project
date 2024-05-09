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
        Web_PO.setTextByX("/html/body/div[1]/div/div/div[1]/div[2]/form/div/div[1]/label/div/div/div[1]/input", varUser)
        Web_PO.setTextByX("/html/body/div[1]/div/div/div[1]/div[2]/form/div/div[2]/label/div/div/div/input", varPass)
        Web_PO.clkByX("/html/body/div[1]/div/div/div[1]/div[2]/form/div/button", 2)

    def clkApp(self, varAppName):

        # 打开应用并获取菜单和url

        # 遍历获取应用
        l_appname = Web_PO.getTextListByX("/html/body/div/section/section/main/div[2]/div[2]/div/div[2]/div[1]")
        l_appcode = Web_PO.getAttrValueListByX("/html/body/div/section/section/main/div[2]/div[2]/div", "id")
        d_applist = dict(zip(l_appname, l_appcode))
        # print(d_applist)
        for k, v in d_applist.items():
            if k == varAppName:

                # 进入应用并切换新页面
                Web_PO.clkById(v, 2)
                Web_PO.swhLabel(1)

                # 获取菜单链接
                l_memuUrl = Web_PO.getAttrValueListByX("//a", "href")
                # print(l_memuUrl)
                # 展开所有菜单（去掉display：none）
                Web_PO.clsDisplayByTagName("ul", len(l_memuUrl))

                # 获取菜单名称
                l_menu = Web_PO.getTextListByX("//a/li/span")
                # print(l_menu)

                # 合并菜单与URL
                d_menuUrl = dict(zip(l_menu, l_memuUrl))

                return d_menuUrl

    # todo 平台管理系统
    def _userManager_Search(self, varOrganizationByX, varStatusByX, varOrganization, varStatus):
        """通用操作"""
        # 选择所属机构
        Web_PO.clkByX(varOrganizationByX)
        l1 = Web_PO.getTextListByX("/html/body/div[3]/div[1]/div[1]/ul")
        l2 = l1[0].split("\n")
        # print(l2)
        d = dict(enumerate(l2, start=1))
        d = {v: k for k, v in d.items()}
        # print(d)
        Web_PO.clkByX("/html/body/div[3]/div[1]/div[1]/ul/li[" + str(d[varOrganization]) + "]")

        # 选择状态
        Web_PO.clkByX(varStatusByX)
        if varStatus == "禁用":
            Web_PO.clkByX("/html/body/div[4]/div[1]/div[1]/ul/li[1]")
        elif varStatus == "启用":
            Web_PO.clkByX("/html/body/div[4]/div[1]/div[1]/ul/li[2]")
        elif varStatus == "限制登录":
            Web_PO.clkByX("/html/body/div[4]/div[1]/div[1]/ul/li[3]")

    def platformManagement_userManagement_search(self, varOption, varValue, varOrganization, varStatus):
        """平台管理系统 - 权限管理 - 用户管理 - 搜索"""
        # Web_PO.userManager_Search("登录名", "mql", "招远市妇幼医院", "启用")

        # 1，选择登录名、用户工号、用户姓名
        # 获取所属机构xpath
        varOrganizationByX = "/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/div[5]/div/div/div/input"
        # 获取状态xpath
        varStatusByX = "/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/div[6]/div/div/div/input"
        if varOption == "登录名":
            Web_PO.clkByX("//input[@placeholder='请选择']")
            Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[1]")
            Web_PO.setTextByX("//input[@placeholder='登录名']", varValue)
        elif varOption == "用户工号":
            Web_PO.clkByX("//input[@placeholder='请选择']")
            Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[2]")
            Web_PO.setTextByX("//input[@placeholder='用户工号']", varValue)
            # 获取所属机构xpath
            varOrganizationByX = "/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/div[4]/div/div/div/input"
            # 获取状态xpath
            varStatusByX = "/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/div[5]/div/div/div/input"
        elif varOption == "用户姓名":
            Web_PO.clkByX("//input[@placeholder='请选择']")
            Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[3]")
            Web_PO.setTextByX("//input[@placeholder='用户姓名']", varValue)
            # 获取所属机构xpath
            varOrganizationByX = "/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/div[4]/div/div/div/input"
            # 获取状态xpath
            varStatusByX = "/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/div[5]/div/div/div/input"
        else:
            print("[warning], 平台管理系统 => 权限管理 => 用户管理 => 第一个下拉框中没有'" + varOption + "'选项！")
            sys.exit(0)

        # 2，选择所属机构和选择状态
        self._userManager_Search(varOrganizationByX, varStatusByX, varOrganization, varStatus)

        # 3，点击搜索
        Web_PO.clkByX("/html/body/div[1]/section/div/section/section/main/div[2]/section/header/form/div/button", 2)

        # 4，获取结果并返回
        result = Web_PO.getTextByX("//span[@class='el-pagination__total']")
        if result == "共 1 条":
            print("[ok], 共 1 条")
        else:
            print("[errorrrrrr], " + result)

    # todo 主数据管理
    def mainDataManagement_orgManagement_search(self, d_search):
        """主数据管理 - 机构管理 - 搜索"""

        # 机构名称
        Web_PO.setTextByX("/html/body/div/section/section/section/main/div[2]/section/header/form/div/div[1]/div/div/div/input", d_search['机构名称'])

        # 机构类别
        if d_search['机构类别'] != "":
            Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/header/form/div/div[2]/div/div/div/div/input", 2)
            l1 = Web_PO.getTextListByX("/html/body/div[2]/div[1]/div[1]/ul")
            l2 = l1[0].split("\n")
            d = dict(enumerate(l2, start=1))
            d = {v: k for k, v in d.items()}
            Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[" + str(d[d_search['机构类别']]) + "]")

        # 所属街道
        if d_search['所属街道'] != "":
            Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/header/form/div/div[3]/div/div/div/div[1]/input", 2)
            if Web_PO.isBooleanAttr("/html/body/div[2]", "x-placement"):
                l1 = Web_PO.getTextListByX("/html/body/div[2]/div[1]/div[1]/ul")
                l2 = l1[0].split("\n")
                d = dict(enumerate(l2, start=1))
                d = {v: k for k, v in d.items()}
                Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[" + str(d[d_search['所属街道']]) + "]")
            if Web_PO.isBooleanAttr("/html/body/div[3]", "x-placement"):
                l1 = Web_PO.getTextListByX("/html/body/div[3]/div[1]/div[1]/ul")
                l2 = l1[0].split("\n")
                d = dict(enumerate(l2, start=1))
                d = {v: k for k, v in d.items()}
                Web_PO.clkByX("/html/body/div[3]/div[1]/div[1]/ul/li[" + str(d[d_search['所属街道']]) + "]")
        # 状态
        if d_search['状态'] != "":
            Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/header/form/div/div[4]/div/div/div/div/input", 2)
            if Web_PO.isBooleanAttr("/html/body/div[2]", "x-placement"):
                if d_search['状态'] == "启用":
                    Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[1]")
                elif d_search['状态'] == "停用":
                    Web_PO.clkByX("/html/body/div[2]/div[1]/div[1]/ul/li[2]")
            elif Web_PO.isBooleanAttr("/html/body/div[3]", "x-placement"):
                if d_search['状态'] == "启用":
                    Web_PO.clkByX("/html/body/div[3]/div[1]/div[1]/ul/li[1]")
                elif d_search['状态'] == "停用":
                    Web_PO.clkByX("/html/body/div[3]/div[1]/div[1]/ul/li[2]")
            elif Web_PO.isBooleanAttr("/html/body/div[4]", "x-placement"):
                if d_search['状态'] == "启用":
                    Web_PO.clkByX("/html/body/div[4]/div[1]/div[1]/ul/li[1]")
                elif d_search['状态'] == "停用":
                    Web_PO.clkByX("/html/body/div[4]/div[1]/div[1]/ul/li[2]")
        # 点击搜索
        Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/header/form/div/div[5]/div/div/button", 2)

    def mainDataManagement_orgManagement_revise(self, varStatus, d_reviseContent, varDelete):
        """主数据管理 - 机构管理 - 修改"""

        # 修改状态
        statusAttrValue = Web_PO.getAttrValueByX("/html/body/div[1]/section/section/section/main/div[2]/section/main/div/div[3]/table/tbody/tr/td[6]/div/div", "class")
        # print(statusAttrValue)
        if statusAttrValue == "el-switch is-checked" and varStatus == "停用":
            Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/main/div/div[3]/table/tbody/tr/td[6]/div/div")
        elif statusAttrValue == "el-switch" and varStatus == "启用":
            Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/main/div/div[3]/table/tbody/tr/td[6]/div/div")

        # # 点击修改
        Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/main/div/div[3]/table/tbody/tr/td[7]/div/button[1]")
        Web_PO.setTextByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/form/div[1]/div/div/input", d_reviseContent['机构名称'])
        Web_PO.setTextByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/form/div[3]/div/div/input", d_reviseContent['招远市医疗机构代码'])
        # 机构类别
        Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/form/div[4]/div/div/div[1]/input")
        l1 = Web_PO.getTextListByX("/html/body/div[6]/div[1]/div[1]/ul")
        l2 = l1[0].split("\n")
        d = dict(enumerate(l2, start=1))
        d = {v: k for k, v in d.items()}
        Web_PO.clkByX("/html/body/div[6]/div[1]/div[1]/ul/li[" + str(d[d_reviseContent['机构类别']]) + "]")

        # 所属街道
        Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/form/div[5]/div/div[2]/div[1]/input")
        l1 = Web_PO.getTextListByX("/html/body/div[7]/div[1]/div[1]/ul")
        l2 = l1[0].split("\n")
        d = dict(enumerate(l2, start=1))
        d = {v: k for k, v in d.items()}
        Web_PO.clkByX("/html/body/div[7]/div[1]/div[1]/ul/li[" + str(d[d_reviseContent['所属街道']]) + "]")

        Web_PO.setTextByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/form/div[6]/div/div/input", d_reviseContent['机构地址'])
        # 状态
        Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/form/div[7]/div/div/div[1]/input")
        if d_reviseContent['状态'] == "启用":
            Web_PO.clkByX("/html/body/div[8]/div[1]/div[1]/ul/li[1]")
        elif d_reviseContent['状态'] == "停用":
            Web_PO.clkByX("/html/body/div[8]/div[1]/div[1]/ul/li[2]")
        sleep(12123)
        # 保存
        Web_PO.clkByX("/html/body/div[1]/section/section/section/main/div[2]/section/div[2]/div/div[2]/div/div/button[1]", 2)

        # 验证修改
        orgName = Web_PO.getTextByX("/html/body/div[1]/section/section/section/main/div[2]/section/main/div/div[3]/table/tbody/tr/td[1]")
        if orgName == d_reviseContent['机构名称']:
            print("ok")
        else:
            print("error", orgName)


        # 点击删除
