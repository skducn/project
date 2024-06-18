#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @ProjectName: Demo
# @Name: gm_test.py.py
# @Auth: arbboter
# @Date: 2022/9/6-14:06
# @Desc:
# @Ver : 0.0.0.1
from gmssl import sm2
# from gmssl import func as GMFunc
# from random import SystemRandom
# from base64 import b64encode, b64decode

# thirdPublicKey: 0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b
# thirdPrivateKey: 686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b
# publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
# privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62


from gmssl import sm2, func


from gmssl import sm2
from base64 import b64encode, b64decode
# sm2的公私钥
# SM2_PRIVATE_KEY = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
# SM2_PUBLIC_KEY = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

# thirdPublicKey: 0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b
# thirdPrivateKey: 686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b
# publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
# privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62

SM2_PRIVATE_KEY = '686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b'
SM2_PUBLIC_KEY = '0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b'

# SM2_PRIVATE_KEY = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
# SM2_PUBLIC_KEY = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'



sm2_crypt = sm2.CryptSM2(public_key=SM2_PUBLIC_KEY, private_key=SM2_PRIVATE_KEY)


class sm2Encrypt:
    # 加密
    def encrypt(self, info):
        encode_info = sm2_crypt.encrypt(info.encode(encoding="utf-8"))
        print(type(encode_info), encode_info)
        encode_info= encode_info.hex()
        print(type(encode_info), encode_info)

        # encode_info = b64encode(encode_info).decode()  # 将二进制bytes通过base64编码
        return encode_info

    # 解密
    def decrypt(self, info):
        # decode_info = b64decode(info.encode())  # 通过base64解码成二进制bytes
        decode_info = sm2_crypt.decrypt(info).decode(encoding="utf-8")
        return decode_info


if __name__ == "__main__":
    origin_pwd = '{"password": "Ww123456", "username": "lbl"}'
    # origin_pwd = "{'password': 'Ww123456', 'username': 'lbl'}"
    sm2 = sm2Encrypt()
    # 加密的密码
    encrypy_pwd = sm2.encrypt(origin_pwd)
    print(encrypy_pwd)
    # 解密的密码
    decrypt_pwd = sm2.decrypt(encrypy_pwd)
    print(decrypt_pwd)