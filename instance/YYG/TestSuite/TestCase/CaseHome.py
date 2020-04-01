# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 任务调度引擎管理客户端入口 Cos
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# from Cos.TestSuite.run1 import *
# from CaseTaskManage import CaseTaskManage


from Cos.Config.config import *
from Cos.PageObject.TaskManagePO import *

import unittest

# TaskManage_PO = TaskManagePO(driver, sheetMain.cell_value(1, 5), sheetMain.cell_value(3, 5))

# conn = MySQLdb.connect(host="10.111.3.16", user='developer', passwd='developer', db='QuartzDB_Run', port=3306, use_unicode=True)
# cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')

# xx = u"\\\\task25190_1237598.zip"
# print xx
# cur.execute('select id from task_version where package_path="%s" order by id desc limit 1' % (xx))
# t4 = cur.fetchone()
# print t4[0]



# import sys, unittest, os, xlwt, xlrd, MySQLdb
# from xlutils.copy import copy
# reload(sys)
# sys.setdefaultencoding("utf-8")
# from selenium import webdriver
# from Public.PageObject.LevelPO import *
#
# # varExcel = os.path.abspath(r"../TestData/Cos.xls")  # run1, 批量跑
# # varExcel = os.path.abspath(r"../../TestData/Cos.xls")  # 单独运行
# varExcel = os.path.abspath(r"/Users/linghuchong/Downloads/51/Project/Cos/TestData/Cos.xls")  # run1, 批量跑
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# sheetParam = bk.sheet_by_name("param")
# styleRed = xlwt.easyxf('font: name Times New Roman, color-index red')
#
# conn = MySQLdb.connect(host='10.111.3.16', user='developer', passwd='developer', db='QuartzDB', port=3306, use_unicode=True)
# cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')
#
# driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver5.log')
# driver.implicitly_wait(10)
# Level_PO = LevelPO(driver, sheetParam.cell_value(1, 1), sheetParam.cell_value(2, 1))
#

class CaseHome(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C1，登录"

    def test1(self):
        for i in range(1, sheetMain.nrows):
            if sheetMain.cell_value(i, 0) == "Y":
                self.Maincol1 = sheetMain.cell_value(i, 1)
                self.Maincol2 = sheetMain.cell_value(i, 2)
                exec (sheetMain.cell_value(i, 4))

    def TestcaseModule(self):
        # 遍历TestCase及调用函数模块,定位测试用例位置及数量
        case1 = caseN = 0
        for j in range(1, sheetTestCase.nrows):
            case1 = case1 + 1
            if sheetTestCase.cell_value(j, 2) == self.Maincol1:
                for k in range(case1 + 1, 100):  # 假设有100个Case
                    if k + 1 > sheetTestCase.nrows:  # 最后一行
                        caseN = caseN + 1
                        break
                    elif sheetTestCase.cell_value(k, 1) == "" and sheetTestCase.cell_value(k, 2) == "":
                        caseN = caseN + 1
                    elif sheetTestCase.cell_value(k, 1) == "skip":
                        caseN = caseN + 1
                    else:
                        caseN = caseN + 1
                        break
                break
        if self.Maincol2 == "skip":
            case1 = case1 + 1
            caseN = caseN - 1

        # 遍历 Testcase1~TestCaseN
        for l in range(case1, caseN + case1):
            str_list = []
            for m in range(7, 30):  # id0 - id16
                if sheetTestCase.cell(l, m).value != "":
                    N = sheetTestCase.cell_value(l, m)
                    if "=" in N:
                        N = sheetMain.cell_value(1, 5) + ":" + N
                    str_list.append(str(N))
                else:
                    break
            self.str_list = str_list
            try:
                if sheetTestCase.cell_value(l, 1) == "skip":
                    newWs = newbk.get_sheet(1)
                    newWs.write(l, 0, "skip", styleGray25)
                    newbk.save(varExcel)
                elif sheetTestCase.cell_value(l, 5) == "":
                    pass
                else:
                    self.l = l
                    exec (sheetTestCase.cell_value(l, 5))
                    newWs = newbk.get_sheet(1)
                    newWs.write(l, 0, varTimeYMDHSM, styleBlue)
                    newbk.save(varExcel)
            except:
                print "Errorrrrrrr , Excel(" + str(l + 1) + ") , " + sheetTestCase.cell_value(case1,
                                                                                              2) + " , " + sheetTestCase.cell_value(
                    l, 3) + " , " + sheetTestCase.cell_value(l, 4) + " , " + sheetTestCase.cell_value(l, 5)
                newWs = newbk.get_sheet(1)
                newWs.write(l, 0, varTimeYMDHSM, styleRed)
                newbk.save(varExcel)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # 登录
    def drv_login(self):
        self.TestcaseModule()
        sleep(2)

    def login(self, varUser, varPass):
        # C1-1,登录系统
        Level_PO.open(3)
        Level_PO.inputID('_username', varUser)
        Level_PO.inputNAME('password', varPass)
        Level_PO.clickTAGNAME('button', 4)
        # admin,您好
        # Level_PO.printIDXPATH('navbar',"//ul[@class='nav navbar-top-links navbar-right']/li")
        print u"OK - C0,登录系统"



    # 首页
    def drv_home(self):
        self.TestcaseModule()
        sleep(2)

    def homeElement(self):
        # C1-2,检查页面元素（菜单、宿主状态、作业状态）
        # 打印 菜单
        Level_PO.printIDXPATH('navbar',"//ul/li")
        print "------------"
        Level_PO.printIDXPATH('navbar', "//ul/li[2]")
        Level_PO.clickLINKTEXT(u'作业管理',2)
        Level_PO.printIDXPATH('navbar', "//ul/li[2]/ul/li")
        print "------------"
        Level_PO.printIDXPATH('navbar', "//ul/li[3]")
        Level_PO.clickLINKTEXT(u'版本管理', 2)
        Level_PO.printIDXPATH('navbar', "//ul/li[3]/ul/li[1]")
        Level_PO.printIDXPATH('navbar', "//ul/li[3]/ul/li[2]")
        print "------------"
        Level_PO.printIDXPATH('navbar', "//ul/li[4]")
        Level_PO.clickLINKTEXT(u'宿主管理', 2)
        Level_PO.printIDXPATH('navbar', "//ul/li[4]/ul/li")
        print "------------"
        Level_PO.printIDXPATH('navbar', "//ul/li[5]")
        Level_PO.clickLINKTEXT(u'日志管理', 2)
        Level_PO.printIDXPATH('navbar', "//ul/li[5]/ul/li[1]")
        Level_PO.printIDXPATH('navbar', "//ul/li[5]/ul/li[2]")
        Level_PO.printIDXPATH('navbar', "//ul/li[5]/ul/li[3]")
        print "------------"
        Level_PO.printIDXPATH('navbar', "//ul/li[6]")
        Level_PO.clickLINKTEXT(u'用户管理', 2)
        Level_PO.printIDXPATH('navbar', "//ul/li[6]/ul/li[1]")
        Level_PO.printIDXPATH('navbar', "//ul/li[6]/ul/li[2]")
        Level_PO.printIDXPATH('navbar', "//ul/li[6]/ul/li[3]")
        print "-----------------------------"
        # # 打印 "当前引擎内部共连接 0 台宿主机，正在进行 0 个作业调度"
        Level_PO.printXPATH("//h5")

        # 遍历显示所有的宿主状态与作业状态
        Level_PO.printTRTD("//tr")

    def homeSearchTask(self, varHost):
        # C1-3,搜索作业,# 选择任意一个宿主名称后进行搜索作业

        # [宿主状态]
        # 刷新
        Level_PO.clickXPATH("//button[@onclick=\"refresh()\"]", 2)

        # 选择一个宿主，进行搜索作业
        varSelect = Level_PO.get_selectRadio("//div[@class='right_content_fff']/div[1]/div[2]/div[1]/div[1]/div[3]/table/tbody/tr", varHost)
        Level_PO.clickXPATH("//input[@id='" + varSelect + "']", 2)
        # 搜索作业
        Level_PO.clickXPATH("//button[@onclick=\"searchJob()\"]", 2)

    def homeTaskStatus(self, varHost, varNum):
        # C1-4,操作作业，选择任意一个作业后进行操作（启动，暂停，恢复，停止，强制停止）
        # # [作业状态]

        # 1,选择指定宿主中第几个作业名称，如果输入的个数不存在，则默认是当前页最后一个作业名称。
        varSelectID = Level_PO.get_selectRadio("//div[@class='right_content_fff']/div[1]/div[2]/div[1]/div[1]/div[3]/table/tbody/tr", varHost)
        xx = Level_PO.get_attFromAtts("//input[@value4='" + varSelectID.split("_")[1] + "']", "id", varNum)
        # print xx

        # 遍历操作前的作业信息状态
        print ">>>>> " + varHost + u" 作业状态（操作前）"
        # Level_PO.printTRTD("//tr[@onclick=\"clickedRow('" + xx + "')\"]")
        x = Level_PO.printTRTDtoList("//tr[@onclick=\"clickedRow('" + xx + "')\"]")
        list1 = json.dumps(x, encoding="UTF-8", ensure_ascii=False)  # 字典 转 unicode
        # str1 = str(list1)
        # print str1
        # x= str(list1).split(u"设置状态：")[1]
        # print x
        varOperStatus = str(list1).split(u"设置状态：")[1].split("\\")[0]   # RUN
        varTriggerStatus = str(list1).split(u"触发器状态：")[1].split("\\")[0]  # NORMAL
        varTaskStatus = str(list1).split(u"作业状态：")[1].split(" ")[0]  # JOB_ENDING
        # print type(varOperStatus)

        # 选择作业
        Level_PO.clickXPATH("//input[@id='" + xx + "']", 2)

        if varOperStatus == "RUN":
            Level_PO.clickXPATH("//button[@onclick=\"setStatus('PAUSED');\"]", 2)  # 暂停
            Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
            print ">>>>> click暂停"
        if varOperStatus == "PAUSED":
            Level_PO.clickXPATH("//button[@onclick=\"setStatus('RESUME');\"]", 2)  # 恢复
            Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
            print ">>>>> click恢复"
        if varOperStatus == "RESUME":
            Level_PO.clickXPATH("//button[@onclick=\"setStatus('SHUTDOWN');\"]", 2)  # 停止
            Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
            print ">>>>> click停止"
        if varOperStatus == "SHUTDOWN":
            Level_PO.clickXPATH("//button[@onclick=\"setStatus('RUN');\"]", 2)  # 启动
            Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
            print ">>>>> click启动"
        print "-----------------------------"

        # Level_PO.clickXPATH("//button[@onclick=\"killJob();\"]", 2)  # 强制停止


        # 遍历操作后,获得作业信息状态
        print ">>>>> " + varHost + u" 作业状态（操作后）"
        Level_PO.printTRTD("//tr[@onclick=\"clickedRow('" + xx + "')\"]")




        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 首页

        # 点击引擎管理
        # Level_PO.clickLINKTEXT(u'引擎管理', 2)

        # 首页菜单(选择一级,二级)（作业管理、版本管理、宿主管理、日志管理、用户管理）
        # Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"用户管理", "//a[@href='#']", u"修改密码")

        # 退出
        # Level_PO.clickXPATH("//a[@href='/JobEngineW3/logout']",2)




        #
        #
        #
        # # # 编辑
        # # Level_PO.clickXPATH("//button[@onclick=\"update();\"]",2)
        # #
        # # # 发布
        # # Level_PO.clickXPATH("//button[@onclick=\"showVersionPublish()\"]",2)
        # #
        # # # 切换宿主
        # # Level_PO.clickXPATH("//button[@onclick=\"changeHost();\"]",2)
        # #
        # # 刷新
        # # Level_PO.clickXPATH("//button[@onclick=\"refresh()\"]",2)
        #
        #
        # # # 选择所属组
        # # Level_PO.select_byName('groupName', u'group1')
        # # # 任务名称
        # # Level_PO.inputID('_taskName', u'job')
        # # # 点击搜索
        # # Level_PO.clickXPATH("//button[@type='submit']", 3)

        # # print "12121212"
        # Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理")
        # sleep(3)
        # # # TaskManage_PO.test()
        # # 选择第二个
        # TaskManage_PO.clickONline(2)
        # # 上线
        # Level_PO.clickXPATH("//a[@class='layui-layer-btn0']", 2)
        # 取消
        # Level_PO.clickXPATH("//a[@class='layui-layer-btn1']", 2)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 作业管理
    def drv_task(self):
        # 作业管理 - 作业框架管理
        Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理")
        sleep(3)
        self.TestcaseModule()

    def taskReg(self,varHost,varGroup,varTask,varTrigger,varCron,varStartTime,varInterval,varRuntimes,varRunway,varParallelNums):
        # C2-2, 作业框架管理，注册任务1
        # 业务场景：创建一个作业任务（4种情况）
        # self.taskReg(u'宿主1',u'group1',u'task',u'简单触发器',u'',u'今天',u'1000',u'3', u'串行',u'')
        # self.taskReg(u'宿主1',u'group1',u'task1',u'简单触发器',u'今天',1000,3, u'并行',5)
        # self.taskReg(u'宿主1',u'group1',u'task1',u'cron表达式',3, u'串行')
        # self.taskReg(u'宿主1',u'group1',u'task1',u'cron表达式',3, u'并行',5)

        # [任务属性列表]
        # 点击注册
        Level_PO.clickXPATH("//button[@onclick=\"register();\"]", 1)
        Level_PO.inIframe("layui-layer-iframe1", 1)

        # [模式1, 简单触发器 + 串行]
        # 对应宿主机
        Level_PO.select_byName1('taskHostId', varHost)
        # 所属组名称
        Level_PO.select_byName1('taskGroup', varGroup)
        # 任务名称  + varRandom4
        self.comTaskName = varTask + Level_PO.varRandom4
        Level_PO.inputNAME('taskName', self.comTaskName)
        # 触发器类型
        Level_PO.select_byName1('cronFlag', varTrigger)

        if varTrigger == u"简单触发器":
            # 起始执行时间,切换框架   //今天
            # Level_PO.inputID("_timeStr", "2017-04-04 12:12:12")
            Level_PO.clickXPATH("//input[@id='_timeStr']", 1)
            Level_PO.outIframe(1)
            Level_PO.inIframeXPATH("//body[@class='gray-bg top-navigation']/div[4]/iframe", 1)
            Level_PO.clickXPATH("//input[@id='dpTodayInput']", 1)
            Level_PO.outIframe(1)
            Level_PO.inIframe("layui-layer-iframe1", 1)
            # 执行间隔
            Level_PO.inputID('_intervalTime', varInterval)
        else:
            Level_PO.inputID("_cronExpression", varCron)

        # 最多执行次数
        Level_PO.inputNAME('maxTimes', varRuntimes)

        if varRunway == u'串行':
            # 运行方式（串行）
            Level_PO.select_byName1('runMode', varRunway)
        else:
            # 运行方式（并行）
            Level_PO.select_byName1('runMode', varRunway)
            # 并行任务最大运行数量
            Level_PO.inputID('_parallelMaxNum', varParallelNums)

        # # 保存
        Level_PO.clickXPATH("//button[@onclick=\"submitForm()\"]", 1)
        Level_PO.outIframe(1)

        # # 退出
        # Level_PO.clickXPATH("//button[@onclick=\"cancelForm()\"]", 2)
        print u"OK, C2-2, 作业框架管理，注册任务1"

    def taskSearch(self,varGroup, varTask):

        Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理")
        sleep(3)

        # 作业管理中搜索功能
        if varGroup != "":
            # 请选择作业所属组
            Level_PO.select_byName('groupName', varGroup)
        if varTask != "":
            # 请输入任务名称
            Level_PO.inputID('_taskName', varTask)
        # 点击 搜索
        Level_PO.clickXPATH("//button[@type='submit']", 2)
        print u">>>>> 搜索后，当前任务属性列表"
        Level_PO.printTRTDtoList("//tr")
        print "\n"

    def taskReleaseVer(self,comTaskName,comVerName):
        # 作业管理 - 发布版本

        # 点击 版本发布
        Level_PO.clickXPATH("//button[@id='versionPublish']", 4)
        Level_PO.inIframe("layui-layer-iframe1", 1)
        print u">>>>> 版本记录，发布前列表清单"
        # Level_PO.printTRTD("//tr[1]")
        list1 = Level_PO.printTRTDtoList("//tr")
        print "\n"

        if u'是' in list1:
            # 点击 退出
            Level_PO.clickXPATH("//button[@onclick=\"cancelForm()\"]", 2)
            Level_PO.outIframe(2)
            # 点击版本撤回
            Level_PO.clickXPATH("//button[@id='retractVersion']", 2)
            Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认


        # # 选择某一个版本，点击 发布
        # xx = "\\\\" + comTaskName + "_" + comVerName + ".zip"
        # print xx
        # cur.execute('select id from task_version where package_path="%s" order by id desc limit 1' % (xx))
        # t4 = cur.fetchone()
        # print t4[0]
        # Level_PO.clickXPATH("//input[@value=\"" + t4[0] + "\"]", 2)

        # 点击 发布
        Level_PO.clickXPATH("//button[@onclick=\"publish()\"]", 2)
        Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认

        print u">>>>> 版本记录，发布后列表清单"
        Level_PO.printTRTD("//tr[1]")

        # 点击 退出
        Level_PO.clickXPATH("//button[@onclick=\"cancelForm()\"]", 2)
        Level_PO.outIframe(2)


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 版本管理
    def drv_ver(self):
        # 版本管理 - 版本管理 - 上传作业文件
        Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"版本管理", "//a[@href='#']", u"版本管理")
        self.TestcaseModule()

    def verSearch(self, varGroup, varTask):
        # C3-1, 作业任务搜索
        # print varTask
        # print "!!!!!!!!!!"
        sleep(4)
        if varGroup != "":
            # 请选择作业所属组
            Level_PO.select_byName('groupName', varGroup)
        if varTask != "":
            # 请输入任务名称
            Level_PO.inputID('_taskName', varTask)
        # 点击 搜索
        Level_PO.clickXPATH("//button[@type='submit']", 2)
        print u">>>>> 当前宿主及作业名称"
        Level_PO.printTRTDtoList("//tr")
        print u"OK,C3 - 1, 作业任务搜索"

    def verUploadTask(self,varStartFile, varType , varVer , varDesc , varInit , varuploadfile):
        # C3-2 ,版本管理之上传作业文件（注意同一个宿主下版本不能重复)

        # 点击 版本管理（默认选择第一条记录）
        Level_PO.clickXPATH("//button[@onclick=\"showTaskVersion()\"]", 4)

        # 判断有没有版本信息，如果有则判断版本信息不能重复，如果无则直接上传
        print u">>>>> 当前页所有版本"
        varRecord = Level_PO.printTRTDtoList("//tr")
        print "\n"

        if u"暂无操作记录列表" not in varRecord:
            varVerinfo = Level_PO.get_TRTD("//tr/td[2]")
        else:
            varVerinfo = ""

        # 点击 上传作业文件
        Level_PO.clickXPATH("//button[@onclick=\"addTaskVersion()\"]", 4)

        # 1启动文件
        Level_PO.inIframe("layui-layer-iframe1", 1)
        Level_PO.inputID("_jobName", varStartFile)
        # 2启动文件类型(1=bat , 2=shell)
        Level_PO.select_byName('jobType', varType)
        # 3作业版本
        if varVer not in varVerinfo:
            Level_PO.inputID("_version", varVer)
            self.comVerName = varVer
        else:
            Level_PO.inputID("_version", varVer + Level_PO.varRandom4)
            print u"[warning] 当前版本\'" + varVer + u"\'已存在！系统自动替换为\'" + varVer + Level_PO.varRandom4 + "\'"
            self.comVerName = varVer + Level_PO.varRandom4

        # 4版本描述
        Level_PO.inputID("_versionDesc", varDesc)
        # 5初始化参数配置
        if varInit != "":
            Level_PO.inputID("_initConfigValue", varInit)
        # 6上传文件
        Level_PO.script('document.getElementById("filePath").style.display="block"', 3)
        Level_PO.sendID("_taskFilePath", varuploadfile, 2)
        # 7保存
        Level_PO.clickXPATH("//button[@onclick=\"save()\"]", 3)
        Level_PO.outIframe(1)

        print u">>>>> 创建完成，版本信息"
        Level_PO.printTRTD("//tr[1]")
        # Level_PO.printTRTD("//tr[2]")
        print "\n"
        print u'OK,C3-2 , 版本管理之上传作业文件'

    def verEdit(self, varStartFile, varType, varDesc):
        # C3-3, 编辑未打包的版本（注：打包后不能再进行编辑）
        # 点击 编辑
        Level_PO.clickXPATH("//button[@onclick=\"updateTaskVersion();\"]", 2)
        Level_PO.inIframe("layui-layer-iframe1", 1)
        # 1启动文件
        Level_PO.inputID("_jobName", varStartFile)
        # 2启动文件类型(1=bat , 2=shell)
        Level_PO.select_byName('jobType', varType)
        # 3版本描述
        Level_PO.inputID("_versionDesc", varDesc)
        # 4保存
        Level_PO.clickXPATH("//button[@onclick=\"submitForm()\"]", 3)
        Level_PO.outIframe(1)

    def verPack(self, comTaskName,comVerName,varRtn):
        # C3-4, 对版本进行打包
        # 默认选择第一个版本进行打包
        sleep(3)

        # # 选择某一个版本id
        # xx = "\\" + comTaskName + "_" + comVerName + ".zip"
        # print xx
        # cur.execute('select id from task_version where package_path="%s" order by id desc limit 1' % (xx))
        # t4 = cur.fetchone()
        # # self.comVerID = t4[0]
        # print t4[0]
        # Level_PO.clickXPATH("//input[@value=\"" + t4[0] + "\"]", 2)
        # print "1111111"

        # 点击 版本打包
        Level_PO.clickXPATH("//button[@onclick=\"packVersion();\"]", 2)
        Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
        print u">>>>> 打包后，版本信息"
        Level_PO.printTRTD("//tr[1]")
        print "\n"
        if varRtn != "":
            Level_PO.clickXPATH("//button[@onclick=\"returnUrl();\"]", 2)  # 返回
            # 作业管理 - 作业框架管理
            Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理")
            sleep(3)
            print ">>>>> 返回，作业管理"
        print u'OK,C3-4, 对版本进行打包'

    def verUnPack(self):
        # C3-5, 对版本进行解包
        # 点击 解包 (默认第一条记录)
        Level_PO.clickXPATH("//button[@onclick=\"unPackVersion();\"]", 2)
        Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
        print u">>>>> 解包后，版本信息"
        Level_PO.printTRTD("//tr[1]")
        print "\n"
        print u'OK,C3-5, 对版本进行解包'






    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 宿主管理
    def drv_host(self):
        self.TestcaseModule()
        sleep(2)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 日志管理
    def drv_log(self):
        self.TestcaseModule()
        sleep(2)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # 用户管理
    def drv_user(self):
        self.TestcaseModule()
        sleep(2)


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(CaseHome)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

