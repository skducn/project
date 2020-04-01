# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2018-4-17
# Description:  from 智药通患者端接口.docx  开发：周肖（申方C端PC端接口文档）
# 测试环境外网请求：http://101.230.200.46:8094/cetcpatient/
# https://md5jiami.51240.com/  MD5在线加密
# http://tool.chacuo.net/crypt3des 在线3DES加密解密、3DES在线加密解密、3DES encryption and decryption
# http://www.gpsspg.com/maps.htm  GPS 经纬度查询
# *******************************************************************************************************************************

from iDriverTerminalC import *
from Public.PageObject.DatabasePO import *
from Public.PageObject.ThirdPO import *
Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetcpatient')
Third_PO = ThirdPO()


# 初始化数据
testPhone = u"13816109050"
# testPhone = u"199" + str(Third_PO.randomDigit(8))  # 随机生成11个数字，模拟手机号
# print testPhone
myMd5 = hashlib.md5()
myMd5.update(u"111111")  # 'MD5加密密码 123456
passwordMd5 = myMd5.hexdigest()
# print passwordMd5

myMd5 = hashlib.md5()
myMd5.update(u"111111")  # 'MD5加密密码 123456
passwordMd5new = myMd5.hexdigest()
# print passwordMd5new

# connRedis = redis.StrictRedis(host='10.111.3.4', port=6379, db=2, password="b840fc02d524045429941cc15f59e41cb7be6c52")
# testphone = "18717779089"
# print connRedis.get('msg_' + testphone)
# sleep(1212)
# *******************************************************************************************************************************

# resp = iCase("用户注册","i1_N1_C1", testPhone, passwordMd5)

resp = iCase("用户登录", "i1_N2_C1", testPhone, passwordMd5)
varUserId = str(resp).split('patientId":')[1].split(",")[0]
varUserSessionId = str(resp).split('userSessionId":"')[1].split('",')[0]
print u"\033[0;36;30m varUserId = " + str(varUserId)
print u"\033[0;36;30m varUserSessionId = " + str(varUserSessionId)
print u"\033[0;30;30m"



# # # 1：注册 2:找回密码 3：修改手机号
# resp = iCase("获取验证码", "i1_N3_C1", testPhone, '2')
# connRedis = redis.StrictRedis(host='10.111.3.4', port=6379, db=4, password="b840fc02d524045429941cc15f59e41cb7be6c52")
# varCode = connRedis.get('msg_2_' + testPhone)
# print varCode
# resp = iCase("短信验证码验证", "i1_N4_C1", testPhone, varCode, '2')
#
# sleep(1212)

# # # 生成新密码
# myMd5 = hashlib.md5()
# myMd5.update(u"111111")
# passwordMd5new = myMd5.hexdigest()
# resp = iCase("重置密码","i1_N5_C1", testPhone, passwordMd5new)
# resp = iCase("用户登录", "i1_N2_C1", testPhone, passwordMd5new)

# resp = iCase("首页搜索", "i1_N6_C1",  u"仁和".encode('raw_unicode_escape').decode('utf8'),"121.5708443416", "31.2509515368", "500", "1", "1")
# resp = iCase("获取用户设置信息", "i1_N7_C1", varUserId, varUserSessionId)
resp = iCase("分类列表", "i1_N8_C1", varUserId, varUserSessionId)
# resp = iCase("获取医生列表", "i1_N9_C1", varUserId, varUserSessionId, classId, "1", "1")

# f = open(r'D:\\pic\\timg.jpg', 'rb')
# ls_f = base64.b64encode(f.read())
# f.close()
# resp = iCase("图片上传", "i1_N15_C1", varUserId, varUserSessionId, ls_f, "1")
# sleep(1212)

resp = iCase("个人中心", "i1_N21_C1", varUserId, varUserSessionId)
resp = iCase("签到", "i1_N22_C1", varUserId, varUserSessionId)
resp = iCase("订单列表", "i1_N23_C1", varUserId, varUserSessionId, "1", "0", "1", "1")
# resp = iCase("订单详情", "i1_N24_C1", varUserId, varUserSessionId, orderId)
# resp = iCase("取消订单", "i1_N25_C1", varUserId, varUserSessionId, orderId)
# resp = iCase("评价订单", "i1_N26_C1", varUserId, varUserSessionId, orderId, "1", "1")
resp = iCase("修改信息", "i1_N27_C1", varUserId, varUserSessionId, "1", u"患者名字".encode('raw_unicode_escape').decode('utf8'))
resp = iCase("咨询历史列表", "i1_N28_C1", varUserId, varUserSessionId, "1", "0", "1", "1")
# resp = iCase("图片处方历史", "i1_N29_C1", varUserId, varUserSessionId, 咨询Id)

resp = iCase("积分记录", "i1_N30_C1", varUserId, varUserSessionId, u"201804", u"1", u"1")
resp = iCase("修改密码", "i1_N31_C1", varUserId, varUserSessionId, passwordMd5, passwordMd5new)
resp = iCase("业务消息", "i1_N32_C1", varUserId, varUserSessionId, "1", "1")
resp = iCase("系统通知", "i1_N33_C1", varUserId, varUserSessionId, "1", "1")

