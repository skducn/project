# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 医云谷 DM管理系统
"""
 @classmethod
 def setUpClass(self):  所有测试函数运行前执行一次

 @classmethod
 def tearDownClass(self):  所有测试函数运行完后执行一次

 def setup(self):  每个测试函数运行前执行

 def teardown(self):  每个测试函数运行后执行
 """
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


from YYG.Config.config import *
Level_PO = LevelPO(driver, varURL, varTitle)
net_PO = netPO()
sheet, newbk = Level_PO.iniExcel(varExcel, varExcelSheetName)
from PIL import ImageGrab


class Main(unittest.TestCase):

    def testMain(self):
        # 遍历main (测试函数)
        sleep(2)
        print u"\n\n----------------------------------------------------------------------"
        for i in range(1, sheet[0].nrows):
            if sheet[0].cell_value(i, 0) == "Y":
                self.Scene = sheet[0].cell_value(i, 1)
                self.SceneDesc = sheet[0].cell_value(i, 2)

                # 遍历TestCase及调用函数模块,定位测试用例位置及数量
                case1 = caseN = 0
                for j in range(1, sheet[1].nrows):
                    case1 = case1 + 1
                    if sheet[1].cell_value(j, 2) == self.Scene:
                        for k in range(case1 + 1, 100):  # 假设有100个Case
                            if k + 1 > sheet[1].nrows:  # 最后一行
                                caseN = caseN + 1
                                break
                            elif sheet[1].cell_value(k, 1) == "" and sheet[1].cell_value(k, 2) == "":
                                caseN = caseN + 1
                            elif sheet[1].cell_value(k, 1) == "skip":
                                caseN = caseN + 1
                            else:
                                caseN = caseN + 1
                                break
                        break
                # if self.Maincol2 == "skip":
                #     case1 = case1 + 1
                #     caseN = caseN - 1

                # 遍历 Testcase1~TestCaseN
                for l in range(case1, caseN + case1):
                    try:
                        if sheet[1].cell_value(l, 1) == "skip":
                            newWs = newbk.get_sheet(1)
                            newWs.write(l, 0, "skip", STYLEGRAY25)
                            newbk.save(varExcel)
                        elif sheet[1].cell_value(l, 5) == "":
                            pass
                        else:
                            self.exlTestCase = sheet[1].cell_value(l, 4)
                            varRtn = eval(sheet[1].cell_value(l, 5))
                            newWs = newbk.get_sheet(1)
                            try:
                                if "error" in varRtn:
                                    newWs.write(l, 0, varDayTime14, STYLERED)
                                    newWs.write(l, 6, varRtn, STYLERED)
                                else:
                                    newWs.write(l, 0, varDayTime14, STYLEBLUE)
                                    newWs.write(l, 6, varRtn, STYLEBLUE)
                                newbk.save(varExcel)
                            except:
                                print "error, 返回错误或无法接收返回值！"
                    except:
                        print "Errorrrrrr , Excel(" + str(l + 1) + ") , " + sheet[1].cell_value(case1, 2) + " , " + sheet[1].cell_value(
                            l, 3) + " , " + sheet[1].cell_value(l, 4) + " , " + sheet[1].cell_value(l, 5)
                        newWs = newbk.get_sheet(1)
                        newWs.write(l, 0, varDayTime14, STYLERED)
                        newbk.save(varExcel)

    ''' 业务场景1 '''

    def getCode(self):
        # 获取验证码
        # 截屏
        Level_PO.catcha('/Users/linghuchong/Desktop/1.jpg')
        box = (1830, 630, 1950, 671)
        im = Image.open('/Users/linghuchong/Desktop/1.jpg')
        im = im.crop(box)
        im.save('/Users/linghuchong/Desktop/1.jpg')
        # 对验证码置灰色
        imgry = im.convert('L')
        x = image_to_string(imgry)
        print u'验证码：' + x
        return x

    def login(self, varUser, varPass):
        ''' 登录 '''

        print self.exlTestCase + u" >>>>>>>>>>>>>>>>>>>>>>>>>>"
        try:
            Level_PO.open(3)
            Level_PO.inputID('_username', varUser)
            Level_PO.inputID('_password', varPass)

            # 验证码元素是否存在
            if Level_PO.isElementXpath("//img[@onclick=\"doChangeCaptcha(this)\"]"):

                # 获取此元素在页面中的位置及尺寸
                # checkcodeimg = Level_PO.getXPATH("//img[@onclick=\"doChangeCaptcha(this)\"]", 2)
                # # x1 = checkcodeimg.location['x']
                # # y1 = checkcodeimg.location['y']
                # # x2 = x1 + checkcodeimg.size['width']
                # # y2 = y1 + checkcodeimg.size['height']
                # # box = (int(x1), int(y1), int(x2), int(y2))

                for i in range(10):  # 如果验证码识别错误，则重复10次
                    Level_PO.inputID('_captcha', self.getCode())
                    Level_PO.clickXPATH("//button[@type='submit']", 2)

                    if Level_PO.isElementXpath("//a[@role='button']"):
                        # print u"登录成功"
                        break
                    else:
                        Level_PO.close_driver()
                        Level_PO.open(1)
                        Level_PO.inputID('_username', varUser)
                        Level_PO.inputID('_password', varPass)
            else:
                print u"error, 验证码元素定位错误！"

        except:
            return u"error, " + self.exlTestCase + u"!"
        print u"[Done], " + self.exlTestCase + u"\n"
        return u""

    def loginNoOpen(self, varUser, varPass):
        ''' 登录 '''

        print self.exlTestCase + u" >>>>>>>>>>>>>>>>>>>>>>>>>>"
        try:
            Level_PO.inputID('_username', varUser)
            Level_PO.inputID('_password', varPass)

            # 验证码元素是否存在
            if Level_PO.isElementXpath("//img[@onclick=\"doChangeCaptcha(this)\"]"):

                # 获取此元素在页面中的位置及尺寸
                # checkcodeimg = Level_PO.getXPATH("//img[@onclick=\"doChangeCaptcha(this)\"]", 2)
                # # x1 = checkcodeimg.location['x']
                # # y1 = checkcodeimg.location['y']
                # # x2 = x1 + checkcodeimg.size['width']
                # # y2 = y1 + checkcodeimg.size['height']
                # # box = (int(x1), int(y1), int(x2), int(y2))

                for i in range(10):  # 如果验证码识别错误，则重复10次
                    Level_PO.inputID('_captcha', self.getCode())
                    Level_PO.clickXPATH("//button[@type='submit']", 2)

                    if Level_PO.isElementXpath("//a[@role='button']"):
                        # print u"登录成功"
                        break
                    else:
                        Level_PO.close_driver()
                        Level_PO.openURL(varURLuser, 2)
                        Level_PO.inputID('_username', varUser)
                        Level_PO.inputID('_password', varPass)
            else:
                print u"error, 验证码元素定位错误！"

        except:
            return u"error, " + self.exlTestCase + u"!"
        print u"[Done], " + self.exlTestCase + u"\n"
        return u"OK"


    def createFactory(self, varName, varArea, varDistrict , varContact, varTel):
        ''' C1-1, 新增生产企业
        # 检查：表 tt_enterprise 中生成一条记录。 
        # 例子1：self.createFactory(u'2',u'',u'北京',u'王志刚',u'13816109050') 
        '''

        print self.exlTestCase + u" >>>>>>>>>>>>>>>>>>>>>>>>>>"

        Level_PO.openURL(u"http://10.111.3.5:88/yygdm/admin/web/app_test.php/enterprise/index", 3)
        # 新增生产企业 （企业名字只能用1次，）
        Level_PO.clickXPATH("//button[@data-target=\"#enterpriseCreateNew\"]", 5)
        # 企业名称
        # Level_PO.inputNAME("TtEnterpriseName", varName)
        Level_PO.clickXPATH("//input[@name='TtEnterpriseName']", 2)
        Level_PO.clickXPATH("//a[@data-index='12']", 2)  # 选择第12个企业

        # 所在地区
        Level_PO.selectXPATHtext(u"//div[@id='TtEnterpriseTtRegion-0']/select", varArea)
        sleep(2)
        Level_PO.selectXPATHtext(u"//div[@id='TtEnterpriseTtRegion-0']/select[2]", varDistrict)

        # 联系人
        Level_PO.inputID("TtEnterpriseLinkMan-0", varContact)
        # 联系电话
        Level_PO.inputID("TtEnterpriseLinkPhoneNumber-0", varTel)
        # save
        Level_PO.clickXPATH("//button[@onclick=\"doCreateEnterprise(this)\"]",2)


        print u"[Done], " + self.exlTestCase + u"\n"
        return u'表task_host中生成一条记录'



    ''' 业务场景5 '''

    def createStatist(self,varName,varPass,varSex,varPhone,varEmail,varCompany,varSelfID):
        ''' C5-1, 新增统计员
           # 检查：表 ？ 中生成一条记录。 
           # 例子1：self.createStatist(u'jinhao', u'123456', u'男', u'13816109050', u'jinhao@123.com', u'cetc', u'310101198004110017') 
        '''


        print self.exlTestCase + u" >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # Level_PO.script('window.open("' + varURLuser+'");', 8)
        Level_PO.openURL(varURLuser,2)
        Level_PO.clickXPATH("//a[@data-target=\"#userCreateNew\"]", 2)
        # 个人信息录入
        Level_PO.inputID('TtEnterpriseName',varName)
        Level_PO.inputID('TtUserPassword',varPass)
        Level_PO.inputID('TtUserPasswordConfirm',varPass)
        Level_PO.clickXPATH("//input[@value=1]",2)
        Level_PO.inputID('TtUserPhoneNumber',varPhone)
        Level_PO.inputID('TtUserMail',varEmail)
        Level_PO.inputID('TtUserCompany',varCompany)
        Level_PO.inputID('TtUserIdCard',varSelfID)
        Level_PO.clickXPATH("//button[@onclick=\"doCreateUser(this)\"]",2)

        if u"身份证格式错误" in Level_PO.getStr_DIV(1):
            Level_PO.clickXPATH("//div[@class=\"modal fade in\"]/div/div/div[3]/button", 2)
            print u"弹框提示：身份证格式错误"
            Level_PO.inputID('TtUserIdCard', varSelfID)
            Level_PO.clickXPATH("//button[@onclick=\"doCreateUser(this)\"]", 2)
        if u"该统计员已经被注册" in Level_PO.getStr_DIV(1):
            Level_PO.clickXPATH("//div[@class=\"modal fade in\"]/div/div/div[3]/button", 2)
            print u"弹框提示：该统计员已经被注册"
            varRandom11 = "".join(Level_PO.myfunc(11))
            Level_PO.inputID('TtUserPhoneNumber', varRandom11)
            Level_PO.clickXPATH("//button[@onclick=\"doCreateUser(this)\"]", 2)

        Level_PO.clickXPATH("//div[@class=\"modal fade in\"]/div/div/div[3]/button", 2)

        # 数据库中直接修改为"审核通过"，便于立即登录。
        try:
            cur.execute('update tt_user set `status`="1" where name="%s" and phone_number=%s' % (varName, varPhone))
            conn.commit()
            print u"数据库手工修改为 => 审核通过"
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        print u"[Done], " + self.exlTestCase + u"\n"
        return u'ok'





    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #  业务场景2

    def drv_Scene2(self):
        self.TestScene()
        sleep(2)
        print "\n"

    def countEngineStatus(self):
        # C2-2, 引擎管理连接宿主数与运行作业数统计

        print u"<C1-S2, 引擎管理连接宿主数与运行作业数统计 >>>>>>>>>>>>>>>>>>>>>>>>>>"
        tmpcount = 0
        list1 = Level_PO.getList_TRTD("//td")
        d1 = json.dumps(list1, encoding="UTF-8", ensure_ascii=False)  # unicode
        d2 = d1[d1.find(u'连接宿主个数'):]  # 连接宿主个数 5
        d3 = d2.split('", "')[0]
        varConnHostCount = d3.split(':')[1]    # 5
        if int(varConnHostCount) != d1.count(u'链接建立') : return u"error,引擎负责状况连接宿主个数！"
        print u" 1-2, 引擎负责状况连接宿主个数:" + str(varConnHostCount)

        d4 = d2.split('", "')[1]
        varRunJobCount = d4.split(':')[1]
        # print txtRUNJOBCOUNT + varRunJobCount # 运行作业个数 13
        d5 = d1[d1.find(u'调度作业数：'):]
        for a in range(d5.count(u'调度作业数')):
            d6 = d5.split(u'调度作业数：')[a+1]
            d7 = d6.split(u'个')[0]
            tmpcount = tmpcount + int(d7)
        if int(varRunJobCount) == tmpcount:
            print u" 2-2, 引擎负责状况运行作业个数:" + str(tmpcount)
            print u" S2, Done\n"
            return u"引擎负责状况，运行作业个数与总数一致。"
        else:
            print u"error，运行作业个数与总数不一致！运行作业个数：" + str(varRunJobCount) + u",运行作业统计个数：" + str(tmpcount)
            return u"error,引擎负责状况运行作业个数!"

    def countEngineSearch(self, varHost, varIP):
        # C2-3, 引擎管理运行作业数搜索统计
        # self.countEngineSearch(u'宿主15','10.111.3.15')

        print u"<C2-S3, 引擎管理运行作业数搜索统计 >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # 1-3、获取表task_host.id值
        tblRtnValue = Level_PO.get_TblOneValueWhere2(cur, conn, "task_host","host_name=" + varHost + ",host_server_ip=" + varIP, "id,id")
        Level_PO.clickXPATH("//button[@onclick=\"searchJob('" + str(tblRtnValue) +"')\"]", 2)

        tmpcount = 0
        list1 = Level_PO.getList_TRTD("//td")
        d1 = json.dumps(list1, encoding="UTF-8", ensure_ascii=False)  # unicode
        # print d1.split(u'连接宿主个数')[0]
        d2 = d1.split(u'连接宿主个数')[0]
        # print d2.count(varHost)  # 3
        # print type(d2.count(varHost))
        # print d1.split(u'连接宿主个数')[1]
        d3 = d1.split(u'连接宿主个数')[1]
        # print d3.split(varHost)[1]
        d4 = d3.split(varHost)[1]
        d5 = d4.split(u'个')[0]
        d6 = d5.split(u'调度作业数：')[1]
        # print d6
        # print type(d6)

        if d2.count(varHost) == int(d6):
            print u" 1-1, 搜索结果一致"
            print u" S3, Done\n"
            return u"引擎负责状况，搜索结果一致。"
        else:
            print u"error，搜索结果不一致！搜索" + varHost + u"右侧数：" + str(d2.count(varHost))  + u",左侧数：" + str(d6)
            return u"error,引擎负责状况搜索结果不一致!"


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #  业务场景3

    def drv_Scene3(self):
        self.TestScene()
        sleep(2)
        print "\n\n"

    def jobConsole(self,varHost, varIP, varTask,varGroup):
        # self.jobConsole(u'宿主15',u'10.111.3.15',u'host15_job2',u'group2')
        # C3-2, 引擎管理之作业控制台

        print u"<C3-S2, 引擎管理之作业控制台 >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # 搜索
        tblRtnValue1 = Level_PO.get_TblOneValueWhere2(cur, conn, "task_host","host_name=" + varHost + ",host_server_ip=" + varIP, "id,id")
        Level_PO.clickXPATH("//button[@onclick=\"searchJob('" + str(tblRtnValue1) + "')\"]", 2)
        print tblRtnValue1

        # 选择作业
        tblRtnValue2 = Level_PO.get_TblOneValueWhere2(cur, conn, "task_frame","task_name=" + varTask + ",task_group=" + varGroup, "id,id")
        Level_PO.clickXPATH("//input[@value='" + str(tblRtnValue2) + "']", 2)
        print tblRtnValue2

        # 点击作业控制台
        Level_PO.clickXPATH("//button[@id='_realtimeBtn']", 2)
        print u"< 1-2, 作业控制台 >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # 点击退出
        Level_PO.inIframeDiv("[@id='showRealtime']", 2)
        Level_PO.clickXPATH("//button[@onclick=\"cancelForm()\"]", 2)
        Level_PO.outIframe(2)

        # 点击查看
        Level_PO.clickXPATH("//span[@onclick=\"queryCallJobDetail('" + varTask + "','" + str(tblRtnValue2) + "','" + str(tblRtnValue1) + "');\"]", 2)
        print u"< 1-2, 查看调度详情 >>>>>>>>>>>>>>>>>>>>>>>>>>"
        return "OK"









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
    def verUnPack(self):
        # C3-5, 对版本进行解包
        # 点击 解包 (默认第一条记录)
        Level_PO.clickXPATH("//button[@onclick=\"unPackVersion();\"]", 2)
        Level_PO.clickXPATH("//div[@class='layui-layer-btn']/a", 2)  # 再次确认
        print u">>>>> 解包后，版本信息"
        Level_PO.printTRTD("//tr[1]")
        print "\n"
        print u'OK,C3-5, 对版本进行解包'


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Main)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

