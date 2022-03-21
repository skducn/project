# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-19
# Description: Numpy_06_字符串处理（常用字符串函数详解）
# https://blog.csdn.net/baidu_41805096/article/details/108698046
# *****************************************************************

'''
1、连接两列表元素列值： np.char.add(L1,L2）
2、按元素进行多重连接： np.char.multiply(L1， i）
3、数组元素居中： np.char.center(a, width, fillchar=' '）
4、字符串首字母大写： np.char.capitalize(）
5、字符串每个单词首字母大写： np.char.title(）
6、字符串全部大写： np.char.upper(）
7、字符串全部小写： np.char.lower(）
8、按照指定字符分割字符串后再合并：np.char.join(）"
9、字符串切割 np.char.split()
10、字符串去除两侧空白 np.char.strip()
11、字符串替换 np.char.replace()
12、指定编码 np.char.encode()
13、解码 np.char.decode()
14、字符串查询 np.char.find()
15、判断字符串是否仅由中文汉字或者字母构成 np.char.isalpha()
16、统计字符串个数 np.char.count()
17、根据字符串前缀查找数据 np.char.startswith()
18、根据字符串后缀查找数据 np.char.endswith()
'''

import numpy as np


print("1、连接两列表元素列值： np.char.add(L1,L2）".center(100, "-"))
# 连接两列表元素列值， 条件，L1,L2 两个数组必须要有相同数量的元素，拼接时自动将数字转成字符串。

L1 = ['字符串', '中国']
L2 = ['连接', '万岁']
print(np.char.add(L1, L2))  # ['字符串连接' '中国万岁']

L1 = ['字符串', 4]
L2 = ['连接', '万岁']
print(np.char.add(L1, L2))  # ['字符串连接' '4万岁']

L1 = ['字符串', 4]
L2 = ['连接', 5]
print(np.char.add(L1, L2))  # ['字符串连接' '45']


print("2、按元素进行多重连接： np.char.multiply(L1，i）".center(100, "-"))
# (a * i),返回按a中每个元素分别*i倍的字符串多重连接的数组 ，注意数字自动转成字符串
L1 = ['中国', '人民']
print(np.char.multiply(L1, 2))  # ['中国中国' '人民人民']
L1 = ['中国', 5]
print(np.char.multiply(L1, 3))  # ['中国中国中国' '555']
print(np.char.multiply(L1, 0))  # ['' '']


print("3、数组元素居中： np.char.center(a, width, fillchar=' '）".center(100, "-"))
# 参数说明
# 1、a：元素为字符串类型的数组
# 2、width：指定字符串总长度
# 3、fillchar：默认空格，两边空格填补，也可指定填充字符
L1 = ['中国家庭', '人民']
print(np.char.center(L1, 10))  # ['   中国家庭   ' '    人民    ']
print(np.char.center(L1, 9))  # ['   中国家庭  ' '    人民   ']   //先满足左边填充
print(np.char.center(L1, 2))  # ['中国' '人民']   //截取多余的文字
print(np.char.center(L1, 1))  # ['中' '人']  //等同于 np.char.center(L1, 0)
print(np.char.center(L1, 10, fillchar='*'))  # ['***中国家庭***' '****人民****']


print("4、字符串首字母大写： np.char.capitalize(）".center(100, "-"))
# 数组a中每个元素的首字母大写
n2 = ['my heart will go on', "i'm your best freind"]
print(np.char.capitalize(n2))  # ['My heart will go on' "I'm your best freind"]



print("5、字符串每个单词首字母大写： np.char.title(）".center(100, "-"))
n2 = ['my heart will go on', "i'm your best freind"]
print(np.char.title(n2))  # ['My Heart Will Go On' "I'M Your Best Freind"]


print("6、字符串全部大写： np.char.upper(）".center(100, "-"))
n2 = ['abcd', "i'm your best freind"]
print(np.char.upper(n2))  # ['ABCD' "I'M YOUR BEST FREIND"]



print("7、字符串全部小写： np.char.lower(）".center(100, "-"))
n2 = ['abcd', "i'm your best freind"]
print(np.char.lower(n2))  # ['abcd' "i'm your best freind"]


print("8、按照指定字符分割字符串后再合并：np.char.join(）".center(100, "-"))
# 参数说明：
# np.char.join(sep1, seq2)
# sep1：分隔符序列
# seq2：字符串、数组序列
# 注意： sep1和seq2要么形状一致，要么符合广播机制
n1 = ['-', '^']
n2 = ['lili', 'bibi']
print(np.char.join(n1, n2))  # ['l-i-l-i' 'b^i^b^i']

n1 = ['-']
n2 = [['lili', 'nana'], ['taotao', 'alibaba']]
n33=np.char.join(n1, n2)
print(np.char.join(n1, n2))
# [['l-i-l-i' 'n-a-n-a']
 # ['t-a-o-t-a-o' 'a-l-i-b-a-b-a']]


print("9、字符串切割 np.char.split()".center(100, "-"))
# 参数说明：
# np.char.split(a, sep=None, maxsplit=None)
# a：字符串或数组
# sep：分隔符（若不指定，默认按空格切割）
# maxsplit：最大切片数

n4 = ['abcd', "i'm your best freind"]
print(np.char.split(n4))  # [list(['abcd']) list(["i'm", 'your', 'best', 'freind'])]
print(np.char.split(n4)[1][2])  # best

# maxsplit = 3,只切割三次，分成四份
print(np.char.split(n33, '-', maxsplit=3))
# [[list(['l', 'i', 'l', 'i']) list(['n', 'a', 'n', 'a'])]
 # [list(['t', 'a', 'o', 't-a-o']) list(['a', 'l', 'i', 'b-a-b-a'])]]
print(np.char.split(n33, '-', maxsplit=3)[1][1][3])  # b-a-b-a


print("10、字符串去除两侧空白 np.char.strip()".center(100, "-"))
# np.char.strip(a, chars=None)
# a：字符串或数组
# chars：要去除的字符串两侧的字符，不指定默认去除字符串两侧空格
# np.char.rstrip(a, chars=None) 去除字符串右侧空白字符或指定字符
# np.char.lstrip(a, chars=None) 去除字符串左侧空白字符或指定字符

n5 = ["    i'm your best freind    ", '   a b c    ']
print(np.char.strip(n5))  # ["i'm your best freind" 'a b c']
n6 = [ "*i'm your best freind **", ' a*b c*****']
# 指定要去除的字符串两侧的字符
print(np.char.strip(n6, chars='*'))  # ["i'm your best freind " ' a*b c']



print("11、字符串替换 np.char.replace()".center(100, "-"))
# np.char.replace(a, old, new, count=None)
# a：字符串或数组
# old：原字符串
# new：新字符串
# count：每个元素中的指定字符的替换次数

n7 = [['茶益道茶庄','庄腾酒庄'],['度假山庄的庄的庄','庄什么庄']]
print(np.char.replace(n7, '庄', 'duang'))
# [['茶益道茶duang' 'duang腾酒duang']
#  ['度假山duang的duang的duang' 'duang什么duang']]

# 指定每个元素仅替换一次
print(np.char.replace(n7,'庄','duang',count=1))
# [['茶益道茶duang' 'duang腾酒庄']
#  ['度假山duang的庄的庄' 'duang什么庄']]



print("12、指定编码 np.char.encode()".center(100, "-"))
# np.char.encode(a, encoding=None, errors=None)
# a：数组
# encoding：编码格式
# errors：指定如何处理编码错误

a = ['我', '可爱']
b = np.char.encode(a)
print(b)  # [b'\xe6\x88\x91' b'\xe5\x8f\xaf\xe7\x88\xb1']



print("13、解码 np.char.decode()".center(100, "-"))
print(np.char.decode(b))  # ['我' '可爱']



print("14、字符串查询 np.char.find()".center(100, "-"))
# np.char.find(a, sub, start=0, end=None)
# a：数组
# sub：查找的字符串
# 查找数组中每个元素是否包含指定字符，
# 若存在，返回在元素中的索引；若不存在，返回-1
n7 = [['茶益道茶庄','度假酒店','庄什么庄']]

# 第二个元素中没有要查找的字符，返回-1
print(np.char.find(n7, '庄'))  # [[ 4 -1  0]]



print("15、判断字符串是否仅由中文汉字或者字母构成 np.char.isalpha()".center(100, "-"))
# np.char.isalpha(a)
# a：数组，如果数组中的元素仅由中文汉字或英文字母构成，返回True;
#          否则返回False
#
# 返回布尔值
a = ['abc12','man','我们','wo们','wo们*']
print(np.char.isalpha(a))  # [False  True  True  True False]



print("16、统计字符串个数 np.char.count()".center(100, "-"))
# np.char.count(a, sub, start=0, end=None)
# a：数组
# sub：要查找的字符串

a = [['茶益道茶庄', '度假酒店', '庄什么庄']]
print(np.char.count(a,'庄'))  # [[1 0 2]]


print("17、根据字符串前缀查找数据 np.char.startswith()".center(100, "-"))
# np.char.startswith(a, prefix, start=0, end=None)
# a：数组
# prefix：前缀
# 返回布尔值
a = [['茶道茶庄', '茶茶酒店', '庄什么庄']]
print(np.char.startswith(a, '茶道'))  # [[ True False False]]


print("18、根据字符串后缀查找数据 np.char.endswith()".center(100, "-"))
# np.char.endswith(a, suffix, start=0, end=None)
# a：数组
# suffix：后缀
# 返回布尔值
a = [['茶道茶庄', '茶茶酒店', '庄什么庄']]
print(np.char.endswith(a, '庄'))  # [[ True False  True]]



