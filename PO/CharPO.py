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

    # 判断字符串中是否包含中文
    def isContainChinese(self, varStr):
        for ch in varStr:
            if u'\u4e00' <= ch <= u'\u9fa5':
                return True
        return False

    # 判断字符串是否全部是中文
    def isChinese(self, varStr):
        for _char in varStr:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True


if __name__ == "__main__":

    Char_PO = CharPO()
    print(Char_PO.isContainChinese("123123123"))  # False   //字符串中没有中文
    print(Char_PO.isContainChinese("12312312jin金浩3"))  # True   //字符串中有中文
    print(Char_PO.isChinese("测试"))  # True //字符串全部是中文
    print(Char_PO.isChinese("测123试"))  # False //字符串有非中文字符

    name = "金浩"
    print(type(name))  # <class 'str'>
    byte1 = name.encode('utf-8')   # //将字符串编码成字节码 byte1。
    print(byte1)  # b'\xe9\x87\x91\xe6\xb5\xa9'
    # byte1 = name.decode('utf-8')  # AttributeError: 'str' object has no attribute 'decode' ，utf-8可以看成是unicode的一个扩展集，name本设就是unicode编码，所以无需再解码，python3开始已不支持decode属性。
    name2 = byte1.decode('utf-8')     # //将字节码解码成字符串 name2
    print(type(name2))  # <class 'str'>
    print(name2)  # 金浩

    # bytes.decode(encoding="utf-8", errors="strict")
    # encoding - - 要使用的编码，如"UTF-8"。
    # errors - - 设置不同错误的处理方案。默认为
    # 'strict', 意为编码错误引起一个UnicodeError。 其他可能得值有
    # 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace'
    # 以及通过codecs.register_error()注册的任何值。

    str = "菜鸟教程"
    str_utf8 = str.encode("UTF-8")
    str_gbk = str.encode("GBK")
    print("UTF-8 编码：", str_utf8)
    print("GBK 编码：", str_gbk)
    print("UTF-8 解码：", str_utf8.decode('UTF-8', 'strict'))
    print("GBK 解码：", str_gbk.decode('GBK', 'strict'))


