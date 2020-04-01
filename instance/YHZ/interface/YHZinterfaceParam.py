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
# varPhone = u"13918794888"
# varPass = u"b123456"

varPhone = u"13816044157"
varPass = u"123456"

# varPhoneZhuli = u"13916109054"
# varPhoneYaoshi = u'14016109054'

# 测试URL
varURL = "http://10.111.3.6:8086/cloudDiagnose"

# 外部数据源
varExcel = "/Users/linghuchong/Downloads/51/Project/YYG/interface/YYGinterface.xls"

# Redis
connRedis5 = redis.StrictRedis(host='10.111.3.6', port=6379, db=1, password="b840fc02d524045429941cc15f59e41cb7be6c52")

# 数据库
conn = MySQLdb.connect(host='10.111.3.6', user='cetc', passwd='20121221', db='yunhuizhen_v2', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')


# # 发邮件参数
# recipient = 'jinhao@cetchealth.com.cn'  # 邮件接收者
# recipient = "'jinhao@cetchealth.com.cn', 'guoweiliang@mo-win.com.cn'"   # 邮件接收者（多人）


