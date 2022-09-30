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

re.sub() 把字符串中所有匹配正则表达式的地方替换成新的字符串。
re.sub(pattern, repl, string, count=0, flags=0)
# pattern：正则中的模式字符串；
# repl：要替换的字符串（即匹配到pattern后替换为repl），也可以是个函数；
# string：原始字符串；
# count：可选参数，表示要替换的最大次数，而且必须是非负整数，该参数默认为0，即所有的匹配都会替换；
# flags：可选参数，表示编译时用的匹配模式（如忽略大小写、多行模式等），数字形式，默认为0。
# # 找到RE匹配的所有子串，并将其用一个不同的字符串替换, count用于指定最多替换次数，不指定时全部替换。


re.match(),从字符串的起点开始做匹配，匹配成功，返回一个匹配的对象，否则返回None
m = re.match(r'hello', 'hello world!')
print(m.group())  # hello

re.search()，扫描整个字符串并返回第一个成功的匹配
re.findall()，在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表。
re.split()，将一个字符串按照正则表达式匹配结果进行分割，返回列表类型。
re.finditer()，在字符串中找到正则表达式所匹配的所有子串，并把它么作为一个迭代器返回。


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


    def purge(self):
        # 清空缓存中的正则表达式
        re.purge()

if __name__ == "__main__":

    Re_PO = RePO()


    # 匹配所有包含'oo'的单词
    print(re.findall(r'\w*oo\w*', "JGood is a handsome boy, he is cool, clever, and so on..."))  #  ['JGood', 'cool']


    # 去掉空格
    print(re.sub(r"\s", "", "hello 111 world"))  #  hello111world

    # 数字替换成*
    print(re.sub(r'[0-9]', "*", "44799217,,,###,,535646343@qq.com. Today is 2021/12/21"))  # ********,,,###,,*********@qq.com. Today is ****/**/**


    # 字符串分割成列表
    print(re.split(r'\W+', "JGood is a ,  so on..+——.", 0, flags=re.IGNORECASE))  # ['JGood', 'is', 'a', 'so', 'on', '']
    print(re.split(r'(\W+)', "JGood is a ,  so on..+——.", 0, flags=re.IGNORECASE))  # ['JGood', ' ', 'is', ' ', 'a', ' ,  ', 'so', ' ', 'on', '..+——.', '']
    print(re.split(r'[a-zA-Z]?', "0etrerta3B9"))  # ['', '0', '', '', '', '', '', '', '', '3', '', '9', '']

    randstr = "Here is Edureka as Edureka"
    res = (re.search(r"Edureka", randstr))
    print(res)   # <re.Match object; span=(8, 15), match='Edureka'>
    print(res.group())  # Edureka
    print(res.start())  # 8
    print(res.end())  # 15
    print(res.span())  # (8, 15)
    print(res.string)  # "Here is Edureka"

    pat = re.compile("[0-9]")
    res = pat.search("abcd23ef4gh")
    print(res)  # <re.Match object; span=(4, 5), match='2'>

    str = 'response body:{"name":"张三","age":20,"Idcard_no":"4100058971","phone":"15011100001"}'
    # 开始匹配
    res = re.search("{.*?}", str)  # 万能的.*?
    print(res.group())  # {"name":"张三","age":20,"Idcard_no":"4100058971","phone":"15011100001"}
