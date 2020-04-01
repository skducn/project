# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2019-9-24
# Description: python 处理BOM文本的解决方案
# 项目中遇到要读取配置的情况, 所有就用了 ConfigParser 模块, 乍一看没有啥问题, 但是测试过程中发现还是有坑.
# 在windows上使用open打开utf-8编码的txt文件时开头会有一个多余的字符\ufeff，它叫BOM,是用来声明编码等信息的,但python会把它当作文本解析。
# 然后ConfigParser在read时候就会抛错, 尝试了一些方法, 最终用指定read的编码方式的方法解决。
# 对UTF-16, Python将BOM解码为空字串。然而对UTF-8, BOM被解码为一个字符\ufeff。
# 如何去掉bom字符？
# 解决修改encoding为utf-8_sig或者utf_8_sig
# open('1.txt', encoding='utf_8_sig' )
# 参考：https://stackoverflow.com/questions/8898294/convert-utf-8-with-bom-to-utf-8-with-no-bom-in-python
# *****************************************************************

# 方法1：使用 encoding="utf-8-sig"
import configparser
# configparser.ConfigParser().read("code.txt", encoding="utf-8-sig")

# # 方法2：使用 read 编码方式
# fp = open("code.txt")
# s = fp.read()
# u = s.decode("utf-8-sig")
# # That gives you a unicode string without the BOM. You can then use
# s = u.encode("utf-8")


import sys, codecs


def detectUTF8(file_name):
    state = 0
    line_num = 0

    file_obj = open(file_name,'rb')
    all_lines = file_obj.readlines()
    file_obj.close()
    for line in all_lines:
        line_num += 1
        line_len = len(line)
        for index in range(line_len):
            if state == 0:
                if (ord(line[index]) & 0x80) == 0x00:  # 上表中的第一种情况
                    state = 0
                    print(state)
                elif ord(line[index]) & 0xE0 == 0xC0:  # 上表中的第二种情况
                    state = 1
                    print(state)
                elif ord(line[index]) & 0xF0 == 0xE0:  # 第三种
                    state = 2
                    print(state)
                elif ord(line[index]) & 0xF8 == 0xF0:  # 第四种
                    state = 3
                    print(state)
                else:
                    print("%s isn't a utf8 file,lineee:\t" % file_name + str(line_num))   # unicode
                    sys.exit(1)
            else:
                if not ord(line[index]) & 0xC0 == 0x80:
                    print("%s isn't a utf8 file in lineww:\t" % file_name + str(line_num))
                    sys.exit(1)
                state -= 1
    if existBOM(file_name):
        print("%s isn't a standard utf8 file,include BOM header." % file_name)   # utf-8
        sys.exit(1)


def existBOM(file_name):
    file_obj = open(file_name)
    code = file_obj.read(3)
    file_obj.close()
    if code == codecs.BOM_UTF8:  # 判断是否包含EF BB BF
        return True
    return False


if __name__ == "__main__":
    file_name = 'code.txt'
    detectUTF8(file_name)