# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 2.0
# Date       : 2017-11-6
# Description: 电科党员学习教育WEB平台, 创建、发布项目
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Dangjian.PageObject.Dangjian20PO import *
varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间时分秒，格式：20170914143616982，类型是 str，
varYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 当天日期年月格式：2016-06-28 ， 类型是 str

# 客户端

from android1_5 import AppDangjian
#
# # 登录
AppDangjian().login(u"13816109060", u"123456")
#
print "end"
sleep(1212)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 测试环境
# varUrlPrefix = u"http://10.111.3.5:88"  # 访问URL
#
# varFstAccount = u"jinhao"   # 登录帐号
# varPass = u"a12345"   # 密码
#
# # varArchitecture = u"中电科软信测试部"  # 帐号角色
# varArchitecture = u"中电科软件信息服务有限公司党委"  # 帐号角色
#
# varProject = u"党员学习任务" + varTime  # 项目标题
# varStartDate = u"2017-06-28"   # varYMD
# varEndDate = u"2017-11-28"   # varYMD
# varReceiveObject = u"长江本部第一党支部"  # 添加接收目标 - 组织架构
#
# # ['问卷答题引导学','化小专题交流学','考量工作结合学','对照言行自省学','其他']
# # ['党小组会','支部大会','支委会','党课','组织生活会','民主生活会','主题讨论','资料自学','考试','投票','学习笔记','直播空间']
#
# varLearnWay = u"问卷答题引导学"   # 四学方式1
# varLearnWay2 = u"问卷答题"   # 四学方式2
# varLearnWay3 = u"投票"    # 四学方式3
# varVote = u"3"
# varExam = u"31"
# # 随机选择列表中的某个元素
# varCover = ['100.jpg','101.jpg','102.jpg','103.jpg','104.jpg']  # 子项目封面 - 选择图片 180*120
# varStartPeriod = varYMD
# varEndPeriod = varYMD
# varLearnOrg = u"中电科软信测试部"  # 添加学习对象 - 组织架构
# varLearnObject = u"令狐冲"   # 添加学习对象 - 学习对象
# # varLearnOrg = u"长江本部第一党支部"  # 添加学习对象 - 组织架构
# # varLearnObject = u"梅玫139"   # 添加学习对象 - 学习对象

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 生产环境

# 登录帐号、密码 ， 如：手机号 = 13816109060
varFstAccount = u"wuxiaohao"
varPass = u"a12345"
# 架构 ， 如：软信测试第一支部  , 测试第一党小组
varArchitecture = u"软信测试第一支部"
# 添加接收目标 - 组织架构 ， 如：u"运营测试第三小组"  ， 如果为空默认选择组织列表中第一个。
varReceiveObject = u""
# 项目标题
varProject = u"党员学习任务" + varTime
# 开始时间，结束时间
varStartDate = u"2017-06-28"
varEndDate = u"2017-11-28"

# 四学方式 - 学习内容
# varLearnWay = [u"问卷答题引导学", u"问卷答题", u"考试", u"21"]  # 选择编号为120的试卷, 如果第四个参数不存在或为空，则默认选择第一个试卷
# varLearnWay = [u"问卷答题引导学", u"问卷答题", u"考试"]  # 默认选择第一个试卷
# varLearnWay = [u"问卷答题引导学", u"问卷答题", u"投票", u"19"]
# varLearnWay = [u"问卷答题引导学", u"问卷答题", u"投票", u""]
# varLearnWay = [u"化小专题交流学", u"资料自学"]
# varLearnWay = [u"考量工作结合学", u"心得笔记"]
# varLearnWay = [u"对照言行自省学", u"组织生活会"]
# varLearnWay = [u"对照言行自省学", u"三会一课", u'支委会']
# varLearnWay = [u"对照言行自省学", u"三会一课", u'支部大会']
# varLearnWay = [u"对照言行自省学", u"三会一课", u'党小组会']
# varLearnWay = [u"对照言行自省学", u"三会一课", u'党课']
# varLearnWay = [u"对照言行自省学", u"民主生活会"]
varLearnWay = [u"其他", u"直播空间", u"大家的直播课堂", u"123456", u"管理员吴总", u"13611958388", u"讲师测试张", u"13636371320", u"客人1", u"13188888888", u"客人2", u"13288888888", varYMD, u"04", u"11", u"22", u"55"]

# 子项目封面 - 选择图片
varCover = ['100.jpg', '101.jpg', '102.jpg', '103.jpg', '104.jpg']
# 考试期间
varStartPeriod = varYMD
varEndPeriod = varYMD
# 添加学习对象 - 组织
varLearnOrg = u"测试第一党小组"    #  为空表示当前组织
# 添加学习对象 - 学习对象
varLearnObject = u"吴小浩"   # 如果查无此人，则选择所有的人
# varLearnObject = u""  #  为空表示选择所有人

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


print u">>>>>>>>>>>>>>>>>>>>>>>>>>> web后创建、发布项目 >>>>>>>>>>>>>>>>>>>>>>>>>>>"


driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver.log')
driver.implicitly_wait(10)

'''登录'''
Level_PO = LevelPO(driver)

# 直播
Level_PO.openURL(1600, 1200, u"https://meeting.iotcetc.com/html5/live-server/index.html", 3)
Level_PO.inputXpath(u"//input[@ng-model='meetingNumber']", u"097010")
Level_PO.inputXpath(u"//input[@ng-model='phoneNumber']", u"13611958388")
Level_PO.clickXPATH(u"//button[@ng-click='login(meetingNumber,phoneNumber);']", 8)
# 直播间密码
Level_PO.inputXpath(u"//input[@ng-model='pin']", u"123456")
Level_PO.clickXPATH(u"//button[@ng-click='joinMeetingWithPin(pin)']", 2)

Level_PO.clickXPATH(u"//button[@ng-click='startRtmp()']", 2)
Level_PO.clickXPATHs(u"//button[@ng-click='action.callback()']", 2, 2)

# 聊天室，输入聊天内容
Level_PO.inputXpath(u"//input[@ng-model='chatMessage']", u"test123")
Level_PO.clickXPATH(u"//form[@class='ng-valid ng-dirty ng-valid-parse']/button", 2)  # 发送
Level_PO.inputXpath(u"//input[@ng-model='chatMessage']", u"haha123456")
Level_PO.clickXPATH(u"//form[@class='ng-valid ng-dirty ng-submitted ng-valid-parse']/button", 2)  # 发送
Level_PO.inputXpath(u"//input[@ng-model='chatMessage']", u"测试党建项目卡卡中文支持程度可以包含多少字符包括澳")
Level_PO.clickXPATH(u"//form[@class='ng-valid ng-dirty ng-submitted ng-valid-parse']/button", 2)  # 发送
list1 = Level_PO.getXpathsText(u"//body")
str1 = "".join(list1)
if u"test123" in str1 and u"haha123456" in str1 and u"测试党建项目卡卡中文支持程度可以包含多少字符包括澳" in str1:
    print "ok"
else:
    print "error"


# 挂断
Level_PO.clickXPATH(u"//button[@ng-click='quitConference()']", 2)
Level_PO.clickXPATHs(u"//button[@ng-click='action.callback()']", 2, 2)  # 退出


print "end"
sleep(1212)



Dangjian20_PO = Dangjian20PO(Level_PO)

Level_PO.openURL(1200, 900, varUrlPrefix + u"/dangjian1.5/web/app.php/DJsecurity/security/login", 3)
Level_PO.inputId(u"_username", varFstAccount)
Level_PO.inputId(u"_password", varPass)
Level_PO.inputId(u"_captcha", Level_PO.getCode(u"test.jpg", 2060, 850, 2187, 900))  # 获取并输入验证码
Level_PO.clickTAGNAME(u'button', 2)
# 多次遍历获取并输入验证码
for i in range(100):
    if Level_PO.isElementId(u"_captcha"):
        Level_PO.inputId(u"_username", varFstAccount)
        Level_PO.inputId(u"_password", varPass)
        Level_PO.inputId(u"_captcha", Level_PO.getCode(u"test1.jpg", 2060, 792, 2187, 849))
        Level_PO.clickTAGNAME(u'button', 2)
    else:
        break
Level_PO.setMaximize()
print u"S1, 已登录 -> " + varFstAccount + u""


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

