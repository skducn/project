# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-1-13
# Description   : 字符 对象
# 关于python3 编码过程中转码问题
# 1，从Python 3开始，所有字符串都是unicode对象，也就是 python3 默认编码为unicode，由str类型进行表示。
# 2，二进制数据使用byte类型表示
# 3，字符串通过编码转换为字节码，str--->(encode)--->bytes ，如：str.encode("utf-8")
# 4，字节码通过解码转换为字符串，bytes--->(decode)--->str ，如：bytes.decode(encoding="utf-8", errors="strict")

# *********************************************************************

class CharPO():

    def __init__(self):
        pass

    # 1，字符串转字节码
    def str2byte(self, varStr, varCoding="utf-8"):
        # 字符串str 编码成 字节码byte
        try:
            byte1 = varStr.encode(varCoding)
            return byte1
        except:
            return None

        # 要点：
        # byte1 = name.decode('utf-8')  # AttributeError: 'str' object has no attribute 'decode'
        # utf-8 可以看成是unicode的一个扩展集，varStr本设就是unicode编码，所以无需再解码，python3开始已不支持decode属性。

    # 2，字节码转字符串
    def byte2str(self, varByte, varCoding="utf-8"):
        # 字节码byte 解码成 字符串str
        try:
            str1 = varByte.decode(varCoding, 'strict')
            return str1
        except:
            return None

        # 说明
        # bytes.decode(encoding="utf-8", errors="strict")
        # encoding - - 要使用的编码，如"UTF-8"。
        # errors - - 设置不同错误的处理方案。默认为
        # 'strict', 意为编码错误引起一个UnicodeError。 其他可能得值有
        # 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace'
        # 以及通过codecs.register_error()注册的任何值。

    # 3，判断元素是不是数字（不支持中文数字）
    def isNumbersType(self, varValue):
        # 支持python Numbers数字类型（int,float,book,complex）以及字符串
        # 注意：支持long类型，python2中有long类型， python3中已没有long类型
        # print(Char_PO.isNumbersType(123))  # True
        # print(Char_PO.isNumbersType(complex(1, 2)))  # True
        # print(Char_PO.isNumbersType(complex("1")))  # True
        # print(Char_PO.isNumbersType(complex("1+2j")))  # True
        # print(Char_PO.isNumbersType((1)))  # True
        # print(Char_PO.isNumbersType(True))  # True
        # print(Char_PO.isNumbersType(False))  # True
        # print(Char_PO.isNumbersType(-123))  # True
        # print(Char_PO.isNumbersType(123456768567868756756757575675657567567567.77434))  # True
        # print(Char_PO.isNumbersType(0.23456))  # True
        # print(Char_PO.isNumbersType(000000.23456))  # True
        # print(Char_PO.isNumbersType("100"))  # True
        # print(Char_PO.isNumbersType("1234.56768567868"))  # True
        # print(Char_PO.isNumbersType("二"))  # False
        # print(Char_PO.isNumbersType("123Abc"))  # False
        try:
            complex(varValue)
        except ValueError:
            return False
        return True

    # 4，补 / 去掉0
    def zeroByDot(self, varNum, varPatchNum):
        # 功能：补/去掉0，支持Numbers类型（int，float，bool，complex）及str字符型
        # 判断varNum是否是数字，并判断小数点后是补0还是去掉0
        # print(Char_PO.zeroByDot(123.56, 2))  # 123.5600
        # print(Char_PO.zeroByDot("11.00000", -4))  # 11.0    //去掉小数后4位
        # print(Char_PO.zeroByDot("22.00000", -5))  # 22      //去掉小数后5位（自动去掉.）,也就是返回整数
        # print(Char_PO.zeroByDot("33.00000", -7))  # 33      //去掉小数后7位，但实际只有5为，因为返回整数。
        # print(Char_PO.zeroByDot(44.0, 1))  # 44.00   //在小数点后再添加1个0
        # print(Char_PO.zeroByDot(55.0, 3))  # 55.0000  //在小数点后再添加3个0
        # print(Char_PO.zeroByDot("66.000", 3))  # 66.000000
        # print(Char_PO.zeroByDot(77, -4))  # None ， 整数去掉小数后4个0，逻辑不通返回None
        # print(Char_PO.zeroByDot(88, 0))  # 88
        # print(Char_PO.zeroByDot(99, 1))  # 99.0
        # print(Char_PO.zeroByDot(12, 6))  # 120.000000
        # print(Char_PO.zeroByDot('13', -4))  # None
        # print(Char_PO.zeroByDot('14', 0))  # 14
        # print(Char_PO.zeroByDot('15', 1))  # 15.0
        # print(Char_PO.zeroByDot('16', 6))  # 16.000000
        # print(Char_PO.zeroByDot(True, 6))  # 1.000000  //True = 1
        # print(Char_PO.zeroByDot(False, 6))  # 0.000000 //False = 0
        # print(Char_PO.zeroByDot(-17, 3))  # -17.000
        # print(Char_PO.zeroByDot(-178, -3))  # None
        # print(Char_PO.zeroByDot((18), 6))  # 18.000000
        # print(Char_PO.zeroByDot(complex(1, 19), 3))  # (1+19j).000
        varStr = ""
        try:
            if self.isNumbersType(varNum) == True:
                if varNum == True:
                    varNum = 1
                if varNum == False:
                    varNum = 0

                if "." not in str(varNum):
                    if isinstance(varPatchNum, int):
                        if varPatchNum < 0 :
                            return None
                        elif varPatchNum == 0 :
                            return varNum
                        else:
                            varStr = str(varNum) + "." + "0" * varPatchNum  # 整数小数位补1个0
                    else:
                        return None
                else:
                    if isinstance(varPatchNum, int):
                        if varPatchNum < 0 :
                            dotLen = str(varNum).split(".")[1]
                            if len(dotLen) <= int(-varPatchNum):
                                return varNum[0:-(len(dotLen)+1)]
                            else:
                                return varNum[0:varPatchNum]
                        else:
                            dotLen = str(varNum).split(".")[1]  # 小数点后一个0
                            if len(dotLen) > 0:
                                varStr = str(varNum) + "0" * varPatchNum  # 整数小数位补1个0
                    else:
                        return None

                return varStr
            else:
                return None
        except:
            return None



if __name__ == "__main__":

    Char_PO = CharPO()

    print("1，字符串转字节码".center(100, "-"))
    print(Char_PO.str2byte("金浩", "utf-8"))  # b'\xe9\x87\x91\xe6\xb5\xa9'
    print(Char_PO.str2byte("金浩", "GBK"))  # b'\xbd\xf0\xba\xc6'
    print(Char_PO.str2byte(123, "GBK"))  # None

    print("2，字节码转字符串".center(100, "-"))
    print(Char_PO.byte2str(b'\xe9\x87\x91\xe6\xb5\xa9', "utf-8"))  # 金浩
    print(Char_PO.byte2str(b'\xbd\xf0\xba\xc6', "gbk"))  # 金浩
    print(Char_PO.byte2str("123123123", "gbk"))  # None



    print("3，判断元素是不是数字（不支持中文数字）".center(100, "-"))
    print(Char_PO.isNumbersType(123))  # True
    print(Char_PO.isNumbersType(complex(1, 2)))  # True
    print(Char_PO.isNumbersType(complex("1")))  # True
    print(Char_PO.isNumbersType(complex("1+2j")))  # True
    print(Char_PO.isNumbersType((1)))  # True
    print(Char_PO.isNumbersType(True))  # True
    print(Char_PO.isNumbersType(False))  # True
    print(Char_PO.isNumbersType(-123))  # True
    print(Char_PO.isNumbersType(123456768567868756756757575675657567567567.77434))  # True
    print(Char_PO.isNumbersType(0.23456))  # True
    print(Char_PO.isNumbersType(000000.23456))  # True
    print(Char_PO.isNumbersType("100"))  # True
    print(Char_PO.isNumbersType("1234.56768567868"))  # True
    print(Char_PO.isNumbersType("二"))  # False
    print(Char_PO.isNumbersType("123Abc"))  # False


    print("4，补 / 去掉0".center(100, "-"))
    print(Char_PO.zeroByDot(123.56, 2))  # 123.5600
    print(Char_PO.zeroByDot("11.00000", -4))  # 11.0    //去掉小数后4位
    print(Char_PO.zeroByDot("22.00000", -5))  # 22      //去掉小数后5位（自动去掉.）,也就是返回整数
    print(Char_PO.zeroByDot("33.00000", -7))  # 33      //去掉小数后7位，但实际只有5为，因为返回整数。
    print(Char_PO.zeroByDot(44.0, 1))  # 44.00   //在小数点后再添加1个0
    print(Char_PO.zeroByDot(55.0, 3))  # 55.0000  //在小数点后再添加3个0
    print(Char_PO.zeroByDot("66.000", 3))  # 66.000000
    print(Char_PO.zeroByDot(77, -4))  # None ， 整数去掉小数后4个0，逻辑不通返回None
    print(Char_PO.zeroByDot(88, 0))  # 88
    print(Char_PO.zeroByDot(99, 1))  # 99.0
    print(Char_PO.zeroByDot(12, 6))  # 120.000000
    print(Char_PO.zeroByDot('13', -4))  # None
    print(Char_PO.zeroByDot('14', 0))  # 14
    print(Char_PO.zeroByDot('15', 1))  # 15.0
    print(Char_PO.zeroByDot('16', 6))  # 16.000000
    print(Char_PO.zeroByDot(True, 6))  # 1.000000  //True = 1
    print(Char_PO.zeroByDot(False, 6))  # 0.000000 //False = 0
    print(Char_PO.zeroByDot(-17, 3))  # -17.000
    print(Char_PO.zeroByDot(-178, -3))  # None
    print(Char_PO.zeroByDot((18), 6))  # 18.000000
    print(Char_PO.zeroByDot(complex(1, 19), 3))  # (1+19j).000
    print(Char_PO.zeroByDot("abc", 2))  # None   //不支持字符串
    print(Char_PO.zeroByDot([1, 2, 3], 2))  # None   //不支持列表






