# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-31
# Description: re --- 正则表达式操作
# 官方网：https://docs.python.org/zh-cn/3/library/re.html
# 参考：https://blog.csdn.net/qq_51182221/article/details/118650262
# https://blog.csdn.net/stcaaa/article/details/83864210
# Python之正则表达式细讲 https://xiaoshiyi.blog.csdn.net/article/details/129170115?spm=1001.2014.3001.5502
# re.findall():搜索所有满足条件的字符串
# re.match():从第一个字符开始匹配模式
# re.search():搜索第一个满足条件的字符串，查找到第一个停止
# re.sub():替换满足条件的字符串
# re.compile() 该函数根据包含的正则表达式的字符串创建模式对象

#***************************************************************

import re
import sys
# todo split 替换方法
r = re.split(r' - |,', '张三 - 李四,      王武 - 赵六')  # ['张三', '李四', '      王武', '赵六']
print(r)




sys.exit()


# 函数式用法：一次性操作
# 分析：要求获取连续的6个数字，[0-4]表示第一个字符在0-4数字之间，\d{5}表示连续5个数字
rst = re.search(r'[0-4]\d{5}', '3BIT500081456 12345678')   # 000814
print(rst.group(0))  # 000814

rst2 = re.findall(r'[0-4]\d{5}', '3BIT50008145672345678')
print(rst2)  # ['000814', '234567']

# 面向对象用法：编译后的多次操作
pat = re.compile(r'[1-9]\d{5}')#先写一个pat对象
rst = pat.search('BIT 3BIT50008145672345678')
print(rst)  # <re.Match object; span=(8, 14), match='500081'>
print(rst.group())  # 500081
rst = pat.findall('BIT 3BIT50008145672345678')
print(rst)  # ['500081', '456723']
# print(rst.group())  # 100081

some_text = 'a,b,,, ,c  d'
# 分析：[]匹配任意单个字符, (逗号后有空格)，表示匹配逗号和空格， + 表示前一个字符1次或无限次扩展，即1个或多个逗号或1个或多个空格
a = re.compile('[, ]+')
print(a)
b = a.search(some_text)
print(b)  # <re.Match object; span=(1, 2), match=','>
print(b.group())  # ,
c = a.findall(some_text)
print(c)
print(a.split(some_text)) # ['a', 'b', 'c', 'd']
print(re.compile('[ ]+').split('a b c  d'))  # ['a', 'b', 'c', 'd']
print(re.compile('[, ]+').split('a,b,c ,,,,, d'))  # ['a', 'b', 'c', 'd']



# # Re库默认情况下为贪婪匹配，输出匹配最长的子串 ,   .*表示任意单个字符的无限多
# match = re.search(r'PY.*N', 'PYANBNCNDNEN')
# print(match.group(0))  # PYANBNCNDNEN
#
# # 这是若想输出最小匹配，就改成以下形式：  .*?表示任意单个字符的1次, 等同于 .+?  .??  .{1,1}?
# match = re.search(r'PY.*?N','PYANBNCNDNEN')
# print(match.group(0))  # PYAN
#
# match = re.search(r'PY.{1,1}?N','PYANBNCNDNEN')
# print(match.group(0))  # PYAN


#查找所有包含'oo'的单词
# 分析：\w单词字符
text = "JGood is a handsooome boy, he is cool, oo clever, and so on..."
a = re.findall(r'\w*oo\w*', text)
print(a)  # ['JGood', 'cool']



string="a   b  c  d"

#带括号与不带括号的区别
# 分析：\w单词 \s空白字符 \w单词
regex=re.compile("((\w+)\s+\w+)")  # 先完成最外一层括号得到 'a   b' ， 再对内层括号得到'a' 并组成元祖。
print(regex.findall(string))  # [('a   b', 'a'), ('c  d', 'c')]

regex=re.compile("(\w+\s+(\w+))")
print(regex.findall(string))  # [('a   b', 'b'), ('c  d', 'd')]

regex1=re.compile("(\w+)\s+\w+")  # 匹配\w单词 \s空白字符 \w单词，但最后只输出带括号 (\w+)的值。
print(regex1.findall(string))  # ['a', 'c']

regex1=re.compile("\w+[,]+(\w+)")  # 匹配\w单词 \s空白字符 \w单词，但最后只输出带括号 (\w+)的值。
print(regex1.findall("a,b,c,d"))  # ['b', 'd']

regex2=re.compile("\w+[,]+\w+")  # 匹配\w单词 \s空白字符 \w单词 ， 分别两组
print(regex2.findall("a,b,c,d"))  # ['a,b', 'c,d']


s="我是一个人((((中国人)aaa[真的]bbbb{确定}"
a = re.sub("\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
print(a)
#我是一个人aaabbbb


# $，匹配一个字符串的结尾或者字符串最后面的换行符
print(re.findall('(foo.$)', 'foo1\nfoo2\n'))  # ['foo2']  //匹配任意一行的行尾
print(re.findall('(foo.$)', 'foo1\nfoo2\n', re.MULTILINE))  # ['foo1', 'foo2']
print(re.findall('(?m)(foo.$)', 'foo1\nfoo2\n'))  # ['foo1', 'foo2']  //同上，注意(?x)标志如果有的话，要放在最前面。
print(re.findall('($)', 'foo1foo2'))  # ['']  // 一个是字符串的结尾
print(re.findall('($)', 'foo1foo2\n'))  # ['', '']  //一个是最后的换行符，一个是字符串的结尾

# re.I(忽略大小写)、re.L(依赖locale)、re.M(多行模式)、re.S(.匹配所有字符)、re.U(依赖Unicode)、re.X(详细模式)


# m=re.match('(?P[a-zA-Z_]\w*)', 'abc=123')
# print(m.group('var'))

# (?<=…) 后顾断言，只有当当前位置之前的字符串匹配
# 分析：获取 - 后面的字符
m = re.search('(?<=-)\w+', 'spam-egg')
# print(m.group(0))  # egg

m = re.findall('(?<=-)\w+', 'spam-egg hello-test')
print(m)  # ['egg', 'test']


# (?<!..) 同理，这个叫做“反后顾断言”
m = re.findall('(?<!-)\w+', 'spam-egg hello-test')
print(m)  # ['spam', 'gg', 'hello', 'est']


# 和findall()类似，但返回的是MatchObject的实例的迭代器。
for m in re.finditer('(\d+).(\d+).(\d+).(\d+)', 'My IP is 192.168.0.2, and your is 192.168.0.3.'):
    print(m.group())
    # 192.168.0.2
    # 192.168.0.3


print(re.sub('x*', '-', 'abcxxd'))  # -a-b-c--d-
print(re.sub('x+', '-', 'abcxxd'))  # abc-d
print(re.sub('x+', '-', 'abcxxxxxxd'))  # abc-d
print(re.sub('x?', '-', 'abcxxd'))  # -a-b-c---d-

x = re.sub('-{1,2}', "A", 'pro----gram-files')
print(x)


# 如果repl是个函数，每次pattern被匹配到的时候，都会被调用一次，传入一个匹配到的MatchObject对象，需要返回一个字符串，在匹配到的位置，就填入返回的字符串。
def f1(matchobj):
    if matchobj.group(0) == '-':
        print(matchobj.group(0))
        return ''
    else:
        print(matchobj.group(0))  # ---
        return 'A'

x = re.sub('-{1,3}', f1, 'pro----gram-files')
print(x)  # proAgramfiles



x = re.sub('-(\d+)-', '-\g<1>0\g<0>', 'a-11-b-22-c')
print(x)  # a-110-11-b-220-22-c

# todo 跟上面的sub()函数一样，只是它返回的是一个元组 (新字符串, 匹配到的次数)
x = re.subn('-(\d+)-', '-\g<1>0\g<0>', 'a-11-b-22-c')
print(x)  # ('a-110-11-b-220-22-c', 2)


# 正则对象由re.compile()返回。它有如下的属性和方法。
# match(string[, pos[, endpos]])
pattern = re.compile('o')
print(pattern.match('dog')) # 开始位置不是o，所以不匹配  None
print(pattern.match('dog', 1)) # 第二个字符是o，所以匹配  <re.Match object; span=(1, 2), match='o'>


# （\g<1>表示查找到的第1个括号内的文本，\g<2>表示第2个括号）
m = re.match('a=(\d+)b=(\d+)', 'a=100b=444')
print(m.expand('above a is \g<1>'))  # above a is 100
print(m.expand('above b is \g<2>'))  # above b is 444
print(m.expand(r'above a is \1'))  # above a is 100

m = re.match(r"(\w+) (\w+)", 'Isaac Newton, physicist')
print(m.group(0))  # Isaac Newton  //整个匹配
print(m.group(1))  # Isaac  //第一个子串
print(m.group(2)) # Newton  //第二个子串
print(m.group(1, 2))  # ('Isaac', 'Newton')


# 用(?P…)这种语法命名过的子串的话，相应的groupN也可以是名字字符串
m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", 'Malcolm Reynolds')
print(m.group('first_name'))  # Malcolm
print(m.groupdict()) # {'first_name': 'Malcolm', 'last_name': 'Reynolds'}


m = re.match(r"(\d+).(\d+)", '24.1632')
# m = re.search(r"(\d+).(\d+)", '24.1632')
print(m.groups())  # ('24', '1632')
print(m.groups(0))  # ('24', '1632')
m = re.match(r"(\d+).?(\d+)?", '24')
print(m.groups())  # ('24', None)
print(m.groups('0'))  # ('24', '0')

print(re.findall(r"(\d+).(\d+)", '24.1632'))  # [('24', '1632')]

# m = re.match(r"(…)+", 'a1b2c3') # 匹配到3次
# print(m.group(1)) # 返回的是最后一次

# todo 把email地址里的“remove_this”去掉的例子 , 只去掉一次。
email = 'tony@tiremove_thisger.net'
m = re.search('remove_this', email)
print(email[:m.start()] + email[m.end():])  # tony@tiger.net