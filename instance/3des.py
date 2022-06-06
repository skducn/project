# coding: utf-8
# # *******************************************************************************************************************************
# Author     : John
# Date       : 2022/6/6
# Description: 3des.py
# pip install pyDes

# 如果参数是中文需设置编码
# data = "你好"
# data = data.encode('utf-8')

# 如果参数是json格式需转成标准的json格式
# import json
# data = {"role_name": "测试"}
# data = json.dumps(data)

# # *******************************************************************************************************************************

import pyDes

import base64

data = 'hello'

key = "kkk11111" # 加密key,加密方式ECB秘钥必须是八位字节

mode = pyDes.ECB # 加密方式 默认是ECB,也可以不填写

IV = "00000000" # 偏移量,加密方式不是ECB的时候加密key字段必须是16位字节,秘钥不够用0补充

k = pyDes.des(key, mode, IV=IV, pad=None, padmode=pyDes.PAD_PKCS5) # 传入秘钥,加密方式

d = k.encrypt(data) # 加密数据

base = str(base64.b64encode(d), encoding="utf-8") # 指定输出格式为base64

print(base)
