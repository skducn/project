#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @ProjectName: Demo
# @Name: gm_test.py.py
# @Auth: arbboter
# @Date: 2022/9/6-14:06
# @Desc:
# @Ver : 0.0.0.1
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
        #return b64encode(info).decode()
        return info.hex()

    def Decrypt(self, data):
        #info = b64decode(data.encode())
        #return self.sm2.decrypt(info).decode()
        return self.sm2.decrypt(bytes.fromhex(data)).decode()
        # return self.sm2.decrypt(bytes.fromhex(data)).decode(encoding='gb18030',errors='ignore')
        # return self.sm2.decrypt(bytes.fromhex(data)).decode(encoding='utf-8-sig',errors='ignore')
        # return self.sm2.decrypt(bytes.fromhex(data)).decode(encoding='unicode_escape')
        # return self.sm2.decrypt(bytes.fromhex(data)).decode(encoding='GB2312')

    def Sign(self, data):
        random_hex_str = GMFunc.random_hex(self.sm2.para_len)
        sign = self.sm2.sign(data.encode(), random_hex_str)
        return sign

    def Verify(self, data, sign):
        return self.sm2.verify(sign, data.encode())

    @staticmethod
    def GenKeyPair():
        pri = PrivateKey()
        pub = pri.PublicKey()
        return pri.ToString(), pub.ToString(compressed=False)


def main():
    """
    主函数
    :return:
    """
    # data = '{"password": "Qa@123456","username": "testwjw","img":"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","code":200,"captchaEnabled":true,"uuid":"a2fdf9b5d9af4e4593aad828a48313fb"}'
    data = '{"password": "Ww123456", "username": "lbl"}'
    # print('原数据:{}'.format(data))
    #
    # e = SM2Util.GenKeyPair()
    # # e = ('', '')
    # print('私钥:{}\n公钥:{}'.format(e[0], e[1]))
    # sm2 = SM2Util(pri_key=e[0], pub_key=e[1][2:])
    #
    # print(e[0])
    # print(e[1][2:])
    #
    # sign = sm2.Sign(data)
    # print('签名:{} 验签:{}'.format(sign, sm2.Verify(data, sign)))
    # # print('签名:{} 验签:{}'.format(sign, sm2.Verify("4fa9de3518e897f29468be4e4e3956e53bae3cbdb8a64310f41ecbdf76843eb4c81acf3721bf8113cf4d3563c698ab74e060989daab802154ea144938bfcdc228608df8ec3548140f9fe745b6fc11bdf0d1c679116d56648d55e362fd3334b0a5f2a0995918b49e3f273c96dc3fd9f1a0b719dccd5910039783c6315bbf2156432003e34d8dada6e81c58d42a674a455ccdfeb41323b379fe1c06ab36462", sign)))
    #
    # cipher = sm2.Encrypt(data)
    # print('加密:{}\n解密:{}'.format(cipher, sm2.Decrypt(cipher)))

    # publicKey:
    # privateKey:
    # sm2 = SM2Util(pri_key='124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62', pub_key='04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249')

    # thirdPublicKey: 0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b
    # thirdPrivateKey: 686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b
    # sm2 = SM2Util(pri_key='686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b', pub_key='0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b')
    # sm2 = SM2Util(pri_key='124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62', pub_key='04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249')
    # sign = sm2.Sign(data)
    # print('签名:{} 验签:{}'.format(sign, sm2.Verify(data, sign)))
    # cipher = sm2.Encrypt(data)
    # print(cipher)

    from base64 import b64encode, b64decode

    sm2_crypt = SM2.CryptSM2(private_key='124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62', public_key='04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249', mode=0)
    data = '{"password": "Ww123456", "username": "lbl"}'.encode('utf-8')
    enc_data = sm2_crypt.encrypt(data)
    print(type(enc_data))
    data = enc_data.hex()
    # data = b64encode(enc_data).decode()
    print('04' + data)
    print(type('04' + data))

    d = '04' + data
    # d = d.encode()
    # print(d)
    a = sm2_crypt.decrypt(d.encode('ascii'))

    chinese1 = a.decode('ascii', "strict")
    print(chinese1)

    print(a)
    # print(sm2.Decrypt('b0ef62c5e179f61dc11dc9154a644f8962970945c2f9c11727f4512cabbff13232aadd4f4aeb313914fe6b8aaadaf23e54773ca50e8d92ea706dad14385fd1dbacea5337aa4d401b333b19fd6599347419795150a5e17f7b5e3436283c3b211a8a15ce1ad86e2c2b78ef06695344'))

    # 469df631ab5f77c4cc5a552b6f7579309bb04dcad21aa126eb8ff2331804d6ab6fdf454228e0c8050ec182cff4b01e35bc6a4be88ed3fc0f52ee690c0b5a14b431fd89d698d2cc5e558f033f55135194271aa60a9af5d50b205e370d564b09bfdd8975cfc0bb8ba916c20b20ad1e33f4123c85a54e38ee2a9392c57784730369a0b41c2ff61975caf29b082fa5deefd6f2a37efef524ca0e786ebad2c6
if __name__ == '__main__':
    main()