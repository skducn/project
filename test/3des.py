# coding: utf-8
# # *******************************************************************************************************************************
# Author     : John
# Date       : 2018/4/20 14:47
# Description: 3des.py
# pip3 install pycryptodome
# 快速方式：pip3 install -i https://pypi.douban.com/simple pycryptodome
# PyCrypto 已死,请替换为 PyCryptodome
# pip3 install 模块 –upgrade –target=”指定的目录”
# # *******************************************************************************************************************************
import base64
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# 定义的 3des 24位 密钥 key ， 及RSA公钥 pub_key_str
key = 'xUHdKxzVCbsgVIwTnc1jtpWn'
pub_key_str = """-----BEGIN RSA PUBLIC KEY-----
       MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHp2h4iGAgtAOWvfIzJgSKDTfbDThNW4DeEh15ENrb3ilrI/bnXYeXtEyTodGtU6sQWQpC6/uhI9gdAfuWHr6cYYtoUvPi7QdT/ZRzo1CerkFv/ZbqEZDleoGi7nt8IZrxDV5SEFMnWtTFdup4npWAwxF4sfqZwUaTD3/RkSwQMwIDAQAB
       -----END RSA PUBLIC KEY-----"""

# *params = '{"userName":"187","passWord":"123"}'

# 3DES 16位加密
def init_str(s):
    l = len(s) % 16
    if l != 0:
        c = 16 - l
        s += chr(c) * c
    return s

# RSA 加密生成 varRSA
def rsa_long_encrypt(pub_key_str, msg, length=100):
    pubobj = rsa.importKey(pub_key_str)
    pubobj = PKCS1_v1_5.new(pubobj)
    res = []
    for i in range(0, len(msg), length):
        res.append(pubobj.encrypt(msg[i:i + length]))
    return "".join(res)
enres = rsa_long_encrypt(pub_key_str, key, 200)  # 生成RSA
varRSA = base64.b64encode(enres)  # 将RSA再通过base64加密


# 3DES ， 对3DES进行base64处理
varParam = {"passWord":"e10adc3949ba59abbe56e057f20f883e","phoneNumber":"13816109059"}
ss = init_str(varParam)
des3 = DES3.new(key, DES3.MODE_ECB)
res2 = des3.encrypt(ss)
var3EDS = base64.b64encode(res2)

# 将 RSA 与 3DES 混合
data = varRSA + "|" + var3EDS

# 对3DES进行解码
des3 = DES3.new(key, DES3.MODE_ECB)
orgResponse = des3.decrypt(base64.b64decode(data))   # 先base64解码，再3DES解码。  解码后原始data