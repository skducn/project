# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
#  publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
#  privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# *****************************************************************


from gmssl import sm2, func

# private_key=func.random_hex(64)  # 生成随机64字节的16进制私钥
# public_key = sm2.CryptSM2._kg('这里填写私钥', '这里填写基点')  # 通过私钥生成随机128字节的16进制公钥，这里要注意格式
# public_key  = '04' + public_key   # 生成128字节的16进制公钥加上04标识符，表示未压缩

public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'

a = 'http://192.168.0.203:30080/assets/index.a5ea955a.js'

print(a[-3:])


# l_div = ['ceshi',3,4,5,'ceshi',333333,'ceshi']
#
# ele_n = l_div.index(333333)
# print(ele_n)
# l_div.insert(ele_n, '其他残疾备注')
# print(l_div)

# import base64
# from gmssl import sm2, func
#
# # 公钥和私钥应该是16进制的字符串
# public_key_hex = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
# private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# # public_key_hex = '04ac0c6afcbf31f******************************'
# # private_key_hex = ''  # 替换为实际的私钥16进制字符串，本文的过程不涉及私钥，主要你也搞不到人家的私钥
# # 初始化SM2加密对象
# # sm2_crypt = sm2.CryptSM2(public_key=public_key_hex, private_key=private_key_hex, mode=0)
#
# # 这里所涉及的mode怎么回事，你可以看看官网文档，如果看不懂，私信我也行
#
# # data = '9b084459d661e54a15b29aec36c837423c664bb16e593ac63bbbd01ac4fc6946936a18eb1e9b216532a7598156d49d94a643a24a593ccbe78e8c6a0e5ab9831fc15d82422502dac8eac754f9c2684f5141ec17d10e5a6b23a5c297054cc37d858cf8739ac8d060f722bfdf97e4310dc3e8'
#
# from gmssl import sm2, func
#
# # 假设你已经有了一个加密的信息和对应的密钥
# # 这里的加密信息是以字节串的形式给出
# encrypted_msg = b'9b084459d661e54a15b29aec36c837423c664bb16e593ac63bbbd01ac4fc6946936a18eb1e9b216532a7598156d49d94a643a24a593ccbe78e8c6a0e5ab9831fc15d82422502dac8eac754f9c2684f5141ec17d10e5a6b23a5c297054cc37d858cf8739ac8d060f722bfdf97e4310dc3e8'
# # 这里的密钥也是以字节串的形式给出
# private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
#
# from gmssl import sm2, func
#
# # private_key = '3AAB68B3D8C805F4D1F6A4D09B9C6CFA6C3C1E1C4820656333C1C94C27F6A049'
# # public_key = '10808F0E5C5B116D0C2E3A791C5DE4D19D37A6C6A1C3A6ED7F8E9D9B6BE1AED8A16F5F8556413B2862A2A3B8D9DC5B9F9F5B10E7F4C547C5D38B28AFD1A0FAF'
#
# sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
#
# data = b'hello,world'
# enc_data = sm2_crypt.encrypt(data)
# print(enc_data)
# a = enc_data.hex()
# print(a)
#
# dec_data = sm2_crypt.decrypt(enc_data)
# print(dec_data)
# a = dec_data.hex()
# print(a)

# 将文本数据编码为UTF-8格式的字节串
# data = password.strip().replace('\n', '').encode('utf-8')

# aa = 'BFaiKXU5FMTbtRtLqVfd6dOw2wJYO9EjESk7ri969NdLlr4jgfQ6OPI3x4wfHn2t2rAZner+CCmp+2szLvAggDNcyoH/2d/4HLd5rlpNrHinRXz0GkltmREjRdjH+MFvTOomiFKOl9cPf/AoQf3LoOwM'
# # 加密数据
# enc_data = sm2_crypt.encrypt(data)
# print(enc_data)
#
# # a = 'BFaiKXU5FMTbtRtLqVfd6dOw2wJYO9EjESk7ri969NdLlr4jgfQ6OPI3x4wfHn2t2rAZner+CCmp+2szLvAggDNcyoH/2d/4HLd5rlpNrHinRXz0GkltmREjRdjH+MFvTOomiFKOl9cPf/AoQf3LoOwM'
# # # 将加密后的数据转换为十六进制字符串
# # hex_enc_data = a.hex()
# print(hex_enc_data)

# {"orgCode":"G02"}


# 更新POST数据中的用户名和密码
# post_data['Password'] = '04' + hex_enc_data

# print("")


# for i in range(len(l_input)):
#     if l_input[i] == 'ceshi':
#         print(i)
        # ele_n = l_input.index(l_input[i])
        # print(ele_n)


# private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# public_key = '025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
# data = '12345'
#
# def encrypt(self, data: str):
#     """
#     进行 SM2 加密操作
#     :param data: String 格式的原文 data
#     :return: String 格式的密文 enc_data
#     """
#     data_utf8 = data.encode("utf-8")
#     enc_data = self._SM2_Util.encrypt(data_utf8)
#     self._SM2_Util = sm2.CryptSM2(public_key=public_key, private_key=private_key)
#
#     enc_data = binascii.b2a_hex(enc_data).decode("utf-8")
#     return enc_data
#
#
# def decrypt(self, enc_data: str):
#     """
#     进行 SM2 解密操作
#     :param enc_data: String 格式的密文 enc_data
#     :return: String 格式的原文 data
#     """
#     enc_data = binascii.a2b_hex(enc_data.encode("utf-8"))
#     dec_data = self._SM2_Util.decrypt(enc_data)
#     dec_data = dec_data.decode("utf-8")
#     return dec_data
#
# print(encrypt(data))

# crypt_sm2 = CryptSM2(private_key = private_key, public_key=public_key)
# # private_key = crypt_sm2.get_random_private_key()
# # public_key = crypt_sm2.get_public_key(private_key)
# # print(private_key)
#
# ciphertext = crypt_sm2.encrypt(b'Hello, World!')
# print(ciphertext)

# from Cryptodome.PublicKey import ECC
# from Cryptodome.Cipher import PKCS1_OAEP
#
# # # 生成SM2密钥对
# # key = ECC.generate(curve="SM2")
# # public_key = key.public_key().export_key(format='PEM')
# # private_key = key.export_key(format='PEM')
#
# private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# public_key = '025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
# data = '12345'
#
# # 加载公钥
# public_key = ECC.import_key(public_key)
#
# # 使用公钥加密
# cipher = PKCS1_OAEP.new(public_key)
# encrypted_data = cipher.encrypt(data.encode())
#
# # 加载私钥
# private_key = ECC.import_key(private_key)
#
# # 使用私钥解密
# cipher = PKCS1_OAEP.new(private_key)
# decrypted_data = cipher.decrypt(encrypted_data)
# print(decrypted_data)

# # 加载私钥
# private_key = ECC.import_key('124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62')
#
# # 使用私钥解密
# cipher = PKCS1_OAEP.new(private_key)
# decrypted_data = cipher.decrypt('9c7167e0a39b1fb5a9b5be06833521398b594852e1a4274f7c2bfc15647a487d4cae422f1e5430302c7c80c73c0598ca09f0685227745de1a2a7337813808e9a1c0b1d6f410613f1f4be4bbed0440905b14387a797139b32bdc58c3c92ac979003edc3c65647e99abd6f95283fdb9c02032bacbc18c7fa9cd73ae6d537bc11440e4e0e548be86b74529d5bc193a9d2d698aaa5b5dd1df8ac454f206a65c1d1d24fe7')
# print(decrypted_data)

# list1 = ['平台管理系统', '应用管理', '权限管理', '安全管理', '标准注册', 'DRG分组管理', 'jh']
# list1.pop()
# list1.pop(0)
# print(list1)

# import chardet
#
# a = b"test"
# print(chardet.detect(a))  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
#
#
# def detect_file_encoding(file_path):
#     with open(file_path, 'rb') as file:
#         data = file.read()
#         result = chardet.detect(data)
#         return result
#
#
# result = detect_file_encoding("/Users/linghuchong/Downloads/51/Python/project/a.txt")
# print(result)  # {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}



