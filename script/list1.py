# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: 列表
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
# 功能：浅拷贝（拷贝父对象，引用子对象）
import copy
a = [1, 2, 3, 4, ['a', 'b'], (1,), {"a": 123}]
b = a  # 赋值引用
c = copy.copy(a)  # 浅拷贝  = list.copy()
d = copy.deepcopy(a)  # 深拷贝
a.append(5)  # 修改对象a
# a[4] = ['z','y']
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
# 功能：获取元素并删除（先进后出）
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
list10 = [11, 22, 33, 44, 55, 22, ["a", 100]]
del list10[1]  # 通过索引号删除列表值
print(list10)  # [11, 33, 44, 55, 22, ['a', 100]]
del list10[-1][0]   # 删除 ["a", 100] 中的 "a"
print(list10)  # [11, 33, 44, 55, 22, [100]]
list10.append(list10.pop()[0])
print(list10)  # [11, 33, 44, 55, 22, 100]
del list10  # 删除列表
# print(list9)  # NameError: name 'list9' is not defined


print("11，list.reverse()".center(100, "-"))
# 功能：就是将列表中的元素前后颠倒，不能print（list.reverse()）
list11 = [123, 456, 789]
list11.reverse()
print(list11)  # [789, 456, 123]


print("12，list.sort()".center(100, "-"))
# 功能：将元素从小到大排序，不能print(list.sort())，这样返回None
list12 = [4, 8, 2, 5, 77]
list12.sort()
print(list12)  # [2, 4, 5, 8, 77]
# sort(reverse=True)：将元素从大到小排序
list12.sort(reverse=True)
print(list12)  # [77, 8, 5, 4, 2]


print("13，列表操作符，组合、重复、判断、截取".center(100, "-"))
print([1, 2, 3] + [4, 5, 6])  # [1, 2, 3, 4, 5, 6]
print(['Hi'] * 4)  # ['Hi', 'Hi', 'Hi', 'Hi']
print(3 in [1, 2, 3])  # True
list13 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(list13[2])  # 3 ， 返回第3个元素
print(list13[-2])  # 9 ， 返回倒数第2个元素
print(list13[1:])  # [2, 3, 4, 5, 6, 7, 8, 9, 0], 返回从第2个到最后的元素列表
print(list13[1:3])  # [2, 3] , 返回从第2个到第3个元素列表
print(list13[1:1])  # [] , 返回空列表
print(list13[1:2])  # [2] , 注意虽然是1个元素，但返回的是1个元素的列表
print(list13[1:2][0])  # 2 , 返回第2个元素
print(list13[1:3][1])  # 3
print(list13[1:-1])  # [2, 3, 4, 5, 6, 7, 8, 9], 返回从第2个到倒数第2个元素列表
print(list13[1:-1:1])  # [2, 3, 4, 5, 6, 7, 8, 9], 返回从第2个到倒数第2个元素列表，并间隔1输出
print(list13[1:-1:2])  # [2, 4, 6, 8] , 隔2取1
print(list13[3::])  # [4, 5, 6, 7, 8, 9, 0]， 从第4个元素开始到最后
print(list13[3::2])  # [4, 6, 8, 0]
print(list13[3::-1])  # [4, 3, 2, 1] , 先判断第三位，如果是负数，先获取第一位之前的元素（包括当前位），最后倒序隔1输出列表
print(list13[4::-2])  # [5, 3, 1], 先判断第三位，如果是负数，先获取第一位之前的元素（包括当前位），最后倒序隔2输出列表


# ************************************************************************************************************************************

print("14，练习题1".center(100, "-"))
# 练习题1：将列表[1, 2, 3, 4, 5, 6] 改为 [1, 200, 300, 5, 6]
list14 = [1, 2, 3, 4, 5, 6]
print(list14[1:3])  # [2, 3, 4]
list14[1:4] = [200, 300]  #   //实际传了3个值 [200,300,?]，只是最后一个值list识别成非法值，索性干掉吧，这样完成了删除4的功能。
print(list14)  # [1, 200, 300, 5, 6]


print("15，练习题2".center(100, "-"))
# 练习题2：将列表[11, 22, 33, ["a", 100, "b"], 44, 55, 22, ["a", 300, "b"]] 改为  [11, 22, 33, 100, 44, 55, 22, 300]
list15 = [11, 22, 33, ["a", 100, "b"], 44, 55, 22, ["a", 300, "b"]]
for x in range(len(list15)):
    if not isinstance(list15[x], int):
        del list15[x][::2]
        list15.insert(x+1, list15[x][0])
        list15.remove(list15[x])
print(list15)


print("16，练习题3".center(100, "-"))
# 练习题2：将列表[11, 22, 33, ["a", 100, "b"], 44, 55, 22, ["a", "c", 300, "b"]] 改为  [11, 22, 33, 100, 44, 55, 22, 300]
list16 = [11, 22, 33, ["a", 100, "b"], 44, 55, 22, ["a", "c", 300, "b"]]
a = 0
for x in range(len(list16)):
    if not isinstance(list16[x], int):
        for i in range(len(list16[x])):
            if isinstance(list16[x][i], int):
                a = list16[x][i]
        list16.insert(x+1, a)
        list16.remove(list16[x])
print(list16)  # [11, 22, 33, 100, 44, 55, 22, 300]


print("17，练习题4".center(100, "-"))
# 练习题4：将列表[11, 22, 33, 44, 55, 22, ["a", 100]] 改为  [11, 22, 33, 44, 55, 22, [100]]
list17 = [11, 22, 33, 44, 55, 22, ["a", 100]]
del list17[-1][0]
print(list17)  # [11, 22, 33, 44, 55, 22, [100]]


print("18，练习题5".center(100, "-"))
# 练习题8：将列表[11, 22, 33, ["a", 100, "b", 200]] 改为  [11, 22, 33, 300]
list18 = [11, 22, 33, ["a", 100, "b", 200]]
a = 0
for x in range(len(list18)):
    if not isinstance(list18[x], int):
        for i in range(len(list18[x])):
            if isinstance(list18[x][i], int):
                a = a + list18[x][i]
        list18.insert(x+1, a)
        list18.remove(list18[x])
print(list18)  # [11, 22, 33, 300]



# 7，列表
l_test = ['a']
l_test = l_test + [2.0, 3]   # 连接+赋值，这会消耗大量内存。 所以应该用 list.append() 添加元素
print(l_test)  # ['a', 2.0, 3]
l_test.insert(0, "tt")
print(l_test)  # ['tt', 'a', 2.0, 3]
l_test.extend("abc")
print(l_test)  # ['tt', 'a', 2.0, 3, 'a', 'b', 'c']
l_test.extend(["abc"])
print(l_test)  # ['tt', 'a', 2.0, 3, 'a', 'b', 'c', 'abc']

# 检索列表中元素出现的次数
print(l_test.count("a"))  # 2
