# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 列表使用方法 common - list1.py
# list，实际上是列表类型的构造函数，列表可变且序可迭代。
# class list([iterable])
# Rather than being a function, list is actually a mutable sequence type, as documented in Lists and Sequence Types — list, tuple, range
# *******************************************************************
'''
列表内置函数 ，查看方法：dir(list)
1、list.append(object) 将对象追加到列表的末尾。
2、list.clear() 清空列表中的所有元素
3、list.copy() （浅拷贝：只拷一层）
4、list.count() 统计某一个成员在列表中的出现次数
5、list.extend(iterable) 从可迭代对象(iterable)添加元素来扩展列表，支持列表、字符串，但不支持数字。
6、list.index(object,start,stop)->int  表示object在第start-1个到第stop-1个位置第一次出现的索引值,返回一个整数索引值。如果该值不存在则报错。
7、list.insert(object)  在索引之前插入对象
8、list.pop(index)->object 删除并返回索引项(最后默认)。如果列表为空或索引超出范围，将引发IndexError。
9、list.remove(object) 删除值的第一次出现。如果该值不存在，将引发ValueError。
10、list.reverse() 翻转列表
11、list.sort(key[,reverse=True]) 升序排序 ，如果reverse=True则是降序排列
'''

# 1，append(object)：向列表中添加成员，一个参数
# 注意1，它每次只能在列表尾添加一个成员。
# 注意2，它使用前列表必须存在，如预先定义一个空列表
# 注意3，它 与 extend(iterable)的区别，前者将参数只作为一个成员，后者将拆分成员。
list1 = []
list1.append('1')
list1.append(55)
list1.append(['john','1',1])
print(list1) # ['1', ['john', '1', 1]]

# 2，清空列表中的所有元素
list2 = [123,456,789]
list2.clear()
print(list2)  # []

# 3，列表拷贝，引用、浅拷贝、深拷贝
import copy
a = [1, 2, 3, 4, ['a', 'b']]
b = a  # 赋值引用
c = copy.copy(a)  # 浅拷贝
d = copy.deepcopy(a)  # 深拷贝
a.append(5)  # 修改对象a
a[4].append('c')  # 修改对象a中的['a', 'b']数组对象
print('a = ', a)  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
print('b = ', b)  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
print('c = ', c)  # [1, 2, 3, 4, ['a', 'b', 'c']]
print('d = ', d)  # [1, 2, 3, 4, ['a', 'b']]


# 4，count()：用来统计某一个成员在列表中的出现次数
list4 = [1,1,1,2,2,2,3,4,5,6,7,8]
print(list4.count(2)) # 3

# 5，extend(iterable)：该方法也是向列表中添加成员，并且也是一个参数，但是它将拆分成员（如列表则拆分单个列表成员，字符串则拆分成字符）
list5 = [1,2,3]
list5.extend(['john','1',1])
print(list5)  # [1, 2, 3, 'john', '1', 1]
list5.extend('love')
print(list5)  # [1, 2, 3, 'john', '1', 1, 'l', 'o', 'v', 'e']
# list5.extend(555) # 报错，TypeError: 'int' object is not iterable

# 6，index()：返回该元素的索引值
list6 = [123,456,789,7,8,456,1,2,3,456]
print(list6.index(456))  # 1 ， 搜索区间从开始到最后，返回元素第一次出现的索引值。
print(list6.index(456,2))  # 5 , 搜索区间从第3个元素开始到最后，搜索456返回的索引号是5.
print(list6.index(456,2,6)) # 5, 搜索区间从第3个元素开始到第6个为止，搜索456，返回的索引号是5.

# 7，insert(object)：在特定位置添加成员。两个参数，insert(m,member)，在索引为m(也就是第m+1的位置进行添加)，例如
list7 = [123,456,789]
list7.insert(1, 'love') # 在第1个索引之前添加
print(list7)  # [123, 'love', 456, 789]
list7.insert(2,[1,2,3])
print(list7)  # [123, 'love', [1, 2, 3], 456, 789]
# list1.insert(0,'wanglu')  # 没有插入，因为索引0之前不符合规则。
list7.insert(2,100)
print(list7)  # [123, 'love', 100, [1, 2, 3], 456, 789]

# 8，pop()：取出指定位置的元素（返回值），并删除。
list8 = [123,456,789]
print(list8.pop(1)) # 返回 456
print(list8) # [123, 789]
print(list8.pop()) #789  , 当pop()无参数时，返回最后一个值
print(list8) # [123]
print(list8.pop()) #123
print(list8) # []
# print(list8.pop()) # IndexError: pop from empty list

# 9，remove()：从列表中删除指定成员，不能print(list.remove())，这样返回None
# 注意：当列表中有多个重复成员的时候，一次只删除第一个。
list9 = [123,456,789,456,'abc',['love',3]]
list9.remove(456)
list9.remove(['love',3])
print(list9.remove('abc'))
print(list9) # [123, 789, 456] ， 第2个456不会删除。

# 9，del ：用索引进行删除 及 删除整个列表
del list9[1] # 通过索引号删除列表值
print(list9)  # [123, 456]
del list9  # 删除列表
# print(list9)  # NameError: name 'list9' is not defined

# 10,reverse()：就是将列表中的元素前后颠倒，不能print（list.reverse()）
list10 = [123,456,789]
list10.reverse()
print(list10) # [789, 456, 123]

# 11，sort()：将元素从小到大排序，不能print(list.sort())，这样返回None
list11= [4,8,2,5,77]
list11.sort()
print(list11) # [2, 4, 5, 8, 77]
# sort(reverse=True)：将元素从大到小排序
list11.sort(reverse = True)
print(list11)  # [77, 8, 5, 4, 2]


# 12，列表转换

# 列表 转 字符串
list12 = [1, 3, 5, '7', "8", 13, 20]
print(type(str(list12)),str(list12))  # <class 'str'> [1, 3, 5, '7', '8', 13, 20]

# 列表 转 元组
print(type(tuple(list12)),tuple(list12)) # <class 'tuple'> (1, 3, 5, '7', '8', 13, 20)

# 列表 转 字典，zip()方法将2个列表合并成字典，建议2个列表数量一致，否则多余的被忽略
l1 = ['a','b','c','d']  # 多出的 'd' 被忽略
l2 = ['123','456','789']
print(dict(zip(l1,l2)))  # {'a': '123', 'b': '456', 'c': '789'}

# 列表 转 字典，列表中keys部分要符合字典要求，如只能是 数字、字符、元组
l3 = [(7, 'xidada'), ('age', 64),((1,2),444)]
print(type(dict(l3)),dict(l3)) # <class 'dict'> {7: 'xidada', 'age': 64, (1, 2): 444}

# 字符串 转 列表
print(type(list('abcd')),list('abcd'))  # <class 'list'> ['a', 'b', 'c', 'd']

# 字节数组 转 列表
print(type(list(bytes('abcd','utf-8'))),list(bytes('abcd','utf-8')))  # <class 'list'> [97, 98, 99, 100]

# 元组 转 列表
print(type(list(('a','b','c',7,['b',55]))),list(('a','b','c',7,['b',55]))) # <class 'list'> ['a', 'b', 'c', 7, ['b', 55]]

# range对象 转 列表
print(type(list(range(1,5))),list(range(1,5)))  # <class 'list'> [1, 2, 3, 4]

dict7 = {'name': 'Zara', 'age': 7, 'class': 'First'}
# 字典 转 列表keys (返回列表内容是keys的集合)
print(list(dict7))  # ['age', 'name', 'class']

# 字典 转 列表values (返回列表内容是values的集合)
print(list(dict7.values()))  # ['Zara', 7, 'First']


# 13，随机获取list中的值
from random import choice
l_s1 = ['411', '1023', '0906', '0225']
print(choice(l_s1))

# 场景2：判断list是否为空？
l_s2 = []
if len(l_s2) == 0 :  # 或 if l_s2 == []
    print( "empty")


# 14，enumerate()获取列表的编号(从0开始)和元素
l_s3 = ['Sun.','Mon.','Tues.','Wed.','Thur.','Fri.','Sat.']
for (i,day) in enumerate(l_s3):
    print (str(i) + ' : ' + day)
# 结果:
# 0 : Sun.
# 1 : Mon.
# 2 : Tues.
# 3 : Wed.
# 4 : Thur.
# 5 : Fri.
# 6 : Sat.
# 14，enumerate()获取列表的编号(从start开始)和元素
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
print (list(enumerate(seasons)))  # # [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
print (list(enumerate(seasons, start=1))) # # [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
for i,j in enumerate(seasons, start=1):
    print (i,j)
# 结果:
# 1 Spring
# 2 Summer
# 3 Fall
# 4 Winter


# 15，输出 1-9 的2次方值
# 方法1：传统方法
l_s4 = []
for x in range(1,10):
    l_s4.append(x**2)
print(l_s4)  # [1, 4, 9, l_s4, 25, 36, 49, 64, 81]
# 方法2：更便捷的方法
l_s4 = [x**2 for x in range(1,10)]
print(l_s4)  # [1, 4, 9, l_s4, 25, 36, 49, 64, 81]


# 16，找出100以内的能够被3整除的正整数
# 方法1：传统做法
l_s5 = []
for n in range(1,100):
  if n % 3 == 0:
      l_s5.append(n)
print (l_s5)  # [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]
# 方法2：更便捷的方法
l_s5 = [n for n in range(1,100) if n % 3 == 0]
print (l_s5)  # [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]


# 17，strip()自动删除元素前后空格
l_s6 = ['   glass','apple   ','  greenleaf  ']
l_s6 = [n.strip() for n in l_s6]
print (l_s6)  # ['glass', 'apple', 'greenleaf']


# 18，列表操作符，组合、重复、判断、截取"
# list[start:end:sort]
print([1, 2, 3] + [4, 5, 6])  # [1, 2, 3, 4, 5, 6]
print(['Hi'] * 4)  # ['Hi', 'Hi', 'Hi', 'Hi']
print(3 in [1, 2, 3]) # True
list18 = [1,2,3,4,5,6,7,8,9,0]
print(list18[2])  # 3 ， 返回第3个元素
print(list18[-2])  # 9 ， 返回倒数第2个元素
print(list18[1:])  # [2, 3, 4, 5, 6, 7, 8, 9, 0], 返回从第2个到最后的元素列表，注意是列表
print(list18[1:3])  # [2, 3] , 返回从第2个到第3个元素列表
print(list18[1:1])  # [] , 返回空列表
print(list18[1:2])  # [2] , 注意虽然是1个元素，但返回的是1个元素的列表
print(list18[1:2][0])  # 2 , 返回第2个元素
print("~~~~~~~~~~~~~~~~~~~~")
print(list18[1:-1])  # [2, 3, 4, 5, 6, 7, 8, 9], 返回从第2个到倒数第二个元素列表
print(list18[1:-1:1]) # [2, 3, 4, 5, 6, 7, 8, 9], 后面：1表示 隔1取1
print(list18[1:-1:2]) # [2, 4, 6, 8] , 隔2取1
print("~~~~~~~~~~~~~~~~~~~~")
print(list18[3::-1])  # [4, 3, 2, 1] , 先获取1-4元素，然后倒序排列隔1取1，输出列表
print(list18[4::-2])  # [5, 3, 1], 先获取1-5元素，然后倒序隔2取1，输出列表
print(list18[3::])  # [4, 5, 6, 7, 8, 9, 0] ， 从第4个元素开始到最后

l = [1,2,3,4,5,6]
l[1:3] = ['a','c'] # 将列表里的 索引为1和2位置的数据修改成a,c
print(l)  # [1, 'a', 'c', 4, 5, 6]