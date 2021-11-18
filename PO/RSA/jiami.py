# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2021-11-18
# Description   : rsa加密
# pip install pycryptodome
# *******************************************************************************************************************************

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 要加密的内容
data = b"Jinhao!123"

# 从文件中读取公钥
public_key = RSA.import_key(open("public_key.pem").read())
# 实例化加密套件
cipher = PKCS1_OAEP.new(public_key)
# 加密
encrypted_data = cipher.encrypt(data)

# 将加密后的内容写入到文件
file_out = open("encrypted_data.bin", "wb")
file_out.write(encrypted_data)