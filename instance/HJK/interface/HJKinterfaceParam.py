# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2017-10-17
# Description   : HJK接口参数
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
# from xlutils.copy import copy
#
# reload(sys)
# sys.setdefaultencoding('utf8')
#
# # # 手机号与密码
# # varPhone = u"13816109050"
# # varPass = u"b123456"
# #
# # # 测试URL
# # varURL = u"http://10.111.3.5:8082/dangjian"
#
# # 外部数据源
# varExcel = os.path.dirname(os.path.abspath("__file__")) + u'/DKDJinterface.xls'
#
# bk = xlrd.open_workbook(varExcel, formatting_info=True)
# newbk = copy(bk)
# styleBlue = xlwt.easyxf('font: height 340 ,name Times New Roman, color-index blue')
# styleRed = xlwt.easyxf('font: height 340 ,name Times New Roman, color-index red')
# # ('font: height 240, name Arial, colour_index black, bold off, italic on; align: wrap on, vert centre, horiz left;')
# alignment = xlwt.Alignment()
# alignment.horz = xlwt.Alignment.HORZ_CENTER
# alignment.vert = xlwt.Alignment.VERT_CENTER
# alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
# styleRed.alignment = alignment
# styleBlue.alignment = alignment
# exlSheetNums = len(bk.sheet_names())
# l_exlSheetNames = bk.sheet_names()
# l_exlSheetNames2 = []
# l_exlSheetSingleNum = []



# # 数据库
# conn = MySQLdb.connect(host='10.111.3.5', user='cetc', passwd='20121221', db='dangjian', port=3306, use_unicode=True)
# cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')


# # Redis
# connRedis5 = redis.StrictRedis(host='10.111.3.6', port=6379, db=1, password="b840fc02d524045429941cc15f59e41cb7be6c52")


