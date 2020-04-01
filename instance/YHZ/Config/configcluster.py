# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-5-23
# Description: 集群配置文件
# ********************************************************************************************************************

import sys, MySQLdb, winrm, unittest, xlwt, xlrd, datetime, random, socket, struct
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium import webdriver
from xlutils.copy import copy
from Public.PageObject.LevelPO import *
from Public.PageObject.netPO import *


# 【远程客户端（启动代理）】
clientRemote = winrm.Session('http://10.111.10.37:5985/wsman', auth=('hp', '123'))
# 【远程服务端（启动WEB项目）】
serverRemote = winrm.Session('http://10.111.10.58:5985/wsman', auth=('hp', '123'))

# 【客户端网址】
varURL = "http://10.111.10.58:8080/admin/"
varTitle = u'集群应用管理系统'


# 【业务场景（测试用例）】
varExcel = '/Users/linghuchong/Downloads/51/Project/Cos/TestData/CosScene.xls'
varExcelSheetName = "main,testcase"

# 【log文件的前缀】
varLogPrefixPath = '/Users/linghuchong/Downloads/51/Project/Cos/log/Cluster_'

# 【数据库】
conn = MySQLdb.connect(host="10.111.3.16", user='developer', passwd='developer', db='jiqun', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')

# 【Webdriver驱动】
driver = webdriver.Firefox(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, proxy=None, executable_path='/usr/local/bin/geckodriver', firefox_options=None, log_path='geckodriver5.log')
driver.implicitly_wait(10)

