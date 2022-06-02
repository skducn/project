# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-5-25
# Description: # rsa算法
# pip install rsa
# https://blog.csdn.net/Quentin_nb/article/details/123353053
# *****************************************************************


# import rsa
#
# # 生成pubkey和privkey
# (pubkey, privkey) = rsa.newkeys(512)  # 512这个数字表示可以加密的字符串长度，可以是1024，4096等等，
# # (pubkey, privkey) = rsa.newkeys(512, poolsize=8)  # 使用多进程加速生成
#
#
# message = 'hello Bob!'.encode('utf8')
#
# # 加密数据
# crypto = rsa.encrypt(message, pubkey)
# print(crypto)
#
# # 解密数据
# message = rsa.decrypt(crypto, privkey)
# print(message)


'''
管理端
'''

import rsa
import os
from rsa.bigfile import *

(pubkey, privkey) = rsa.newkeys(1024)
print('公钥:', pubkey)
print('私钥:', privkey)

# 保存公/私钥
pub = pubkey.save_pkcs1()
with open('public.pem', 'wb+') as pubfile:
        pubfile.write(pub)
pri = privkey.save_pkcs1()
with open('private.pem', 'wb+') as prifile:
        prifile.write(pri)
print('公/私钥已保存')

# 加密前文件路径
ontology_path = '自定义1'

# 加密后文件路径
ontology_sec_path = '自定义1_1'

# 导入公钥
with open('public.pem', 'rb+') as publickfile:
        p = publickfile.read()
pubkey = rsa.PublicKey.load_pkcs1(p)
print('**********公钥已导入,开始RSA加密**********')

# 加密文件
with open(ontology_path, 'rb') as infile, open(ontology_sec_path, 'wb+') as outfile:
        encrypt_bigfile(infile, outfile, pubkey)
        print('%s文件已成功RSA加密' % os.path.basename(ontology_path))
#
# '''
# 客户端
# '''
# # # 导入私钥
# import rsa
# from rsa.bigfile import *
#
# with open('private.pem', 'rb+') as privatefile:
#         p = privatefile.read()
# privkey = rsa.PrivateKey.load_pkcs1(p)
# print('**********私钥已导入,开始解密**********')
#
# # 解密前文件路径
# ontology_sec_path = '自定义1_1'
#
# # 解密后文件路径
# ontology_path = '自定义1'
#
# # 解密文件
# with open(ontology_sec_path, 'rb') as infile, open(ontology_path, 'wb') as outfile:
#         decrypt_bigfile(infile, outfile, privkey)
#
# print('文件已成功解密')