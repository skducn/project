# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-6-26
# Description: 医云谷 - 医务端
# https://md5jiami.51240.com/  MD5在线加密
# *******************************************************************************************************************************

# 云会诊
# varHost = '10.111.3.6'
# varUser = 'cetc'
# varPasswd = '20121221'
# varDatabase = 'yunhuizhen_v2'

from YHZinterfaceDriver import *
myMd5 = hashlib.md5()
myMd5.update(varPass)
myMd5_Digest = myMd5.hexdigest()
# Icase("YYG1_N1_C1", "RtnOK", "{\"codeType\":\"register\",\"phoneNumber\":\"" + varPhone + "\"}")


def response(interName, interUrl, interParam, *rtnMessageStatus):
    m1 = md5.new()
    # m1.update(json.dumps(varParam).replace(" ", "") + "123456")
    m1.update(interParam + "123456")
    values = {"check": m1.hexdigest(), "json": interParam}
    x = varURL + interUrl
    resp = urllib2.urlopen(urllib2.Request(x, json.dumps(values))).read()
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if u"操作成功" in str(resp):
        print u"[OK] => " + interName
        if rtnMessageStatus == ('y',):
            print u"    [paramIN] => " + interUrl + u" , " + str(values)
            print u"    [paramOUT] => " + str(resp)
    else:
        print u"[errorrrrrrrrrr] => " + interName
        print u"    [paramIN] => " + interUrl + u" , " + str(values)
        print u"    [paramOUT] => " + str(resp)
    return resp



# # 1,发送验证码
# resp = response(u"发送验证码",'/v1/system/getSMSCode',"{\"codeType\":\"register\",\"phoneNumber\":\"" + varPhone + "\"}",'y')
# varCode = resp.split("code")[1].split("}")[0].replace('"',"").replace(":","")
# print u"////////// " + varPhone + u'的验证码 = ' + str(varCode)

#
# # 2,检验验证码
# resp = response(u"[检验验证码]",'/v1/system/checkCode',"{\"codeType\":\"register\",\"phoneNumber\":\"" + varPhone + "\",\"code\":\"" + str(varCode) + "\"}","y")
#
#
# # 3,上传图片，fileTye(1=头像)
# f = open(r'//Users//linghuchong//Downloads//51//Picture//flying.jpg','rb')
# ls_f = base64.b64encode(f.read())
# f.close()
# resp = response(u"上传图片",'/v1/system/uploadImage',"{\"imageFile\":\"" + ls_f + "\",\"fileType\":\"1\"}","y")


# 4,登录
resp = response(u"登录",'/v1/user/login',"{\"phoneNumber\":\"" + varPhone + "\",\"passWord\":\"" + myMd5_Digest + "\",\"identityType\":\"1\"}",'y')
varUserId = resp.split("userId\":\"")[1].split("\"")[0]
varUserSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
print u'////////// userId = ' + varUserId
print u'////////// userSessionId = ' + varUserSessionId



# # 5,找回密码或者更新密码
# m1 = md5.new()
# m1.update("b123456")
# myMd5_Digest = m1.hexdigest()
# print myMd5_Digest
# 忘记密码 type = 0
# resp = response(u'找回密码','/v1/user/findPassWord',"{\"phoneNumber\":\"" + varPhone + "\",\"passWord\":\"" + myMd5_Digest + "\",\"verificationCode\":\"" + str(varCode) + "\",\"type\":\"0\"}",'y')
# 更新密码 type = 1
# resp = response(u'找回密码','/v1/user/findPassWord',"{\"userId\":\"" + varUserId + "\",\"phoneNumber\":\"" + varPhone + "\",\"passWord\":\"" + myMd5_Digest + "\",\"verificationCode\":\"" + str(varCode) + "\",\"type\":\"1\"}",'y')

# # 校验手机号是否已经注册 ????
# resp = response(u"校验手机号是否已经注册",'/v1/user/checkPhone',"{\"phoneNumber\":\"" + varPhone + "\",\"identityType\":\"1\"}",'y')



# 7.机构列表
resp = response(u"7,机构列表",'/v1/meetingSubscribe/orgList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"1\",\"pageNum\":\"1\"}",'y')
varOrgId = resp.split("orgId\":\"")[1].split("\"")[0]
print u'////////// orgId = ' + varOrgId
varOrgName = resp.split("orgName\":\"")[1].split("\"")[0]
print u'////////// orgName = ' + varOrgName

# 8,科室列表
resp = response(u"8,科室列表",'/v1/meetingSubscribe/officeList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"1\",\"pageNum\":\"1\",\"orgId\":\"" + varOrgId + "\"}",'y')
varOfficeId = resp.split("officeId\":\"")[1].split("\"")[0]
print u'////////// officeIdList = ' + varOfficeId
varOfficeName = resp.split("officeName\":\"")[1].split("\"")[0]
print u'////////// officeName = ' + varOfficeName

# 9,医生列表
resp = response(u"9,医生列表",'/v1/meetingSubscribe/doctorList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"1\",\"pageNum\":\"1\",\"officeIdList\":\"" + varOfficeId + "\"}",'y')
varDoctorId = resp.split("doctorId\":\"")[1].split("\"")[0]
print u'////////// doctorId = ' + varDoctorId
varDoctorName = resp.split("doctorName\":\"")[1].split("\"")[0]
print u'////////// doctorName = ' + varDoctorName


# # 11,添加患者
# # 同一个患者不能多次添加
# resp = response(u"11,添加患者",'/v1/meetingSubscribe/addPatient',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"officeName\":\""+varOfficeName+"\",\"officeId\":\""+ varOfficeId + "\",\"diagnosisNo\":\"1234567\",\"name\":\"王志文\",\"idCard\":\"610430198206156693\",\"age\":\"33\",\"phoneNumber\":\"13816109090\",\"orgName\":\""+varOrgName+"\",\"orgId\":\""+varOrgId+"\",\"diseasyHistory\":\"无\",\"doctorId\":\""+varDoctorId+"\",\"doctorName\":\""+varDoctorName+"\"}",'y')
# varPatientId = resp.split("patientId\":\"")[1].split("\"")[0]
# print u'////////// patientId = ' + varPatientId

# 10,患者列表
resp = response(u"10,患者列表",'/v1/meetingSubscribe/patientList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"1\",\"pageNum\":\"1\",\"searchConent\":\"王\"}",'y')
varPatientId = resp.split("patientId\":\"")[1].split("\"")[0]
print u'////////// patientId = ' + varPatientId


# # 6,会诊预约
# # scaled的值：A=2方，B=5方，C=10方，D=25方
# resp = response(u"6,会诊预约",'/v1/meetingSubscribe/addMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetTitle\":\"接口主题1\",\"meetDate\":\"2017-07-11\",\"startTime\":\"10:10\",\"endTime\":\"12:12\",\"managePwd\":\"123456\",\"canPwd\":\"111111\",\"description\":\"病情描述1\",\"purpose\":\"目的很明确\",\"remark\":\"备注有效\",\"inviteDoctorIds\":\""+varDoctorId+"\",\"patientId\":\""+varPatientId+"\",\"scale\":\"B\",\"sendDoctorIds\":\""+varDoctorId+"\"}",'y')


# 12,会诊列表
resp = response(u"12,会诊列表",'/v1/meetingAudit/meetList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"5\",\"pageNum\":\"1\"}",'y')
varMeetId = resp.split("meetId\":\"")[1].split("\"")[0]
print u'////////// meetId = ' + varMeetId
varPexipId = resp.split("pexipId\":\"")[1].split("\"")[0]
print u'////////// pexipId = ' + varPexipId
varMeetNo = resp.split("meetNo\":\"")[1].split("\"")[0]
print u'////////// meetNo = ' + varMeetNo

varMeetId = "69"
varPexipId = "251"
varMeetNo="989725"

# 16,启用会诊
resp = response(u"16,启用会诊",'/v1/meetingAudit/enterMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\"}",'y')


# 13,进入会诊
resp = response(u"13,进入会诊",'/v1/meetingAudit/enterMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\"}",'y')


# # 14,退出会诊
# resp = response(u"14,退出会诊",'/v1/meetingAudit/quitMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\"}",'y')


# # 15,结束会诊
# resp = response(u"15,结束会诊",'/v1/meetingAudit/closeMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\",\"pexipId\":\""+varPexipId+"\"}",'y')

# # 17,删除会诊(废弃）
# resp = response(u"17,删除会诊",'/v1/meetingAudit/deleteMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\",\"pexipId\":\""+varPexipId+"\"}",'y')


# 18,会诊审核列表
resp = response(u"18,会诊审核列表",'/v1/meetingAudit/meetList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"3\",\"pageNum\":\"1\"}",'y')

# # 19,同意会诊
# resp = response(u"19,同意会诊",'/v1/meetingAudit/agreeMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\",\"meetNo\":\""+varMeetNo+"\"}",'y')
#
# # 20,拒绝会诊
# resp = response(u"20,拒绝会诊",'/v1/meetingAudit/refuseMeet',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\",\"content\":\"john拒绝了你\",\"meetNo\":\""+varMeetNo+"\"}",'y')


# 21,会诊详情
resp = response(u"21,会诊详情",'/v1/meetingAudit/meetInfo',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\"}",'y')

# 22,患者档案
resp = response(u"22,患者档案",'/v1/meetingAudit/patientRecord',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"patientId\":\""+varPatientId+"\"}",'y')

# 23,成员添加会诊报告
resp = response(u"23,成员添加会诊报告",'/v1/meetingAudit/addMemberMeetReport',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\",\"conclusion\":\"会诊很成功\",\"evaluate\":\"满分\",\"starLevel\":\"5\",\"plan\":\"无解决方案\",\"remark\":\"备注信息\"}",'y')

# 24,添加会诊报告(只能添加一次）
resp = response(u"24,添加会诊报告",'/v1/meetingAudit/addMeetReport',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\",\"conclusion\":\"会诊很成功\",\"evaluate\":\"满分\",\"starLevel\":\"5\",\"plan\":\"无解决方案\",\"remark\":\"备注信息\"}",'y')


# 25,会诊报告列表
resp = response(u"25,会诊报告列表",'/v1/meetingAudit/meetReportList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"patientId\":\""+varPatientId+"\"}",'y')


# 26,会诊报告详情
resp = response(u"26,会诊报告详情",'/v1/meetingAudit/meetReportInfo',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"meetId\":\""+varMeetId+"\"}",'y')


# 查询直播列表
resp = response(u"查询直播列表",'/v1/Live/LiveList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\"}",'y')
varLessonMeetingId = resp.split("lessonMeetingId\":\"")[1].split("\"")[0]
print u'////////// lessonMeetingId = ' + varLessonMeetingId

# 直播创建群组
m1 = md5.new()
m1.update("createIMAccount_PHP")
myMd5_Digest = m1.hexdigest()
resp = response(u"直播创建青群组",'/v1/Live/liveAddGroupId',"{\"userId\":\"" + varUserId + "\",\"authToken\":\""+myMd5_Digest.upper()+"\",\"lessonMeetId\":\"" + varLessonMeetingId + "\"}",'y')

# 创建云通讯账号
m1 = md5.new()
m1.update("createIMAccount_PHP")
myMd5_Digest = m1.hexdigest()
resp = response(u"创建云通讯账号",'/v1/IM/createIMAccount',"{\"userId\":\"" + varUserId + "\",\"authToken\":\""+myMd5_Digest.upper()+"\"}",'y')









# print "？？？？？~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[注册]"
# url = 'http://10.111.3.6:8083/DCloudDoctor/v1/user/register'
# myMd5 = hashlib.md5()
# myMd5.update(varPass)
# myMd5_Digest = myMd5.hexdigest()
# varParam = "{\"identityType\":\"1\",\"phoneNumber\":\"" + varPhone + "\",\"passWord\":\"" + myMd5_Digest + "\",verificationCode\",\"" + str(redisCode) + "\",\"name\":\"john\"" + varPhone + "\",sex\":\"1\",\"hospitalId\":\"医院1\",\"hospitalName\":\"医院名称\",\"officeId\":\"科室id\"}"
# resp = response('Y')
# varUserId = resp.split("userId\":\"")[1].split("\"")[0]
# # print varUserId
# varUserSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
# # print varUserSessionId
# # varImVoip = resp.split("imVoip\":\"")[1].split("\"")[0]
#  #注册(医生助理）
# m1 = md5.new()
# m2 = md5.new()
# m2.update("645713")
# m1.update("{\"codeType\":\"register\",\"phoneNumber\":\"" + phoneNumber + "\"}" + "123456")
# # values = {"check":m1.hexdigest(),"json":{"identityType":"1","phoneNumber":"" + phoneNumber + "","passWord":m2.hexdigest(),"verificationCode":"??????","name":"johnjin","sex":"1","education":"博士","major":"药师","experience":"10","IDcardNum":"310101198004110014","invitationCode":"123456","hospitalId":"上海医院N10","hospitalName":"上海医院","officeId":"123","officeName":"血液科","title":"高级职称","titleId":"222","goodAt":"灵床","medicalBackground":"无","achievement":"wu","doctorCertificateList.url":"111","pharmacistCertificateList.url":"11111","IDcardList.url":"wu"}}
# # values = {"check":m1.hexdigest(),"json":{"identityType":"3","phoneNumber":"" + phoneNumber + "","passWord":m2.hexdigest(),"verificationCode":"264000","name":"johnjin","IDcardNum":"310101198004110014","invitationCode":"drQ6JN"}}
#
# values = {"check":m1.hexdigest(),"json":{"identityType":"2","phoneNumber":"" + phoneNumber + "","passWord":m2.hexdigest(),"verificationCode":"264000","name":"johnjin","education":"博士","major":"药师","experience":"10","pharmacistCertificateList.url":"11111","IDcardList.url":"http://111.jpg"}}



# # 找回密码或者更新密码
# # 更新密码,type = 1
# url = 'http://10.111.3.6:8083/DCloudDoctor/v1/user/findPassWord'
# myMd5.update("jinhao000")  # 新密码
# myMd5_Digest = myMd5.hexdigest()
# resp = response(u'更新密码','/v1/user/findPassWord',"{\"userId\":\"" + varUserId + "\",\"phoneNumber\":\"" + varPhone + "\",\"passWord\":\"" + myMd5_Digest + "\",\"verificationCode\":\"" + str(redisCode) + "\",\"type\":\"1\"}",'y')
#

# # 重新填写获取信息
# resp = response(u"[重新填写获取信息]",'/v1/user/againWrite',"{\"userId\":\"" + varUserId + "\"}",'y')


# # 提交重新填写信息 ???
# # 药师
# resp = response(u"[提交重新填写信息 - 药师]",'/v1/user/updateAgainUserInfo',"{\"userId\":\"" + varUserId + "\"}",'y')
#
# #医生助理
#
# #医生
# resp = response(u"[提交重新填写信息 - 医生]",'/v1/user/updateAgainUserInfo',"{\"userId\":\"" + varUserId + "\"}",'y')



# # 医生首页 , 注意orderNo 需要添加患者后才有数据。
# resp = response(u"[医生首页]",'/v1/user/doctorHome',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"1\",\"pageNum\":\"1\",\"serviceStatus\":\"1\"}",'y')
# varOrderNo = resp.split("orderNo\":\"")[1].split("\"")[0]
# print u'////////// varOrderNo = ' + str(varOrderNo)
#
# # 添加备注,  修改备注 ,可修改 病人姓名 与 备注说明
# # 依赖于varOrderNo
# resp = response(u"[添加备注]",'/v1/user/addRemark',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"orderNo\":\"" + varOrderNo + "\",\"patientName\":\"二货2\",\"remark\":\"病得不清哦！\"}",'y')
#
# # 完成服务，客户端上状态从 进行中 变为 待评价
# # 依赖于varOrderNo
# resp = response(u"[完成服务]",'/v1/user/finishService',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"orderNo\":\"" + varOrderNo + "\"}",'y')
#
# resp = response(u"[我的服务]",'/v1/user/myServiceHome',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\"}",'y')


# 开启我的服务设置 ,?????旧服务的服务id集合orservIdList
# resp = response(u"[开启我的服务设置]",'/v1/user/openService',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"servList.servId\":\"5\",\"servList.title\":\"33333\",\"servList.price\":\"1.34\",\"orservIdList\":\"" + ? + "\"}",'y')


# 暂时服务 ,  ????servList.servId 哪里获取
# resp = response(u"[暂时服务]",'/v1/user/updateService',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"servList.servId\":\"5\"}",'y')


# # 体验官评分页面列表 , 日期dateType
# # 1：全部(默认)
# # 2：最近一个月；
# # 3：最近三个月；
# # 4：最近一年；
# resp = response(u"[体验官评分页面列表]",'/v1/user/experienceScoreList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"type\":\"1\",\"dateType\":\"1\",\"pageSize\":\"1\",\"pageNum\":\"1\"}",'y')
#
# resp = response(u"[问题详情]",'/v1/user/questionDetail',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"orderNo\":\"" + varOrderNo + "\"}",'y')

# 医额宝？？
# resp = response(u"[医额宝]",'/v1/pay/doctorwalletHome',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\"}",'y')

resp = response(u"[收支明曦]",'/v1/pay/paymentsDetail',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"payType\":\"0\",\"pageSize\":\"1\",\"pageNum\":\"1\"}",'y')

resp = response(u"[体现清单列表]",'/v1/pay/depositDetailedList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"depositType\":\"0\",\"pageSize\":\"1\",\"pageNum\":\"1\"}",'y')

resp = response(u"[添加银行卡]",'/v1/pay/addBankCard',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"cardName\":\"马艳丽\",\"BankCardNo\":\"6225880214011035\"}",'y')

resp = response(u"[支持银行卡]",'/v1/pay/supportBank',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\"}",'y')

resp = response(u"[银行卡列表]",'/v1/pay/bankCardList',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\"}",'y')


sleep(1212)



# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[查询省市级地区列表]"
# url = 'http://10.111.3.6:8083/DCloudDoctor/v1/system/regionList'
# myMd5 = hashlib.md5()
# myMd5.update(varPass)
# myMd5_Digest = myMd5.hexdigest()
# varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\"}"
# resp = response('Y')



# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 首页]"
# url = 'http://43.254.24.107:8080/dangjian/v1/home/homePage'
# varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')
#
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - IM推送]"
# url = 'http://43.254.24.107:8080/dangjian/v1/group/IMPush'
# varParam = "{\"imVoip\":\"" + varImVoip + "\",\"msgContent\":\"" + varSessionId + "\"}"
# response('Y')

# sleep(1212)
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 修改密码]"
# url = 'http://43.254.24.107:8080/dangjian/v1/user/modifyPassWord'
# myMd5 = hashlib.md5()
# myMd5.update("jinhao111")
# myMd5_new = myMd5.hexdigest()
# print myMd5_new
# varParam = "{\"oldPassWord\":\"" + myMd5_Digest + "\",\"newPassWord\":\"" + myMd5_new + "\",\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')

# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 退出登录]"
# url = 'http://43.254.24.107:8080/dangjian/v1/user/loginOut'
# varParam = "{\"userSessionId\":\"" + varSessionId + "\",\"userId\":\"" + varUserId + "\"}"
# response('Y')



# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 随时学-学习历史记录列表]"
# url = 'http://43.254.24.107:8080/dangjian/v1/anyMomentStudy/historyList'
# varParam = "{\"userId\":\"" + varUserId + "\",\"flag\":\"0\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
# response()
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 随时学]"
# url = 'http://43.254.24.107:8080/dangjian/v1/anyMomentStudy/homePage'
# varParam = "{\"userId\":\"" + varUserId + "\",\"flag\":\"0\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')
#
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 猜你喜欢换一组]"
# url = 'http://43.254.24.107:8080/dangjian/v1/anyMomentStudy/otherLike'
# varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
# response()
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 消息盒子-通知]"
# url = 'http://43.254.24.107:8080/dangjian/v1/sysMessage/noticeList'
# varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')

# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 消息盒子-提醒]"
# url = 'http://43.254.24.107:8080/dangjian/v1/sysMessage/remindList'
# varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[???党建 - 消息盒子-未读消息数]"
# url = 'http://43.254.24.107:8080/dangjian/v1/sysMessage/readMsgCount'
# varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')
#
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 学习计划列表]"
# url = 'http://43.254.24.107:8080/dangjian/v1/learn/getLearnPlan'
# varParam = "{\"userId\":\"" + varUserId + "\",\"companyType\":\"1\",\"planType\":\"1\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 学习项目排行榜]"
# url = 'http://43.254.24.107:8080/dangjian/v1/learn/getProjectRanking'
# varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')
#
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 音频列表]"
# url = 'http://43.254.24.107:8080/dangjian/v1/source/audioList'
# varParam = "{\"userId\":\"" + varUserId + "\",\"typeId\":\"0\",\"pageNum\":\"1\",\"pageSize\":\"1\",\"userSessionId\":\"" + varSessionId + "\"}"
# response()
#
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 我的讨论小组]"
# url = 'http://43.254.24.107:8080/dangjian/v1/group/getGroupList'
# varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"10\",\"userSessionId\":\"" + varSessionId + "\"}"
# response('Y')


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 个人信息]"
# url = 'http://43.254.24.107:8080/dangjian/v1/user/modifyUserInfo'
# varParam = "{\"content\":\"test\",\"type\":\"1\",\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
# response()
#
#
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 上传图片]"
# url = 'http://43.254.24.107:8080/dangjian/v1/user/modifyUserImage'
# f = open(r'//Users//linghuchong//Downloads//51//Picture//flying.jpg','rb') #二进制方式打开图文件
# ls_f = base64.b64encode(f.read())
# f.close()
# varParam = "{\"imageFile\":\""+ls_f+"\",\"type\":\"4\",\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
# response()










# # 党建 —— 上传图片
# f=open(r'//Users//linghuchong//Downloads//51//Picture//flying.jpg','rb') #二进制方式打开图文件
# ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
# f.close()
# src = "{\"imageFile\":\""+ls_f+"\",\"type\":\"4\",\"userId\":\"82\",\"userSessionId\":\"" + varSessionId + "\"}" + "123456"
# m1 = md5.new()
# m1.update(src)
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``"
# # print m1.hexdigest()
# # {"check":"45fe6ea0b03bb943d6a0cab9ae6c9272","json":{"codeType":"register","phoneNumber":"15601822035"}}
# def http_post():
#     url = 'http://43.254.24.107:8080/dangjian/v1/user/modifyUserImage'
#     # url = 'http://10.111.3.5:8082/v1/user/login'
#     # values = {"check":m1.hexdigest(),"json":{"type":"4","imageFile":{"data":"image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAApAHgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAoopD0oAM0ZqC5E3lnydu73rHt9VvRq6Wc4i2n+71qrXQXN7IxnNLkVGWxnpisC/wDEQhuRDAu8g4Y9vwpRgyeY6PIxnNGRWHq2rTWH2fYilZBk5HSrlpqEd5beahBYDkelPle4cxo5FJkVzEWvXT2d3I6x74SAu3p1rX027ku7GOZ9u5uuKOVhzGhmjNYn9pynX/sYX92O9bC53HOMdqTVgTJKKSikULRRRQAUh6UtIeRQAzcOlcycDxeMjnt+VXrma8tNRMgjMlu/ZRkiotMsZri+bUbobZD91B2+taLQhpjNX1FpLv8As+F/KJ++7cflWXqkVrbi1jglV2B5YHk/WuslsrZ3MskKs57kVh69p2Jbb7LbLgn5sLVQkkyXEg8Qskq2YVyQRjIPFFoTpF+1vjbBIvDt9Ksa1ZOUs47eLO3rgdK0tS0/7bp3lgDzAo2k9qfMrJCsY2gQpIL4FQwfselP0Wf7GbqGeTZt+6rnGPpUvhq1nt2n8+NlzjGRxUPiDS2kvEmhDs0h+bHQU2020NIl8Oo8s9xdTKW3H5WNdIByKr2NutrapCvQCrIrGbuacthaKWioQwooopgFIelLQaAImVsgDG3vSKrA5br7VLRQAnXnFIRmnUUAMwTwByPWl+6OlPooFYi2nPGcilCZycdeoqSigLEY+h5p+OaWihjA0UGigD//2Q=="},"userId":"82","userSessionId":"" + x + "" }}
#     values = {"check":m1.hexdigest(),"json":{"type":"4","imageFile":"" + ls_f + "","userId":"82","userSessionId":"" + x + "" }}
#
#     jdata = json.dumps(values)  # 对数据进行JSON格式化编码
#     req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
#     response = urllib2.urlopen(req)  # 发送页面请求
#     return response.read()  # 获取服务器返回的页面信息
# resp = http_post()
# print resp

