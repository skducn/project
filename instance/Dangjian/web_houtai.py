# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.5
# Date       : 2017-9-14
# Description: 电科党员学习教育平台
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Dangjian.Config.config import *
# from Dangjian.PageObject.LoginPO import *
Level_PO = LevelPO(driver, "", "")


class Web(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass


    '''登录后台'''
    Level_PO.open(3)
    Level_PO.inputID(u"_username", u"yoyo")
    Level_PO.inputID(u"_password", u"123456")
    Level_PO.clickTAGNAME(u'button', 2)
    print u"C1，电科党员学习教育平台 - yoyo登录成功"

    Level_PO.clickLINKTEXT(u'项目管理', 2)


    '''创建母项目'''
    print u"C2，创建母项目 - 开始"
    varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 类型是 str，20170914143616982
    varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 2016-06-28
    varProject = u"党员学习任务" + varTime

    Level_PO.clickLINKTEXT(u'新建项目',2)
    Level_PO.inputID(u"subjectbundle_tttask_title", varProject)
    Level_PO.inputID(u"subjectbundle_tttask_resume", u"党员学习计划描述" + varTime)
    Level_PO.jsDate(u"subjectbundle_tttask_beginDate")
    Level_PO.inputID(u"subjectbundle_tttask_beginDate", varYMD)
    Level_PO.jsDate(u"subjectbundle_tttask_endDate")
    Level_PO.inputID(u"subjectbundle_tttask_endDate", varYMD)
    Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/4729.jpg")
    Level_PO.clickLINKTEXT(u'添加接收目标', 2)
    Level_PO.inputNAME(u'filter_company', u"测试二级单位")
    Level_PO.clickLINKTEXT(u'查询',2)
    Level_PO.clickXPATH(u"//input[@value='188']", 2)
    Level_PO.clickXPATH(u"//input[@value='194']", 2)
    Level_PO.clickXPATH(u"//button[@class='btn btn-success']", 2)

    '''添加子项目'''
    Level_PO.clickLINKTEXT(u'添加子项目',2)
    Level_PO.inIframeTopDiv(u"[@class='modal-body no-padding']", 4)
    Level_PO.inputID(u"subjectbundle_ttsubject_title", u" - 子项目")
    Level_PO.inputID(u"subjectbundle_ttsubject_resume", u" - 子项目")
    Level_PO.selectID(u"subjectbundle_ttsubject_type", u"党课")
    Level_PO.selectID(u"subjectbundle_ttsubject_fourLearnType", u"考量工作结合学")
    Level_PO.inputNAME(u"file", u"//Users/linghuchong/Downloads/51/Picture/4729.jpg")
    Level_PO.clickLINKTEXT(u'添加学习对象',2)
    Level_PO.clickXPATH(u"//input[@value='12110']", 2)
    Level_PO.clickXPATH(u"//button[@class='btn btn-success']", 5)
    Level_PO.screenTop(u'10000', 2)
    Level_PO.clickXPATH(u"//a[@data-target='#popup-target-group-owner-0']", 2)
    Level_PO.clickXPATH(u"//button[@class='btn btn-success btn-confirm-group-owner']", 2)
    Level_PO.screenTarget(u"//button[@class='btn btn-primary']", 2)
    Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)
    Level_PO.outIframe(2)

    '''提交'''
    Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 6)
    print u"C2，创建母项目 - 结束"


    '''检查是否需要审核人'''
    Level_PO.clickLINKTEXT(u'发件箱', 6)
    varString1 = Level_PO.rtnTRTD(u"//tr")
    if u"审核中" in str(varString1.split(varProject)[0]):
        Level_PO.clickLINKTEXT(u'退出登录', 2)

        Level_PO.inputID(u"_username", u"johnjinhao")
        Level_PO.inputID(u"_password", u"123456")
        Level_PO.clickTAGNAME(u'button', 2)
        print u"C1，电科党员学习教育平台 - johnjinhao 登录成功"

        Level_PO.clickLINKTEXT(u'项目管理', 2)
        Level_PO.clickLINKTEXT(u'待审核', 2)
        Level_PO.clickLINKTEXT(varProject, 2)
        Level_PO.clickLINKTEXT(u'通过', 6)
        Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)
        Level_PO.clickLINKTEXT(u'退出登录', 2)
        print u"C1，审核通过，johnjinhao退出系统"

        Level_PO.inputID(u"_username", u"yoyo")
        Level_PO.inputID(u"_password", u"123456")
        Level_PO.clickTAGNAME(u'button', 2)
        print u"C1，电科党员学习教育平台 - yoyo登录成功"
        Level_PO.clickLINKTEXT(u'项目管理', 2)
        Level_PO.clickLINKTEXT(u'发件箱', 2)
        # varString2 = Level_PO.rtnTRTD(u"//tr")
        # print varString2


    '''已发布'''
    x = str(Level_PO.printA(varProject))
    x = x.replace(u"http://10.111.3.5:88", u"")
    x = x.replace(u"/edit", u"/publish")
    Level_PO.clickXPATH("//a[@href='" + str(x) + "']", 2)
    Level_PO.clickXPATH(u"//button[@class='btn btn-primary']", 2)

