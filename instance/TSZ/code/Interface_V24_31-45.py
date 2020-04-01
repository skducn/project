# coding: utf-8

import requests,redis,MySQLdb
from time import sleep
print  "\n====================== 2.4版本_APP接口测试_支付接口 ======================"


def Icommon1_(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    # 字段说明：
    # redNumber(count) ＝ 红包总数量
    # redSumAmount(amount) = 红包总金额
    # source（payType） = 推广来源 （1微信充值，2支付宝充值，3余额充值）
    # brandContent ＝ 品牌商户名称
    # door =   1首页进入 2红包再发一次
    # id（t_extension_channel_redPic）(picIds)＝渠道推广图片ID
    ########################################################################
    varInterfaceName =  "I24_30_1,支付接口"
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"

def I24_31(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: redPoolId = 红包池id, userId = 用户ID, uninAmount = 单位金额,payType=支付类型,channel =渠道类型,
    # brandContent =品牌,lvl =层级,count =红包数量,labelIds =红包群选择分类(新增),
    ########################################################################
    varInterfaceName =  "I24_31_2,渠道推广红包个分享渠道记录接口(新增参数)"
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "设置数量不正确":
            if response.json()['errorcode'] == 1 and response.json()['success'] == False:
                print "[OK,设置数量不正确]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                 print "[Error,设置数量不正确]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception,data:
        print Exception,":",data,"\n"
def I24_35(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,param12,param13,param14,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数: userId = 用户ID, shareType = 类型, platform = 分享渠道，amount = 红包总金额, tranId = 红包池id,
    # count = 红包数量,uninAmount=单个红包金额,payType =支付类型,channel=渠道类型,lvl =层级，brandContent =品牌名称,
    # context=推广内容,labelIds =红包群选择分类(新增)，name=品牌名称（如果是微薄就必填，其他渠道选填）
    #业务逻辑

    #该接口是建立在支付接口与回调接口的基础上，红包池id必须继承上id
    #接口发送成功后t_share会插入一条消息记录
    #t_redgroup_message也会插入一条数据对应的platform，红包群选择分类

    ########################################################################
    varInterfaceName =  "I24_35,获取分享内容及分享链接接口(新增参数)"
    varUrl = "http://192.168.2.176:9999/payment/share/1.0/get_share_url.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"shareType":param2,"platform":param3
        , "amount": param4,"tranId":param5,"count":param6,"uninAmount":param7,"payType":param8,"channel":param9
        , "lvl": param10,"brandContent":param11,"context":param12,"labelIds":param13,"name":param14,
        }
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']== True and response.json()['data'] <> []:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==1 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
            if response.json()['success']== True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "DonGrab":
            if response.json()['errorcode'] == 0 and response.json()['success'] != False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"



# 支付接口传入的值，需要调用一下，才能进行一下操作  返回ID ,t_extension_channel_redpool
Icommon1_("RtnOK", "10001679", "3", "1.0", "2360", "10001476", "alibaba1", "1","1","Common1,推广来源,红包总金额,渠道推广图片ID,userid,品牌商户名称,红包总数量,door")



#I24_31渠道推广红包个分享渠道记录接口
# I24_31依赖于I22接口 , 支付接口获得的红包池id，通过红包池与金额来验证是否回调成功

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT id from t_extension_channel_redPool  WHERE userId=10001679 and brandContent="alibaba1"')
data1 = curT.fetchone()

I24_31("RtnOK","10001679",data1[0],"10001679","100","3","1","alibaba1","1","1","","C31-1,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")


# 检查数据库分别在t_extension_channel_redPool,t_extension_channel新增1条，并且修改t_extension_channel中的渠道类型
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT COUNT(id) from  t_extension_channel_redPool WHERE id="%s"'%(data1[0]))
data2 = curT.fetchone()
if data2[0]==1:
    print "[OK,数据库t_extension_channel_redPool新增1条成功],I24_31_2,渠道推广红包个分享渠道记录接口"
else:
    print "[Error,数据库t_extension_channel_redPool新增1条失败],I24_31_2,渠道推广红包个分享渠道记录接口"
# 检测t_extension_channel新增一条
curT = conn.cursor()
curT.execute('SELECT COUNT(id) from  t_extension_channel WHERE extensionRedPoolId="%s"'%(data1[0]))
data3 = curT.fetchone()
if data3[0] == 1:
    print "[OK,数据库t_extension_channel新增1条成功],I24_31_2,渠道推广红包个分享渠道记录接口"
else:
    print "[Error,数据库t_extension_channel新增1条失败],I24_31_2,渠道推广红包个分享渠道记录接口"
# 检查t_extension_channel修改类型
curT = conn.cursor()
curT.execute('SELECT COUNT(id) from  t_extension_channel WHERE channel=1 and extensionRedPoolId="%s"'%(data1[0]))
data4 = curT.fetchone()
if data4[0] == 1:
    print "[OK,数据库t_extension_channel修改一条成功],I24_31_2,渠道推广红包个分享渠道记录接口"
else:
    print "[Error,数据库t_extension_channel修改一条失败],I24_31_2,渠道推广红包个分享渠道记录接口"
I24_31("RtnParamErr","10001476","","10001476","100","3","1","aaaaa","1","","","C31-2,用户ID,红包池id(空),用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("RtnParamErr","10001476",data1,"","100","3","1","aaaaa","1","","","C31-3,用户ID,红包池id,用户ID（空）,单位金额,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("RtnParamErr","10001476",data1,"10001476","","3","1","aaaaa","1","","","C31-4,用户ID,红包池id,用户ID,单位金额（空）,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("RtnOK","10001476",data1,"10001476","2","3","1","aaaaa","1","","","C31-5,用户ID,红包池id,用户ID,单位金额（错）,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
# 检查t_extension_channel_redPool,t_extension_channel中的支付过后的红包总额是否一致
curT = conn.cursor()
curT.execute('SELECT redSumAmount from  t_extension_channel_redPool WHERE id=%s'%(data1[0]))
data5 = curT.fetchone()
if data5[0] == 100:
    print "[OK,数据库t_extension_channel_redPool红包总额验证通过"
else:
    print "[Error,t_extension_channel_redPool红包总额验证失败"
#验证t_extension_channel中的channelRedAmount，channelRedSumAmount金额
curT = conn.cursor()
curT.execute('SELECT COUNT(id) from t_extension_channel WHERE channelRedSumAmount=100 and channelRedAmount=100 and extensionRedPoolId=%s'%(data1[0]))
data6 = curT.fetchone()
if data6[0] == 1:
    print "[OK,数据库t_extension_channel_redPool红包总额验证通过"
else:
    print "[Error,t_extension_channel_redPool红包总额验证失败"
I24_31("RtnOK","10001476",data1,"10001476","-10","3","1","aaaaa","1","","","C31-6,用户ID,红包池id,用户ID,单位金额（负数）,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
# 检查t_extension_channel_redPool,t_extension_channel中的支付过后的红包总额是否一致
curT = conn.cursor()
curT.execute('SELECT redSumAmount from  t_extension_channel_redPool WHERE id=%s'%(data1[0]))
data5 = curT.fetchone()
if data5[0] == 100:
    print "[OK,数据库t_extension_channel_redPool红包总额验证通过"
else:
    print "[Error,t_extension_channel_redPool红包总额验证失败"
#验证t_extension_channel中的channelRedAmount，channelRedSumAmount金额
curT = conn.cursor()
curT.execute('SELECT COUNT(id) from t_extension_channel WHERE channelRedSumAmount=100 and channelRedAmount=100 and extensionRedPoolId=%s'%(data1[0]))
data6 = curT.fetchone()
if data6[0] == 1:
    print "[OK,数据库t_extension_channel_redPool红包总额验证通过"
else:
    print "[Error,t_extension_channel_redPool红包总额验证失败"
I24_31("RtnOK","10001476",data1,"10001476","1.11","3","1","aaaaa","1","","","C31-7,用户ID,红包池id,用户ID,单位金额（小数）,支付类型,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
# 检查t_extension_channel_redPool,t_extension_channel中的支付过后的红包总额是否一致
curT = conn.cursor()
curT.execute('SELECT redSumAmount from  t_extension_channel_redPool WHERE id=%s'%(data1[0]))
data5 = curT.fetchone()
if data5[0] == 100:
    print "[OK,数据库t_extension_channel_redPool红包总额验证通过"
else:
    print "[Error,t_extension_channel_redPool红包总额验证失败"
#验证t_extension_channel中的channelRedAmount，channelRedSumAmount金额
curT = conn.cursor()
curT.execute('SELECT COUNT(id) from t_extension_channel WHERE channelRedSumAmount=100 and channelRedAmount=100 and extensionRedPoolId=%s'%(data1[0]))
data6 = curT.fetchone()
if data6[0] == 1:
    print "[OK,数据库t_extension_channel_redPool红包总额验证通过"
else:
    print "[Error,t_extension_channel_redPool红包总额验证失败"
I24_31("RtnParamErr","10001476",data1,"10001476","100","","1","aaaaa","1","","","C31-8,用户ID,红包池id,用户ID,单位金额,支付类型（空）,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("RtnOK","10001476",data1,"10001476","100","6","1","aaaaa","1","","","C31-9,用户ID,红包池id,用户ID,单位金额,支付类型（错）,渠道类型,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("RtnParamErr","10001476",data1,"10001476","100","3","","aaaaa","1","","","C31-10,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型（空）,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("RtnOK","10001476",data1,"10001476","100","3","6","aaaaa","1","","","C31-11,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型（错）,品牌,层级,红包数量,红包群选择分类(新增)")
I24_31("设置数量不正确","10001476",data1,"10001476","100","3","2","aaaaa","1","2","","C31-1,用户ID,红包池id,用户ID,单位金额,支付类型,渠道类型,品牌,层级,红包数量(错),红包群选择分类(新增)")



#I24_32获得红包群分类列表接口
I24_32("RtnOK","10001476","C32-1,用户ID")
I24_32("RtnOK","","C32-2,用户ID(空)")

#I24_33红包群设置店铺链接接口
I24_33("RtnOK","10001476","10001476","7","http://www.baidu.com/","C33-1,用户ID,群ID,店铺链接")
I24_33("RtnOK","10001476","10001476","7","","C33-2,用户ID,群ID,店铺链接（空）")
I24_33("RtnParamErr","10001476","","7","http://www.baidu.com/","C33-3,用户ID(空),群ID,店铺链接")
I24_33("RtnParamErr","10001490","10001490","7","http://www.baidu.com1111/","C33-4,用户ID（错）,群ID,店铺链接")
I24_33("RtnParamErr","10001476","10001476","8","http://www.baidu.com1111/","C33-5,用户ID,群ID（错）,店铺链接")
I24_33("RtnParamErr","10001476","10001476","","http://www.baidu.com1111/","C33-6,用户ID,群ID（空）,店铺链接")
I24_33("RtnSysErr","10001476","10001476","7","阿飞似懂斯蒂芬非懂阿地方飞打发打发似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂阿飞似懂非懂","C33-7,用户ID,群ID（空）,店铺链接")

#34红包群分类设置接口
I24_34("RtnOK","10001476","10001476","7","0","C34-1,用户ID,群ID,分类ID")
I24_34("RtnParamErr","10001476","","7","0","C34-2,用户ID（空）,群ID,分类ID")
I24_34("RtnParamErr","10001476","10001476","","0","C34-3,用户ID,群ID（空）,分类ID")
I24_34("RtnParamErr","10001476","10001476","8","0","C34-4,用户ID,群ID（错）,分类ID")
I24_34("RtnSysErr","10001476","10001476","7","","C34-5,用户ID,群ID,分类ID（空）")


#35获取分享内容及分享链接接口
I24_35("RtnOK","10001476","10001476","25","1","100",data1,"1","100","3","1","1","品牌名","推广内容","1","","C35-1,用户ID,类型,分享渠道，红包总金额 ，红包池id，红包数量，单个红包金额，支付类型，渠道类型，层级，品牌名称，推广内容，红包群选择分类，品牌名称，")
I24_35("RtnOK","10001476","10001476","25","8","100",data1,"1","100","3","2","1","品牌名","推广内容","1","","C35-2,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
I24_35("RtnOK","10001476","10001476","25","10","100",data1,"1","100","3","2","1","品牌名","推广内容","1","","C35-3,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
#检测t_share新增一条
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306,use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT obj_id from ukardapp.t_share WHERE user_id=10001476 ORDER BY id DESC limit 0,1')
data2 = curT.fetchone()
if data2[0] == data1[0]:
    print "[OK,数据库t_redgroup_message新增1条成功],I24_35,获取分享内容及分享链接接口"
else:
    print "[Error,数据库t_redgroup_message新增1条失败],I24_35,获取分享内容及分享链接接口"
I24_35("RtnDeviceErr","10001476","","25","1","100",data1,"1","100","3","1","1","品牌名","推广内容","1","","C35-4,用户ID（空）,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
I24_35("RtnDeviceErr","10001476","10001477","25","1","100",data1,"1","100","3","1","1","品牌名","推广内容","1","","C35-5,用户ID（错）,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
# ###platform在验证不存在的
I24_35("RtnSysErr","10001476","10001476","25","11","100",data1,"1","10000","3","1","1","品牌名","推广内容","1","","C35-6,用户ID,类型,分享渠道（错）,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
I24_35("RtnOK","10001476","10001476","25","10","1",data1,"1","100000","3","4","1","品牌名","推广内容","1","","C35-7,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")
##验证已发送过二维码红包，需要上一个用例做铺垫，需要跑两次
I24_35("RtnSysErr","10001476","10001476","25","10","1",data1,"1","100000","3","4","1","品牌名","推广内容","1","","C35-8,用户ID,类型,分享渠道,红包总金额 ,红包池id,红包数量,单个红包金额,支付类型,渠道类型,层级,品牌名称,推广内容,红包群选择分类,品牌名称,")

#36用户发的红包广告统计信息接口
I24_36("RtnOK","10001476","10001476","7","0","5","C36-1,用户ID,群ID,分页开始位置,每页显示条数")
I24_36("RtnSysErr","10001476","10001476","7","0","1000000000000","C36-2,用户ID,群ID,分页开始位置,每页显示条数(错)")
I24_36("RtnParamErr","10001476","","7","0","5","C36-3,用户ID（空）,群ID,分页开始位置,每页显示条数")
I24_36("RtnDeviceErr","1000147","10001476","7","0","5","C36-4,用户ID,群ID,分页开始位置,每页显示条数")

#37红包群成员_群成员排序分类
I24_37("RtnOK","10001476","C36-1,用户ID")

#38获取我关注的红包群群主列表接口
I24_38("RtnOK","10001476","10001476",data1,"C38-1,用户ID,搜索名称")
I24_38("RtnParamErr","10001476","",data1,"C38-2,用户ID(空),搜索名称")
I24_38("RtnDeviceErr","","","","C38-3,用户ID(空),搜索名称(空)")

#39我的红包群信息接口
I24_39("RtnOK","10001476","10001476","C39-1,用户ID")
I24_39("RtnSysErr","10001476","100014761","C39-2,用户ID")
I24_39("RtnParamErr","10001476","","C39-3,用户ID(空)")

#40我的红包群信息接口
I24_40("RtnOK","10001476","10001476","10001800","0","C40-1,登录人用户ID,查看人用户ID,是否群主1群主/0非群主")
I24_40("RtnParamErr","","","","","C40-2,登录人用户ID(空),查看人用户ID(空),是否群主1群主/0非群主(空)")
I24_40("RtnOK","10001476","10001476","10001800","1","C40-3,登录人用户ID,查看人用户ID,是否群主1群主/0非群主")

#41群新成员红点接口
I24_41("RtnOK","10001476","10001476","C41-1,登录人用户ID")
I24_41("RtnParamErr","10001476","","C41-2,登录人用户ID(空)")

#42我关注的红包群分类接口
I24_42("RtnOK","10001476","10001476","C42-1,登录人用户ID")
I24_42("RtnParamErr","10001476","","C42-2,登录人用户ID(空)")



#43抢红包回调接口
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT channelId from t_internal_redDetail WHERE userId=10001476 and redState=3 ORDER BY id DESC limit 0,1')
data1 = curT.fetchone()
curT.execute('SELECT batchId from t_internal_redDetail WHERE userId=10001476 and redState=3 ORDER BY id DESC limit 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from t_redgroup_baseinfo WHERE userId=10001476')
data3 = curT.fetchone()


# data:1是抢完的0是抢到的
I24_43("RtnOK","10001476","10001476",data1,data2,data3,"C43-1,登录人用户ID,渠道ID,批次ID,群Id")
I24_43("RtnParamErr","10001476","","","","","C43-2,登录人用户ID(空),渠道ID,批次ID,群Id")
I24_43("DonGrab","10001476","10001476","155556","455似懂非懂445","s斯蒂芬斯蒂芬斯蒂芬森的dfd","C43-3,登录人用户ID(),渠道ID（错）,批次ID（错）,群Id（错）")
I24_43("DonGrab","10001476","10001476",data1,data2,"1000","C43-4,登录人用户ID(),渠道ID,批次ID,群Id（错）")

#44更新进入店铺链接打开数接口
curT = conn.cursor()
curT.execute('SELECT channelId from t_internal_redDetail WHERE userId=10001476 and redState=3 ORDER BY id DESC limit 0,1')
data10 = curT.fetchone()
I24_44("RtnOK","10001476","10001476","1",data10,"C44-1,用户ID,渠道ID,批次ID")
I24_44("RtnParamErr","10001476","10001476","","","C44-2,用户ID,渠道ID,批次ID")
I24_44("RtnParamErr","10001476","","1",data10,"C44-3,用户ID,渠道ID,批次ID")


#45红包群查看分享奖励条数接口
curT = conn.cursor()
curT.execute('SELECT id from t_redgroup_baseinfo WHERE userId=10001476')
data11 = curT.fetchone()
curT.close(),conn.close()
I24_45("RtnOK","10001800","10001800",data11,"10001476","C45-1,用户ID,群ID,群主用户ID")
I24_45("RtnParamErr","10001800","",data11,"10001476","C45-2,用户ID（空）,群ID,群主用户ID")
I24_45("RtnParamErr","10001800","10001800","","10001476","C45-3,用户ID,群ID（空）,群主用户ID")
I24_45("RtnParamErr","10001800","10001800",data11,"","C45-4,用户ID,群ID,群主用户ID（空）")








