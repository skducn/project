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


# 1,首页_发红包炸弹_设置广告内容问号接口
# 2,APP登录接口
# 3,我_设置_点击授权，找回红包_第三方绑定接口
# 4,首页_发红包_私信红包_获取用户私信初始金额接口
# 5,首页_发红包_私信红包_私信内容列表接口
# 6,我_设置_提现密码_获取设置提现密码验证码
# 7,我_设置_提现密码_保存提现密码接口
# 8,我_设置_提现密码_修改提现密码接口
# 9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)
# 10,红包模板_红包类型列表
# 11,红包模板_红包模板列表
# 12,红包模板_保存红包模板
# 13,红包模板_删除红包模板

# 14,首页_红包群_我的红包群私信详情接口(新增返回值)
# 15,首页_红包群_我的红包群_领私信转账接口
# 16,首页_红包群_我的红包群_转账详情接口
# 17,私首页_红包群_我的红包群_重新发送私信转账接口
# 18,首页_红包群_我的红包群_私信转账退回接口
# 19,首页_红包群_我的红包群_领私信红包接口
# 20,首页_红包群_我的红包群_私信红包详情接口
# 21,红包群_我的红包群_发普通红包接口
# 22,红包群_我的红包群_发普通红包设置标签接口
# 23,红包群_我的红包群_取消发普通红包接口
# 24,红包群_我的红包群_发拼手气红包接口
# 25,红包群_我的红包群_发拼手气红包设置标签接口
# 26,红包群_我的红包群_取消发拼手气红包接口

# 27,发红包_广告红包发送接口
# 28,发红包_微信支付用户回调接口
# 29,发红包_红包充值接口
# 30,红包列表_红包放入红包池、余额回收接口
# 31,发红包_微信支付用户回调接口
# 32,发红包_红包充值接口
# 33,红包列表_红包放入红包池、余额回收接口
# 34,我的_个人信息接口（新增返回值）
# 35,首页_发红包_私信红包_发送私信红包接口
# 36,首页_发红包_私信红包_发送私信转帐接口
# 37,我的_个人信息接口（新增返回值）
# 38,首页_发红包_私信红包_发送私信红包接口
# 39,首页_发红包_私信红包_发送私信转帐接口
# 40,分享红包_获取分享链接接口

# Icommon3 ,获取验证码接口
def Icommon3(param1,param2):
    # 参数: type=1 获取登录验证码 , 2 提现验证码 , 4=设置提现密码  ;mobileNum=手机号
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
    querystring = {"type":param1,"mobileNum":param2}
    headers = {'cache-control': "no-cache"}
    requests.request("GET", varUrl, headers=headers, params=querystring)
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    ########################################################################
    #"Icommon3,获取验证码接口"
    if param1=="1":
        varVerifyCode = r.get("app_login_" + str(param2))
        print param2 +" 验证码: " + varVerifyCode
        return varVerifyCode
    elif param1 =="4":
        varVerifyCode = r.get("app_withdrawCode_" + str(param2))
        print param2 +" 验证码: " + varVerifyCode
        return varVerifyCode


def I25_1(varnum,varuserId,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: 无
    ########################################################################
    varInterfaceName =  "I25_1,首页_发红包炸弹_设置广告内容问号接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/appDesc/2.5/get_ad_red_url.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode}
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
def I25_2(varnum,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    # r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    # varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: phone = 手机号, cityId=城市ID, channelId= 下载渠道 , channel = 渠道(0手机/1微信/2QQ/3微博),nickName=第三方昵称(可选),
    # headPic=第三方头像(可选),token=第三方token(可选),unionId=微信唯一标识(可选,微信时必传) ,password =验证码
    ########################################################################
    varInterfaceName =  "I25_2,APP登录接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.5/login.do"
    querystring = {"phone":param1,"cityId":param2,"channelId":param3,"channel":param4,"nickName":param5,"headPic":param6,"token":param7,"unionId":param8,"password":param9}
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
def I25_3(varnum,varuserId,param1,param2,param3,param4,param5,param6,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
    # varid = r2.hget("t_redgroup_baseinfo:"+varuserId,"id")
    # 参数: userId = 用户ID, channel = 渠道(0手机/1微信/2QQ/3微博), labelName = 绑定第三方名称 , belongThumb=绑定第三方头像(可选) , openId=第三方标识(微信传 unionId)
    ########################################################################
    varInterfaceName =  "I25_3,我_设置_点击授权，找回红包_第三方绑定接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.5/bindUserThirdInfo.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"channel":param2,"labelName":param3,"belongThumb":param4,"openId":param5,"cityId":param6}
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
def I25_4(varnum,varuserId,param1,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID
    ########################################################################
    varInterfaceName =  "I25_4,首页_发红包_私信红包_获取用户私信初始金额接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_init_amount.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1}
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
def I25_5(varnum,varuserId,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: 无
    ########################################################################
    varInterfaceName =  "I25_5,首页_发红包_私信红包_私信内容列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_content_list.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode}
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
def I25_6(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验证用户ID, mobileNum = 手机号, type=类型(1：动态密码 2：提现验证码 4:设置提现密码)
    ########################################################################
    varInterfaceName =  "I25_6,我_设置_提现密码_获取设置提现密码验证码"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"mobileNum":param2,"type":param3}
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
def I25_7(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验证用户ID, phone = 手机号, curPwd=当前密码 ,mobileCode= 验证码
    ########################################################################
    varInterfaceName =  "I25_7,我_设置_提现密码_保存提现密码接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/withdraw/2.5/save_withdraw_pwd.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"phone":param2,"curPwd":param3,"mobileCode":param4}
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
def I25_8(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验证用户ID, oldPwd = 原始密码, curPwd=当前密码
    ########################################################################
    varInterfaceName =  "I25_8,我_设置_提现密码_修改提现密码接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/withdraw/2.5/update_withdraw_pwd.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"oldPwd":param2,"curPwd":param3}
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
def I25_9(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, groupId= 群ID, startIndex=分页开始位置 ,pageSize=每页显示条数
    ########################################################################
    varInterfaceName =  "I25_9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupSta/2.2/user_redAdvert_statistics.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"startIndex":param3,"pageSize":param4}
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
def I25_10(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: 无
    ########################################################################
    varInterfaceName =  "I25_10,红包模板_红包类型列表"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/getRedPacketTypeList.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"templateType":param2}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']==True and len(response.json()['data'])>0:
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
def I25_11(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, templateType= 模板, startIndex=分页开始位置 ,pageSize=每页显示条数
    ########################################################################
    varInterfaceName =  "I25_11,红包模板_红包模板列表"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/getTemplateList.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"templateType":param2,"startIndex":param3,"pageSize":param4}
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
def I25_13(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, templateId = 模版ID
    ########################################################################
    varInterfaceName =  "I25_13,红包模板_删除红包模板"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/delTemplateInfo.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"templateId":param2}
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

def I25_14(varnum,varuserId,param1,param2,param3,param4,param5,param6,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, groupId= 群ID, startIndex=分页开始位置 ,pageSize=每页显示条数 ,acceptId=收件人ID ,isGroup=是否为群主(0:否,1:是)
    ########################################################################
    varInterfaceName =  "I25_14,首页_红包群_我的红包群私信详情接口(新增返回值)"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivate/2.2/user_private_detail.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"templateType":param2,"startIndex":param3,"pageSize":param4,"acceptId":param5,"isGroup":param6}
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
def I25_15(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName =  "I25_15,首页_红包群_我的红包群_领私信转账接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_lead_transfer.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"redId":param2}
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
def I25_16(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName =  "I25_16,首页_红包群_我的红包群_转账详情接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_transfer_detail.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"redId":param2}
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
def I25_17(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName =  "I25_17,私首页_红包群_我的红包群_重新发送私信转账接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_transfer_resend.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"redId":param2}
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
def I25_18(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName =  "I25_18,首页_红包群_我的红包群_私信转账退回接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_transfer_return.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"redId":param2}
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
def I25_19(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName =  "I25_19,首页_红包群_我的红包群_领私信红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_lead_red.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"redId":param2}
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
def I25_20(varnum,varuserId,param1,param2,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName =  "I25_20,首页_红包群_我的红包群_私信红包详情接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_red_detail.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"verifyUserId":param1,"redId":param2}
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
def I25_21(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: groupId = 群id, cityId=城市ID, brandContent= 标题 , redNumber = 红包个数 ,redAmount=红包单个金额(单位:元),
    # payType=支付类型(1 微信，2 支付宝，3 余额),payPwd=支付密码（可选）, payType=3时，(必选),templateId=模板ID（可选）
    ########################################################################
    varInterfaceName =  "I25_21,红包群_我的红包群_发普通红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"groupId":param1,"cityId":param2,"brandContent":param3
        ,"redNumber":param4,"redAmount":param5,"payType":param6,"payPwd":param7,"templateId":param8}
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
def I25_22(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    ########################################################################
    varInterfaceName =  "I25_22,红包群_我的红包群_发普通红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed.do"
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
    except Exception,data:
        print Exception,":",data,"\n"
def I25_23(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    ########################################################################
    varInterfaceName =  "I25_23,红包群_我的红包群_取消发普通红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/cancel_send_commonRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"batchId":param3
        ,"channelId":param4}
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
def I25_24(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: groupId = 群id, cityId=城市ID, brandContent= 标题 , redNumber = 红包个数 ,redSumAmount=红包单个金额(单位:元),
    # payType=支付类型(1 微信，2 支付宝，3 余额),payPwd=支付密码（可选）, payType=3时，(必选),templateId=模板ID（可选）
    ########################################################################
    varInterfaceName =  "I25_24,红包群_我的红包群_发拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuckRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"groupId":param1,"cityId":param2,"brandContent":param3
        ,"redNumber":param4,"redSumAmount":param5,"payType":param6,"payPwd":param7,"templateId":param8}
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
def I25_25(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    ########################################################################
    varInterfaceName =  "I25_25,红包群_我的红包群_发拼手气红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuck_auth.do"
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
    except Exception,data:
        print Exception,":",data,"\n"
def I25_26(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    ########################################################################
    varInterfaceName =  "I25_26,红包群_我的红包群_取消发拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/cancel_fightLuckRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"batchId":param3
        ,"channelId":param4}
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

def I25_27(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId ,amount=红包总金额（元）(必填), count=红包数量(必填), payType= 支付类型，1微信，2支付宝，3余额，4群账户(必填) , door = 入口标记，1 首页充值，2 红包再发一次 ,type=资金类型，0正常充值,1体验金,2大咖充值，3群账户,
    # cityId= 城市编码 ,groupId,templateId
    ########################################################################
    varInterfaceName =  "I25_27,发红包_广告红包发送接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeGetOrderNew.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"amount":param2,"count":param3
        ,"payType":param4,"door":param5,"type":param6,"cityId":param7,"groupId":param8,"templateId":param9}
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
def I25_28(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , amount , redPoolId=红包批次id ,payOrderId=订单编号
    ########################################################################
    varInterfaceName =  "I25_28,发红包_微信支付用户回调接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeOrderReturnNew.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"amount":param2,"redPoolId":param3
        ,"payOrderId":param4}
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
def I25_29(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId ,amount=红包总金额（元）(必填), count=红包数量(必填), payType= 支付类型，1微信，2支付宝，3余额，4群账户(必填) , door = 入口标记，1 首页充值，2 红包再发一次 ,type=资金类型，0正常充值,1体验金,2大咖充值，3群账户,
    # cityId= 城市编码 ,groupId,templateId,qrFlag=是否是二维码充值，0不是，1是
    ########################################################################
    varInterfaceName =  "I25_27,发红包_广告红包发送接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeGetOrderNew.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"amount":param2,"count":param3
        ,"payType":param4,"door":param5,"type":param6,"cityId":param7,"groupId":param8,"templateId":param9,"qrFlag":param10}
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
def I25_30(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , callBackType=回收类型，1放入红包池，2回收余额 , redPoolId=红包批次id
    ########################################################################
    varInterfaceName =  "I25_30,红包列表_红包放入红包池、余额回收接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/redpackCallBack.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"callBackType":param2,"redPoolId":param3}
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
def I25_31(varnum,varuserId,param1,param2,param3,param4,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , amount=支付金额 ,redPoolId=红包批次id,payOrderId=订单编号
    ########################################################################
    varInterfaceName =  "I25_31,发红包_微信支付用户回调接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeOrderReturnNew.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"amount":param2,"redPoolId":param3,"payOrderId":param4}
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
def I25_32(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,param12,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,amount=红包总金额（元）(必填),count=红包数量(必填),payType=支付类型，1微信，2支付宝，3余额，4群账户(必填),door=入口标记，1 首页充值，2 红包再发一次,type=资金类型，0正常充值,1体验金,2大咖充值，3群账户,cityId,groupId,templateId=模板id(必填),qrFlag=是否是二维码充值，0不是，1是,redPoolId=批次id(必填),payPwd=支付密码（余额）
    ########################################################################
    varInterfaceName =  "I25_32,发红包_红包充值接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/advertApprentice.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"amount":param2,"count":param3,"payType":param4
                   ,"door":param5,"type":param6,"cityId":param7,"groupId":param8
                   ,"templateId":param9,"qrFlag":param10,"redPoolId":param11,"payPwd":param12}
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
def I25_33(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , callBackType=回收类型，1放入红包池，2回收余额 ,redPoolId=红包批次id
    ########################################################################
    varInterfaceName =  "I25_33,红包列表_红包放入红包池、余额回收接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/redpackCallBack.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"callBackType":param2,"redPoolId":param3}
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
def I25_34(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , visitUserId=访问人id,isGroup=是否群主，1是，0否
    ########################################################################
    varInterfaceName =  "I25_34,我的_个人信息接口（新增返回值）"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/redpackCallBack.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"visitUserId":param2,"isGroup":param3}
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
def I25_35(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,payType=支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡),amount=红包金额,acceptId=收红包用户ID,
    # groupId=群ID,content=信息内容(可选),picUrls=图片路径，多张逗号分隔(可选),videoUrl=视频链接(可选)
    # payPwd=支付密码(可选,3、5必传), templateId=模板ID(可选)

    ########################################################################
    varInterfaceName =  "I25_35,首页_发红包_私信红包_发送私信红包接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_red.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"payType":param2,"amount":param3,"acceptId":param4
                   ,"groupId":param5,"content":param6,"picUrls":param7,"videoUrl":param8
                   ,"payPwd":param9,"templateId ":param10}
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
def I25_36(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,payType=支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡),amount=红包金额,acceptId=收红包用户ID,
    # groupId=群ID,content=信息内容(可选),payPwd=支付密码(可选,3、5必传),
    ########################################################################
    varInterfaceName =  "I25_36,首页_发红包_私信红包_发送私信转帐接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_transfer.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"payType":param2,"amount":param3,"acceptId":param4
                   ,"groupId":param5,"content":param6,"payPwd":param7}
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
def I25_37(varnum,varuserId,param1,param2,param3,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId , visitUserId = 访问人id ,isGroup =是否群主，1是，0否
    ########################################################################
    varInterfaceName =  "I25_37,我的_个人信息接口（新增返回值）"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/redpackCallBack.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"visitUserId":param2,"isGroup":param3}
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
def I25_38(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,payType=支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡),amount=红包金额,acceptId=收红包用户ID,
    # groupId=群ID,content=信息内容(可选),payPwd=支付密码(可选,3、5必传) , templateId=模板ID(可选)

    ########################################################################
    varInterfaceName =  "I25_38,首页_发红包_私信红包_发送私信红包接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_red.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"payType":param2,"amount":param3,"acceptId":param4
                   ,"groupId":param5,"content":param6,"payPwd":param7,"templateId ":param8}
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
def I25_39(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,payType=支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡),amount=红包金额,acceptId=收红包用户ID,
    # groupId=群ID,content=信息内容(可选),payPwd=支付密码(可选,3、5必传)

    ########################################################################
    varInterfaceName =  "I25_39,首页_发红包_私信红包_发送私信转帐接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_transfer.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"payType":param2,"amount":param3,"acceptId":param4
                   ,"groupId":param5,"content":param6,"payPwd":param7}
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
def I25_40(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId,shareType=分享类型，20app分享,25红包分享,platform=分享渠道，1：新浪微博 2：腾讯微博 3：微信好友 4：微信朋友圈 5：短信 6：qq好友 7：qq空间,
    # amount=金额,tranId=批次ID, channel=渠道类型1外平台,2红包池，3红包群,4二维码 ,channelId=渠道ID
    # lvl=层次id，1一级，2二级, =群ID,labelIds=红包群标签，逗号表达式

    ########################################################################
    varInterfaceName =  "I25_40,分享红包_获取分享链接接口"
    varUrl = "http://192.168.2.176:9999/payment/share/1.0/get_share_url.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"shareType":param2,"platform":param3,"amount":param4
                   ,"tranId":param5,"channel":param6,"channelId":param7,"lvl":param8,"labelIds":param9}
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

print  "\n====================== 2.5版本_APP接口测试 ======================"


# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('select userId from t_redgroup_memberinfo where groupId=213 order by userId desc')
# data3 = curT.fetchall()
# for each in data3[0]:
#     testId=int(each)+1
# print "  => [测试数据userId => " + str(testId)
# # 删除前先新增一个群成员 from I24_9 ,需确保此群成员userId不在 t_redgroup_memberinfo 表中.
# # I24_9业务逻辑: 分别在t_redgroup_user_label 和 t_redgroup_memberinfo 中新增1条记录.
# for i in range(0,5):
#     I24_9("RtnOK","10001679",testId,"213","10001679","500","C9-1,用户ID,群ID,群主用户ID,用户标签")
#     testId=testId+1
#
# sleep(1212)

# 1 首页_发红包炸弹_设置广告内容问号接口
print "1,================================================================================================="
I25_1("RtnOK","10001679","C1-1无参数")

# 2,APP登录接口(只测手机号)
# 先调用获取验证码接口
print "2,================================================================================================="
I25_2("RtnOK","13816109050","3101000000","0","0",u"令狐冲","","","",Icommon3("1","13816109050"),"C2-1,手机号,城市ID,下载渠道,渠道(手机),第三方昵称,第三方头像,token,微信唯一标识别(空),验证码")


# 3 我_设置_点击授权，找回红包_第三方绑定接口(微信标识无法获取 ?)
# print "3,================================================================================================="
# I25_3("RtnOK","10001679","10001679","0","John","","","3101000000","C3-1,登录ID,渠道,绑定第三方名称,绑定第三方头像(选),第三方标识(微信传unionId)")


# 4,首页_发红包_私信红包_获取用户私信初始金额接口
print "4,================================================================================================="
I25_4("RtnOK","10001679","10001679","C4-1,用户ID")
I25_4("RtnDeviceErr","10001679","","C4-2,用户ID(空)")
I25_4("RtnDeviceErr","10001679","123456789","C4-3,用户ID(错)")


# 5,首页_发红包_私信红包_私信内容列表接口
print "5,================================================================================================="
I25_5("RtnOK","10001679","C5-1无参数")

# # 6,我_设置_提现密码_获取设置提现密码验证码  2=提现验证码 ,4=设置提现密码
print "6,================================================================================================="
I25_6("RtnOK","10001679","10001679","13816109050","1","C6-1,用户ID,手机号,类型")
I25_6("RtnOK","10001679","10001679","13816109050","2","C6-2,用户ID,手机号,类型")
I25_6("RtnOK","10001679","10001679","13816109050","4","C6-3,用户ID,手机号,类型")
I25_6("RtnParamErr","10001679","10001679","13816109050","","C6-4,用户ID,手机号,类型(空)")


# 7,我_设置_提现密码_保存提现密码接口
print "7,================================================================================================="
xx=Icommon3("4","13816109050")
I25_7("RtnOK","10001679","10001679","13816109050","123456",xx,"C7-1,用户ID,手机号,当前密码,验证码")
I25_7("RtnParamErr","10001679","10001679","13816109050","123456","0000","C7-2,用户ID,手机号,当前密码,验证码(错)")
I25_7("RtnParamErr","10001679","10001679","13816109050","123456000",xx,"C7-3,用户ID,手机号,当前密码(错),验证码")
I25_7("RtnParamErr","10001679","10001679","13816109050","123456","","C7-4,用户ID,手机号,当前密码,验证码(空)")
I25_7("RtnParamErr","10001679","10001679","13816109050","",xx,"C7-5,用户ID,手机号,当前密码(空),验证码")


# 8,我_设置_提现密码_修改提现密码接口
print "8,================================================================================================="
I25_8("RtnOK","10001679","10001679","123456","111111","C8-1,用户ID,原密码,当前密码")
I25_8("RtnOK","10001679","10001679","111111","111111","C8-2,用户ID,原密码,当前密码")
I25_8("RtnParamErr","10001679","10001679","666666","111111","C8-3,用户ID,原密码(错),当前密码")
I25_8("RtnParamErr","10001679","10001679","","111111","C8-4,用户ID,原密码(空),当前密码")
I25_8("RtnParamErr","10001679","10001679","666666","","C8-5,用户ID,原密码,当前密码(空)")
I25_8("RtnParamErr","10001679","10001679","","","C8-6,用户ID,原密码(空),当前密码(空)")



# 9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)
print "9,================================================================================================="
I25_9("RtnOK","10001679","10001679","213","1","1","C9-1,用户ID,群ID,分页开始位置,每页显示条数")

# 10,红包模板_红包类型列表, 类型1=广告红包炸弹 ; 2=好评红包 ; 3=普通群红包 ; 4=普通群红包 ; 5=私信红包
print "10,================================================================================================="
I25_10("RtnOK","10001679","10001679","1","C10-1,用户id,模版类型1")
I25_10("RtnOK","10001679","10001679","2","C10-2,用户id,模版类型2")
I25_10("RtnOK","10001679","10001679","3","C10-3,用户id,模版类型3")
I25_10("RtnOK","10001679","10001679","4","C10-4,用户id,模版类型4")
I25_10("RtnOK","10001679","10001679","5","C10-5,用户id,模版类型5")
I25_10("RtnOKNone","10001679","10001679","6","C10-6,用户id,模版类型(错)")


# 11,红包模板_红包模板列表
print "11,================================================================================================="
I25_11("RtnOK","10001679","10001679","1","1","1","C11-1,用户id,模版类型1,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","2","1","1","C11-2,用户id,模版类型2,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","3","1","1","C11-3,用户id,模版类型3,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","4","1","1","C11-4,用户id,模版类型4,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","5","1","1","C11-5,用户id,模版类型5,分页开始位置,每页显示条数")
I25_11("RtnParamErr","10001679","10001679","66","1","1","C11-6,用户id,模版类型(错),分页开始位置,每页显示条数")

# 12,	红包模板_保存红包模板 ,1-5 分别对应 t_sys_config 表里5个类型
print "12,================================================================================================="
I25_12("RtnOK","10001679","10001679","1","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-1,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","2","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-2,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","3","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-3,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","4","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-4,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","5","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-5,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnParamErr","10001679","10001679","166","title1","pinpai","neirong","www.baidu.com","vedio.com","166","http://pic.com","","C12-6,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")

# 13,红包模板_删除红包模板
print "13,================================================================================================="
I25_13("RtnOK","10001679","10001679","1","C13-1,用户ID,模版ID")
I25_13("RtnOK","10001679","10001679","2","C13-1,用户ID,模版ID")
I25_13("RtnOK","10001679","10001679","3","C13-1,用户ID,模版ID")
I25_13("RtnOK","10001679","10001679","4","C13-1,用户ID,模版ID")
I25_13("RtnOK","10001679","10001679","5","C13-1,用户ID,模版ID")


