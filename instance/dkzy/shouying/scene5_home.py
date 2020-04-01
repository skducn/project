# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 电科智药，首页
# 业务场景：修改手机号，修改邮箱
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from dkzy.shouying.config.config import *
from dkzy.shouying.PageObject.ShouyingPO import *
from Public.PageObject.ThirdPO import *
from Public.PageObject.DatabasePO import *
Level_PO = LevelPO(driver)
Shouying_PO = ShouyingPO(Level_PO)
Third_PO = ThirdPO()
Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetc_sy')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''检查修改手机号'''
# newPhone = Third_PO.randomPhone()
newPhone = u"13449368522"
print newPhone
Level_PO.openURL(1200, 900, varUrl, 3)
Level_PO.setMaximize()
Shouying_PO.login(u"14416109001", u"q123456")
Level_PO.clickId("btn-modify-phone-number", 2)  # 修改手机号
Level_PO.inputId("modal-phone-number", newPhone)  # 输入新的手机号
Level_PO.clickId("btn-modify-phone-number-send-sms", 2)  # 发送验证码
varCaptcha = connRedis.get('sms_' + newPhone)
Level_PO.inputId("modify-phone-number-sms-code", varCaptcha.split('code":"')[1].split('"')[0])  # 输入验证码
Level_PO.clickId("btn-consume-validate-message", 2)  # 确认


