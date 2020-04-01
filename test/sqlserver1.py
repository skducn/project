# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2019-3-3
# Description: sqlserver, pymssql-2.1.4
# pymssql官方:https://pypi.org/project/pymssql/
# pip3 install pymssql
# http://www.cnblogs.com/toheart/p/9802990.html
#***************************************************************
import hashlib
import hmac
import json
import pymssql
from requests import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, HttpRequest




@api_view(['GET', 'POST'])
def userlogin(req,format=None):
    ms = MSSQL(host="192.168.0.164", user="sa", pwd="qwert123!@#", db="pim")
    if req.method == 'GET':
        username = req.GET['username']
        password = req.GET['password']
    elif req.method == 'POST':
        username=  req.POST['username']
        password = req.POST['password']
    newsql =  "select * from t_upms_user where name = '"+username+"'"
    print(newsql)
    reslist = ms.ExecQuery(newsql.encode('utf-8'))
    # //验证password加密后==LoginPwd
    print(password)
    print(reslist[0].get("LoginKey"))
    if Encrypt(password,reslist[0].get("LoginKey"))==reslist[0].get("LoginKey"):
        reslist =json_success(reslist)
    else:
        reslist =json_error(reslist)
    # meizis = System_Users.objects.all()
    # serializer = MeiziSerializer(reslist, many=True)
    # return Response(serializer.data)
    return HttpResponse(json.dumps(reslist, default=lambda obj: obj.__dict__), content_type='application/json')
    # return reslist

def Encrypt(password="",salt = ""):
    clearBytes=[]
    hasheByte=[]
    # # encoding = unicode
    # clearBytes= bytes(salt.lower().strip()+password.strip(),encoding='Unicode')
    # salt = crypt.mksalt(crypt.METHOD_SHA512)
    # 然后再进行数据加密:
    # hasheByte = crypt.crypt("helloworld", salt)
    # hasheByte =crypt.crypt(clearBytes, salt)
    # password = hmac.new(key=clearBytes, msg=password)
    # 待加密信息
    str =salt.lower().strip()+password.strip()
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    print('MD5加密前为 ：' + str)
    hl.update(str.encode(encoding='utf-16'))
    print('MD5加密后为 ：' + hl.hexdigest())
    hl.update(str.encode(encoding='UTF-8'))
    print('MD5加密后为 ：' + hl.hexdigest())
    hl.update(str.encode(encoding='GBK'))
    print('MD5加密后为 ：' + hl.hexdigest())
    hl.update(str.encode(encoding='GB2312'))
    print('MD5加密后为 ：' + hl.hexdigest())
    print(password)
    return password


def json_success(data, code=200, foreign_penetrate=False, **kwargs):
     data = {
         "status": code,
         "msg": "成功",
         "data": data,
     }
     print(data)
     return data

def json_error(error_string="失败", code=500, **kwargs):
     data = {
            "status": code,
            "msg": error_string,
            "data": {}
        }
     data.update(kwargs)
     return data

class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
def __GetConnect(self):
    if not self.db:
        raise (NameError, "没有设置数据库信息")
    self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="GBK")
    cur = self.conn.cursor()
    if not cur:
        raise (NameError, "连接数据库失败")
    else:
        return cur

def ExecQuery(self, sql):
    cur = self.__GetConnect()
    cur.execute(sql)
    resList = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]

    result = []
    for row in resList:
        objDict = {}
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(row):
            index, col_names[index], value
            objDict[col_names[index]] = value
        result.append(objDict)

    # 查询完毕后必须关闭连接
    self.conn.close()
    return result

def ExecNonQuery(self, sql):
    cur = self.__GetConnect()
    cur.execute(sql)
    self.conn.commit()
    self.conn.close()
