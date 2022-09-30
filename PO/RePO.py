# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2017-10-26
# Description   : 正则表达式对象层，re模块
# Python正则表达式指南 https://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html
# 正则表达式元字符  http://www.runoob.com/regexp/regexp-metachar.html
# *********************************************************************
# 正则表达式中用“\”表示转义，而python中也用“\”表示转义，当遇到特殊字符需要转义时，你要花费心思到底需要几个“\”，所以为了避免这个情况，推荐使用原生字符串类型(raw string)来书写正则表达式。
# raw string 就是用'r'作为字符串的前缀，如 r"\n"：表示两个字符"\"和"n"，而不是换行符了，Python中写正则表达式时推荐使用这种形式。
# 注意：在操作写文件路径时，切记不能使用 raw string ，这里存在陷阱。
'''
re.match(),从字符串的起点开始做匹配，匹配成功，返回一个匹配的对象，否则返回None
m = re.match(r'hello', 'hello world!')
print(m.group())  # hello

re.search()，扫描整个字符串并返回第一个成功的匹配
re.findall()，在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。
re.split()，将一个字符串按照正则表达式匹配结果进行分割，返回列表类型。
re.finditer()，在字符串中找到正则表达式所匹配的所有子串，并把它么作为一个迭代器返回。
re.sub()，把字符串中所有匹配正则表达式的地方替换成新的字符串。
re.sub(pattern, repl, string[, count=0])
# print(re.sub("\s+", "?", text, count=2)  #  hello?111?world 1132 , 只匹配前2个

# # 找到RE匹配的所有子串，并将其用一个不同的字符串替换, count用于指定最多替换次数，不指定时全部替换。

re.compile(strPattern[,flag]) , 这个是Pattern类的工厂方法，用于将字符串形式的正则表达式编译为Pattern对象。
第二个参数flag是匹配模式，取值可以使用按位或运算符'|'表示同时生效，比如re.I | re.M。另外，你也可以在regex字符串中指定模式，比如re.compile('pattern', re.I | re.M)与re.compile('(?im)pattern')是等价的。
pattern = re.compile(r'hello')
match = pattern.match('hello world!')
print(match.group())

flag 标志如下：
re.I(re.IGNORECASE): 忽略大小写（括号内是完整写法）
M(MULTILINE): 多行模式，改变'^'和'$'的行为
S(DOTALL): 点任意匹配模式，改变'.'的行为
L(LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
U(UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
X(VERBOSE): 详细模式。这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释。以下两个正则表达式是等价的：
a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
b = re.compile(r"\d+\.\d*")
'''

import re

class RePO():

    def __init__(self):
        pass

    def subBlank(self, varText, toSub):
        # 将 varText 中空格匹配成 varRe
        return re.sub(r'\s', lambda m: '[' + m.group(0) + ']', varText, 0).replace("[ ]", toSub)
        # print(regex.sub(lambda m: '[' + m.group(0) + ']', varText))  # 将字符串中含有'oo'的单词用[]括起来 ， [JGood] is a handsome boy, he is [cool], clever, and so on...

    def split_list(self, varText, varRe, varMaxsplit):
        # maxsplit是分离的次数，maxsplit = 1 ， 分离一次，默认为0，不限制次数。
        return (re.split(varRe, varText, varMaxsplit, flags=re.IGNORECASE))

    def findall_list(self, varText, varRe):
        # 匹配 varRe，列表形式返回 匹配到的单词。
        return re.findall(varRe, varText)

    # def finditer(self, varText, varRe):
    #     # re.finditer(pattern, string, flags=0)
    #     # 匹配 varRe，并与 varParma 进行运算后返回一个列表。
    #     it = re.finditer(varRe, varText)
    #     for m in it:
    #         print(m.group()

    def purge(self):
        # 清空缓存中的正则表达式
        re.purge()

if __name__ == "__main__":

    Re_PO = RePO()

    print(Re_PO.subBlank("JGood is a handsome boy, he is cool, clever, and so on...", ""))   # 去掉字符串中的空格 JGoodisahandsomeboy,heiscool,clever,andsoon...
    print(Re_PO.split_list("JGood is a handsome boy, he is cool, clever, and so on...", r'\W+', 0)) # ['JGood', 'is', 'a', 'handsome', 'boy', 'he', 'is', 'cool', 'clever', 'and', 'so', 'on', '']
    print(Re_PO.split_list("JGood is a handsome boy, he is cool, clever, and so on...", r'(\W+)', 0))

    x = (Re_PO.split_list("0etrerta3B9", '[a-z]+', 0))  # ['0', '3', '9']




    print(Re_PO.findall_list("JGood is a handsome boy, he is cool, clever, and so on...", r'\w*oo\w*'))  # 匹配所有包含'oo'的单词 ， ['JGood', 'cool']
