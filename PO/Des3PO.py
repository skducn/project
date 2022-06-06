# coding: utf-8
# # *******************************************************************************************************************************
# Author     : John
# Date       : 2022/6/6
# Description: 3des.py
# pip3.9 install pyDes
# k = pyDes.des(key, mode, IV=IV, pad=None, padmode=pyDes.PAD_PKCS5) # 传入秘钥,加密方式
# k = key加密方式ECB秘钥必须是八位字节
# mode = pyDes.ECB # 加密方式 默认是ECB,也可以不填写
# IV = "00000000" # 偏移量,加密方式不是ECB的时候加密key字段必须是16位字节,秘钥不够用0补充
# d = k.encrypt(data) # 加密数据
# base = str(base64.b64encode(d), encoding="utf-8") # 指定输出格式为base6

# 如果参数是json格式需转成标准的json格式
# import json
# data = {"role_name": "测试"}
# data = json.dumps(data)

# # *******************************************************************************************************************************

import pyDes
import base64

from Crypto.Cipher import DES3
import codecs
import base64,json


class Des3PO():

    def __init__(self, key):

        # k = pyDes.des(key, mode, IV=IV, pad=None, padmode=pyDes.PAD_PKCS5)  # 传入秘钥,加密方式

        self.key = key  # key加密方式ECB秘钥必须是八位字节
        self.mode = pyDes.ECB  # 加密方式默认是ECB, 可不写
        self.iv = b'01234567'  # 偏移量，加密方式不是ECB的时候加密key字段必须是16位字节,秘钥不够用0补充
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
        msg = str(base64.b64encode(res), encoding="utf8")  # 指定输出格式为base6
        # msg =  res.hex()
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        # res = bytes.fromhex(decrData)
        msg = self.des3.decrypt(res).decode("utf8")
        return self.unpad(msg)


if __name__ == "__main__":


    my24 = "skducn@163.com!@#$%^&*()"  # 加密key,加密方式ECB秘钥必须是八位字节


    print("1 加密字符串".center(100, "-"))
    Des3_PO = Des3PO(my24)
    res = Des3_PO.encrypt("测试123")
    # print(res)  # 6oA9kbmEB5RuS2zwFALL92ntpMdr9Tw5
    Des3_PO = Des3PO(my24)
    print(Des3_PO.decrypt(res))  # 测试123


    print("2 加密json格式字符串".center(100, "-"))
    data = {"role_name": "55555hao好"}
    data = json.dumps(data, ensure_ascii=False)  # 不使用的ascii编码，以gbk编码
    Des3_PO = Des3PO(my24)
    res = Des3_PO.encrypt(data)
    # print(res)  # UEeI1QLXuU32t/B6MPglC4MYxfSxiGxm1wi0AQi7TbY=
    Des3_PO = Des3PO(my24)
    print(Des3_PO.decrypt(res))  # {"role_name": "55555hao好"}




