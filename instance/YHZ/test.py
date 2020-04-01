# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description:
# HTMLTestRunner.py /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7
#***************************************************************

import Image

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt

N = 5
menMeans = (20, 35, 30, 25, 27)
menStd = (0, 3, 4, 1, 2)


ind = np.arange(N)  # the x locations for the groups
width = 0.3     # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (25, 32, 34, 20, 25)
womenStd =   (3, 5, 2, 3, 3)
rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

# add some
ax.set_ylabel(u'bug数12323123123')
# x = (u'党建bug分布图').encode('GBK')
# print x
ax.set_title('dangjian')

ax.set_xticks(ind+width)
ax.set_xticklabels( ('android', 'iOs', 'PHP', 'Server', '') )

ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

savefig('/Users/linghuchong/Downloads/51/Project/Cos/TestData/2.png')
# plt.show()

# from PIL import ImageGrab
# pic = ImageGrab.grab(plt.show())
# pic.save('/Users/linghuchong/Downloads/51/Project/Cos/TestData/1.png')

print "12121212"

# customPic('/Users/linghuchong/Downloads/51/Project/Cos/TestData/1.png',100, 100, 600, 600)

sleep(1212)


import matplotlib.pyplot as plt

import numpy as np

import xlrd

import os

from StringIO import StringIO

if __name__ == '__main__':

    data = xlrd.open_workbook('/Users/linghuchong/Downloads/51/Project/Cos/TestData/Cos.xls')

    plt.figure(figsize=(8, 4))

    plt.xlabel(u'second')

    plt.ylabel(u'xxx')

    x_index = 1

    data.sheet_names()

    table = data.sheets()[0]

    table = data.sheet_by_index(0)

    table = data.sheet_by_name(u'Sheet1')

    print("Good")

    COLOR_INDEX = 1

    INDEX_NAME = ''

    ## init data





    nrows = table.nrows

    ncols = table.ncols

    print("nr=%d nc=%d \n" % (nrows, ncols))

    '''

    for rownum in range(table.nrows): 

            value = table.cell(rownum,2).value 

            if rownum == 0:

                print("")

            else: 

                try:

                    value_int = int(value)

                    x.append(x_index)

                    y.append(value_int)

                   # line = ax.plot(x_index,value_int,label="xx ",color="red",linewidth=2)

                    #plt.plot(x_index,value_int,label="xx ",color="red",linewidth=2)

                    print("index=%d"%x_index)



                    #plt.plot_date(x_index,value_int)

                    x_index=x_index+1

                except:

                    print("error") 

    plt.plot(x,y,label="xx ",color="red",linewidth=2) 

    '''

    for colnum in range(table.ncols):

        x = []

        y = []

        for rownum in range(table.nrows):

            value = table.cell(rownum, colnum).value

            # print("nr=%d nc=%d value=%d \n"%(rownum,colnum,value ))

            # print(value)

            # print("rownum=%d colnum=%d "%(rownum,colnum))

            if rownum == 0:

                print("")

            else:

                try:

                    value_int = int(value)

                    x.append(x_index)

                    y.append(value_int)

                    # plt.plot(x_index,value_int,label=" ",color="red",linewidth=2)

                    # print("index=%d"%x_index)



                    # plt.plot_date(x_index,value_int)

                    x_index = x_index + 1

                except:

                    print("error")

        if COLOR_INDEX == 1:

            COLOR_INDEX = 0

            plt.plot(x, y, color="red", linewidth=2)

        else:

            COLOR_INDEX = 1

            plt.plot(x, y, color="blue", linewidth=2)

        print("==============================>")

    plt.title("Test")

    # plt.ylim(10,2000)

    plt.legend()

    plt.show()


sleep(1212)

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
import json,socket,struct
x = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))



from win32com.client import Dispatch




# b = "444"
# y =b + "." + x.split(".")[1] +"." +x.split(".")[2] +"." +x.split(".")[3]
# print y

sleep(1212)

# x = "192.168.1.2"
# print x.split(".")[0]
# print x.split(".")[1]
# a = x.split(".")[0] + "." + x.split(".")[1]
# print a

import random
import socket
import struct

print socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

sleep(112)

x = "1234567"
y= "34"
print x.find(y)
print x[3:]


sleep(1212)
import winrm
serverRemote = winrm.Session('http://10.111.3.22:5985/wsman', auth=('Administrator', '1q2w3e$R'))
r = serverRemote.run_ps('dir e:\engine\upload')
print r.std_out

sleep(1212)
import datetime

now = datetime.datetime.now()

t = now.strftime('%Y-%m-%d %H:%M:%S')
print t

varTimestamp = str(t).replace("-", "").replace(":", "").replace(" ", "")
print varTimestamp
sleep(1212)

# 数据库
conn = MySQLdb.connect(host="10.111.3.16", user='developer', passwd='developer', db='QuartzDB_Run', port=3306, use_unicode=True)
cur = conn.cursor();cur.execute('SET NAMES utf8;');conn.set_character_set('utf8');cur.execute('show tables')


def get_TblOneValue(cur, conn, tblName, whr1, sel1):
    # 统计表中某字段值是否存在，如果存在1条则返回对应的值，否则返回0
    # Level_PO.get_TblOneValue(cur, conn, "task_host", "id", "host_server_ip=127.0.0.1")

    where1 = whr1.split(',')[0].split('=')
    where2 = whr1.split(',')[1].split('=')
    select1 = sel1.split(',')[0]
    select2 = sel1.split(',')[1]
    cur.execute('select count(%s),%s from %s where %s="%s" and %s="%s"' % (select1, select2, tblName, where1[0], where1[1], where2[0], where2[1]))
    t = cur.fetchone()
    conn.autocommit(1)
    if t[0] == 1:return t[1]
    else:return t[0]

x= get_TblOneValue(cur, conn, "task_frame", "task_name=task6530,task_group=group1", "id,id")
print x
sleep(1212)




whr1 = "host_server_ip=127.0.0.1"
x = whr1.split('=')
sel1="id"
tblName = "task_host"
cur.execute('select count(%s),%s from %s where %s="%s"' % (sel1, sel1,tblName, x[0], x[1]))
t = cur.fetchone()
conn.autocommit(1)
if t[0] == 1:
    print t[1]
else:
    print "error"

sleep(1212)

x = "127.0.0.1"
cur.execute('select count(id),id from task_host where host_server_ip="%s"' % (x))
t = cur.fetchone()
if t[0] == 1:
    print t[1]

sleep(1212)

# whr2="127.0.0.1"
# cur.execute('select count(id) from task_host where host_server_ip="%s"' % (whr2))
# tbl = cur.fetchone()
# conn.autocommit(1)
# if tbl[0] != 0:
#     print u"errorrrrr - S2,创建宿主,IP地址已重复"
# else:
#     print u"1212121"
#
# sleep(1212)
# x = 'select count(id) from task_host where host_server_ip=127.0.0.1'
# x = 'select count(id) from task_host where host_server_ip=127.0.0.1'
a = "select "
x = "count(id) from task_host where host_server_ip=\"127.0.0.1\""
y = a + x
print y
def TblCount(cur, conn, y):
    # x = whr1.split('=')
    # print x[0]
    # print x[1]
    cur.execute(y)

    cur.execute('select count(id) from task_host where host_server_ip="127.0.0.1"')
    tbl = cur.fetchone()
    conn.autocommit(1)
    if tbl[0] != 0:
        print u"errorrrrr - S2,创建宿主,IP地址已重复"
        # return u"errorrrrr - S2,创建宿主,IP地址已重复"
    else:
        print u"1212121"


TblCount(cur,conn,x)
sleep(1212)



def myfunc(n):
    import random
    ret = []
    for i in range(n):
        while 1:
            number = random.randrange(0, 10)
            if number not in ret:
                ret.append(str(number))
                break
    return ret

varRandom4 = "".join(myfunc(4))
print varRandom4
print type(varRandom4)
print type(int(varRandom4))
x = int(varRandom4)+9
print x


x= "task????"
print len(x.split("?"))-1

def myfunc(n):
    import random
    ret = []
    for i in range(n):
        while 1:
            number = random.randrange(0, 10)
            if number not in ret:
                ret.append(str(number))
                break
    return ret


varRandom4 = "".join(myfunc(3))
varRandom3 = "".join(myfunc(3))

print varRandom4
print varRandom3

sleep(1212)

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

















