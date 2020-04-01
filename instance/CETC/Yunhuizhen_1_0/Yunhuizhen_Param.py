# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2017-4-7
# Description   : 电科党建 配置
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

# varExcel = "/Users/linghuchong/Downloads/51/Project/mySVN/Test/Backup/InterfaceExcel.xls"  # 数据xls
# testURL = "http://10.111.3.5:88/dangjian/event/web/app_test.php/security/login"  # 测试URL
#
# accountGroup = "Tasl_test1"
# accountOperation = "qiju"
#
# accountLevel2 = "Task_Test2"
# accountLevel3 = "Task_Test3"
# accountLevel4 = "?"
# accountAudit2 = "level11"
#
# accountLevel2_2 = "Task_Test22"
# accountLevel3_2 = "Task_Test33"
# accountLevel4_2 = "?"
# accountAudit2_2 = "?"

conn = MySQLdb.connect(host='10.111.3.6', user='cetc', passwd='20121221', db='yunhuizhen', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')

# vardeerNumber = "2016111410026"
#
# varlabelName = "john" + randomDigits(4)   # 单标签名
#
# # 发邮件参数
# recipient = 'jinhao@cetchealth.com.cn'  # 邮件接收者
# # recipient = "'jinhao@mo-win.com.cn', 'guoweiliang@mo-win.com.cn'"   # 邮件接收者（多人）
