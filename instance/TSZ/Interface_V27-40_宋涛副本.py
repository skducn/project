# coding: utf-8
#****************************************************************
# Author     : John
# Version    : V 2.5.0
# Date       : 2016-7
# Description: 三藏红包 app接口文档
#****************************************************************

import sys,requests,redis,MySQLdb,random,datetime,time
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


def Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, **query):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    query1 = {}
    for x in query:
        query1[x] = str(query[x])
    query1["verifyUserId"] = varuserId
    query1["verifyCode"] = varverifyCode
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=query1)
    try:
        if varnum == "RtnNullOK":  # 如:{"data":null,"errorstr":"","errorcode":0,"success":true}
            if response.json()['success'] == True:
                print "[OK,RtnNullOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnNullOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnOK":  # 如:{"data":149,"errorstr":"","errorcode":0,"success":true}
            if response.json()['success'] == True and len(str(response.json()['data'])) > 0:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnNoDATAOK":  # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
            if response.json()['success'] == True and response.json()['data'] == []:
                print "[OK,RtnNoDATAOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnNoDATAOK]," + varInterfaceName + " => " + testcase + " => " + response.content
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
        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnParamErr1":
            if response.json()['errorcode'] == 1 and response.json()['success'] == False:
                print "[OK,RtnParamErr1]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr1]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"



#发普通红包接口
def I25_21(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    ########################################################################
    varInterfaceName =  "I21,红包群_我的红包群_发普通红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"groupId":param1,"cityId":param2,"brandContent":param3
        ,"redNumber":param4,"amount":param5,"payType":param6,"payPwd":param7,"templateId":param8,"userId":param9}
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

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"



#发普通红包设置标签接口
def I25_22(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    ########################################################################
    varInterfaceName =  "I22,红包群_我的红包群_发普通红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed_auth.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"batchId":param3
        ,"channelId":param4,"labelId":param5}
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

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"



#发拼手气红包接口
def I25_24(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    ########################################################################
    varInterfaceName ="I24,红包群_我的红包群_发拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuckRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"groupId":param1,"cityId":param2,"brandContent":param3
        ,"redNumber":param4,"amount":param5,"payType":param6,"payPwd":param7,"templateId":param8,"userId":param9}
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

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"


#发拼手气红包设置标签接口
def I25_25(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    ########################################################################
    varInterfaceName ="I25,红包群_我的红包群_发拼手气红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuck_auth.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "groupId": param2,
                   "batchId": param3, "channelId": param4, "labelId": param5}
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

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"



#如果是新用户没有模版就需要调用保存模版接口
def I25_12(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, templateType= 模板, title=标题,brandContent=品牌,extensionSub=推广内容,extensionUrl=推广链接,videoUrl=视频链接,picFlag=添加图文标记,picUrls=图片链接（逗号表达式）,
    # templateId=模板id（没有修改，不需要传递）

    ########################################################################
    varInterfaceName =  "I25_12,红包模板_保存红包模板"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/saveTemplateInfo.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"templateType":param2,"title":param3,"brandContent":param4,
                   "extensionSub":param5,"extensionUrl":param6,"videoUrl":param7,"picFlag":param8,"picUrls":param9,"templateId":param10}
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

#广告红包发送接口
def I25_33(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    # userId = 用户Id(必填)
    # amount = 红包总金额（元）(必填)
    # count＝红包数量(必填)
    # payType ＝ 支付类型
    # door =   1首页进入 2红包再发一次
    # type ＝ 资金类型
    # cityId ＝ 城市编码
    # groupId ＝ 群id(必填)
    # templateId ＝ 模板id(必填)
    ########################################################################
    varInterfaceName =  "I33,发红包_广告红包发送接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeGetOrderNew.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"amount":param2,"count":param3
        ,"payType":param4,"door":param5,"type":param6,"cityId":param7,"groupId":param8,"templateId":param9,"payPwd":param10,"redPoolId":param11}
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

#抢普通红包接口
def I25_27(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，messageId = 消息ID，groupId = 群Id，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName =  "I27,红包群_我关注的红包群_抢普通红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robCommonRed/2.5/rob_commonRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"messageId":param2,"groupId":param3
        ,"batchId":param4,"channelId":param5}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK":
            if response.json()['success']==True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr":
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr":
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"

#抢拼手气红包接口
def I25_28(varnum, varuserId, param1, param2, param3, param4, param5, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，messageId = 消息ID，groupId = 群Id，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName = "I28,红包群_我关注的红包群_抢拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robFightLuckRed/2.5/rob_fightLuck_Red.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "messageId": param2,
                   "groupId": param3, "batchId": param4, "channelId": param5}
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

#29抢广告红包接口
def I25_29(varnum, varuserId, param1, param2, param3, param4, param5, testcase):
    # type: (object, object, object, object, object, object, object, object) -> object
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，messageId = 消息ID，groupId = 群Id，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName = "I29,红包群_我关注的红包群_抢广告红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/rob_advertRed.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "messageId": param2,
                   "groupId": param3, "batchId": param4, "channelId": param5}
    print  querystring
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

#30红包群_我关注的红包群_领取广告红包消息接口
def I25_30(varnum, varuserId, param1, param2, param3, param4, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，groupId = 群ID，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName = "I29,红包群_我关注的红包群_领取广告红包消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/redGroup_robRed_receive.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "groupId": param2,
                   "batchId": param3, "channelId": param4}
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

# 31红包群_我关注的红包群_抢广告红包回调接口
def I25_31(varnum, varuserId, param1, param2, param3, param4, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，groupId = 群ID，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName = "31,红包群_我关注的红包群_抢广告红包回调接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/redGroup_robRed_callback.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "groupId": param2,"batchId": param3, "channelId": param4}
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

# 32红包群_我关注的红包群_查看是否还有可抢红包接口
def I25_32(varnum, varuserId, param1, param2, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，channelId = 批次ID
    ########################################################################
    varInterfaceName = "32,红包群_我关注的红包群_查看是否还有可抢红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robFightLuckRed/2.5/is_red.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "channelId": param2}
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

# 34发红包_微信支付用户回调接口
def I25_34(varnum, varuserId, param1, param2, param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，redPoolId = 红包批次id，payOrderId = 订单编号
    ########################################################################
    varInterfaceName = "34，发红包_微信支付用户回调接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeOrderReturnNew.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "redPoolId": param2,"payOrderId": param3}
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

# 35发红包_红包充值接口
def I25_35(varnum, varuserId, param1, param2, param3,param4, param5, param6, param7, param8, param9, param10,param11,param12, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，amount = 红包总金额，count = 红包数量，payType = 支付类型，door = 入口标记，
    # type = 资金类型，cityId = 城市编码，groupId = 群id，templateId = 模板id，qrFlag = 是否是二维码充值，redPoolId = 批次id，payPwd = 支付密码
    ########################################################################
    varInterfaceName = "35,发红包_红包充值接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/advertApprentice.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                   "amount": param2, "count": param3, "payType": param4, "door": param5, "type": param6, "cityId": param7,
                   "groupId": param8, "templateId": param9, "qrFlag": param10, "redPoolId": param11, "payPwd": param12}
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



def I25_36(varnum, varuserId, param1, param2, param3, param4, testcase):
    varInterfaceName = "I25_36,红包列表_红包放入红包池、余额回收接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/redpackCallBack.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, callBackType=param2, redPoolId=param3,
             redType=param4)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，callBackType = 回收类型，redPoolId = 批次号，redType = 红包类型


def I25_37(varnum, varuserId, param1, param2, param3, testcase):
    varInterfaceName = "I25_37,我的_个人信息接口（新增返回值）"
    varUrl = "http://192.168.2.176:9999/WebBusi/personalHomePage/2.2/homePage_info.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, visitUserId=param2,isGroup=param3)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，visitUserId = 访问人id，isGroup = 是否群主，1是，0否


def I25_38(varnum, varuserId, param1, param2, param3, param4, param5, param6, param7, param8, testcase):
    varInterfaceName = "I25_38,首页_发红包_私信红包_发送私信红包接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_red.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, payType=param2, amount=param3,acceptId=param4, groupId=param5,
             content=param6, payPwd=param7, templateId=param8)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，payType = 支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡)，amount = 红包金额，
    # acceptId = 红包金额，groupId=群ID，content=信息内容(可选)，payPwd=付密码(可选,支付类型3、5必传)，templateId =模板ID(可选)

def I25_39(varnum, varuserId, param1, param2, param3, param4, param5, param6, param7, testcase):
    varInterfaceName = "I25_39,首页_发红包_私信红包_发送私信转帐接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_transfer.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, payType=param2, amount=param3,
             acceptId=param4, groupId=param5,content=param6, payPwd=param7)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，payType = 支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡)，amount = 红包金额，
    # acceptId = 红包金额，groupId=群ID，content=信息内容(可选)，payPwd=付密码(可选,支付类型3、5必传)


def I25_40(varnum, varuserId, param1, param2, param3, param4, param5, param6, param7,param8,param9, testcase):
    varInterfaceName = "I25_40,分享红包_获取分享链接接口"
    varUrl = "http://192.168.2.176:9999/payment/share/1.0/get_share_url.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase,userId=param1,shareType=param2,platform=param3,
             amount=param4,tranId=param5,channel=param6,channelId=param7,lvl=param8,labelIds=param9)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，shareType = 分享类型，20app分享,25红包分享，platform = 分享渠道，1：新浪微博 2：腾讯微博 3：微信好友 4：微信朋友圈 5：短信 6：qq好友 7：qq空间，
    # amount = 金额，tranId=批次id，channel=渠道类型1外平台,2红包池，3红包群,4二维码，channelId=渠道id，lvl=层次id，1一级，2二级,id，labelIds=红包群标签，逗号表达式

def I25_44(varnum, varuserId, param1, testcase):
    varInterfaceName = "I25_44,广告红包分成_同城红包生成批处理接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redPacketBuilder/2.2/city_redPacket.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase,userId=param1)



##发普通红包接口
I25_21("RtnOK","10001588","118","3101000000","红包标题","5","0.5","4","111111","","10001588","C21-1,userId,payType,cityId,payPwd,groupId,redNumber,amount,brandContent,templateId")

##发普通红包设置标签接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
conn.commit()
I25_22("RtnOK","10001588","10001588","118",data1,data2,"0","C22-1,userId,groupId,batchId,channelId,labelId")

##发拼手气红包接口
I25_24("RtnOK","10001588","118","3101000000","红包标题","5","2.5","4","111111","","10001588", "C24-1,userId,groupId,cityId,brandContent,redNumber,amount,payType")

##发拼手气红包设置标签接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
conn.commit()
sleep(10)  #########################################整体后需要放开#############################################################
I25_25("RtnOK","10001588","10001588","118",data1,data2,"0","C25-1,userId,groupId,batchId,channelId,labelId")


#27红包群_我关注的红包群_抢普通红包接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
conn.commit()
I25_27("RtnOK","10001801","10001801",data3,"118",data1,data2, "C27-1,userId,messageId,groupId,batchId,channelId")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id),id from ukardweb.t_external_redDetail WHERE belongId=10001801 and redState=3 and redType=32 and batchId=%s' %(data1[0]))
data4 = curT.fetchone()
if data4[0]==1:print "  => [Ok,t_external_redDetail数据库记录新增1条成功并且10001801领取成功,C27-1]"
else:print "  => [errorrrrrrrrrr,t_external_redDetail数据库记录新增1条失败且领取失败,C27-1]"

I25_27("RtnParamErr","10001801","",data3,"118",data1,data2, "C27-2,userId(空),messageId,groupId,batchId,channelId")
I25_27("RtnParamErr","10001801","10001801","","118",data1,data2, "C27-3,userId,messageId（空),groupId,batchId,channelId")
I25_27("RtnParamErr","10001801","10001801",data3,"118",'',data2, "C27-4,userId,messageId,groupId,batchId(空),channelId")
I25_27("RtnParamErr","10001801","10001801",data3,"118",data1,'', "C27-5,userId,messageId,groupId,batchId,channelId(空)")
I25_27("RtnDeviceErr","","",data3,"118",data1,data2, "C27-6,userId（空）,messageId,groupId,batchId,channelId(空)")
#黑名单用户
I25_27("RtnOK","10001813","10001813",data3,"118",data1,data2, "C27-7,userId,messageId,groupId,batchId,channelId")

# 28红包群_我关注的红包群_抢拼手气红包接口
#调用一下
I25_24("RtnOK","10001588","118","3101000000","红包标题","5","2.5","4","111111","","10001588", "C24-1,userId,groupId,cityId,brandContent,redNumber,amount,payType")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
conn.commit()
sleep(10)  #########################################整体后需要放开#############################################################
I25_25("RtnOK","10001588","10001588","118",data1,data2,"0","C25-1,userId,groupId,batchId,channelId,labelId")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
I25_28("RtnOK","10001801","10001801",data3,"118",data1,data2, "C28-1,userId,messageId,groupId,batchId,channelId")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT count(id),id from ukardweb.t_external_redDetail WHERE belongId=10001801 and redState=3 and redType=33 and batchId=%s' %(data1[0]))
data4 = curT.fetchone()
if data4[0]==1:print "  => [Ok,t_external_redDetail数据库记录新增1条成功并且10001801领取成功,C27-1]"
else:print "  => [errorrrrrrrrrr,t_external_redDetail数据库记录新增1条失败且领取失败,C27-1]"
I25_28("RtnParamErr","10001801","",data3,"118",data1,data2, "C28-2,userId(空),messageId,groupId,batchId,channelId")
I25_28("RtnParamErr","10001801","10001801","","118",data1,data2, "C28-3,userId,messageId（空),groupId,batchId,channelId")
I25_28("RtnParamErr","10001801","10001801",data3,"118",'',data2, "C28-4,userId,messageId,groupId,batchId(空),channelId")
I25_28("RtnParamErr","10001801","10001801",data3,"118",data1,'', "C28-5,userId,messageId,groupId,batchId,channelId(空)")
I25_28("RtnDeviceErr","","",data3,"118",data1,data2, "C28-6,userId（空）,messageId,groupId,batchId,channelId(空)")
#黑名单用户
I25_28("RtnOK","10001813","10001813",data3,"118",data1,data2, "C28-7,userId,messageId,groupId,batchId,channelId")

##新用户没有模版就需要调用一下，老用户有模版就不需要
# #I25_12("RtnOK","10001588","10001588","1","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-1,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")

#33发红包_广告红包发送接口
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
#连续执行会提示重复提交
sleep(5)
I25_33("RtnParamErr","10001588","10001588","1","100000","0.01","1","0","3101000000","0","31","111111","0","C33-2,userId,amount,count(错误),payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnDeviceErr","10001588","","1","1","0.01","1","0","3101000000","0","31","111111","0","C33-3,userId（空）,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr","10001588","10001588","","1","3","1","0","3101000000","0","31","111111","0","C33-4,userId,amount（空）,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr","10001588","10001588","1","-1","3","1","0","3101000000","0","31","111111","0","C33-5,userId,amount,count（负数）,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "2", "3", "100", "3101000000", "0", "31", "111111", "0","C33-6,userId,amount,count,payType（错不在数据类型范围内）,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "", "111111", "0","C33-7,userId,amount,count,payType,door,cityId,groupId,templateId（空）,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31", "", "0","C33-8,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（空）,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31", "", "0","C33-9,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（错）,redPoolId,")
sleep(5)
I25_33("RtnOK", "10001588", "10001588", "1", "2", "3", "2", "0", "3101000000", "0", "31", "111111", "3452","C33-10,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（错）,redPoolId,")


#29红包群_我关注的红包群_抢广告红包接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
I25_29("RtnOK", "10001877", "10001877","123", "118", data1, data2,"C29-1,userId,messageId,groupId,batchId,channelId,")
I25_29("RtnParamErr", "10001877", "","123", "118", data1, data2,"C29-2,userId(空),messageId(groupId,batchId,channelId,")
I25_29("RtnParamErr", "10001877", "10001877","123", "", data1, data2,"C29-3,userId,messageId,groupId（空）,batchId,channelId,")
I25_29("RtnParamErr", "10001877", "10001877","123", "118", "", data2,"C29-4,userId,messageId,groupId,batchId(空),channelId,")
I25_29("RtnParamErr", "10001877", "10001877","123", "118", data1, "","C29-5,userId,messageId,groupId,batchId,channelId（空）,")


#30红包群_我关注的红包群_领取广告红包消息接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
I25_30("RtnOK", "10001877", "10001877","118", data1, data2,"C30-1,userId,groupId,batchId,channelId,")
I25_30("RtnParamErr", "10001877", "","118", data1, data2,"C30-2,userId,groupId,batchId,channelId,")
I25_30("RtnParamErr", "10001877", "10001877","", data1, data2,"C30-3,userId,groupId（空）,batchId,channelId,")
I25_30("RtnParamErr", "10001877", "10001877","119", "", data2,"C30-4,userId,groupId,batchId(空),channelId,")
I25_30("RtnParamErr", "10001877", "10001877","119", data1, "","C30-5,userId,groupId,batchId,channelId(空),")

#31红包群_我关注的红包群_抢广告红包回调接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
I25_31("RtnOK", "10001877", "10001877","118",data1,data2 ,"C31-1,userId,groupId,batchId,channelId,")
I25_31("RtnParamErr", "10001877", "","118",data1,data2 ,"C31-2,userId（空）,groupId,batchId,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","",data1,data2 ,"C31-3,userId,groupId（空）,batchId,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","",data1,data2 ,"C31-4,userId,groupId,batchId（空）,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","118","",data2 ,"C31-5,userId,groupId,batchId（空）,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","118",data1,"" ,"C31-6,userId,groupId,batchId,channelId（空）,")


#32红包群_我关注的红包群_查看是否还有可抢红包接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
I25_32("RtnOK", "10001877", "10001877",data2,"C32-1,userId,channelId,")
I25_32("RtnParamErr", "10001877", "10001877","","C32-2,userId,channelId(空),")


#34发红包_微信支付用户回调接口  ##################该接口正常业务无法正常测试####################
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT pay_order_id  from ukardweb.t_user_withdraw WHERE user_id=10001588 and object_id=%s' %(data1[0]))
data2 = curT.fetchone()
#首先要发红包微信支付
sleep(10)
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
I25_34("RtnParamErr", "10001588", "10001588",data1,data2,"C34-1,userId,redPoolId,payOrderId")
I25_34("RtnParamErr", "10001588", "10001588","","","C34-1,userId,redPoolId,payOrderId空)")
I25_34("RtnParamErr", "10001588", "10001588","",data2,"C34-1,userId,redPoolId（空）,payOrderId")

#35发红包_红包充值接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
conn.commit()
I25_35("RtnOK", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1, "111111","C35-1,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# #本人应无法给别人红包充值已修复
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", "3680", "111111","C35-2,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1, "111111","C35-3,userId（空）,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId（别人的红包批次）,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "", "2", "3", "1", "0", "3101000000", "0", "31","0", data1, "111111","C35-4,userId,amount（空）,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "-1", "3", "1", "0", "3101000000", "0", "31","0", data1, "111111","C35-5,userId,amount,count（负数）,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "", "1", "0", "3101000000", "0", "31","0", data1, "111111","C35-6,userId,amount,count,payType（空）,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", "", "111111","C35-7,userId,amount,count,payType（空）,door,cityId,groupId,templateId,qrFlag,redPoolId（空）,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1, "","C35-8,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd(错),")

#36红包列表_红包放入红包池、余额回收接口
#先生成一个广告红包做铺垫怕影响到别的接口
sleep(10)
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,推广来源,红包总金额,渠道推广图片ID,userid,品牌商户名称,红包总数量,door")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
#回收余额需要先修改红包主表updateTime
curT.execute('UPDATE t_extension_channel_redPool set updateTime=ADDDATE(NOW(),2) WHERE id=%s'%(data1[0]))
conn.commit()

#激活同城红包
I25_44("RtnOK", "10001588", "10001588","C44-1,userId")
#放入红包池目前不用测试了，下个版本没有了
I25_36("RtnOK", "10001588", "10001588","2",data1[0],"34","C36-1,userId,callBackType,redPoolId,redType")
I25_36("RtnParamErr", "10001588", "","2",data1[0],"34","C36-2,userId(空),callBackType,redPoolId,redType")
I25_36("RtnParamErr", "10001588", "10001588","",data1[0],"34","C36-2,userId,callBackType（空）,redPoolId,redType")
I25_36("RtnParamErr", "10001588", "10001588","9",data1[0],"34","C36-2,userId,callBackType（不在回收范围内的类型）,redPoolId,redType")
########别人的批次的ID问题以修复
I25_36("RtnParamErr", "10001588", "10001588","2","3485","34","C36-2,userId,callBackType,redPoolId（别人的批次ID）,redType")
I25_36("RtnParamErr", "10001588", "10001588","2","","34","C36-2,userId,callBackType,redPoolId(空),redType")
I25_36("RtnOK", "10001588", "10001588","2",data1[0],"33","C36-2,userId,callBackType,redPoolId,redType（不匹配用户批次的类型）")


#37我的_个人信息接口（新增返回值）
I25_37("RtnOK", "10001588", "10001588","10001877","1","C37-1,userId,visitUserId,isGroup")
I25_37("RtnOK", "10001588", "10001588","10001877","0","C37-2,userId,visitUserId,isGroup")
I25_37("RtnParamErr", "10001588", "","10001877","0","C37-3,userId（空）,visitUserId,isGroup")
I25_37("RtnParamErr", "10001588", "10001588","","0","C37-4,userId,visitUserId（空）,isGroup")
I25_37("RtnParamErr", "10001588", "10001588","10001877","","C37-5,userId,visitUserId,isGroup（空）")


#38首页_发红包_私信红包_发送私信红包接口
I25_38("RtnOK", "10001588", "10001588", "3", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-1,userId,payType,amount,""acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnDeviceErr", "10001588", "", "3", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-2,userId（空）,payType,amount,""acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-3,userId,payType（空）,amount,""acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-4,userId,payType,amount（空）,acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "-1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-5,userId,payType,amount（负数）,acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-6,userId,payType,amount,acceptId（不是群成员）,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "", "10001588给10001588发送私信红包1", "111111", "",
       "C38-7,userId,payType,amount,acceptId,groupId（空）,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "119", "10001588给10001588发送私信红包1", "111111", "",
       "C38-8,userId,payType,amount,acceptId,groupId（不匹配的群ID）,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "119", "10001588给10001588发送私信红包1", "", "",
       "C38-9,userId,payType,amount,acceptId,groupId,content,payPwd(空),templateId ")

#39发送私信转帐接口
I25_39("RtnOK","10001588","10001588","3","1","10001877","118","10001588给10001877发送私信转账1元","111111",
       "C39-1,userId,payType,amount,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnDeviceErr", "10001588", "", "3", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId（空）,payType,amount,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId,payType（空）,amount,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId,payType,amount（空）,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "-1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId,payType,amount（负数）,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "1", "10001588", "118", "10001588给10001588发送私信转账1元", "111111",
       "C39-1,userId,payType,amount,acceptId（不是群成员的成员）,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "",
       "C39-1,userId,payType,amount,acceptId,groupId,content,payPwd（错误）,templateId ")

#40分享红包_获取分享链接接口
sleep(10)
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT pay_order_id  from ukardweb.t_user_withdraw WHERE user_id=10001588 and object_id=%s' %(data1[0]))
data2 = curT.fetchone()
conn.commit()

I25_40("RtnOK", "10001588", "10001588", "20", "7", "1", data1[0],"2" ,data2[0], "1","0",
       "C40-1,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnOK", "10001588", "10001588", "25", "7", "1", data1[0], "2", data2[0], "1", "0",
       "C40-2,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", data2[0], "1", "0",
       "C40-3,userId,shareType（不在范围内的类型）,platform,amount,tranId,channel,channelId,lvl,labelIds")


I25_40("RtnParamErr1", "10001588", "10001588", "60", "70", "1", data1[0], "2", data2[0], "1", "0",
       "C40-4,userId,shareType,platform（不在分享渠道内）,amount,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "", data1[0], "2", data2[0], "1", "0",
       "C40-5,userId,shareType,platform,amount（空）,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "-1", data1[0], "2", data2[0], "1", "0",
       "C40-6,userId,shareType,platform,amount（负数）,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnOK", "10001588", "10001588", "20", "7", "1", "3547", "2", data2[0], "1", "0",
       "C40-4,userId,shareType,platform,amount,tranId（不是自己的批次）,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "", data2[0], "1", "0",
       "C40-7,userId,shareType,platform,amount,tranId,channel（空）,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "1", "0",
       "C40-8,userId,shareType,platform,amount,tranId,channel,channelId(不是自己的渠道ID),lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "3", "0",
       "C40-9,userId,shareType,platform,amount,tranId,channel,channelId,lvl(超过层级范围),labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "3", "",
       "C40-10,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds（空）")