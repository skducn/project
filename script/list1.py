# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 列表内置属性及使用方法 list1.py
# list，实际上是列表类型的构造函数，列表可变且序可迭代。class list([iterable])
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

12、列表操作符，组合、重复、判断、截取"
'''

print(dir(list))

print("1，list.append(object)".center(100, "-"))
# 功能：向列表中添加成员，每次只能在列表尾添加一个成员，在使用前列表必须存在，如预先定义一个空列表。
# 原地修改列表，且没有返回值，不能赋值给某个变量
# append 将参数视为 element，作为追加一个元素拼接（整体追加）
list1 = []
list1.append('1')
print(id(list1))  # 2637392327616
list1.append(55)
print(id(list1))  # 2637392327616
list1.append(['john', '1', 1])
print(id(list1))  # 2637392327616
list1.append((1,2,3))
list1.append({1:"a"})
print(list1)  # ['1', 55, ['john', '1', 1]]


print("2，list.clear()".center(100, "-"))
# 功能：清空列表中的所有元素
list2 = [123,456,789]
list2.clear()
print(list2)  # []


print("3，list.copy()".center(100, "-"))
# 功能：浅拷贝，影响子列表
import copy
a = [1, 2, 3, 4, ['a', 'b']]
b = a  # 赋值引用
c = copy.copy(a)  # 浅拷贝  = list.copy()
d = copy.deepcopy(a)  # 深拷贝
a.append(5)  # 修改对象a
a[4].append('c')  # 修改对象a中的['a', 'b']数组对象
print('a = ', a)  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
print('b = ', b)  # [1, 2, 3, 4, ['a', 'b', 'c'], 5]
print('c = ', c)  # [1, 2, 3, 4, ['a', 'b', 'c']]
print('d = ', d)  # [1, 2, 3, 4, ['a', 'b']]


print("4，list.count()".center(100, "-"))
# 功能：统计某一个成员在列表中的出现次数
list4 = [1, 1, 1, 2, 2, 2, 2, 3, 4, 5, 6, 7, 8]
print(list4.count(2))  # 4  //统计列表中2出现的次数。


print("5，list.extend(iterable)".center(100, "-"))
# 功能：该方法也是向列表中添加成员，并且也是一个参数，但是它将拆分成员（如列表则拆分单个列表成员，字符串则拆分成字符）
# iterable 不支持int类型的对象
# 原地修改列表，且没有返回值，不能赋值给某个变量
# extend 将参数视为 list，拼接两个列表（个体化扩编追加）
list5 = [1, 2, 3]
print(id(list5))
list5.extend(['john', '1', 1])
print(id(list5))  # 经过extend()方法进行扩容后，还是原来的ID地址，这就是列表的原地修改。
print(list5)  # [1, 2, 3, 'john', '1', 1]
list5.extend('love')    # list5.extend('love') 等效于 list[len(list5):]= 'love'
# list5[len(list5):] = 'love'   # [1, 2, 3, 'john', '1', 1, 'l', 'o', 'v', 'e']
print(list5)  # [1, 2, 3, 'john', '1', 1, 'l', 'o', 'v', 'e']
# list5.extend(555) # TypeError: 'int' object is not iterable  //报错，不支持int类型的对象
# list5.extend(100)    # TypeError: 'int' object is not iterable


print("6，list.index()".center(100, "-"))
# 功能：返回该元素的索引值
list6 = [123, 456, 789, 7, 8, 456, 1, 2, 3, 456]
print(list6.index(456))  # 1 ， 搜索区间从开始到最后，返回元素第一次出现的索引值。
print(list6.index(456, 2))  # 5 , 搜索区间从第3个元素开始到最后，搜索456返回的索引号是5.
print(list6.index(456, 2, 6))  # 5, 搜索区间从第3个元素开始到第6个为止，搜索456，返回的索引号是5.


print("7，list.insert()".center(100, "-"))
# 功能：在特定位置添加成员。两个参数，insert(m,member)，在索引为m(也就是第m+1的位置进行添加)，例如
list7 = [123, 456, 789]
list7.insert(1, 'love')  # 在第1个索引之前添加
print(list7)  # [123, 'love', 456, 789]
list7.insert(2, [1, 2, 3])
print(list7)  # [123, 'love', [1, 2, 3], 456, 789]
list7.insert(0, "太阳")
print(list7)  # ['太阳', 123, 'love', [1, 2, 3], 456, 100, 789]
list7.insert(-1, 100)  # 不存在，没有报语法错



print("8，list.pop()".center(100, "-"))
# 功能：获取元素并删除。先进后出
list8 = [11, 22, 33, 44, 55]
print(list8.pop(1))  # 22
print(list8)  # [11, 33, 44, 55]
print(list8.pop())  # 55  //默认获取最后一个元素
print(list8)  # [11, 33, 44]
print(list8.pop(-1))  # 44  //如同上
print(list8)  # [11, 33]
print(list8.pop())  # 33
print(list8.pop())  # 11
# print(list8.pop()) # IndexError: pop from empty list   所以对pop操作要小心，建议异常判断或数量判断。


print("9，list.remove()".center(100, "-"))
# 功能：从左到右删除列表中第一个符合要求的元素
# 注意：remove() 无返回值，默认None，当列表中有多个重复元素时，从左到右只删除第一个元素。
list9 = [11, 22, 33, 22, 'abc', ['love', 3]]
list9.remove(22)
list9.remove(['love', 3])
print(list9.remove('abc'))  # None
print(list9)  # [11, 33, 22]


print("10，del list()".center(100, "-"))
# 功能：用索引号部分元素、内嵌列表元素、全部元素
list9 = [11, 22, 33, 44, 55, 22, ["a", 100]]

del list9[1]  # 通过索引号删除列表值
print(list9)  # [11, 33, 44, 55, 22, ['a', 100]]

del list9[-1][0]   # 删除 ["a", 100] 中的 "a"
print(list9)  # [11, 33, 44, 55, 22, [100]]

list9.append(list9.pop()[0])
print(list9)  # [11, 33, 44, 55, 22, 100]

del list9  # 删除列表
# print(list9)  # NameError: name 'list9' is not defined


print("11，list.reverse()".center(100, "-"))
# 功能：就是将列表中的元素前后颠倒，不能print（list.reverse()）
list10 = [123, 456, 789]
list10.reverse()
print(list10)  # [789, 456, 123]


print("12，list.sort()".center(100, "-"))
# 功能：将元素从小到大排序，不能print(list.sort())，这样返回None
list11 = [4, 8, 2, 5, 77]
list11.sort()
print(list11)  # [2, 4, 5, 8, 77]
# sort(reverse=True)：将元素从大到小排序
list11.sort(reverse=True)
print(list11)  # [77, 8, 5, 4, 2]


print("13，列表操作符，组合、重复、判断、截取".center(100, "-"))
print([1, 2, 3] + [4, 5, 6])  # [1, 2, 3, 4, 5, 6]
print(['Hi'] * 4)  # ['Hi', 'Hi', 'Hi', 'Hi']
print(3 in [1, 2, 3])  # True
list18 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(list18[2])  # 3 ， 返回第3个元素
print(list18[-2])  # 9 ， 返回倒数第2个元素
print(list18[1:])  # [2, 3, 4, 5, 6, 7, 8, 9, 0], 返回从第2个到最后的元素列表，注意是列表
print(list18[1:3])  # [2, 3] , 返回从第2个到第3个元素列表
print(list18[1:1])  # [] , 返回空列表
print(list18[1:2])  # [2] , 注意虽然是1个元素，但返回的是1个元素的列表
print(list18[1:2][0])  # 2 , 返回第2个元素
print(list18[1:3][1])  # 3
print("~~~~~~~~~~~~~~~~~~~~")
print(list18[1:])  # [2, 3, 4, 5, 6, 7, 8, 9, 0]
print(list18[1:-1])  # [2, 3, 4, 5, 6, 7, 8, 9], 返回从第2个到倒数第二个元素列表
print(list18[1:-1:1])  # [2, 3, 4, 5, 6, 7, 8, 9], 后面：1表示 隔1取1
print(list18[1:-1:2])  # [2, 4, 6, 8] , 隔2取1
print("~~~~~~~~~~~~~~~~~~~~")
print(list18[3::])  # [4, 5, 6, 7, 8, 9, 0]， 从第4个元素开始到最后
print(list18[3::-1])  # [4, 3, 2, 1] , 先获取1-4元素，然后倒序排列隔1取1，输出列表
print(list18[4::-2])  # [5, 3, 1], 先获取1-5元素，然后倒序隔2取1，输出列表
print(list18[3::2])  # [4, 6, 8,0]


# 练习题2：
l = [1, 2, 3, 4, 5, 6]
print(id(l))
print(l[1:4])  # [2, 3, 4]
l[1:4] = ['a', 'c']  # 将列表里的 索引为1和2位置的数据修改成a,c
print(l)  # [1, 'a', 'c', 5, 6]
print(id(l))


# 练习题1：
list9 = [11, 22, 33, ["a", 100, "b"], 44, 55, 22, ["a", 300, "b"]]
print(id(list9))
for x in range(len(list9)):
    if not isinstance(list9[x], int):
        del list9[x][::2]   # del x[0],x[1]
        # print(list9[x][0])
        list9.insert(x+1, list9[x][0])
        list9.remove(list9[x])
        # break
print(list9)
print(id(list9))

