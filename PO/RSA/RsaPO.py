# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2021-11-18
# Description   : rsa加密 , 加密字符串
# pip install pycryptodome
# 步骤：
# 1，执行 RsaPO.py 生成 公钥私钥
# 2，jiami.py
# 3,jiemi.py
# *******************************************************************************************************************************

from Crypto.PublicKey import RSA

key = RSA.generate(2048)
# print(key)

# 提取私钥并存入文件
private_key = key.export_key()
file_out = open("private_key.pem", "wb")
file_out.write(private_key)

# 提取公钥存入文件
public_key = key.publickey().export_key()
file_out = open("public_key.pem", "wb")
file_out.write(public_key)