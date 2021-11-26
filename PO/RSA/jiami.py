# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2021-11-18
# Description   : rsa加密
# pip install pycryptodome
# *******************************************************************************************************************************

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 机密数字或英文
# data ="12121212"

# 加密中文
data = "招远防疫项目接口测试报告"
data = data.encode("utf-8")  # 转换成bytes , 如：b'\xe6\x8b\x9b\xe8\xbf\x9c\xe9\x98\xb2\xe7\x96\xab\xe9\xa1\xb9\xe7\x9b\xae\xe6\x8e\xa5\xe5\x8f\xa3\xe6\xb5\x8b\xe8\xaf\x95\xe6\x8a\xa5\xe5\x91\x8a'

print(data)

# 从文件中读取公钥
public_key = RSA.import_key(open("public_key.pem").read())
# 实例化加密套件
cipher = PKCS1_OAEP.new(public_key)
# 加密
encrypted_data = cipher.encrypt(data)
# 将加密后的内容写入到文件
file_out = open("encrypted_data.bin", "wb")
file_out.write(encrypted_data)