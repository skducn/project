# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-1-13
# Description   : 字符 对象
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
