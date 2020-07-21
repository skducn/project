# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 字编码与解码对象层
# # 中文\unicode编码在线转换工具, http://www.bangnishouji.com/tools/chtounicode.html
# # 在线base64编码解码、base64加密解密 - aTool在线工具 http://www.atool.org/base64.php
# ***************************************************************
import sys

# Python 默认脚本文件都是 ANSCII 编码的
# unicode 是万国码，一种字码表。
# utf-8 是unicode的一种实现方式，unicode、gbk、gb2312是编码字符集
# utf-8 是这种unicode字码表储存的编码方法，其他还有utf-16,utf-32等。

'''Python中字符串类型分为 byte string 和 unicode string 两种。'''
# 在python中有两种字符串类型，分别是 str 和 unicode ，他们都是basestring的派生类；
# str类型是一个包含Characters represent (at least) 8-bit bytes的序列；unicode的每个unit是一个unicode obj;
# 所以：
print(len(u'中国'))  # 2
print(len('ab'))  # 2

class CodingPO():
    pass

if __name__ == '__main__':
    coding_PO = CodingPO()
