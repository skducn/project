# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-31
# Description: re --- 正则表达式操作
# 官方网：https://docs.python.org/zh-cn/3/library/re.html
# 参考：https://blog.csdn.net/qq_51182221/article/details/118650262
#***************************************************************

import re

# 函数式用法：一次性操作
rst = re.search(r'[1-9]\d{5}', 'BIT 400081456')
print(rst.group(0))

# 面向对象用法：编译后的多次操作
pat = re.compile(r'[1-9]\d{5}')#先写一个pat对象
rst = pat.search('BIT 100081')
print(rst)

# Re库默认情况下为贪婪匹配，输出匹配最长的子串 ,   .*表示任意单个字符的无限多
match = re.search(r'PY.*N', 'PYANBNCNDNEN')
print(match.group(0))  # PYANBNCNDNEN

# 这是若想输出最小匹配，就改成以下形式：  .*?表示任意单个字符的1次, 等同于 .+?  .??  .{1,1}?
match = re.search(r'PY.*?N','PYANBNCNDNEN')
print(match.group(0))  # PYAN

match = re.search(r'PY.{1,1}?N','PYANBNCNDNEN')
print(match.group(0))  # PYAN
