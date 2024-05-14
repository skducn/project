# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 列表（list）是一个有序的、可重复的、可变的元素序列，用[]表示。
# 列表的元素是有序的
# 列表的元素是可重复的
# 列表的元素是可变的
# 列表的元素支持索引、切片、嵌套
# *******************************************************************

'''
列表内置函数 ，查看方法：dir(list)

1，list.append(object) 将对象追加到列表的末尾。
2，list.clear() 清空列表中的所有元素
3，list.copy() （浅拷贝：只拷一层）
4，list.count() 统计某一个成员在列表中的出现次数
5，list.extend(iterable) 从可迭代对象(iterable)添加元素来扩展列表，支持列表、字符串，但不支持数字。
6，list.index(object,start,stop)->int  表示object在第start-1个到第stop-1个位置第一次出现的索引值,返回一个整数索引值。如果该值不存在则报错。
7，list.insert(object)  在索引之前插入对象
8，list.pop(index)->object 删除并返回索引项(最后默认)。如果列表为空或索引超出范围，将引发IndexError。
9，list.remove(object) 删除值的第一次出现。如果该值不存在，将引发ValueError。
10，del list() 删除列表
11，list.reverse() 翻转列表
12，list.sort(key[,reverse=True]) 升序排序 ，如果reverse=True则是降序排列

13.1，合并、可复制、成员操作符"
13.2，切片
'''


# print("1，list.append(object)".center(100, "-"))
# # 功能：向列表中添加成员，每次只能在列表尾添加一个成员，在使用前列表必须存在，如预先定义一个空列表。
# # 原地修改列表，且没有返回值，不能赋值给某个变量
# # append 将参数视为 element，作为追加一个元素拼接（整体追加）
# list1 = []
# list1.append('1')
# print(id(list1))  # 2637392327616
# list1.append(55)
# print(id(list1))  # 2637392327616
# list1.append(['john', '1', 1])
# print(id(list1))  # 2637392327616
# list1.append((1,2,3))
# list1.append({1:"a"})
# print(list1)  # ['1', 55, ['john', '1', 1]]
#
#
# print("2，list.clear()".center(100, "-"))
# # 功能：清空列表中的所有元素
# list2 = [123,456,789]
# list2.clear()
# print(list2)  # []
#
#
# print("3，list.copy()".center(100, "-"))
# # 功能：浅拷贝（拷贝父对象，引用子对象）
# import copy
# a = [1, 2, 3, 4, ['a', 'b'], (1,), {"a": 123}]
# b = a  # 赋值引用
# c = copy.copy(a)  # 浅拷贝  = list.copy()
# d = copy.deepcopy(a)  # 深拷贝
# a.append(5)  # 修改对象a
# # a[4] = ['z','y']
# a[4].append('c')  # 修改对象a中的['a', 'b']数组对象
# print('a = ', a)  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
# print('b = ', b)  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
# print('c = ', c)  # [1, 2, 3, 4, ['a', 'b', 'c']]
# print('d = ', d)  # [1, 2, 3, 4, ['a', 'b']]
#
#
# print("4，list.count()".center(100, "-"))
# # 功能：统计某一个成员在列表中的出现次数
# list4 = [1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8]
# print(list4.count(2))  # 4  //统计列表中2出现的次数。
#
#
# print("5，list.extend(iterable)".center(100, "-"))
# # 功能：该方法也是向列表中添加成员，并且也是一个参数，但是它将拆分成员（如列表则拆分单个列表成员，字符串则拆分成字符）
# # iterable 不支持int类型的对象
# # 原地修改列表，且没有返回值，不能赋值给某个变量
# # extend 将参数视为 list，拼接两个列表（个体化扩编追加）
# list5 = [1, 2, 3]
# print(id(list5))
# list5.extend(['john', '1', 1])
# print(id(list5))  # 经过extend()方法进行扩容后，还是原来的ID地址，这就是列表的原地修改。
# print(list5)  # [1, 2, 3, 'john', '1', 1]
# list5.extend('love')    # list5.extend('love') 等效于 list[len(list5):]= 'love'
# # list5[len(list5):] = 'love'   # [1, 2, 3, 'john', '1', 1, 'l', 'o', 'v', 'e']
# print(list5)  # [1, 2, 3, 'john', '1', 1, 'l', 'o', 'v', 'e']
# # list5.extend(555) # TypeError: 'int' object is not iterable  //报错，不支持int类型的对象
# # list5.extend(100)    # TypeError: 'int' object is not iterable
#
#
# print("6，list.index()".center(100, "-"))
# # 功能：返回该元素的索引值
# list6 = [123, 456, 789, 7, 8, 456, 1, 2, 3, 456]
# print(list6.index(456))  # 1 ， 搜索区间从开始到最后，返回元素第一次出现的索引值。
# print(list6.index(456, 2))  # 5 , 搜索区间从第3个元素开始到最后，搜索456返回的索引号是5.
# print(list6.index(456, 2, 6))  # 5, 搜索区间从第3个元素开始到第6个为止，搜索456，返回的索引号是5.
#
#
# print("7，list.insert()".center(100, "-"))
# # 功能：在特定位置添加成员。两个参数，insert(m,member)，在索引为m(也就是第m+1的位置进行添加)，例如
# list7 = [123, 456, 789]
# list7.insert(1, 'love')  # 在第1个索引之前添加
# print(list7)  # [123, 'love', 456, 789]
# list7.insert(2, [1, 2, 3])
# print(list7)  # [123, 'love', [1, 2, 3], 456, 789]
# list7.insert(0, "太阳")
# print(list7)  # ['太阳', 123, 'love', [1, 2, 3], 456, 100, 789]
# list7.insert(-1, 100)  # 不存在，没有报语法错
#
#
# print("8，list.pop()".center(100, "-"))
# # 功能：获取元素并删除（先进后出）
# list8 = [11, 22, 33, 44, 55]
# print(list8.pop(1))  # 22
# print(list8)  # [11, 33, 44, 55]
# print(list8.pop())  # 55  //默认获取最后一个元素
# print(list8)  # [11, 33, 44]
# print(list8.pop(-1))  # 44  //如同上
# print(list8)  # [11, 33]
# print(list8.pop())  # 33
# print(list8.pop())  # 11
# # print(list8.pop()) # IndexError: pop from empty list   所以对pop操作要小心，建议异常判断或数量判断。
#
#
# print("9，list.remove()".center(100, "-"))
# # 功能：从左到右删除列表中第一个符合要求的元素
# # 注意：remove() 无返回值，默认None，当列表中有多个重复元素时，从左到右只删除第一个元素。
# list9 = [11, 22, 33, 22, 'abc', ['love', 3]]
# list9.remove(22)
# list9.remove(['love', 3])
# print(list9.remove('abc'))  # None
# print(list9)  # [11, 33, 22]
#
#
# print("10，del list()".center(100, "-"))
# # 功能：用索引号部分元素、内嵌列表元素、全部元素
# list10 = [11, 22, 33, 44, 55, 22, ["a", 100]]
# del list10[1]  # 通过索引号删除列表值
# print(list10)  # [11, 33, 44, 55, 22, ['a', 100]]
# del list10[-1][0]   # 删除 ["a", 100] 中的 "a"
# print(list10)  # [11, 33, 44, 55, 22, [100]]
# list10.append(list10.pop()[0])
# print(list10)  # [11, 33, 44, 55, 22, 100]
# del list10  # 删除列表
# # print(list9)  # NameError: name 'list9' is not defined
#
#
# print("11，list.reverse()".center(100, "-"))
# # 功能：就是将列表中的元素前后颠倒，不能print（list.reverse()）
# list11 = [123, 456, 789]
# list11.reverse()
# print(list11)  # [789, 456, 123]


print("12，list.sort()".center(100, "-"))
list12 = [4, 8, 2, 5, 77]
list12.sort()
print(list12)  # [2, 4, 5, 8, 77]
list12.sort(reverse=True)
print(list12)  # [77, 8, 5, 4, 2]


# 深入理解python中的排序sort ， https://www.jianshu.com/p/4dd8f1b44704
# 效率比较：  cmp < DSU < key

print("2.8，排序优先级以此为 level降序，start降序，time升序".center(100, "-"))
lst = [{'level': 19, 'star': 36, 'time': 1},
       {'level': 20, 'star': 40, 'time': 2},
       {'level': 20, 'star': 40, 'time': 3},
       {'level': 20, 'star': 40, 'time': 4},
       {'level': 20, 'star': 40, 'time': 5},
       {'level': 18, 'star': 40, 'time': 1}]

# 先按time排序
lst.sort(key=lambda k: (k.get('time', 0)))
print(lst)

# # [{'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}, {'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}]
#
# # # 再按照level和star降序
# # lst.sort(key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
# # print(lst)
# s = sorted(s, key=lambda k: (k.get('level', 0), k.get('star', 0)), reverse=True)
# print(s)
# # [{'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}, {'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}]
# # [{'level': 20, 'star': 40, 'time': 2}, {'level': 20, 'star': 40, 'time': 3}, {'level': 20, 'star': 40, 'time': 4}, {'level': 20, 'star': 40, 'time': 5}, {'level': 19, 'star': 36, 'time': 1}, {'level': 18, 'star': 40, 'time': 1}]
# #
# # for idx, r in enumerate(lst):
# #     print('idx[%d]\tlevel: %d\t star: %d\t time: %d\t' % (idx, r['level'], r['star'],r['time']))
# # # # idx[0]	level: 20	 star: 40	 time: 2
# # # # idx[1]	level: 20	 star: 40	 time: 3
# # # # idx[2]	level: 20	 star: 40	 time: 4
# # # # idx[3]	level: 20	 star: 40	 time: 5
# # # # idx[4]	level: 19	 star: 36	 time: 1
# # # # idx[5]	level: 18	 star: 40	 time: 1
# for idx, r in enumerate(s):
#     print('idx[%d]\tlevel: %d\t star: %d\t time: %d\t' % (idx, r['level'], r['star'],r['time']))
# #





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
# # 类与实例 K:
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













print("13.1，合并、可复制、成员操作符".center(100, "-"))
print([1, 2, 3] + [4, 5, 6])  # [1, 2, 3, 4, 5, 6]
print(['Hi'] * 4)  # ['Hi', 'Hi', 'Hi', 'Hi']
print(3 in [1, 2, 3])  # True

print("13.2，切片".center(100, "-"))
list13 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(list13[2])  # 3 ， 返回第3个元素，第一个从0开始算
print(list13[-2])  # 9 ， 返回倒数第2个元素，最后一个从-1开始算
print(list13[1:])  # [2, 3, 4, 5, 6, 7, 8, 9, 0], 返回从第2个到最后的列表
print(list13[1:3])  # [2, 3] , 返回从第2个到第3个元素的列表
print(list13[1:1])  # [] , 返回空列表
print(list13[1:2])  # [2] , 返回的是1个元素的列表
print(list13[1:2][0])  # 2 , 返回第2个元素
print(list13[1:3][1])  # 3
print(list13[1:-1])  # [2, 3, 4, 5, 6, 7, 8, 9], 返回从第2个到倒数第2个元素列表
print(list13[1:-1:1])  # [2, 3, 4, 5, 6, 7, 8, 9], 返回从第2个到倒数第2个元素列表，并间隔1取值（默认间隔就是1，所以和上面的一样）
print(list13[1:-1:2])  # [2, 4, 6, 8] , 回从第2个到倒数第2个元素列表，并间隔2取值
print(list13[3::])  # [4, 5, 6, 7, 8, 9, 0]， 从第4个元素开始到最后，并间隔1取值
print(list13[3::2])  # [4, 6, 8, 0]
print(list13[3::-1])  # [4, 3, 2, 1] , 如果最后每间隔是负数，先获取从切片第一个N个元素之前的所有元素，最后倒序隔1输出列表
print(list13[4::-2])  # [5, 3, 1], 如果最后每间隔是负数，先获取从切片第一个N个元素之前的所有元素，最后倒序隔2输出列表
print(list13[::2])  # [1, 3, 5, 7, 9] ， 所有数据，每间隔2取值
print(list13[5:2:-1])  # [6, 5, 4]， 如果最后每间隔是负数，先获取从切片第一个N元素之前的所有元素，最后倒序隔1输出列表
# ************************************************************************************************************************************



print("14，练习题1, 将列表[1, 2, 3, 4, 5, 6] 改为 [1, 200, 300, 5, 6]".center(100, "-"))
# 分析：被替换的元素是列表中连续的，用切片定位后替换
list14 = [1, 2, 3, 4, 5, 6]
print(list14[1:4])  # [2, 3, 4]
list14[1:4] = [200, 300]
print(list14)  # [1, 200, 300, 5, 6]


print("15，练习题2, 将列表[11, ['a', 100], 44, ['a', 300]] 改为  [11, 100, 44, 300]".center(100, "-"))
# 分析：被替换的元素是子列表中固定位置的一个数字，先遍历获取非整数的子列表，然后获取子列表中的数字，最后替换子列表
list15 = [11, ["a", 100], 44, ["a", 300]]
for x in range(len(list15)):
    # 如果是子列表
    if not isinstance(list15[x], int):
        list15.insert(x+1, list15[x][1])
        list15.remove(list15[x])
print(list15)  # [11, 100, 44, 300]


print("16，练习题3，将列表[11, ['a', 100], ['a', 'c', 300, 'b']] 改为  [11, 100, 300]".center(100, "-"))
list16 = [11, ["a", 100], ["a", "c", 300, "b"]]
a = 0
for x in range(len(list16)):
    if not isinstance(list16[x], int):
        for i in range(len(list16[x])):
            if isinstance(list16[x][i], int):
                a = list16[x][i]
        list16.insert(x+1, a)
        list16.remove(list16[x])
print(list16)  # [11, 100, 300]


print("17，练习题5,将列表[11, ['a', 100, 'b', 200]] 改为  [11, 300]".center(100, "-"))
list18 = [11, ["a", 100, "b", 200]]
a = 0
for x in range(len(list18)):
    if not isinstance(list18[x], int):
        for i in range(len(list18[x])):
            if isinstance(list18[x][i], int):
                a = a + list18[x][i]
        list18.insert(x+1, a)
        list18.remove(list18[x])
print(list18)  # [11, 300]

