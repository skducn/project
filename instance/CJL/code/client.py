# -*- coding: UTF-8 -*-
# import socket,struct
# import threading
# import SocketServer
# import json,sys
# # reload(sys)
# # sys.setdefaultencoding('utf8')
# from time import sleep
#
# from CJLinterfaceDriver import *
# myPhone = "13816109080"
# cityID = "310100"  # 城市id
# headPic = "https://cjl.dailylife365.com/pic/0000/0000/0000/0032.jpg"  # 头像
# headPic2 = "https://cjl.dailylife365.com/pic/0000/0000/0000/0033.jpg"  # 头像2
# nickName = "动量令狐"  # 昵称
# sign = "正确做事，更要做正确的事"  #个人签名
# Icase("CJL1_N6_C1", "RtnOK", "123456789", '"%s","1"' %(myPhone))
# Icase("CJL1_N7_C1", "RtnOK", redisVerifyCode(myPhone), '"%s","0","%s","%s"' %(myPhone,cityID,redisVerifyCode(myPhone)))
# redisCheckuser = r.exists("login:app:user:" + myPhone)
# if redisCheckuser: redisTmpuserid = r.hget("login:app:user:" + myPhone, "userId")
# else: redisTmpuserid = r.hget("login:tmpuser:" + myPhone, "userId")
# Icase("CJL1_N8_C1","RtnOK",redisTmpuserid,'"1","%s","%s","%s","%s"' %(headPic,nickName,sign,cityID))
# redisCode = r.hget("app:verify:" + redisUserID(myPhone),"code")
#
# # 场景聊天_登录用户_建立长连接后初始化接口
# msg1 = {"code": redisCode, "sendUserId": redisUserID(myPhone), "t": 6}
# print msg1
# print type(msg1)
# jmsg1 = json.dumps(msg1)
# print jmsg1
# print type(jmsg1)
# print "~~~~~~~~~~~~~~~~~~~~~~~~"
#
# msg2 ={
# "code": redisCode,
# "sendUserId": redisUserID(myPhone),
# "tempId":1234567,
# "sceneId": "G_10000341",
# "content": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa>>>",
# "msgType ": 1,
# "t": 0
# }
# jmsg2 = json.dumps(msg2)
#
#
# # print len(jmsg1)
#
#
# # str0 = struct.pack('is',len(jmsg1), jmsg1)
# # print len(str0)
# # buffer, = struct.unpack('5s', str0)
# # print buffer
#
#
# # address = ('192.168.2.113', 16888)
# #
# # # address = ('127.0.0.1', 31500)
# # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # json_string = json.dumps(mylist)
# # s.sendto(json_string, address)
# # # s.shutdown(socket.SHUT_RDWR)
# # s.close()
# # import binascii
# #
# #
# def client(message):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.connect(('192.168.2.113', 16888))
#
#     try:
#         address = ('192.168.2.113', 16888)
#
#         # print "Send: {}".format(message)
#         sock.send(b'hello')
#         # sock.sendto(message)
#         # mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         # json_string = json.dumps(message)
#         # sock.sendto(json_string, address)
#         reply = sock.recv(1024)
#         sock.close()
#         print (repr(reply))
#
#         while True:
#             buf = sock.recv(500)
#             if not len(buf):
#                 break
#             print buf
#
#         # jresp = json.loads(response)
#         # print "Recv: ",jresp
#
#         print "~~~~~~"
#
#         # while True:
#         #     a = sock.recv(1024)
#         #     if not len(a):break
#         # print "123"
#         #
#         # response = sock.recv(1024)
#         # # response = sock.setblocking(0)
#         # jresp = json.loads(response)
#         # print "Recv: ",jresp
#
#
#         # json_string, addr = sock.recvfrom(2048)
#         # mylist = json.loads(json_string)
#         # print mylist
#         # sock.shutdown(socket.SHUT_RDWR)
#
#
#     finally:
#         sock.close()
#
# client(jmsg2)


#
#
#
#

#
# s = struct.Struct('I3sf')
# packed_data = s.pack(*jmsg1)
# unpacked_data = s.unpack(packed_data)
#
# print 'Original values:', jmsg1
# print 'Format string :', s.format
# print 'Uses :', s.size, 'bytes'
# print 'Packed Value :', binascii.hexlify(packed_data)
# print 'Unpacked Type :', type(unpacked_data), ' Value:', unpacked_data
#
# sleep(1212)
#
# # print repr(str)
# #
# # print repr(jmsg1)
# # print jmsg1
# # print "~~~~~~~~"
#
# # a = 80
# # str = struct.pack('i',a)
# # print len(str)
# # print repr(str)
# # format = '!%i' % len(jmsg1)
# # buffer = struct.pack("!i4s",len(jmsg1), str)
#
# # struct.calcsize(format)
#
# # decode_json = json.loads(jmsg1)
# # print type(decode_json) #查看一下解码后的对象类型
# # print decode_json #输出结果
#
#
#
#
#
#

import socket
HOST='192.168.2.64'
PORT= 52378
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      #定义socket类型，网络通信，TCP
s.connect((HOST,PORT))       #要连接的IP与端口
while 1:
       cmd=raw_input("Please input cmd:")       #与人交互，输入命令
       s.sendall(cmd)      #把命令发送给对端
       data=s.recv(1024)     #把接收的数据定义为变量
       print data         #输出变量
s.close()   #关闭连接


#
# #coding=utf-8
#
# import socket
# import time
# from time import sleep
# host = '192.168.2.113'
# port = 16888
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护
# client.connect((host, port))
# while True:
#     client.send('hello world\r\n'.encode())
#     print('send data')
#     time.sleep(1) #如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点
#
# sleep(1212)
#
#
# import socket,struct
#
#
# HOST = "192.168.2.113"                 # Symbolic name meaning all available interfaces
# PORT = 16888              # Arbitrary non-privileged port
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# conn, addr = s.accept()
# print 'Connected by', addr
# while 1:
#     data = conn.recv(1024)
#     if not data: break
#     conn.sendall(data)
# conn.close()
#
# sleep(1212)
#
# import httplib
#
# httpClient = httplib.HTTPConnection('127.0.0.1', 8090)
# for url in url_for_mem_list:
#     httpClient.request('GET', '/hot' + url[4:], "", {"Connection":"Keep-Alive"})
#     response = httpClient.getresponse()
# response.read()
#
# sleep(1212)
#
# import socket
# import struct
# BUF_SIZE = 1024
# host = '192.168.2.113'
# port = 16888
#
#
# def Ip2Int(host):
#     return struct.unpack("!I",socket.inet_aton(host))[0]
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((socket.ntohl(struct.unpack("i",socket.inet_aton(host))[0]), socket.htons(port)))
# server.listen(1) #接收的连接数
# client, address = server.accept() #因为设置了接收连接数为1，所以不需要放在循环中接收
# while True: #循环收发数据包，长连接
#     data = client.recv(BUF_SIZE)
#     print(data.decode()) #python3 要使用decode
#     # client.close() #连接不断开，长连接
#



# import socket




# HOST = 'https://cjl.dailylife365.com/sceneMsg/initAction/1.0/initHost.do'    # The remote host
# PORT = 8080             # The same port as used by the server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))
# s.sendall({"code" : "2033ffb8c51040ee9bd4a48204345d52","sendUserId" : "10000014","sceneId" : "G_10000092","t":"9"})
# data = s.recv(1024)
# s.close()
# print 'Received', repr(data)

#
# HOST = ''                # Symbolic name meaning all available interfaces
# PORT = 16888              # Arbitrary non-privileged port
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# conn, addr = s.accept()
# print 'Connected by', addr
# while 1:
#     data = conn.recv(1024)
#     if not data: break
#     conn.sendall(data)
# conn.close()

# import socket

# HOST = '192.168.2.113'    # The remote host
# PORT = 16888             # The same port as used by the server
# import socket

# address = ('192.168.2.113', 16888)
# # # https://cjl.dailylife365.com/sceneMsg/initAction/1.0/initHost.do

# import socket
# s=socket.socket()
# s.connect(('192.168.2.113',16888))   #与服务器程序ip地址和端口号相同
# data=s.recv(512)
# s.send('hihi')
# s.close()
# print 'the data received is',data


# import urllib,unittest
#
# class PressureTest(unittest.TestCase):
#     times=100
#     data='''
#         <?xml version="1.0" encoding="UTF-8"?>
#         <message >
#         </message>
#         '''
#
#     def testSend(self):
#          import httplib
#          headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","Connection":"Keep-Alive"}
#          conn = httplib.HTTPConnection("192.168.31.124",16888)
#          for i in range(self.times):
#              conn.request("POST", "https://cjl.dailylife365.com/sceneMsg/initAction/1.0/initHost.do", self.data, headers)
#              response = conn.getresponse()
#              response.read()
#          conn.close()
#
# if __name__ == "__main__":
#      unittest.main()


#coding=gbk
#
# import socket
# import sys
# import time
#
# if __name__=='__main__':
#
#     try :
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     except socket.eorror,e:
#         print 'socket false:%s'%e
#     print 'socket ...'
#
#
#     try :
#         sock.connect(('220.18.111.148',80))
#     except socket.error,e:
#         print 'connect false %s'%e
#         sock.close()
#     print 'connect ...'
#
#     try :
#         print 'send start...'
#         str='GET / HTTP/1.1\r\nHost:www.baidu1.com\r\nConnection:keep-alive\r\n\r\n'
#         sock.send(str)
#     except socket.eorror,e:
#         print 'send false'
#         sock.close()
#
#     data=''
#     data = sock.recv(1024)
#     while (1):
#
#         print data
#         beg = data.find('Content-Length:',0,len(data))
#         end = data.find('Content-Type:',0,len(data))
#         print beg
#         print end
#         if(beg == end):
#             print 'connecting closed'
#             break
#         num = long(data[beg+16:end-2])
#         print num
#         nums = 0
#         while (1):
#             data=sock.recv(1024)
#             print data
#             nums +=len(data)
#             if(nums >= num):
#                 break
#         word = raw_input('please input your word----->')
#         str='''''GET /s?wd=''' + word + ''''' HTTP/1.1
# Host:www.baidu.com
# Connection: Keep-Alive
#
# '''
#         print str
#         sock.send(str)
#         data = ''
#         data = sock.recv(1024)
#     sock.close()
#     print data



#
# import urllib3,unittest
# class PressureTest(unittest.TestCase):
#     times=100
#     data='''
#         <?xml version="1.0" encoding="UTF-8"?>
#         <message >
#         </message>
#         '''
#
#     def testSend(self):
#         import httplib
#         headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","Connection":"Keep-Alive"}
#         conn = httplib.HTTPConnection("192.168.31.124",16888)
#         for i in range(self.times):
#             conn.request("POST", "https://cjl.dailylife365.com/sceneMsg/initAction/1.0/initHost.do", self.data, headers)
#             response = conn.getresponse()
#             response.read()
#         conn.close()
# if __name__ == "__main__":
#     unittest.main()