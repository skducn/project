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


# 单点调试
# SwaggerPO_PO.getOne("phs-third-api", '保存第三方问诊记录')
SwaggerPO_PO.getOne("phs-server", '老年人批量登记')


# 获取全部
# SwaggerPO_PO.getAll("phs-auth")
# SwaggerPO_PO.getAll("phs-job")
# SwaggerPO_PO.getAll("phs-server")
# SwaggerPO_PO.getAll("phs-server-export")
# SwaggerPO_PO.getAll("phs-third-api")


# 导入数据库
# # Sqlserver_PO.list2db(['tags','summary','path','method','consumes','query','body'], SwaggerPO_PO.getAll("phs-auth"), "a_phs_auth")  # 生成index
# Sqlserver_PO.list2db(['tags','summary','path','method','consumes','query','body'], SwaggerPO_PO.getAll("phs-job"), "a_phs_job")  # 生成index
# Sqlserver_PO.list2db(['tags','summary','path','method','consumes','query','body'], SwaggerPO_PO.getAll("phs-third-api"), "a_phs_third_api")  # 生成index
# Sqlserver_PO.list2db(['tags','summary','path','method','consumes','query','body'], SwaggerPO_PO.getAll("phs-server"), "a_phs_server")  # 生成index
# Sqlserver_PO.list2db(['tags','summary','path','method','consumes','query','body'], SwaggerPO_PO.getAll("phs-server-export"), "a_phs_server_export")  # 生成index
# Sqlserver_PO.list2db(['tags','summary','path','method','consumes','query','body'], SwaggerPO_PO.getAll("phs-system"), "a_phs_system")  # 生成index







