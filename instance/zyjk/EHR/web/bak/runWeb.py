# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2020-3-11
# Description: web自动化测试框架
# 注意：case.xls中testcase工作本最后一行要用over结束。
# 功能：自动化测试web页面，并将结果记录excel表格。
# 记录内容包括：测试时间（蓝色表示通过，红色表示失败），错误或警告输出内容。
#***************************************************************

import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,numpy
import subprocess,re,pytesseract

from xlutils.copy import copy
from xlwt.Style import *
from xlrd import open_workbook

import base64,mimetypes,email,smtplib
from email.mime.multipart import *
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.header import Header

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from PIL import Image
from time import sleep
from requests.adapters import HTTPAdapter

# from PO.webdriverPO import *
# from instance.zyjk.EHR.config.config import *
# from PO.listPO import *
# list_PO = ListPO()

from instance.zyjk.EHR.PageObject.DataMonitorPO import *
DataMonitor_PO = DataMonitorPO()


class Web(unittest.TestCase):

    def runTest(self):
        pass

    @classmethod
    def setUpClass(self):
        self.Level_PO = Level_PO
        self.varExcel = os.path.abspath(r"case.xls")
        self.varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 获取当天日期时间,格式：20161020130318
        bk = xlrd.open_workbook(varExcel, formatting_info=True)
        self.newbk = copy(bk)
        self.sheetMain = bk.sheet_by_name("main")
        self.sheetTestCase = bk.sheet_by_name("testcase")
        self.styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
        self.styleBlue = xlwt.easyxf('font: name Times New Roman, color-index blue')
        self.styleGray25 = xlwt.easyxf('font: name Times New Roman, color-index gray25')

    @classmethod
    def tearDownClass(self):
        pass

    def test_Main(self):
        for i in range(1, self.sheetMain.nrows):
            if sheetMain.cell_value(i, 0) == "Y":
                self.mainModule = sheetMain.cell_value(i, 1)
                self.readTestcase()

    def readTestcase(self):
        # 遍历TestCase及调用函数模块,定位测试用例位置及数量
        caseEnd = 0
        caseFrom = 0
        for j in range(1, sheetTestCase.nrows):  # 遍历所有记录
            if sheetTestCase.cell_value(j, 2) == self.mainModule:  # 如：判断 module = 登录 的编号
                caseFrom = j
                break
        # print("caseFrom:" + str(caseFrom))

        for j in range(caseFrom + 1, sheetTestCase.nrows):  # 如：遍历从登录记录到结尾的记录
            if j > sheetTestCase.nrows:
                caseEnd = j
            elif sheetTestCase.cell_value(j, 2) != "" :
                caseEnd = j
                break
        # if caseFrom == caseEnd - 1 :
        #     print("\n执行第[" + str(caseFrom + 1) + "]行")
        # else:
        #     print("\n执行第[" + str(caseFrom + 1) + "～" + str(caseEnd) + "]行")


        # 遍历 module 的case
        newWs = newbk.get_sheet(1)
        for l in range(caseFrom, caseEnd):
            try:
                if sheetTestCase.cell_value(l, 1) == "n" or sheetTestCase.cell_value(l, 1) == "N" or sheetTestCase.cell_value(l, 4) == "":
                    pass
                else:
                    print("\nrow " + str(l + 1) + "..................")
                    newWs.write(l, 0, "", styleBlue)  # 清空
                    newWs.write(l, 5, "", styleBlue)  # 清空
                    varResult, varDatetime = eval(sheetTestCase.cell_value(l, 4))
                    if varResult != 1:
                        newWs.write(l, 5, varResult, styleBlue)  # output
                    newWs.write(l, 0, varDatetime, styleBlue)
            except:
                print("[errorrrrrrrrrr],row " + str(l+1) + ", " + str(sheetTestCase.cell_value(caseFrom, 2)) + " - " + str(sheetTestCase.cell_value(l, 3)) + " - " + str(sheetTestCase.cell_value(l, 4)))
                newWs.write(l, 0, varTimeYMDHSM, styleRed)
        newbk.save(varExcel)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def clickMenu(self, varName):

        ''' 点击菜单 '''

        varCount = 0
        d_menu = {}
        l_menu = Level_PO.getXpathsText("//li")
        for i in range(len(l_menu)):
            if l_menu[i] != "":
                varCount = varCount + 1
                d_menu[l_menu[i]] = varCount
                # 打开单或多级菜单
                if l_menu[i] == varName:
                    Level_PO.clickXpath("//ul[@role='menubar']/li[" + str(d_menu[varName]) + "]", 2)
                    break
                # 关闭多级菜单，如 系统管理
                if varName+"\n" in l_menu[i]:
                    Level_PO.clickXpath("//ul[@role='menubar']/li[" + str(varCount) + "]/div", 2)
                    break

    def login(self, varAccount, varPass):

        ''' 登录 '''

        DataMonitor_PO.login(varAccount, varPass)
        varResult = Level_PO.getXpathText("//*[@id='app']/div/div[1]/div[1]/span")
        # 检查
        if varResult == "健康档案数据监测管理系统" :
            print("[ok]")
            return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return "[errorrrrrrrrrr], 无法登录或登录后标题不是健康档案数据监测管理系统", datetime.datetime.now().strftime('%Y%m%d%H%M%S')



    def clickUser(self):

        # 系统管理
        self.clickMenu("系统管理")
        # 用户管理
        Level_PO.clickXpathsContain("//a", "href", '#/system/user', 2)
        print("[ok]")
        return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def getUserList(self):

        # 遍历用户列表
        DataMonitor_PO.user_printList2()
        return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def user_addUser(self, varNewUser, varNewNickName, varNewPhone, varType, varCommunity):

        # 新增用户（用户名，昵称，电话，用户属性，所属社区）
        # 用户属性：家庭医生，家庭医生助理，院长，护士
        # 所属社区：['安亭镇黄渡社区卫生服务中心', '安亭镇社区卫生服务中心', '白鹤社区卫生服务中心', '半淞园街道社区卫生服务中心', '宝山路街道社区卫生服务中心', '堡镇社区卫生服务中心', '北蔡社区卫生服务中心', '北新泾街道社区卫生服务中心', '北站街道社区卫生服务中心', '曹家渡街道社区卫生服务中心', '曹路社区卫生服务中心', '曹杨街道社区卫生服务中心', '漕河泾街道社区卫生服务中心', '漕泾镇社区卫生服务中心', '长白社区卫生服务中心', '长风街道白玉社区卫生服务中心', '长风街道长风社区卫生服务中心', '长桥街道社区卫生服务中心', '长寿街道社区卫生服务中心', '长兴镇社区卫生服务中心', '长征镇社区卫生服务中心', '车墩街道社区卫生服务中心', '陈家镇社区卫生服务中心', '城桥镇社区卫生服务中心', '程家桥街道社区卫生服务中心', '川沙社区卫生服务中心', '打浦桥街道社区卫生服务中心', '大场镇大场社区卫生服务中心', '大场镇第三社区卫生服务中心', '大场镇祁连社区卫生服务中心', '大宁路街道社区卫生服务中心', '大桥社区卫生服务中心', '大团社区卫生服务中心', '定海社区卫生服务中心', '东明社区卫生服务中心', '东平镇社区卫生服务中心', '洞泾镇社区卫生服务中心', '方松街道社区卫生服务中心', '枫泾镇社区卫生服务中心', '枫泾镇兴塔社区卫生服务中心', '枫林街道社区卫生服务中心', '奉城镇社区卫生服务中心', '甘泉街道社区卫生服务中心', '港西镇社区卫生服务中心', '港沿镇社区卫生服务中心', '高东社区卫生服务中心', '高境镇社区卫生服务中心', '高桥社区卫生服务中心', '高行社区卫生服务中心', '共和新路街道社区卫生服务中心', '古美社区卫生服务中心', '顾村镇菊泉新城社区卫生服务中心', '顾村镇社区卫生服务中心', '光明社区卫生服务中心', '广中路街道社区卫生服务中心', '海湾镇社区卫生服务中心', '海湾镇社区卫生服务中心奉新分中心', '航头社区卫生服务中心', '合庆社区卫生服务中心', '横沙乡社区卫生服务中心', '虹梅街道社区卫生服务中心', '虹桥街道社区卫生服务中心', '虹桥社区卫生服务中心', '胡桥社区卫生服务中心', '沪东社区卫生服务中心', '花木社区卫生服务中心', '华漕社区卫生服务中心', '华泾镇社区卫生服务中心', '华新镇社区卫生服务中心', '华阳街道社区卫生服务中心', '淮海中路街道社区卫生服中心', '黄楼社区卫生服务中心', '惠南社区卫生服务中心', '机场社区卫生服务中心', '嘉定工业区社区卫生服务中心', '嘉定区华亭镇社区卫生服务中心', '嘉定区徐行镇社区卫生服务中心', '嘉定区迎园医院/新成街道社区卫生服务中心', '嘉定区真新社区卫生服务中心', '嘉定镇街道社区卫生服务中心', '嘉兴路街道社区卫生服务中心', '建设镇社区卫生服务中心', '江川社区卫生服务中心', '江宁路街道社区卫生服务中心', '江浦社区卫生服务中心', '江桥镇社区卫生服务中心', '江苏街道社区卫生服务中心', '江湾镇街道社区卫生服务中心', '江镇社区卫生服务中心', '金汇镇社区卫生服务中心', '金桥社区卫生服务中心', '金山工业区社区卫生服务中心', '金山卫镇社区卫生服务中心', '金杨社区卫生服务中心', '金泽镇社区卫生服务中心', '静安寺街道社区卫生服务中心', '九亭街道社区卫生服务中心', '菊园社区卫生服务中心', '康健街道社区卫生服务中心', '康桥社区卫生服务中心', '控江社区卫生服务中心', '廊下镇社区卫生服务中心', '老港社区卫生服务中心', '老西门街道社区卫生服务中心', '联洋社区卫生服务中心', '练塘镇社区卫生服务中心', '凉城新村街道社区卫生服务中心', '燎原社区卫生服务中心', '临汾路街道社区卫生服务中心', '凌桥社区卫生服务中心', '凌云街道社区卫生服务中心', '六灶社区卫生服务中心', '龙柏社区卫生服务中心', '龙华街道社区卫生服务中心', '芦潮港社区卫生服务中心', '陆家嘴社区卫生服务中心', '吕巷镇干巷镇社区卫生服务中心', '吕巷镇社区卫生服务中心', '绿华镇社区卫生服务中心', '罗店镇社区卫生服务中心', '罗泾镇社区卫生服务中心', '马陆镇社区卫生服务中心', '马桥社区卫生服务中心', '泖港镇社区卫生服务中心', '梅陇社区卫生服务中心', '庙行镇社区卫生服务中心', '庙镇社区卫生服务中心', '南京东路街道社区卫生服务中心', '南京西路街道社区卫生服务中心', '南码头社区卫生服务中心', '南桥镇社区卫生服务中心', '南桥镇社区卫生服务中心贝港分中心', '南翔镇社区卫生服务中心', '泥城社区卫生服务中心', '欧阳路街道社区卫生服务中心', '彭浦新村街道社区卫生服务中心', '彭浦镇社区卫生服务中心', '平安社区卫生服务中心', '平凉社区卫生服务中心', '浦江社区卫生服务中心', '浦兴社区卫生服务中心', '七宝社区卫生服务中心', '齐贤社区卫生服务中心', '钱桥社区卫生服务中心', '青村镇社区卫生服务中心', '曲阳路街道社区卫生服务中心', '瑞金二路街道社区卫生服务中心', '三林社区卫生服务中心', '三星镇社区卫生服务中心', '山阳镇社区卫生服务中心', '上钢社区卫生服务中心', '上海市白茅岭医院', '上海市军天湖医院', '佘山镇社区卫生服务中心分中心', '石湖荡镇社区卫生服务中心', '石化街道社区卫生服务中心', '石门二路街道社区卫生服务中心', '石泉街道社区卫生服务中心', '书院社区卫生服务中心', '竖新镇社区卫生服务中心', '四川北路街道社区卫生服务中心', '四平社区卫生服务中心', '四团镇社区卫生服务中心', '四团镇社区卫生服务中心邵场分中心', '泗泾街道社区卫生服务中心', '淞南镇社区卫生服务中心', '孙桥社区卫生服务中心', '泰日社区卫生服务中心', '唐镇社区卫生服务中心', '塘桥社区卫生服务中心', '塘外社区卫生服务中心', '桃浦镇社区卫生服务中心', '提篮桥街道社区卫生服务中心', '天目西路街道社区卫生服务中心', '天平街道社区卫生服务中心', '天山社区卫生服务中心', '田林街道社区卫生服务中心', '亭林镇社区卫生服务中心', '头桥社区卫生服务中心', '外冈镇社区卫生服务中心', '外滩街道社区卫生服务中心', '万祥社区卫生服务中心', '王港社区卫生服务中心', '潍坊社区卫生服务中心', '邬桥社区卫生服务中心', '吴泾社区卫生服务中心', '吴淞街道社区卫生服务中心', '五角场街道社区卫生服务中心', '五角场镇社区卫生服务中心', '五里桥街道社区卫生服务中心', '五四社区卫生服务中心', '西渡社区卫生服务中心', '仙霞街道社区卫生服务中心', '香花桥街道社区卫生服务中心', '向化镇社区卫生服务中心', '小东门街道社区卫生服务中心', '小昆山镇社区卫生服务中心', '斜土街道社区卫生服务中心', '莘庄社区卫生服务中心', '新浜镇社区卫生服务中心', '新场社区卫生服务中心', '新村乡社区卫生服务中心', '新海镇社区卫生服务中心', '新河镇社区卫生服务中心', '新虹社区卫生服务中心', '新华街道社区卫生服务中心', '新泾镇社区卫生服务中心', '新桥街道社区卫生服务中心', '新寺社区卫生服务中心', '徐家汇街道社区卫生服务中心', '徐泾镇社区卫生服务中心', '宣桥社区卫生服务中心', '延吉社区卫生服务中心', '杨行镇社区卫生服务中心', '洋泾社区卫生服务中心', '叶榭镇社区卫生服务中心', '宜川街道社区卫生服务中心', '殷行社区卫生服务中心', '迎博社区卫生服务中心', '盈浦街道社区卫生服务中心', '永丰街道社区卫生服务中心', '友谊街道社区卫生服务中心', '豫园街道社区卫生服务中心', '月浦镇盛桥社区卫生服务中心', '月浦镇月浦社区卫生服务中心', '岳阳街道社区卫生服务中心', '张江社区卫生服务中心', '张庙街道长江路社区卫生服务中心', '张庙街道泗塘社区卫生服务中心', '张堰镇社区卫生服务中心', '赵巷镇社区卫生服务中心', '柘林镇社区卫生服务中心', '真如镇社区卫生服务中心', '芷江西路街道社区卫生服务中心', '中山街道社区卫生服务中心', '中兴镇社区卫生服务中心', '重固镇社区卫生服务中心', '周家渡社区卫生服务中心', '周浦社区卫生服务中心', '周桥街道社区卫生服务中心', '朱家角镇社区卫生服务中心', '朱泾社区卫生服务中心', '朱泾镇新农社区卫生服务中心', '祝桥社区卫生服务中心', '颛桥社区卫生服务中心', '庄行镇社区卫生服务中心']
        varStatus1,varResult1 = DataMonitor_PO.user_searchUser("用户名", varNewUser)
        if varStatus1 == 1:
            print(varResult1)
            DataMonitor_PO.user_operateDel(varNewUser)  # 检查并删除已存在的新用户
            varStatus, varResult = DataMonitor_PO.user_addUser(4, varNewUser, varNewNickName, varNewPhone, varType,
                                                               varCommunity)
        else:
            varStatus, varResult = DataMonitor_PO.user_addUser(3,varNewUser, varNewNickName, varNewPhone, varType, varCommunity)
        if varStatus == 1:
            print(varResult)
            return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return varResult, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def user_searchKey(self, varType, varContent):

        # 分别搜用户名、昵称、手机
        varStatus, varResult = DataMonitor_PO.user_searchUser(varType, varContent)
        if varStatus == 1:
            print(varResult)
            return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return varResult, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def user_optRole(self, varUser, *varRole):

        # 搜索用户名，操作角色，勾选3个角色
        # 角色：超级管理员，社区机构管理员，家庭医生，ai核对管理员，档案查看管理员
        varStatus, varResult = DataMonitor_PO.user_operateRole(varUser, *varRole)
        if varStatus == 1:
            print(varResult)
            return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return varResult, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def user_optEdit(self, varUser, varUser2, varNickName2, varPhone2, varType2, varCommunity2):

        # ？开发bug，编辑后会刷新页面导致提示2次（成功及无数据），用户体验不好，自动化会报错，找不到数据。
        # 搜索用户名并编辑用户
        varStatus, varResult = DataMonitor_PO.user_operateEdit(varUser, varUser2, varNickName2, varPhone2, varType2, varCommunity2)
        if varStatus == 1:
            print(varResult)
            return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return varResult, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def user_optDele(self, varUser):

        # 搜索用户并删除用户
        varStatus, varResult = DataMonitor_PO.user_operateDel(varUser)
        if varStatus == 1:
            print(varResult)
            return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            return varResult, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def clickHome(self):

        # 首页
        self.clickMenu("首页")
        print("[ok]")
        return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def getMark(self):

        # 获取总体指标分布
        a = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]")
        b = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div/div[2]")
        c = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div/div[2]")
        d = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div[4]/div/div[2]")
        e = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div[5]/div/div[2]")
        f = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div[6]/div/div[2]")
        print("常驻人口：" + str(a))
        print("户籍人口：" + str(b))
        print("目标建档总数：" + str(c))
        print("实际建档总数：" + str(d))
        print("合格建档总数：" + str(e))
        print("更新建档总数：" + str(f))

        g = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/div[2]")
        h = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div[2]")
        i = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div[3]/div[1]/div/div[2]")
        j = Level_PO.getXpathText("//*[@id='app']/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div[4]/div[1]/div/div[2]")
        hjrkzb = '%.2f' % (int(b)/int(a)*100)
        if float(hjrkzb) == float(g.split("%")[0]) :
            print("户籍人口占比：" + str(g))
        else:
            print("户籍人口占比实测值：" + str(hjrkzb) + "%，显示值：" + str(g))

        sjjdl = '%.2f' % (int(d) / int(a) * 100)
        if float(sjjdl) == float(h.split("%")[0]):
            print("实际建档率：" + str(h))
        else:
            print("实际建档率实测值：" + str(sjjdl) + "%，显示值：" + str(h))

        dahgl = '%.2f' % (int(e) / int(d) * 100)
        if float(dahgl) == float(i.split("%")[0]):
            print("档案合格率：" + str(i))
        else:
            print("档案合格率实测值：" + str(dahgl) + "%，显示值：" + str(i))

        dagxl = '%.2f' % (int(f) / int(d) * 100)
        if float(dagxl) == float(j.split("%")[0]):
            print("档案更新率：" + str(j))
        else:
            print("档案更新率实测值：" + str(dagxl) + "%，显示值：" + str(j))


        return 1, datetime.datetime.now().strftime('%Y%m%d%H%M%S')


    def qcAnalysis_optRuleType(self, varExcelNum, *varRules):

        # 档案数据质控分析
        # 查询档案，操作问题档案
        Level_PO.clickXpath("//input[@placeholder='请选择']", 2)  # 定位第一下拉框
        #
        # x= Level_PO.getXpathsText("//li/span")
        # for i in range(len(x)):
        #     if "-" not in x[i]:
        #         x.pop(0)
        # print(x)

        Level_PO.clickXpath("//body/div[@类与实例='el-select-dropdown el-popper is-multiple']/div[1]/div[1]/ul/li[1]", 2)  # 选择第1个  li[1]
        Level_PO.clickXpath("//button[@类与实例='el-button el-button--primary']", 2)  # 查找
        Level_PO.clickXpath("//button[@类与实例='el-button el-button--text el-button--small']", 2)  # 操作详情
        # 问题档案列表之 规则类型勾选
        for i in range(len(varRules)):
            Level_PO.clickXpathsNum("//span[@aria-checked='mixed']", varRules[i], 2)  # 勾选第？个
        sleep(4)

        # 勾选规则后，页面自动匹配显示符合条件的问题档案列表，并点击第一条记录
        l_data = Level_PO.getXpathsText("//div[@类与实例='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div")
        x = int(len(l_data) / 9)
        l_record = numpy.array_split(l_data, x)
        l_title = ['操作:', '档案编号:', '姓名:', '社区医院:', '表单名称:', '字段名称:', '规则类型:', '错误描述:']
        l_merge = [i + j for i, j in zip(l_title, l_record[0])]
        # print(l_merge)
        c = list_PO.alignmentKey(l_merge, ":")
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

        Level_PO.clickXpathsNum("//div[@类与实例='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 1, 2)  # 点击 第一条记录
        # Level_PO.clickXpathsNum("//div[@类与实例='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 10, 2)  #  点击 第二条记录
        # Level_PO.clickXpathsNum("//div[@类与实例='tableTemplate']/div[2]/div[1]/div/div/div/div/div/div", 19, 2)  # 点击 第三条记录

    def qcAnalysis_cover(self, varExcelNum):
        print("\n【健康档案封面】")
        Level_PO.clickId("tab-0", 2)  # 健康档案封面
        l_data = Level_PO.getXpathsText("//div[@id='pane-0']/div/div/div/div[1]/div/div/div")
        l_data.pop(0)
        c = list_PO.alignmentKey(l_data, ":\n")  # 将记录信息保存到excel
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

    def qcAnalysis_person(self, varExcelNum, varTitle, varSplit):
        print("\n" + varTitle)
        l_data = []
        c = []
        Level_PO.clickId("tab-1", 2)  # 个人基本信息表
        l_data = Level_PO.getXpathsText("//div[@id='pane-1']/div/div/div/div[1]/div/div/div")
        l_data.pop(0)
        if varTitle == "\n【个人基本信息表 - 生活环境】":
            c = list_PO.alignmentKey(l_data, ":\n")
        else:
            # 合并
            l_temp = []
            for i in range(0, len(l_data)):
                if varSplit != l_data[i]:
                    l_temp.append(l_data[i])
                else:
                    for j in range(i):
                        l_data.pop(0)
                    l_data.pop(0)
                    break
            l_temp.pop()
            if varSplit == "家族史" or varSplit == "遗传病史" or varSplit == "残疾情况" or varSplit == "生活环境" or varSplit == "反面":
                c = list_PO.alignmentKey(l_temp, ":\n")
            else:
                l_temp = list_PO.elementMerge(l_temp, 3)
                c = list_PO.alignmentKey(l_temp, ":")
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

    def qcAnalysis_arichive(self ,varExcelNum):
        print("\n【档案信息卡 - 正面反面】")
        Level_PO.clickId("tab-3", 2)  # 档案信息卡
        list1 = Level_PO.getXpathsText("//div[@id='pane-3']/form/div/div[1]/div/div/div")
        l11 = []
        l22 = []
        l33 = []
        for i in range(len(list1)):
            if list1[i].count(":\n") > 0:
                l11.append(list1[i].split("\n"))
        for i in range(len(l11)):
            l22 = list_PO.elementMerge(l11[i], 2)
            l33 = l33 + l22
        c = list_PO.alignmentKey(l33, ":")
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, c, styleBlue)
        newbk.save(varExcel)

    def qcAnalysis_project(self,varExcelNum):
        print("\n【质控项目汇总 - 个人基本信息表】")
        l_person1 = Level_PO.getXpathText("//div[@类与实例='main']/div[1]/div[2]/div[1]")
        l_person1Value = Level_PO.getXpathText("//div[@类与实例='main']/div[1]/div[2]/div[2]")
        # print(l_person1)
        # print(l_person1Value)
        newWs = newbk.get_sheet(1)
        newWs.write(varExcelNum, 5, l_person1Value, styleBlue)
        newbk.save(varExcel)

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Web)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

