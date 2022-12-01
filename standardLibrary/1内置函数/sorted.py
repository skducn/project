# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: sorted(iterable, *, key=None, reverse=False)
# 定义：根据 iterable 中的项返回一个新的已排序列表。（即不会影响原值）
# 升序排序规则是 空格，特殊字符，大写字母，小写字母，中文

# 深入理解python中的排序sort ， https://www.jianshu.com/p/4dd8f1b44704
# 效率比较：  cmp < DSU < key

# todo sorted与 list.sort()区别
# 1，sorted() 不改变原值返回排序后新列表，而list.sort() 改变原值且没有返回值。
# 2，sorted() 可接受任何可迭代对象它是通用方法，而list.sort()只可迭代列表对象它是列表的方法。

# todo 参数key的用法
# 规则：key的值可以是一个函数，将函数结果返回给key，然后对key进行排序，最后输出排序后的原值。
# 用途：一般用于复杂对象属性的排列， 如 "This is a App andrew".split() 对每个单词首字母顺序排列（不区分大小写）；
# 如 对list1列表中嵌套元组元素中最后一个的值进行排序 list1 = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
# operator库函数( itemgetter(), attrgetter())自定义排序，这种方法更好理解并且效率更高, from operator import itemgetter, attrgetter


# 标准库：https://docs.python.org/zh-cn/3.7/library/functions.html#sorted
# ********************************************************************************************************************

from operator import itemgetter, attrgetter


print("1，基本排序".center(100, "-"))
print(sorted({2: 200, 1: 100, 33: 300, 4: 400}))  # [1, 2, 4, 33]  //数据是字典时，只输出排序后的key
print(sorted([2, 5, 3, 77, 6]))  # [2, 3, 5, 6, 77]  // 数据时列表
print(sorted(("g", "a", "c")))  # ['a', 'c', 'g']  // 数据是元组
print(sorted("Mye is S。.kn"))  # [' ', ' ', '.', 'M', 'S', 'e', 'i', 'k', 'n', 's', 'y', '。']  // 数据是字符串，字符打散后，排序规则是 空格，特殊字符，大写字母，小写字母，中文
print(sorted("This is a App andrew".split()))  # ['App', 'This', 'a', 'andrew', 'is']  // 数据是字符串，按照split规则打散后排序，排序规则是 空格，特殊字符，大写字母，小写字母，中文


print("2.1，key，对字符串中每个单词首字母（不区分大小写）顺序排序，输出每个单词".center(100, "-"))
print(sorted("This is a App andrew".split(), key=str.lower))  # ['a', 'andrew', 'App', 'is', 'This']  //每个单词从a - z 排序，输出原值
print(sorted("This is a App andrew".split(), key=str.upper))  # ['a', 'andrew', 'App', 'is', 'This']  //每个单词从A - Z 排序，输出原值
print(sorted("This is a App andrew".split(), key=str.lower, reverse=True))  # ['This', 'is', 'App', 'andrew', 'a']  // 降序


print("2.2，key，对list1列表中嵌套元组中第三个元素进行排序".center(100, "-"))
list1 = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
print(sorted(list1, key=lambda list1: list1[2]))  # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]


print("2.3，key，对类中对象中age元素进行排序".center(100, "-"))
class Student:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    def __repr__(self):
        return repr((self.name, self.grade, self.age))
student_objects = [
    Student('john', 'A', 25),
    Student('jane', 'B', 22),
    Student('dave', 'B', 20)]
print(sorted(student_objects, key=lambda student: student.age))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]


print("2.4，key，姓名与成绩分开存储，对指定的姓名进行排序，忽略不存在的姓名。".center(100, "-"))
name = ['dave', 'john', 'YOYO']
score = {'john': 'C', 'YOYO' : 'A', 'dave': 'B', 'steven': 'F'}
print(sorted(name, key=score.__getitem__))  # ['YOYO', 'dave', 'john']


print("2.5，operator库函数自定义排序".center(100, "-"))
list1 = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
print(sorted(list1, key=itemgetter(2)))  # [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
print(sorted(student_objects, key=attrgetter('age')))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]

print("2.6，operator，多个排序，先对第一关键字排序，在对第二关键字排序".center(100, "-"))
print(sorted(list1, key=itemgetter(1, 2)))  # [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]
print(sorted(student_objects, key=attrgetter('grade', 'age')))  # [('john', 'A', 25), ('dave', 'B', 20), ('jane', 'B', 22)]
print(sorted(list1, key=itemgetter(2), reverse=True))  # [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)] 对年龄进行降序


print("2.7，operator，排序稳定，对相同key值的多个记录进行排序之后，原始的前后关系保持不变".center(100, "-"))
list2 = [('red', 199), ('blue', 122), ('red', 2), ('blue', 2)]
print(sorted(list2, key=itemgetter(0)))  # [('blue', 122), ('blue', 2), ('red', 199), ('red', 2)]

s = sorted(student_objects, key=attrgetter('age'))
print(sorted(s, key=attrgetter('grade'), reverse=True))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]
# 结果同上
s = sorted(student_objects, key=attrgetter('grade'), reverse=True)
print(sorted(s, key=attrgetter('age')))  # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]


print("2.8，排序优先级以此为 level降序，start降序，time升序".center(100, "-"))
lst = [{'level': 19, 'star': 36, 'time': 1},
       {'level': 20, 'star': 40, 'time': 2},
       {'level': 20, 'star': 40, 'time': 3},
       {'level': 20, 'star': 40, 'time': 4},
       {'level': 20, 'star': 40, 'time': 5},
       {'level': 18, 'star': 40, 'time': 1}]

# # 先按time排序
# lst.sort(key=lambda k: (k.get('time', 0)))
# print(lst)
s = sorted(lst, key=lambda k: (k.get('time', 0)))
print(s)
# [{'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}, {'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}]
# [{'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}, {'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}]

# # 再按照level和star降序
# lst.sort(key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
# print(lst)
s = sorted(s, key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
print(s)
# [{'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}, {'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}]
# [{'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}, {'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}]
#
# for idx, r in enumerate(lst):
#     print('idx[%d]\tlevel: %d\t star: %d\t time: %d\t' % (idx, r['level'], r['star'],r['time']))
# # # idx[0]	level: 20	 star: 40	 time: 2
# # # idx[1]	level: 20	 star: 40	 time: 3
# # # idx[2]	level: 20	 star: 40	 time: 4
# # # idx[3]	level: 20	 star: 40	 time: 5
# # # idx[4]	level: 19	 star: 36	 time: 1
# # # idx[5]	level: 18	 star: 40	 time: 1
for idx, r in enumerate(s):
    print('idx[%d]\tlevel: %d\t star: %d\t time: %d\t' % (idx, r['level'], r['star'],r['time']))
#





# 传统的 DSU(Decorate-Sort-Undecorate)的排序方法 *******************************************************************************888
# # Decorate，给list添加一个新的值，这个值一般是用来控制排序的顺序
# # sort，排序
# # Undecorate，将添加的值去掉。
# decorated = [(student.grade, i, student) for i, student in enumerate(student_objects)]
# decorated.sort()
# print([student for grade, i, student in decorated])  # undecorate
# # [('john', 'A', 25), ('jane', 'B', 22), ('dave', 'B', 20)]
#
# # 实例
# L = [('b', 2), ('a', 1), ('c', 7), ('d',4)]
# A = [(x[0], i, x) for i, x in enumerate(L)]  # X[0] 表示对第一关键字升序
# A.sort()
# L = [s[2] for s in A]
# print(L)  # [('a', 1), ('b', 2), ('c', 7), ('d', 4)]
# L = [s[0] for s in A]
# print(L)  # ['a', 'b', 'c', 'd']
#
# L = [('b', 2), ('a', 1), ('c', 7), ('d',4)]
# A = [(x[1], i, x) for i, x in enumerate(L)]  # X[0] 表示对第2关键字升序
# A.sort()
# L = [s[2] for s in A]
# print(L)  # [('a', 1), ('b', 2), ('d', 4), ('c', 7)]
# L = [s[0] for s in A]
# print(L)  # [1, 2, 4, 7]
#
# # 因为元组是按字典序比较的，比较完grade之后，会继续比较i。
# # 添加index的i值不是必须的，但是添加i值有以下好处：
# # 可以保证排序的稳定性，如果key值相同，就可以利用i来维持原有的顺序
# # 原始对象的item不用进行比较，因为通过key和i的比较就能将数组排序好
# # 现在python3提供了key-function，所以DSU方法已经不常用了
#
#
# # 6，利用cmp方法进行排序的原始方式
# # python2.x版本中，是利用cmp参数自定义排序。
# # python3.x已经将这个方法移除了，但是我们还是有必要了解一下cmp参数
# # cmp参数的使用方法就是指定一个函数，自定义排序的规则，和java等其他语言很类似
# from functools import cmp_to_key
# L = [2, 3, 1, 4]
# L.sort(reverse=True)  # 降序
# print(L)  # [4,3,2,1]
# L.sort(key=cmp_to_key(lambda a, b: b-a))  # 降序
# print(L)  # [4,3,2,1]
# L.sort(key=cmp_to_key(lambda a, b: a-b))  # 升序
# print(L)  # [1,2,3,4]
#
# # >>> def numeric_compare(x, y):
# # ... return x - y
# # >>> sorted([5, 2, 4, 1, 3], cmp=numeric_compare)
# # [1, 2, 3, 4, 5]
# # 也可以反序排列
# #
# # >>> def reverse_numeric(x, y):
# # ... return y - x
# # >>> sorted([5, 2, 4, 1, 3], cmp=reverse_numeric)
# # [5, 4, 3, 2, 1]
# # python3.x中可以用如下方式：
# #
# # def cmp_to_key(mycmp):
# # 'Convert a cmp= function into a key= function'
# # class K:
# # def __init__(self, obj, *args):
# # self.obj = obj
# # def __lt__(self, other):
# # return mycmp(self.obj, other.obj) < 0
# # def __gt__(self, other):
# # return mycmp(self.obj, other.obj) > 0
# # def __eq__(self, other):
# # return mycmp(self.obj, other.obj) == 0
# # def __le__(self, other):
# # return mycmp(self.obj, other.obj) <= 0
# # def __ge__(self, other):
# # return mycmp(self.obj, other.obj) >= 0
# # def __ne__(self, other):
# # return mycmp(self.obj, other.obj) != 0
# # return K
# # >>> sorted([5, 2, 4, 1, 3], key=cmp_to_key(reverse_numeric))
# # [5, 4, 3, 2, 1]
#
#
# # 7，__It__函数来指定两个对象比较的方式
# Student.__lt__ = lambda self, other: self.age < other.age
# print(sorted(student_objects)) # [('dave', 'B', 20), ('jane', 'B', 22), ('john', 'A', 25)]
#
#
#
#
#
#
#



