# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : gw swagger导入数据库
# http://192.168.0.203:38080/doc.html
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
# Swagger_PO.getOne("phs-third-api", 'REST - 第三方模块老年人接口', '保存第三方问诊记录')
# Swagger_PO.getOne("phs-server", '残疾人管理-专项登记', '分页查询')
# Swagger_PO.getOne("phs-server", 'REST - 三高、冠心病、脑卒中随访任务管理', '获取登陆人机构逾期随访数')
# ['phs-server', 'REST - 三高、冠心病、脑卒中随访任务管理', '获取登陆人机构逾期随访数']

# todo 获取全部接口
# Swagger_PO.getAll("phs-auth")
# Swagger_PO.getAll("phs-job")
# Swagger_PO.getAll("phs-system")
# Swagger_PO.getAll("phs-server")
# Swagger_PO.getAll("phs-server-export")
# Swagger_PO.getAll("phs-third-api")

# todo 导入数据库
importDb({"phs-auth": "a_phs_auth"})
# importDb({"phs-job": "a_phs_job"})
# importDb({"phs-system": "a_phs_system"})
# importDb({"phs-server": "a_phs_server"})
# importDb({"phs-server-export": "a_phs_server_export"})
# importDb({"phs-third-api": "a_phs_third_api"})







