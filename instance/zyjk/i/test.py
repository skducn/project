#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @ProjectName: Demo
# @Name: gm_test.py.py
# @Auth: arbboter
# @Date: 2022/9/6-14:06
# @Desc:
# @Ver : 0.0.0.1
from gmssl import sm2
# from gmssl import func as GMFunc
# from random import SystemRandom
# from base64 import b64encode, b64decode

# thirdPublicKey: 0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b
# thirdPrivateKey: 686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b
# publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
# privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62

import binascii
# from gmssl import sm2, func
#
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
public_key = '025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
#
sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
#
data = '{"password": "Qa@123456", "username": "testwjw"}'
data = data.encode("utf-8")

enc_data = sm2_crypt.encrypt(data)
# enc_data = self._SM2_Util.encrypt(data_utf8)
enc_data = binascii.b2a_hex(enc_data).decode("utf-8")
# return enc_data
print(enc_data)

# enc_data = 'b3e3562c188004201ddd02dbd53f3f735dddda6a282d216ee181d722557173c10894c51ef5905f7e224d2e25d443443a65983eddbe65264fbc72c1f6bc78e75df7e9502cbc4a89294893021a06429f8d180e3b863aef0f59d3eaa1d9734dfa970d4472e79775bfdaaccc47a6a47a651c089fcc0668cfa718959b5e6cf94757ee8142b01489dc3a1709b39c34239643794a7d254f774167b9b2bc7ec14efcea6baafc96083b394ae7059b92721f6ce1123d67fe795804a2b106bed0c4527f7036514e8667c9'
enc_data = '73e28912e15615778fe496146cad41c120cbfd145304288cf0e97104404218c89df717d2d8772638caaba2af7a2209037c68964dab8ce89411bb853fe89835ef1cc63d45a2d6187f5f6ab747617331b38696fa00622379303648b9f9cf7436b9290ca9cc66197f6237a889671ce9452e71474b92c2672a3fa41f45701f079c2e9d224ffbf3531d1703e24ca310c0a190'
enc_data = binascii.a2b_hex(enc_data.encode("utf-8"))
# dec_data = self._SM2_Util.decrypt(enc_data)
# print(enc_data)
dec_data = sm2_crypt.decrypt(enc_data)
dec_data = dec_data.decode("utf-8")
# dec_data = dec_data.decode("utf-8")
print(dec_data)

# dec_data = sm2_crypt.decrypt(enc_data)
# print(dec_data)
#
#
# dec_data = sm2_crypt.decrypt(b'd60ba7249cb4baba98d23e937c2b88b36229b5c78d6129b9db081cfa35ebde9f337aa6c6c46171908a05c7eefecc37a504216606b11c41eba1bb44bfa54ecd44d4795f1fdd09543e9d1cb72e31024a11c745b922ef1d900e5f961c2d1202a0ef47486a541a8c4bed903686bad93656205e6baed842653b81edad17fb770c1633f2f93a179635f9565487bd1ae40cfdbddf7ed753b00e3a5bdcb634f79e')
# print(dec_data)
#
# # print("1.1 中文转字节码".center(100, "-"))
# # print(Char_PO.chinese2byte("金浩", "utf-8"))  # b'\xe9\x87\x91\xe6\xb5\xa9'
# # print(Char_PO.chinese2byte("金浩", "GBK"))  # b'\xbd\xf0\xba\xc6'
# #
# # print("1.2 字节码转中文字符串".center(100, "-"))
# # print(Char_PO.byte2chinese(b"\xe9\x87\x91\xe6\xb5\xa9", "utf-8"))  # 金浩
# # print(Char_PO.byte2chinese(b"\xbd\xf0\xba\xc6", "gbk"))  # 金浩
#
#
# print(dec_data.decode())


# from PO.Sm2PO import *
#
# d = SM2Util.GenKeyPair()
# print(d)
#
# # todo 对数据签名与验证
# data = '123456'
# sm2 = SM2Util(pri_key=d['private'], pub_key=d['public'][2:])
# sign = sm2.Sign(data)
# print('签名:{} 验签:{}'.format(sign, sm2.Verify(data,
#                                             sign)))  # 签名:e63652b2c2c3f983a06e5c7b6fe7d37f0fc42f058ce70ee3c6f6fdaf3c7b7534a05659bd2f7ab5d4c6a15a4d7512c92bcda48d2af607cedebb5190d863d20210 验签:True
#
# # todo 加密与解密
# dataEncrypt = sm2.Encrypt(data)
# print('加密:{}'.format(dataEncrypt))  # 加密:jbm5KDRjoZSgJinaAxcsbOPakFKQ/oLiwn49LCpm7johHp9wSZud12GMqXdYGC35XA8cmOCZJ70FS7hpdAAcGWDen47AvH/htbqprHLhteR54OPWbeYSl80xgz/tBL3RwgAg6UJh
#
# dataDecrypt = sm2.Decrypt(dataEncrypt)
# print('解密:{}'.format(dataDecrypt))  # 解密:123456