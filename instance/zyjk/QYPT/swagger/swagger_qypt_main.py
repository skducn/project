# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : 区域平台 swagger导入数据库
# http://192.168.0.201:28801/doc.html
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
Swagger_PO.getOne("auth", '鉴权中心', 'pc用户登录')


# todo 获取全部接口
# Swagger_PO.getAll("auth")
# Swagger_PO.getAll("regional-api")
# Swagger_PO.getAll("regional-bi")
# Swagger_PO.getAll("regional-upv")
# Swagger_PO.getAll("regional-dqc")
# Swagger_PO.getAll("regional-dict")
# Swagger_PO.getAll("regional-user")
# Swagger_PO.getAll("regional-spd")
# Swagger_PO.getAll("regional-cda")
# Swagger_PO.getAll("regional-bus")

# todo 导入数据库
# importDb({"auth": "a_auth"})
# importDb({"regional-bi": "a_regional_bi"})
# importDb({"regional-upv": "a_regional_upv"})
# importDb({"regional-dqc": "a_regional_dqc"})
# importDb({"regional-dict": "a_regional_dict"})
# importDb({"regional-user": "a_regional_user"})
# importDb({"regional-spd": "a_regional_spd"})
# importDb({"regional-cda": "a_regional_cda"})
# importDb({"regional-bus": "a_regional_bus"})








