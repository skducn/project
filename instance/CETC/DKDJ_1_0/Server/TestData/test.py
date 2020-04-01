# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
#***************************************************************


import yaml
import os, sys, unittest, xlwt, xlrd, MySQLdb, tempfile,shutil,chardet,random,webbrowser,platform,string,datetime,redis,commands,urllib2,MultipartPostHandler
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from xlwt.Style import *
from xlrd import open_workbook
from xlutils.copy import copy
import json
L1=['c','b','中国']
L2=[1,2,3]

L3=dict(zip(L1[::-1],L2))

ll=json.dumps(L3, encoding="UTF-8", ensure_ascii=False)

print ll



dict = {"asdf": "我们的python学习"}
list =["中国人民","12",0]
# print dict
# print u'\xe6\x88\x91\xe4\xbb\xac\xe7\x9a\x84'.encode('utf-8')
# {'asdf': '\xe6\x88\x91\xe4\xbb\xac\xe7\x9a\x84python\xe5\xad\xa6\xe4\xb9\xa0'}




t1=['1','2','3']
t2=['12' ,'52','43']
# print json.dumps(dict, encoding="UTF-8", ensure_ascii=False)
# list1=json.dumps(t1, encoding="UTF-8", ensure_ascii=False)
# list2= json.dumps(t2, encoding="UTF-8", ensure_ascii=False)
# print list1
# print list2

tmp = zip(t1, t2)
kk = dict((y, x) for x, y in tmp)
print kk
# print json.dumps(kk, encoding="UTF-8", ensure_ascii=False)


# kk = json.dumps(dict(map(lambda x,y:[x,y],t1,t2)), encoding="UTF-8", ensure_ascii=False))
# print kk


# print '中国'.decode("utf-8")
#
# tmp = zip(list1,list2)
# print dict((y, x) for x, y in tmp)



#
# list1=[]list2=[]
# kk={}
# checkboxs1 = self.driver.find_elements_by_xpath("//label[@class='checkbox']")
# for a in checkboxs1:
#     print a.text
#     list1.append(a.text)
#
# if choose == 'all':
#      self.driver.find_element_by_xpath("//input[@onclick='doSelectCompanyAll(this)']").click()
#
# checkboxs1 = self.driver.find_elements_by_xpath("//input[@name='task_company_info[][company_id]']")
# for a1 in checkboxs1:
#     list2.append(a1.text)
#
# tmp = zip(list1, list2)
# dict((y, x) for x, y in tmp)
# kk=dict(map(lambda x,y:[x,y],list1,list2))
# print kk


#***************************************************************
str = """
name: john
age: 37
job: manager
"""

y = yaml.load(str)
print y
# {'job': 'manager', 'age': 37, 'name': 'john'}

#***************************************************************
python_obj = {
    'name':"yoyo",
    "age":32,
    "job":"kuaiji"
}
y = yaml.dump(python_obj, default_flow_style=False)
print y
# age: 32
# job: kuaiji
# name: yoyo
#***************************************************************


# yaml转字典
# conf.yaml中内容如下
# name: blue
# age: 100
# job: teacher

# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y
# {'job': 'teacher', 'age': 100, 'name': 'blue'}

#***************************************************************
# yaml转列表
# # conf.yaml中内容如下
# - worker
# - 100
# - Terst
# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y
# ['worker', 100, 'Terst']
#***************************************************************
# yaml , 列表中包含dict
# # conf.yaml中内容如下
# - name: worker
#   age: 90
#   job: tester
# - age: 100
# - nagme: Terst
#   job: 30
# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y
# [{'job': 'tester', 'age': 90, 'name': 'worker'}, {'age': 100}, {'job': 30, 'nagme': 'Terst'}]

#***************************************************************
# yaml , 字典中包括所有类型
# # conf.yaml中内容如下
# str: "hello world"
# int: 100
# float: 3.1415
# boolean: true
# None: null
# time: 2017-02-26
# data: 2017-02-26
# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y
# {'None': None, 'boolean': True, 'str': 'hello world', 'time': datetime.date(2017, 2, 26), 'int': 100, 'float': 3.1415, 'data': datetime.date(2017, 2, 26)}
#***************************************************************
# yaml , 字符串是单引号或双引号(转义)
# # conf.yaml中内容如下
# str1: 'hello world'
# str2: "hello\njohn"
# str3: 'hello\njohn'
# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y['str1']
# print y['str2']
# print y['str3']
# hello world
# hello
# john
# hello\njohn

#***************************************************************
# yaml , & 和 * 引用
# name: &name john
# tester: *name
# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y
# {'name': 'john', 'tester': 'john'}


#***************************************************************
# yaml , 强制转换
# test: !!str 3.14
# num: !!int "123"
# y = yaml.load(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
# print y
# {'num': 123, 'test': '3.14'}


#***************************************************************
# yaml, 分段 使用laod_all
# ---
# name: john
# age: 36
# ---
# name: yoyo
# age: 34
ys = yaml.load_all(file('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','r'))
for y in ys:
  print y
# {'age': 36, 'name': 'john'}
# {'age': 34, 'name': 'yoyo'}

#***************************************************************
# yaml, 对应的dump_all()
# obj1 = {"name": "James","age": "15"}
# obj2 = ["lily",19]
# with open('/Users/linghuchong/Downloads/51/Project/XXX_AutoTest/baidu/Config/conf.yaml','w') as f:
#     yaml.dump_all([obj1,obj2],f)

# {age: '15', name: James}
# --- [lily, 19]

#***************************************************************
# 生成有序列表
y = yaml.dump(range(11))
print y
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

















