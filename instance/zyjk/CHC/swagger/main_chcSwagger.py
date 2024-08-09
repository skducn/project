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
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))  # 测试环境
def importDb(d_varMenu_varDbTable):
    # 导入数据库
    for k,v in d_varMenu_varDbTable.items():
        Sqlserver_PO.list2db(['tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url'], Swagger_PO.getAll(k), v)  # 生成index



# todo 获取单接口
# Swagger_PO.getOne("chc-system", 'REST - 用户信息表', '获取没有绑定家医的医助信息')

# todo 获取全部接口
# Swagger_PO.getAll("chc-auth")
# Swagger_PO.getAll("chc-job")
Swagger_PO.getAll("chc-system")
# Swagger_PO.getAll("chc-server")
# Swagger_PO.getAll("chc-rlues")

# todo 导入数据库
# importDb({"chc-auth": "a_chc_auth"})
# importDb({"chc-job": "a_chc_job"})
# importDb({"chc-system": "a_chc_system"})
# importDb({"chc-server": "a_chc_server"})
# importDb({"chc-rlues": "a_chc_rlues"})


