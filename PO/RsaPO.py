# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2021-11-18
# Description   : rsa加密 , 加密字符串
# pip install pycryptodome
# 步骤：
# 1，RsaPO.py 生成公钥与私钥
# 2，用公钥加密内容
# 3，用私钥解密内容
# *******************************************************************************************************************************

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import sys

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

    def encrypt(self, public_key_pem, varContent, toBinFile):
        '''
        用公钥加密内容，生成encrypted_data.bin
        :param public_key_pem:
        :param varContent:
        :param toBinFile:
        :return:
        '''

        try:
            # 加密中文
            data = varContent.encode("utf-8")  # 转换成bytes , 如：b'\xe6\x8b\x9b\xe8\xbf\x9c\xe9\x98\xb2\xe7\x96\xab\xe9\xa1\xb9\xe7\x9b\xae\xe6\x8e\xa5\xe5\x8f\xa3\xe6\xb5\x8b\xe8\xaf\x95\xe6\x8a\xa5\xe5\x91\x8a'

            # 读公钥
            public_key = RSA.import_key(open(public_key_pem).read())
            cipher = PKCS1_OAEP.new(public_key)
            # 加密
            encrypted_data = cipher.encrypt(data)
            # 将加密后的内容写入到文件
            file_out = open(toBinFile, "wb")
            file_out.write(encrypted_data)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


    def decrypt(self, private_key_pem, fromBinFile):
        '''
        用私钥解密内容
        :param private_key_pem:
        :param fromBinFile:
        :return:
        '''

        try:
            # 读取私钥
            private_key = RSA.import_key(open(private_key_pem, "rb").read())
            cipher = PKCS1_OAEP.new(private_key)
            # 从文件中读取加密内容
            encrypted_data = open(fromBinFile, "rb").read()
            # 解密
            data = cipher.decrypt(encrypted_data)
            data = data.decode("utf-8", 'strict')  # 将 bytes转换成字符串
            return (data)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


if __name__ == "__main__":

    Rsa_PO = RsaPO("./data/private_key.pem", "./data/public_key.pem")
    Rsa_PO.encrypt("./data/public_key.pem", "招远防疫项目接口测试报告", "./data/encrypted_data.bin")
    print(Rsa_PO.decrypt("./data/private_key.pem", "./data/encrypted_data.bin"))  # 招远防疫项目接口测试报告
