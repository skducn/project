# coding: utf-8

import socket, threading, sys, time, MySQLdb, time
import time, json
import struct
from CJLinterfaceDriver import *

def uploadfile1(x):
    # 文件上传
    testURL = "https://cjl.88uka.com"
    print "121212"
    varNums = len(x.split(","))
    varLists = x.split(",")
    print varNums
    print varNums
    for k in range(1,varNums):
       print varLists[k]

    params = {varLists[2]:varLists[3], varLists[4]:open(varLists[5],'rb'), 'userId':redisUserID(myPhone)}
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
    res = opener.open(testURL + varLists[1], params)
    sleep(2)
    xx = res.read()
    if "success\":true" in xx:
        print xx
        return 0,xx
    else:
        print xx
        return 1,xx

# x = "uploadfile1,/sceneDeerUpload/upload/1.0/upload_file.do,fileType,1,files,/Users/linghuchong/Downloads/51/Picture/flying.jpg"
#
# varNums = len(x.split(","))
# varLists = x.split(",")
# eval(varLists[0])(x)

# y = '"1","2","3","4"'
# print eval(y)
#
# sleep(1212)
# for k in range(varNums):
#     print varLists[k]   // 如多余2个参数，这里是写死
# varThirdway = 1
# varRtnStatus,varJson = eval(varLists[0])(varLists[1],varLists[2],varLists[3],varLists[4],varLists[5])




    #
# sleep(1212)
## a = "2016-12-05 16:21:09"
# t = time.strptime(a, "%Y-%m-%d %H:%M:%S")
# print int(time.mktime(t)*1000)
# sleep(1212)
#
# 1480926069
# 1480926069247

#
# x = time.mktime(time.strptime(a,'%Y-%m-%d %H:%M:%S'))
# print long(x)

# sleep(1212)

# 1480926069247
#
# x = time.localtime(1480926069247)
# print time.strftime('%Y-%m-%d %H:%M:%S',x)
# sleep(1212)

# text = '{MSKS}{ASPKEPEQLRKLFIGGLSFETTD}{ESLRSAHFESSSYGSAGRRF}'
# search = '}'
# start = 0
# while True:
#     index = text.find(search, start)
#     # if search string not found, find() returns -1
#     # search is complete, break out of the while loop
#     if index == -1:
#         break
#     # print( "%s found at index %d"  % (search, index) )
#     # print list(text)
#     print text[start:index] + "}"
#     # move to next possible start position
#     start = index  + 1

# sleep(1212)
# from collections import defaultdict
# s = 'baidu zhidao zhidao baidu'
#
# d = defaultdict(lambda :0)
# for char in s:
#     d[char] += 1
#     if d[char] == 3:
#         print d(char)[:-1]
#         break
# sleep(1212)


myPhone = "18918814236"  #13816109082"
sceneId = "G_10000173"

cityID = "310100"  # 城市id
headPic = "https://cjl.dailylife365.com/pic/0000/0000/0000/0032.jpg"  # 头像
headPic2 = "https://cjl.dailylife365.com/pic/0000/0000/0000/0033.jpg"  # 头像2
nickName = "动量令狐"  # 昵称
sign = "正确做事，更要做正确的事"  #个人签名

conn= MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='scenemsg', port=3306, use_unicode=True)
conn.set_character_set('utf8')
cur = conn.cursor()
cur.execute('SET NAMES utf8;')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 用户登录
Icase("CJL1_N6_C1", "RtnOK", "123456789", '"%s","1"' %(myPhone))
Icase("CJL1_N7_C1", "RtnOK", redisVerifyCode(myPhone), '"%s","0","%s","%s"' %(myPhone,cityID,redisVerifyCode(myPhone)))
redisCheckuser = r.exists("login:app:user:" + myPhone)
if redisCheckuser: redisTmpuserid = r.hget("login:app:user:" + myPhone, "userId")
else: redisTmpuserid = r.hget("login:tmpuser:" + myPhone, "userId")
Icase("CJL1_N8_C1","RtnOK",redisTmpuserid,'"1","%s","%s","%s","%s"' %(headPic,nickName,sign,cityID))
redisCode = r.hget("app:verify:" + redisUserID(myPhone),"code")

# 25,初始化_用户获取长连接IP接口
x = Icase("CJL1_N25_C1","RtnOK",redisUserID(myPhone),'')
HOST = str(x["host"])
PORT = 16888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# 长连接场景
print ">>>" * 80
print "[长连接场景1：进入公共场景，发送消息接口]\n"
print "30 , 场景聊天_登录用户_建立长连接后初始化接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# 返回值 15=通知消息
msg6 = {"code": redisCode, "sendUserId": redisUserID(myPhone), "t": 6}
jmsg6 = json.dumps(msg6)
print jmsg6
s.send(jmsg6)
sleep(3)

print "28 , 场景聊天_登录用户_进场接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# 如果没有离线消息，则无返回值。
msg9 = {"code": redisCode,"sendUserId": redisUserID(myPhone),"sceneId": sceneId,"cityId":"310100","t": 9}
jmsg9 = json.dumps(msg9)
print jmsg9
s.send(jmsg9)
sleep(3)

print "31 , 场景聊天_发送消息接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
msg0 = {"code":redisCode,"sendUserId":redisUserID(myPhone),"tempId":12345678,"sceneId":sceneId,"content": "11111111111111111111111111111111111111>>>","msgType":1,"t": 0}
jmsg0 = json.dumps(msg0)
print jmsg0
s.send(jmsg0)
sleep(3)

print "32 , 场景聊天_接收消息接口（无入参，返回值t=0） >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# print "33 , 场景聊天_接收成功消息接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# cur.execute('select createTime from t_scene_msg where sceneId="%s" order by createTime desc limit 1' % (sceneId))
# varCreateTime = cur.fetchone()
# conn.commit()
# str = varCreateTime[0].strftime("%Y-%m-%d %H:%M:%S")
# t = time.strptime(str, "%Y-%m-%d %H:%M:%S")
# print int(time.mktime(t)*1000)
# msg5 = {
# "code": redisCode,
# "sendUserId": redisUserID(myPhone),
# "msgTime": long(time.mktime(t)*1000),
# "sceneId": sceneId,
# "t": 5
# }
# jmsg5 = json.dumps(msg5)
# print jmsg5
# s.sendall(jmsg5)
# sleep(3)



# print "t1 , 私聊_发送消息接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# msg1 = {
# "code": redisCode,
# "userId": redisUserID(myPhone),
# "acceptId": "10000074",
# "content": "hahahahahahahahahahahahahahahahahahahahahahahahahahhahahahah",
# "type": "1",
# "t": 1
# }
# jmsg1 = json.dumps(msg0)
# print jmsg1
# s.sendall(jmsg1)
# sleep(1)
# print "\n"

# print "t10 , 场景聊天_登录用户_出场接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# msg10 = {
# "code": redisCode,
# "sendUserId": redisUserID(myPhone),
# "sceneId": sceneId,
# "cityId":"310100",
# "t": 10
# }
# jmsg10 = json.dumps(msg10)
# print jmsg10
# s.sendall(jmsg10)
# sleep(1)
# print "\n"

while 1:
    data = s.recv(10000)
    if data:
        search = '}'
        start = 0
        print "返回值 => "
        while True:
            index = data.find(search, start)
            if index == -1:
                break
            print data[start:index] + "}\n"
            if "\"t\":4" in data[start:index]:
                xx = data[start:index] + "}"
                varcreateTime = eval(xx).get("createTime")
                # break
            start = index + 1
        print "\n"
        # print "返回值 => " + data
    else:
        break

s.shutdown(socket.SHUT_RDWR)
s.close()

print varcreateTime

# s.sendall(struct.pack('s', jmsg3))
# s.sendall(struct.pack('s', '')+jmsg3)
