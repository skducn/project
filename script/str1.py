# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 字符串使用方法 str1.py
# *******************************************************************
'''
查看字符串内置函数：dir('')
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
'capitalize', 'casefold', 'center', 'count',
'encode', 'endswith', 'expandtabs',
'find', 'format', 'format_map',
'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper',
'join',
'ljust', 'lower', 'lstrip',
'maketrans',
'partition',
'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip',
'split', 'splitlines', 'startswith', 'strip', 'swapcase',
'title', 'translate',
'upper',
'zfill']
'''


print("1，str.capitalize()将字符串第一个首字母转为大写，其他字母转为小写。".center(100, "-"))
print("my naMe Is John".capitalize())  # My name is john


print("2，str.casefold()将字符串中所有大写字符转为小写字符。".center(100, "-"))
# casefold() 方法是Python3.3 版本之后引入的，其效果和 lower()方法非常相似，都可以转换字符串中所有大写字符为小写。
# 两者的区别是：lower() 方法只对ASCII编码，也就是‘A - Z’有效，对于其他语言（非汉语或英文）中把大写转换为小写的情况只能用 casefold()方法。
S1 = "Runoob EXamPLE....WOW!!!"  # 英文
S2 = "ß"  # 德语
print(S1.lower())   # runoob example....wow!!!
print(S1.casefold())  # runoob example....wow!!!
print(S2.lower())  # ß
print(S2.casefold())  # ss   //德语的"ß"正确的小写是"ss"


print("3，str.center(width[,fillchar]), 返回一个以width为宽度，str1居中的，使用fillchar填充的字符串。".center(100, "-"))
# # 注意：fillchar不写时默认为空格。
str1 = "1234"
print(str1.center(10))    #    1234     // 1234前后各有3个空格，等同于 print(str1.center(10, " "))
print(str1.center(10, "-"))   # ---1234---
print(str1.center(10, "k"))  # kkk1234kkk
print(str1.center(10, "9"))  # 9991234999
# print(str1.center(10, ""))   # 报错，因为fillchar不能没有值。


print("3，str.count('sub'[,start,end)), 统计sub在str中出现的次数，若不指定start与end则默认统计整个字符串".center(100, "-"))
# # 若指定start与end，则统计的范围[start,end)
str1 = "12343335673"
print(str1.count("3"))   # 5
print(str1.count("3", 5))   # 3
print(str1.count("3", 5, 7))   # 2


print("5，str1.encode()，将普通字符串转为二进制".center(100, "-"))
# # byte1.decode()，将二进制字符串转为普通字符串
# # 注意：编码的格式与解码的格式必须保持一致
str1 = "1234"
str2 = b"1234"
byte1 = str1.encode()
print(byte1)  # b'1234'
print(byte1.decode("utf-8"))  # 1234


print("6，str1.startswith('xx'[,start,end]) , 若是以xx开头则返回True，否则返回False,若指定范围，则取值范围为[start,end)".center(100, "-"))
# # 若不指定范围，则默认整个字符串
str1 = "you are a nice man"
print(str1.startswith("y"))  # True
print(str1.startswith("o", 1))  # True
# 同理，endswith从尾部开始
print(str1.endswith("a", 1, 5))  # True  //在 you a 区间从尾往前。


print("7，str.expandtabs(tabsize=8), 把字符串中的 tab 符号('\t')转为空格，tab 符号('\t')默认的空格数是 8。".center(100, "-"))
str = "this is\tstring example....wow!!!"
print("替换 \\t 符号: " + str.expandtabs())  # 替换 \t 符号: this is string example....wow!!!
print("使用16个空格替换 \\t 符号: " + str.expandtabs(16))   # 使用16个空格替换 \t 符号: this is         string example....wow!!!


print("8，str1.find(sub, start, end)".center(100, "-"))
# str1.rfind(sub, start, end)
# 功能：从左往右在str1中查找sub是否存在，若存在则返回第一匹配到的下标值，若不存在则返回 - 1
# 注意：若指定start与end，则在[start, end)范围内查询，若不指定则查询整个字符串。
str1 = "you are a nice man"
print(str1.find("are"))   # 4
print(str1.find("aare"))   # -1
print(str1.rfind("are"))  # 4


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


print("11，str.index() 访问字符串中的字符的位置".center(100, "-"))
str1 = "you are a nice man"
print(str1.index("are"))  # 4


print("12，str1.isalnum(), 判断str1是否由数字与字母组成，若是则返回True，否则返回False。".center(100, "-"))
# # 注意：中文默认也是字母
str1 = "youman"
str2 = "you123man"
str3 = "1234"
str4 = "you@man"
str5 = "you man"
str6 = "you你好man"
print(str1.isalnum())  # True
print(str2.isalnum())  # True
print(str3.isalnum())  # True
print(str4.isalnum())  # False   //有特殊字符
print(str5.isalnum())  # False   //有空格
print(str6.isalnum())  # True



print("13，str1.isalpha(), 判断str1是否为纯字母，若是则返回True，否则返回False。".center(100, "-"))
# 注意：中文默认也是字母
str1 = "youman"
str2 = "you123man"
str3 = "1234"
str4 = "you@man"
str5 = "you man"
str6 = "you你好man"
print(str1.isalpha())  # True
print(str2.isalpha())  # False
print(str3.isalpha())  # False
print(str4.isalpha())  # False
print(str5.isalpha())  # False
print(str6.isalpha())  # True


print("14，isascii ?".center(100, "-"))


print("15，str1.isdecimal()：只能识别阿拉伯数字".center(100, "-"))
str1 = "1234"
print(str1.isdecimal())  # True

print("15，str1.isdigit()：只能识别阿拉伯数字".center(100, "-"))

print("16，isidentifier(), Python3 isidentifier() 方法用于判断字符串是否是有效的 Python 标识符，可用来判断变量名是否合法。".center(100, "-"))
print("if".isidentifier())  # True
print("def".isidentifier())  # True
print("class".isidentifier())  # True
print("_a".isidentifier())  # True
print("中国123a".isidentifier())  # True
print("123".isidentifier())  # False
print("3a".isidentifier())  # False
print("".isidentifier())  # False

print("17， str1.islower()".center(100, "-"))
# # 功能：判断str1中出现的字母是否全部为小写，若是则返回True，否则返回False
print("\n17")
str1 = "youman"
str2 = "youAman"
print(str1.islower())  # True
print(str2.islower())  # False


print("18，str1.isnumeric()：除了阿拉伯数字还可以识别中文的一二三".center(100, "-"))
str1 = "一二三四"
str2 = "1234"
print(str1.isnumeric())  # True
print(str2.isnumeric())  # True


print("19，isprintable(), 如果字符串中的所有字符都是可打印的字符或字符串为空返回 True，否则返回 False".center(100, "-"))
print('oiuas\tdfkj'.isprintable())  # 制表符  # False
print('oiuas\ndfkj'.isprintable())  # 换行符  # False
print('oiu 123'.isprintable())  # True
print('~'.isprintable())  # True
print(''.isprintable())  # True


print("20， str1.isspace()".center(100, "-"))
# # 功能：判断str1中是否只包含空白符，若是则返回True，否则返回False。
str1 = " "
print(str1.isspace())  # True


print("21, str1.istitle(), 如果字符串中所有的单词拼写首字母是否为大写，且其他字母为小写则返回 True，否则返回 False.".center(100, "-"))
str1 = "This Is String Example...Wow!!!"
str2 = "This is string example....wow!!!"
print(str1.istitle())  # True
print(str2.istitle())  # False


print("22，str1.isupper()".center(100, "-"))
# # 功能：判断str1中出现的字母是否全部为大写，若是则返回True，否则返回False
str1 = "youman"
str2 = "youAman"
str3 = "ABC"
print(str1.isupper())  # False
print(str2.isupper())  # False
print(str3.isupper())  # True


print("23，str.join(sequence) , 用于将序列中的元素以指定的字符连接生成一个新的字符串。".center(100, "-"))
# # sequence - - 要连接的元素序列。
# # 使用join函数进行拼接，使用字符分隔序列， 如：" 字符 ".join(序列)
# # 注意：序列中的元素必须是字符串
print("\n23")
s1 = "-"
s2 = ""
seq = ("r", "u", "n", "o", "o", "b")  # 字符串序列
print(s1.join(seq))  # r-u-n-o-o-b
print(s2.join(seq))  # runoob


print("24，str.ljust(width,fillchar)".center(100, "-"))
# # 返回一个原字符串左对齐, 并使用空格填充至指定长度的新字符串。如果指定的长度小于原字符串的长度则返回原字符串。
str = "Runoob example....wow!!!"
print(str.ljust(50, '*'))


print("25，str.lower() 返回将字符串中所有大写字符转换为小写后生成的字符串。".center(100, "-"))
str = "Runoob EXAMPLE....WOW!!!"
print(str.lower())  # runoob example....wow!!!


print("26，str.lstrip() , 返回截掉字符串左边的空格或指定字符后生成的新字符串。".center(100, "-"))
str = "     this is string example....wow!!!     "
print(str.lstrip())  # this is string example....wow!!!     , 右面有空格
str = "88888888this is string example....wow!!!8888888"
print(str.lstrip('8'))    # this is string example....wow!!!8888888

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

