# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-6-26
# Description: 医云谷 - 医务端(药师）
# https://md5jiami.51240.com/  MD5在线加密
# *******************************************************************************************************************************

from YYGinterfaceDriver import *
myMd5 = hashlib.md5()
myMd5.update(varPass)
myMd5_Digest = myMd5.hexdigest()


def response(interName, interUrl, interParam, *rtnMessageStatus):
    m1 = md5.new()
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


# 发送验证码
resp = response(u"发送验证码",'/v1/system/getSMSCode',"{\"codeType\":\"register\",\"phoneNumber\":\"" + varPhone + "\"}",'y')
redisCode = connRedis5.get("register_" + varPhone)
print u"////////// " + varPhone + u'的验证码 = ' + str(redisCode)

# 检验验证码, 验证码在redis，db1，register_13816109055
resp = response(u"[检验验证码]",'/v1/system/checkCode',"{\"codeType\":\"register\",\"phoneNumber\":\"" + varPhone + "\",\"code\":\"" + str(redisCode) + "\"}","y")


# 药师登录
resp = response(u"[登录]",'/v1/user/login',"{\"phoneNumber\":\"" + varPhoneYaoshi + "\",\"passWord\":\"" + myMd5_Digest + "\",\"identityType\":\"2\"}",'y')
varUserId = resp.split("userId\":\"")[1].split("\"")[0]
varUserSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
print u'////////// varUserId = ' + varUserId
print u'////////// varUserSessionId = ' + varUserSessionId


resp = response(u"[药师首页]",'/v1/user/pharmacistHome',"{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varUserSessionId + "\",\"pageSize\":\"1\",\"pageNum\":\"1\"}",'y')












