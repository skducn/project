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

'''
1，中文字符串转字节码
2，字节码转中文字符串
3，判断元素是不是数字类型（不支持中文大写数字及英文字母）
4, Numbers类型小数点后补0或去掉0（规则)
5，列表中浮点数或字符串，小数点后0优化方法
6，单个浮点数或字符串，小数点后0优化方法

7.1 中文转拼音（不带声调）
7.2 中文转拼音（带声调,支持多音字）
7.3, 中文转拼音(声调，分隔符，大小写)

'''

import sys, pypinyin
from xpinyin import Pinyin

class CharPO():

    def __init__(self):
        pass

    # 1，中文字符串转字节码
    def str2byte(self, varStr, varCoding="utf-8"):
        # str 转 byte
        # utf-8 可以看成是unicode的一个扩展集，varStr就是unicode编码，所以无需再解码，python3开始已不支持decode属性。
        # 如：byte1 = varStr.decode('utf-8')     # AttributeError: 'str' object has no attribute 'decode'
        try:
            byte1 = varStr.encode(varCoding)
            return byte1
        except:
            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 2，字节码转中文字符串
    def byte2str(self, varByte, varCoding="utf-8"):
        # byte 转 str
        # bytes.decode(encoding="utf-8", errors="strict")
        # encoding - - 要使用的编码，如"UTF-8"。
        # errors - - 设置不同错误的处理方案，默认为 strict 表示编码错误引起一个UnicodeError，其他还有：'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace'
        # 以及通过codecs.register_error()注册的任何值。
        try:
            str1 = varByte.decode(varCoding, 'strict')
            return str1
        except:
            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 3，判断元素是不是数字类型（不支持中文大写数字及英文字母）
    def isNumbersType(self, varValue):
        # 支持数字类型有：int、float、bool、complex、字符串、long类型（python2中有long类型， python3中没有long类型）
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

    # 4，Numbers类型小数点后补0或去掉0（规则)
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
                            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")
                        elif varPatchNum == 0 :
                            return varNum
                        else:
                            varStr = str(varNum) + "." + "0" * varPatchNum  # 整数小数位补1个0
                    else:
                        print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")
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
                        print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

                return varStr
            else:
                print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")
        except:
            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 5，列表中浮点数或字符串，小数点后0优化方法
    def zeroByDotSmart(self, varList, varPatchNum=2):
        # 将列表中所有元素的格式变成.00，如： [11, 22.0, 33.00] => [11.00, 22.0, 33.00]
        # 非规则，支持 数字或字符串，0.00，0.0等
        list4 = []
        list3 = []
        try:
            for i in varList:
               if self.isNumbersType(i) == True:
                   if isinstance(i, str):
                       if "." in i:
                           list3.append(float(i))
                       else:
                           list3.append(int(i))
                   else:
                       list3.append(i)

            if varPatchNum == 0:
                for i in list3:
                    list4.append('{:g}'.format(i))
                return list4
            elif varPatchNum < 0:
                print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

            for i in list3:
                list4.append('{:g}'.format(i))

            for i in range(len(list4)):
                if "." not in list4[i]:  # //整数，在数位后补N个0
                    if list4[i] != "0":
                        list4[i] = list4[i] + "." + "0" * varPatchNum
                    else:
                        list4[i] = "0"
                else:
                    list4[i] = list4[i] + "0" * (varPatchNum - len(list4[i].split(".")[1]))
            return (list4)
        except:
            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 6，单个浮点数或字符串，小数点后0优化方法
    def zeroByDotSmartStr(self, varValue):
        try:
            return ('{:g}'.format(float(varValue)))
        except:
            print("[ERROR], " + sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 7.1 中文转拼音（不带声调）
    def chinese2pinyin(self, varWord, varMode=False):
        # print(Char_PO.chinese2pinyin("金浩"))  # jinhao
        s = ''
        for i in pypinyin.pinyin(varWord, style=pypinyin.NORMAL, heteronym=varMode):
            s += ''.join(i)
        return s

    # 7.2 中文转拼音（带声调）
    def chinese2pinyinTone(self, varWord, varMode=False):
        # 开启多音字 ：heteronym = True
        # print(Char_PO.chinese2pinyinTone("金浩"))  # jīn hào
        s = ''
        for i in pypinyin.pinyin(varWord, heteronym=varMode):
            s = s + ''.join(i) + " "
        return s


    # 7.3, 中文转拼音(声调，分隔符，大小写)
    def chinese2pinyin1(self, varWord, splitter="", convert='lower', tone_marks=""):
        p = Pinyin()
        # get_pinyin(self, chars=u'你好', splitter=u'-',tone_marks=None, convert='lower'):
        # print(Char_PO.chinese2pinyin1("你好"))  # nihao
        # print(Char_PO.chinese2pinyin1("你好", splitter="-"))  # ni-hao
        # print(Char_PO.chinese2pinyin1("你好", tone_marks="marks"))  # nǐhǎo
        # print(Char_PO.chinese2pinyin1("你好", tone_marks="marks", convert="upper"))  # NǏHǍO
        # print(Char_PO.chinese2pinyin1("你好", tone_marks="numbers", splitter="-"))  # ni3-hao3
        return p.get_pinyin(varWord, splitter=splitter,tone_marks=tone_marks, convert=convert)

if __name__ == "__main__":

    Char_PO = CharPO()

    print("1，中文字符串转字节码".center(100, "-"))
    print(Char_PO.str2byte("金浩", "utf-8"))  # b'\xe9\x87\x91\xe6\xb5\xa9'
    print(Char_PO.str2byte("金浩", "GBK"))  # b'\xbd\xf0\xba\xc6'

    print("2，字节码转中文字符串".center(100, "-"))
    print(Char_PO.byte2str(b'\xe9\x87\x91\xe6\xb5\xa9', "utf-8"))  # 金浩
    print(Char_PO.byte2str(b'\xbd\xf0\xba\xc6', "gbk"))  # 金浩

    print("3，判断元素是不是数字类型（不支持中文大写数字及英文字母）".center(100, "-"))
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

    print("4，Numbers类型小数点后补0或去掉0".center(100, "-"))
    print(Char_PO.zeroByDot(123.56, 2))  # 123.5600
    print(Char_PO.zeroByDot("11.00000", -4))  # 11.0    //去掉小数后4位
    print(Char_PO.zeroByDot("22.00000", -5))  # 22      //去掉小数后5位（自动去掉.）,也就是返回整数
    print(Char_PO.zeroByDot("33.00000", -7))  # 33      //去掉小数后7位，但实际只有5为，因为返回整数。
    print(Char_PO.zeroByDot(44.0, 1))  # 44.00   //在小数点后再添加1个0
    print(Char_PO.zeroByDot(55.0, 3))  # 55.0000  //在小数点后再添加3个0
    print(Char_PO.zeroByDot("66.000", 3))  # 66.000000
    print(Char_PO.zeroByDot(77, -4))  # None ， 整数去掉小数后4个0，逻辑不通返回None  ??
    print(Char_PO.zeroByDot(88, 0))  # 88
    print(Char_PO.zeroByDot(99, 1))  # 99.0
    print(Char_PO.zeroByDot(12, 6))  # 120.000000
    print(Char_PO.zeroByDot('13', -4))  # None ???
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


    print("5，浮点数尾部无效0去掉和无效的‘.’号（非规则）".center(100, "-"))
    list1 = [0, 1.0, 2.00, 3.000, 4.4400, 5.5000, 6.0006, 0.0007, 0.00008, 8.123456789, 9.90]
    # print(Char_PO.zeroByDotSmart([12.12300, 12.00, 200.12000, 200.0, 88.0009, 5.000, 0.001], ""))  # None
    print(Char_PO.zeroByDotSmart(list1, 0))  # ['0', '1', '2', '3', '4.44', '5.5', '6.0006', '0.0007', '8e-05', '8.12346', '9.9']
    print(Char_PO.zeroByDotSmart(list1, 1))  # ['0', '1.0', '2.0', '3.0', '4.44', '5.5', '6.0006', '0.0007', '8e-05.0', '8.12346', '9.9']
    print(Char_PO.zeroByDotSmart(list1, 2))  # ['0', '1.00', '2.00', '3.00', '4.44', '5.50', '6.0006', '0.0007', '8e-05.00', '8.12346', '9.90']
    print(Char_PO.zeroByDotSmart(list1))  # ['0', '1.00', '2.00', '3.00', '4.44', '5.50', '6.0006', '0.0007', '8e-05.00', '8.12346', '9.90']
    print(Char_PO.zeroByDotSmart(list1, 4))  # ['0', '1.0000', '2.0000', '3.0000', '4.4400', '5.5000', '6.0006', '0.0007', '8e-05.0000', '8.12346', '9.9000']

    list2 = [1.0, 2.0, 3.0, 4.0, 5.0]
    print(Char_PO.zeroByDotSmart(list2))  # ['1.00', '2.00', '3.00', '4.00', '5.00']

    list3 = [11.00, 22.00, 3.00, '4.0', '5.00000','6.60']
    print(Char_PO.zeroByDotSmart(list3))  # ['11.00', '22.00', '3.00', '4.00', '5.00', '6.00']
    print(Char_PO.zeroByDotSmart(list3, 0))  # ['11', '22', '3', '4', '5', '6.6']
    print(Char_PO.zeroByDotSmart(list3, 1))  # ['11.0', '22.0', '3.0', '4.0', '5.0', '6.0']

    print("6，单个浮点数或字符串，小数点后0优化方法".center(100, "-"))
    print(Char_PO.zeroByDotSmartStr("1.00"))
    print(Char_PO.zeroByDotSmartStr("1.10"))
    print(Char_PO.zeroByDotSmartStr("1"))
    print(Char_PO.zeroByDotSmartStr("0"))
    print(Char_PO.zeroByDotSmartStr("0.00"))
    print(Char_PO.zeroByDotSmartStr("27457.67"))
    print(Char_PO.zeroByDotSmartStr("3457.67"))

    print(Char_PO.zeroByDotSmartStr(1.00))
    print(Char_PO.zeroByDotSmartStr(1.10))
    print(Char_PO.zeroByDotSmartStr(1))
    print(Char_PO.zeroByDotSmartStr(0))
    print(Char_PO.zeroByDotSmartStr(0.00))

    tmpdict1 = {"abc":"100.00", "ddd":"7.08", "ccc":"5.80"}
    for k, v in tmpdict1.items():
        tmpdict1[k] = str(Char_PO.zeroByDotSmartStr(v))
    print(tmpdict1)

    tmpdict2 = {}
    tuple1 = (('门诊药房(新院)', 1565.00), ('发热门诊药房', 11.10), ('外科', '1545.00'))
    for k, v in tuple1:
        tmpdict2[k] = str(Char_PO.zeroByDotSmartStr(v))
    print(tmpdict2)


    print("7 中文转拼音".center(100, "-"))
    print(Char_PO.chinese2pinyin("曾祥云", True))  # jinhao
    print(Char_PO.chinese2pinyin("金浩", True))  # jinhao
    print(Char_PO.chinese2pinyinTone("金浩"))  # jīn hào
    print(Char_PO.chinese2pinyinTone("金浩", True))  # jīnjìn hàogǎogé

    print(Char_PO.chinese2pinyin1("jin你好"))  # nihao
    print(Char_PO.chinese2pinyin1("你好", splitter="-"))  # ni-hao
    print(Char_PO.chinese2pinyin1("你好",tone_marks="marks"))  # nǐhǎo
    print(Char_PO.chinese2pinyin1("你好",tone_marks="marks",convert="upper"))  # NǏHǍO
    print(Char_PO.chinese2pinyin1("你好",tone_marks="numbers", splitter="-"))  # ni3-hao3