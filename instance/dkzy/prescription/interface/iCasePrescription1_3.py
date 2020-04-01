# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-7-26
# Description: 党建接口1.5
# https://md5jiami.51240.com/  MD5在线加密
# *******************************************************************************************************************************

from iDriverPrescription import *
from Public.PageObject.DatabasePO import *
# Database_PO = DatabasePO('10.111.3.5', 'cetc', '20121221', 'dangjian')



# 我的手机
varPhone = sheet0.cell_value(12, 1)
varPass = sheet0.cell_value(13, 1)

# # 好友的 手机号 、二维码、userId
# varPhone_Friend5 = sheet0.cell_value(14, 1)
# varPass_Friend5 = sheet0.cell_value(15, 1)
# varEdCode_Friend5 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend5), "ed_code")
# varUserId_Friend5 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend5), "user_id")
#
# varPhone_Friend6 = sheet0.cell_value(16, 1)
# varPass_Friend6 = sheet0.cell_value(17, 1)
# varEdCode_Friend6 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend6), "ed_code")
# varUserId_Friend6 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend6), "user_id")
#
# varPhone_Friend7 = sheet0.cell_value(18, 1)
# varPass_Friend7 = sheet0.cell_value(19, 1)
# varEdCode_Friend7 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend7), "ed_code")
# varUserId_Friend7 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend7), "user_id")
#
# varPhone_Friend8 = sheet0.cell_value(20, 1)
# varPass_Friend8 = sheet0.cell_value(21, 1)
# varEdCode_Friend8 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend8), "ed_code")
# varUserId_Friend8 = Database_PO.search1get1("tt_user_login", "phone_number", str(varPhone_Friend8), "user_id")


# 新群名
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
varNewGroupName = u"群" + varTimeYMDHSM

# for i in range(3):
#     varRandom4 = "".join(myfunc(3))
#     print u"80000013" + varRandom4
# sleep(1212)

# 已完成 到 16245

# 登录 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for k in range(3001):
    varPhone = str(80000013310 + k)

    # varPhone = u"80000013100"
    myMd5 = hashlib.md5()
    myMd5.update(u"a123456")
    myMd5_Digest = myMd5.hexdigest()
    resp = Icase("登录","i1_N1_C1", myMd5_Digest, varPhone)
    varUserId = resp.split("userId\":\"")[1].split("\"")[0]
    varSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
    varImVoip = resp.split("imVoip\":\"")[1].split("\"")[0]
    print u"varUserId = " + varUserId
    # print u"varSessionId = " +varSessionId
    # print u"varImVoip = " + varImVoip
    list1 = []
    listtime = []
    # test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(20):
        varTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 当天日期时间，格式：20170914143616982，类型是 str，
        resp = Icase("四学 - 引导学 - 提问","i15_N17_C1",varUserId, varSessionId, varTime, "提出100个理由")
        varQuestionId = resp.split("questionId\":\"")[1].split("\"")[0]
        listtime.append(varTime)
        list1.append(varQuestionId)

    # varPhone = u"80000016000"
    # myMd5 = hashlib.md5()
    # myMd5.update(u"a123456")
    # myMd5_Digest = myMd5.hexdigest()
    # resp = Icase("登录","i1_N1_C1", myMd5_Digest, varPhone)
    # varUserId = resp.split("userId\":\"")[1].split("\"")[0]
    # varSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
    #
    # for j in range(20):
    #     resp = Icase("四学 - 引导学 - 回答", "i15_N19_C1", varUserId, varSessionId, list1[j], u"压测"+listtime[j]+str(j))
    # # print varPhone
    list1 =[]
    listtime =[]

print "end"
sleep(1212)

# varGroupId = 192
# varImGroupId = g800027275
# varNewGroupName = 群20170811173041
# resp = Icase("我的学习群 - 添加、删除群成员", "i15_N38_C1", varUserId, varSessionId, "188", "g800027271", str(varUserId_Friend1) + "," +str(varUserId_Friend4), "1")  # 1 = 添加，2 = 删除

# resp = Icase("我的学习群 - 一键解散群", "i15_N36_C1", varUserId, varSessionId, "192", "g800027275")
# resp = Icase("我的学习群 - 一键解散群", "i15_N36_C1", varUserId, varSessionId, varGroupId, varImGroupId)

# # 35，我的学习群 - 成员退出群聊（1.5）>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# print "\nDKDJ1.5_N35 " + ">" * 150
# resp = Icase("我的学习群 - 成员退出群聊", "i15_N35_C1", varUserId, varSessionId, "188", "g800027271")

# sleep(1212)

resp = Icase("头条列表","i15_N1_C1", varUserId, varSessionId, "1", "1", "20")
resp = Icase("随时学 - 音频列表","i15_N2_C1", varUserId, varSessionId, "1", "20", "1")
resp = Icase("随时学 - 音频详情","i15_N3_C1", varUserId, varSessionId, "11")
resp = Icase("随时学 - 时长列表","i15_N4_C1", varUserId, varSessionId, "30", "2")
resp = Icase("随时学 - 视频列表","i15_N5_C1", varUserId, varSessionId, "1", "20", "1","30")
resp = Icase("随时学 - 我的书架","i15_N6_C1", "1", "20",varUserId, varSessionId)
resp = Icase("随时学 - 热门推荐","i15_N7_C1", "1", "20", varUserId, varSessionId)
resp = Icase("随时学 - 书的类别列表","i15_N8_C1", "150", "1", "20", varUserId, varSessionId)

resp = Icase("随时学 - 加入书架", "i15_N9_C1", "196", varUserId, varSessionId)
resp = Icase("随时学 - 加入书架", "i15_N9_C2", "19611212", varUserId, varSessionId)

resp = Icase("随时学 - 移出书架", "i15_N10_C1", "196", varUserId, varSessionId)
resp = Icase("随时学 - 移出书架", "i15_N10_C2", "19611212", varUserId, varSessionId)

resp = Icase("收藏 - 我的讲师列表", "i15_N11_C1", varUserId, varSessionId, "1", "1")
resp = Icase("收藏 - 我的收藏列表", "i15_N12_C1", varUserId, varSessionId, "1", "1")


# 四学 - 引导学
resp = Icase("四学 - 引导学 - 提问","i15_N17_C1", varUserId, varSessionId, u"john", u"提出100个理由")
varQuestionId = resp.split("questionId\":\"")[1].split("\"")[0]

resp = Icase("四学 - 引导学 - 回答", "i15_N19_C1", varUserId, varSessionId, varQuestionId, u"内容123")
varAnswerId = resp.split("answerId\":\"")[1].split("\"")[0]


resp = Icase("四学 - 引导学 - 点赞", "i15_N20_C1", varUserId, varSessionId,varQuestionId, varAnswerId,"2")  # 2=回答 , 提问的人给回答点赞
# resp = Icase("四学 - 引导学 - 点赞", "i15_N20_C2", varUserId, varSessionId, "1")  # 1=问题 ， 回答的人给提问点赞

resp = Icase("四学 - 引导学 - 你问我答列表", "i15_N13_C1", varUserId, varSessionId, "1", "20")

resp = Icase("四学 - 引导学 - 你问我答头部信息详情", "i15_N14_C1", varUserId, varSessionId, varQuestionId)
resp = Icase("四学 - 引导学 - 你问我答回答详情", "i15_N15_C1", varUserId, varSessionId, varQuestionId,"1","1")

# # 16，四学 - 引导学 - 问卷答题列表(V1.5)(不用，使用公共代替)>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# print "\nDKDJ1.5_N16 " + ">" * 150
# resp = Icase("i15_N16_C1", varUserId, varSessionId, "1", "10")



resp = Icase("四学 - 引导学 - @的人列表", "i15_N18_C1", varUserId, varSessionId, "1", "20")


resp = Icase("四学 - 引导学 - 设置最佳答案","i15_N21_C1", varUserId, varSessionId, varQuestionId, varAnswerId)
resp = Icase("四学 - 交流学 - 群组交流列表","i15_N22_C1", varUserId, varSessionId, "1", "10")

resp = Icase("广告页","i15_N23_C1", varUserId, varSessionId)

resp = Icase("IM登录","i15_N24_C1", varUserId, varSessionId, "1")
resp = Icase("IM登录","i15_N24_C2", varUserId, varSessionId, "0")

resp = Icase("用户主页 - 个人资料","i15_N25_C1", varUserId, varSessionId,"7","0","0","","0","1","1")
resp = Icase("用户主页 - 个人资料分类","i15_N26_C1", varUserId, varSessionId)

resp = Icase("用户主页 - 个人笔记","i15_N27_C1", varUserId, varSessionId,"","","0","1","1")
varSubjectNoteId = resp.split("subject_note_id\":\"")[1].split("\"")[0]
print u"varSubjectNoteId = " + varSubjectNoteId

resp = Icase("用户主页 - 个人笔记","i15_N28_C1", varUserId, varSessionId, "1", "1")
resp = Icase("用户主页 - 笔记评论","i15_N29_C1", varUserId, varSessionId, varSubjectNoteId, "内容一致")
resp = Icase("用户主页 - 首页新闻头条","i15_N30_C1", varUserId, varSessionId)
resp = Icase("其他功能 - 选择架构","i15_N31_C1", varUserId, varSessionId, "")



# 加好友

resp = Icase("我的学习群 - 好友信息","i15_N52_C1", varUserId, varSessionId, str(varEdCode_Friend5))

resp = Icase("我的学习群 - 添加好友","i15_N51_C1", varUserId, varSessionId, str(varEdCode_Friend5))


# 好友登录,接受邀请
myMd5 = hashlib.md5()
myMd5.update(str(varPass_Friend5))
varPass_Friend1_Md5 = myMd5.hexdigest()
resp = Icase("登录", "i1_N1_C1", varPass_Friend1_Md5, str(varPhone_Friend5))
varUserId_Friend5 = resp.split("userId\":\"")[1].split("\"")[0]
varSessionId_Friend5 = resp.split("userSessionId\":\"")[1].split("\"")[0]

# 新的朋友列表 中 显示 被接受人的id ，这个id = requestId
resp = Icase("我的学习群 - 新的朋友列表", "i15_N55_C1", str(varUserId_Friend5), varSessionId_Friend5)
x = resp.split(",\"friendId\":\"" + varUserId)[0]
varRequestId = str(x).split("{")[x.count("{")].replace('"', "").replace("id:", "")

resp = Icase("我的学习群 - 接受好友请求", "i15_N53_C1", str(varUserId_Friend5), varSessionId_Friend5, varRequestId, "1")   # 1 = 接收

# 删除新的朋友
# resp = Icase("我的学习群 - 删除好友请求","i15_N53_C1", str(varUserId_Friend5), varSessionId_Friend5, varRequestId, "0")   # 0 = 删除

# # 删除通讯录中的好友
resp = Icase("用户主页 - 删除好友","i15_N47_C1",  varUserId, varSessionId, str(varUserId_Friend5))


resp = Icase("我的学习群 - 通讯录列表", "i15_N54_C1", varUserId, varSessionId)




resp = Icase("我的学习群 - 新建群", "i15_N32_C1", varUserId, varSessionId, varNewGroupName)
varGroupId = resp.split("group_id\":\"")[1].split("\"")[0]
varImGroupId = resp.split("imGroupId\":\"")[1].split("\"")[0]
print u"varGroupId = " + str(varGroupId)
print u"varImGroupId = " + str(varImGroupId)
print u'varNewGroupName = ' + str(varNewGroupName)


resp = Icase("我的学习群 - 获取群信息", "i15_N33_C1", varUserId, varSessionId, varGroupId)
resp = Icase("我的学习群 - 群消息免打扰", "i15_N34_C1", varUserId, varSessionId, varGroupId,"0")  # 0 = 否   ，是否打扰
# resp = Icase("我的学习群 - 群消息免打扰", "i15_N34_C2", varUserId, varSessionId, varGroupId,"1")  # 1 = 是



# 群成员是已存在的好友
resp = Icase("我的学习群 - 添加、删除群成员", "i15_N38_C1", varUserId, varSessionId, varGroupId, varImGroupId, str(varUserId_Friend5), "1")  # 1 = 添加，2 = 删除
# resp = Icase("我的学习群 - 添加、删除群成员", "i15_N38_C1", varUserId, varSessionId, varGroupId, varImGroupId, str(varPhone_Friend5) + "," +str(varPhone_Friend8), "1")  # 1 = 添加，2 = 删除
# resp = Icase("我的学习群 - 添加、删除群成员", "i15_N38_C1", varUserId, varSessionId, varGroupId, varImGroupId, str(varUserId_Friend1), "2")  # 1 = 添加，2 = 删除


# varPhone_Friend8 退出群
myMd5 = hashlib.md5()
myMd5.update(str(varPass_Friend5))
varPass_Friend1_Md5 = myMd5.hexdigest()
resp = Icase("登录", "i1_N1_C1", varPass_Friend1_Md5, str(varPhone_Friend5))
varUserId_Friend5 = resp.split("userId\":\"")[1].split("\"")[0]
varSessionId_Friend5 = resp.split("userSessionId\":\"")[1].split("\"")[0]
resp = Icase("我的学习群 - 成员退出群聊", "i15_N35_C1", varUserId_Friend5, varSessionId_Friend5, varGroupId, varImGroupId)



resp = Icase("我的学习群 - 群成员列表","i15_N37_C1", varUserId, varSessionId, varGroupId)

varNewGroupName_R = varNewGroupName + "（改）"
resp = Icase("我的学习群 - 修改群名称", "i15_N39_C1", varUserId, varSessionId, varImGroupId, varGroupId, varNewGroupName_R)
# # 检查群名是否修改成功
# resp = Icase("我的学习群 - 获取群信息", "i15_N33_C1", varUserId, varSessionId, varGroupId)
# varGroupName = resp.split("group_name\":\"")[1].split("\"")[0]
# if varGroupName == varNewGroupName_R: print "OK , 修改群名称"
# else: print "errorrrrrrrrrr, 修改群名称"


resp = Icase("我的学习群 - 群聊记录", "i15_N40_C1", varUserId, varSessionId, varImGroupId, varGroupId,"1","1")
resp = Icase("我的学习群 - 一键解散群", "i15_N36_C1", varUserId, varSessionId, varGroupId, varImGroupId)


# # 36，我的学习群 - 一键解散群（1.5）>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# print "\nDKDJ1.5_N36 " + ">" * 150
# # type=1 讨论小组， type=2 学习群
# # resp = Icase("i15_N36_C1", varUserId, varSessionId, varGroupId, varImGroupId, "1")
# resp = Icase("i15_N36_C2", varUserId, varSessionId, varGroupId, varImGroupId, "2")

# #######################################################

resp = Icase("设计师榜","i15_N41_C1", varUserId, varSessionId)
resp = Icase("学习计划","i15_N42_C1", varUserId, varSessionId,"1","1","1")
varSubjectId = resp.split("subject_id\":\"")[1].split("\"")[0]
varLearn_plan_id = resp.split("learn_plan_id\":\"")[1].split("\"")[0]

resp = Icase("学习计划 - 项目详情", "i15_N43_C1", varUserId, varSessionId,"2", varSubjectId)  # 子项目
# resp = Icase("i15_N43_C1", varUserId, varSessionId,"1",varLearn_plan_id)  # 母项目 的id不知道 ？？？


resp = Icase("学习计划 - 学习项目排行榜", "i15_N44_C1", varUserId, varSessionId,"0","0","1","1")

resp = Icase("随时学 - 热门标签", "i15_N45_C1", varUserId, varSessionId)


# # 46,随时学 - 根据模块名称找数据（1.5）>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# print "\nDKDJ1.5_N46 " + ">" * 150
# resp = Icase("i15_N46_C1", varUserId, varSessionId,"1","1","2_你问我答")


resp = Icase("直播信息","i15_N48_C1", varUserId, varSessionId,"344")

resp = Icase("驾驶舱","i15_N49_C1", varUserId, varSessionId, "2017-08-01")

resp = Icase("学习计划 - 小组信息","i15_N50_C1", varUserId, varSessionId, "2")

resp = Icase("四学 - 引导学 - 搜索","i15_N56_C1", varUserId, varSessionId, u"123467890john","1","1")

