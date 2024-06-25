# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2022-12-15
# Description: sm2 对象层
# 来源：https://www.cnblogs.com/arbboter/p/16662305.html
# 使用 Python 脚本执行国密 sm2 加解密 https://www.cnblogs.com/wonz/p/14181844.html
# SM2是非对称加密算法
# 它是基于椭圆曲线密码的公钥密码算法标准，其秘钥长度256bit，包含数字签名、密钥交换和公钥加密，用于替换RSA/DH/ECDSA/ECDH等国际算法。可以满足
# 电子认证服务系统等应用需求，由国家密码管理局于2010年12月17号发布。
# SM2采用的是ECC 256位的一种，其安全强度比RSA 2048位高，且运算速度快于RSA。随着密码技术和计算技术的发展，目前常用的1024位RSA算法面临严重的
# 安全威胁，我们国家密码管理部门经过研究，决定采用SM2椭圆曲线算法替换RSA算法。SM2算法在安全性、性能上都具有优势。
# RSA算法的危机在于其存在亚指数算法，对ECC算法而言一般没有亚指数攻击算法 SM2椭圆曲线公钥密码算法：我国自主知识产权的商用密码算法，是ECC
# （Elliptic Curve Cryptosystem）算法的一种，基于椭圆曲线离散对数问题，计算复杂度是指数级，求解难度较大，同等安全程度要求下
# ，椭圆曲线密码较其他公钥算法所需密钥长度小很多。
# ***************************************************************

from gmssl import sm2 as SM2
from gmssl import func as GMFunc
from random import SystemRandom
from base64 import b64encode, b64decode


class CurveFp:
    def __init__(self, A, B, P, N, Gx, Gy, name):
        self.A = A
        self.B = B
        self.P = P
        self.N = N
        self.Gx = Gx
        self.Gy = Gy
        self.name = name

class SM2Key:
    sm2p256v1 = CurveFp(
        name="sm2p256v1",
        A=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC,
        B=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93,
        P=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF,
        N=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123,
        Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7,
        Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    )

    @staticmethod
    def multiply(a, n, N, A, P):
        return SM2Key.fromJacobian(SM2Key.jacobianMultiply(SM2Key.toJacobian(a), n, N, A, P), P)

    @staticmethod
    def add(a, b, A, P):
        return SM2Key.fromJacobian(SM2Key.jacobianAdd(SM2Key.toJacobian(a), SM2Key.toJacobian(b), A, P), P)

    @staticmethod
    def inv(a, n):
        if a == 0:
            return 0
        lm, hm = 1, 0
        low, high = a % n, n
        while low > 1:
            r = high // low
            nm, new = hm - lm * r, high - low * r
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    @staticmethod
    def toJacobian(Xp_Yp):
        Xp, Yp = Xp_Yp
        return Xp, Yp, 1

    @staticmethod
    def fromJacobian(Xp_Yp_Zp, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        z = SM2Key.inv(Zp, P)
        return (Xp * z ** 2) % P, (Yp * z ** 3) % P

    @staticmethod
    def jacobianDouble(Xp_Yp_Zp, A, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        if not Yp:
            return 0, 0, 0
        ysq = (Yp ** 2) % P
        S = (4 * Xp * ysq) % P
        M = (3 * Xp ** 2 + A * Zp ** 4) % P
        nx = (M ** 2 - 2 * S) % P
        ny = (M * (S - nx) - 8 * ysq ** 2) % P
        nz = (2 * Yp * Zp) % P
        return nx, ny, nz

    @staticmethod
    def jacobianAdd(Xp_Yp_Zp, Xq_Yq_Zq, A, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        Xq, Yq, Zq = Xq_Yq_Zq
        if not Yp:
            return Xq, Yq, Zq
        if not Yq:
            return Xp, Yp, Zp
        U1 = (Xp * Zq ** 2) % P
        U2 = (Xq * Zp ** 2) % P
        S1 = (Yp * Zq ** 3) % P
        S2 = (Yq * Zp ** 3) % P
        if U1 == U2:
            if S1 != S2:
                return 0, 0, 1
            return SM2Key.jacobianDouble((Xp, Yp, Zp), A, P)
        H = U2 - U1
        R = S2 - S1
        H2 = (H * H) % P
        H3 = (H * H2) % P
        U1H2 = (U1 * H2) % P
        nx = (R ** 2 - H3 - 2 * U1H2) % P
        ny = (R * (U1H2 - nx) - S1 * H3) % P
        nz = (H * Zp * Zq) % P
        return nx, ny, nz

    @staticmethod
    def jacobianMultiply(Xp_Yp_Zp, n, N, A, P):
        Xp, Yp, Zp = Xp_Yp_Zp
        if Yp == 0 or n == 0:
            return (0, 0, 1)
        if n == 1:
            return (Xp, Yp, Zp)
        if n < 0 or n >= N:
            return SM2Key.jacobianMultiply((Xp, Yp, Zp), n % N, N, A, P)
        if (n % 2) == 0:
            return SM2Key.jacobianDouble(SM2Key.jacobianMultiply((Xp, Yp, Zp), n // 2, N, A, P), A, P)
        if (n % 2) == 1:
            mv = SM2Key.jacobianMultiply((Xp, Yp, Zp), n // 2, N, A, P)
            return SM2Key.jacobianAdd(SM2Key.jacobianDouble(mv, A, P), (Xp, Yp, Zp), A, P)

class PrivateKey:
    def __init__(self, curve=SM2Key.sm2p256v1, secret=None):
        self.curve = curve
        self.secret = secret or SystemRandom().randrange(1, curve.N)

    def PublicKey(self):
        curve = self.curve
        xPublicKey, yPublicKey = SM2Key.multiply((curve.Gx, curve.Gy), self.secret, A=curve.A, P=curve.P, N=curve.N)
        return PublicKey(xPublicKey, yPublicKey, curve)

    def ToString(self):
        return "{}".format(str(hex(self.secret))[2:].zfill(64))

class PublicKey:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def ToString(self, compressed=True):
        return '04' + {
            True: str(hex(self.x))[2:],
            False: "{}{}".format(str(hex(self.x))[2:].zfill(64), str(hex(self.y))[2:].zfill(64))
        }.get(compressed)

class SM2Util:
    def __init__(self, pub_key=None, pri_key=None):
        self.pub_key = pub_key
        self.pri_key = pri_key
        self.sm2 = SM2.CryptSM2(public_key=self.pub_key, private_key=self.pri_key)

    def Encrypt(self, data):
        info = self.sm2.encrypt(data.encode())
        return b64encode(info).decode()

    def Decrypt(self, data):
        info = b64decode(data.encode())
        return self.sm2.decrypt(info).decode()

    def Sign(self, data):
        random_hex_str = GMFunc.random_hex(self.sm2.para_len)
        sign = self.sm2.sign(data.encode(), random_hex_str)
        return sign

    def Verify(self, data, sign):
        return self.sm2.verify(sign, data.encode())

    @staticmethod
    def GenKeyPair():
        d = {}
        pri = PrivateKey()
        pub = pri.PublicKey()
        d['private'] = pri.ToString()
        d['public'] = pub.ToString(compressed=False)
        return d
        # return pri.ToString(), pub.ToString(compressed=False)



if __name__ == '__main__':

    # from PO.Sm2PO import *

    # # todo 生成私钥和公钥
    d = SM2Util.GenKeyPair()
    print(d) # {'private': '1d3509589095e652dd3008acef9fb36657d2dfdd0777bf2ba4b85e83b2f7767e', 'public': '04c5e5bfe650a5fbdb6dfe40cba0fca92468be18783141cc444c387e32394aea6728504f720adb50afb82163d4642c5ce717f6863b0a63c6db291d563eff8e8f47'}
    # print(d['private'])
    # print(d['public'])

    # # todo 对数据签名与验证
    data = '123456'
    # sm2 = SM2Util(pri_key='124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62', pub_key='025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249')
    sm2 = SM2Util(pri_key=d['private'], pub_key=d['public'][2:])
    sign = sm2.Sign(data)
    print('签名:{} 验签:{}'.format(sign, sm2.Verify(data, sign)))  # 签名:e63652b2c2c3f983a06e5c7b6fe7d37f0fc42f058ce70ee3c6f6fdaf3c7b7534a05659bd2f7ab5d4c6a15a4d7512c92bcda48d2af607cedebb5190d863d20210 验签:True
    #
    #
    # # todo 加密与解密
    dataEncrypt = sm2.Encrypt(data)
    print('加密:{}'.format(dataEncrypt))  # 加密:jbm5KDRjoZSgJinaAxcsbOPakFKQ/oLiwn49LCpm7johHp9wSZud12GMqXdYGC35XA8cmOCZJ70FS7hpdAAcGWDen47AvH/htbqprHLhteR54OPWbeYSl80xgz/tBL3RwgAg6UJh
    #
    dataDecrypt = sm2.Decrypt(dataEncrypt)
    print('解密:{}'.format(dataDecrypt))  # 解密:123456

