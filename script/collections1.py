# coding: utf-8
# ***************************************************************
# Author     : John
# Date       : 2024-1-25
# Description: collections
# 参考：https://blog.csdn.net/peng78585/article/details/125387640
# 官网：https://docs.python.org/zh-cn/3/library/collections.html
# ***************************************************************

import collections, re
from collections import Counter

# 查看所有的子类，一共包含9个
print(collections.__all__)  # ['deque', 'defaultdict', 'namedtuple', 'UserDict', 'UserList', 'UserString', 'Counter', 'OrderedDict', 'ChainMap']
# namedtuple()	创建命名元组子类的工厂函数，生成可以使用名字来访问元素内容的tuple子类
# deque	类似列表(list)的容器，实现了在两端快速添加(append)和弹出(pop)
# ChainMap	类似字典(dict)的容器类，将多个映射集合到一个视图里面
# Counter	字典的子类，提供了可哈希对象的计数功能
# OrderedDict	字典的子类，保存了他们被添加的顺序，有序字典
# defaultdict	字典的子类，提供了一个工厂函数，为字典查询提供一个默认值
# UserDict	封装了字典对象，简化了字典子类化
# UserList	封装了列表对象，简化了列表子类化
# UserString	封装了字符串对象，简化了字符串子类化（中文版翻译有误）


# todo 计数器
# Counter是一个dict的子类，用于计数可哈希对象。
# 它是一个集合，元素像字典键(key)一样存储，它们的计数存储为值。
# 计数可以是任何整数值，包括0和负数。简单说，就是可以统计计数

# 计算top10的单词
text = 'remove an existing key one level down remove an existing key one level down'
words = re.findall("\w+", text)
w = Counter(words).most_common(10)
print(w)  # [('remove', 2), ('an', 2), ('existing', 2), ('key', 2), ('one', 2), ('level', 2), ('down', 2)]
print(w[0][0])  # remove
print(w[0][1])  # 2

# 计算单词个数
L = ['red', 'blue', 'red', 'green', 'blue', 'blue']
c = Counter(L)
print(c)  # Counter({'blue': 3, 'red': 2, 'green': 1})
print(c['red'])  # 2
print(c.most_common(2))  # [('blue', 3), ('red', 2)]  // 获取频率最高的2个单词及数量

# 字符串计数
print(Counter("gallah"))  # Counter({'a': 2, 'l': 2, 'g': 1, 'h': 1})

# 列表计数

print(Counter(['red', 'blue', 'red', 'green', 'blue', 'blue']))  # Counter({'blue': 3, 'red': 2, 'green': 1})

# 字典计数(什么鬼)
print(Counter(cats=4, dogs=8))  # Counter({'dogs': 8, 'cats': 4})
print(Counter(cats=4, dogs='8'))  # Counter({'cats': 4, 'dogs': '8'})

# 计数器对象除了字典方法以外，还提供了三个其他的方法：
# 1、elements()
# 描述：返回一个迭代器，其中每个元素将重复出现计数值所指定次。 元素会按首次出现的顺序返回。 如果一个元素的计数值小于1，elements() 将会忽略它。
c = Counter(R=4, b=2, c=0, d=-2)
print(c.elements())  # <itertools.chain object at 0x7f92af56e9a0>
print(list(c.elements()))  # ['R', 'R', 'R', 'R', 'b', 'b']
print(sorted(c.elements()))  # ['R', 'R', 'R', 'R', 'b', 'b']

# 2、most_common()
# 返回一个列表，其中包含n个最常见的元素及出现次数，按常见程度由高到低排序。
# 如果 n 被省略或为None，most_common() 将返回计数器中的所有元素，计数值相等的元素按首次出现的顺序排序，经常用来计算top词频的词语。
print(c.most_common())  # [('R', 4), ('b', 2), ('c', 0), ('d', -2)]
print(c.most_common(3))  # [('R', 4), ('b', 2), ('c', 0)]

# 3、subtract()
# 从迭代对象或映射对象减去元素。像dict.update() 但是是减去，而不是替换。输入和输出都可以是0或者负数。
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d)  # // c - d
print(c)  # Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})

# 数学操作
# 可以结合 Counter 对象，以生产 multisets (计数器中大于0的元素）。
# 加和减，结合计数器，通过加上或者减去元素的相应计数。交集和并集返回相应计数的最小或最大值。
# 每种操作都可以接受带符号的计数，但是输出会忽略掉结果为零或者小于零的计数。
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
print(c + d)  # Counter({'a': 4, 'b': 3})
print(c - d)  # Counter({'a': 2})
print(c & d)  # Counter({'a': 1, 'b': 1})  // 交集输出最小的值
print(c | d)  # Counter({'a': 3, 'b': 2}) // 并集输出最大的值

# 单目加和减，意思是从空计数器加或者减去。
c = Counter(a=2, b=4, c=-1, d=-33)
print(c)  # Counter({'b': 4, 'a': 2, 'c': -1, 'd': -33})
print(+c)  # Counter({'b': 4, 'a': 2})
print(-c)  # Counter({'d': 33, 'c': 1})


# todo 双向队列-deque
from collections import deque
d = deque('test')
d.append('kk')
print(d)  # deque(['t', 'e', 's', 't', 'kk'])
print(d[2])  # s
d.appendleft('a1')
print(d)  # deque(['a1', 't', 'e', 's', 't', 'kk'])

