# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2022-6-10
# Description: bytes
# https://blog.csdn.net/amorhuang/article/details/82502773
# https://blog.csdn.net/weixin_39685130/article/details/111787739
# *******************************************************************
# todo 什么是Unicode？统一字符编码，从0-111411（0x10FFFF）空间，每个编码对应一个字符
# Unicode是一个字符集，他给每一个符号（包括汉字）都规定了二进制代码，但是没有规定应该如何存储。
# 他是字符的唯一的标识。
# Unicode是固定的用两个字节表示，当然现在也有四个字节的版本。比如“黄”字用Unicode表示为“9e c4”，这是两个16进制的字节。
# Python3里面的字符都是用Unicode表示，即 str 就是 unicode
# nicode字符串是一个代码点(code point)序列，代码点取值范围为0到0x10FFFF(对应的十进制为1114111)。这个代码点序列在存储(包括内存和物理磁盘)中需要被表示为一组字节(0到255之间的值)，而将Unicode字符串转换为字节序列的规则称为编码

# todo 字符与字节，字符编码？
# 比如字母A-Z都可以用ASCII码表示(占用一个字节)，也可以用UNICODE表示(占两个字节)，还可以用UTF-8表示(占用一个字节)。字符编码的作用就是将人类可识别的字符转换为机器可识别的字节码，以及反向过程。
# UNICDOE才是真正的字符串（str），而用ASCII、UTF-8、GBK等字符编码表示的是字节串（bytes）。
# 无论中文还是英文对字符串对应的字节串取长度，就跟编码(encode)过程使用的字符编码有关了(比如：UTF-8编码，一个中文字符需要用3个字节来表示；GBK编码，一个中文字符需要2个字节来表示)
# 注意：Windows的cmd终端字符编码默认为GBK，因此在cmd输入的中文字符需要用两个字节表示
# # python2中，
# a = 'Hello,中国'
# print(len(a))  # 10  6+2*2
# b = u'Hello,中国'
# print(len(b)) # 8   6+2=8



# todo 什么是字符集？

# todo 什么是UTF-8？它是一种编码
# UTF-8是Unicode的一种编码规则，是变长的。可以把一个Unicode字符编码为1到4个字节。
# 16进制的Unicode与2进制的UTF-8可互相转换。如：
# U+ 0000 ~ U+ 007F: 0XXXXXXX
# U+ 0080 ~ U+ 07FF: 110XXXXX 10XXXXXX
# U+ 0800 ~ U+ FFFF: 1110XXXX 10XXXXXX 10XXXXXX
# U+10000 ~ U+1FFFF: 11110XXX 10XXXXXX 10XXXXXX 10XXXXXX

# 字符串的十进制与十六进制
a = "学"
print(ord(a))  # 23398   //十进制的学
print(hex(ord(a)))  # 0x5b66  //16进制的学

# todo 字符串（str）通过一种编码（utf-8）转换成bytes
# 将"学"转换成bytes，需指定的编码类型，默认是utf-8，其他编码类型还有gb2312/gbk
print(bytes(a, "utf-8"))  # b'\xe5\xad\xa6'   \x代表这是一个16进制
print(bytes(a, "gb2312"))  # b'\xd1\xa7'
print(bytes(a, "gbk"))  # b'\xd1\xa7'

# todo bytes与str的区别？
# bytes包含的是由8位值所组成的序列，str包含的是由 Unicode码点所组成的序列。
# 用UTF-8给字符串编码,得到的就是这样的一系列8位值
# \x代表这是一个16进制，而一位十六进制代表了四位二进制，所以这里两位十六进制代表了8位二进制，也就是说这代表一个字节
a = b'h\x65llo'   # \x65等于e
print(str('\x65'))  # e
print(a)  # b'hello'  #
print(list(a))  # [104, 101, 108, 108, 111]
print(ord('h'))  # 104   字母h的十进制是104

# todo bytes是由8位值组成。在计算机里面str 等于 bytes，而bytes却不等于str,
#  因为计算机bytes可以表示更多的格式，音频、视频、字符串、文档等等。


# todo 将str编码成bytes用encode，将bytes对象解码成字符串用decode，默认utf-8编码。
demo_str = "你好"
print(demo_str.encode("utf-8")) # b'\xe4\xbd\xa0\xe5\xa5\xbd'
demo_bytes = b'\xe4\xbd\xa0\xe5\xa5\xbd'
print(demo_bytes.decode("utf-8"))  # 你好




