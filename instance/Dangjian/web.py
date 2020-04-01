# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.5
# Date       : 2017-9-14
# Description: 电科党员学习教育平台, web平台创建项目、发布（包括审核）
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Dangjian.Config.config import *
from random import choice
# from android1_5 import AppDangjian
import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands
from selenium.webdriver.common.by import By



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ini

# varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间，格式：20170914143616982，类型是 str，
# varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 当天日期，格式：2016-06-28 ， 类型是 str


l_varCover = ['100.jpg', '101.jpg', '102.jpg', '103.jpg', '104.jpg'] # 附件，选择文件，（子项目封面）
varProject = u"党员学习任务" + varTime  # 项目标题
varProjectDesc = u"党员学习任务描述" + varTime # 项目描述
varStartDate = u"2017-01-01"  # 开始时间
varEndDate = varYMD  # 结束时间
# 项目描述 , 子项目描述
varDesc = u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十" \
          u"一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十"

# 四学方式
# l_fourLearn = ["问卷答题引导学", "问卷答题", "考试"]
# l_fourLearn = ["问卷答题引导学", "问卷答题", "投票"]
# l_fourLearn = ["化小专题交流学", "群组交流"]
# l_fourLearn = ["化小专题交流学", "资料自学"]
# l_fourLearn = ["考量工作结合学", "心得笔记"]
l_fourLearn = ["对照言行自省学", "三会一课", "支委会"]
# l_fourLearn = ["对照言行自省学", "三会一课", "支部大会"]
# l_fourLearn = ["对照言行自省学", "三会一课", "党小组会"]
# l_fourLearn = ["对照言行自省学", "三会一课", "党课"]
# l_fourLearn = ["对照言行自省学", "民主生活会"]
# l_fourLearn = ["对照言行自省学", "组织生活会"]
# l_fourLearn = ["其他", "直播空间"]

print l_fourLearn[0]
print l_fourLearn[1]
print varProject
sleep(2)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 测试环境
# varURL = u"http://10.111.3.5:88"
# Level_PO = LevelPO(driver, u"http://10.111.3.5:88/dangjian1.5/web/app_test.php/DJsecurity/security/login", u"中国电科党员日常学习教育平台")
# varUser = u"yoyo"
# varPwd = u"123456"
# varTargetObject = u"测试二级单位" # 接收目标
# varObject = u"测试张"  # 学习对象

# 生产环境
varURL = u"http://meeting.iotcetc.com"
Level_PO = LevelPO(driver)

# Level_PO = LevelPO(driver, varURL + u"/dangjian1.5/web/app_test.php/DJsecurity/security/login", u"中国电科党员日常学习教育平台")
# varUser = u"jinhao"
# varPwd = u"111111"
varAudit = u"off"
# varArchitecture = u'软信测试第一支部'  # 选择架构
# varTargetObject = u"测试第一党小组" # 学习对象
varTargetObject1 = u"测试第一党小组" # 学习对象

varObject = u"金浩"   # 学习人员
varObject1 = u"吴小浩" # 学习人员


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class WebTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass
    def test_Main(self):
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
            try :
                if sheetTestCase.cell_value(l, 1) == "skip":
                    newWs = newbk.get_sheet(1)
                    newWs.write(l, 0, "skip", styleGray25)
                    newbk.save(varExcel)
                elif sheetTestCase.cell_value(l, 5) == "":
                    print "error,Function值为空"
                else:
                    # self.l = l
                    exec (sheetTestCase.cell_value(l, 5))
                    newWs = newbk.get_sheet(1)
                    newWs.write(l, 0, varTimeYMDHSM, styleBlue)
                    newbk.save(varExcel)
            except:
                print "Errorrrrrrr , Excel(" + str(l + 1) + ") , " + sheetTestCase.cell_value(case1,2) + " , " + sheetTestCase.cell_value(l, 3) + " , " + sheetTestCase.cell_value(l, 4) + " , " + sheetTestCase.cell_value(l, 5)
                newWs = newbk.get_sheet(1)
                newWs.write(l, 0, varTimeYMDHSM, styleRed)
                newbk.save(varExcel)


    # 客户端登录
    # AppDangjian().login()

    # web登录


    def drv_login(self, varPrefix):
        self.varPrefix = varPrefix
        self.TestcaseModule()
    def webLogin(self, varEnv, varUser, varPwd):
        # self.webLogin(u"prod", u"jinhao", u"111111")
        ''' 登录 '''
        if varEnv == u"prod":varURL = u"http://meeting.iotcetc.com"
        else:varURL = u"http://10.111.3.5:88"
        # Level_PO = LevelPO(driver, varURL + u"/dangjian1.5/web/app_test.php/DJsecurity/security/login", u"中国电科党员日常学习教育平台")

        Level_PO.openURL(varURL + u"/dangjian1.5/web/app_test.php/DJsecurity/security/login", 3)
        Level_PO.inputID(u"_username", varUser)
        Level_PO.inputID(u"_password", varPwd)

        # 获取验证码
        Level_PO.inputID(u"_captcha", Level_PO.getCode(u"test.jpg", 2060, 850, 2187, 900))
        Level_PO.clickTAGNAME(u'button', 2)

        for i in range(10):
            if Level_PO.isElementId(u"_captcha"):
                sleep(2)
                Level_PO.inputID(u"_username", varUser)
                Level_PO.inputID(u"_password", varPwd)
                Level_PO.inputID(u"_captcha", Level_PO.getCode(u"test1.jpg", 2060, 792, 2187, 849))
                Level_PO.clickTAGNAME(u'button', 2)
                break

        print "\n" + self.varPrefix + u"" + varUser + u"登录成功"
        self.varEnv = varEnv
        sleep(1122)


    def drv_home(self, varPrefix):
        self.varPrefix = varPrefix
        self.TestcaseModule()
    def myRole(self, varArchitecture):
        # self.myRole(u"软信测试第一支部")
        # self.myRole(u"测试第一党小组")
        ''' 架构切换 ，切换到 软信测试第一支部 '''

        # if self.varEnv == u"prod":
        #     Level_PO.clickXPATH(u"//a[@class='dropdown-toggle']", 2)
        #     dict2 = Level_PO.getList_LinktextHref(u"//ul[@class='dropdown-menu']/li/a")
        #     for key in dict2:
        #         print str(dict2[key])
        #         print str(dict2[key]).split(u'meeting.iotcetc.com')[1]

        if not varArchitecture in Level_PO.get_valueFromAtt(u"//a[@class='dropdown-toggle']"):
            Level_PO.clickXPATH(u"//a[@class='dropdown-toggle']", 2)
            dict2 = Level_PO.getList_LinktextHref(u"//ul[@class='dropdown-menu']/li/a")
            for key in dict2:
                # print str(dict2[key])
                # print str(dict2[key]).split(u'meeting.iotcetc.com')[1]
                if varArchitecture in key:
                    Level_PO.clickXPATH(u"//a[@href='" + str(dict2[key]).split(u'meeting.iotcetc.com')[1] + u"']", 2)
                    break
        print self.varPrefix + u"切换角色至 '" + varArchitecture + u"'"


    def drv_project(self, varPrefix):
        self.varPrefix = varPrefix
        self.TestcaseModule()

    def flowSetup(self, varExecute, *varObjects):
        '''流程设置'''
        # del, all   self.audit(u"del", u"all")
        # del, 支部书记    self.audit(u"del", u"支部书记")
        # del, 审核项目,支部书记  self.audit(u"del", u"支部书记,审核项目")

        # add, 审核项目  self.audit(u"add", u"审核项目")
        # add, 审核项目,支部书记,支部学习委员    self.audit(u"add", u"支部书记,审核项目,支部学习委员")

        Level_PO.clickLINKTEXT(u'项目管理', 2)

        '''流程设置'''
        Level_PO.clickLINKTEXT(u'流程设置', 2)

        if varExecute == u"del" and varObjects[0] == u"all":
            #  获取所有的岗位的ID，如 onclick="doAddRole('6', '审核项目')" ， ID=6
            x = Level_PO.get_attFromAtts(u"//a[@class='btn btn-block btn-info']", u"onclick", u"all")
            for i in range(x[-1]):
                # print x[i]
                y = str(x[i]).replace(u"doAddRole('", u"").split(u"'")[0]
                if Level_PO.isElementId(u"approval-item-" + y):
                    Level_PO.clickXPATH(u"//div[@id='approval-item-" + y + u"']/i[1]", 2)
            Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 2)
            print u"项目管理 - 流程设置 - 已取消所有审批人"
            self.varIsAudit = u"N"

        elif varExecute == u"del":
            dict1 = {}
            x = Level_PO.get_attFromAtts(u"//a[@class='btn btn-block btn-info']", u"onclick", u"all")
            for i in range(x[-1]):
                # print x[i]
                dictKey = str(x[i]).replace(u"doAddRole('", u"").split(u"'")[0]
                dictValue = str(x[i]).replace(u"doAddRole('", u"").split(u"', ")[1].replace(u"'", u"").replace(u')', u"")
                dict1[dictKey] = dictValue
            varComma = str(varObjects[0]).count(",")
            # print dict1
            # print varComma

            if int(varComma) > 0:
                for j in range(int(varComma)+1):
                    varAudit = str(varObjects[0]).split(",")[j]
                    # print varAudit
                    for dictKey in dict1:
                        if varAudit == str(dict1[dictKey]):
                            varKey = list(dict1.keys())[list(dict1.values()).index(dict1[dictKey])]  # 从字典value得到对应的key
                            if Level_PO.isElementId(u"approval-item-" + varKey):
                                Level_PO.clickXPATH(u"//div[@id='approval-item-" + varKey + u"']/i[1]", 2)
                                print u"项目管理 - 流程设置 - 已取消 '" + str(dict1[dictKey]) + u"' 审批人"
            else:
                if varObjects[0] == str(dict1[dictKey]):
                    varKey = list(dict1.keys())[list(dict1.values()).index(dict1[dictKey])]  # 从字典value得到对应的key
                    if Level_PO.isElementId(u"approval-item-" + varKey):
                        Level_PO.clickXPATH(u"//div[@id='approval-item-" + varKey + u"']/i[1]", 2)
                        print u"项目管理 - 流程设置 - 已取消 '" + str(dict1[dictKey]) + u"' 审批人"

            Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 2)
            self.varIsAudit = u"N"

            # sleep(1212)
            # Level_PO.clickLINKTEXT(u"off", 2)
            # Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 6)
            # self.varIsAudit = u"Y"

        Level_PO.clickLINKTEXT(u'项目管理', 2)

            # if varStatus == u"on":
        #     Level_PO.clickLINKTEXT(u"off", 2)
        #     Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 6)
        #     self.varIsAudit = u"Y"
        # else:
        #     # 取消
        #     Level_PO.clickXPATH(u"//div[@id='approval-item-18']/i[1]", 2)
        #     Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 2)
        #     self.varIsAudit = u"N"

    def newProject(self, varEnv, varFlow, varProject, varProjectDesc, varStartDate, varEndDate, varTargetObject, l_fourLearn, l_varCover, varLearnObject, varObject):

        # self.newProject(u"prod", u"off", u"党员学习任务" + varTime, u"党员学习任务描述" + varTime, u"2017-01-01", varYMD, u"测试第一党小组",
        #                 ["对照言行自省学", "三会一课", "支委会"], ['100.jpg', '101.jpg', '102.jpg', '103.jpg', '104.jpg'], u"测试第一党小组",
        #                 u"金浩")

        if varEnv == u"prod":
            varURL = u"http://meeting.iotcetc.com"
        else:
            varURL = u"http://10.111.3.5:88"
        Level_PO = LevelPO(driver, varURL + u"/dangjian1.5/web/app_test.php/DJsecurity/security/login", u"中国电科党员日常学习教育平台")

        ''' 新建项目 '''

        Level_PO.clickLINKTEXT(u'项目管理',2)
        Level_PO.clickLINKTEXT(u'新建项目',4)
        Level_PO.inputID(u"subjectbundle_tttask_title", varProject)
        Level_PO.inputID(u"subjectbundle_tttask_resume", varProjectDesc)
        Level_PO.jsRemoveReadonly(u"subjectbundle_tttask_beginDate")
        Level_PO.inputID(u"subjectbundle_tttask_beginDate", varStartDate)
        Level_PO.inputID(u"subjectbundle_tttask_beginDate", Keys.TAB)
        Level_PO.jsRemoveReadonly(u"subjectbundle_tttask_endDate")
        Level_PO.inputID(u"subjectbundle_tttask_endDate", varEndDate)
        Level_PO.inputID(u"subjectbundle_tttask_endDate", Keys.TAB)
        # 附件 选择文件
        Level_PO.clickXPATH(u"//button[@class='btn btn-info']", 2)
        Level_PO.clickXPATH(u"//input[@name='learn_source_id[]']", 2)
        Level_PO.clickXPATH(u"//button[@onclick='doAddAttachment()']", 2)


        # 接收目标 ， 如果是最底层架构，则无接收目标
        if Level_PO.isElementXpath(u"//a[@data-target='#popup-target-company']"):
            Level_PO.clickLINKTEXT(u'添加接收目标', 2)
            # Level_PO.inputNAME(u'filter_company', varTargetObject)
            # Level_PO.clickLINKTEXT(u'查询',4)

            if u"10.111.3.5" in varURL:
                cur.execute('select company_id from tt_company where name="%s" order by company_id limit 1' % (varTargetObject))
                t1 = cur.fetchone()
                Level_PO.clickXPATH(u"//input[@value='" + str(t1[0]) + u"']", 2)
            else:
                varContent = Level_PO.getList_TRTD(u"//div[@class='text-left company-name']")
                varValueNum = Level_PO.get_attFromAtts(u"//input[@class='checkbox-company']", u"value", u"all")
                d_SerialRow = dict(zip(varContent, varValueNum))

                for key in d_SerialRow:
                    print key
                    if key == varTargetObject:
                        Level_PO.clickXPATH(u"//input[@value='" + str(d_SerialRow[key]) + u"']", 2)
                # Level_PO.clickXPATH(u"//input[@value='154']", 2)  # 选 测试第一党小组
            sleep(1212)
            Level_PO.clickXPATH(u"//button[@class='btn btn-success']", 2)   # 提交


        ''' 子项目列表 '''
        Level_PO.clickLINKTEXT(u'添加子项目',6)
        Level_PO.inIframeTopDiv(u"[@class='modal-body no-padding']", 2)
        Level_PO.inputID(u"subjectbundle_ttsubject_title", u" - 子项目")
        # Level_PO.inputID(u"subjectbundle_ttsubject_resume", varSubDesc)

        # 四学方式
        if l_fourLearn[0] == u"问卷答题引导学":
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnType", l_fourLearn[0])
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnSeting", l_fourLearn[1])
            Level_PO.selectID(u"subjectbundle_ttsubject_type", l_fourLearn[2])
            Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/" + choice(l_varCover))
            Level_PO.jsRemoveReadonly(u"subjectbundle_ttsubject_planBeginDateYmd")
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", Keys.TAB)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", Keys.TAB)

            # '''添加学习内容'''
            if l_fourLearn[2] == u"考试":
                Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-topSurvey-add']", 2)
                Level_PO.inIframeXPATH(u"//iframe[@src='" + varURL + u"/dangjian1.5/web/app_test.php/survey/popup/index']", 4)
                # 默认选择第一个
                Level_PO.clickXPATH(u"//input[@name='selected']", 2)
                Level_PO.inIframeTopDivParent(2)
                Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailTopSurvey(event);']", 2)
            if l_fourLearn[2] == u"投票":
                Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-topVote-add']", 2)
                Level_PO.inIframeXPATH(u"//iframe[@src='" + varURL + u"/dangjian1.5/web/app_test.php/vote/popup/index']", 4)
                Level_PO.clickXPATH(u"//input[@name='selected']", 2)
                Level_PO.inIframeTopDivParent(2)
                Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailTopVote(event);']", 2)
        if l_fourLearn[0] == u"化小专题交流学":
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnType", l_fourLearn[0])
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnSeting", l_fourLearn[1])
            if l_fourLearn[1] == u"主题讨论":
                pass
            elif l_fourLearn[1] == u"资料自学":
                # '''添加学习内容'''
                Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-source-add']", 2)
                # 默认，选择资料
                Level_PO.clickXPATH(u"//input[@name='learn_source_id[]']", 2)

                # or 选择附件
                # Level_PO.inIframeTopDiv(u"[@class='modal-body no-padding']", 4)
                # Level_PO.clickID(u"profile-tab", 4)
                # # Level_PO.clickXPATH(u"//input[@value='1270']", 2)
                # # Level_PO.clickXPATH(u"//input[@value='1268']", 2)
                # Level_PO.clickXPATH(u"//input[@value='1265']", 2)
                # Level_PO.get_selectRadio1("//input[@name='learn_source_id[]']", u"1277")
                # Level_PO.inIframeTopDivParent(2)

                Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailSource(event);']", 6)
            Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/" + choice(l_varCover))
            Level_PO.jsRemoveReadonly(u"subjectbundle_ttsubject_planBeginDateYmd")
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", Keys.TAB)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", Keys.TAB)

        if l_fourLearn[0] == u"考量工作结合学":
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnType", l_fourLearn[0])
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnSeting", l_fourLearn[1])
            Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/" + choice(l_varCover))
            Level_PO.jsRemoveReadonly(u"subjectbundle_ttsubject_planBeginDateYmd")
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", Keys.TAB)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", Keys.TAB)

        if l_fourLearn[0] == u"对照言行自省学":
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnType", l_fourLearn[0])
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnSeting", l_fourLearn[1])
            if l_fourLearn[1] == u"三会一课":
                Level_PO.selectID(u"subjectbundle_ttsubject_type", l_fourLearn[2])
            Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/" + choice(l_varCover))
            Level_PO.jsRemoveReadonly(u"subjectbundle_ttsubject_planBeginDateYmd")
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", Keys.TAB)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planEndDateYmd", Keys.TAB)

        if l_fourLearn[0] == u"其他":
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnType", l_fourLearn[0])
            Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnSeting", l_fourLearn[1])
            Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/" + choice(l_varCover))
            Level_PO.jsRemoveReadonly(u"subjectbundle_ttsubject_planBeginDateYmd")
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", varEndDate)
            Level_PO.inputID(u"subjectbundle_ttsubject_planBeginDateYmd", Keys.TAB)
            Level_PO.selectID(u"subjectbundle_ttsubject_planBeginDateH", u"04")
            Level_PO.selectID(u"subjectbundle_ttsubject_planBeginDateI", u"08")
            Level_PO.selectID(u"subjectbundle_ttsubject_planEndDateH", u"20")
            Level_PO.selectID(u"subjectbundle_ttsubject_planEndDateI", u"58")
            '''添加学习内容'''
            Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-lesson-add']", 2)

            # 直播计划
            Level_PO.inIframeXPATH(u"//iframe[@src='" + varURL + u"/dangjian1.5/web/app_test.php/lesson/lesson/blank?lesson_id=0']", 4)
            Level_PO.inputID(u"lesson_name", u"大家的直播课堂")
            Level_PO.inputID(u"lesson_pin", u"123456")
            Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/" + choice(l_varCover))
            # 参与人员复选框
            Level_PO.clickXPATH(u"//input[@onclick='doCheckAll(this)']", 2)
            Level_PO.inputID(u"lesson_manager_name", u"管理员吴总")
            Level_PO.inputID(u"lesson_manager_phone_number", u"13611958388")
            Level_PO.inputID(u"lesson_person_lecturer_name", u"金浩")
            Level_PO.inputID(u"lesson_person_lecturer_phone_number", u"13816109050")
            # Level_PO.inputXPATH(u"//input[@name='lesson_person_info_json[1][name]']", u"周立人")
            # Level_PO.inputXPATH(u"//input[@name='lesson_person_info_json[1][phone_number]']", u"12100000000")
            # Level_PO.inputXPATH(u"//input[@name='lesson_person_info_json[2][name]']", u"吴梦")
            # Level_PO.inputXPATH(u"//input[@name='lesson_person_info_json[2][phone_number]']", u"12100000001")
            Level_PO.inIframeTopDivParent(2)
            Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailLesson(event);']", 6)


        # 添加学习对象

        Level_PO.screenTop(u'10000', 2)
        Level_PO.clickLINKTEXT(u'添加学习对象',4)

        # if varObject == u"测试人员1" :
        #     Level_PO.clickXPATH(u"//tr[@data-company-parent-id='3' and @data-level='1']/td[1]/div[2]/a[1]/i", 2)
        #     Level_PO.clickXPATH(u"//tr[@data-company-parent-id='3' and @data-level='1'][2]/td[1]/div[2]/a[1]/i", 2)
        #     Level_PO.clickXPATH(u"//tr[@data-company-parent-id='3' and @data-level='1'][3]/td[1]/div[2]", 2)

        Level_PO.clickXPATH(u"//tr[@data-company-parent-id='127' and @data-level='1']/td[1]/div[2]/a[1]/i", 2)

        # 查询
        Level_PO.inputXPATH(u"//form[@id='search-user-login-form']/div[1]/div[1]/input", varObject)
        Level_PO.clickXPATH(u"//a[@onclick='doSearchUserLogin(this)']", 2)

        Level_PO.clickXPATH(u"//input[@data-name='" + varObject + u"']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-success']", 5)

        # Level_PO.inputXPATH(u"//form[@id='search-user-login-form']/div[1]/div[1]/input", varObject)
        # Level_PO.clickXPATH(u"//a[@onclick='doSearchUserLogin(this)']", 2)
        # cur.execute('select user_id from tt_user_login where name="%s" order by user_id desc limit 1' % (varObject))
        # t3 = cur.fetchone()
        # conn.commit()
        # print t3[0]
        # Level_PO.clickXPATH(u"//input[@value='" + str(t3[0]) + u"']", 2)

        # '''2.0三级单位 from 蒋艳'''
        # Level_PO.clickXPATH(u"//tr[@data-company-parent-id='198' and @data-level='1']/td[1]/div[2]/a[1]/i", 2)
        # Level_PO.inputXPATH(u"//form[@id='search-user-login-form']/div[1]/div[1]/input", varObject1)
        # Level_PO.clickXPATH(u"//a[@onclick='doSearchUserLogin(this)']", 2)
        # cur.execute('select user_id from tt_user_login where name="%s" order by user_id desc limit 1' % (varObject1))
        # t2 = cur.fetchone()
        # Level_PO.clickXPATH(u"//input[@value='" + str(t2[0]) + u"']", 2)
        # ''''''''

        Level_PO.screenTop(u'10000', 2)
        # 设为群主
        Level_PO.clickXPATH(u"//a[@data-target='#popup-target-group-owner-0']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-success btn-confirm-group-owner']", 2)
        Level_PO.screenTarget(u"//button[@class='btn btn-primary']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)
        Level_PO.outIframe(4)
        # 提交
        Level_PO.screenTop(u'10000', 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 4)

        print "\n" + self.varPrefix + u"新建项目成功"
        self.varIsAudit = u"N"

        '''审核流程'''
        if self.varIsAudit != u"Y":
            # 发布
            Level_PO.clickXPATH(u"//div[@id='popup-publish-form']/div[1]/div[1]/div[2]/form/button", 2)

            if l_fourLearn[0] == u"其他":
                '''发件箱 - 直播空间'''
                Level_PO.clickLINKTEXT(u'发件箱', 2)
                Level_PO.clickLINKTEXT(varProject, 2)
                Level_PO.clickLINKTEXT(u'编辑', 4)
                Level_PO.inIframeTopDiv(u"[@class='modal-body no-padding']", 2)
                Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-lesson-view']", 2)
                Level_PO.inIframeXPATH(u"//iframe[@data-url='/dangjian1.5/web/app_test.php/lesson/lesson/blank']", 2)
                # 直播间号码
                x = Level_PO.get_attFromAtt(u"//input[@id='lesson_meeting_id']", u"value")
                print u"直播间号码: " + str(x)
                print u"直播间地址: https://meeting.iotcetc.com/html5/live-server/index.html"
                Level_PO.clickLINKTEXT(u'u6.gg/rt', 2)
                Level_PO.inputXPATH(u"//input[@ng-model='meetingNumber']", x)
                Level_PO.inputXPATH(u"//input[@ng-model='phoneNumber']", u"13611958388")
                Level_PO.clickXPATH(u"//button[@ng-click='login(meetingNumber,phoneNumber);']", 2)
                Level_PO.inputXPATH(u"//input[@ng-model='pin']", u"123456")
                Level_PO.clickXPATH(u"//button[@ng-click='joinMeetingWithPin(pin)']", 2)
        else:
            # 需要审核 , 切换帐号
            Level_PO.clickLINKTEXT(u"退出登录", 2)
            Level_PO.inputID(u"_username", u"wuxiaohao")
            Level_PO.inputID(u"_password", u"123456")
            Level_PO.clickTAGNAME(u'button', 2)
            print "\n" + u"wuxiaohao 登录成功"

            ''' 架构切换 ，切换到 软信测试第一支部'''
            if not u"10.111.3.5" in varURL:
                if not varArchitecture in Level_PO.get_valueFromAtt(u"//a[@class='dropdown-toggle']"):
                    Level_PO.clickXPATH(u"//a[@class='dropdown-toggle']", 2)
                    Level_PO.clickXPATH(
                        u"//a[@href='/dangjian1.5/web/app_test.php/switch_manageuser?companyId=127&roleId=23']", 4)

            # 待审核
            Level_PO.clickLINKTEXT(u"项目管理", 2)
            Level_PO.clickLINKTEXT(u"待审核", 2)
            Level_PO.clickLINKTEXT(varProject, 4)
            Level_PO.screenTop(u'10000', 2)
            Level_PO.clickLINKTEXT(u"通过", 2)
            Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 6)

            ''' 切回帐号'''
            Level_PO.clickLINKTEXT(u"退出登录", 2)
            Level_PO.inputID(u"_username", varUser)
            Level_PO.inputID(u"_password", varPwd)
            Level_PO.clickTAGNAME(u'button', 2)
            print "\n" + u"jinhao 登录成功"

            ''' 架构切换 ，切换到 软信测试第一支部'''
            if not u"10.111.3.5" in varURL:
                if not varArchitecture in Level_PO.get_valueFromAtt(u"//a[@class='dropdown-toggle']"):
                    Level_PO.clickXPATH(u"//a[@class='dropdown-toggle']", 2)
                    Level_PO.clickXPATH(
                        u"//a[@href='/dangjian1.5/web/app_test.php/switch_manageuser?companyId=127&roleId=23']", 4)

            Level_PO.clickLINKTEXT(u"项目管理",2)

            Level_PO.clickLINKTEXT(u"发件箱",2)
            Level_PO.clickLINKTEXT(varProject, 4)
            Level_PO.screenTop(u'10000', 2)
            x = Level_PO.get_attFromAtt(u"//a[@class='btn btn-primary btn-publish']", u"href")
            # print x
            x = str(x).replace(u"http://meeting.iotcetc.com", u"")
            # print x
            Level_PO.clickXPATH(u"//a[@class='btn btn-primary btn-publish']", 2)  # 发布项目
            Level_PO.clickXPATH(u"//form[@action='" + x + u"']/button[1]", 2)

            # 发件箱中

                    # Level_PO.clickLINKTEXT(u'流程设置', 2)
    # Level_PO.clickLINKTEXT(u'驾驶舱管理员', 2)
    # Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 2)
    #


            # Level_PO.clickLINKTEXT(u'发件箱', 6)
    # varString1 = Level_PO.rtnTRTD(u"//tr")
    # if u"审核中" in str(varString1.split(varProject)[0]):
    #     Level_PO.clickLINKTEXT(u'退出登录', 2)
    #
    #     Level_PO.inputID(u"_username", u"johnjinhao")
    #     Level_PO.inputID(u"_password", u"123456")
    #     Level_PO.clickTAGNAME(u'button', 2)
    #     print u"C1，电科党员学习教育平台 - johnjinhao 登录成功"
    #
    #     Level_PO.clickLINKTEXT(u'项目管理', 2)
    #     Level_PO.clickLINKTEXT(u'待审核', 2)
    #     Level_PO.clickLINKTEXT(varProject, 2)
    #     Level_PO.clickLINKTEXT(u'通过', 6)
    #     Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)
    #     Level_PO.clickLINKTEXT(u'退出登录', 2)
    #     print u"C1，审核通过，johnjinhao退出系统"
    #
    #     Level_PO.inputID(u"_username", u"yoyo")
    #     Level_PO.inputID(u"_password", u"123456")
    #     Level_PO.clickTAGNAME(u'button', 2)
    #     print u"C1，电科党员学习教育平台 - yoyo登录成功"
    #     Level_PO.clickLINKTEXT(u'项目管理', 2)
    #     Level_PO.clickLINKTEXT(u'发件箱', 2)
    #     # varString2 = Level_PO.rtnTRTD(u"//tr")
    #     # print varString2
    #
    #
    # '''已发布'''
    # x = str(Level_PO.printA(varProject))
    # x = x.replace(u"http://10.111.3.5:88", u"")
    # x = x.replace(u"/edit", u"/publish")
    # Level_PO.clickXPATH("//a[@href='" + str(x) + "']", 2)
    # Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)


    # @classmethod
    # def tearDownClass(self):
    #     driver.quit()



    def drv_accessory(self,varPrefix):
        self.varPrefix = varPrefix
        self.TestcaseModule()
    def uploadfile(self):
        Level_PO.clickLINKTEXT(u'附件管理', 2)
        Level_PO.clickXPATH(u"//a[@href='/dangjian1.5/web/app_test.php/attach/index']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-primary btn-sm']", 2)
        Level_PO.inputID(u"title", u"test1")
        Level_PO.inputID(u"fileUpload", u"//Users/linghuchong/Downloads/51/Picture/1.txt")

        # 所属分类
        Level_PO.selectID(u"class", u"测试")
        # Level_PO.inputID(u"className", u"我的分类")
        Level_PO.clickXPATH(u"//input[@name='isShare2']", 2)
        Level_PO.clickID(u'doUploadFileId', 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-default cetc-popup-confirm-btn']", 2)

        print "\n" + self.varPrefix + u"1.txt 上传成功"

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(WebTest)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

