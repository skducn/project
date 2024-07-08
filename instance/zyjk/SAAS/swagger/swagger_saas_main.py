# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : CHC swagger
# http://192.168.0.202:22081/doc.html
# https://www.sojson.com/
# *********************************************************************
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
from instance.zyjk.swagger.SwaggerPO import *
Swagger_PO = SwaggerPO(Configparser_PO.HTTP("url"), Configparser_PO.HTTP("pagename"))
from PO.MysqlPO import *
Mysql_PO = MysqlPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("port"))  # 测试环境
def importDb(d_varMenu_varDbTable):
    # 导入数据库
    for k,v in d_varMenu_varDbTable.items():
        Mysql_PO.list2db(['tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url'], Swagger_PO.getAll(k), v)  # 生成index



# todo 获取单接口
# Swagger_PO.getOne("hypertension", '高血压首页Server', '查询高血压首页数据')
# Swagger_PO.getOne("saasuser", '短信发送接口', '短信发送')
# Swagger_PO.getOne("saasuser", 'saasuser-医联体接口', '医院机构查询-PC')


# todo 获取全部接口
# Swagger_PO.getAll("auth")
# Swagger_PO.getAll("saasuser")
# Swagger_PO.getAll("cms")
# Swagger_PO.getAll("cuser")
# Swagger_PO.getAll("ecg")
# Swagger_PO.getAll("saascrf")
# Swagger_PO.getAll("hypertension")
Swagger_PO.getAll("saassign")

# todo 导入数据库
importDb({"auth": "a_saas_auth"})
importDb({"saasuser": "a_saas_saasuser"})
importDb({"cms": "a_saas_cms"})
importDb({"cuser": "a_saas_cuser"})
importDb({"ecg": "a_saas_ecg"})
importDb({"saascrf": "a_saas_saascrf"})
importDb({"hypertension": "a_saas_hypertension"})
importDb({"saassign": "a_saas_saassign"})


