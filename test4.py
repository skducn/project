# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2019-1-8
# Description: ChainMap
# ********************************************************************************************************************



# -*- coding: utf-8 -*-

import binascii
import re
import requests
import logging

from gmssl import sm2, func

class Sm2Tools:
    """
    通用sm2算法类
    """
    class KeyStore:
        """
        SM2 密钥对类，包含密钥对生成、获取方法
        """
        _PRIVATE_KEY = ""
        _PUBLIC_KEY = ""

        def __init__(self) -> None:
            pass

        def setKey(self, priKey: str, pubKey: str) -> bool:
            """
            简单判断密钥对格式
            :param priKey: 私钥
            :param pubKey: 公钥
            :return: bool
            """
            result = re.match(r"^[a-fA-F\d]{64}$", priKey)
            if result is None:
                logging.error("KeyStore.setKey() -> priKey is invalid.")
                return False
            result = re.match(r"^[a-fA-F\d]{128}$", pubKey)
            if result is None:
                logging.error("KeyStore.setKey() -> pubKey is invalid.")
                return False
            self._PRIVATE_KEY = priKey
            self._PUBLIC_KEY = pubKey
            return True

        def createLocal(self) -> bool:
            """
            本地创建密钥对
            :return: bool
            """

            class _Generate_SM2_Key(sm2.CryptSM2):

                #初始化
                def __init__(self, private_key=None, public_key=None, ecc_table=sm2.default_ecc_table):
                    super().__init__(private_key, public_key, ecc_table)

                #获取私钥
                def get_private_key(self):
                    if self.private_key is None:
                        self.private_key = func.random_hex(self.para_len)  # d∈[1, n-2]
                    private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
                    return private_key
                    # return self.private_key

                # private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
                # public_key = '025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'

                #获取共钥
                def get_public_key(self):
                    if self.public_key is None:
                        self.public_key = self._kg(int(self.get_private_key(), 16), self.ecc_table['g'])  # P=[d]G
                    # return self.public_key
                    public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
                    return public_key
            try:
                # _sm2Generator = _Generate_SM2_Key()
                # self._PRIVATE_KEY = _sm2Generator.get_private_key()
                self._PRIVATE_KEY = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
                # self._PUBLIC_KEY = _sm2Generator.get_public_key()
                self._PUBLIC_KEY = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
                return True
            except:
                logging.error("KeyStore.createLocal() can't create the correct keys. ",
                              "Please call the Lib's Designer. ")
                return False

        def getSelf(self) -> dict:
            """
            获取创建的密钥对
            :return: dict: keyStore 格式：
            {
                "PRIVATE_KEY": "",
                "PUBLIC_KEY": ""
            }
            """
            return {
                "PRIVATE_KEY": self._PRIVATE_KEY,
                "PUBLIC_KEY": self._PUBLIC_KEY
            }

        def getPrivateKey(self) -> str:
            """
            返回公钥
            :return: str
            """
            return self._PRIVATE_KEY

        def getPublicKey(self) -> str:
            """
            返回私钥
            :return: str
            """
            return self._PUBLIC_KEY

    class SM2_Util(Exception):
        """
        SM2 加解密类
        """

        _SM2_Util = None

        def __init__(self, exception="") -> None:
            """
            构造函数
            :param exception: 默认参数，用于自定义异常
            """

            self._EXCPTION = None
            self._INIT_FLAG = False

        def setKey(self, keyStore: dict) -> bool:
            """
            初始化密钥对
            :param keyStore: dict: keyStore 格式：
                {
                    "PRIVATE_KEY": "",
                    "PUBLIC_KEY": ""
                }
            :return: bool
            """
            try:
                # 判断是否为全为英文和数字，且是 16 个字符的字符串
                # 不是，则抛出异常
                if re.match(r"^[a-fA-F\d]{64}$", keyStore["PRIVATE_KEY"]) is None:
                    raise Sm2Tools.SM2_Util(exception="SM2_Util.setKey() -> PRIVATE_KEY is invalid.")
                if re.match(r"^[a-fA-F\d]{128}$", keyStore["PUBLIC_KEY"]) is None:
                    raise Sm2Tools.SM2_Util(exception="SM2_Util.setKey() -> PUBLIC_KEY is invalid.")
            except Sm2Tools.SM2_Util as e:
                logging.error(e._EXCPTION)
                return False
            self._SM2_Util = sm2.CryptSM2(public_key=keyStore["PUBLIC_KEY"], private_key=keyStore["PRIVATE_KEY"])
            self._INIT_FLAG = True
            return True

        def getSelf(self) -> sm2.CryptSM2:
            """
            获取加解密类对象
            :return: sm2.CryptSM2 类实例
            """
            return self._SM2_Util

        def encrypt(self, data: str):
            """
            进行 SM2 加密操作
            :param data: String 格式的原文 data
            :return: String 格式的密文 enc_data
            """
            data_utf8 = data.encode("utf-8")
            enc_data = self._SM2_Util.encrypt(data_utf8)
            enc_data = binascii.b2a_hex(enc_data).decode("utf-8")
            return enc_data

        def decrypt(self, enc_data: str):
            """
            进行 SM2 解密操作
            :param enc_data: String 格式的密文 enc_data
            :return: String 格式的原文 data
            """
            enc_data = binascii.a2b_hex(enc_data.encode("utf-8"))
            dec_data = self._SM2_Util.decrypt(enc_data)
            dec_data = dec_data.decode("utf-8")
            return dec_data

def test_sm2():
    # """
    # SM2 test
    # """
    keyStore = Sm2Tools.KeyStore()
    SM2_Util = Sm2Tools.SM2_Util()
    if keyStore.createLocal():
        keysDict = keyStore.getSelf()
        SM2_Util.setKey(keysDict)
        data = "哈哈，我的国密算法改造，已完成了！！！"
        print("data: " + data)
        enc_data = SM2_Util.encrypt(data)
        print("encode_data: " + enc_data)
        dec_data = SM2_Util.decrypt(enc_data)
        print("decode_data: " + dec_data)
        if data == dec_data:
            print("data == decode_data: True")
    else:
        print("create fail")

# main
if __name__ == '__main__':
    print("main begin");
    test_sm2();
    print("main end");



# numbers = [1, 2, 2, 3, 2, 3, 3]
# counts = {num: numbers.count(num) for num in set(numbers)}
# print(counts)
#
# # for num in set(numbers):
# #     print(num)
#
# print(numbers.count(2))


# # import pymysql
# # pymysql.install_as_MySQLdb()
#
# args = "FullArgSpec(args=['self', 'interName', 'param'], varargs=None, varkw=None, defaults=('',), kwonlyargs=[], kwonlydefaults=None, annotations={})"
# print(args.find('self'))
# # print(args.find(', varargs'))
# # args = args[args.find('args=') + 5:args.find(', varargs')]  # ['self', 'interName', 'param']
# # # print(args)
# # print(args[args.find('args=') + 5:args.find(', varargs')])  # ['self', 'interName', 'param']
# # print(args[17:47])
# # args = (args[17:47])
# # print(args)
# # # print(args)
#










# import collections
# from math import hypot
# from random import choice
#
# Card = collections.namedtuple('Card', ['rank', 'suit'])
#
# 类与实例 PokeDeck(object):
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
# engine.say('Sally sells seashells by the seashore.')
# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()

# import pyttsx3
# # Initialize the converter
# converter = pyttsx3.init()
# # Set properties before adding
# # Things to say
# # Sets speed percent
# # Can be more than 100
# converter.setProperty('rate', 150)
# # Set volume 0-1
# converter.setProperty('volume', 0.7)
# # Queue the entered text
# # There will be a pause between
# # each one like a pause in
# # a sentence
# converter.say("Hello GeeksforGeeks")
# converter.say("I'm also a geek")
# # Empties the say() queue
# # Program will not continue
# # until all speech is done talking
# converter.runAndWait()

# # 文本转语音
# import pyttsx3
# engine = pyttsx3.init()
# rate = engine.getProperty('rate')
# # engine.setProperty('rate', rate-55)
# engine.say('The quick brown fox jumped over the lazy dog. 你是金浩吗？')
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
import uuid
#
#
# 类与实例 Spider:
#
#     pool_manager = urllib3.PoolManager()
#
#     @staticmethod
#     def get(url):
#         return Spider.pool_manager.urlopen('GET', url)
#
#
# 类与实例 ImageDownLoader:
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
# 类与实例 People :
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