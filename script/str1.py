# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 字符串使用方法 str1.py
# *******************************************************************
'''
字符串内置函数 ，查看方法：dir('')
1，capitalize，将字符串首字母转为大写，其余字母转为小写。如：str.capitalize() ，"my naMe Is John" => "My name is john"
2，casefold，将字符串中所有大写字母转为小写，支持多国语言。如：str.casefold()，"my naMe Is John" => "my name is john"  ， "ß => "ss"
3，center，将字符串以某种形式居中。如：str.center(10, "-")) ，"1234"=> "---1234---"
4，count，统计字符串中某字符出现的次数。如：str.count("3")，"12343335673"  => 5
5，encode，将普通字符串转二进制，如 str.encode('utf-8')  ，"李四" => b'\xe6\x9d\x8e\xe5\x9b\x9b'
6，endswith，从右往左判断某个字符正确返回True，错误返回False。
7，expandtabs，将字符串中tab符号(\\t)转为空格。如：str.expandtabs(16)，"this is\ta apply" => "this is         a apply"
8，find，从左往右查找字符串中某字符是否存在，找到则返回下标，否则返回-1。如 str.find("are"), "you are a man"  => 4
9，format，字符串格式化。 如：'{} {}'.format(str1,str2)
10，format_map，字典格式化。如：'{class}班{name}总分{score}'.format_map(dict1), 如：{'name': '小明', 'class': '20190301', 'score': 597.5}  => "20190301班小明总分：597.5"
11，index，获取字符串中字符位置下标，如：str.index("are")，"you are a man" => 4
12，isalnum，判断str1是否由数字、字母、中文组成， 如：str.isalnum() , "you你好123" => True
13，isalpha，判断str1是否为纯字母（包括中文），如：str.isalpha(),  "you你好rrrr" => True
14，isascii
15，isdecimal，判断是否是阿拉伯数字( Unicode，全角)，如：str.isdecimal(), "123" => True
16，isdigit，判断是否是阿拉伯数字(Unicode,byte,全角)，如：str.isdigit(), "１２３４" => True
17，isidentifier，判断字符串是否是有效标识符，如： str.isidentifier(), "中国123" => True
18，islower，判断字符串是否全部为小写，如：str.islower(), "youman" => True
19，isnumeric，判断是否是阿拉伯数字(Unicode,全角,罗马,中文数字)，如：str.isnumeric,  "Ⅲ" => True
20，isprintable，判断字符串中所有字符是否都是可打印字符(in repr())或字符串为空。如：''.isprintable()  => True
21，isspace，判断字符串中是否只有空白符。如："   ".isspace()   => True
22，istitle，判断字符串中每个单词首字母是否为大写及其他字母是否为小写，如：str.istitle()，"This Is String" => True
23，isupper，判断字符串是否全部为大写，如：str.isupper(), "ABC" => True
24，join，用于将序列中的元素以指定的字符连接生成一个新的字符串，如：s2.join(("j", "i", "n"))，"-" => "jin"
25，ljust，在字符串右边新增字符，如：str.ljust(10, '*'))  "jinhao" => "jinhao****"
26，lower，将字符串中大写字符转小写，如：str.lower(),  "JinHao" => "jinhao"
27，lstrip，去掉字符串左边字符（默认空格）,如：str.lstrip('3'), "33333jinhao"  => "jinhao"
28，maketrans，创建字符映射转换表
29，partition，从左向右寻找，以字符串中的某个元素为中心将左右分割共分割成三个元素并放入到元组中，如：a.partition("is")，"hello is goog is world" =>('hello ', 'is', ' goog is world')
30，replace，将字符串中某字符进行替换，至指定替换次数不超过N次，如：str.replace("is", "was", 3) ，"he is is is is man" => "he was was was is man"
31，rfind ，类似find
32，rindex ，类似index
33，rjust，类似ljust
34，rpartition，从右向左寻找，以字符串中的某个元素为中心将左右分割共分割成三个元素并放入到元组中，如：a.partition("is")，"hello is goog is world" =>('hello is goog ', 'is', ' world')
35，rsplit，从右向左通过指定分隔符对字符串进行切片，如 S.rsplit('i',1)，"this is string example....wow!!!" => ['this is str', 'ng example....wow!!!']
36，rstrip，类似lstrip
37，split，通过指定分隔符对字符串进行切片，类似rsplit
38，splitlines，通过特殊符号分隔符对字符串进行切片。如：str1.splitlines() ，  'ab c\n\nde fg\rkl\r\n' => ['ab c', '', 'de fg', 'kl'] ; str2.splitlines(True) =>['ab c\n', '\n', 'de fg\r', 'kl\r\n']
39，startswith，从左往右判断某个位置的字符是否是预期值，如：str.startswith("y"), "you are a man"  => True
40，strip
41，swapcase
42，title
43，translate
44，upper

45,f-string
46, 原始字符串
47，表示真除，%表示取余，//结果取整
'''


print("1，str.capitalize() 将字符串首字母转为大写，其余字母转为小写。".center(100, "-"))
print("my naMe Is John".capitalize())  # My name is john


print("2，str.casefold() 将字符串中所有大写字母转为小写。".center(100, "-"))
# casefold() 方法是Python3.3 版本之后引入的，其效果和 lower()方法非常相似，可将字符串中所有大写字母转为小写。
# 两者的区别是：lower() 方法只对ASCII编码，也就是‘A - Z’有效，对于其他语言（非英文）的大转小只能用 casefold()方法。
S1 = "Runoob EXamPLE....WOW!!!"  # 英文
S2 = "ß"  # 德语
print(S1.lower())   # runoob example....wow!!!
print(S1.casefold())  # runoob example....wow!!!
print(S2.lower())  # ß
print(S2.casefold())  # ss   //德语的"ß"正确的小写是"ss"


print("3，str.center(width[,fillchar]) 将字符串以某种形式居中".center(100, "-"))
# 功能：返回一个以width为宽度，str居中，以fillchar填充的字符"
# 注意：fillchar默认为空格，且fillchar只能是单个字符。
str1 = "标题"
print(str1.center(10))    #    1234     // 1234前后各有3个空格
print(str1.center(22, "-"))   # ---1234--
print(str1.center(10, "-"))   # ---1234---
print(str1.center(10, "k"))  # kkk1234kkk
print(str1.center(10, "9"))  # 9991234999
print(str1.center(10, "和"))  # 和和和1234和和和
# print(str1.center(10, "88"))  # 报错，TypeError: The fill character must be exactly one character long   因为只能是单个字符
# print(str1.center(10, ""))   # 报错，TypeError: The fill character must be exactly one character long 因为fillchar不能没有值。


print("4，str.count('sub'[,start,end)) 统计字符串中某字符出现的次数".center(100, "-"))
# 功能：统计sub在str中出现的次数，若不指定start与end则默认统计整个字符串，[start,end) 表示字符的起始范围，中括号表示包含，圆括号表示不包含。
str1 = "12343335673"
print(str1.count("3"))   # 5
print(str1.count("3", 5))   # 3
print(str1.count("3", 5, 7))   # 2
print(str1.count("3", 0, 0))   # 0
print(str1.count("3", 2, 11111))   # 5
str1 = "31233334563"
print(str1.count("3", 1, len(str1)-1))   # 4  //统计字符串“31233334563”中除前后2个3以外所有3出现的个数。


print("5，str1.encode() 将字符串转二进制".center(100, "-"))
# byte1.decode()，将二进制字符串转为普通字符串
# 注意：编码的格式与解码的格式必须保持一致
# Python3 里有两种表示字符序列的类型，分别是 bytes 和 str, 其中bytes 的实例包含 8 位值，str 的则包含 Unicode 字符。
# Python2 里有两种表示字符序列的类型，分别是 str 和 Unicode，它与 Python3 的不同是，str 的实例包含原始的 8 位值，而 Unicode 的实例包含 Unicode 字符。
# 所以：Python3 中字符串默认为 Unicode；如：str1 = "你好"
# 而Python2 中使用 Unicode，则必须在字符串的前面加一个 「u」前缀，如 ：str1= u"你好"   。 python2中 通过 from __future__ import unicode_literals 可设置默认unicode字符串。
s = "李四"   # Unicode 的表现形式
b = s.encode('utf-8')   # utf-8 是一种编码形式，是Unicode 的一种存储形式罢了。
print(b)  # b'\xe6\x9d\x8e\xe5\x9b\x9b'
# 存储形式用在哪里？文本文件里内容与文件编码格式不一致的话保存就会报错，如文件编码默认是 ASCII 编码，显然用 Unicode 表示的汉字是无法用 ASCII 码存储的，所以就抛出了 UnicodeEncodeError 异常。
# python3 很好地解决了这个问题，通过open 参数 encoding='utf-8' 进行内容编码。其实也就是 name.encode('utf-8') ，将 unicode 转为 二进制数据，如：
# with open('./Desktop/data.txt', 'w', encoding='utf-8') as f:
# ...    f.write(name)
str1 = "测试"
str2 = b'\xe6\xb5\x8b\xe8\xaf\x95'
byte1 = str1.encode()
print(byte1)  # b'\xe6\xb5\x8b\xe8\xaf\x95'
print(byte1.decode("utf-8"))  # 测试
unicodestring = "金浩"
print(unicodestring.encode("utf-8"))  # b'\xe9\x87\x91\xe6\xb5\xa9'
print(unicodestring.encode("utf-16"))  # b'\xff\xfe\xd1\x91im'
# print(unicodestring.encode("ascii"))   # 报错，UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)  因为超出的127个字符
# print(unicodestring.encode("ISO-8859-1"))  # 报错， UnicodeEncodeError: 'latin-1' codec can't encode characters in position 0-1: ordinal not in range(256)   因为超出的256个字符

s = "ABCD金浩"
print(s[1])  # B
print(s[0:3])  # ABC
b = s.encode("utf-8")
print(b[0])  # 65
print(b[0] + b[1])  # 131 = 65 + 66
if b[0] < b[1]:
    print("ok")
print(b[4])  #  233
print(b)  # b'ABCD\xe9\x87\x91\xe6\xb5\xa9'
s = b.decode("utf-8")
print(s)  # ABCD金浩

s = "金"
b = s.encode("utf-8")
print(b)  # b'\xe9\x87\x91'
b = s.encode("utf-16")
print(b)  # b'\xe9\x87\x91'

# 将字符转ascii或unicode编码
s = "金"
x = "浩"
print(ord(s))  # 37329
print(ord(x))  # 28009
print(type(ord(s)))  # <class 'int'>
s = chr(37329)  # 金
x = chr(28009)  # 浩
print(s + x)  # 金浩
# s = "马"
s = "严"
print(s.encode('utf-8'))  # b'\xe4\xb8\xa5'  //unicode内存编码，十六进制
print(s.encode('gb2312'))  # b'\xd1\xcf'   //unicode内存编码，十六进制
print(s.encode('unicode_escape'))  # b'\\u9a6c'    //unicode内存编码，十六进制
print(type(s.encode('unicode_escape')))  # <class 'bytes'>
print(s.encode('unicode_escape').decode())  # \u9a6c   //unicode编号 0x9A6C
print(type(s.encode('unicode_escape').decode()))  # <class 'str'>
print(ord(s))  # 39532   //unicode整数编号
print(type(ord(s)))  # <class 'int'>
print(bin(ord(s)))  # 0b 1001101001101100     //二进制形式的字符串
print(type(bin(ord(s))))  # <class 'str'>
print(bytes(b'\\u9a6c').decode("unicode_escape"))  # 马   //解码


print("6，str1.endswith('xx'[,start,end]) 从右往左判断某个位置的字符是否是预期值，返回True或False ".center(100, "-"))
# 功能：从右往左判断某个位置的字符是否是预期值，返回True或False，可指定范围，则取值范围为[start,end)
str1 = "you are a nice man"
print(str1.endswith("a", 0, 5))  # True  //在 you a 区间从右往左判断。


print("7，str.expandtabs(tabsize=8) 将字符串中tab符号(\\t)转为空格".center(100, "-"))
# tab 符号('\t')默认的空格数是 8
str = "this is\tstring example....wow!!!"
print(str.expandtabs())  # this is string example....wow!!!   //去掉\t符号
print(str.expandtabs(16))   # this is         string example....wow!!!    //8个空格替换\t


print("8，str1.find(sub, start, end) 从左往右查找字符串中某字符是否存在，并返回下标".center(100, "-"))
# 功能：从左往右查找字符串中某字符是否存在，若存在则返回第一匹配到的下标值，若不存在则返回 - 1
# 注意：若指定start与end，则在[start, end)范围内查询，若不指定则查询整个字符串。
str1 = "you are a nice man"
print(str1.find("are"))   # 4
print(str1.find("aare"))   # -1


print("9，str.format() 字符串格式化".center(100, "-"))
str1 = "you are a nice man"
str2 = "hello john"
x = "{} str3 {}".format(str1, str2)
print(x)  # you are a nice man str3 hello john   # 如：在str1和str2中插入str3，无空格（可在str3前后增加空格）


print("10, str.format_map(map) 字典格式化".center(100, "-"))
# 参考：https://blog.csdn.net/LaoYuanPython/article/details/89478668  第3.10节 Python强大的字符串格式化新功能：使用format字符串格式化
student = {'name': '小明', 'class': '20190301', 'score': 597.5}
s1 = '{st[class]}班{st[name]}总分：{st[score]}'.format(st=student)
print(s1)  # 20190301班小明总分：597.5
s1 = '{class}班{name}总分：{score}'.format_map(student)
print(s1)  # 20190301班小明总分：597.5


print("11，str.index() 获取字符串中字符位置下标".center(100, "-"))
str1 = "you are a nice man"
print(str1.index("are"))  # 4
# print(str1.index("are2"))  # 报错，ValueError: substring not found


print("12，str1.isalnum() 判断str1是否由数字、字母、中文，返回True或False".center(100, "-"))
# 注意：中文默认也是字母
print("1234".isalnum())  # True
print("测试".isalnum())  # True
print("abc".isalnum())  # True
print("hi john".isalnum())  # False   //有空格
print("@#$".isalnum())  # False   //有特殊字符


print("13，str1.isalpha() 判断str1是否字母、中文，返回True或False".center(100, "-"))
print("test".isalpha())  # True
print("测试".isalpha())  # True
print("1234".isalpha())  # False
print("you@#$".isalpha())  # False
print("hi john".isalpha())  # False


print("14，isascii ?".center(100, "-"))


print("15，str1.isdecimal() 判断是否是阿拉伯数字(Unicode，全角)".center(100, "-"))
# True: 阿拉伯数字、全角阿拉伯数字（双字节）
# False: 汉字数字、罗马数字、小数
# Error: byte数字（单字节）
print("1234".isdecimal())  # True
print("１２３４".isdecimal())  # True
print("一".isdecimal())  # False
print("III".isdecimal())  # False
print("0.11".isdecimal())  # False
print("测试1234".isdecimal())  # False

print("16，str1.isdigit() 判断是否是阿拉伯数字(Unicode,byte,全角)".center(100, "-"))
# True: 阿拉伯数字、全角阿拉伯数字（双字节）、bytes数字（单字节）
# False: 汉字数字、罗马数字、小数、汉字与数字混合
print('1234'.isdigit())  # True
print("１２３４".isdigit())  # True
print(b"1234".isdigit())  # True
print("一".isdigit())  # False
print("III".isdigit())  # False
print("0.11".isdigit())  # False
print("测试1234".isdigit())  # False


print("17，isidentifier() 判断字符串是否是有效标识符".center(100, "-"))
# 如果字符串仅包含字母数字字母（a-z）和（0-9）或下划线（_）或中文，则该字符串被视为有效标识符。有效的标识符不能以数字开头或包含任何空格。
print("if".isidentifier())  # True
print("def".isidentifier())  # True
print("class".isidentifier())  # True
print("_a".isidentifier())  # True
print("中国123a".isidentifier())  # True
print("123".isidentifier())  # False
print("3a".isidentifier())  # False
print("".isidentifier())  # False



print("18， str1.islower() 判断字符串是否全部为小写".center(100, "-"))
str1 = "youman"
str2 = "youAman"
print(str1.islower())  # True
print(str2.islower())  # False


print("19，str1.isnumeric() 判断是否是阿拉伯数字(Unicode,全角,罗马,中文数字)".center(100, "-"))
# True: 阿拉伯数字、全角阿拉伯数字（双字节）、罗马数字、汉字数字
# False: 小数
# Error: byte数字（单字节）
print("1234".isnumeric())  # True
print("３４".isnumeric())  # True
print("Ⅲ".isnumeric())  # True
print("一二三四".isnumeric())  # True
print("0.11".isnumeric())  # False
print("测试1234".isnumeric())  # False


print("20，isprintable() 判断字符串中所有字符是否都是可打印字符(in repr())或字符串为空".center(100, "-"))
# 如果字符串中的所有字符都是可打印的字符或字符串为空返回 True，否则返回 False
print('oiuas\tdfkj'.isprintable())  # 制表符  # False
print('oiuas\ndfkj'.isprintable())  # 换行符  # False
print('oiu 123'.isprintable())  # True
print('~'.isprintable())  # True
print(''.isprintable())  # True


print("21， str1.isspace() 判断字符串中是否只有空白符".center(100, "-"))
# # 功能：判断字符串中是否只包含空白符，若是则返回True，否则返回False。
str1 = "    "
print(str1.isspace())  # True
str1 = ""
print(str1.isspace())  # False



print("22, str1.istitle(), 判断字符串中每个单词首字母是否为大写及其他字母是否为小写，是则返回True，否则返回 False.".center(100, "-"))
str1 = "This Is String Example...Wow!!!"
str2 = "This is string example....wow!!!"
str3 = "This Is String Example...WoW!!!"
print(str1.istitle())  # True
print(str2.istitle())  # False
print(str3.istitle())  # False  //因为最后WoW中有大写


print("23，str1.isupper() 判断字符串是否全部为大写".center(100, "-"))
str1 = "youman"
str2 = "youAman"
str3 = "ABC"
print(str1.isupper())  # False
print(str2.isupper())  # False
print(str3.isupper())  # True


print("24，str.join(sequence) 用于将序列中的元素以指定的字符连接生成一个新的字符串。".center(100, "-"))
# sequence 表示要连接的元素序列，序列中的元素必须是字符串。
# join进行拼接，使用字符分隔序列， 如：" - ".join(序列)
seq = ("r", "u", "n", "o", "o", "b")  # 字符串序列
s1 = "-"
print(s1.join(seq))  # r-u-n-o-o-b

s2 = ""
print(s2.join(("r", "u", "n", "o", "o", "b")))  # runoob


print("25，str.ljust(width,fillchar) 在字符串右边新增字符".center(100, "-"))
# # 返回一个原字符串左对齐, 并使用空格填充至指定长度的新字符串。如果指定的长度小于原字符串的长度则返回原字符串。
str = "jinhao"
print(str.ljust(10, '*'))  # jinhao****



print("26，str.lower() 将字符串中大写字符转小写".center(100, "-"))
str = "Runoob EXAMPLE....WOW!!!"
print(str.lower())  # runoob example....wow!!!


print("27，str.lstrip() 去掉字符串左边字符（默认空格）".center(100, "-"))
str = "     this is string example....wow!!!     "
print(str.lstrip())  # "this is string example....wow!!!     "     //右面有空格
str = "88888888this is string example....wow!!!8888888"
print(str.lstrip('8'))    # this is string example....wow!!!8888888


print("28，str.translate(intab,outtab[,deltab]) 创建字符映射转换表".center(100, "-"))
# 接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串，表示转换的目标。两个字符串的长度必须相同，为一一对应的关系。
# bytearray.maketrans()、bytes.maketrans()、str.maketrans()
# 一般 maketrans() 方法需要配合 translate() 方法一起使用。
intab = "aeiou"
outtab = "12345"
deltab = "thw"
trantab1 = str.maketrans(intab, outtab)  # 创建字符映射转换表
trantab2 = str.maketrans(intab, outtab, deltab)  # 创建字符映射转换表，并删除指定字符
test = "this is string example....wow!!!"
print(test.translate(trantab1))  # th3s 3s str3ng 2x1mpl2....w4w!!!
print(test.translate(trantab2))  # 3s 3s sr3ng 2x1mpl2....4!!!



print("29，str.partiton(str) 从左向右寻找，以字符串中的某个元素为中心将左右分割共分割成三个元素并放入到元组中".center(100, "-"))
a = "hello is goog is world"
print(a.partition("is"))  # ('hello ', 'is', ' goog is world')


print("30，str.replace(old,new[,max]) 将字符串中某字符进行替换，至指定替换次数不超过N次".center(100, "-"))
str = "he is is is is man"
print(str.replace("is", "was"))  # he was was was was man
print(str.replace("is", "was", 3))  # he was was was is man



print("33，str.rjust(width,fillchar) 在字符串左边新增字符".center(100, "-"))
# # 返回一个原字符串右对齐, 并使用空格填充至指定长度的新字符串。如果指定的长度小于原字符串的长度则返回原字符串。
str = "jinhao"
print(str.rjust(10, '*'))  # ****jinhao



print("34，str.rpartiton(str) 从右向左寻找，以字符串中的某个元素为中心将左右分割共分割成三个元素并放入到元组中".center(100, "-"))
a = "hello is goog is world"
print(a.rpartition("is"))  # ('hello is goog ', 'is', ' world')
print(a.rpartition("is")[2])


print("35，str.rsplit(str="", num) 从右向左通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则分隔 num+1 个子字符串".center(100, "-"))
# str -- 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
# num -- 分割次数, 默认为 -1, 即分隔所有。
S = "this is string example....wow!!!"
print(S.rsplit( ))  # ['this', 'is', 'string', 'example....wow!!!']
print(S.rsplit('i',1))  # ['this is str', 'ng example....wow!!!']
print(S.rsplit('w'))  # ['this is string example....', 'o', '!!!']


print("36，str.rstrip() 去掉字符串右边字符（默认空格）".center(100, "-"))
str = "     this is string example....wow!!!     "
print(str.rstrip())  #  "     this is string example....wow!!!
str = "88888888this is string example....wow!!!8888888"
print(str.rstrip('8'))    # 88888888this is string example....wow!!!



print("37，str.split(str="", num) 通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则分隔 num+1 个子字符串".center(100, "-"))
# str -- 分隔符，默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
# num -- 分割次数, 默认为 -1, 即分隔所有。
str = "Line1-abcdef \nLine2-abc \nLine4-abcd";
print(str.split( ))  # ['Line1-abcdef', 'Line2-abc', 'Line4-abcd']   //以空格为分隔符，包含 \n
print(len(str.split( )))
print(str.split(' ', 1 ))  # ['Line1-abcdef', '\nLine2-abc \nLine4-abcd']  //以空格为分隔符，分隔成两个


print("38，str.splitlines(str="", num) 通过特殊符号分隔符对字符串进行切片".center(100, "-"))
# 按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。
str1 = 'ab c\n\nde fg\rkl\r\n'
print(str1.splitlines())  # ['ab c', '', 'de fg', 'kl']
str2 = 'ab c\n\nde fg\rkl\r\n'
print(str2.splitlines(True))  # ['ab c\n', '\n', 'de fg\r', 'kl\r\n']



print("39，str1.startswith('xx'[,start,end]) 从左往右判断某个位置的字符是否是预期值".center(100, "-"))
# 功能：从左往右判断某个位置的字符是否是预期值，返回True或False，可指定范围，则取值范围为[start,end)
str1 = "you are a nice man"
print(str1.startswith("y"))  # True
print(str1.startswith("o", 1))  # True

# ****************************************************************************************************************************************************

#
# # json实现 字典 与 字符串 互转换
# dict7 = {'a':'192.168.1.1','b':'192.168.1.2'}
# import json
# # 字典 转 字符串，json.dumps()
# str7 = json.dumps(dict7)
# print(type(str7)) # <class 'str'>
# print(str7)   # {"a": "192.168.1.1", "b": "192.168.1.2"} , 技巧，如果输出结果中是双引号，这一组就是字符串
#
# # 字符串 转 字典，json.loads()
# x = '{"a": "192.168.1.1", "b": "192.168.1.211111"} '
# dict7 = json.loads(x)
# print(dict7)  # {'a': '192.168.1.1', 'b': '192.168.1.2'} # 技巧，如果输出结果中是单引号，这一组就是字典
#


print("45, f-string".center(100, "-"))
name = "john"
print(f'hello {name} + {1}')  # hello john + 1
x = 1
print(f'{x+1=}')  # x+1=2
print(f'{x+1}')  # 2


print("46, 原始字符串".center(100, "-"))
print( r'\n123' )
print( '\\n123' )
para_str = """这是一个多行字符串的实例
多行字符串可以使用制表符
TAB ( \t )。
也可以使用换行符 [ \n ]。
"""
print(para_str)


print("47，表示真除，%表示取余，//结果取整".center(100, "-"))
print('3 / 2 =', 3 / 2)  # 真除
print('3 // 2 =', 3 // 2)  # 取整
print('3 / 2.0 =', 3 / 2.0)
print('3 // 2.0 =', 3 // 2.0)
