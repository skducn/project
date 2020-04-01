# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2016-12-14
# Description   : 医云谷接口参数
# *******************************************************************************************************************************

import os, sys, redis, MySQLdb, requests, xlwt, xlrd, urllib3, random, time, urllib2, MultipartPostHandler, cookielib, string ,datetime, smtplib, json, md5, base64, hashlib, mimetypes, email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.encoders import encode_base64
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from time import sleep
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')


# *******************************************************************************************************************************
# 手机号与密码
varPhone = u"13816109054"
varPass = u"a123456"
# varPhone = "13918794888"
# varPass = "a123456"

varPhoneZhuli = u"13916109054"
varPhoneYaoshi = u'14016109054'

# 测试URL
# varURL = "http://10.111.3.6:8083/DCloudDoctor"

# 正式URL
# varURL = "39.108.3.241"
varURL = "http://api.copp-zk.com:8083/DCloudDoctor"   # 医生端api
# varURL = "http://api.copp-zk.com:8084"   # 患者端api
# 39.108.3.241

# 外部数据源
varExcel = "/Users/linghuchong/Downloads/51/Project/YYG/interface/YYGinterface.xls"

# # 测试Redis
# connRedis5 = redis.StrictRedis(host='10.111.3.5', port=6379, db=1, password="b840fc02d524045429941cc15f59e41cb7be6c52")
# 测试Redis
connRedis5 = redis.StrictRedis(host='120.77.46.127', port=6379, db=1, password="b840fc02d524045429941cc15f59e41cb7be6c52")


# 测试数据库
# conn = MySQLdb.connect(host='10.111.3.5', user='cetc', passwd='20121221', db='yygapp', port=3306, use_unicode=True)
# cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')
# 正式数据库
conn = MySQLdb.connect(host='120.77.46.127', user='cetc', passwd='20121221', db='yygapp', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')


# # 发邮件参数
# recipient = 'jinhao@cetchealth.com.cn'  # 邮件接收者
# recipient = "'jinhao@cetchealth.com.cn', 'guoweiliang@mo-win.com.cn'"   # 邮件接收者（多人）


