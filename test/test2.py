# -*- coding: utf-8 -*-

import os,shutil,datetime
# from time import sleep
# import paramiko
# import signal
# import subprocess
# import time

from functools import reduce

# 一行代码解决10阶乘(10!=1*2*3....*10)
print(reduce(lambda x, y: x * y, range(1, 11)))  # 3628800

import operator
class People :
     age = 0
     gender = 'male'

     def __init__(self, age, gender ):
         self.age = age
         self.gender = gender
     def toString ( self ):
         return 'Age:' + str( self.age ) + ' /t Gender:' + self.gender

List = [ People ( 21 , 'male' ), People ( 20 , 'famale' ), People ( 34 , 'male' ), People ( 19 , 'famale' )]
print ('Befor sort:')
for p in List :
    print(p.toString())

# key=lambda p1,p2: operator.eq(p1.age,p2.age)
# List.sort(key(1,1))

L = [('b',6),('a',1),('c',3),('d',4)]
print(L.sort(key=lambda x,y:operator.eq(x[1],y[1])))

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
# # 88888888881 - 88888883225
# # x= 1
# # for i in range(0,3000):
# #     y = 88888881000 + i
# #     print '"' + str(y) + '"'
# #     # print y
# # sleep(1212)
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
# print os.getcwd()
#
# # varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S');  #20160623183734
# varTimeYMD = datetime.datetime.now().strftime('%Y-%m-%d')  # 20160628
# print varTimeYMD
# # varTimeY_M_D = datetime.datetime.now().strftime('%Y-%m-%d'); # 2016-06-28 00:00:01
# # varTimeFrom = varTimeY_M_D +" 00:00:01"
# # varTimeEnd = varTimeY_M_D+" 23:59:59"
#
# varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S');  #20160623183734
# print "自动" + varTimeYMDHSM
# sleep(1212)
#
#
#
#
# # ============= 判断一个list是否为空
# mylist=[]
# # 方法1
# if len(mylist):
#     pass
# else:
#     print "empty"
# # 方法2
# if mylist:
#     pass
# else:
#     print "empty2"
#
# # ============= 遍历list同时获取索引
# mylist = [['abc'],['cde\n']]
# i=0
# for element in mylist:
#     i+=1
#     print i     #结果1 2 ,表示有2个元素
#     print element
#     print element[0]
# # 结果:
# # 1
# # ['abc']
# # abc
# # 2
# # ['cde\n']
# # cde
#
# for i,element in enumerate(mylist):
#     i+=1
#     print i
#     print element
#     print element[0]
# # 结果: 同上
#
# # ============= list解析,输出1-9 的2次方值
# squares = [x**2 for x in range(1,10)]
# print squares
# # 结果:[1, 4, 9, 16, 25, 36, 49, 64, 81]
#
# # ============= list解析,找出100以内的能够被3整除的正整数
# aliquot = [n for n in range(1,100) if n%3==0]
# print aliquot
# # 结果:[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]
# # 传统做法:
# aliquot = []  # 必须先初始化列表
# for n in range(1,100):
#   if n%3 == 0:
#     aliquot.append(n)
# print aliquot
# # 结果:[3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]
#
# # ============= list解析,去掉列表中元素前后空格
# mybag = [' glass',' apple','green leaf ']  #有的前面有空格，有的后面有空格
# xx= [one.strip() for one in mybag]
# print xx
# # 结果:['glass', 'apple', 'green leaf']
#
# # ============= list解析,enumerate获取列表的编号和元素
#
# week=['Sun.','Mon.','Tues.','Wed.','Thur.','Fri.','Sat.']
# for (i,day) in enumerate(week):
#     print day+' is '+str(i)
# # 结果:
# # Sun. is 0
# # Mon. is 1
# # Tues. is 2
# # Wed. is 3
# # Thur. is 4
# # Fri. is 5
# # Sat. is 6
#
# seasons = ['Spring', 'Summer', 'Fall', 'Winter']
# print list(enumerate(seasons))
# print list(enumerate(seasons, start=1))
# for i,j in enumerate(seasons, start=1):
#     print i,j
# # 结果:
# # [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
# # [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
# # 1 Spring
# # 2 Summer
# # 3 Fall
# # 4 Winter
#
# # ============= 字典, 使用clear方法清除字典全部数据
# d = {}
# d['name'] = 'Gumby'
# d['age'] = 42
# print d
# returned_value = d.clear()
# print d
# print returned_value
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