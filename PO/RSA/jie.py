# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2021-11-18
# Description   : rsa加密
# pip install pycryptodome
# *******************************************************************************************************************************

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# 从私钥文件中读取私钥
private_key = RSA.import_key(open("private_key.pem", "rb").read())
# 实例化加密套件
cipher = PKCS1_OAEP.new(private_key)
# 从文件中读取加密内容
encrypted_data = open("encrypted_data.bin", "rb").read()
# 解密
data = cipher.decrypt(encrypted_data)
data = data.decode("utf-8", 'strict')  # 将 bytes转换成字符串
print(data)
