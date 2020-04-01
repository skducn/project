# coding: utf-8

import socket,threading,sys
import time, json
import struct
from CJLinterfaceDriver import *

myPhone = "13816109080"
cityID = "310100"  # 城市id
headPic = "https://cjl.dailylife365.com/pic/0000/0000/0000/0032.jpg"  # 头像
headPic2 = "https://cjl.dailylife365.com/pic/0000/0000/0000/0033.jpg"  # 头像2
nickName = "动量令狐"  # 昵称
sign = "正确做事，更要做正确的事"  #个人签名
sceneId = "G_10000341"


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 用户登录
Icase("CJL1_N6_C1", "RtnOK", "123456789", '"%s","1"' %(myPhone))
Icase("CJL1_N7_C1", "RtnOK", redisVerifyCode(myPhone), '"%s","0","%s","%s"' %(myPhone,cityID,redisVerifyCode(myPhone)))
redisCheckuser = r.exists("login:app:user:" + myPhone)
if redisCheckuser: redisTmpuserid = r.hget("login:app:user:" + myPhone, "userId")
else: redisTmpuserid = r.hget("login:tmpuser:" + myPhone, "userId")
Icase("CJL1_N8_C1","RtnOK",redisTmpuserid,'"1","%s","%s","%s","%s"' %(headPic,nickName,sign,cityID))
redisCode = r.hget("app:verify:" + redisUserID(myPhone),"code")

HOST = '192.168.2.113'
PORT = 16888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# 长连接场景
print ">>>" * 80
print "[长连接场景1：进入公共场景，发送消息接口]\n"

print "t6 , 场景聊天_登录用户_建立长连接后初始化接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
msg6 = {"code": redisCode, "sendUserId": redisUserID(myPhone), "t": 6}
# msg6 = {"code": "c3e5c21c9125474bbacc002fb8f9caa3", "sendUserId": "10000004", "t": 6}
jmsg6 = json.dumps(msg6)
print jmsg6
s.send(jmsg6)
sleep(3)
print "\n"

print "t9 , 场景聊天_登录用户_进场接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
msg9 = {"code": redisCode,"sendUserId": redisUserID(myPhone),"sceneId": sceneId,"t": 9}
# msg9 = {"code": "c3e5c21c9125474bbacc002fb8f9caa3", "sendUserId": "10000004","sceneId": sceneId,"t": 9}
jmsg9 = json.dumps(msg9)
print jmsg9
s.send(jmsg9)
sleep(3)
print "\n"

print "t0 , 场景聊天_发送消息接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
msg0 = {"code":redisCode,"sendUserId":redisUserID(myPhone),"tempId":12345678,"sceneId":sceneId,"content": "2222222222222222222222222222222222222222>>>","msgType":1,"t": 0}
# msg0 = {"code": "c3e5c21c9125474bbacc002fb8f9caa3","sendUserId": "10000004","tempId": 12345678,"sceneId": sceneId,"content": "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm>>>","msgType ": 1,"t": 0}
jmsg0 = json.dumps(msg0)
print jmsg0
s.send(jmsg0)
sleep(3)
print "\n"

# print "t5 , 场景聊天_接收成功消息接口 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# msg5 = {
# "code": redisCode,
# "sendUserId": redisUserID(myPhone),
# "msgTime": 147898898767,
# "sceneId": sceneId,
# "t": 5
# }
# jmsg5 = json.dumps(msg0)
# print jmsg5
# s.sendall(jmsg5)
# sleep(3)
# print "\n"



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
# "t": 10
# }
# jmsg10 = json.dumps(msg10)
# print jmsg10
# s.sendall(jmsg10)
# sleep(1)
# print "\n"

while 1:
    data = s.recv(1024)
    if data:
        print "返回值 => " + data
    else:
        break
s.shutdown(socket.SHUT_RDWR)
s.close()

# s.sendall(struct.pack('s', jmsg3))
# s.sendall(struct.pack('s', '')+jmsg3)
