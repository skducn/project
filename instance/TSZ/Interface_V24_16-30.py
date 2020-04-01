# coding: utf-8

import requests,redis,MySQLdb
from time import sleep

print  "\n====================== 2.4版本_APP接口测试 ======================"

# data = {"data":{"dataList":[{"groupId":"","createTime":"2016-06-24 16:41:41","channelType":5,"nickname":"宋哈哈","userId":"10001484","pic":"-1","headPic":"http://sit2.88uka.com/000/000/004/815.jpg"},{"groupId":"","createTime":"2016-06-23 14:47:01","channelType":5,"nickname":"中国移动民居模块命名公民look名民","userId":"10001481","pic":"-1","headPic":"http://sit2.88uka.com/000/000/004/304.jpg"}],"list2":"1212","isEnd":1,"count":2,"validamount":"","list1":"1212","nextStartIndex":-1,"variableMap":{}},"errorstr":"","errorcode":0,"success":'true'}
# dd1= data['data']
# print 'count' in dd1.keys()
#
# sleep(12121)

def I24_9(varnum, varuserId, param1, param2, param3, param4, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId =  用户ID, groupId = 群ID,groupUserId = 群主用户ID , groupLabel=用户标签(可选)
    ########################################################################
    varInterfaceName = "I24_9,红包群成员_添加红包群成员接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupMember/2.4/add_redGroup_member.do"
    if param4 == "":
        querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                       "groupId": param2, "groupUserId": param3}
    else:
        querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1,
                       "groupId": param2, "groupUserId": param3, "groupLabel": param4}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()[
                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()[
                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"
def I24_27(varnum, varuserId, param1, param2, param3, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,
                          password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数: userId = 用户ID, groupId = 群ID, groupUserId = 群主用户ID
    ########################################################################
    varInterfaceName = "I24_26,红包群消息_我关注的红包群消息列表接口"
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
                print "[Error,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and \
                            response.json()[
                                'success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and \
                            response.json()[
                                'success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[Error,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
    except Exception, data:
        print Exception, ":", data, "\n"


# "====================== 2.4版本_APP接口测试用例 ======================"

#
#
#
# # # 18 红包群成员_修改群备注接口
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select userId,groupId from t_redgroup_memberinfo where groupId=213')
# data1 = curT.fetchone()
# # nickname18=u"中文Ts~!@#$%……*()"
# nickname18="jinhaoremark"
# I24_18("RtnOK",str(data1[0]),data1[0],"213",nickname18,"C18-1,用户ID,群ID,群呢称(改)")
#
# # C18-1,检查数据库修改记录
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('select count(userId) from t_redgroup_memberinfo where userId=%s and groupId=213 and groupRemark="%s"' %(data1[0],nickname18))
# data2 = curT.fetchone()
# if data2[0]==1:
#     print "  => [Ok,t_redgroup_memberinfo数据库群备注修改1条成功,I24_18]"
# else:
#     print "  => [Error,t_redgroup_memberinfo数据库群备注修改1条失败,I24_18]"
#
# I24_18("RtnOK",str(data1[0]),data1[0],"213","","C18-2,用户ID,群ID,群呢称(空)")
#
# # C18-2,检查数据库修改记录为空
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('select count(userId) from t_redgroup_memberinfo where userId=%s and groupId=213 and groupRemark=""' %(data1[0]))
# data3 = curT.fetchone()
# if data3[0]==1:
#     print "  => [OK,t_redgroup_memberinfo数据库群备注修改1条为空成功,I24_18]"
# else:
#     print "  => [Error,t_redgroup_memberinfo数据库群备注修改1条为空失败,I24_18]"
#
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('select userId from t_redgroup_memberinfo where groupId=213 order by userId')
# data3 = curT.fetchall()
# for each in data3[0]:
#     TestUserId18_sub=int(each)-1
# I24_18("RtnParamErr",str(data1[0]),"","213",nickname18,"C18-3,用户ID(空),群ID,群呢称")
# I24_18("RtnParamErr",str(data1[0]),data1[0],"",nickname18,"C18-4,用户ID,群ID(空),群呢称")
# I24_18("RtnParamErr",str(data1[0]),"","",nickname18,"C18-5,用户ID(空),群ID(空),群呢称")
# I24_18("RtnParamErr",str(data1[0]),TestUserId18_sub,"213",nickname18,"C18-6,用户ID(错),群ID,群呢称")
# I24_18("RtnOK",str(data1[0]),data1[0],"0",nickname18,"C18-6,用户ID,群ID(错),群呢称")


# # 19 红包群成员_获取所有新成员列表接口
# # 涉及表, t_group_memberinfo 中 ,is_check =1 1表示未查看 , 0=已查看 ,
# # 业务逻辑: 返回 t_group_memberinfo 表中未查看的新成员,统计count计数
# # # 获取 t_group_memberinfo 表中 is_check=1 的数量,统计count计数
# # 如果 count计数=0 则验证json返回count是否等于 0 ,并新增1个成员如I24_9-2 最终删除此用户;
# # 如果 count计数>=1 则验证json返回count是否>=1
#
# # 获取 t_group_memberinfo 表中 is_check=1 的个数
# varJsonRtnIsCheckNums=I24_19("RtnOK","10001679","10001679","213","0","5","C19-1,用户ID,群ID,分页开始位置,每页显示条数")
#
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('select count(id) from t_redgroup_memberinfo where isCheck=1 and groupUserId=10001679')
# data3 = curT.fetchone()
# if data3[0]==0:
#     # 如果 count计数=0 则验证json返回count是否等于 0 ,并新增1个成员如I24_9-2 最终删除此用户;
#     conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
#     curT = conn.cursor()
#     a_list=[]
#     curT.execute('select userId from t_redgroup_memberinfo where groupId=213 and groupUserId=10001679')
#     data1 = curT.fetchall()
#     for i in range(len(data1)):
#         for each in data1[i]:
#            a_list.append(str(each))
#     TestUserId19_last = ''.join(a_list[-1])   # 获取 t_redgroup_memberinfo 第最后1个符合要求的userId
#     TestUserId19_sub = int(TestUserId19_last)-1
#     if data1[0]>=1:
#      curT.execute('delete from t_redgroup_memberinfo where userId=%s and groupId=213 and groupUserId=10001679' %(TestUserId19_sub))
#      conn.commit()
#     curT.execute('select count(id) from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId19_sub))
#     data1 = curT.fetchone()
#     if data1[0]>=1:
#      curT.execute('delete from t_redgroup_user_label where userId=%s and groupId=213 ' %(TestUserId19_sub))
#      conn.commit()
#
#     I24_9("RtnOK","10001679",TestUserId19_sub,"213","10001679","","C9-2,用户ID,群ID,群主用户ID,用户标签(空)")
#     varJsonRtnIsCheckNums=I24_19("RtnOK","10001679","10001679","213","0","5","C19-1,用户ID,群ID,分页开始位置,每页显示条数")
#
#     conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
#     curT = conn.cursor()
#     curT.execute('select count(id) from t_redgroup_memberinfo where isCheck=1 and groupUserId=10001679')
#     data2 = curT.fetchone()
#     if data2[0]>=1 and data2[0]==varJsonRtnIsCheckNums:print "  => [OK,t_redgroup_memberinfo数据库isCheck数量与Json返回数量一致,I24_19-1]"
#     else: "  => [Error,t_redgroup_memberinfo数据库isCheck数量与Json返回数量不一致,I24_19-1]"
#
#     # 销毁新增的I24_9数据 ,由于调用了I24_9-2 ,因此不会在t_redgroup_user_label中创建记录,只需删除 t_redgroup_memberinfo 表中记录即可.
#     curT.execute('delete from t_redgroup_memberinfo where userId=%s and groupId=213 ' %(TestUserId19_sub))
#     conn.commit()
#
# # 如果 count计数>=1 则验证json返回count是否>=1
# if data3[0]>=1 and data3[0]==varJsonRtnIsCheckNums:print "  => [OK,t_redgroup_memberinfo数据库isCheck数量与Json返回数量一致,I24_19-1]"
# else: "  => [Error,t_redgroup_memberinfo数据库isCheck数量与Json返回数量不一致,I24_19-1]"
#
# I24_19("RtnOK","10001679","100016791212","213","","5","C19-2,用户ID,群ID,分页开始位置(空),每页显示条数")
# I24_19("RtnOK","10001679","10001679","213","-1","5","C19-3,用户ID,群ID,分页开始位置(错),每页显示条数")
# I24_19("RtnOK","10001679","10001679","213","0","0","C19-4,用户ID,群ID,分页开始位置,每页显示条数(0)")
# I24_19("RtnParamErr","10001679","","213","0","5","C19-5,用户ID(空),群ID,分页开始位置,每页显示条数")
# I24_19("RtnParamErr","10001679","10001679","","1","5","C19-6,用户ID,群ID(空),分页开始位置,每页显示条数")
# I24_19("RtnParamErr","10001679","10001680","213","1","5","C19-7,用户ID(错),群ID,分页开始位置,每页显示条数")
# I24_19("RtnParamErr","10001679","10001679","000","1","5","C19-8,用户ID,群ID(错),分页开始位置,每页显示条数")
# I24_19("RtnSysErr","10001679","10001679","213","0","","C19-9,用户ID,群ID,分页开始位置,每页显示条数(空)")
# I24_19("RtnSysErr","10001679","10001679","213","0","llkk","C19-10,用户ID,群ID,分页开始位置,每页显示条数(错)")

#20 红包群查看分享奖励列表接口(新增返回值,老数据batchIndex默认从0开始)
I24_20("RtnOK","10001684","10001684","213","10001679","C20-1,用户ID,群ID,群主用户ID")#batchIndex确认
I24_20("RtnOK","10001684","-1","213","10001679","C20-2,用户ID(错),群ID,群主用户ID")

I24_20("RtnParamErr","10001684","","213","10001679","C20-2,用户ID(空),群ID,群主用户ID")
I24_20("RtnParamErr","10001684","10001684","","10001679","C20-2,用户ID,群ID(空),群主用户ID")
I24_20("RtnParamErr","10001684","10001684","213","","C20-2,用户ID,群ID,群主用户ID(空)")
I24_20("RtnParamErr","10001684","10001684","2.13","10001679","C20-2,用户ID,群ID(错),群主用户ID")
I24_20("RtnParamErr","10001684","10001684","213","00000","C20-2,用户ID,群ID,群主用户ID(错)")

# #账户余额初始化为5000
# r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
# r2.hset("t_user:id:10001679","Commission_residue","5000")
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# curT.execute('update t_user set Commission_residue = 5000 where id = 10001679 ')
# conn.commit()
#21 红包群消息_保存消息接口
# I24_21("RtnOK","10001679","10001679","213","xianliqiong_保存消息","113","7","C20-1, 用户ID, 群ID, 消息内容, 标签id(1个), 消息类型")
# # C21-1,检查数据库t_redgroup_message新增1条且标签id=113,t_redgroup_messamge_auth新增1条,t_redgroup_memberinfo中对应userId的isMessage+1
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and groupMessage="xianliqiong_保存消息" and labelIds=",113," and type = 7')
# data1 = curT.fetchone()
# print data1[0]
# if data1[0]==1:
#     print "[OK,数据库t_redgroup_message新增1条成功],I24_21,红包群消息_保存消息接口"
# else:
#     print "[Error,数据库t_redgroup_message新增1条失败],I24_21,红包群成员_修改群备注接口"
# curT.close(), conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select id from t_redgroup_message where groupId=213 and groupMessage="xianliqiong_保存消息" and labelIds=",113," and type = 7')
# data2 = curT.fetchone()
# print data2[0]
# curT.close(),conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and labelId=113 and messageState = 0 and messageId=%s' % (data2[0]))
# data3 = curT.fetchone()
# print  data3[0]
# if data3[0]==1:
#     print "[Ok,t_redgroup_messamge_auth数据库记录新增1条成功],I24_21,红包群消息_保存消息接口"
# else:
#     print "[Error,t_redgroup_messamge_auth数据库记录新增1条失败],I24_21,红包群消息_保存消息接口"
# curT.close(),conn.close()


# I24_21("RtnOK","10001679","10001679","213","xianliqiong_保存消息","137,138","8","C20-2, 用户ID, 群ID, 消息内容, 标签id(2个), 消息类型")
# # C21-2,检查数据库t_redgroup_message新增1条且标签id有137,138,t_redgroup_messamge_auth新增2条,t_redgroup_memberinfo中对应userId的isMessage+1
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and groupMessage="xianliqiong_保存消息" and labelIds =",137,138," and type = 8')
# data4 = curT.fetchone()
# if data4[0]==1:
#     print "[OK,数据库t_redgroup_message新增1条成功],I24_21,红包群消息_保存消息接口"
# else:
#     print "[Error,数据库t_redgroup_message新增1条失败],I24_21,红包群成员_修改群备注接口"
# curT.close(), conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select id from t_redgroup_message where groupId=213 and groupMessage="xianliqiong_保存消息" and labelIds =",137,138," and type = 8')
# data5 = curT.fetchone()
# curT.close(),conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and labelId in ("137","138") and messageState = 0 and messageId=%s' % (data5[0]))
# data6 = curT.fetchone()
# if data6[0]==2:
#     print "[Ok,t_redgroup_messamge_auth数据库记录新增2条成功],I24_21,红包群消息_保存消息接口"
# else:
#     print "[Error,t_redgroup_messamge_auth数据库记录新增2条失败],I24_21,红包群消息_保存消息接口"
# curT.close(),conn.close()


# I24_21("RtnOK","10001679","10001679","213","xianliqiong_保存/撤回消息","0","2","C21-3, 用户ID, 群ID, 消息内容, 标签id(全部), 消息类型")
# # C21-3,检查数据库t_redgroup_message新增1条且标签id为全部群成员(共6个),t_redgroup_messamge_auth新增6条,t_redgroup_memberinfo中对应userId的isMessage+1
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and groupMessage="xianliqiong_保存/撤回消息" and labelIds =",0," and type = 2')
# data4 = curT.fetchone()
# if data4[0]==1:
#     print "[OK,数据库t_redgroup_message新增1条成功],I24_21,红包群消息_保存消息接口"
# else:
#     print "[Error,数据库t_redgroup_message新增1条失败],I24_21,红包群成员_修改群备注接口"
# curT.close(), conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select id from t_redgroup_message where groupId=213 and groupMessage="xianliqiong_保存/撤回消息" and labelIds =",0," and type = 2')
# data5 = curT.fetchone()
# print  data5[0]
# curT.close(),conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and labelId =0 and messageState = 0 and messageId=%s' % (data5[0]))#全部群成员labelId=0
# data6 = curT.fetchone()
# if data6[0]==1:
#     print "[Ok,t_redgroup_messamge_auth数据库记录新增1条成功],I24_21,红包群消息_保存消息接口"
# else:
#     print "[Error,t_redgroup_messamge_auth数据库记录新增1条失败],I24_21,红包群消息_保存消息接口"
# curT.close(),conn.close()
#
#
#
# #22 红包群消息_群主删除消息接口
# I24_22("RtnOK","10001679","10001679","213",data5[0],"C22-1, 用户ID, 群ID, 消息ID")
# # C22-1,检查数据库t_redgroup_message删除1条(messageState=1)
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and messageState=1 and id=%s' %(data5[0]))
# data7 = curT.fetchone()
# if data7[0]==1:
#     print "[OK,数据库t_redgroup_message删除1条成功],I24_22,红包群消息_群主删除消息接口"
# else:
#     print "[Error,数据库t_redgroup_message删除1条失败],I24_22,红包群成员_群主删除消息接口"
# curT.close(),conn.close()

#23 红包群消息_群主撤回消息接口
# I24_23("RtnOK","10001679","10001679","213",data5[0],"C23-1, 用户ID, 群ID, 消息ID")
# # C23-1,检查数据库t_redgroup_message撤回1条(messageState=2),t_redgroup_messamge_auth撤回一条(messageState=2)
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and messageState=2 and id=%s' %(data5[0]))
# data8 = curT.fetchone()
# print  data8[0]
# if data8[0]==1:
#     print "[OK,数据库t_redgroup_message撤回1条成功],I24_23,红包群消息_群主撤回消息接口"
# else:
#     print "[Error,数据库t_redgroup_message撤回1条失败],I24_23,红包群成员_群主撤回消息接口"
# curT.close(),conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and messageState=2 and messageId=%s' %(data5[0]))
# data9 = curT.fetchone()
# print  data9[0]
# if data9[0]==1:
#     print "[OK,数据库t_redgroup_messamge_auth撤回1条成功],I24_23,红包群消息_群主撤回消息接口"
# else:
#     print "[Error,数据库t_redgroup_messamge_auth撤回1条失败],I24_23,红包群成员_群主撤回消息接口"
# curT.close(),conn.close()

# I24_23("RtnOK","10001679","10001679","213","287","C23-2, 用户ID, 群ID, 消息ID")#超时撤回,App端判断,调链接不管超不超时都可撤回
# # C23-1,检查数据库t_redgroup_message撤回1条(messageState=2),t_redgroup_messamge_auth撤回一条(messageState=2)
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and messageState=2 and id=287')
# data8 = curT.fetchone()
# print  data8[0]
# if data8[0]==1:
#     print "[OK,数据库t_redgroup_message撤回1条成功],I24_23,红包群消息_群主撤回消息接口"
# else:
#     print "[Error,数据库t_redgroup_message撤回1条失败],I24_23,红包群成员_群主撤回消息接口"#超时撤回,App端判断,调链接不管超不超时都可撤回
# curT.close(),conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and messageState=2 and messageId=287')
# data9 = curT.fetchone()
# print  data9[0]
# if data9[0]==1:
#     print "[OK,数据库t_redgroup_messamge_auth撤回1条成功],I24_23,红包群消息_群主撤回消息接口"
# else:
#     print "[Error,数据库t_redgroup_messamge_auth撤回1条失败],I24_23,红包群成员_群主撤回消息接口"#超时撤回,App端判断,调链接不管超不超时都可撤回
# curT.close(),conn.close()

# I24_24("RtnOK","10001679","10001679","213","278","C24-1, 用户ID, 群ID, 消息ID")
# # C24-1,检查数据库t_redgroup_message举报1条(messageState=3),t_redgroup_messamge_auth举报一条(messageState=3)
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_message where groupId=213 and messageState=3 and id=278')
# data8 = curT.fetchone()
# print  data8[0]
# if data8[0]==1:
#     print "[OK,数据库t_redgroup_message举报1条成功],I24_24,红包群消息_群成员举报消息接口"#审核后状态变3
# else:
#     print "[Error,数据库t_redgroup_message举报1条失败],I24_24,红包群消息_群成员举报消息接口"
# curT.close(),conn.close()
# conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
# curT = conn.cursor()
# conn.set_character_set('utf8')
# curT.execute('SET NAMES utf8;')
# curT.execute('SET CHARACTER SET utf8;')
# curT.execute('SET character_set_connection=utf8;')
# curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=213 and messageState=3 and messageId=278')
# data9 = curT.fetchone()
# print  data9[0]
# if data9[0]==1:
#     print "[OK,数据库t_redgroup_messamge_auth举报1条成功],I24_24,红包群消息_群成员举报消息接口"#审核后状态变3
# else:
#     print "[Error,数据库t_redgroup_messamge_auth举报1条失败],I24_24,红包群消息_群成员举报消息接口"
# curT.close(),conn.close()

# # 25 红包群消息_我的红包群消息列表接口
# I24_25("RtnOK", "10001679","10001679", "213", "C25-1,用户ID,群ID")
# I24_25("RtnParamErr", "10001679","", "", "C25-2,用户ID(空),群ID(空)")
# I24_25("RtnParamErr", "10001679","", "213", "C25-3,用户ID(空),群ID")
# I24_25("RtnParamErr", "10001679","10001679", "", "C25-4,用户ID,群ID(空)")
# I24_25("RtnParamErr", "10001679","1", "213", "C25-5,用户ID(错),群ID")#bug
# I24_25("RtnSysErr", "10001679","10001679", "0.1", "C25-6,用户ID,群ID(错)")
# I24_25("RtnSysErr", "10001679","0", "0", "C25-7,用户ID(0),群ID(0)")
# I24_25("RtnSysErr", "10001679","-1", "-1", "C25-8,用户ID(负数),群ID(负数)")
# print "\n"

# # 26 红包群消息_我的红包群消息查看确认接口
# I24_26("RtnOK", "10001800","2016-06-23 15:48:22", "335", "C26-1,最近一条消息时间,群ID")
# I24_26("RtnParamErr", "10001800","", "", "C26-2,最近一条消息时间(空),群ID(空)")
# I24_26("RtnParamErr", "10001800","2016-06-24 15:48:22", "", "C26-3,最近一条消息时间,群ID(空)")
# I24_26("RtnParamErr", "10001800","", "213", "C26-4,最近一条消息时间(空),群ID")
# I24_26("RtnParamErr", "10001800","1290", "213", "C26-5,最近一条消息时间(错),群ID")
# I24_26("RtnParamErr", "10001800","2016-06-24 15:48:22", "0.1", "C26-6,最近一条消息时间,群ID(错)")
# I24_26("RtnParamErr", "10001800","0", "0", "C26-7,最近一条消息时间(0),群ID(0)")
# I24_26("RtnParamErr", "10001800","-1", "-1", "C26-8,最近一条消息时间(负数),群ID(负数)")
# print "\n"

# # 27 红包群消息_我关注的红包群消息列表接口
# I24_27("RtnOK", "10001483", "10001483","10001679", "213", "C27-1,用户ID,群ID,群主用户ID")
# print "\n"