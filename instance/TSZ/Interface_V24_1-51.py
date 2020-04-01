# coding: utf-8
#****************************************************************
# Author     : John
# Version    : V 24.0
# Date       : 2016-6-19
# Description: 三藏红包 app接口文档
# I24_1 ~ I24_15 ,47-51 from John
# I24_16 ~ I24_30 from 冼丽琼
# I24_31 ~ I24_45 from 宋涛
#****************************************************************

import sys,requests,redis,MySQLdb,random,datetime,time
import smtplib,pytesseract
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep

# 当前时间字符串 , 20160623183734,20160628,2016-06-28 00:00:01
varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S');
varTimeYMD = datetime.datetime.now().strftime('%Y%m%d');
varTimeY_M_D = datetime.datetime.now().strftime('%Y-%m-%d');
varTimeFrom = varTimeY_M_D +" 00:00:01"
varTimeEnd = varTimeY_M_D+" 23:59:59"

# 随即生成4位数
def myfunc(n):
    ret = []
    for i in range(n):
        while 1:
            number = random.randrange(0,10)
            if number not in ret:
                ret.append(str(number))
                break
    return ret
varRandom4="".join(myfunc(4))

# 1,更多红包群接口(update)
# 2,红包群首页_我关注的红包群列表接口(新增参数)
# 3,红包群标签_添加红包群标签接口
# 4,红包群标签_修改红包群标签名称接口
# 5,红包群标签_修改红包群标签成员接口
# 6,红包群标签_删除红包群标签接口
# 7,红包群标签_获取单个红包群标签接口
# 8,红包群标签_获取红包群所有标签接口
# 9,红包群成员_添加红包群成员接口
# 10,红包群成员_修改红包群成员备注接口
# 11,红包群成员_加入或移除群成员黑名单接口
# 12,红包群成员_修改单个群成员标签接口
# 13,红包群黑名单用户列表接口（新增参数，修改返回值）
# 14,红包群成员_删除群成员接口
# 15,红包群成员_获取所有群成员接口
# 16,红包群成员_获取群标签所有成员接口
# 17,红包群成员_获取单个群成员在该群的所有标签接口
# 18,红包群成员_修改群备注接口
# 19,红包群成员_获取所有新成员列表接口
# 20,红包群查看分享奖励列表接口(新增返回值)
# 21,红包群消息_保存消息接口
# 22,红包群消息_群主删除消息接口
# 23,红包群消息_群主撤回消息接口
# 24,红包群消息_群成员举报消息接口
# 25,红包群消息_我的红包群消息列表接口
# 26,红包群消息_我的红包群消息查看确认接口
# 27,红包群消息_我关注的红包群消息列表接口
# 28,红包群消息_我关注的红包群消息查看确认接口
# 29,账户微信充值接口
# 30,账户微信充值回调接口
# 31,渠道推广红包个分享渠道记录接口(新增参数)
# 32,获得红包群分类列表接口
# 33,红包群设置店铺链接接口
# 34,红包群分类设置接口
# 35,获取分享内容及分享链接接口(新增参数)
# 36,用户发的红包广告统计信息接口(新增返回值)
# 37,红包群成员_群成员排序分类
# 38,红包群通讯录_获取我关注的红包群群主列表接口
# 39,红包群首页_我的红包群信息接口(新增返回值)
# 40,用户个人主页信息接口(新增返回值)
# 41,红包群红点_群新成员红点接口
# 42,我关注的红包群分类接口
# 43,红包群抢红包_抢红包回调接口
# 44,更新进入店铺链接打开数接口
# 45,红包群查看分享奖励条数接口
# 46,发红包消息规则说明接口
# 47,红包群标签_获取红包群标签(指定标签ID)接口
# 48,用户发的红包广告红包详情接口
# 49,用户发的红包广告红包详情接口（新增参数和返回值）
# 50,红包群_加入红包群接口（新增返回值）
# 51,红包群抢红包_领取红包消息(点击领取红包炸弹时调用)
# 52,红包群红点_我的红包群私信红点接口

def Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,**query):
     r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
     varverifyCode = r.hget("app:verify:"+varuserId,"code")
     query1={}
     query1["verifyUserId"]= varuserId
     query1["verifyCode"]=varverifyCode
     for x in query:
        query1[x] =  str(query[x])
     headers = {'cache-control': "no-cache"}
     response = requests.request("GET", varUrl, headers=headers, params=query1)
     try:
        if varnum=="RtnNullOK" :  #如:{"data":null,"errorstr":"","errorcode":0,"success":true}
            if response.json()['success']==True:print "[OK,RtnNullOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
               print "[errorrrrrrrrrr,RtnNullOK]," + varInterfaceName + " => " + testcase + " => " + response.content
               sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
        if varnum=="RtnOK" : #如:{"data":149,"errorstr":"","errorcode":0,"success":true}
            if response.json()['success']==True and len(str(response.json()['data']))>0:print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnNoDATAOK" : # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
            if response.json()['success'] == True and response.json()['data'] == []:print "[OK,RtnNoDATAOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:print "[errorrrrrrrrrr,RtnNoDATAOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else: print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnDeviceErr" :
            if response.json()['errorcode']==100003 and response.json()['success']== False:print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
     except Exception,data:
        print Exception,":",data,"\n"
def sendemail(varTitle,varContent):
    # 邮箱配置
    sender = '<jinhao@mo-win.com.cn>'
    receiver = 'jinhao@mo-win.com.cn'
    msg = MIMEText(varContent,'text','utf-8')
    msg['Subject'] = varTitle  # u'三藏红包gameTAble'
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com')
        smtp.login('jinhao@mo-win.com.cn','Jinhao123')
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(e)
# [main]****************************************************************
# self.driver.switch_to.context("WEBVIEW")
# self.driver.switch_to_default_content()

print  "\n====================== 2.4版本_APP接口测试 ======================"
def I24_1(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    varInterfaceName =  "I24_1,更多红包群接口(update)"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.2/all_redGroup.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,likeName=param2,industryId=param3)
def I24_2(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    # 参数: userId = 用户ID, likeName = 搜索名称(可选), industryId = 分类(可选),startIndex=分页开始位置,pageSize =每页显示条数
    varInterfaceName =  "I24_2,红包群首页_我关注的红包群列表接口(新增参数)"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.2/my_redGroup_info.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,likeName=param2,industryId=param3,startIndex=param4,pageSize=param5)
def I24_3(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId = 用户ID, groupId = 群ID, labelName = 标签名称 ,memberIds = 标签成员ID(多个逗号,分隔)
    varInterfaceName =  "I24_3,红包群标签_添加红包群标签接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/add_group_label.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,labelName=param3,memberIds=param4)
def I24_4(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: userId = 用户ID, groupId = 群ID, labelName = 标签名称 ,memberIds = 标签成员ID(多个逗号,分隔)
    varInterfaceName =  "I24_4,红包群标签_修改红包群标签名称接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/update_group_label.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,id=param1,groupId=param2,labelName=param3)
def I24_5(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, groupId = 群ID, labelName = 标签名称 ,memberIds = 标签成员ID(多个逗号,分隔)
    ########################################################################
    varInterfaceName =  "I24_5,红包群标签_修改红包群标签成员接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/update_group_label_member.do"
    if param3=="":
        querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"labelId":param1,"groupId":param2,"delUserId":param4}
    elif param4=="":
        querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"labelId":param1,"groupId":param2,"newUserId":param3}
    else:
        querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"labelId":param1,"groupId":param2,"newUserId":param3,"delUserId":param4}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']==True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnDeviceErr" :
            if response.json()['errorcode']==100003 and response.json()['success']== False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_6(varnum,varuserId,param1,param2,testcase):
    # 参数: id = 标签ID, groupId = 群ID,
    varInterfaceName =  "I24_6,红包群标签_删除红包群标签接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/del_group_label.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,id=param1,groupId=param2)
def I24_7(varnum,varuserId,param1,testcase):
    # 参数: id = 标签ID
    varInterfaceName =  "I24_7,红包群标签_获取单个红包群标签接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/get_group_label.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,id=param1)
def I24_8(varnum,varuserId,param1,testcase):
    # 参数: groupId = 群ID,
    varInterfaceName =  "I24_8,红包群标签_获取红包群所有标签接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/getAll_group_label.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,groupId=param1)
def I24_9(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId =  用户ID, groupId = 群ID,groupUserId = 群主用户ID , groupLabel=用户标签(可选)
    ########################################################################
    varInterfaceName =  "I24_9,红包群成员_添加红包群成员接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/add_redGroup_member.do"
    if param4=="":
        querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"groupUserId":param3}
    else:
        querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"groupUserId":param3,"groupLabel":param4}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']==True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_10(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: userId =  用户ID, groupId = 群ID,remarks = 用户昵称
    varInterfaceName =  "I24_10,红包群成员_修改红包群成员备注接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/update_redGroup_member.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,remarks=param3)
def I24_11(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: userId =  用户ID, groupId = 群ID,isBlack = 是否为黑名单成员(0:不是，1:是)
    varInterfaceName =  "I24_11,红包群成员_加入或移除群成员黑名单接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/add_black.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,isBlack=param3)
def I24_12(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId =  用户ID, groupId = 群ID, oldGroupLabel = 群成员老标签 ,groupLabel=群成员新标签
    varInterfaceName =  "I24_12,红包群成员_修改单个群成员标签接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/update_redGroup_memberLabel.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,oldGroupLabel=param3,groupLabel=param4)
def I24_13(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: userId =  用户ID, groupId = 群ID, nickname = 搜索名称
    varInterfaceName =  "I24_13,红包群黑名单用户列表接口（新增参数，修改返回值）"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.4/redGroup_black_userInfo_list.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,nickname=param3)
def I24_14(varnum,varuserId,param1,param2,testcase):
    # 参数: userId =  用户ID, groupId = 群ID
    varInterfaceName =  "I24_14,红包群成员_删除群成员接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/del_redGroup_member.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2)
def I24_15(varnum,varuserId,param1,param2,tblNum,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: groupId = 群ID , sortId = 排序ID(0:默认排序)
    ########################################################################
    varInterfaceName =  "I24_15,红包群成员_获取所有群成员接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/get_all_redGroup_member.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"groupId":param1,"sortId":param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']==True and len(response.json()['data'])==tblNum:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                sendemail("I24_15,红包群成员_获取所有群成员接口","[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_16(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: groupId = 群ID, groupLabel = 群标签ID
    ########################################################################
    varInterfaceName =  "I24_16,红包群成员_获取群标签所有成员接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/get_groupLabel_member.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "groupId": param1, "groupLabel": param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success'] == True and response.json()['data'] <> None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_17(varnum, varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID
    ########################################################################
    varInterfaceName = "I24_17,红包群成员_获取单个群成员在该群的所有标签接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/update_groupMember_allLabel.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "groupId": param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_18(varnum, varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, groupRemark = 群呢称
    ########################################################################
    varInterfaceName = "I24_18,红包群成员_修改群备注接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/update_group_remark.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "groupId": param2,
                   "groupRemark": param3}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_19(varnum, varuserId, param1, param2, param3, param4, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, startIndex=分页开始位置,pageSize =每页显示条数
    ########################################################################
    varInterfaceName = "I24_19,红包群成员_获取所有新成员列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/get_newUser_info.do"
    if param3 == "":
        querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                       "groupId": param2, "pageSize": param4}
    else:
        querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                       "groupId": param2, "startIndex": param3, "pageSize": param4}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    data = response.json()
    data1= data['data']
    try:
        if varnum == "RtnOK" :
            if response.json()['success'] == True and data1.has_key('count')==True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                return data1['count']
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_20(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, groupUserId = 群主用户ID
    ########################################################################
    varInterfaceName = "I24_20,红包群查看分享奖励列表接口(新增返回值)"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupRobRed/2.4/redGroup_shareAward_list.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "groupId": param2,
                   "groupUserId": param3}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    data = response.json()['data']
    if response.json()['data']<> None:
        for i in data.get('dataList'):
            global ExistAmount,varAmount
            if data.has_key('dataList')==[]:
                ExistAmount=False
            else:
                varAmount=i.get('amount')
                ExistAmount=True
    else:
        ExistAmount=False

    try:
        if varnum == "RtnOK" :
            if response.json()['success'] == True and ExistAmount==True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                return varAmount
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_21(varnum, varuserId, param1, param2, param3, param4, param5, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, groupMessage = 消息内容, labelId = 标签id(全部为0,多个以逗号,分隔),
    #  messageType = 消息类型(0文字消息,1红包炸弹消息,2分享消息,3抢到红包消息,4分享奖励消息,5红包抢完消息,6第一次加入消息,7图片消息)
    ########################################################################
    varInterfaceName = "I24_20,红包群消息_保存消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/save_redGroup_message.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "groupId": param2,
                   "groupMessage": param3,
                   "labelId":param4,
                   "messageType":param5
                   }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_22(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, messageId = 消息ID
    ########################################################################
    varInterfaceName = "I24_22,红包群消息_群主删除消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/del_redGroup_message.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "groupId": param2,
                   "messageId": param3
                   }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_23(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, messageId = 消息ID
    ########################################################################
    varInterfaceName = "I24_23,红包群消息_群主撤回消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/revoke_redGroup_message.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode,
                   "userId": param1,
                   "groupId": param2,
                   "messageId": param3
                   }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_24(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,
                          password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, messageId = 消息ID
    ########################################################################
    varInterfaceName = "I24_24,红包群消息_群成员举报消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/report_redGroup_message.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode,
                   "userId": param1,
                   "groupId": param2,
                   "messageId": param3
                   }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_25(varnum, varuserId, param1, param2, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,
                          password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID
    ########################################################################
    varInterfaceName = "I24_25,红包群消息_我的红包群消息列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/my_redGroupMessages_info.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode,
                   "userId": param1, "groupId": param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers,
                                params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_26(varnum, varuserId, param1, param2, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,
                          password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: updateTime = 最近一条消息时间, groupId = 群ID
    ########################################################################
    varInterfaceName = "I24_26,红包群消息_我的红包群消息查看确认接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/get_myMessage_callback.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode,
                   "updateTime": param1, "groupId": param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers,
                                params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_27(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,
                          password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, groupUserId = 群主用户ID
    ########################################################################
    varInterfaceName = "I24_27,红包群消息_我关注的红包群消息列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/my_publicityRedGroupMessages_info.do"
    querystring = {"verifyUserId": varuserId,
                   "verifyCode": varverifyCode,
                   "userId": param1, "groupId": param2, "groupUserId": param3}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers,
                                params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and \
                            response.json()[
                                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and \
                            response.json()[
                                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_28(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,
                          password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: updateTime = 最近一条消息时间, groupId = 群ID, userId = 用户ID
    ########################################################################
    varInterfaceName = "I24_28,红包群消息_我关注的红包群消息查看确认接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMessage/2.4/get_myPublicityMessage_callback.do"
    querystring = {"verifyUserId": varuserId,
                   "verifyCode": varverifyCode,
                   "updateTime": param1, "groupId": param2, "userId": param3}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers,
                                params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and \
                            response.json()[
                                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and \
                            response.json()[
                                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_29(varnum, varuserId, param1, param2, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 群ID, amount = 充值金额（元）
    ########################################################################
    varInterfaceName = "I24_29,账户微信充值接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/accountPreOrder.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "amount": param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    data1 = response.json()['data']
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True and response.json()['data'] <> None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                return str(data1['orderId'])
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        # if varnum == "RtnParamErr1":
        #     if response.json()['errorcode'] == 1 and response.json()['success'] == False:
        #         print "[OK,RtnParamErr1]," + varInterfaceName + " => " + testcase + " => " + response.content
        #     else:
        #         print "[errorrrrrrrrrr,RtnParamErr1]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_30(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, amount = 交易金额 ,payOrderId =交易订单号
    ########################################################################
    varInterfaceName = "I24_30,账户微信充值回调接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/accountOrderReturn.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                       "amount": param2, "payOrderId": param3}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True : # and response.json()['data'] == "您取消了支付！"
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_31(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: redPoolId = 红包池id, userId = 用户ID, uninAmount = 单位金额,payType=支付类型,channel =渠道类型,
    # brandContent =品牌,lvl =层级,count =红包数量,labelIds =红包群选择分类(新增),
    ########################################################################
    varInterfaceName =  "I24_31,渠道推广红包个分享渠道记录接口(新增参数)"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/channelShare.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"redPoolId":param1,"userId":param2,"uninAmount":param3
        ,"payType":param4,"channel":param5,"brandContent":param6,"lvl":param7,"count":param8,"labelIds":param9}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success'] == True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "设置数量不正确":
            if response.json()['errorcode'] == 1 and response.json()['success'] == False:
                print "[OK,设置数量不正确]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                 print "[errorrrrrrrrrr,设置数量不正确]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_32(varnum,varuserId,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
        # 参数: 该接口可不入传入参数
        ########################################################################
    varInterfaceName =  "I24_32,获得红包群分类列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.4/getRedGroupIndustrylist.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_33(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, groupId = 群ID, shopLink = 店铺链接
    #业务逻辑
    #userId必须与群id对应，只有自己才可以修改自己的群店铺链接（t_redgroup_baseinfo）
    ########################################################################
    varInterfaceName =  "I24_33,红包群设置店铺链接接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.4/saveShopLink.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"shopLink":param3
        }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_34(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, groupId = 群ID，industry=分类ID
    #业务逻辑
    #userId必须与群id对应，自己给自己的群分类（t_redgroup_baseinfo）,
    ########################################################################
    varInterfaceName =  "I24_34 ,红包群分类设置接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.4/saveRedGroupIndustry.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"industry":param3
        }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_35(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,param12,param13,param14,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, shareType = 类型, platform = 分享渠道，amount = 红包总金额, tranId = 红包池id,
    # count = 红包数量,uninAmount=单个红包金额,payType =支付类型,channel=渠道类型,lvl =层级，brandContent =品牌名称,
    # context=推广内容,labelIds =红包群选择分类(新增)，name=品牌名称（如果是微薄就必填，其他渠道选填）
    ########################################################################
    varInterfaceName =  "I24_35,获取分享内容及分享链接接口(新增参数)"
    varUrl = "http://192.168.2.176:9999/payment/share/1.0/get_share_url.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"shareType":param2,"platform":param3
        , "amount": param4,"tranId":param5,"count":param6,"uninAmount":param7,"payType":param8,"channel":param9
        , "lvl": param10,"brandContent":param11,"context":param12,"labelIds":param13,"name":param14}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==1 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_36(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, groupId = 群ID（实际没有这个参数）, startIndex = 分页开始位置，pageSize = 每页显示条数
    varInterfaceName =  "I24_36,用户发的红包广告统计信息接口(新增返回值)"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupSta/2.2/user_redAdvert_statistics.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,
                   "startIndex":param3,"pageSize": param4}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_37(varnum,varuserId,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: 这个接口只是个分类，什么都不用传，测的意义不大
    varInterfaceName =  "I24_37,红包群成员_群成员排序分类"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/get_group_member_category.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_38(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, likeName = 搜索名称
    varInterfaceName =  "I24_38,获取我关注的红包群群主列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupAddressList/2.4/get_my_allGroupMain.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"likeName":param2}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()["data"]<>None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_39(varnum,varuserId,param1,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID
    varInterfaceName =  "I24_39,我的红包群信息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.2/redGroup_baseInfo.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_40(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 登录人用户ID，visitUserId=查看人用户ID，isGroup=是否群主1群主/0非群主
    varInterfaceName =  "I24_40,我的红包群信息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personalHomePage/2.2/homePage_info.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"visitUserId":param2,"isGroup":param3}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_41(varnum,varuserId,param1,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 登录人用户ID
    varInterfaceName =  "I24_41,群新成员红点接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupSta/2.4/get_newMember_redDot.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_42(varnum,varuserId,param1,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 登录人用户ID
    varInterfaceName =  "I24_42,我关注的红包群分类接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.4/getMyGroupIndustrylist.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_43(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 登录人用户ID,channelId=渠道ID,batchId=批次ID,groupId=群Id
    varInterfaceName =  "I24_43,抢红包回调接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupRobRed/2.4/redGroup_robRed_callback.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"channelId":param2,"batchId":param3,"groupId":param4}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "DonGrab":
            if response.json()['errorcode'] == 0 and response.json()['success'] != False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_44(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID,batchId=批次ID,channel=渠道类型
    varInterfaceName =  "I24_44,更新进入店铺链接打开数接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.4/update_red_link_open_count.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"channel":param2,"batchId":param3}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_45(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID,groupId=群ID,groupUserId=群主用户ID
    varInterfaceName =  "I24_45,红包群查看分享奖励条数接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupRobRed/2.4/redGroup_shareAward_count.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"groupUserId":param3}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"

def I24_46(varnum,varuserId,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    varInterfaceName =  "I24_46,发红包消息规则说明接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/h5Coupon/2.4/get_red_message_desc.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_47(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: groupId=群ID,labels=标签ID(多个以逗号分隔)
    varInterfaceName =  "I24_47 红包群标签_获取红包群标签(指定标签ID)接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupLabel/2.4/get_group_labels.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"groupId":param1,"labels":param2}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <>None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_48(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: batchId=批次ID ,startIndex= , pageSize=翻页标签
    varInterfaceName =  "I24_48 用户发的红包广告红包详情接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupSta/2.2/user_redAdvert_page.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"batchId":param1,"startIndex":param2,"pageSize":param3}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <>None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_49(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,channelId,startIndex,pageSize
    varInterfaceName =  "I24_49 用户发的红包广告红包详情接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupRobRed/2.2/redGroup_robLuck.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"channelId":param2,"startIndex":param3,"pageSize":param4}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <>None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_50(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId , groupUserId
    varInterfaceName =  "I24_50 红包群_加入红包群接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.2/add_user_redGroup.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"groupUserId":param3}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <>None:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_51(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId , batchid, channelid
    varInterfaceName =  "I24_51 红包群抢红包_领取红包消息(点击领取红包炸弹时调用)接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupRobRed/2.4/redGroup_robRed_receive.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"batchId":param3,"channelId":param4}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True :
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I24_52(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId
    varInterfaceName =  "I24_52 红包群红点_我的红包群私信红点接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupSta/2.4/get_userChat_redDot.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True :
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnOKNone" :
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOKNone]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"

def Icommon1(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    # source（payType） = 推广来源 （1微信充值，2支付宝充值，3余额充值）
    # redSumAmount(amount) = 红包总金额
    # id（t_extension_channel_redPic）(picIds)＝渠道推广图片ID
    # brandContent ＝ 品牌商户名称
    # redNumber(count) ＝ 红包总数量
    # door =   1首页进入 2红包再发一次
    ########################################################################
    varInterfaceName =  "Icommon1,塞钱进红包支付接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeGetOrderNew.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"payType":param1,"amount":param2,"picIds":param3
        ,"userId":param4,"brandContent":param5,"count":param6,"door":param7}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def Icommon2(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    #userId=用户ID(必填)
    #redPoolId=t_extension_channel_redPool的红包id(必填)
    #uninAmount=红包金额(必填)
    #payType（source）=支付类型(必填)
    #channel=渠道类型(必填)
    #labelIds=群分组，传空也可以默认是0代表全部（必填）
    #brandContent=品牌名
    #lvl=层级
    #count=红包当前数量
    #channelId=渠道ID
    ########################################################################
    varInterfaceName =  "Icommon2,抢红包接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/channelShare.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"redPoolId":param2,"uninAmount":param3,"payType":param4
        ,"channel":param5,"labelIds":param6,"brandContent":param7,"lvl":param8,"count":param9,"channelId":param10}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"


"====================== 2.4版本_APP接口测试用例 ======================"

# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('select userId from t_redgroup_memberinfo where groupId=213 order by userId desc')
# data3 = curT.fetchall()
# for each in data3[0]:
#     testId=int(each)+1
# print "  => [测试数据userId => " + str(testId)
# # 删除前先新增一个群成员 from I24_9 ,需确保此群成员userID不在 t_redgroup_memberinfo 表中.
# # I24_9业务逻辑: 分别在t_redgroup_user_label 和 t_redgroup_memberinfo 中新增1条记录.
# for i in range(0,5):
#     I24_9("RtnOK","10001679",testId,"213","10001679","500","C9-1,用户ID,群ID,群主用户ID,用户标签")
#     testId=testId+1
#

# print "1,================================================================================================="
# 1 更多红包群接口(update)
I24_1("RtnOK","10001679","10001679","","","C1-1,用户ID,搜索名称(空),分类(空)")
I24_1("RtnOK","10001755","10001755","138****1118","","C1-2,用户ID,搜索名称,分类(空)")
# I24_1("RtnParamErr","10001755","","","","C1-3,用户ID(空),搜索名称(空),分类(空)")

print "2,================================================================================================="
# # 2 红包群首页_我关注的红包群列表接口(新增参数)
I24_2("RtnOK","10001755","10001755","13","","0","0","C2-1,用户ID,搜索名称(空),分类(空),分页开始位置,每页显示条数")
I24_2("RtnParamErr","10001755","","","","0","0","C2-2,用户ID(空),搜索名称(空),分类(空),分页开始位置,每页显示条数")
I24_2("RtnSysErr","10001755","10001755","","","","","C2-3,用户ID,搜索名称(空),分类(空),分页开始位置(空),每页显示条数(空)")
I24_2("RtnSysErr","10001755","10001755","","","0","","C2-4,用户ID,搜索名称(空),分类(空),分页开始位置,每页显示条数(空)")
I24_2("RtnOK","10001755","10001755","","","","0","C2-5,用户ID,搜索名称(空),分类(空),分页开始位置(空),每页显示条数") # 如分页开始位置(空),则默认时0

print "3,================================================================================================="
# 3 红包群标签_添加红包群标签接口
# 涉及3张表,t_redgroup_memberinfo , t_redgroup_label , t_redgroup_user_label
# 业务逻辑: 先获取10001679的所有群成员, select * from t_redgroup_memberinfo where  groupUserId=10001679 ,然后指定一个或多个成员ID,如10001497,设置标签
# 其次在 t_redgroup_label 表中生成一条 labelName记录(获取id=129) , 最后 t_redgroup_user_label 表生成一条记录,labelId = 129
# 自动化处理逻辑: 获取 t_redgroup_memberinfo 表中符合条件的群成员 , 条件是groupId=213
# 获取10001679 所有群成员userId , 用于稍后的使用 ; 自动生成一串labelName3字符用于labelname(实际业务中标签不能重复)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
a_list=[]
curT.execute('select userId from t_redgroup_memberinfo where groupUserId="10001679" ')
data9 = curT.fetchall()
for i in range(len(data9)):
    for each in data9[i]:
       a_list.append(str(each))
# print  "[info] memberIds = " + str(a_list)
TestUserId3_1 = ''.join(a_list[0:1])   # 列表转字符串,获取第1个userId
TestUserId3_2 = ''.join(a_list[1:2])   # 列表转字符串,获取第2个userId
TestUserId3_3 = ''.join(a_list[2:3])   # 列表转字符串,获取第2个userId
TestUserId3_23=TestUserId3_2 + "," + TestUserId3_3
labelName3 = "jinhao"+str(varTimeYMDHSM)

I24_3("RtnOK","10001679","10001679","213",labelName3,TestUserId3_1,"C3-1,用户ID,群ID,标签名称,标签成员ID(1个)")

# C3-1,检查数据库 t_redgroup_label 表 新增1条且标签人数=1,
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id),id,labelName from t_redgroup_label where groupId=213 and labelName="%s" and userNumber=1' % (labelName3))
data9 = curT.fetchone()
if data9[0]==1:print "  => [Ok,t_redgroup_label数据库记录新增1条成功,I24_3-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_label数据库记录新增1条失败,I24_3-1]"

# C3-1,检查数据库 t_redgroup_user_label新增1条,且labelId = ID(t_redgroup_label)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId=%s' %(data9[1]))
data8 = curT.fetchone()
if data8[0]==1:print "  => [Ok,t_redgroup_user_label数据库记录新增1条成功,I24_3-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录新增1条失败,I24_3-1]"
curT.close(),conn.close()

labelName3_23 = "jinhao"+str(varTimeYMDHSM)+"j"
I24_3("RtnOK","10001679","10001679","213",labelName3_23,TestUserId3_23,"C3-2,用户ID,群ID,标签名称,标签成员ID(2个)")

# C3-2,检查数据库t_redgroup_label新增1条且标签人数=2,t_redgroup_user_label新增2条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id),id from t_redgroup_label where groupId=213 and labelName="%s" and userNumber=2' % (labelName3_23))
data7 = curT.fetchone()
if data7[0]==1:print "  => [Ok,t_redgroup_label数据库记录新增1条成功,I24_3-2]"
else:print "  => [errorrrrrrrrrr,t_redgroup_label数据库记录新增1条失败,I24_3-2]"
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId=%s' %(data7[1]))
data7 = curT.fetchone()
if data7[0]==2:print "  => [Ok,t_redgroup_user_label数据库记录新增1条成功,I24_3-2]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录新增1条失败,I24_3-2]"
curT.close(),conn.close()

I24_3("RtnSysErr","10001679","10001679","213","test","100014721212","C3-3,用户ID,群ID,标签名称,标签成员ID(错)")
I24_3("RtnParamErr","10001679","","213","test","10001684","C3-4,用户ID(空),群ID,标签名称,标签成员ID(1个)")
I24_3("RtnParamErr","10001679","10001679","21312","test1","10001684","C3-5,用户ID,群ID(错),标签名称,标签成员ID(1个)")

print "4,================================================================================================="
# 4 红包群标签_修改红包群标签名称接口
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213 and labelName="%s"' %(labelName3))
data1 = curT.fetchone()
# print "[info] id = " + str(data1[0])
I24_4("RtnOK","10001679",data1[0],"213","jinhaoRevised","C4-1,标签ID,群ID,标签名称(改)")
sleep(2)
# C4-1,检查数据库修改记录
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_label where groupId=213 and labelName="jinhaoRevised"')
data1 = curT.fetchone()
if data1[0]==1:print "  => [Ok,t_redgroup_label数据库记录修改1条成功,I24_1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_label数据库记录修改1条失败,I24_1]"
I24_4("RtnParamErr","10001679",data1[0],"213","","C4-2,标签ID,群ID,标签名称(空)")
I24_4("RtnParamErr","10001679",data1[0],"21312123","jinhaoRevised","C4-3,标签ID,群ID(错),标签名称")
I24_4("RtnParamErr","10001679","","21312","jinhaoRevised","C4-4,标签ID(空),群ID(错),标签名称")
I24_4("RtnParamErr","10001679",data1[0],"","jinhaoRevised","C4-5,标签ID,群ID(空),标签名称")

print "5,================================================================================================="
# 5 红包群标签_修改红包群标签成员接口
# 相关表, t_redgroup_user_label , t_redgroup_label , t_redgroup_baseinfo , t_redgroup_memberinfo
# 业务逻辑:
# 1,新增群成员,t_redgroup_user_label对应labelid=46,groupid=213,userid=10001471
# 2,删除群成员,t_redgroup_user_label对应labelid=46,groupid=213,userid=10001497
# [info] 从t_redgroup_memberinfo中获取指定群ID可用userID
# 标签ID 来自 t_redgroup_label 表中 id字段,
# I24_5 前置条件是执行了I24_3 , 获取t_redgroup_label 表中 id字段,
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213 and labelName="jinhaoRevised"')
data1 = curT.fetchone()
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213 and labelName="%s"' %(labelName3_23))
data2 = curT.fetchone()

I24_5("RtnOK","10001679",data1[0],"213","","","C5-1,标签ID,群ID,新增成员ID(空),删除成员ID(空)")

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
a_list=[]
curT.execute('select userId from t_redgroup_memberinfo where groupUserId="10001679" ')
data9 = curT.fetchall()
for i in range(len(data9)):
    for each in data9[i]:
       a_list.append(str(each))
# print  "[info] memberIds = " + str(a_list)
TestUserId5_1 = ''.join(a_list[0:1])   # 获取 t_redgroup_memberinfo 第1个符合要求的userId
TestUserId5_2 = ''.join(a_list[1:2])   # 列表转字符串,获取第2个userId
TestUserId5_3 = ''.join(a_list[2:3])   # 列表转字符串,获取第3个userId
TestUserId5_23=TestUserId5_2 + "," + TestUserId5_3
TestUserId5_4 = ''.join(a_list[3:4])   # 列表转字符串,获取第4个userId
TestUserId5_5 = ''.join(a_list[4:5])   # 列表转字符串,获取第5个userId
TestUserId5_6 = ''.join(a_list[5:6])   # 列表转字符串,获取第6个userId
TestUserId5_56=TestUserId5_5 + "," + TestUserId5_6

# I24_5-2 新增1条标签用户
I24_5("RtnOK","10001679",data1[0],"213",TestUserId5_4,"","C5-2,标签ID,群ID,新增成员ID(1个),删除成员ID(空)")

# C5-2,检查新增1条记录
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId=%s and userId=%s' %(data1[0],TestUserId5_4))
data8 = curT.fetchone()
if data8[0]==1:print "  => [Ok,t_redgroup_user_label数据库记录新增1条成功,I24_5-2]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录新增1条失败,I24_5-2]"
curT.close(),conn.close()

#删除 I24_3-1 , I24_5-2
# I24_5("RtnOK","10001679",data1[0],"213","",TestUserId5_1,"C5-2,标签ID,群ID,新增成员ID(空),删除成员ID(1个)")
I24_5("RtnOK","10001679",data1[0],"213","",TestUserId5_4,"C5-2,标签ID,群ID,新增成员ID(空),删除成员ID(1个)")

# C5-2,检查删除1条记录
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId=%s and userId=%s' %(data1[0],TestUserId5_1))
data1 = curT.fetchone()
if data1[0]==1:print "  => [Ok,t_redgroup_user_label数据库记录删除1条成功,I24_5-2]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录删除1条失败,I24_5-2]"
curT.close(),conn.close()

# I24_5-3 新增2条标签用户
I24_5("RtnOK","10001679",data2[0],"213",TestUserId5_56,"","C5-3,标签ID,群ID,新增成员ID(2个),删除成员ID(空)")

# C5-3,检查新增2条记录
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId=%s' %(data2[0]))
data1 = curT.fetchone()
if data1[0]==4:print " => [Ok,t_redgroup_user_label数据库记录新增2条成功,I24_5-3]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录新增2条失败,I24_5-3]"
curT.close(),conn.close()

# 删除 I24_3-2 , I24_5-3
# I24_5("RtnOK","10001679",data2[0],"213","",TestUserId5_23,"C5-5,标签ID,群ID,新增成员ID(空),删除成员ID(2个)")
I24_5("RtnOK","10001679",data2[0],"213","",TestUserId5_56,"C5-5,标签ID,群ID,新增成员ID(空),删除成员ID(2个)")

# C5-6,检查删除2条记录
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId=%s' %(data2[0]))
data1 = curT.fetchone()
if data1[0]==2:print "  => [Ok,t_redgroup_user_label数据库记录删除2条成功,I24_5-5]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录删除2条失败,I24_5-5]"
curT.close(),conn.close()

I24_5("RtnSysErr","10001679","","213",TestUserId5_1,"","C5-6,标签ID(空),群ID,新增成员ID,删除成员ID(空)")
I24_5("RtnParamErr","10001679",varRandom4,"",TestUserId5_1,"","C5-7,标签ID,群ID(空),新增成员ID,删除成员ID(空)")
I24_5("RtnParamErr","10001679","","",TestUserId5_1,"","C5-8,标签ID(空),群ID(空),新增成员ID(1个),删除成员ID(空)")
I24_5("RtnParamErr","10001679",varRandom4,"213112","","","C5-9,标签ID,群ID(错),新增成员ID(空),删除成员ID(空)")

print "6,================================================================================================="
# 6 红包群标签_删除红包群标签接口
# 已完成, 删除 t_redgroup_label 1条 , t_redgroup_user_label 1条. (已完成 删除 t_redgroup_label 1条 , t_redgroup_user_label 2条. )
# 获取I24_3-1新增记录的ID,如 # I24_3("RtnOK","10001679","10001679","213",labelName,TestUserId3_1,"C3-1,用户ID,群ID,标签名称,标签成员ID(1个)") ,后修改过labelName = jinhaoRevised
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213 and labelName="jinhaoRevised"')
data1 = curT.fetchone()
curT.close(),conn.close()

I24_6("RtnOK","10001679",data1[0],"213","C6-1,标签ID,群ID") # 删除I24_3-1
sleep(2)
# I24_6-1,检查2个表, t_redgroup_label,id(删1条) , t_redgroup_user_label,labelId(删1条)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_label where groupId=213 and labelName="jinhaoRevised"')
data2 = curT.fetchone()
if data2[0]==0:print "  => [Ok,t_redgroup_label数据库记录删除1条成功,I24_6-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_label数据库记录删除1条失败,I24_6-1]"
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId="%s"' % (data1[0]))
data1 = curT.fetchone()
if data1[0]==0:print "  => [Ok,t_redgroup_user_label数据库记录删除1条成功,I24_6-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录删除1条失败,I24_6-1]"
curT.close(),conn.close()

# 获取I24_3-2新增记录的ID,如 # I24_3("RtnOK","10001679","10001679","213",labelName3_23,TestUserId3_23,"C3-2,用户ID,群ID,标签名称,标签成员ID(2个)")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213 and labelName="%s"' %(labelName3_23))
data3 = curT.fetchone()
curT.close(),conn.close()

I24_6("RtnOK","10001679",data3[0],"213","C6-2,标签ID,群ID") # 删除I24_3-2

# I24_6-2,检查2个表, t_redgroup_label,id(删1条) , t_redgroup_user_label,labelId(删1条)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_label where groupId=213 and labelName="%s"' %(labelName3_23))
data2 = curT.fetchone()
if data2[0]==0:print "  => [Ok,t_redgroup_label数据库记录删除2条成功,I24_6-2]"
else:print "  => [errorrrrrrrrrr,t_redgroup_label数据库记录删除2条失败,I24_6-2]"
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and labelId="%s"' % (data3[0]))
data1 = curT.fetchone()
if data1[0]==0:print "  => [Ok,t_redgroup_user_label数据库记录删除2条成功,I24_6-2]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库记录删除2条失败,I24_6-2]"
curT.close(),conn.close()
I24_6("RtnParamErr","10001679","","213","C6-3,标签ID(空),群ID")
I24_6("RtnParamErr","10001679","89","","C6-4,标签ID,群ID(空)")
I24_6("RtnParamErr","10001679","","","C6-5,标签ID(空),群ID(空)")
I24_6("RtnParamErr","10001679","-1.00","-0.01","C6-6,标签ID(错),群ID(错)")

print "7,================================================================================================="
# 7 红包群标签_获取单个红包群标签接口
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
a_list=[]
curT.execute('select id from t_redgroup_label where groupId=213')
data9 = curT.fetchall()
for i in range(len(data9)):
    for each in data9[i]:
       a_list.append(str(each))
print  "[info] id = " + str(a_list)
TestUserId7_1 = ''.join(a_list[0:1])   # 获取 t_r

I24_7("RtnOK","10001679",TestUserId7_1,"C7-1,标签ID")
# I24_7("RtnOK","10001679","13812","C7-1,标签ID(错)") # 后端未处理.
I24_7("RtnParamErr","10001679","","C7-2,标签ID(空)")
I24_7("RtnSysErr","10001679","-1.00","C7-3,标签ID(错)")

print "8,================================================================================================="
# 8 红包群标签_获取红包群所有标签接口
I24_8("RtnOK","10001679","213","C8-1,群ID")
I24_8("RtnParamErr","10001679","","C8-2,群ID(空)")
I24_8("RtnSysErr","10001679","-1.00","C8-3,群ID(错)")

print "9,================================================================================================="
# 9 红包群成员_添加红包群成员接口
# I24_9业务逻辑: 分别在t_redgroup_user_label 和 t_redgroup_memberinfo 表中创建 1 条记录.
# 前置条件1: 执行(select * from t_redgroup_memberinfo where groupUserId=10001679),如结果中无 userId=10001484 记录时. 则分别在 t_redgroup_memberinfo 和 t_redgroup_user_label 表中创建 1 条记录.
# 前置条件2: 执行(select * from t_redgroup_memberinfo where groupUserId=10001679),如结果中有 userId=10001484 记录时. 则不在两表中创建记录.
# 前置条件3: 在前置条件1基础上,如果参数用户标签为空时,则t_redgroup_user_label表中不创建记录.
# 依据前置条件2, 遍历 t_redgroup_memberinfo 和 t_redgroup_user_label 表 , 如果记录存在则先删除.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
a_list=[]
curT.execute('select userId from t_redgroup_memberinfo where groupId=213 and groupUserId=10001679')
data1 = curT.fetchall()
for i in range(len(data1)):
    for each in data1[i]:
       a_list.append(str(each))
TestUserId9_last = ''.join(a_list[-1])   # 获取 t_redgroup_memberinfo 第最后1个符合要求的userId
TestUserId9_sub = int(TestUserId9_last)-1
# print TestUserId9_sub
if data1[0]>=1:
 curT.execute('delete from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId9_sub))
 conn.commit()
curT.execute('select count(id) from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId9_sub))
data1 = curT.fetchone()
if data1[0]>=1:
 curT.execute('delete from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId9_sub))
 conn.commit()

# 满足前置条件1,分别在t_redgroup_user_label 和 t_redgroup_memberinfo 表中创建 1 条记录.
I24_9("RtnOK","10001679",TestUserId9_sub,"213","10001679",varRandom4,"C9-1,用户ID,群ID,群主用户ID,用户标签")

# C9-1 检查 t_redgroup_memberinfo 表中新增1条记录 userId=10001484,groupId=213,labelId=115
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId9_sub))
data1 = curT.fetchone()
if data1[0]==1:print "  => [OK,t_redgroup_memberinfo数据库新增1条记录成功,I24_9-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库新增1条记录失败,I24_9-1]"
# C9-1 检查 t_redgroup_user_label 表中新增1条记录 userId=10001484,groupId=213,labelId=115
curT.execute('select count(id) from t_redgroup_user_label where userId=%s and groupId=213' %(TestUserId9_sub))
data1 = curT.fetchone()
if data1[0]==1:print "  => [OK,t_redgroup_user_label数据库新增1条记录成功,I24_9-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库新增1条记录失败,I24_9-1]"
curT.close(),conn.close()

# 依据前置条件2,分别对 t_redgroup_memberinfo 和 t_redgroup_user_label 表 , 释放零时数据.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId9_sub))
data1 = curT.fetchone()
if data1[0]>=1:
 curT.execute('delete from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId9_sub))
 conn.commit()
curT.execute('select count(id) from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId9_sub))
data1 = curT.fetchone()
if data1[0]>=1:
 curT.execute('delete from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId9_sub))
 conn.commit()

# 满足前置条件3
I24_9("RtnOK","10001679",TestUserId9_sub,"213","10001679","","C9-2,用户ID,群ID,群主用户ID,用户标签(空)")

# C9-2,检查 t_redgroup_memberinfo 表, 新增1条记录 userId=10001484,groupId=213,labelId=115
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId9_last))
data1 = curT.fetchone()
if data1[0]==1:
 print "  => [OK,t_redgroup_memberinfo数据库新增1条记录成功,I24_9-2]"
else:
 print "  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库新增1条记录失败,I24_9-2]"
# C9-2,检查 t_redgroup_user_label 表 , 无新增记录 userId=10001484,groupId=213,labelId=115
curT.execute('select count(id) from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId9_last))
data1 = curT.fetchone()
if data1[0]==0:
 print "  => [OK,t_redgroup_user_label数据库新增1条记录成功,I24_9-2]"
else:
 print "  => [errorrrrrrrrrr,t_redgroup_user_label数据库新增1条记录失败,I24_9-2]"
curT.close(),conn.close()

I24_9("RtnParamErr","10001679","","213","10001679","113","C9-3,用户ID(空),群ID,群主用户ID,用户标签")
I24_9("RtnParamErr","10001679",TestUserId9_last,"","10001679","113","C9-4,用户ID,群ID(空),群主用户ID,用户标签")
I24_9("RtnParamErr","10001679",TestUserId9_last,"213","","113","C9-5,用户ID,群ID,群主用户ID(空),用户标签")

print "10,================================================================================================="
# 10 红包群成员_修改红包群成员备注接口
# 业务逻辑: 修改群成员备注时,会涉及到2张表,t_redgroup_memberinfo 表中remarks , t_redgroup_user_label 表中remarks ,
# 两张表中群主ID的成员非一一对应,如在 t_redgroup_user_label 表中没有找到 与之对应的(t_redgroup_memberinfo)成员记录时,则忽略不处理.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
conn.set_character_set('utf8')
curT.execute('SET NAMES utf8;')
curT.execute('SET CHARACTER SET utf8;')
curT.execute('SET character_set_connection=utf8;')
curT.execute('select count(id),userId,remarks from t_redgroup_memberinfo where groupUserId=10001679')
data1 = curT.fetchone()
# 如果t_redgroup_memberinfo 表中, groupUserId=10001679 中有群成员记录时,则修改第一条记录的备注,输出修改前\修改后\恢复后的结果.
if data1[0]>=1:
    print u"  => [t_redgroup_memberinfo,数据修改前 => " + str(data1[2]) +"(" + str(data1[1]) +")]"

    I24_10("RtnOK","10001679",data1[1],"213","jinhaoI24_10-1","C10-1,用户ID,群ID,用户昵称")

    # 检查 修改后的备注,并最终恢复到修改前的备注
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('select count(id),userId,remarks from t_redgroup_memberinfo where groupUserId=10001679')
    data2 = curT.fetchone()
    if data2[2]=="jinhaoI24_10-1":
        print u"  => [t_redgroup_memberinfo数据修改后 => " + str(data2[2]) +"(" + str(data2[1]) +")]"
        conn.set_character_set('utf8')
        curT.execute('SET NAMES utf8;')
        curT.execute('SET CHARACTER SET utf8;')
        curT.execute('SET character_set_connection=utf8;')
        curT.execute('update t_redgroup_memberinfo set remarks="%s" where groupUserId=10001679 and userId=%s' % (data1[2],data2[1]))
        conn.commit()
        print u"  => [t_redgroup_memberinfo,数据已恢复 => " + str(data1[2]) +"(" + str(data2[1]) +")]"
    else:
        print u"  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库中修改后的备注未找到,C10-1]"
else:
    print "  => [errorrrrrrrrrr,数据库中无法找到10001679对应的群成员,因此C10-1测试用例未执行.]"

# 如果 t_redgroup_user_label 表中, 与之t_redgroup_memberinfo中无对应的userId记录,则忽略,否则同时被修改备注, 检查后恢复原始备注信息.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id),userId,remarks from t_redgroup_user_label where groupId=213 and userId=%s ' %(data1[1]))
data3 = curT.fetchone()
if data3[0]<>0:
    if data3[2]=="jinhaoI24_10-1":
        print "  => t_redgroup_user_label,数据修改后 => " + str(data3[2]) +"(" + str(data3[1]) +")]"
        conn.set_character_set('utf8')
        curT.execute('SET NAMES utf8;')
        curT.execute('SET CHARACTER SET utf8;')
        curT.execute('SET character_set_connection=utf8;')
        curT.execute('update t_redgroup_user_label set remarks="%s" where groupId=213 and userId=%s' % (data1[2],data3[1]))
        conn.commit()
        print u"  => [t_redgroup_user_label,数据已恢复 => " + str(data1[2]) +"(" + str(data3[1]) +")]"

I24_10("RtnParamErr","10001679","","213","alibaba","C10-2,用户ID(空),群ID,用户昵称")
I24_10("RtnParamErr","10001679","10001684","","alibaba","C10-3,用户ID,群ID(空),用户昵称")
I24_10("RtnOK","10001679","10001684","213","","C10-4,用户ID,群ID,用户昵称(空)") # 用户昵称为空时,使用原先的昵称
I24_10("RtnParamErr","10001679","0.1","0.1","alibaba1","C10-5,用户ID(错),群ID(错),用户昵称")

print "11,================================================================================================="
# 11 红包群成员_加入或移除群成员黑名单接口
# 涉及到2张表, t_redgroup_user_label 和 t_redgroup_memberinfo
# 业务逻辑: 筛选出符合条件的记录(select * from t_redgroup_memberinfo where groupUserId=10001679 and groupId=213),加入黑名单则将isBlack值修改为1 ,移除黑名单则将isBlack值修改为0
# 自动化处理逻辑: 在 t_redgroup_memberinfo 表中筛选出符合要求的第一条记录(如userId=10001497,remarks=年糕测试) ,输出修改前的黑名单值, 然后执行接口测试,输出修改后的黑名单值,最后恢复黑名单值.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id),userId,isBlack from t_redgroup_memberinfo where groupUserId=10001679')
data1 = curT.fetchone()
# 如果t_redgroup_memberinfo 表中, groupUserId=10001679 中有群成员记录时,则修改第一条记录的备注,输出修改前\修改后\恢复后的结果.
if data1[0]>=1:
    print u"  => [t_redgroup_memberinfo,数据修改前 => " + str(data1[2]) +"(" + str(data1[1]) +")]"

    if data1[2]==1:
        I24_11("RtnOK","10001679",data1[1],"213","0","C11-2,用户ID,群ID,是否为黑名单成员(移出)")    #   # 移除黑名单
    else:
        I24_11("RtnOK","10001679",data1[1],"213","1","C11-1,用户ID,群ID,是否为黑名单成员(加入)")    # 加入黑名单

    # 检查 修改后的黑名单值,并最终恢复到修改前的黑名单值
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('select count(id),userId,isBlack from t_redgroup_memberinfo where groupUserId=10001679')
    data2 = curT.fetchone()
    if data2[2]==1:
        print u"  => [t_redgroup_memberinfo,数据修改后 => " + str(data2[2]) +"(" + str(data2[1]) +")]"
        curT.execute('update t_redgroup_memberinfo set isBlack=%s where groupUserId=10001679 and userId=%s' % (data1[2],data2[1]))
        conn.commit()
        print u"  => [t_redgroup_memberinfo,数据已恢复 => " + str(data1[2]) +"(" + str(data2[1]) +")]"
    else:
        print u"  => [errorrrrrrrrrr,数据库中修改后的黑名单值未找到,C11-1]"
else:
    print "  => [errorrrrrrrrrr,数据库中无法找到10001679对应的群成员,因此C11-1测试用例未执行.]"

# 如果 t_redgroup_user_label 表中, 与之t_redgroup_memberinfo中无对应的userId记录,则忽略,否则同时被修改黑名单值, 检查后恢复原始黑名单值.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id),userId,isBlack from t_redgroup_user_label where groupId=213 and userId=%s ' %(data1[1]))
data3 = curT.fetchone()
if data3[0]<>0:
    if data3[2]==1:
        print "  => [t_redgroup_user_label,数据修改后 => " + str(data3[2]) +"(" + str(data3[1]) +")]"
        curT.execute('update t_redgroup_user_label set isBlack="%s" where groupId=213 and userId=%s' % (data1[2],data3[1]))
        conn.commit()
        print u"  => [t_redgroup_user_label,数据已恢复 => " + str(data1[2]) +"(" + str(data3[1]) +")]"

I24_11("RtnOK","10001679",data1[1],"213","2","C11-3,用户ID,群ID,是否为黑名单成员(错)")
I24_11("RtnSysErr","10001679",data1[1],"213","","C11-4,用户ID,群ID,是否为黑名单成员(空)")
I24_11("RtnParamErr","10001679","","213","1","C11-5,用户ID(空),群ID,是否为黑名单成员")
I24_11("RtnParamErr","10001679",data1[1],"","1","C11-6,用户ID,群ID(空),是否为黑名单成员")

print "12,================================================================================================="
# 12 红包群成员_修改单个群成员标签接口
# 涉及2张表, 获取 t_redgroup_label , t_redgroup_user_label
# 业务逻辑: 先获取 t_redgroup_lael 表中,条件是groupId=213 的所有id ,将 t_redgroup_user_label 表中,条件是groupId=213 某个userId的labelId值(如113),修改为 t_redgroup_lael 表中存在的任何一个id(如46)
# 自动化处理逻辑: 输出2张表中符合要求的id(t_redgroup_lael) 和 labelId(t_redgroup_lael),然后修改t_redgroup_lael中labelId的值(此值来自t_redgroup_lael的id)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213')
data3 = curT.fetchall()
if len(data3)>=2:
    s=""
    for i in range(len(data3)):
     for each in data3[i]:
      s = s + "," + str(each)
    print u"  => [t_redgroup_label,可用ID => " + s[1:] + "]"
    list1=[]
    for each in data3[0]:
      list1.append(str(each))
    for each in data3[1]:
      list1.append(str(each))
    # print list1[0]
    # print list1[1]
    curT.execute('select labelId from t_redgroup_user_label where groupId=213')
    data3 = curT.fetchall()
    # print len(data3)
    for j in range(len(data3)):
        for i in range(2):
            for each in data3[j]:
               y1 = str(each)
            if y1==list1[i]:
                varLabelid = list1[i]
                break
    # print varLabelid
    if list1[0]==varLabelid:
        curT.execute('select userId from t_redgroup_user_label where groupID=213 and labelId=%s ' % (varLabelid))
        data4 = curT.fetchone()
        varID=list1[1]
    if list1[1]==varLabelid:
        curT.execute('select userId from t_redgroup_user_label where groupID=213 and labelId=%s ' % (varLabelid))
        data4 = curT.fetchone()
        varID=list1[0]

    print u"  => [t_redgroup_user_label,数据修改前 => " + str(varLabelid) + "(" + str(data4[0]) + ")]"
else:
    print "  => [errorrrrrrrrrr,可用ID少于2个,无法测试,C12-1]"

I24_12("RtnOK","10001679",data4[0],"213",varLabelid,varID,"C12-1,用户ID,群ID(10001483),群成员老标签(113),群成员新标签(46)")

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select labelId from t_redgroup_user_label where groupID=213 and userId=%s ' % (data4[0]))
data5 = curT.fetchone()
print u"  => [t_redgroup_user_label,数据修改后 => " + str(data5[0]) + "(" + str(data4[0]) + ")]"

# 恢复数据
curT.execute('update t_redgroup_user_label set labelId="%s" where groupId=213 and userId=%s' % (varLabelid,data4[0]))
conn.commit()
curT.execute('select labelId,userId from t_redgroup_user_label where groupID=213 and userId=%s ' % (data4[0]))
data5 = curT.fetchone()
print u"  => [t_redgroup_user_label,数据已恢复 => " + str(data5[0]) + "(" + str(data5[1]) + ")]"

I24_12("RtnParamErr","10001679","","213",varLabelid,varID,"C12-2,用户ID(空),群ID,群成员老标签,群成员新标签")
I24_12("RtnParamErr","10001679",data4[0],"",varLabelid,varID,"C12-3,用户ID(空),群ID(空),群成员老标签,群成员新标签")

print "13,================================================================================================="
# 13 红包群黑名单用户列表接口（新增参数，修改返回值）
# select * from t_redgroup_memberinfo where groupUserId=10001679 and isBlack=1
I24_13("RtnOK","10001679","10001679","213","","C13-1,用户ID,群ID,搜索名称(空)")
I24_13("RtnOK","10001679","10001679","213","你","C13-2,用户ID,群ID,搜索名称(模糊)")
I24_13("RtnOK","10001679","10001679","213","errnick","C13-3,用户ID,群ID,搜索名称(错)")

print "14,================================================================================================="
# 14 红包群成员_删除群成员接口
# 涉及到2个表, 分别在 t_redgroup_user_label , t_redgroup_memberinfo
# 业务逻辑: 同时删除此2个表中符合条件的记录.
# 自动化处理逻辑:先获取一份 t_redgroup_memberinfo 表中所有userId字段, 获取最小的那个userID并减1,用于稍后的群成员操作.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select userId from t_redgroup_memberinfo where groupId=213 order by userId')
data3 = curT.fetchall()
for each in data3[0]:
    testId=int(each)-1
print "  => [测试数据userId => " + str(testId)
# 删除前先新增一个群成员 from I24_9 ,需确保此群成员userID不在 t_redgroup_memberinfo 表中.
# I24_9业务逻辑: 分别在t_redgroup_user_label 和 t_redgroup_memberinfo 中新增1条记录.
I24_9("RtnOK","10001679",testId,"213","10001679","500","C9-1,用户ID,群ID,群主用户ID,用户标签")

I24_14("RtnOK","10001679",testId,"213","C14-1,用户ID,群ID")
# I24_14-1,检查2个数据库记录是否已删除.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where groupId=213 and userId=%s ' % (testId))
data4 = curT.fetchone()
if data4[0]==0:print "  => [t_redgroup_memberinfo,数据库记录删除成功,I24_14-1]"
else:print "  => [t_redgroup_memberinfo,数据库记录删除失败,I24_14-1]"
curT.execute('select count(id) from t_redgroup_user_label where groupId=213 and userId=%s ' % (testId))
data4 = curT.fetchone()
if data4[0]==0:print "  => [t_redgroup_user_label,数据库记录删除成功,I24_14-1]"
else:print "  => [t_redgroup_user_label,数据库记录删除失败,I24_14-1]"
I24_14("RtnParamErr","10001679","","213","C14-1,用户ID(空),群ID")
I24_14("RtnParamErr","10001679",testId,"","C14-2,用户ID,群ID(空)")
I24_14("RtnParamErr","10001679","0.01","1.1","C14-3,用户ID(错),群ID(错)")

print "15,================================================================================================="
# 15 红包群成员_获取所有群成员接口(完成) (不包括黑名单,不包括进群又退群的人)
# 业务逻辑: 检查表 t_redgroup_memberinfo ,条件:groupId=213 且 isBlack=0 的所有成员.
# 从表中获取符合条件的个数,譬如 将个数存入data1[0],并与接口Json返回的数量对比.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where groupUserId=10001679 and memberState=0 and groupId=213 and isBlack=0')
data1 = curT.fetchone()
curT.close(),conn.close()
I24_15("RtnOK","10001679","213","0",data1[0],"C15-1,群ID,排序ID")
I24_15("RtnParamErr","10001679","","0","","C15-2,群ID(空),排序ID")
I24_15("RtnSysErr","10001679","213","1000","","C15-3,群ID,排序ID(错)") # ? 排序ID有相应的接口文档
I24_15("RtnSysErr","10001679","213","","","C15-3,群ID,排序ID(空)")
print "16,================================================================================================="
# # 16 红包群成员_获取群标签所有成员接口
# 相关表, t_redgroup_user_label
I24_16("RtnOK", "10001684","213", "75", "C16-1,群ID,群标签ID")
I24_16("RtnOKNone", "10001684","0", "0", "C16-2,群ID(0),群标签ID(0)")
I24_16("RtnOKNone", "10001684","-1", "-1", "C16-3,群ID(负数),群标签ID(负数)")
I24_16("RtnOKNone", "10001684","1", "1", "C16-4,群ID(错),群标签ID(错)")
I24_16("RtnParamErr", "10001684","", "", "C16-5,群ID(空),群标签ID(空)")
I24_16("RtnParamErr", "10001684","", "75", "C16-6,群ID(空),群标签ID")
I24_16("RtnParamErr", "10001684","213", "", "C16-7,群ID,群标签ID(空)")
I24_16("RtnSysErr", "10001684","0.1", "75", "C16-8,群ID(小数),群标签ID")

print "17,================================================================================================="
# 17 红包群成员_获取单个群成员在该群的所有标签接口
# 相关表, t_redgroup_user_label , t_redgroup_label
# 先创建群标签和群成员,I24_3 ,最后删除群标签 和群成员
a_list=[]
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select userId from t_redgroup_memberinfo where groupId=213 and groupUserId=10001679')
data1 = curT.fetchall()
for i in range(len(data1)):
    for each in data1[i]:
       a_list.append(str(each))
TestUserId17_last = ''.join(a_list[-1])   # 获取 t_redgroup_memberinfo 第最后1个符合要求的userId

labelName17 = "jinhao"+str(varTimeYMDHSM)
I24_3("RtnOK","10001679","10001679","213",labelName17,TestUserId17_last,"C3-1,用户ID,群ID,标签名称,标签成员ID(1个)")

I24_17("RtnOK", "10001678",TestUserId17_last, "213", "C17-1,用户ID,群ID")
# I24_17("RtnOK", "10001678","0", "0", "C17-2,用户ID(0),群ID(0)")
# I24_17("RtnOK", "10001678","-1", "-1", "C17-3,用户ID(负数),群ID(负数)")
# I24_17("RtnOK", "10001678","1", "1", "C17-4,用户ID(错),群ID(错)")
I24_17("RtnParamErr", "10001678","", "", "C17-5,用户ID(空),群ID(空)")
I24_17("RtnParamErr", "10001678","", "213", "C17-6,用户ID(空),群ID")
I24_17("RtnParamErr", "10001678",TestUserId17_last, "", "C17-7,用户ID,群ID(空)")
I24_17("RtnSysErr", "10001678",TestUserId17_last, "0.1", "C17-8,用户ID,群ID(小数)")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_redgroup_label where groupId=213 and labelName="%s"' %(labelName17))
data1 = curT.fetchone()
curT.close(),conn.close()
I24_6("RtnOK","10001679",data1[0],"213","C6-1,标签ID,群ID") # 删除I24_3-1

print "18,================================================================================================="
# # 18 红包群成员_修改群备注接口
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
conn.set_character_set('utf8')
curT.execute('SET NAMES utf8;')
curT.execute('SET CHARACTER SET utf8;')
curT.execute('SET character_set_connection=utf8;')
curT.execute('select userId,groupId from t_redgroup_memberinfo where groupId=213')
data1 = curT.fetchone()
# nickname18=u"中文Ts~!@#$%……*()"
nickname18="jinhaoremark"

I24_18("RtnOK",str(data1[0]),data1[0],"213",nickname18,"C18-1,用户ID,群ID,群呢称(改)")

# C18-1,检查数据库修改记录
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(userId) from t_redgroup_memberinfo where userId=%s and groupId=213 and groupRemark="%s"' %(data1[0],nickname18))
data2 = curT.fetchone()
if data2[0]==1:print "  => [Ok,t_redgroup_memberinfo数据库群备注修改1条成功,I24_18]"
else:print "  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库群备注修改1条失败,I24_18]"

# 业务逻辑, 如果群昵称为空时, 自动获取原先默认昵称
I24_18("RtnOK",str(data1[0]),data1[0],"213","","C18-2,用户ID,群ID,群呢称(空)")

# C18-2,检查数据库修改记录为空
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select groupRemark from t_redgroup_memberinfo where userId=%s and groupId=213 ' %(data1[0]))
data3 = curT.fetchone()
if data3[0]<>"":print "  => [OK,t_redgroup_memberinfo数据库群备注修改1条为空成功,I24_18]"
else:print "  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库群备注修改1条为空失败,I24_18]"

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select userId from t_redgroup_memberinfo where groupId=213 order by userId')
data3 = curT.fetchall()
for each in data3[0]:
    TestUserId18_sub=int(each)-1

I24_18("RtnParamErr",str(data1[0]),"","213",nickname18,"C18-3,用户ID(空),群ID,群呢称")
I24_18("RtnParamErr",str(data1[0]),data1[0],"",nickname18,"C18-4,用户ID,群ID(空),群呢称")
I24_18("RtnParamErr",str(data1[0]),"","",nickname18,"C18-5,用户ID(空),群ID(空),群呢称")
I24_18("RtnParamErr",str(data1[0]),TestUserId18_sub,"213",nickname18,"C18-6,用户ID(错),群ID,群呢称")
I24_18("RtnOK",str(data1[0]),data1[0],"0",nickname18,"C18-6,用户ID,群ID(错),群呢称")

print "19,================================================================================================="
# 19 红包群成员_获取所有新成员列表接口
# 涉及表, t_group_memberinfo 中 ,is_check =1 1表示未查看 , 0=已查看 ,
# 业务逻辑: 返回 t_group_memberinfo 表中未查看的新成员,统计count计数
# # 获取 t_group_memberinfo 表中 is_check=1 的数量,统计count计数
# 如果 count计数=0 则验证json返回count是否等于 0 ,并新增1个成员如I24_9-2 最终删除此用户;
# 如果 count计数>=1 则验证json返回count是否>=1

# 获取 t_group_memberinfo 表中 is_check=1 的个数
varJsonRtnIsCheckNums=I24_19("RtnOK","10001679","10001679","213","0","5","C19-1,用户ID,群ID,分页开始位置,每页显示条数")

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where isCheck=1 and groupUserId=10001679')
data3 = curT.fetchone()
if data3[0]==0:
    # 如果 count计数=0 则验证json返回count是否等于 0 ,并新增1个成员如I24_9-2 最终删除此用户;
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    a_list=[]
    curT.execute('select userId from t_redgroup_memberinfo where groupId=213 and groupUserId=10001679')
    data1 = curT.fetchall()
    for i in range(len(data1)):
        for each in data1[i]:
           a_list.append(str(each))
    TestUserId19_last = ''.join(a_list[-1])   # 获取 t_redgroup_memberinfo 第最后1个符合要求的userId
    TestUserId19_sub = int(TestUserId19_last)-1
    if data1[0]>=1:
     curT.execute('delete from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId19_sub))
     conn.commit()
    curT.execute('select count(id) from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId19_sub))
    data1 = curT.fetchone()
    if data1[0]>=1:
     curT.execute('delete from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId19_sub))
     conn.commit()

    I24_9("RtnOK","10001679",TestUserId19_sub,"213","10001679","","C9-2,用户ID,群ID,群主用户ID,用户标签(空)")
    varJsonRtnIsCheckNums=I24_19("RtnOK","10001679","10001679","213","0","5","C19-1,用户ID,群ID,分页开始位置,每页显示条数")

    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('select count(id) from t_redgroup_memberinfo where isCheck=1 and groupUserId=10001679')
    data2 = curT.fetchone()
    if data2[0]>=1 and data2[0]==varJsonRtnIsCheckNums:print "  => [OK,t_redgroup_memberinfo数据库isCheck数量与Json返回数量一致,I24_19-1]"
    else: "  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库isCheck数量与Json返回数量不一致,I24_19-1]"

    # 销毁新增的I24_9数据 ,由于调用了I24_9-2 ,因此不会在t_redgroup_user_label中创建记录,只需删除 t_redgroup_memberinfo 表中记录即可.
    curT.execute('delete from t_redgroup_memberinfo where userId=%s and groupId=213 ' %(TestUserId19_sub))
    conn.commit()

# 如果 count计数>=1 则验证json返回count是否>=1
if data3[0]>=1 and data3[0]==varJsonRtnIsCheckNums:print "  => [OK,t_redgroup_memberinfo数据库isCheck数量与Json返回数量一致,I24_19-1]"
else: "  => [errorrrrrrrrrr,t_redgroup_memberinfo数据库isCheck数量与Json返回数量不一致,I24_19-1]"

I24_19("RtnOK","10001679","10001679","213","-1","5","C19-2,用户ID,群ID,分页开始位置(错),每页显示条数")
I24_19("RtnOK","10001679","10001679","213","0","0","C19-3,用户ID,群ID,分页开始位置,每页显示条数(0)")

I24_19("RtnParamErr","10001679","100016791212","213","","5","C19-4,用户ID,群ID,分页开始位置(空),每页显示条数")
I24_19("RtnParamErr","10001679","","213","0","5","C19-5,用户ID(空),群ID,分页开始位置,每页显示条数")
I24_19("RtnParamErr","10001679","10001679","","1","5","C19-6,用户ID,群ID(空),分页开始位置,每页显示条数")
I24_19("RtnParamErr","10001679","10001680","213","1","5","C19-7,用户ID(错),群ID,分页开始位置,每页显示条数")
I24_19("RtnParamErr","10001679","10001679","000","1","5","C19-8,用户ID,群ID(错),分页开始位置,每页显示条数")
I24_19("RtnSysErr","10001679","10001679","213","0","","C19-9,用户ID,群ID,分页开始位置,每页显示条数(空)")
I24_19("RtnSysErr","10001679","10001679","213","0","llkk","C19-10,用户ID,群ID,分页开始位置,每页显示条数(错)")

print "20,================================================================================================="
#20 红包群查看分享奖励列表接口(新增返回值,老数据batchIndex默认从0开始)
# 获取belongId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
a_list=[]
curT.execute('select count(id),belongId from t_extension_fallinto where userId=10001679')
data1 = curT.fetchone()
# print data1[0]
# print data1[1]

if data1[0]>0:
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    a_list=[]
    curT.execute('select redAmount from t_extension_fallinto where userId=10001679 and belongId=%s' %(data1[1]))
    data2 = curT.fetchone()
    tmpamout = float(data2[0])/100.00

    varJsonRtnAmount = I24_20("RtnOK","10001679",data1[1],"213","10001679","C20-1,用户ID,群ID,群主用户ID")#batchIndex确认

    if tmpamout == float(varJsonRtnAmount):print "  => [OK,t_extension_fallinto 数据库amount数量与Json返回数量一致,I24_20-1]"
    else: print "  => [errorrrrrrrrrr,t_extension_fallinto 数据库amount数量与Json返回数量不一致,I24_20-1]"
else: print "  => [errorrrrrrrrrr,t_extension_fallinto , 暂无匹配数据,I24_20-1]"

I24_20("RtnOK","10001684","-1","213","10001679","C20-2,用户ID(错),群ID,群主用户ID")
I24_20("RtnParamErr","10001684","","213","10001679","C20-2,用户ID(空),群ID,群主用户ID")
I24_20("RtnParamErr","10001684","10001684","","10001679","C20-2,用户ID,群ID(空),群主用户ID")
I24_20("RtnParamErr","10001684","10001684","213","","C20-2,用户ID,群ID,群主用户ID(空)")
I24_20("RtnParamErr","10001684","10001684","2.13","10001679","C20-2,用户ID,群ID(错),群主用户ID")
I24_20("RtnParamErr","10001684","10001684","213","00000","C20-2,用户ID,群ID,群主用户ID(错)")

print "21,================================================================================================="
# I24_21 红包群消息_保存消息接口
# 涉及3张条, t_redgroup_message , t_redgroup_messamge_auth ,t_redgroup_memberinfo
# 业务逻辑: 执行I24_21接口后, 在 t_redgroup_message 表中新增1条记录,标签id=113  ;在 t_redgroup_messamge_auth 表中新增1条记录;
# 在 t_redgroup_memberinfo 表中 条件groupId=213 and isBlack=0 ,如果设置标签,如labelId= 113,则对应的isMessage +1 ;
# 如果无标签,则对应groupId所有成员的isMesage 均 +1
# 考虑到发送消息会扣费,因此需确保帐号内有钱,给账户余额初始化50元.(规则:前3次免费,第四次开始扣费)

# 初始化 账户余额=50元 及群成员人数
# 501~1000,1.5元/条
varMessage = "jinhao"+str(varTimeYMDHSM) # 发送的消息体
varMessageType = "0"  # 消息体类型 0=文字消息
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_memberinfo where groupId=213 and isBlack=0 and memberState=0')
data0 = curT.fetchone()
print u"[info] 10001679的群成员:" + str(data0[0]) + u"人 初始化账户余额=50元,消息内容:jinhao" + str(varTimeYMDHSM)
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10001679","countNumber",data0[0])
r2.hset("t_user:id:10001679","Commission_residue","5000")

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('update t_redgroup_baseinfo set countNumber = 1 where userId = 10001679 and id=213')
curT.execute('update t_user set Commission_residue = 5000 where id = 10001679 ')
conn.commit()

# 获取t_redgroup_user_label 表中groupId=213 的第一条记录 的 userId , LabelId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select userId,labelId from t_redgroup_user_label where groupId=213 ')
data1 = curT.fetchone()

# 获取 t_redgroup_memberinfo 表中 条件groupId=213 and isBlack=0 and userId = data1[0]的 isMessage ,如=9
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select isMessage from t_redgroup_memberinfo where groupId=213 and isBlack=0 and userId = %s' %(data1[0]))
data4 = curT.fetchone()

# 创建第1条,只有标签为113的用户可以收到消息 ,
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

# I24_21-1,检查数据库 t_redgroup_message 新增1条且标签id=113,
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id),id from t_redgroup_message where groupId=213 and groupMessage="%s" ' %(varMessage))
data2 = curT.fetchone()
if data2[0]>=1:print "  => [OK,t_redgroup_message数据库新增1条成功,I24_21]"
else:print "  => [errorrrrrrrrrr,t_redgroup_message数据库新增1条失败,I24_21]"
curT.close(), conn.close()

# I24_21-1,检查数据库  t_redgroup_messamge_auth 表中新增1条,
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and labelId=%s and messageState=0 and messageId=%s' % (data1[1],data2[1]))
data3 = curT.fetchone()
if data3[0]==1:print "  => [Ok,t_redgroup_messamge_auth数据库记录新增1条成功,I24_21]"
else:print "  => [errorrrrrrrrrr,t_redgroup_messamge_auth数据库记录新增1条失败,I24_21]"
curT.close(),conn.close()

# 获取 t_redgroup_memberinfo 表中 条件groupId=213 and isBlack=0 and userId = data1[0]的 isMessage ,如=10 ,原isMessage加1
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select isMessage from t_redgroup_memberinfo where groupId=213 and isBlack=0 and userId = %s' %(data1[0]))
data5 = curT.fetchone()
if data5[0]==data4[0]+1:print "  => [OK,t_redgroup_message数据库isMessage+1成功,I24_21-1]"
else:print "  => [errorrrrrrrrrr,t_redgroup_message数据库isMessage+1成功,I24_21-1]"

# 创建第2条
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

# 获取 t_redgroup_message  表中groupId=213的个数,如果<=3 免费,否则<=50扣费1元/条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_message where createTime between "%s" And "%s" and groupId=213 ' %(varTimeFrom,varTimeEnd))
data6 = curT.fetchone()
if data6[0]<3:
    #判断 t_user 中 commission_residue 是否是50元
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('select commission_residue from t_user where id=10001679')
    data7 = curT.fetchone()
    if data7[0]==5000:print "  => [OK,t_user,发信息" + str(data6[0]) +"次,账户余额=50]"
    else:print "  => [errorrrrrrrrrr,t_user,发信息" + str(data6[0]) +"次,账户余额<>50,I24_21-1]"

# 创建第3条
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

# 创建第4条
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

# message记录为4条时
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select commission_residue from t_user where id=10001679')
data7 = curT.fetchone()
if data7[0]==4900:print "  => [OK,t_user,发信息4次,账户余额=49]"
else:print "  => [errorrrrrrrrrr,t_user,发信息4次,账户余额<>49,I24_21-1]"

# 501~1000,1.5元/条
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10001679","countNumber","501")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('update t_redgroup_baseinfo set countNumber = 501 where userId = 10001679 and id=213')
conn.commit()

# 创建第5条
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select commission_residue from t_user where id=10001679')
data7 = curT.fetchone()
if data7[0]==4750:print "  => [OK,t_user,修改群成员501人,账户余额=47.50]"
else:print "  => [errorrrrrrrrrr,t_user,修改群成员501人,账户余额<>47.50,I24_21-1]"

# 1001~2000,2元/条
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10001679","countNumber","1001")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('update t_redgroup_baseinfo set countNumber = 1001 where userId = 10001679 and id=213')
conn.commit()

# 创建第6条
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select commission_residue from t_user where id=10001679')
data7 = curT.fetchone()
if data7[0]==4550:print "  => [OK,t_user,修改群成员1001人,账户余额=45.50]"
else:print "  => [errorrrrrrrrrr,t_user,修改群成员1001人,账户余额<>45.50,I24_21-1]"

# 2001以上,3元/条
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10001679","countNumber","2001")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('update t_redgroup_baseinfo set countNumber = 2001 where userId = 10001679 and id=213')
conn.commit()

# 创建第7条
I24_21("RtnOK","10001679","10001679","213",varMessage,data1[1],varMessageType,"C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
sleep(3)

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select commission_residue from t_user where id=10001679')
data7 = curT.fetchone()
if data7[0]==4250:print "  => [OK,t_user,修改群成员2001人,账户余额=42.50]"
else:print "  => [errorrrrrrrrrr,t_user,修改群成员2001人,账户余额<>42.50,I24_21-1]"

#  恢复群成员人数 ,修改redis 和 t_redgroup_baseinfo
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('update t_redgroup_baseinfo set countNumber=%s where userId=10001679' %(data0[0]))
conn.commit()
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10001679","countNumber",data0[0])

print "22,================================================================================================="
# #22 红包群消息_群主删除消息接口 , data2[0]依赖I24_21
I24_22("RtnOK","10001679","10001679","213",data2[1],"C22-1, 用户ID, 群ID, 消息ID")
# C22-1,检查数据库t_redgroup_message删除1条(messageState=1)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_message where groupId=213 and messageState=1 and id=%s' %(data2[1]))
data8 = curT.fetchone()
if data8[0]==1:print "  => [OK,t_redgroup_message数据库删除1条成功,I24_22]"
else:print "  => [errorrrrrrrrrr,t_redgroup_message数据库删除1条失败,I24_22]"
curT.close(),conn.close()

print "23,================================================================================================="
#23 红包群消息_群主撤回消息接口
# 业务逻辑:撤回条件是在2分钟内发送的信息才能被撤回.
I24_23("RtnOK","10001679","10001679","213",data2[1],"C23-1, 用户ID, 群ID, 消息ID")
# C23-1,检查数据库t_redgroup_message撤回1条(messageState=2),t_redgroup_messamge_auth撤回一条(messageState=2)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_message where groupId=213 and messageState=2 and id=%s' %(data2[1]))
data9 = curT.fetchone()
if data9[0]==1:print "  => [OK,t_redgroup_message数据库撤回1条成功,I24_23]"
else:print "  => [errorrrrrrrrrr,t_redgroup_message数据库撤回1条失败,I24_23]"
curT.close(),conn.close()
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and messageState=2 and messageId=%s' %(data2[1]))
data9 = curT.fetchone()
if data9[0]==1:print "  => [OK,t_redgroup_messamge_auth数据库撤回1条成功,I24_23]"
else:print "  => [errorrrrrrrrrr,t_redgroup_messamge_auth数据库撤回1条失败,I24_23]"
curT.close(),conn.close()

print "24,================================================================================================="
# # 24红包群消息_群成员举报消息接口
# # 业务逻辑:执行I24_24接口后,需在后台 投诉/举报管理 页面中 审核后, t_redgroup_message 的nessageState为3.
I24_24("RtnOK","10001679","10001679","213",data2[1],"C24-1, 用户ID, 群ID, 消息ID")

# # 清除I24_21测试数据
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('delete from t_redgroup_message where groupId=213 and groupMessage="%s"' %(varMessage))
curT.execute('delete from t_redgroup_messamge_auth where groupId=213 and labelId=%s' %(data1[1]))
conn.commit()

print "25,================================================================================================="
# 25 红包群消息_我的红包群消息列表接口
I24_25("RtnOK", "10001679","10001679", "213", "C25-1,用户ID,群ID")
I24_25("RtnParamErr", "10001679","", "", "C25-2,用户ID(空),群ID(空)")
I24_25("RtnParamErr", "10001679","", "213", "C25-3,用户ID(空),群ID")
I24_25("RtnParamErr", "10001679","10001679", "", "C25-4,用户ID,群ID(空)")
I24_25("RtnParamErr", "10001679","1", "213", "C25-5,用户ID(错),群ID")
I24_25("RtnParamErr", "10001679","10001679", "0.1", "C25-6,用户ID,群ID(错)")
I24_25("RtnParamErr", "10001679","0", "0", "C25-7,用户ID(0),群ID(0)")
I24_25("RtnParamErr", "10001679","-1", "-1", "C25-8,用户ID(负数),群ID(负数)")

print "26,================================================================================================="
# 26 红包群消息_我的红包群消息查看确认接口
# 涉及表, t_redgroup_baseinfo , lastLookUpMessageTime
I24_26("RtnOK", "10001800","2016-06-23 15:48:22", "335", "C26-1,最近一条消息时间,群ID")
I24_26("RtnParamErr", "10001800","", "", "C26-2,最近一条消息时间(空),群ID(空)")
I24_26("RtnParamErr", "10001800","2016-06-24 15:48:22", "", "C26-3,最近一条消息时间,群ID(空)")
I24_26("RtnParamErr", "10001800","", "213", "C26-4,最近一条消息时间(空),群ID")
I24_26("RtnParamErr", "10001800","1290", "213", "C26-5,最近一条消息时间(错),群ID")
I24_26("RtnParamErr", "10001800","2016-06-24 15:48:22", "0.1", "C26-6,最近一条消息时间,群ID(错)")
I24_26("RtnParamErr", "10001800","0", "0", "C26-7,最近一条消息时间(0),群ID(0)")
I24_26("RtnParamErr", "10001800","-1", "-1", "C26-8,最近一条消息时间(负数),群ID(负数)")

print "27,================================================================================================="
# # 27 红包群消息_我关注的红包群消息列表接口
I24_27("RtnOK", "10001483", "10001483","213", "10001679", "C27-1,用户ID,群ID,群主用户ID")
I24_27("RtnParamErr", "10001483", "","213", "10001679", "C27-2,用户ID(空),群ID,群主用户ID")
I24_27("RtnParamErr", "10001483", "10001483","", "10001679", "C27-3,用户ID,群ID(空),群主用户ID")
I24_27("RtnParamErr", "10001483", "10001483","213", "", "C27-4,用户ID,群ID,群主用户ID(空)")
I24_27("RtnParamErr", "10001483", "0000000","213", "10001679", "C27-5,用户ID(错),群ID,群主用户ID")
I24_27("RtnParamErr", "10001483", "10001483","000", "10001679", "C27-6,用户ID,群ID(错),群主用户ID")
I24_27("RtnParamErr", "10001483", "10001483","213", "00000000", "C27-7,用户ID,群ID,群主用户ID(错)")
I24_27("RtnParamErr", "10001483", "0.1","213", "10001679", "C27-8,用户ID(错),群ID,群主用户ID")
I24_27("RtnParamErr", "10001483", "10001483","-1", "10001679", "C27-9,用户ID,群ID(错),群主用户ID")
I24_27("RtnParamErr", "10001483", "10001483","213", "-5", "C27-10,用户ID,群ID,群主用户ID(错)")

print "28,================================================================================================="
# 28 红包群消息_我关注的红包群消息查看确认接口
# 涉及表, t_redgroup_memberinfo , lastLookUpMessageTime
I24_28("RtnOK", "10001483", "2016-06-24 10:10:37","213", "10001483", "C28-1,最近一条消息时间,群ID,用户ID")
I24_28("RtnOK", "10001483", "2016-06-24 10:10:37","0.1", "10001483", "C28-2,最近一条消息时间,群ID(错),用户ID") #不进行t_redgroup_memberinfo的修改
I24_28("RtnParamErr", "10001483", "","213", "10001483", "C28-3,最近一条消息时间(空),群ID,用户ID")
I24_28("RtnParamErr", "10001483", "2016-06-24 10:10:37","", "10001483", "C28-4,最近一条消息时间,群ID(空),用户ID")
I24_28("RtnParamErr", "10001483", "2016-06-24 10:10:37","213", "", "C28-5,最近一条消息时间,群ID,用户ID(空)")
I24_28("RtnParamErr", "10001483", "2016-06-24 10:10:37","213", "000000", "C28-6,最近一条消息时间,群ID,用户ID(错)")
I24_28("RtnSysErr", "10001483", "-1","213", "10001483", "C28-7,最近一条消息时间(错),群ID,用户ID")

print "29,================================================================================================="
# 29 账户微信充值接口
I24_29("RtnOK", "10001679", "10001679", "13", "C29-1,用户ID,充值金额（元）")
# C29-1,检查数据库t_user_withdraw新增1条且w_state=1, is_valid=1, moneyType=39, pay_type=1
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_user_withdraw where user_id = 10001679 and amount = 1300 and w_state=0 and is_valid=1 and moneyType=39 and pay_type=1')
data1 = curT.fetchone()
if data1[0]>=1:print "  => [OK,t_user_withdraw,充值成功,I24_29]"
else:print "  => [errorrrrrrrrrr,t_user_withdraw,充值失败,I24_29]"
curT.close()
conn.close()
sleep(7)

I24_29("RtnParamErr", "10001679", "10001679", "0", "C29-2,用户ID,充值金额（元）")
# C29-1,检查数据库t_user_withdraw新增1条且w_state=1, is_valid=1, moneyType=39, pay_type=1
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_user_withdraw where user_id = 10001679 and amount = 0 and w_state=2 and is_valid=1 and moneyType=39 and pay_type=1')
data1 = curT.fetchone()
if data1[0]>=1:print "  => [errorrrrrrrrrr,t_user_withdraw,充值0元,I24_29]"
else:print "  => [OK,t_user_withdraw,充值0元,I24_29]"
curT.close()
conn.close()
sleep(7)

I24_29("RtnParamErr", "10001679", "10001679", "-5", "C29-3,用户ID,充值金额（元）")
# C29-1,检查数据库t_user_withdraw新增1条且w_state=1, is_valid=1, moneyType=39, pay_type=1
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_user_withdraw where user_id = 10001679 and amount = -500 and w_state=2 and is_valid=1 and moneyType=39 and pay_type=1')
data1 = curT.fetchone()
if data1[0]>=1:print "  => [errorrrrrrrrrr,t_user_withdraw,充值-5元,I24_29]"
else:print "  => [OK,t_user_withdraw,充值-5元,I24_29]"
curT.close(), conn.close()
sleep(7)

I24_29("RtnParamErr", "10001679", "10001679", "0.001", "C29-4,用户ID,充值金额（元）")
# C29-1,检查数据库t_user_withdraw新增1条且w_state=1, is_valid=1, moneyType=39, pay_type=1
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_user_withdraw where user_id = 10001679 and amount = 0.001 and w_state=2 and is_valid=1 and moneyType=39 and pay_type=1')
data1 = curT.fetchone()
if data1[0]>=1:print "  => [errorrrrrrrrrr,t_user_withdraw,充值0.001元,I24_29]"
else:print "  => [OK,t_user_withdraw,充值0.0001元,I24_29]"
curT.close(), conn.close()
sleep(7)

varOrderId = I24_29("RtnOK", "10001679", "10001679", "90.01", "C29-5,用户ID,充值金额（元）")
# print varOrderVerifCode
# print varOrderId
# C29-1,检查数据库t_user_withdraw新增1条且w_state=1, is_valid=1, moneyType=39, pay_type=1
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select count(id) from t_user_withdraw where user_id = 10001679 and amount = 9001 and w_state=0 and is_valid=1 and moneyType=39 and pay_type=1')
data1 = curT.fetchone()
if data1[0]>=1:print "  => [OK,t_user_withdraw,充值90.01元,I24_29]"
else: print "  => [errorrrrrrrrrr,t_user_withdraw,充值90.01元,I24_29]"
curT.close(), conn.close()

print "30,================================================================================================="
# 30 账户微信充值回调接口
# 业务逻辑: 由于是模拟测试,实际没有付款,所以成功支付后微信回调会显示 "您取消了支付",表示接口已通.
I24_30("RtnOK", "10001679", "10001679", "90.01", varOrderId, "C30-1,用户ID,交易金额,交易订单号")
# 以下各类错误情况,接口未做处理,无法测试.
# I24_30("RtnOK", "10001679", "10000000", "90.01", varOrderVerifCode, varOrderId, "C30-2,用户ID(错),交易金额,交易验证码,交易订单号") #"errorcode":100003,文档中没有,返回实际账户余额
# I24_30("RtnOK", "10001679", "10001679", "4000", varOrderVerifCode, varOrderId, "C30-3,用户ID,交易金额(错),交易验证码,交易订单号")#返回实际账户余额
# I24_30("RtnOK", "10001679", "10001679", "90.01", "1m5m", varOrderId, "C30-4,用户ID,交易金额,交易验证码(错),交易订单号")#返回实际账户余额
# I24_30("RtnOK", "10001679", "10001679", "90.01", varOrderVerifCode, "wx201606270949498d02df2feb0570000000", "C30-5,用户ID,交易金额,交易验证码,交易订单号(错)")#返回实际账户余额

# 清除I24_29测试数据
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('delete from t_user_withdraw where create_time between "%s" And "%s" and user_id = 10001679 and amount = 1300 ' %(varTimeFrom,varTimeEnd))
curT.execute('delete from t_user_withdraw where create_time between "%s" And "%s" and user_id = 10001679 and amount = 9001 ' %(varTimeFrom,varTimeEnd))
conn.commit()

print "Common1,================================================================================================="
# Icommon1，塞钱进红包支付接口
# 涉及表：t_extension_channel_redpool新增1
# t_extension_channel_redPool 新增1
# t_extension_channel_redPic 新增1
# t_extension_channel 新增1
# t_operate_audit 新增1
# t_user_withdraw 新增1
# t_extension_userdeed_count 新增4
# 业务逻辑: 执行后 t_user 表中 commission_residue 金额减1元.
# 自动化逻辑: 执行前,需预判 t_user 表中账户是否有足额金额

Icommon1("RtnOK", "10001588", "3", "1", "2370", "10001588", "alibaba1", "1","1","Common1,推广来源,红包总金额,渠道推广图片ID,userid,品牌商户名称,红包总数量,door")

# Icommon1,检查 t_extension_channel_redPool 新增1条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT id,createTime from t_extension_channel_redPool  WHERE userId=10001588 and brandContent="alibaba1" order by id desc')
data1 = curT.fetchone()
# print data1[0] #1396
# print data1[1] #2016-06-29 10:26:44

# Icommon1,检查 t_extension_channel_redPic 新增1条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id) from t_extension_channel_redPic  WHERE extensionRedPoolId=%s order by id desc ' %(data1[0]))
data2 = curT.fetchone()
# print data2[0] #1
if data2[0] == 1:print "  => [OK,t_extension_channel_redPic,新增1条成功,Icommon1]"
else:print "  => [errorrrrrrrrrr,t_extension_channel_redPic,新增1条失败,Icommon1]"

# Icommon1,检查 t_extension_channel 新增1条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id) from t_extension_channel  WHERE extensionRedPoolId=%s order by id desc ' %(data1[0]))
data3 = curT.fetchone()
# print data3[0]  #1
if data3[0] == 1:print "  => [OK,t_extension_channel,新增1条成功,Icommon1]"
else:print "  => [errorrrrrrrrrr,t_extension_channel,新增1条失败,Icommon1]"

# Icommon1,检查 t_operate_audit 新增1条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id) from t_operate_audit WHERE object_id=%s and submit_user_id=10001588 order by id desc ' %(data1[0]))
data3 = curT.fetchone()
# print data3[0]  #1
if data3[0] == 1:print "  => [OK,t_operate_audit,新增1条成功,Icommon1]"
else:print "  => [errorrrrrrrrrr,t_operate_audit,新增1条失败,Icommon1]"

# Icommon1,检查 t_user_withdraw 新增1条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id) from t_user_withdraw WHERE user_id=10001588 and create_time="%s"  order by id desc '%(data1[1]))
data3 = curT.fetchone()
# print data3[0]  #1
if data3[0] == 1:print "  => [OK,t_user_withdraw,新增1条成功,Icommon1]"
else:print "  => [errorrrrrrrrrr,t_user_withdraw,新增1条失败,Icommon1]"

# Icommon1,检查 t_extension_userdeed_count 新增4条
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id) from t_extension_userdeed_count WHERE batchId=%s order by id desc '%(data1[0]))
data3 = curT.fetchone()
# print data3[0]  #4
if data3[0] == 4:print "  => [OK,t_extension_userdeed_count,新增4条成功,Icommon1]"
else:print "  => [errorrrrrrrrrr,t_extension_userdeed_count,新增4条失败,Icommon1]"

print "I24_31================================================================================================="
# # I24_31 渠道推广红包个分享渠道记录接口(新增参数)
# 涉及表, t_agent_store,t_user
# # 业务逻辑:
# 前置条件: I24_31 回调接口依赖于Icommon1接口的执行 , 因此先执行Icommon1.
# # 支付接口传入的值，需要调用一下，才能进行一下操作  返回ID ,t_extension_channel_redpool , Id = data1[0]

# 业务场景1: 10001588（普通商户） ,支付类型=3（账户余额），渠道类型=4（二维码）  预期：能发二维码
# 检查t_agent_store 商户用户 ,手机号:17000000020
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id),userId from t_agent_store WHERE phone=17000000020 and auditFlag=2')
data0 = curT.fetchone()
if data0[0] == 1:
    # print data0[1] # 10001588
    # 检查t_user 确认用户身份及金额.
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('SELECT count(id) from t_user WHERE id=%s and commission_residue>0 and rechargeAmount=0 '%(data0[1]))
    data1 = curT.fetchone()
    if data1[0] <> 1 :
        curT.execute('update t_user set commission_residue=50000 WHERE id=%s '%(data0[1]))
        curT.execute('update t_user set rechargeAmount=0 WHERE id=%s '%(data0[1]))
        conn.commit()

    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('SELECT id,createTime from t_extension_channel_redPool  WHERE userId=%s and brandContent="alibaba1" order by id desc' %(data0[1]))
    data2 = curT.fetchone()
    # print data2[0] #1396
    # print data2[1] #2016-06-29 10:26:44

    # 100=1元,支付类型=3（账户余额），渠道类型=4（二维码）,data0[1]=10001588
    I24_31("RtnOK",str(data0[1]),data2[0],data0[1],"100","3","4","alibaba1","1","1","","C31-1,用户ID,红包池id,用户ID,单位金额,支付类型(账户余额),渠道类型(二维码),品牌,层级,红包数量,红包群选择分类(新增)")

    # Icommon1,检查 t_extension_channel 新增1条
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    curT.execute('SELECT count(id) from t_extension_channel  WHERE extensionRedPoolId=%s and channel=4 order by id desc ' %(data2[0]))
    data3 = curT.fetchone()
    # print data3[0]  #1
    if data3[0] == 1:print "  => [OK,t_extension_channel,channel=4 新增1条成功,I24_31-1]"
    else:print "  => [errorrrrrrrrrr,t_extension_channel,channel=4 新增1条失败,I24_31-1]"
else: print "  => [errorrrrrrrrrr,t_agent_store,17000000020不是有效商户,I24_31-1未执行]"

sleep(10)
# 初始化 10001679, 用于 业务场景2\3\4 , 注意:抢红包是调用Icommon2接口
Icommon1("RtnOK","10001679", "3", "1", "2371","10001679", "alibaba1679", "1","1","Icommon1,推广来源,红包总金额,渠道推广图片ID,userid(10001679),品牌商户名称,红包总数量,door")

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT id,createTime from t_extension_channel_redPool  WHERE userId=10001679 and brandContent="alibaba1679" order by id desc' )
data2 = curT.fetchone()

# 业务场景2:10001679（大咖用户） ,支付类型=1（微信），渠道类型=4（二维码）
I24_31("RtnOK","10001679",data2[0],"10001679","100","1","4","alibaba1679","1","1","90","C31-2,用户ID,红包池id,用户ID(大咖),单位金额,支付类型(微信),渠道类型(二维码),品牌,层级,红包数量,红包群选择分类(新增)")

# 业务场景3:10001679（大咖用户） ,支付类型=1（微信），渠道类型=1（外平台）
I24_31("RtnOK","10001679",data2[0],"10001679","100","1","1","alibaba1679","1","1","90","C31-3,用户ID,红包池id,用户ID(大咖),单位金额,支付类型(微信),渠道类型(外平台),品牌,层级,红包数量,红包群选择分类(新增)")

# 业务场景4:10001679（大咖用户） ,支付类型=1（微信），渠道类型=3（红包群）
I24_31("RtnOK","10001679",data2[0],"10001679","100","1","3","alibaba1679","1","1","90","C31-4,用户ID,红包池id,用户ID(大咖),单位金额,支付类型(微信),渠道类型(红包群),品牌,层级,红包数量,红包群选择分类(新增)")

# 业务场景5:10001679（大咖用户）,支付类型=3（账户余额），渠道类型=1（外平台）,#备注：该用例如果支付接口的支付类型是微信，回调的支付类型是账户余额也返回成功
I24_31("RtnOK","10001679",data2[0],"10001679","100","3","1","alibaba1679","1","1","90","C31-5,用户ID,红包池id,用户ID(大咖),单位金额,支付类型(账户余额),渠道类型(外平台),品牌,层级,红包数量,红包群选择分类(新增)")


# 初始化 10001679, 用于 业务场景2\3\4 , 注意:抢红包是调用Icommon2接口
Icommon1("RtnOK","10001803", "3", "1", "2370","10001803", "alibaba1803", "1","1","Icommon1,推广来源,红包总金额,渠道推广图片ID,userid(10001803),品牌商户名称,红包总数量,door")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT id,createTime from t_extension_channel_redPool  WHERE userId=10001803 and brandContent="alibaba1803" order by id desc' )
data1 = curT.fetchone()

# 业务场景6:10001803（普通用户） ,支付类型=3（账户余额），渠道类型=1（外平台）  预期：能发送外平台
I24_31("RtnOK","10001803",data1[0],"10001803","100","3","1","alibaba1","1","1","90","C31-6,用户ID,红包池id,用户ID(普通用户),单位金额,支付类型(账户余额),渠道类型(外平台),品牌,层级,红包数量,红包群选择分类(新增)")

# 业务场景7:10001803（普通用户） ,支付类型=3（账户余额），渠道类型=2（抢红包）  预期：能发抢红包
I24_31("RtnOK","10001803",data1[0],"10001803","100","3","2","alibaba1","1","1","90","C31-7,用户ID,红包池id,用户ID(普通用户),单位金额,支付类型(账户余额),渠道类型(抢红包),品牌,层级,红包数量,红包群选择分类(新增)")

# 业务场景8:10001803（普通用户） ,支付类型=3（账户余额），渠道类型=3（红包群）  预期：能发红包群
I24_31("RtnOK","10001803",data1[0],"10001803","100","3","3","alibaba1","1","1","90","C31-8,用户ID,红包池id,用户ID(普通用户),单位金额,支付类型(账户余额),渠道类型(红包群),品牌,层级,红包数量,红包群选择分类(新增)")

# 业务场景9: 10001813普通用户 ,分享红包选 抢红包 验证
Icommon1("RtnOK","10001813", "3", "1", "2370","10001813", "alibaba1813", "1","1","Icommon1,推广来源,红包总金额,渠道推广图片ID,userid(10001813),品牌商户名称,红包总数量,door")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT id,createTime from t_extension_channel_redPool  WHERE userId=10001813 and brandContent="alibaba1813" order by id desc' )
data1 = curT.fetchone()
Icommon2("RtnOK","10001813","10001813", data1[0], "1", "3","2", "0", "alibaba1813","1","1","2","Icommon2,userId(10001813),红包池id,红包金额,支付类型,渠道类型,群分组,品牌名,层级,红包当前数量,渠道ID")

print "32,================================================================================================="
# ################以下暂不考虑
# # 业务场景9:10001803（普通用户） ,支付类型=3（账户余额），渠道类型=4（二维码）  预期：不能发二维码
# I24_31("RtnOK","10001803",data1[0],"10001803","100","3","4","alibaba1","1","1","90","C31-9,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
#
# # 业务场景10:10001679（大咖用户）,支付类型=3（账户余额），渠道类型=2（抢红包） 预期：不能发送抢红包
#
# # 业务场景11:10001679（大咖用户）,支付类型=3（账户余额），渠道类型=3（红包群） 预期：不能发送红包群
# I24_31("RtnOK","10001679",data1[0],"10001679","100","3","3","alibaba1","1","1","90","C31-11,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
# # 业务场景12:10001679（大咖用户） ,支付类型=9（无该类型），渠道类型=1（外平台）
# I24_31("RtnOK","10001679",data1[0],"10001679","100","9","1","alibaba1","1","1","90","C31-12,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
# # 业务场景13:10001679（大咖用户） ,支付类型=3（账户余额），渠道类型=20（无该渠道）
# I24_31("RtnOK","10001679",data1[0],"10001679","100","1","20","alibaba1","1","1","90","C31-13,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")


# I24_32获得红包群分类列表接口
I24_32("RtnOK","10001476","C32-1,用户ID")
I24_32("RtnOK","","C32-2,用户ID(空)")

print "33,================================================================================================="
#I24_33 红包群设置店铺链接接口
# 涉及表: t_redgroup_baseinfo,shopLink
I24_33("RtnOK","10001679","10001679","213","www.163.com","C33-1,用户ID,群ID,店铺链接")
I24_33("RtnOK","10001476","10001476","7","","C33-2,用户ID,群ID,店铺链接（空）")
I24_33("RtnParamErr","10001476","","7","http://www.baidu.com/","C33-3,用户ID(空),群ID,店铺链接")
I24_33("RtnParamErr","10001490","10001490","7","http://www.baidu.com1111/","C33-4,用户ID（错）,群ID,店铺链接")
I24_33("RtnParamErr","10001476","10001476","8","http://www.baidu.com1111/","C33-5,用户ID,群ID（错）,店铺链接")
I24_33("RtnParamErr","10001476","10001476","","http://www.baidu.com1111/","C33-6,用户ID,群ID（空）,店铺链接")
I24_33("RtnSysErr","10001476","10001476","7","阿飞似懂斯蒂芬非懂阿地方飞打发打发似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂","C33-7,用户ID,群ID（空）,店铺链接")

print "34,================================================================================================="
# #34红包群分类设置接口
I24_34("RtnOK","10001679","10001679","213","0","C34-1,用户ID,群ID,分类ID")
I24_34("RtnParamErr","10001679","","213","0","C34-2,用户ID（空）,群ID,分类ID")
I24_34("RtnParamErr","10001679","10001679","","0","C34-3,用户ID,群ID（空）,分类ID")
I24_34("RtnParamErr","10001679","10001679","8","0","C34-4,用户ID,群ID（错）,分类ID")
I24_34("RtnParamErr","10001679","10001679","7","","C34-5,用户ID,群ID,分类ID（空）")

print "35,================================================================================================="
#35获取分享内容及分享链接接口
# 涉及表 t_share,t_redgroup_message
# 前置条件依赖于 Icommon1接口,该接口是建立在支付接口与回调接口的基础上，红包池id必须继承上id
# 业务逻辑
# 接口发送成功后t_share会插入一条消息记录
# t_redgroup_message 也会插入一条数据对应的platform，红包群选择分类
Icommon1("RtnOK","10001476", "3", "1", "2370","10001476", "alibaba1476", "1","1","Icommon1,推广来源,红包总金额,渠道推广图片ID,userid(10001803),品牌商户名称,红包总数量,door")

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT id,createTime from t_extension_channel_redPool  WHERE userId=10001476 and brandContent="alibaba1476" order by id desc' )
data1 = curT.fetchone()
# print data1[0]

I24_35("RtnOK","10001476","10001476","25","1","100",data1[0],"1","100","3","1","1","alibaba1476","推广内容","1","","C35-1,用户ID,类型,分享渠道，红包总金额 ，红包池id，红包数量，单个红包金额，支付类型，渠道类型，层级，品牌名称，推广内容，红包群选择分类，品牌名称，")
I24_35("RtnOK","10001476","10001476","25","8","100",data1[0],"1","100","3","2","1","alibaba1476","推广内容","1","","C35-2,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
I24_35("RtnOK","10001476","10001476","25","10","100",data1[0],"1","100","3","2","1","alibaba1476","推广内容","1","","C35-3,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
#检测t_share新增一条
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306,use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT obj_id from ukardapp.t_share WHERE user_id=10001476 ORDER BY id DESC limit 0,1')
data2 = curT.fetchone()
if data2[0] == data1[0]:print "  => [OK,ukardapp.t_share,新增1条成功,I24_35]"
else:print "  => [errorrrrrrrrrr,ukardapp.t_share,新增1条失败,I24_35]"

I24_35("RtnParamErr","10001476","","25","1","100",data1[0],"1","100","3","1","1","alibaba1476","推广内容","1","","C35-4,用户ID（空）,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
# 用户Id不存在时,接口无判断,无法验证.
# I24_35("RtnParamErr","10001476","50001476","25","1","100",data1[0],"1","100","3","1","1","alibaba1476","推广内容","1","","C35-5,用户ID（错）,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
# 分享渠道 platform 错误时,验证不存在的
I24_35("RtnSysErr","10001476","10001476","25","11","100",data1[0],"1","10000","3","1","1","alibaba1476","推广内容","1","","C35-6,用户ID,类型,分享渠道（错）,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
I24_35("RtnOK","10001476","10001476","25","10","1",data1[0],"1","100000","3","4","1","alibaba1476","推广内容","1","","C35-7,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
# 验证已发送过二维码红包，需要上一个用例I24_35-7做铺垫，需要跑两次
I24_35("RtnSysErr","10001476","10001476","25","10","1",data1[0],"1","100000","3","4","1","alibaba1476","推广内容","1","","C35-8,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")

print "36,================================================================================================="
# I24_36用户发的红包广告统计信息接口
I24_36("RtnOK","10001476","10001476","7","0","5","C36-1,用户ID,群ID,分页开始位置,每页显示条数")
I24_36("RtnSysErr","10001476","10001476","7","0","1000000000000","C36-2,用户ID,群ID,分页开始位置,每页显示条数(错)")
I24_36("RtnParamErr","10001476","","7","0","5","C36-3,用户ID（空）,群ID,分页开始位置,每页显示条数")
I24_36("RtnDeviceErr","1000147","10001476","7","0","5","C36-4,用户ID,群ID,分页开始位置,每页显示条数")

print "37,================================================================================================="
# I24_37红包群成员_群成员排序分类
I24_37("RtnOK","10001476","C36-1,用户ID")

print "38,================================================================================================="
# I24_38红包群通讯录_获取我关注的红包群群主列表接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306,use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT count(id),groupRemark from t_redgroup_memberinfo WHERE userId=10001679 and isBlack=0')
data2 = curT.fetchone()
if data2[0] >=1:
    I24_38("RtnOK","10001679","10001679",data2[1],"C38-1,用户ID,搜索名称")
    I24_38("RtnParamErr","10001476","",data2[1],"C38-2,用户ID(空),搜索名称")
    I24_38("RtnOKNone","10001679","10001679","linghuchong123123213","C38-3,用户ID,搜索名称(错)")

else:print "  => [errorrrrrrrrrr,t_redgroup_memberinfo,没有我关注的群,I24_38]"
I24_38("RtnDeviceErr","","","","C38-4,用户ID(空),搜索名称(空)")

print "39,================================================================================================="
#I24_39我的红包群信息接口
I24_39("RtnOK","10001679","10001679","C39-1,用户ID")
I24_39("RtnSysErr","10001679","100014761","C39-2,用户ID(错)")
I24_39("RtnParamErr","10001679","","C39-3,用户ID(空)")

print "40,================================================================================================="
# I24_40 用户个人主页信息接口(新增返回值)
I24_40("RtnOK","10001679","10001679","10001679","0","C40-1,登录人用户ID,查看人用户ID,是否群主1群主/0非群主")
I24_40("RtnOK","10001476","10001476","10001800","1","C40-2,登录人用户ID,查看人用户ID,是否群主1群主/0非群主")
I24_40("RtnParamErr","","","","","C40-3,登录人用户ID(空),查看人用户ID(空),是否群主1群主/0非群主(空)")

print "41,================================================================================================="
# I24_41 红包群红点_群新成员红点接口
I24_41("RtnOK","10001476","10001476","C41-1,登录人用户ID")
I24_41("RtnParamErr","10001476","","C41-2,登录人用户ID(空)")

print "42,================================================================================================="
# I24_42 我关注的红包群分类接口
I24_42("RtnOK","10001476","10001476","C42-1,登录人用户ID")
I24_42("RtnParamErr","10001476","","C42-2,登录人用户ID(空)")

print "43,================================================================================================="
# I24_43 抢红包回调接口
# 涉及到表 t_internal_redDetail , t_redgroup_baseinfo
# redState=3表示已抢完的红包
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
# 渠道ID
curT.execute('SELECT channelId from t_internal_redDetail WHERE userId=10001476 and redState=3 ORDER BY id DESC limit 0,1')
data1 = curT.fetchone()

# 批次Id
curT.execute('SELECT batchId from t_internal_redDetail WHERE userId=10001476 and redState=3 ORDER BY id DESC limit 0,1')
data2 = curT.fetchone()

# 群Id
curT.execute('SELECT id from t_redgroup_baseinfo WHERE userId=10001476')
data3 = curT.fetchone()

# data: 1是抢完的 0是抢到的
I24_43("RtnOK","10001476","10001476",data1,data2,data3,"C43-1,登录人用户ID,渠道ID,批次ID,群Id")
I24_43("RtnParamErr","10001476","","","","","C43-2,登录人用户ID(空),渠道ID,批次ID,群Id")
I24_43("DonGrab","10001476","10001476","155556","455似懂非懂445","s斯蒂芬斯蒂芬斯蒂芬森的dfd","C43-3,登录人用户ID(),渠道ID（错）,批次ID（错）,群Id（错）")
I24_43("DonGrab","10001476","10001476",data1,data2,"1000","C43-4,登录人用户ID(),渠道ID,批次ID,群Id（错）")

print "44,================================================================================================="
# I24_44 更新进入店铺链接打开数接口
curT = conn.cursor()
curT.execute('SELECT channelId from t_internal_redDetail WHERE userId=10001476 and redState=3 ORDER BY id DESC limit 0,1')
data10 = curT.fetchone()
I24_44("RtnOK","10001476","10001476","1",data10,"C44-1,用户ID,批次ID,渠道ID")
I24_44("RtnParamErr","10001476","10001476","","","C44-2,用户ID,批次ID,渠道ID")
I24_44("RtnParamErr","10001476","","1",data10,"C44-3,用户ID,批次ID,渠道ID")

print "45,================================================================================================="
# I24_45 红包群查看分享奖励条数接口
I24_45("RtnOK","10001679","100016792","213","10001679","C45-1,用户ID,群ID,群主用户ID")
I24_45("RtnParamErr","10001800","","213","10001476","C45-2,用户ID（空）,群ID,群主用户ID")
I24_45("RtnParamErr","10001800","10001800","","10001476","C45-3,用户ID,群ID（空）,群主用户ID")
I24_45("RtnParamErr","10001800","10001800","213","","C45-4,用户ID,群ID,群主用户ID（空）")

print "46,================================================================================================="
# I24_46 发红包消息规则说明接口
I24_46("RtnOK","10001679","C46-1,无参数")

print "47,================================================================================================="
#I24_47 红包群标签_获取红包群标签(指定标签ID)接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306,use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT count(id) from t_redgroup_label WHERE groupId=213')
data1 = curT.fetchone()
if data1[0] >=1:
    conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
    curT = conn.cursor()
    if data1[0]>=2:
        a_list=[]
        curT.execute('select id from t_redgroup_label WHERE groupId=213')
        data9 = curT.fetchall()
        for i in range(len(data9)):
            for each in data9[i]:
               a_list.append(str(each))
        TestUserId47_1 = ''.join(a_list[0:1])   # 列表转字符串,获取第1个userId
        TestUserId47_2 = ''.join(a_list[1:2])   # 列表转字符串,获取第2个userId
        TestUserId47_23=TestUserId47_1 + "," + TestUserId47_2
        I24_47("RtnOK","10001679","213",TestUserId47_23,"C47-1,群ID,标签ID(2个)")

    I24_47("RtnOK","10001679","213",TestUserId47_1,"C47-2,群ID,标签ID")
    I24_47("RtnOKNone","10001679","213","42","C47-3,群ID,标签ID(错)")
    I24_47("RtnParamErr","10001679","","42","C47-4,群ID(空),标签ID(错)")
else: print "  => [errorrrrrrrrrr,t_redgroup_label,群ID=213不存在]"

print "48,================================================================================================="
# I24_48 用户发的红包广告红包详情接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306,use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT count(id),batchId from t_internal_redPool WHERE userId=10001679')
data1 = curT.fetchone()
if data1[0] >=1:
    I24_48("RtnOK","10001679",data1[1],"0","1","C48-1,批次ID,启始页,翻页")
    I24_48("RtnSysErr","10001679",data1[1],"0","","C48-2,批次ID,启始页,翻页(空)")
    I24_48("RtnOK","10001679",data1[1],"","1","C48-3,批次ID,启始页(空),翻页")
else: print "  => [errorrrrrrrrrr,t_internal_redPool,未找到对应的batchId]"
I24_48("RtnSysErr","10001679","1212121212","0","0","C48-4,批次ID(错),启始页,翻页")
I24_48("RtnParamErr","10001679","","0","0","C48-5,批次ID(空),启始页,翻页")

print "49,================================================================================================="
# # I24_49 用户发的红包广告红包详情接口（新增参数和返回值）
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306,use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT count(id),channelId from t_internal_redPool WHERE userId=10001679')
data1 = curT.fetchone()
if data1[0] >=1:
    # print data1[1]
    I24_49("RtnOK","10001679","10001679",data1[1],"0","1","C49-1,userId,channel,startIndex,pageSize")
    I24_49("RtnParamErr","10001679","",data1[1],"0","0","C49-2,userId(空),channel,startIndex,pageSize")
    I24_49("RtnSysErr","10001679","10001679","90909","0","1","C49-3,userId,channel(错),startIndex,pageSize")
    I24_49("RtnParamErr","10001679","10001679","","0","1","C49-4,userId,channel(空),startIndex,pageSize")
    I24_49("RtnSysErr","10001679","10001679",data1[1],"0","","C49-5,userId,channel,startIndex,pageSize(空)")
else: print "  => [errorrrrrrrrrr,t_internal_redPool,未找到对应的batchId,channelId]"

print "50,================================================================================================="
# I24_50 红包群_加入红包群接口（新增返回值）
# 此接口需调用i24_49接口中data1[1]
I24_50("RtnOK","10001679","10001497","213","10001679","C50-1,userId,groupid,groupUserId")
I24_50("RtnParamErr","10001679","10001497","213","","C50-2,userId,groupid,groupUserId(空)")
I24_50("RtnParamErr","10001679","10001497","","","C50-3,userId,groupid(空),groupUserId(空)")
I24_50("RtnParamErr","10001679","","213","10001679","C50-4,userId(空),groupid,groupUserId")
I24_50("RtnOK","10001588","10001588","213","10001679","C50-5,userId,groupid,groupUserId")
I24_50("RtnSysErr","10001679","60002588","213","10001679","C50-6,userId,groupid,groupUserId")

print "51,================================================================================================="
# I24_51 红包群抢红包_领取红包消息(点击领取红包炸弹时调用)接口
I24_51("RtnOK","10001679","10001679","213","13827",data1[1],"C51-1,userId,groupid,batchId(错),channelId")
I24_51("RtnParamErr","10001679","10001679","213","",data1[1],"C51-2,userId,groupid,batchId(空),channelId")
I24_51("RtnParamErr","10001679","","213","",data1[1],"C51-3,userId(空),groupid,batchId(空),channelId")
I24_51("RtnParamErr","10001679","10001679","","",data1[1],"C51-4,userId,groupid(空),batchId(空),channelId")
I24_51("RtnOK","10001679","10001679","213","0000","1234567","C51-4,userId,groupid,batchId(错),channelId(错)")

print "52,================================================================================================="
I24_52("RtnOK","10001679","10001679","213","C1-52,用户Id,群Id")
I24_52("RtnParamErr","10001679","10001679","","C1-52,用户Id,群Id(空)")
I24_52("RtnParamErr","10001679","","","C1-52,用户Id(空),群Id")
I24_52("RtnParamErr","10001679","10001679","12122","C1-52,用户Id,群Id(错)")

# **********************************************************************************************
# 接口应用
# # # 批量生成多个标签的用户
# alist=[10001575,10001593,10001588,10001589,10001587]
# for i in alist:
#     print i
#     I24_3("RtnOK","10001482","10001482","13","xlq"+varTimeYMDHSM,i,"C3-1,用户ID,群ID,标签名称,标签成员ID(1个)")
#     sleep(1)
#     varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S');
# sleep(12121221)
