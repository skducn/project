# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-22
# Description   : 字符串应用
# *********************************************************************
"""
# todo 转换

1.1 字符串转列表
1.2 字符串转元组
1.3 字符串转字典
1.4 字符串转换日期 str2date()

# todo 判断
2.0 判断字符串是否为浮点数 isFloat()
2.1 判断字符串是否为数字 isNumber()
2.2 判断字符串是否全部是中文 isChinese()
2.3 判断字符串中是否包含中文 isContainChinese()
2.4 判断复数 isComplex()

# todo 操作
3.1 删除特殊字符 delSpecialChar()
3.2 浮点数四舍五入到整数位（取整）roundInt()
3.3 小数点最后位去0 subZero()
3.4 小数点后统一位数 patchZero()

# todo 应用
4.1 字符串列表大写转小写  print([str(i).lower() for i in x])
4.2 字符串反转 print("abc"[::-1])
4.3 每个单词的第一个字母大写 print("my name is john".title())
4.4 字符串查找唯一元素 print(''.join(set("aabbddcdswer")))
4.5 重复打印字符串和列表n次
4.6 多个字符串组合为一个字符串 ' '.join()
4.7 统计列表中元素的次数
"""

from PO.StrPO import *
Str_PO = StrPO()

# print("1.1，字符串转列表".center(100, "-"))
# print(list("123"))  # ['1', '2', '3']
# print([eval(i) for i in list("123")])  # [1, 2, 3]    //必须是数字型字符串
# print(list(map(int, "123")))  # [1, 2, 3]

# print("123".split())  # ['123']
# print([eval(i) for i in "123".split()])  # [123]  //必须是数字型字符串
#
# print("1.2，字符串转元组".center(100, "-"))
# print(tuple("123"))  # ('1', '2', '3')
# print(tuple(int(i) for i in "123"))  # (1, 2, 3)
#
# print("1.3，字符串转字典".center(100, "-"))
# print(dict(eval("{'a':'1', 'b':2}")))  # {'a': '1', 'b': 2}
#
# print("1.4，字符串转换成日期".center(100, "-"))
# print(Str_PO.str2date('2020年11月23日'))
# print(Str_PO.str2date('2020-11-23'))
# print(Str_PO.str2date('2020/11/23'))
# print(Str_PO.str2date('二零二零年十一月二十三日'))
# print(Str_PO.str2date('二零年十一月二三日'))
# print(Str_PO.str2date('20年1月5日'))
# print(Str_PO.str2date('20年01月05日'))


# print("2.1，判断字符串是否为数字".center(100, "-"))
# print(Str_PO.isNumber('1'))  # True
# print(Str_PO.isNumber('1.3'))  # True
# print(Str_PO.isNumber('-1.37'))  # True
# print(Str_PO.isNumber('1e3'))  # True
# print(Str_PO.isNumber('٥'))  # True   //# 阿拉伯语 5
# print(Str_PO.isNumber('๒'))  # True  //# 泰语 2
# print(Str_PO.isNumber('四'))  # True  /# 中文数字
# print(Str_PO.isNumber('©'))  # False  /# 版权号
# print(Str_PO.isNumber('foo'))  # False
#
# print("2.2，判断字符串是否是中文".center(100, "-"))
# print(Str_PO.isChinese("测试"))  # True //字符串全部是中文
# print(Str_PO.isChinese("测123试"))  # False //字符串有非中文字符
#
# print("2.3，判断字符串中是否包含中文".center(100, "-"))
# print(Str_PO.isContainChinese("123你好"))  # True
# print(Str_PO.isContainChinese("测试一下"))  # True
# print(Str_PO.isContainChinese("123"))  # False

# print("2.4 判断复数".center(100, "-"))
# print(Str_PO.isComplex(123))  # True
# print(Str_PO.isComplex(-123))  # True
# print(Str_PO.isComplex(123456768567868756756757575675657567567567.77434))  # True
# print(Str_PO.isComplex(0.23456))  # True
# print(Str_PO.isComplex(000000.23456))  # True
# print(Str_PO.isComplex(complex(1, 2)))  # True
# print(Str_PO.isComplex(complex("1")))  # True
# print(Str_PO.isComplex(complex("1+2j")))  # True
# print(Str_PO.isComplex(True))  # True
# print(Str_PO.isComplex(False))  # True
# print(Str_PO.isComplex("100"))  # True
# print(Str_PO.isComplex("1234.56768567868"))  # True
# print(Str_PO.isComplex("二"))  # False
# print(Str_PO.isComplex("123Abc"))  # False


# print('3.1，删除特殊字符"*<>?\\/|: '.center(100, "-"))
# print(Str_PO.delSpecialChar('"*<>?\\/|: 123'))  # 123

# print("3.2 浮点数四舍五入到整数位（取整）".center(100, "-"))
# print(Str_PO.roundInt(12.523))  # 13
# print(Str_PO.roundInt(13.523))  # 14

# # print("3.3 小数点最后位去0".center(100, "-"))
# print(Str_PO.subZero("1.00"))  # 1
# print(Str_PO.subZero("1.10"))  # 1.1
# print(Str_PO.subZero("0.0"))  # 0
# print(Str_PO.subZero(1.00))  # 1
# print(Str_PO.subZero(1.10))  # 1.1
# print(Str_PO.subZero(0.00))  # 0

# print("3.4 小数点后统一位数".center(100, "-"))
# list3 = [11.00, 22.00, 3.00, '4.0', '5.00000', '6.60']
# print(Str_PO.patchZero(list3))  # ['11.00', '22.00', '3.00', '4.00', '5.00', '6.00']
# print(Str_PO.patchZero(list3, 0))  # ['11', '22', '3', '4', '5', '6.6']
# print(Str_PO.patchZero(list3, 1))  # ['11.0', '22.0', '3.0', '4.0', '5.0', '6.6']


#
# print("4.1，字符串大写转小写".center(100, "-"))
# print([str(i).lower() for i in ['ADD', 'ANALYZEs']])  # ['add', 'analyzes']

# print("4.2 字符串反转".center(100, "-"))
# print("abc"[::-1])  # cba

# print("4.3 每个单词的第一个字母大写".center(100, "-"))
# print("my name is john".title())  # My Name Is John

# print("4.4 字符串查找唯一元素 ".center(100, "-"))
# print(''.join(set("aabbddcdswer")))  # awdebcsr
#
# print("4.5 重复打印字符串和列表n次".center(100, "-"))
# print('abc' * 3)  #abcabcabc
# print([1, 2, 3] * 3)  # [1, 2, 3, 1, 2, 3, 1, 2, 3]
#
# print("4.6 多个字符串组合为一个字符串".center(100, "-"))
# print(' '.join(['My', 'name', 'is', 'Chaitanya', 'Baweja']))  # My name is Chaitanya Baweja

# print("4.7 统计列表中元素的次数".center(100, "-"))
# from collections import Counter
# my_list = ['a','a','b','b','b','c','d','d','d','d','d']
# count = Counter(my_list)
# print(count['b'])  # 3
# print(count.most_common(1))  # [('d', 5)]  //统计最多的哪个元素及数量

