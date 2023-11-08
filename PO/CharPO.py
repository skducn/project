# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-1-13
# Description   : 字符 对象

# todo: 关于 python3 编码过程中转码问题
# 1，python 3中所有字符串都是 unicode 对象，也就是默认编码为 unicode，由str类型进行表示。
# 2，二进制数据使用byte类型表示
# 3，字符串通过编码转换为字节码，str--->(encode)--->bytes ，如：str.encode("utf-8")
# 4，字节码通过解码转换为字符串，bytes--->(decode)--->str ，如：bytes.decode(encoding="utf-8", errors="strict")

# 过滤掉非法的多字节序列问题
# b = "型➕换季收纳法🔥叠衣"
# print(b.encode('gbk', 'ignore').decode('gbk') )   # 型换季收纳法叠衣
# *********************************************************************

"""
1.1 中文转字节码
1.2 字节码转中文
1.3 中文转拼音（不带声调）
1.4 中文转拼音（带声调,支持多音字）
1.5 中文转拼音(声调，分隔符，大小写)
"""

import sys, pypinyin
from xpinyin import Pinyin

# p = Pinyin()
# hanzi = "北京欢迎你"
# pinyin_list = p.get_initials(hanzi, '')
# print(pinyin_list)



class CharPO:
    def __init__(self):
        pass

        # 2 判断字符串是否为数字

    # 1.1 中文转字节码
    def chinese2byte(self, varChinese, varCoding="utf-8"):
        # 默认unicode编码是utf-8
        # 注意：utf-8 可以看成是unicode的一个扩展集，varChinese就是unicode编码，所以无需再解码，python3开始已不支持decode属性。如：byte1 = varStr.decode('utf-8')     # AttributeError: 'str' object has no attribute 'decode'
        # print(Char_PO.chinese2byte("金浩", "utf-8"))  # b'\xe9\x87\x91\xe6\xb5\xa9'
        # print(Char_PO.chinese2byte("金浩", "GBK"))  # b'\xbd\xf0\xba\xc6'
        try:
            byte1 = varChinese.encode(varCoding)
            return byte1
        except:
            print(
                "[ERROR], "
                + sys._getframe(1).f_code.co_name
                + ", line "
                + str(sys._getframe(1).f_lineno)
                + ", in "
                + sys._getframe(0).f_code.co_name
                + ", SourceFile '"
                + sys._getframe().f_code.co_filename
                + "'"
            )

    # 1.2 字节码转中文
    def byte2chinese(self, varByte, varCoding="utf-8"):
        # bytes.decode(encoding="utf-8", errors="strict")
        # encoding - - 要使用的编码，如"UTF-8"。
        # errors - - 设置不同错误的处理方案，默认为 strict 表示编码错误引起一个UnicodeError，其他还有：'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace'
        # 以及通过codecs.register_error()注册的任何值。

        chinese1 = varByte.decode(varCoding, "strict")
        return chinese1


        # 7.1 中文转拼音（不带声调）

    # 1.3 中文转拼音
    def chinese2pinyin(self, varChinese, varMode=False):
        # 开启多音字 ：heteronym = True
        # print(Char_PO.chinese2pinyin("曾祥云", True))  # cengzengxiangyun
        # print(Char_PO.chinese2pinyin("金浩", True))  # jinhaogaoge
        # print(Char_PO.chinese2pinyin("金浩"))  # jinhao
        pinyin = ""
        for i in pypinyin.pinyin(varChinese, style=pypinyin.NORMAL, heteronym=varMode):
            pinyin += "".join(i)
        return pinyin

    # 1.4 中文转拼音（带声调）
    def chinese2pinyinTone(self, varWord, varMode=False):
        # 开启多音字 ：heteronym = True
        # print(Char_PO.chinese2pinyinTone("金浩"))  # jīn hào
        # print(Char_PO.chinese2pinyinTone("金浩", True))  # jīnjìn hàogǎogé
        pinyinTone = ""
        for i in pypinyin.pinyin(varWord, heteronym=varMode):
            pinyinTone = pinyinTone + "".join(i) + " "
        return pinyinTone

    # 1.5 中文转拼音（声调，分隔符，大小写）
    def chinese2pinyin3(self, varChinese, splitter="", convert="lower", tone_marks=""):
        # 默认输出小写
        # get_pinyin(self, chars=u'你好', splitter=u'-',tone_marks=None, convert='lower'):
        # print(Char_PO.chinese2pinyin1("你好", splitter="-"))  # ni-hao
        # print(Char_PO.chinese2pinyin1("你好", tone_marks="marks"))  # nǐhǎo
        # print(Char_PO.chinese2pinyin1("你好", tone_marks="marks", convert="upper"))  # NǏHǍO
        # print(Char_PO.chinese2pinyin1("你好", tone_marks="numbers", splitter="-"))  # ni3-hao3
        p = Pinyin()
        return p.get_pinyin(
            varChinese, splitter=splitter, tone_marks=tone_marks, convert=convert
        )


if __name__ == "__main__":

    Char_PO = CharPO()

    # print("1.1 中文转字节码".center(100, "-"))
    # print(Char_PO.chinese2byte("金浩", "utf-8"))  # b'\xe9\x87\x91\xe6\xb5\xa9'
    # print(Char_PO.chinese2byte("金浩", "GBK"))  # b'\xbd\xf0\xba\xc6'
    #
    # print("1.2 字节码转中文字符串".center(100, "-"))
    # print(Char_PO.byte2chinese(b"\xe9\x87\x91\xe6\xb5\xa9", "utf-8"))  # 金浩
    # print(Char_PO.byte2chinese(b"\xbd\xf0\xba\xc6", "gbk"))  # 金浩
    #
    # print("1.3 中文转拼音".center(100, "-"))
    # print(Char_PO.chinese2pinyin("上海市"))  # cengzengxiangyun
    # print(Char_PO.chinese2pinyin("金浩", True))  # jinhaogaoge
    #
    # print("1.4 中文转拼音（带声调）".center(100, "-"))
    # print(Char_PO.chinese2pinyinTone("金浩"))  # jīn hào
    # print(Char_PO.chinese2pinyinTone("金浩", True))  # jīnjìn hàogǎogé
    #
    # print("1.5 中文转拼音（声调，分隔符，大小写）".center(100, "-"))
    # print(Char_PO.chinese2pinyin3("你好", splitter="-"))  # ni-hao
    # print(Char_PO.chinese2pinyin3("你好", tone_marks="marks"))  # nǐhǎo
    # # print(Char_PO.chinese2pinyin3("你好", tone_marks="marks", convert="upper"))  # NǏHǍO
    # print(Char_PO.chinese2pinyin3("你好", tone_marks="numbers", splitter="-"))  # ni3-hao3

