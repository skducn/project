# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-6-7
# Description: 党建接口
# https://md5jiami.51240.com/  MD5在线加密
# *******************************************************************************************************************************

import os, sys,requests, xlwt, xlrd, MySQLdb, redis, urllib3, random, time, MultipartPostHandler, cookielib, string ,datetime, smtplib,urllib,urllib2,json,md5,base64,hashlib
from time import sleep
reload(sys)
sys.setdefaultencoding('utf8')

from CETCinterfaceDriver import *


varPhone = "13816109050"
varPass = "123456"

# varPhone = "13918794888"
# varPass = "123"

def response(*rtnMessageStatus):
    m1 = md5.new()
    # m1.update(json.dumps(varParam).replace(" ", "") + "123456")
    m1.update(varParam + "123456")
    values = {"check": m1.hexdigest(), "json": varParam}
    resp = urllib2.urlopen(urllib2.Request(url, json.dumps(values))).read()
    if u"操作成功" in str(resp):
        print u"[result] => [OK]"
        if rtnMessageStatus == ('Y',) :
            print u"[url] => " + url
            print u"[param] => " + str(values)
            print u"[result] => " + str(resp)
    else:
        print u"[url] => " + url
        print u"[param] => " + str(values)
        print u"[result] => " + str(resp)
    return resp

# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# print u"[党建 - 登录]"
# url = 'http://10.111.3.5:8082/dangjian/v1/user/login'
# myMd5 = hashlib.md5()
# myMd5.update(varPass)
# myMd5_Digest = myMd5.hexdigest()
# varParam = "{\"passWord\":\"" + myMd5_Digest + "\",\"phoneNumber\":\"" + varPhone + "\"}"
# print varParam
# resp = response('Y')
#
# m1 = md5.new()
# # m1.update(json.dumps(varParam).replace(" ", "") + "123456")
# m1.update(varParam + "123456")
# values = {"check": m1.hexdigest(), "json": varParam}
# resp = urllib2.urlopen(urllib2.Request(url, json.dumps(values))).read()
# if u"操作成功" in str(resp):
#     print u"[result] => [OK]"
#     # if rtnMessageStatus == ('Y',):
#     print u"[url] => " + url
#     print u"[param] => " + str(values)
#     print u"[result] => " + str(resp)
# else:
#     print u"[url] => " + url
#     print u"[param] => " + str(values)
#     print u"[result] => " + str(resp)
#
#
# varUserId = resp.split("userId\":\"")[1].split("\"")[0]
# varSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
# varImVoip = resp.split("imVoip\":\"")[1].split("\"")[0]

# sleep(1212)
# 1，登录>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nDKDJ1_N1 " + ">" * 150
# 业务场景描述
myMd5 = hashlib.md5()
myMd5.update("123456")
myMd5_Digest = myMd5.hexdigest()

resp = Icase("i1_N1_C1", myMd5_Digest,"13816109050")

varUserId = resp.split("userId\":\"")[1].split("\"")[0]
varSessionId = resp.split("userSessionId\":\"")[1].split("\"")[0]
varImVoip = resp.split("imVoip\":\"")[1].split("\"")[0]
# print varUserId
# print varSessionId
# print varImVoip

# 2，侧边栏消息中的通知>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nDKDJ1_N2 " + ">" * 150
resp = Icase("i1_N2_C1", varUserId, varSessionId, "1", "20")


# 3，侧边栏消息中的提醒>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nDKDJ1_N3 " + ">" * 150
resp = Icase("i1_N3_C1", varUserId, varSessionId, "1", "20")


# 4，侧边栏消息通知中查看会议>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nDKDJ1_N4 " + ">" * 150
resp = Icase("i1_N4_C1", varUserId, varSessionId,"190")


# 5，随时学首页>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nDKDJ1_N5 " + ">" * 150
resp = Icase("i1_N5_C1", varUserId, varSessionId, "0", "1", "20")




# print "\nDKDJ1_N4 " + ">" * 150
#
# resp = Icase("i1_N4_C1", "20")
#
# print "\nDKDJ1_N5 " + ">" * 150
#
# resp = Icase("i1_N5_C1", "20")
#
# print "\nDKDJ1_N6 " + ">" * 150
#
# resp = Icase("i1_N6_C1", "20")

sleep(1212)





print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 首页]"
url = 'http://43.254.24.107:8080/dangjian/v1/home/homePage'
varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - IM推送]"
url = 'http://43.254.24.107:8080/dangjian/v1/group/IMPush'
varParam = "{\"imVoip\":\"" + varImVoip + "\",\"msgContent\":\"" + varSessionId + "\"}"
response('Y')

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



print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 随时学-学习历史记录列表]"
url = 'http://43.254.24.107:8080/dangjian/v1/anyMomentStudy/historyList'
varParam = "{\"userId\":\"" + varUserId + "\",\"flag\":\"0\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
response()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 随时学]"
url = 'http://43.254.24.107:8080/dangjian/v1/anyMomentStudy/homePage'
varParam = "{\"userId\":\"" + varUserId + "\",\"flag\":\"0\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 猜你喜欢换一组]"
url = 'http://43.254.24.107:8080/dangjian/v1/anyMomentStudy/otherLike'
varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
response()

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 消息盒子-通知]"
url = 'http://43.254.24.107:8080/dangjian/v1/sysMessage/noticeList'
varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 消息盒子-提醒]"
url = 'http://43.254.24.107:8080/dangjian/v1/sysMessage/remindList'
varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"20\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[???党建 - 消息盒子-未读消息数]"
url = 'http://43.254.24.107:8080/dangjian/v1/sysMessage/readMsgCount'
varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 学习计划列表]"
url = 'http://43.254.24.107:8080/dangjian/v1/learn/getLearnPlan'
varParam = "{\"userId\":\"" + varUserId + "\",\"companyType\":\"1\",\"planType\":\"1\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 学习项目排行榜]"
url = 'http://43.254.24.107:8080/dangjian/v1/learn/getProjectRanking'
varParam = "{\"userId\":\"" + varUserId + "\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 音频列表]"
url = 'http://43.254.24.107:8080/dangjian/v1/source/audioList'
varParam = "{\"userId\":\"" + varUserId + "\",\"typeId\":\"0\",\"pageNum\":\"1\",\"pageSize\":\"1\",\"userSessionId\":\"" + varSessionId + "\"}"
response()


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print u"[党建 - 我的讨论小组]"
url = 'http://43.254.24.107:8080/dangjian/v1/group/getGroupList'
varParam = "{\"userId\":\"" + varUserId + "\",\"pageNum\":\"1\",\"pageSize\":\"10\",\"userSessionId\":\"" + varSessionId + "\"}"
response('Y')


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

