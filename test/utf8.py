# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2017-4-6
# Description: 编码与解码
# 中文\unicode编码在线转换工具, http://www.bangnishouji.com/tools/chtounicode.html
# 在线base64编码解码、base64加密解密 - aTool在线工具 http://www.atool.org/base64.php
#****************************************************************


# 在str的文档中有这样的一句话:
# 也就是说在读取一个文件的内容或者从网络上读取到内容时，保持的对象为str类型；
# 如果想把一个str转换成特定编码类型，需要把str转为Unicode,然后从unicode转为特定的编码类型如：utf-8、gb2312等；

# unicode 转 gb2312,utf-8等
s = '中国'
s_gb1 = s.encode('gb2312')
s_gb2 = s.encode('utf-8')
print(s_gb1)  # �й�
print(s_gb2)  # 中国

#
# # utf-8,GBK 转 unicode 使用函数unicode(s,encoding) 或者s.decode(encoding)
# s = u'上海'
# s_utf8 = s.encode('UTF-8')  # 先将unicode 转 utf-8
# print s_utf8.decode('utf-8')  # 上海
#
#
# # str 转 unicode
# s = '北京'  #因为s为所在的.py(# -*- coding=UTF-8 -*-)编码为utf-8
# s_unicode = s.decode('UTF-8')  # 将 utf-8 转 unicode
# print s_unicode  # 北京
# print s.decode('utf-8').encode('gb2312')  # ���� , s 先转 unicode 再转 gb2312
# # 如果直接执行s.encode('gb2312')会发生什么？
# # print s.encode('gb2312')  # UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
# # Python 会自动的先将 s 解码为 unicode ，然后再编码成 gb2312。因为解码是python自动进行的，我们没有指明解码方式，
# # python 就会使用 sys.defaultencoding 指明的方式来解码。很多情况下 sys.defaultencoding 是 ANSCII，如果 s 不是这个类型就会出错。
# # 拿上面的情况来说，我的 sys.defaultencoding 是 anscii，而 s 的编码方式和文件的编码方式一致，是 utf8 的，
# # 所以出错了: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
# # 如：
# import sys
# reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
# sys.setdefaultencoding('utf-8')
# str = '中文'
# print str.encode('gb2312')  # ����
#
#
# # 文件编码与print函数
# # 建立一个文件test.txt，文件格式用ANSI，内容为: abc中文
# # text.py 内容如下：
# # coding=gbk
# # print open("Test.txt").read()
# # 结果：abc中文
# # 把文件格式改成UTF-8，结果：abc涓枃
# # 显然，这里需要解码：
# # coding=gbk
# import codecs
# # print open("Test.txt").read().decode("utf-8")
# # 结果：abc中文
# # 上面的test.txt我是用Editplus来编辑的，但当我用Windows自带的记事本编辑并存成UTF-8格式时，
# # 运行时报错：
# # Traceback (most recent call last):
# #   File "ChineseTest.py", line 3, in <module>
# #     print open("Test.txt").read().decode("utf-8")
# # UnicodeEncodeError: 'gbk' codec can't encode character u'/ufeff' in position 0: illegal multibyte sequence
# # 原来，某些软件，如notepad，在保存一个以UTF-8编码的文件时，会在文件开始的地方插入三个不可见的字符（0xEF 0xBB 0xBF，即BOM）。
# # 因此我们在读取时需要自己去掉这些字符，python中的codecs module定义了这个常量：
# # # coding=gbk
# # import codecs
# # data = open("Test.txt").read()
# # if data[:3] == codecs.BOM_UTF8:
# #   data = data[3:]
# # print data.decode("utf-8")
# # 结果：abc中文
#
#
#
# # 如果在python文件中指定编码方式为 utf-8(# coding=utf-8)，那么所有带中文的字符串都会被认为是utf-8编码的 byte string
# # （例如：mystr="你好"），
# # 但是在函数中所产生的字符串则被认为是 unicode string。
#
# # 问题就出在这边，unicode string和 byte string 是不可以混合使用的，一旦混合使用了，就会产生这样的错误。例如：
# # self.response.out.write("你好" + self.request.get("argu"))
# # 其中，"你好"被认为是byte string，而self.request.get("argu")的返回值被认为是unicodestring。
# # 由于预设的解码器是ascii，所以就不能识别中文bytestring。然后就报错了。
#
# # 以下有两个解决方法：
# # 1.将字符串全都转成byte string。
# # self.response.out.write("你好" + self.request.get("argu").encode("utf-8"))
# #
# # 2.将字符串全都转成unicode string。
# # self.response.out.write(u"你好" + self.request.get("argu"))
# # bytestring转换成unicode
# # string可以这样转unicode(unicodestring, "utf-8")
#
# # python中包含UTF-8编码中文的列表或字典的输出  https://segmentfault.com/a/1190000002447836
# dict = {"abcd123": "测试学习"}
# print dict   # {'abcd123': '\xe6\xb5\x8b\xe8\xaf\x95\xe5\xad\xa6\xe4\xb9\xa0'}
# list = ["人民解放军", "12", 0]  # ['\xe4\xba\xba\xe6\xb0\x91\xe8\xa7\xa3\xe6\x94\xbe\xe5\x86\x9b', '12', 0]
# print list
# list = [u"人民解放军", "12", 0] # [u'\u4eba\u6c11\u89e3\u653e\u519b', '12', 0]
# print list
#
# # 格式化输出
# import json
# print json.dumps(dict, encoding="UTF-8", ensure_ascii=False)  # {"abcd123": "测试学习"}
# print json.dumps(list, encoding="UTF-8", ensure_ascii=False)  # ["人民解放军", "12", 0]
#
# # Python encode() 方法以 encoding 指定的编码格式编码字符串。errors参数可以指定不同的错误处理方案。
# # 字符串的话直接用 encode("utf-8")
#
# str = u"中国"
# print str  # 中国
#
# # 将 字符串 转 base64
# str = "this is string example....wow!!!"
# print str.encode("base64", 'strict')  # 中国
#
#
# # ======================================================================================
# # 2、[python]去掉 unicode 字符串前面的 u
# # https://mozillazg.com/2013/12/python-raw-unicode.html
# # unicode.encode('raw_unicode_escape')
# print "~~~~~~~"
# a = ['你好']
# print a
# print u"你好".encode('raw_unicode_escape')
# print u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape')
# print u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape').decode('utf8')   # u'\u4f60\u597d'
# print u'\u4f60\u597d'
# str2='\u91d1\u91d1 \u7ed9\u60a8\u53d1\u73b0\u91d1\u7ea2\u5305\u5566\uff010.20\u5143\u7ea2\u5305\u7b49\u5927\u5bb6\u6765\u62a2\uff0c\u62a2\u5230\u5c31\u80fd\u63d0\u73b0\u54e6~'
# print str2.decode('unicode_escape')
# print "!!!!!!!!"
#
#
# # ======================================================================================
# # 3、关于python编码的文章，http://blog.csdn.net/liuxincumt/article/details/8183391
#
# # ======================================================================================
# # 4、普通字符串可以用多种方式编码成Unicode
# # Description: Python如何将Unicode中文字符串转换成 string字符串
# # http://python.jobbole.com/81244/
# unicodestring = u"Hello world"
# # 将Unicode转化为普通Python字符串："encode"
# utf8string = unicodestring.encode("utf-8")
# asciistring = unicodestring.encode("ascii")
# isostring = unicodestring.encode("ISO-8859-1")
# utf16string = unicodestring.encode("utf-16")
# print utf8string
# print asciistring
# print isostring
# print utf16string
#
#
# # 将普通Python字符串转化为Unicode："decode"
# plainstring1 = unicode(utf8string, "utf-8")
# plainstring2 = unicode(asciistring, "ascii")
# plainstring3 = unicode(isostring, "ISO-8859-1")
# plainstring4 = unicode(utf16string, "utf-16")
# print plainstring1
# print plainstring2
# print plainstring3
# print plainstring4
#
#
# # ======================================================================================
# # 5、自动编码转换
# stri = "金浩"
# def zh2unicode(stri):
#    """Auto converter encodings to unicode
#    It will test utf8,gbk,big5,jp,kr to converter"""
#    for c in ('utf-8', 'gbk', 'big5', 'jp', 'euc_kr', 'utf16', 'utf32'):
#        try:
#             return stri.decode(c)
#        except:
#             pass
#    return stri
# print zh2unicode(stri)
#
#
# # 6、自动识别是unicode还是utf-8
# # s = u"中文"
# s = "中文"
# if isinstance(s, unicode):
#    #s=u"中文"
#    print s.encode('utf-8')
#    print "1111"
# else:
#    #s="中文"
#    print s.decode('utf-8').encode('utf-8')
#    print "2222"
#
# # ======================================================================================================================
# #  python raw-input odd behavior with accents containing strings
# # 它是将终端的输入编码通过decode转换成unicode编码
# # https://stackoverflow.com/questions/11068581/python-raw-input-odd-behavior-with-accents-containing-strings
# # To read a unicode string in, you need to realise that raw_input gives you a bytestring - so, you need to convert it
# # using its .decode method. You need to pass .decode the encoding of your STDIN - which is available as sys.stdin.encoding
# #  (don't just assume that this is UTF8 - it often will be, but not always) - so, the whole line will be:
# # string = raw_input(...).decode(sys.stdin.encoding)
# # But by far the easiest way around this is to upgrade to Python 3 if you can - there, input() (which behaves like the
# # Py2 raw_input otherwise) gives you a unicode string (it calls .decode for you so you don't have to remember it), and
# # unprefixed strings are unicode strings by default. Which all makes for a much easier time working with accented characters
# # - it essentially implies that the logic you were trying would just work in Py3, since it does the right thing.
# # Note, however, that the error you're seeing would still manifest in Py3 - but since it does the right thing by default,
# # you have to work hard to run into it. But if you did, the comparison would just be False, with no warning - Py3 doesn't
# # ever try to implictly convert between byte and unicode strings, so any byte string will always compare unequal to any
# # unicode string, and trying to order them will throw an exception.
#
# varProductName = raw_input(unicode('\n请输入产品名称：', 'utf-8').encode('gbk')).decode(sys.stdin.encoding)
# print type(varProductName)  # <type 'unicode'>
#
# # ======================================================================================================================
# # 从cmd中输入中文传入python，如下
#
# unicode(varValue, 'gbk')
#
# https://blog.csdn.net/eastmount/article/details/48841593