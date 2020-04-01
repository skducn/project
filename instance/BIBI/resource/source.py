#!/usr/bin/env python
#coding:utf-8
# Author:   --<qingfengkuyu>
# Purpose: MongoDB的使用
# Created: 2014/4/14
#32位的版本最多只能存储2.5GB的数据（NoSQLFan：最大文件尺寸为2G，生产环境推荐64位）

# http://www.jb51.net/article/28694.htm
# MongoDB 语法使用小结

import os, sys, requests, xlwt, xlrd, MySQLdb, datetime, redis
from time import sleep
import pymongo, datetime, random

# from pymongo import MongoClient
# conn = MongoClient('192.168.2.121',10005)
# db = conn.sceneWeb
#
# #打印所有聚集名称，连接聚集
# print u'所有聚集:',db.collection_names()
# sceneDto = db.sceneDto #posts = db['post']
# # print sceneDto
# print "--------------"
# #插入记录
# new_post = {"AccountID":22,"UserName":"libing",'date':datetime.datetime.now()}
# new_posts = [{"AccountID":22,"UserName":"liuw",'date':datetime.datetime.now()},
#              {"AccountID":23,"UserName":"urling",'date':datetime.datetime.now()}]#每条记录插入时间都不一样
#
# posts.insert(new_post)
# #posts.insert(new_posts)#批量插入多条数据
#
# #删除记录
# print u'删除指定记录:\n',posts.find_one({"AccountID":22,"UserName":"libing"})
# posts.remove({"AccountID":22,"UserName":"libing"})
#
# #修改聚集内的记录
# posts.update({"UserName":"urling"},{"$set":{'AccountID':random.randint(20,50)}})

#查询记录，统计记录数量
# print u'记录总计为：',posts.count(),posts.find().count()
# print u'查询单条记录:\n',posts.find_one()
# print sceneDto.find({"_id":"G_10000006"})


# # 获取mongdb中指定记录的内容 ， 字典中的key转换为列表
# a = db.sceneDto.find_one({"_id":"G_10000011"})
# key_value = list(a.keys())
# value_list = list(a.values())
# sum=0
# for i in range(len(key_value)):
#     for j in range(len(value_list)):
#         print key_value[i]
#         print value_list[j+sum]
#         print "-------"
#         if value_list[j+sum] == u"我的家园3":print "[OK,G_10000011,sceneName = 我的家园3]"
#         if value_list[j+sum] == u"myaddresstest":print "[OK,G_10000011,address = myaddresstest]"
#         sum=sum+1
#         break


#查询所有记录
# 查询所有记录print u'查询多条记录:'
#for item in posts.find():#查询全部记录
#for item in posts.find({"UserName":"urling"}):#查询指定记录
#for item in posts.find().sort("UserName"):#查询结果根据UserName排序，默认为升序
#for item in posts.find().sort("UserName",pymongo.ASCENDING):#查询结果根据UserName排序，ASCENDING为升序,DESCENDING为降序
# for item in posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]):#查询结果根据多列排序
#     print item
#
# #查看查询语句的性能
# #posts.create_index([("UserName", pymongo.ASCENDING), ("date", pymongo.DESCENDING)])#加索引
# print posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]).explain()["cursor"]#未加索引用BasicCursor查询记录
# print posts.find().sort([("UserName",pymongo.ASCENDING),('date',pymongo.DESCENDING)]).explain()["nscanned"]#查询语句执行时查询的记录数


# ,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# eval() 使用方法
# 官方demo解释为：将字符串str当成有效的表达式来求值并返回计算结果。
# 用法1：转换 list、tuple、dict、string 互相转化
string1 = '["123456"]'
print eval(string1)  # 转换成list   ，结果：['123456']

string2 = '{"1000":1}'
print eval(string2)  # 转换成dict

string3 = '(1,2,3,4)'
print eval(string3)  # 转换成tuple

# 用法2：将列表中单引号转双引号，并进行引号转义，如 string1输出结果
print str(eval(string1)).replace("'","\\\"")   # 结果：[\"123456\"]

# 用法3：获取字典中的key，结果是列表
print str(eval(string2).keys()).replace("'","\"")    # 结果：["1000"],




