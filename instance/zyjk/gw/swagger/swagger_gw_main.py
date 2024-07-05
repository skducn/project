# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2022-6-13
# Description   : swagger导入数据库
# http://192.168.0.203:38080/doc.html
# *********************************************************************

from SwaggerGwPO import *
SwaggerPO_PO = SwaggerGwPO()

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")

iUrl = 'http://192.168.0.203:38080'
iDoc = '/doc.html'


# 单点调试
SwaggerPO_PO.getOne("phs-third-api", 'REST - 第三方模块老年人接口', '保存第三方问诊记录')
# SwaggerPO_PO.getOne("phs-server", '残疾人管理-专项登记', '分页查询')
# SwaggerPO_PO.getOne("phs-server", 'REST - 三高、冠心病、脑卒中随访任务管理', '获取登陆人机构逾期随访数')
# ['phs-server', 'REST - 三高、冠心病、脑卒中随访任务管理', '获取登陆人机构逾期随访数']

# 获取全部
# SwaggerPO_PO.getAll("phs-auth")
# SwaggerPO_PO.getAll("phs-job")
# SwaggerPO_PO.getAll("phs-system")
# SwaggerPO_PO.getAll("phs-server")
# SwaggerPO_PO.getAll("phs-server-export")
# SwaggerPO_PO.getAll("phs-third-api")



def importDb(d_varMenu_varDbTable):
    # 导入数据库
    for k,v in d_varMenu_varDbTable.items():
        Sqlserver_PO.list2db(['tags', 'summary', 'path', 'method', 'consumes', 'query', 'body', 'url'], SwaggerPO_PO.getAll(k), v)  # 生成index


# importDb({"phs-auth": "a_phs_auth"})
# importDb({"phs-job": "a_phs_job"})
# importDb({"phs-system": "a_phs_system"})
# importDb({"phs-server": "a_phs_server"})
# importDb({"phs-server-export": "a_phs_server_export"})
# importDb({"phs-third-api": "a_phs_third_api"})







