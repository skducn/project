# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2017-11-20
# Description: HJK, B端His 排版管理
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from HJK.PageObject.HJK10PO import *
varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间时分秒，格式：20170914143616982，类型是 str，
varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 当天日期年月格式：2016-06-28 ， 类型是 str

from selenium.webdriver.common.action_chains import ActionChains

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 测试环境

# 登录帐号、密码 ， 如：手机号 = 13816109060
varFstAccount = u"15020171114"
varPass = u"111111"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


print u">>>>>>>>>>>>>>>>>>>>>>>>>>> web后创建、发布项目 >>>>>>>>>>>>>>>>>>>>>>>>>>>"


driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver.log')
driver.implicitly_wait(10)

'''登录'''
Level_PO = LevelPO(driver)
HJK10_PO = HJK10PO(Level_PO)

Level_PO.openURL(1200, 900, varUrlPrefix , 3)
Level_PO.inputId(u"loginName", varFstAccount)
Level_PO.inputId(u"password", varPass)
Level_PO.clickXPATH(u"//button[@class='layui-btn layui-btn-big']", 2)
Level_PO.setMaximize()
print u"S1, 已登录 -> " + varFstAccount + u""


'''排版管理'''
Level_PO.clickID(u"menu0000_05", 2)
Level_PO.clickLINKTEXT(u"人员排班管理", 4)
Level_PO.inIframe(u"myFrame", 2)
Level_PO.printXpathText(u"//div[@class='location']")
Level_PO.clickXPATH(u"//a[@onclick=\"redirectEditPage('1', '136');\"]", 2)
Level_PO.clickXPATHright(u"//td[@data-date='2017-11-06']", u"right-context-menu")
Level_PO.clickXPATH(u"//li[@data-id='4']", 2)
sleep(1212)

'''架构切换'''
'''架构及用户管理'''

l_OrgUsers = Dangjian20_PO.orgUsers(varArchitecture)
print u"info - 可添加接收目标如下："
for i in range(len(l_OrgUsers)):
    print u"l_OrgUsers[" + str(i) + u"] = " + str(l_OrgUsers[i])

# 添加接收目标 - 组织架构
l_varReceiveObject = []
if varReceiveObject == "":
    # 默认给一个接收目标，或多个
    l_varReceiveObject = [l_OrgUsers[2]]  # 选择第一个接收目标
    l_varReceiveObject = [l_OrgUsers[0], l_OrgUsers[1], l_OrgUsers[3]]   # 选择第1、3接收目标
else:
    l_varReceiveObject = [varReceiveObject]

'''项目管理'''

Level_PO.clickLINKTEXT(u'项目管理', 2)

'''流程设置'''

# varFlow = Dangjian20_PO.flowSetup(u"del", u"all")
# print u"S3, 流程设置 " + varFlow


'''新建项目'''

Level_PO.clickLINKTEXT(u'新建项目',8)
Level_PO.inputId(u"subjectbundle_tttask_title", varProject)
Level_PO.inputId(u"subjectbundle_tttask_resume", varProject + u"描述")
Level_PO.jsRemoveReadonlyId(u"subjectbundle_tttask_beginDate")
Level_PO.inputId(u"subjectbundle_tttask_beginDate", varStartDate)
Level_PO.inputId(u"subjectbundle_tttask_beginDate", Keys.TAB)
Level_PO.jsRemoveReadonlyId(u"subjectbundle_tttask_endDate")
Level_PO.inputId(u"subjectbundle_tttask_endDate", varEndDate)
Level_PO.inputId(u"subjectbundle_tttask_endDate", Keys.TAB)

# # 附件 - 选择文件
# Level_PO.clickXPATH(u"//button[@data-target='#popup-task-attachments']", 2)
# Level_PO.clickXPATH(u"//input[@name='learn_source_id[]']", 2)
# Level_PO.clickXPATH(u"//button[@onclick='doAddAttachment()']", 2)

# 添加接收目标
if Level_PO.isElementText(u"添加接收目标"):
    Level_PO.clickLINKTEXT(u'添加接收目标', 2)

    if len(l_varReceiveObject) == 1:
        # 搜索 接收目标对象
        Level_PO.inputName(u'filter_company', l_varReceiveObject[0])
        Level_PO.clickLINKTEXT(u'查询', 2)
        # 勾选 对象
        varTRNum = Level_PO.getXpathsPartTextRow(u"//tr", l_varReceiveObject[0])
        varCheckNum = Level_PO.getXpathAttr(
            u"//tr[" + str(varTRNum) + u"]/td[1]/div[1]/label/input[@type='checkbox']", u"value")
        Level_PO.clickXPATH(u"//input[@value='" + str(varCheckNum) + u"']", 2)

    elif len(l_varReceiveObject) > 1:
        for i in range(len(l_varReceiveObject)):
            # 勾选 对象
            varTRNum = Level_PO.getXpathsPartTextRow(u"//tr", l_varReceiveObject[i])
            varCheckNum = Level_PO.getXpathAttr(
                u"//tr[" + str(varTRNum) + u"]/td[1]/div[1]/label/input[@type='checkbox']", u"value")
            Level_PO.clickXPATH(u"//input[@value='" + str(varCheckNum) + u"']", 2)
    else:
        print u"errorrrrrrrrrrr", sys._getframe().f_lineno, u"行，接收目标不存在！！！", __file__
        os._exit(0)

    Level_PO.clickXPATH(u"//button[@class='btn btn-success']", 2)
else:
    print u"warning, 本角色是最后一层架构，没有下级接收目标。"



'''添加子项目'''

Level_PO.screenTop(u'10000', 4)

Level_PO.clickLINKTEXT(u'添加子项目',4)
Level_PO.inputId(u"subjectbundle_tttask_subjects___name___title", u" - 子项目")
Level_PO.inputId(u"subjectbundle_tttask_subjects___name___resume", u" - 子项目")

# 四学方式
Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___fourLearnType", varLearnWay[0])
Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___fourLearnSeting", varLearnWay[1])

# 子项目封面 - 选择图片（自动选择一张）
Level_PO.inputName(u"file", u"//Users/linghuchong/Desktop/testpic/" + choice(varCover))
Level_PO.screenTop(u'10000', 4)

if varLearnWay[1] == "资料自学":
    if Level_PO.isElementXpath(u"//button[@class='btn btn-default btn-subject-detail-source-add']") == True :
        Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-source-add']", 6)
        Level_PO.clickXPATHs(u"//input[@name='learn_source_id[]' and @type='radio']", 3, 2)   # 选择第3个
        Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailSource(event);']", 6)
    else:
        print u"errorrrrrrrrrrr", sys._getframe().f_lineno, u"行，资料学习 - 添加学习内容按钮不存在！！！", __file__
        os._exit(0)

if varLearnWay[1] == "直播空间":
    # 直播时间
    Level_PO.jsRemoveReadonlyId(u"subjectbundle_tttask_subjects___name___planBeginDateYmd")
    Level_PO.inputId(u"subjectbundle_tttask_subjects___name___planBeginDateYmd", varLearnWay[12])
    Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___planBeginDateH", varLearnWay[13])
    Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___planBeginDateI", varLearnWay[14])
    Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___planEndDateH", varLearnWay[15])
    Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___planEndDateI", varLearnWay[16])

    # 添加学习内容
    if Level_PO.isElementXpath(u"//button[@class='btn btn-default btn-subject-detail-lesson-add']") == True:
        Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-lesson-add']", 4)
        Level_PO.inputId(u"lesson_name", varLearnWay[2])
        Level_PO.inputId(u"lesson_pin", varLearnWay[3])
        # 课程封面
        Level_PO.inputXpath(u"//div[@id='web-uploader-image-lesson_image_url-picker']/div[2]/input", u"//Users/linghuchong/Desktop/testpic/" + choice(varCover))
        # 全选 参与人员
        # Level_PO.clickXPATH(u"//input[@onclick='doLessonCheckAll(this)']", 2)
        Level_PO.inputId(u"lesson_manager_name", varLearnWay[4])
        Level_PO.inputId(u"lesson_manager_phone_number", varLearnWay[5])
        Level_PO.inputId(u"lesson_person_lecturer_name", varLearnWay[6])
        Level_PO.inputId(u"lesson_person_lecturer_phone_number", varLearnWay[7])
        # 以下可选项
        Level_PO.inputName(u"lesson_person_info_json[1][name]", varLearnWay[8])
        Level_PO.inputName(u"lesson_person_info_json[1][phone_number]", varLearnWay[9])
        Level_PO.inputName(u"lesson_person_info_json[2][name]", varLearnWay[10])
        Level_PO.inputName(u"lesson_person_info_json[2][phone_number]", varLearnWay[11])

        Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailLesson(this);']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-default cetc-popup-confirm-btn']", 4)

        # 多处来的事情
        Level_PO.clickXPATH(u"//button[@class='btn btn-default cetc-popup-confirm-btn']", 4)
        Level_PO.inputXpath(u"//div[@id='web-uploader-image-lesson_image_url-picker']/div[2]/input", u"//Users/linghuchong/Desktop/testpic/" + choice(varCover))
        Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailLesson(this);']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-default cetc-popup-confirm-btn']", 6)
        # 查看直播间号码
        Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-lesson-view']", 4)
        varBroadcaseNums = Level_PO.getXpathAttr(u"//input[@name='lesson_meeting_id']", u"value")
        print u"直播间号码：" + str(varBroadcaseNums)
        Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailLesson(this);']", 2)
        Level_PO.clickXPATH((u"//button[@class='btn btn-default cetc-popup-confirm-btn']"), 6)

    else:
        print u"errorrrrrrrrrrr", sys._getframe().f_lineno, u"行，直播空间 - 添加学习内容按钮不存在！！！", __file__
        os._exit(0)


elif len(varLearnWay) > 2 and len(varLearnWay) < 5:
    Level_PO.selectIdText(u"subjectbundle_tttask_subjects___name___type", varLearnWay[2])
    if varLearnWay[2] == "考试":
        # 添加学习内容
        if Level_PO.isElementXpath(u"//button[@class='btn btn-default btn-subject-detail-topSurvey-add']") == True:
            Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-topSurvey-add']", 2)
            try:
                if varLearnWay[3] == u"":
                    Level_PO.clickXPATHs(u"//input[@name='topSurveyId']", 1, 2)  # 默认选择第一个
                else:
                    Level_PO.clickXPATH(u"//input[@value='" + varLearnWay[3] + u"']", 2)
            except:
                Level_PO.clickXPATHs(u"//input[@name='topSurveyId']", 1, 2)  # 默认选择第一个
            Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailTopSurvey(event);']", 2)
        else:
            print u"errorrrrrrrrrrr", sys._getframe().f_lineno, u"行，考试 - 添加学习内容按钮不存在！！！", __file__
            os._exit(0)
    if varLearnWay[2] == "投票":
        # 添加学习内容
        if Level_PO.isElementXpath(u"//button[@class='btn btn-default btn-subject-detail-topVote-add']") == True:
            Level_PO.clickXPATH(u"//button[@class='btn btn-default btn-subject-detail-topVote-add']", 2)
            try:
                if varLearnWay[3] == u"":
                    Level_PO.clickXPATHs(u"//input[@name='topVoteId']", 1, 2)  # 默认选择第一个
                else:
                    Level_PO.clickXPATH(u"//input[@value='" + varLearnWay[3] + u"']", 2)
            except:
                Level_PO.clickXPATHs(u"//input[@name='topVoteId']", 1, 2)  # 默认选择第一个
            Level_PO.clickXPATH(u"//button[@onclick='doChangeSubjectDetailTopVote(event);']", 2)
        else:
            print u"errorrrrrrrrrrr", sys._getframe().f_lineno, u"行，投票 - 添加学习内容按钮不存在！！！", __file__
            os._exit(0)


# 直播时间（默认）

'''添加学习对象'''

Level_PO.screenTop(u'10000', 4)
Level_PO.clickLINKTEXT(u'添加学习对象', 4)

#  如果为空，默认当前架构
if varLearnOrg == u"":
    if varLearnObject != u"":
    # 当前架构，查询后选择1个或多个学习对象
        Level_PO.inputXpath(u"//input[@name='name'][@type='text']", varLearnObject)
        Level_PO.clickXPATH(u"//a[@onclick='doSearchUserLogin(this)']", 4)

        if Level_PO.isElementXpath(u"//input[@data-name='" + varLearnObject + u"']"):
            Level_PO.clickXPATH(u"//input[@data-name='" + varLearnObject + u"']", 2)
        else:
            # 如果搜索无结果则全选学习对象
            Level_PO.inputClearXpath(u"//input[@name='name'][@type='text']")
            Level_PO.clickXPATH(u"//a[@onclick='doSearchUserLogin(this)']", 4)
            Level_PO.clickXPATH(u"//input[@onclick='doCheckAllUser(this)']", 2)
            print u"warning, '" + varLearnObject + u"' 查无此人，系统自动选项所有学习对象。"

    elif varLearnObject == u"":
        # 当前架构，全选学习对象
        Level_PO.clickXPATH(u"//input[@onclick='doCheckAllUser(this)']", 2)
else:
    # 选择其他架构
    varTRNum = Level_PO.getXpathsPartTextRow(u"//table[@id='select-company-container']/tbody/tr", varLearnOrg)
    # 将滚动条定位到需要显示的元素位置
    Level_PO.screenTarget(u"//table[@id='select-company-container']/tbody/tr[" + str(varTRNum) + u"]/td[1]/div[2]/a[1]/i", 2)
    Level_PO.clickXPATH(u"//table[@id='select-company-container']/tbody/tr[" + str(varTRNum) + u"]/td[1]/div[2]/a[1]/i", 6)
    if varLearnObject == u"":
        # 全选学习对象
        Level_PO.clickXPATH(u"//input[@onclick='doCheckAllUser(this)']", 2)
    elif varLearnObject != u"":
        # 选择架构后，搜索学习对象，并选中某人
        Level_PO.inputXpath(u"//input[@type='text' and @name='name']", varLearnObject)
        sleep(2)
        Level_PO.clickXPATH(u"//a[@onclick='doSearchUserLogin(this)']", 4)
        varValue = Level_PO.getXpathsAttr(u"//input[@data-name='" + varLearnObject + u"']", u"value")
        Level_PO.clickXPATH(u"//input[@value='" + str(varValue[0]) + u"']", 2)

# 提交 - 添加学习对象
Level_PO.clickXPATH(u"//button[@onclick='doAddSubjectUser(this)']", 5)

Level_PO.screenTop(u'10000', 4)

# 设置群主 ，选择学习对象
Level_PO.clickXPATH(u"//a[@onclick='doChangeGroupOwner(this)']", 2)
Level_PO.clickXPATH(u"//button[@class='btn btn-success btn-confirm-group-owner']", 2)
Level_PO.clickXPATH(u"//button[@onclick='doAddSubject(this)']", 2)

Level_PO.clickXPATH(u"//form[@onsubmit='doSubmitForm()']/div[5]/button", 2)  # 提交
print u"S4, 创建项目成功"


'''发布项目'''

Level_PO.clickXPATH(u"//div[@id='popup-publish-form']/div[1]/div[1]/div[2]/form/button", 2)  # 确定
print u"S5, 发布项目成功"
print u">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


# 直播
Level_PO.openURL(1600, 1200, u"https://meeting.iotcetc.com/html5/live-server/index.html", 3)
Level_PO.inputXpath(u"//input[@ng-model='meetingNumber']", varBroadcaseNums)
Level_PO.inputXpath(u"//input[@ng-model='phoneNumber']", varLearnWay[5])
Level_PO.clickXPATH(u"//button[@ng-click='login(meetingNumber,phoneNumber);']", 8)
# 直播间密码
Level_PO.inputXpath(u"//input[@ng-model='pin']", varLearnWay[3])
Level_PO.clickXPATH(u"//button[@ng-click='joinMeetingWithPin(pin)']", 2)

Level_PO.clickXPATH(u"//button[@ng-click='startRtmp()']", 2)
Level_PO.clickXPATHs(u"//button[@ng-click='action.callback()']", 2, 2)


# 发布后页面停留在 发件箱


# 客户端

from android1_5 import AppDangjian

# 登录
AppDangjian().login()
# AppDangjian().exitMember()




# sleep(1212)
#
# '''检查是否需要审核人'''
# Level_PO.clickLINKTEXT(u'发件箱', 6)
# varString1 = Level_PO.rtnTRTD(u"//tr")
# if u"审核中" in str(varString1.split(varProject)[0]):
#     Level_PO.clickLINKTEXT(u'退出登录', 2)
#
#     Level_PO.inputId(u"_username", u"johnjinhao")
#     Level_PO.inputId(u"_password", u"123456")
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
#     Level_PO.inputId(u"_username", u"yoyo")
#     Level_PO.inputId(u"_password", u"123456")
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

