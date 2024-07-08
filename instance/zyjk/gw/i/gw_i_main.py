# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : gw 公卫接口测试
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  testwjw, Qa@123456

# 在线国密SM2加密/解密 https://the-x.cn/zh-cn/cryptography/Sm2.aspx
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# 密钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# 公钥：04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249

# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
# *****************************************************************

from Gw_i_PO import *
gw_i_PO = Gw_i_PO()

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"), Configparser_PO.DB("charset"))  # 测试环境




# # 登录(testwjw, Qa@123456)
encrypt_data = gw_i_PO.encrypt('{"username":"testwjw","password":"Qa@123456","code":"","uuid":""}')
gw_i_PO.curlLogin(encrypt_data)


# # 获取首页信息（健康档案状况）
encrypt_data = gw_i_PO.encrypt('{"orgCode":""}')
r = gw_i_PO.curl('GET', "/server/tEhrInfo/getEhrHomeInfo?0=" + encrypt_data)
print(r)
# 获取健康档案状况信息首页参数和接口url
l_d_result = Sqlserver_PO.select("select summary, query,url from a_phs_server where path='/tEhrInfo/getEhrHomeInfo'")
# print(l_d_result[0]['summary'])
# print(l_d_result[0]['query'])
print("接口url =>", l_d_result[0]['url'])


# 招远市卫健局 - 泉山社区卫生服务中心 - 孙家大沟村
encrypt_data = gw_i_PO.encrypt('{"orgCode":"06850300201"}')
r = gw_i_PO.curl('GET', "/server/tEhrInfo/getEhrHomeInfo?0=" + encrypt_data)
print(r)  # {'code': 200, 'msg': None, 'data': {'manageEhrNum': 26, '...
print(gw_i_PO.decrypt(encrypt_data))

