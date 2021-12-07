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
from Crypto.Cipher import PKCS1_OAEP

class RsaPO():

    def __init__(self, private_key_pem, public_key_pem):

        # 初始化生成公钥私钥
        key = RSA.generate(2048)

        # 私钥
        private_key = key.export_key()
        file_out = open(private_key_pem, "wb")
        file_out.write(private_key)

        # 公钥
        public_key = key.publickey().export_key()
        file_out = open(public_key_pem, "wb")
        file_out.write(public_key)

    def jiami(self, varContent, toBinFile):
        # jiami("加密的字符串", "encrypted_data.bin")
        # 加密中文
        data = varContent.encode("utf-8")  # 转换成bytes , 如：b'\xe6\x8b\x9b\xe8\xbf\x9c\xe9\x98\xb2\xe7\x96\xab\xe9\xa1\xb9\xe7\x9b\xae\xe6\x8e\xa5\xe5\x8f\xa3\xe6\xb5\x8b\xe8\xaf\x95\xe6\x8a\xa5\xe5\x91\x8a'
        # print(data)

        # 读公钥
        public_key = RSA.import_key(open("public_key.pem").read())
        cipher = PKCS1_OAEP.new(public_key)
        # 加密
        encrypted_data = cipher.encrypt(data)
        # 将加密后的内容写入到文件
        file_out = open(toBinFile, "wb")
        file_out.write(encrypted_data)

    def jiemi(self, fromBinFile):
        # Rsa_PO.jiemi("data.bin")
        # 读取私钥
        private_key = RSA.import_key(open("private_key.pem", "rb").read())
        cipher = PKCS1_OAEP.new(private_key)
        # 从文件中读取加密内容
        encrypted_data = open(fromBinFile, "rb").read()
        # 解密
        data = cipher.decrypt(encrypted_data)
        data = data.decode("utf-8", 'strict')  # 将 bytes转换成字符串
        return (data)


if __name__ == "__main__":

    Rsa_PO = RsaPO("private_key.pem", "public_key.pem")
    Rsa_PO.jiami("招远防疫项目接口测试报告", "encrypted_data.bin")
    Rsa_PO.jiemi("encrypted_data.bin")
