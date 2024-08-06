# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-8-6
# Description: 社区健康管理中心 接口
# 接口文档：http://192.168.0.202:22081/doc.html
# https://www.sojson.com/

# 测试环境 http://192.168.0.243:8010/#/login
# 'cs', '12345678'

# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'

# todo nacos
# http://192.168.0.223:8848/nacos/	nacos,Zy123456
# chc-test
# chc-gateway-sqlserver.yml
# enabled: false    // 改为false无法登录，因为页面加密，用于接口测试
# 安全配置
# # security:
#   验证码
#   # captcha:
#   #   enabled: false    //去掉验证码

# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2
#***************************************************************

from ChcIquanquPO import *
ChcIquanqu_PO = ChcIquanquPO('{"username":"cs","password":"12345678","code":"","uuid":""}')


# 1，获取菜单
d = ChcIquanqu_PO.curl("GET", '/system/sysSystem/systemMenuInfoBySystemId?0=', '{"systemId":1}')
print(d)  # {'code': 200, 'msg': None, 'data': [{'id': 2, 'systemId': 1, 'name': '居民健康服务', 'paren...
print(d['data'][0]['name'], d['data'][0]['url'])  # 居民健康服务 /SignManage
print(d['data'][0]['children'][0]['name'], d['data'][0]['children'][0]['url'])  # 健康服务 /SignManage/service



