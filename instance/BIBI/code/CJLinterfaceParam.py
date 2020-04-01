# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2016-12-14
# Description   : 场景鹿1.0参数配置
# *******************************************************************************************************************************
import os, sys,requests, xlwt, xlrd, MySQLdb, redis, urllib3, random, time, urllib2, MultipartPostHandler, cookielib, string ,datetime, smtplib
import mimetypes, email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.encoders import encode_base64
import urllib2,MultipartPostHandler,cookielib
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep
from pymongo import MongoClient
# https://en.wikipedia.org/wiki/Wikipedia:Scripts/ImageFileMigrator/MultipartPostHandler.py
reload(sys)
sys.setdefaultencoding('utf8')

def randomDigits(n):
    # 返回随机生成的4位数
    ret = []
    for i in range(n):
        while 1:
            number = random.randrange(0,10)
            if number not in ret:
                ret.append(str(number))
                break
    return "".join(ret)

# ********************************************************************************************************************************
# 参数列表

myPhone = "13716101001"  # 手机号
varExcel = "/Users/linghuchong/Downloads/51/Project/mySVN/Test/Backup/InterfaceExcel.xls"  # 数据xls
testURL = "https://cjl.88uka.com"  # 测试URL

connMongo155 = MongoClient('192.168.2.155', 10005); db = connMongo155.sceneWeb  # mongodb
connRedis166 = redis.StrictRedis(host='192.168.2.166', port=6379, db=0, password="dlhy123456")  # redis CJL66
connRedis167 = redis.StrictRedis(host='192.168.2.167', port=6380, db=0, password="dlhy123456")  # redis CJL67

connPersonal = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='personal', port=3306, use_unicode=True)
curPersonal = connPersonal.cursor();curPersonal.execute('SET NAMES utf8;');connPersonal.set_character_set('utf8');curPersonal.execute('show tables')

connScenemsg = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='scenemsg', port=3306, use_unicode=True)
curScenemsg = connScenemsg.cursor();curScenemsg.execute('SET NAMES utf8;');connScenemsg.set_character_set('utf8');curScenemsg.execute('show tables')

connSysparam = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='sysparam', port=3306, use_unicode=True)
curSysparam = connSysparam.cursor();curSysparam.execute('SET NAMES utf8;');connSysparam.set_character_set('utf8');curSysparam.execute('show tables')

connUpload = MySQLdb.connect(host='192.168.2.164', user='remote', passwd='Dlhy66506043', db='upload', port=3306, use_unicode=True)
curUpload = connUpload.cursor();curUpload.execute('SET NAMES utf8;');connUpload.set_character_set('utf8');curUpload.execute('show tables')

cityID = "310100"  # 城市id
nickName = "动量令狐"  # 昵称
sign = "正确做事，更要做正确的事"  # 个人签名
comSceneName = "上海外滩" + randomDigits(4)  # 公共场景名
comSceneAddress = "上海外滩地址" + randomDigits(4)   # 公共场景地址
splitSceneName = "迪斯尼咖啡屋" + randomDigits(4)   # 分场景名
splitScenePic = "https://cjl.88uka.com/pic/0000/0000/0000/0022.jpg"   # 场景图片
lon = "121.401307"  # 百度经度
lat = "31.218743"  # 百度纬度
gpslon = "121.4013090000"  # gps经度
gpslat = "31.2188120000"  # gps纬度
headPic = "https://cjl.88uka.com/pic/0000/0000/0000/0032.jpg"  # 公共场景头像
headPic2 = "https://cjl.88uka.com/pic/0000/0000/0000/0033.jpg"  # 分场景头像

friendID1 = "10000018"  # 好友id（需验证=1）
friendID2 = "10000019"  # 好友id（免验证=0）
friendID3 = "10000020"  # 好友id（免验证）
friendID4 = "10000021"  # 好友id（免验证）
friendID5 = "10000022"  # 好友id（免验证）
friendID6 = "10000023"  # 好友id（免验证）
friendID7 = "10000025"  # 好友id（免验证）

vardeerNumber = "2016111410026"

varlabelName = "john" + randomDigits(4)   # 单标签名

# 发邮件参数
recipient = 'jinhao@mo-win.com.cn'  # 邮件接收者
# recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"   # 邮件接收者（多人）
