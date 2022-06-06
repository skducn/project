# coding: utf-8
# # *******************************************************************************************************************************
# Author     : John
# Date       : 2022/6/6
# Description: 3des.py
# pip install pyDes

# 如果参数是中文需设置编码
# data = "你好"
# data = data.encode('utf-8')

# 如果参数是json格式需转成标准的json格式
# import json
# data = {"role_name": "测试"}
# data = json.dumps(data)

# # *******************************************************************************************************************************

import pyDes
import base64

from Crypto.Cipher import DES3
import codecs
import base64


class EncryptDate:
    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.iv = b'01234567'  # 偏移量
        self.length = DES3.block_size  # 初始化数据块大小
        self.des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)  # 初始化AES,CBC模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数

        res = self.des3.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        # msg =  res.hex()
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        # res = bytes.fromhex(decrData)
        msg = self.des3.decrypt(res).decode("utf8")
        return self.unpad(msg)


eg = EncryptDate("liuyunqiang@lx100$#365#$")  # 这里密钥的长度必须是16的倍数
# res = eg.encrypt("test123123123345345")
# print(res)

import json
data = {"role_name": "55555hao好"}
data = json.dumps(data)
print(data)
res = eg.encrypt(data)
print(res)

# data = "你好吗"
# res = eg.encrypt(data)
# print(res)



eg1 = EncryptDate("liuyunqiang@lx100$#365#$")
print(eg1.decrypt(res))

# data = "你好吗"
# data = data.encode("utf-8")
# res = eg.encrypt(data)
# eg1 = EncryptDate("liuyunqiang@lx100$#365#$")
# print(eg1.decrypt(res))


# import pyDes
#
# import base64
#
# data = 'hello'
#
# key = "kkk11111" # 加密key,加密方式ECB秘钥必须是八位字节
#
# mode = pyDes.ECB # 加密方式 默认是ECB,也可以不填写
#
# IV = "00000000" # 偏移量,加密方式不是ECB的时候加密key字段必须是16位字节,秘钥不够用0补充
#
# k = pyDes.des(key, mode, IV=IV, pad=None, padmode=pyDes.PAD_PKCS5) # 传入秘钥,加密方式
#
# d = k.encrypt(data) # 加密数据
#
#
# base = str(base64.b64encode(d), encoding="utf-8") # 指定输出格式为base64
#
# print(base)
