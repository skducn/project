# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2016-6-13
# Description: 资源文件
#****************************************************************

import os,sys,unittest,xlwt,xlrd,MySQLdb,tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis
from appium import webdriver
# from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import smtplib,pytesseract
from PIL import Image
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
from PIL import Image
from pyh import *
#from jhj_v1_5_setup import *
#win32api,win32con,HTMLTestRunner
# import HTMLTestRunner
import time,Image,ImageChops

def Getred():
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    # info = r.info() # redis信息
    # for key in info:
    #     print "%s : %s" % (key,info[key])
    # 查数据库大小
    print '\ndbsize: %s' % r.dbsize()

    # 看连接
    print "ping %s" % r.ping()

    print r.get("app_question_10001679")

    print r.scard("randomRed:34:3855")  # 返回key的set的基数 ,结果80个
    print r.sismember("randomRed:34:3855","68:1") # 判断key中member元素是否存在,返回 true 或 false
    sum=0
    for i in r.smembers("randomRed:34:3855"):
        sum = sum +int(i.split(":",1)[1])
    print sum
Getred()


#
# class A:
#     def __init__(self,name):
#         print name

def sendemail(self,varFile):
        # 邮箱配置
        sender = '<jinhao@mo-win.com.cn>'
        receiver = 'jinhao@mo-win.com.cn'
        f = open(varFile,'rb')
        mail_body = f.read()
        f.close()
        msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
        # msg = MIMEText('<html><h1>你好！</h1></html>','html','utf-8')
        # msg = MIMEText('你好','text','utf-8')
        # msg['Subject'] = Header(subject,'utf-8')
        msg['Subject'] = u'三藏红包gameTAble'
        try:
            smtp = smtplib.SMTP()
            smtp.connect('smtp.exmail.qq.com')
            smtp.login('jinhao@mo-win.com.cn','Jinhao80')
            smtp.sendmail(sender,receiver,msg.as_string())
            smtp.quit()
        except Exception, e:
            print str(e)

# def test2(x):
#     print x
#     print "source121212121hahaha"

#****************************************************************
# 1,变量定义规则:
# app页面变量 = appTest
# Excel外部变量 = xlsTest
# redis变量 = redisTest
# 表结构变量 = tblTest ,  tblTmp1,tblTmp2
# 程序变量 = varTest # varPhone="13816107078"
# 临时变量 = tmp
# web函数命名 = b_userlogin
# 外部文件或路径变量 =
# ProjectPath = "/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ"
# ExcelFile = "/excel/tsz_amount.xls"
# ReportHtml = "/report/testreport_amount.html" # TestReport文件
# ScreenshotFolder="/screenshot/"  #org\curr 截屏
# ErrorScreenshotFolder = "/errscreenshot/"  # 错误截屏

#****************************************************************
# 2, by.xpath 用法
# by.xpath("//android.widgit.TextView[contains(@text,'热门')]")
# by.xpath("//android.widgit.ImageButton[contains(@content-desc,'导航')]")

# browser.find_element_by_xpath('//div[@class="nav"]/ul/li[2]').click()    # 点击主菜单 商户
# browser.find_element_by_xpath('//div[@id="container"]/div/dl/dd[2]').click()  # 点击侧边菜单 代理商发展商户
# browser.find_element_by_xpath('//select[@id="busiId"]/option[' + str(varAgentNum)+ ']').click()  # 代理商 譬如6=john代理商1
# by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/child::android.widget.FrameLayout[1]/android.widget.RelativeLayout/android.widget.EditText[1]").send_keys("123456")

#****************************************************************
# 3, 调用其他文件中的类或方法,
# 场景:如A目录里有一个文件叫aa.py,此文件中有abc()方法,先需要在当前脚本中调用A目录里的aa文件中的abc方法,操作如下:
# 1) 在A目录里新建一个 __init__.py
# 2) 在当前脚本头部调用,from A.aa.abc import *  或 from A.aa import abc
# 或如下:
# sys.path.append('/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/A')
# from aa import *    #引入模块中的函, 此时aa有红色下划线,但可以正常使用

#****************************************************************
# 4,关于路径
# sys.path.append('/Users/linghuchong/Downloads/51/ForWin/Python/03_Project/TSZ/resource') # 临时性添加路径
# print sys.path # 打印当前路径
# 获取当前程序路径, 如获取Pycharm程序的路径,
# print os.path.abspath("")  # 结果: /Applications/PyCharm.app/Contents/bin
# PATH = lambda p: os.path.abspath(p)

#****************************************************************
# 页面格式化 http://www.tuicool.com/articles/IRvEBr
# page =PyH('JHJ_TestReport')
# page.addCSS('myStylesheet1.css','myStylesheet2.css')
# page << h2(u'极好家V1.5自动化测试报告', cl='center')
# page << h4(u'Start Time:',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# page << h4(u'用例执行情况：')

#****************************************************************
# 5,保留两位数的方法
# x="%.2lf" % (5000/100)
# print x

#****************************************************************
# 6,关于时间显示方式
# 输出当前时间
# varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S');  #20160623183734
# varTimeYMD = datetime.datetime.now().strftime('%Y%m%d');  # 20160628
# varTimeY_M_D = datetime.datetime.now().strftime('%Y-%m-%d'); # 2016-06-28 00:00:01
# varTimeFrom = varTimeY_M_D +" 00:00:01"
# varTimeEnd = varTimeY_M_D+" 23:59:59"

# 时间戳与时间的转换
# 时间戳与时间之间的转换，需要一个中间过程，即将先将时间或时间戳先转为时间元组！
# 1、时间 转 时间戳：
# import datetime
# s = datetime.datetime(2012,6,22)
# time.mktime(s.timetuple())
# 1340294400.0

# 2、时间戳 转 时间:
# import time
# timeTuple = time.localtime(1340294400.0)
# time.strftime('%Y-%m-%d',timeTuple)
# '2011-06-22'

# 输出时间 + 3位, 如 :20160802171111559 ,
# unicode1 = u"%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 类型是unicode
# str1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3] # 类型是 str

#****************************************************************
# 7,关于编码与解码
    # https://segmentfault.com/a/1190000002447836

# python处理Excel，pythonexcel http://www.bkjia.com/Pythonjc/926154.html

# [python]去掉 unicode 字符串前面的 u（转） # http://www.cnblogs.com/ajianbeyourself/p/5670872.html ,https://mozillazg.com/2013/12/python-raw-unicode.html
# 转 python中包含UTF-8编码中文的列表或字典的输出 https://segmentfault.com/a/1190000002447836

# str2='\u91d1\u91d1 \u7ed9\u60a8\u53d1\u73b0\u91d1\u7ea2\u5305\u5566\uff010.20\u5143\u7ea2\u5305\u7b49\u5927\u5bb6\u6765\u62a2\uff0c\u62a2\u5230\u5c31\u80fd\u63d0\u73b0\u54e6~'
# str1 = '\u4f60\u597d'
# print str1.decode('unicode_escape')
# 关于python编码的文章，http://blog.csdn.net/liuxincumt/article/details/8183391
# 中文\unicode编码在线转换工具, http://www.bangnishouji.com/tools/chtounicode.html

# 普通字符串可以用多种方式编码成Unicode
# unicodestring = u"Hello world"
# # 将Unicode转化为普通Python字符串："encode"
# utf8string = unicodestring.encode("utf-8")
# asciistring = unicodestring.encode("ascii")
# isostring = unicodestring.encode("ISO-8859-1")
# utf16string = unicodestring.encode("utf-16")
# # 将普通Python字符串转化为Unicode："decode"
# plainstring1 = unicode(utf8string, "utf-8")
# plainstring2 = unicode(asciistring, "ascii")
# plainstring3 = unicode(isostring, "ISO-8859-1")
# plainstring4 = unicode(utf16string, "utf-16")

#****************************************************************
# 8,随即生成4位数字符串
# def myfunc(n):
#     import random
#     ret = []
#     for i in range(n):
#         while 1:
#             number = random.randrange(0,10)
#             if number not in ret:
#                 ret.append(str(number))
#                 break
#     return ret
# varRandom4="".join(myfunc(4))
# print varRandom4
# print type(varRandom4)

#****************************************************************
# Python中函数的参数定义和可变参数
# http://www.cnblogs.com/tqsummer/archive/2011/01/25/1944416.html

#****************************************************************
# 功能:通过EXCEL外部调用id,EXcel中 ID0 - ID9 参数
# for i in range(0,len(self.str_list)): # 遍历参数
#     print self.str_list[i]
# print self.str_list[0]  # 第一个参数 ,以此类推
# 调用方法:  self.driver.find_element_by_id(self.str_list[1]).send_keys(varPhone)

#****************************************************************
# [python]dictionary方法说明

# # len(a)	the number of items in a 得到字典中元素的个数
# # a[k]	the item of a with key k 取得键K所对应的值
# # a[k] = v	set a[k] to v 设定键k所对应的值成为v
# # del a[k]	remove a[k] from a 从字典中删除键为k的元素
# # a.clear()	remove all items from a 清空整个字典
# # a.copy()	a (shallow) copy of a 得到字典副本
# # k in a	True if a has a key k, else False 字典中存在键k则为返回True，没有则返回False
# # k not in a	Equivalent to not k in a   字典中不存在键k则为返回true,反之返回False
# # a.has_key(k)	Equivalent to k in a, use that form in new code 等价于k in a
# # a.items()	a copy of a's list of (key, value) pairs 得到一个键，值的list ,如:[('a', 'apple'), ('c', 'grape'), ('b', 'banana'), ('d', 'orange')]
# # a.keys()	a copy of a's list of keys 得到键的list
# # a.update([b])	updates (and overwrites) key/value pairs from b从b字典中更新a字典，如果键相同则更新，a中不存在则追加
# # a.fromkeys(seq[, value])	Creates a new dictionary with keys from seq and values set to value
# # a.values()	a copy of a's list of values
# # a.get(k[, x])	a[k] if k in a, else x
# # a.setdefault(k[, x])	a[k] if k in a, else x (also setting it)
# # a.pop(k[, x])	a[k] if k in a, else x (and remove k)
# # a.popitem()	remove and return an arbitrary (key, value) pair
# # a.iteritems()	return an iterator over (key, value) pairs
# # a.iterkeys()	return an iterator over the mapping's keys
# # a.itervalues()	return an iterator over the mapping's values
#
# #字典的添加、删除、修改操作
# dict = {"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}
# dict["z"] = "watermelon"
# del(dict["a"])
# dict["g"] = "grapefruit"
# print dict.pop("b")
# print dict
# # dict.clear()
#
# #字典的遍历
# dict = {"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}
# for k in dict:
#     print "dict[%s] =" % k,dict[k]
#
# #字典items()的使用
# dict = {"a" : "apple", "b" : "banana", "c" : "grape", "d" : "orange"}
# #每个元素是一个key和value组成的元组，以列表的方式输出
# print dict.items()
#
# #调用items()实现字典的遍历
# dict = {"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}
# for (k, v) in dict.items():
#     print "dict[%s] =" % k, v
#
#
#
# #调用iteritems()实现字典的遍历
# dict = {"a" : "apple", "b" : "banana", "c" : "grape", "d" : "orange"}
# print dict.iteritems()
# for k, v in dict.iteritems():
#     print "dict[%s] =" % k, v
# for (k, v) in zip(dict.iterkeys(), dict.itervalues()):
#     print "dict[%s] =" % k, v
#
# #使用列表、字典作为字典的值
# dict = {"a" : ("apple",), "bo" : {"b" : "banana", "o" : "orange"}, "g" : ["grape","grapefruit"]}
# print dict["a"]
# print dict["a"][0]
# print dict["bo"]
# print dict["bo"]["o"]
# print dict["g"]
# print dict["g"][1]
#
#
# dict = {"a" : "apple", "b" : "banana", "c" : "grape", "d" : "orange"}
# #输出key的列表
# print dict.keys()
# #输出value的列表
# print dict.values()
# #每个元素是一个key和value组成的元组，以列表的方式输出
# print dict.items()
# dict = {"a" : "apple", "b" : "banana", "c" : "grape", "d" : "orange"}
# it = dict.iteritems()
# print it
#
# #字典中元素的获取方法
# dict = {"a" : "apple", "b" : "banana", "c" : "grape", "d" : "orange"}
# print dict
# print dict.get("c", "apple")  # 如果有c这个key,则输出 grape
# print dict.get("e", "apple")  # 否则如果e这个key不存在,则输出 apple
#
#
# #get()的等价语句
# D = {"key1" : "value1", "key2" : "value2"}
# if "key1" in D:
#     print D["key1"]
# else:
#     print "None"
#
#
# #字典的更新
# dict = {"a" : "apple", "b" : "banana"}
# print dict
# dict2 = {"c" : "grape", "d" : "orange"}
# dict.update(dict2)
# print dict
#
#
# #udpate()的等价语句
# D = {"key1" : "value1", "key2" : "value2"}
# E = {"key3" : "value3", "key4" : "value4"}
# for k in E:
#     D[k] = E[k]
# print D
#
# #字典E中含有字典D中的key
# D = {"key1" : "value1", "key2" : "value2"}
# E = {"key2" : "value3", "key4" : "value4"}
# for k in E:
#     D[k] = E[k]
# print D
# #设置默认值
# dict = {}
# dict.setdefault("a")
# print dict
# dict["a"] = "apple"
# dict.setdefault("a","default")
# print dict
# #调用sorted()排序
# dict = {"a" : "apple", "b" : "grape", "c" : "orange", "d" : "banana"}
# print dict
# #按照key排序
# print sorted(dict.items(), key=lambda d: d[0])
# #按照value排序
# print sorted(dict.items(), key=lambda d: d[1])
# #字典的浅拷贝
# dict = {"a" : "apple", "b" : "grape"}
# dict2 = {"c" : "orange", "d" : "banana"}
# dict2 = dict.copy()
# print dict2
#
print "--------------"
#字典的深拷贝
import copy
dict = {"a": "apple", "b": {"g": "grape","o" : "orange"}}
dict2 = copy.deepcopy(dict)
dict3 = copy.copy(dict)
dict2["b"]["g"] = "orange"
print dict
dict3["b"]["g"] = "orange"
print dict

#****************************************************************
# redis

# http://www.cnblogs.com/snow-backup/p/4021554.html

def zh2unicode(stri):
   """Auto converter encodings to unicode
   It will test utf8,gbk,big5,jp,kr to converter"""
   for c in ('utf-8', 'gbk', 'big5', 'jp','euc_kr','utf16','utf32'):
       try:
            return stri.decode(c)
       except:
            pass
   return stri