# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2019-1-8
# Description: ChainMap
# ********************************************************************************************************************

from PO.TimePO import *
Time_PO = TimePO()

x = '../report/saas_' + str(Time_PO.getDatetime()) + '.html'
print(x)

#
# def abc(x):
#     if x == 1:
#         print(11111)
#         return True
#     else:
#         print(22222)
#         return False
#
# exec("x = abc(1)")
# print(x)

for i in range(111):
    if i == 5:
        exit()
    else:
        print(i)


# varRule = "11222"
# varQty = varRule.split(",")
# print(len(varQty))

# def x(*aa):
#     pass
#     print(aa[1])


# x("a","b","c")

# l_basic = ['问题数：19', '联系人姓名:', '(联系人姓名未填写)', '联系人电话:', '(联系人电话未填写)', '文化程度:', '大学本科', '(文化程度超出字典范围)', '生活环境_禽畜栏:', '(禽畜栏未填写)', '生活环境_燃料类型:', '其他', '(燃料类型超出字典范围)', '生活环境_厨房排风设施:', '(厨房排风设施超出字典范围)', '生活环境_厕所:', '(厕所未填写)', '生活环境_饮水:', '其他', '(饮水超出字典范围)', '家族史子女:', '(家族史（子女）未填写)', '既往史输血:', '无', '(既往史输血时间未填写)', '既往史手术:', '无', '(既往史手术时间未填写)', '既往史外伤:', '无', '(既往史外伤时间未填写)', '婚姻状况:', '(婚姻状况未填写)', '民族:', '(民族填写错误;民族超出字典范围)', '职业:', '(职业未填写)', '本人电话:', '(本人电话未填写)', 'RH血型编号:', '不详', '(RH超出字典范围)', '工作单位:', '(工作单位未填写)', '医疗支付方式:', '(医疗费用支付方式未填写)', '健康档案封面']
# ll = []
# for i in range(len(l_basic)):
#     if i < len(l_basic):
#         if ":" in l_basic[i] and "(" not in l_basic[i + 1]:
#             ll.append(l_basic[i] + l_basic[i + 1])
#             l_basic.pop(i + 1)
#         else:
#             ll.append(l_basic[i])
#
# print(ll.pop(0))
# dict1 = List_PO.list2dictBySerial(ll)
# for k in dict1:
#     print(k, dict1[k])


# import collections
# from math import hypot
# from random import choice
#
# Card = collections.namedtuple('Card', ['rank', 'suit'])
#
# class PokeDeck(object):
#     ranks = [str(n) for n in range(2, 11)] + list('JQKA')
#     suits = ['spades', 'diamonds', 'clubs', 'hearts']
#
#     def __init__(self):
#         self._card = [Card(rank, suit) for rank in self.ranks
#                                        for suit in self.suits]
#
#     def __len__(self):
#         return len(self._card)
#
#     def __getitem__(self, item):
#         return self._card[item]
#
#     def __repr__(self):
#         return "This is a deck"
#
# card = PokeDeck()
# print(card)
# print(card[0])
# print(len(card))
# print(choice(card))


# import pyttsx3
# engine = pyttsx3.init()
# rate = engine.getProperty('rate')
# engine.setProperty('rate', rate-55)
# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()
#
#
# """
# 本地语音文件识别测试
# """
# import speech_recognition as sr
# import sys
#
# say = '你看看'
# r = sr.Recognizer()
#
# # 本地语音测试
# harvard = sr.AudioFile(sys.path[0]+'/youseesee.wav')
# with harvard as source:
#     # 去噪
#     r.adjust_for_ambient_noise(source, duration=0.2)
#     audio = r.record(source)
#
# # 语音识别
# test = r.recognize_google(audio, language="cmn-Hans-CN", show_all=True)
# print(test)
#
# # 分析语音
# flag = False
# for t in test['alternative']:
#     print(t)
#     if say in t['transcript']:
#         flag = True
#         break
# if flag:
#     print('Bingo')

# engine = pyttsx3.init()
# engine.say("风飘荡，雨濛茸，翠条柔弱花头重")
# engine.runAndWait()



import imghdr

# if __name__ == '__main__':
#     # 检测一个文件
#     with open('D:/test/123.jpg', 'rb') as img_file:
#         print(imghdr.what(img_file))

import imghdr
import urllib3
import uuid
#
#
# class Spider:
#
#     pool_manager = urllib3.PoolManager()
#
#     @staticmethod
#     def get(url):
#         return Spider.pool_manager.urlopen('GET', url)
#
#
# class ImageDownLoader:
#     """
#     图片下载器
#     """
#
#     @staticmethod
#     def download(url, path):
#         """
#         这个方法用来下载图片并保存
#         :param url:  图片的路径
#         :param path: 要保存到的路径
#         :return:
#         """
#         response = Spider.get(url)
#         save_name = path + uuid.uuid1().hex + "." + imghdr.what(None, response.data)
#         with open(save_name, 'wb') as img_file:
#             img_file.write(response.data)
#
#
# if __name__ == '__main__':
#     ImageDownLoader.download('http://img3.doubanio.com/view/photo/albumcover/public/p2327732376.webp', 'D:/')
#     with open('D:/e5c59ac59b4311eaa1a0505bc2b637ea.webp', 'rb') as img_file:
#         print(imghdr.what(img_file))




# import os,shutil,datetime
# # from time import sleep
# # import paramiko
# # import signal
# # import subprocess
# # import time
#
#
# import operator
# class People :
#      age = 0
#      gender = 'male'
#
#      def __init__(self, age, gender ):
#          self.age = age
#          self.gender = gender
#      def toString ( self ):
#          return 'Age:' + str( self.age ) + ' /t Gender:' + self.gender
#
# List = [ People ( 21 , 'male' ), People ( 20 , 'famale' ), People ( 34 , 'male' ), People ( 19 , 'famale' )]
# print ('Befor sort:')
# for p in List :
#     print(p.toString())
#
# # key=lambda p1,p2: operator.eq(p1.age,p2.age)
# # List.sort(key(1,1))
#
# L = [('b',6),('a',1),('c',3),('d',4)]
# print(L.sort(key=lambda x,y:operator.eq(x[1],y[1])))

# List.sort(key=lambda p1,p2 : operator.eq(p1.age,p2.age))
# # List.sort(lambda p1,p2:operator.eq(p1.age, p2.age))
# print (' /n After ascending sort:')
# for p in List :
#     print(p.toString())
#
# # List . sort ( lambda p1 , p2 : - operator.eq ( p1 . age , p2 . age ))
# # print (' /n After descending sort:')
# # for p in List :
# #     print (p . toString () )
#
# #
#

# logFile1 = "/dkvlm/tomcat_yygdoctor/logs/catalina.out"
# logFile2 = 'test2.log'
#
#
# # 日志文件一般是按天产生，则通过在程序中判断文件的产生日期与当前时间，更换监控的日志文件
# # 程序只是简单的示例一下，监控test1.log 10秒，转向监控test2.log
# def monitorLog(logFile):
#     print '监控的日志文件 是%s' % logFile
#     # 程序运行10秒，监控另一个日志
#     stoptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 10))
#     popen = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     pid = popen.pid
#     print('Popen.pid:' + str(pid))
#     while True:
#         line = popen.stdout.readline().strip()
#         print line
#         # 判断内容是否为空
#         if line:
#             print(line)
#             # 当前时间
#         thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         if thistime >= stoptime:
#             # 终止子进程
#             popen.kill()
#             print '杀死subprocess'
#             break
#     time.sleep(2)
#     monitorLog(logFile2)
#
#
# monitorLog(logFile1)
#
# sleep(1212)
#
# remotedir = "/root"
# remotefile = "/root/log_history.txt"
# hostname = "10.111.3.6"
# port = 22
# username = "root"
# password = "gen"
#
# paramiko.util.log_to_file('paramiko.log')
# s = paramiko.SSHClient()
# s.load_system_host_keys()
#
# s.connect(hostname,port,username,password)
# command = 'tail -f /dkvlm/tomcat_yygdoctor/logs/catalina.out'
# #command = 'df -h'
# stdin,stdout,stderr = s.exec_command(command)
# #print(2,stdout.read())
# logs = stdout.readlines()
# for i in range(len(logs)):
#     print(logs[i].rstrip())
# s.close()
#
# sleep(1212)
#
#
#
# import pexpect
#
# import paramiko
# import threading
# def ssh2(ip,username,passwd,cmd):
#   try:
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(ip,22,username,passwd,timeout=5)
#     for m in cmd:
#       stdin, stdout, stderr = ssh.exec_command(m)
# #      stdin.write("Y")  #简单交互，输入 ‘Y'
#       out = stdout.readlines()
#       #屏幕输出
#       for o in out:
#         print o,
#     print '%s\tOK\n'%(ip)
#     ssh.close()
#   except :
#     print '%s\tError\n'%(ip)
#
# ssh2("10.111.3.6", "root", "gen", ['tail -f /dkvlm/tomcat_yygdoctor/logs/catalina.out','echo hello!'])
#
# sleep(1212)
#
# def ssh_cmd(ip, user, passwd, cmd):
#     ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
#     try:
#         i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
#         if i == 0:
#             ssh.sendline(passwd)
#             r = ssh.read()
#         elif i == 1:
#             ssh.sendline('yes\n')
#             ssh.expect('password: ')
#             ssh.sendline(passwd)
#             r = ssh.read()
#     except pexpect.EOF:
#         ssh.close()
#     return r
#
#
# hosts = '''
# 10.111.3.6:root:gen:tail -f,//dkvlm//tomcat_yygdoctor//logs//catalina.out
# 10.111.3.6:root:gen:ls
# '''
#
# for host in hosts.split("\n"):
#     if host:
#         ip, user, passwd, cmds = host.split(":")
#         for cmd in cmds.split(","):
#             print "-- %s run:%s --" % (ip, cmd)
#             print ssh_cmd(ip, user, passwd, cmd)
#
#
# sleep(1212)
#
#
# import ftplib
# connect = ftplib.FTP("10.111.3.6")
# connect.login("root", "gen")
# data = []
# connect.dir(data.append)
# connect.quit()
# for line in data:
#    print(line)
#
# sleep(1212)
#
# x = 88888888110
#
# for i in range(1000):
#      sum = x + i
#      tmp = u"a" + str(sum) + u"z"
#      tmp1 = tmp.replace("a",'"').replace("z",'"')
#      print tmp1
# sleep(1212)
#
#

#
#
#

#


# # json与python中dict互相转换，把dict转换成json-使用json.dumps()，将json转换为dict-使用json.loads()
# eth = {}
# eth['eth0'] = "192.168.2.12"
# eth['eth1'] = "192.168.212.12"
# print eth
# import json
# ethjson = json.dumps(eth)
# print type(ethjson)
# print ethjson
# ethdict = json.loads(ethjson)
# print ethdict
# print ethdict['eth0'], ethdict['eth1']
#
# # 结果:
# # {'eth1': '192.168.212.12', 'eth0': '192.168.2.12'}
# # <type 'str'>
# # {"eth1": "192.168.212.12", "eth0": "192.168.2.12"}
# # {u'eth1': u'192.168.212.12', u'eth0': u'192.168.2.12'}
# # 192.168.2.12 192.168.212.12
#
# a=[1,2,3]
# b=[4,5,4]
# # a.append(b)
# # print a
# a.extend(b)
# print a
# del a[3]
# print a
# a.pop()
# print a
# a.remove(3)
# print a