# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# *********************************************************************
"""
todo：【转换】
1.1 列表生成同值字典（fromkeys）
    => dict.fromkeys(['a',5], 1) # {'a':1, 5:1}
    => dict.fromkeys(['a', 5]) # {'a': None, 5: None}
1.2 列表生成序列字典 print(dict(enumerate(['a','b','c'], start=1)))  # {1: 'a', 2: 'b', 3: 'c'}
1.3 列表转字典（键值对,覆盖update）list2dictBySerial([key1, value1, key2, value2])  # {key1: value1, key2: value2}
1.4 列表转字典（键值对格式,覆盖update）list2dictByKeyValue(['key1:value1', 'key2:value2']))  # {key1: value1, key2: value2}
1.5 列表转字典（元组格式,覆盖update） print(dict([(1, 'a'), ('b', 2), ((1, 2), 444)]))  => {1: 'a', 'b': 2, (1, 2): 444}
1.6 列表转字符串  return "".join(list(map(str, [1,'a'])))  => 1a
1.7 两列表合成字典(覆盖update) print(dict(zip([1, 2], ['skducn', 'yoyo']))) # {1: 'skducn', 2: 'yoyo'}

todo：【类型转换】
2.1 数字字符串与数字互相转换 convertNumericStr([123]))  # ['123']
    # print(List_PO.convertNumericStr(['123'], "numeric"))  # [123]

todo：【分离、拆分、合并与分开】
2.1 列表数组分离   print(numpy.array_split([1, 2, 3, 4, 5], 2)) //元素奇数时，前多后少
    print(numpy.array_split([1, 2, 3, 4, 5], 2)[0])  # [1 2 3]
    print(numpy.array_split([1, 2, 3, 4, 5], 2)[1])  # [4 5]
2.2 列表拆分 resolveList(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]
2.3 切片列表 sliceList([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 1))  # [4, 5, '测试', 6]   只处理第一个参数

2.4 列表元素合并与分开 closeOpenElement(["a", "b", "c", "d"], 4))  # ['abcd']
2.5 两列表元素相加或连接 addTwoList([1, [111], "a", 0.01], [2, [222], "b", 0.07 , 66]))  # [3, [111, 222], 'ab', 0.08]
2.6 生成元素索引 setIndex(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
               setIndex(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]

todo：【比较】
3.1 获取两列表差异元素 twoListGetDiff(['张三', '王五', '老二'], ['张三', '老二', '王七']))  # (['王五'], ['王七'])
3.2 获取两列表相同元素 twoListGetSame(['张三', '李四', '王五', '老二'], ['张三', '李四', '老二', '王七']))  # ['张三', '李四', '老二']
3.3 获取两列表中在list1且不在list2的元素 twoListGetLeftNotContainRight(['张三', '李四', '王五', '老二', 'test'], ['张三', '李四', '老二', '王七']))  # ['王五', 'test'] //返回list1中的哪些元素不在list2中，并以列表方式返回
3.4 获取两列表相同元素的索引号 twoListGetSameIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))  # [1, 3]

todo：【替换】
4.1 替换元素一对多 replaceElemByOne2more(["1", 2, "3", ":"], 2, ""))  # ['1', '', '3', ':']
4.2 替换元素多对一 replaceElemByMore2one(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
4.3 替换元素多对多 replaceElemByMore2more(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
4.4 替换元素首字母大写且其余小写 replaceElemCaptain(['adam', 'LISA', 'barT'])  # ['Adam', 'Lisa', 'Bart']

todo：【删除】
5.1 删除元素左右空格 stripElem(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']
5.2 ? 删除原列表元素中的特殊字符（\n\t\r\xa0等）listClearSpecialChar(['0\n编号', '1\n既往史', 444, '2\n既\r往    史\t\n逻\xa0辑', 'abc'], "abc", ":"))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
5.3 删除列表中指定的（或模糊的）元素 listBatchDel(['0', "错误", '1', 222, "错误"], "错误", "-like"))  # ['0', '1', 222]
5.4 删除列表中重复的元素 delRepeatElem([2, "a", 1, "\n", "\n", 13, "", "test", 6, 2, "", "", 1, "a"]))  # [13, 'test', 6]
5.5 列表元素去重 deduplicationElem([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]

6 获取重复的元素数量 getRepeatElemCount()

7 随机获取列表元素 getRandomElem()

8 对齐列表的键值对格式 alignKeyValue(['key1,value1', 'key1,value1'], ","))

# todo 应用
整数转列表


"""


from PO.ListPO import *
List_PO = ListPO()


a = [('YLJGDM', 'VARCHAR2'), ('GRDAID', 'VARCHAR2')]
# print(dict(a))  # {'YLJGDM': 'VARCHAR2', 'GRDAID': 'VARCHAR2'}





# print("1.2 列表转字典之相邻元素键值对（覆盖update）".center(100, "-"))
# print(List_PO.list2dictBySerial(["a", "1", 100, 2]))  # {'a': '1', 100: 2}
# print(List_PO.list2dictBySerial(["a", "1", "a", "2"]))  # {'a': '2'}   //如遇到重复key，则取后面的key值
# print(List_PO.list2dictBySerial(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //如果元素个数是奇数，则忽略最后一个元素
#
# print("1.3 列表转字典之键值对格式（覆盖update）".center(100, "-"))
# print(List_PO.list2dictByKeyValue(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
# print(List_PO.list2dictByKeyValue(['a,3', 'b,4'], ","))  # {'a': '3', 'b': '4'}
# print(List_PO.list2dictByKeyValue(['a:1', 'b:2', 'a:133']))  # {'a': '133', 'b': '2'}  //转换后如果有重复的key，则后面的key替代前面的key
# print(List_PO.list2dictByKeyValue(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //不符合键值对格式的字符串被删除
#

# print("1.5 覆盖两列表转字典".center(100, "-"))
# print(dict(zip([1, 2], ['skducn', 'yoyo'])))  # {1: 'skducn', 2: 'yoyo'}
# print(dict(zip([1, 1], ['skducn', 'yoyo'])))  # {1: 'yoyo'}
#

"""[变换]"""

# print("2.1 数字字符串与数字互相转换".center(100, "-"))
# print(List_PO.convertNumericStr([123]))  # ['123']
# print(List_PO.convertNumericStr([123], "str"))  # ['123']
# print(List_PO.convertNumericStr(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
# print(List_PO.convertNumericStr(['123'], "numeric"))  # [123]
# print(List_PO.convertNumericStr(["a", "123", "555"], "numeric"))  # ['a', 123, 555]
# print(List_PO.convertNumericStr([1, 3, '13', "一", 20], "numeric"))  # [1, 3, 13, '一', 20]
# print(List_PO.convertNumericStr(["a", "0.123", "123.00", "56.0", "555.455678"], "numeric"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
#
# # print("2.2 列表元素合并与分开".center(100, "-"))
# print(List_PO.closeOpenElement(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素链接在一起组成一个元素
# print(List_PO.closeOpenElement(["a", "b", "c"], 4))  # ['abc']
# print(List_PO.closeOpenElement(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']
# print(List_PO.closeOpenElement(["a", "b", 123, "d", "e", "f"], 4))  # None  //元素必须是字符串，否则返回None
#
# print("2.3 两列表元素相加或连接".center(100, "-"))
# list1 = [1, [111], "a", 0.01]
# list2 = [2, [222], "b", 0.07 ,66]
# list3 = [-25, [222], "b", -0.07]
# list4 = [2, [222], "b", "111"]
# print(
#     List_PO.addTwoList([1, [111], "a", 0.01], [2, [222], "b", 0.07, 66]))  # [3, [111, 222], 'ab', 0.08]  //多余的元素被忽略
# print(List_PO.addTwoList(list1, list3))  # [-24, [111, 222], 'ab', -0.060000000000000005]   //注意浮点数负数计算出现问题，未知
# print(List_PO.addTwoList(list1, list4))  # None
#
# print("2.4 生成元素索引".center(100, "-"))
# print(List_PO.setIndex(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]  //默认编号从0开始
# print(List_PO.setIndex(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]    //指定编号从2开始
# for i, j in enumerate(['Spring', 'Summer', 'Fall', 'Winter'], start=1):
#     print(i, j)
# # 1 Spring
# # 2 Summer
# # 3 Fall
# # 4 Winter
#

#
# print("2.5 打散列表".center(100, "-"))
# print(
#     List_PO.resolveList(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
# print(List_PO.resolveList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
# print(List_PO.resolveList(['1', '2', '3', '4', '5', '6'],
#                           5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。
#
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 2)[0])
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 2)[1])
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)[0][1])
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)[1])

# print("2.6 切片列表".center(100, "-"))
# print(List_PO.sliceList([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 0))  # [1,2,3]
# print(List_PO.sliceList([1, 2, 3, '测试', 4, 5, 6], '测试', 1))  # [4,5,6]
# print(List_PO.sliceList([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 1))  # [4, 5, '测试', 6]   只处理第一个参数

"""[比较]"""

# print("3.1 获取两列表差异元素".center(100, "-"))
# print(List_PO.twoListGetDiff(['01', '02', '03'], ['02', '05']))  # (['王五'], ['王七'])
# # print(List_PO.twoListGetDiff(['张三', '12', '33'], ['张三', '12']))  # (['33'], [])
# #
# print("3.2 获取两列表相同元素".center(100, "-"))
# print(List_PO.twoListGetSame(['张三', '李四', '王五', '老二'], ['张三', '李四', '老二', '王七']))  # ['张三', '李四', '老二']
# #
# print("3.3 获取两列表中在list1且不在list2的元素".center(100, "-"))
# print(List_PO.twoListGetLeftNotContainRight(['张三', '李四', '王五', '老二', 'test'], ['张三', '李四', '老二', '王七']))  # ['王五', 'test'] //返回list1中的哪些元素不在list2中，并以列表方式返回
# print(List_PO.twoListGetLeftNotContainRight(['01', '02', '03'], ['01',"03"]))  # ['王五', 'test'] //返回list1中的哪些元素不在list2中，并以列表方式返回
# #
# print("3.4 获取两列表相同元素的索引号".center(100, "-"))
# print(List_PO.twoListGetSameIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))  # [1, 3]

"""[替换]"""

# print("4.1 1对多替换原列表中元素".center(100, "-"))
# print(List_PO.replaceElemByOne2more(["1", 2, "3", "2", 2], 2, ""))  # ['1', '', '3', '2', '']
# print(List_PO.replaceElemByOne2more(["1", 2, "3", ":"], "3", 88))  # ['1', 2, 88, ':']
# print(List_PO.listBatchReplaceByOne(["1", 2, "3", 2, 2, 2], 2, "j"))  # ['1', 'j', '3', 'j', 'j', 'j']  //把所有2替换成j

# print("4.2 替换元素多对一".center(100, "-"))
# print(List_PO.replaceElemByMore2one(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
# print(List_PO.replaceElemByMore2one(["1", 2, "3", ":"], [":", "2"], 7))  # ['1', 2, '3', 7]  //原列表中没有找到“2”所以不做替换。
#
# print("4.3 替换元素多对多".center(100, "-"))
# print(List_PO.replaceElemByMore2more(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
# print(List_PO.replaceElemByMore2more(["1", 2, "3", ":"], {":": 12, 1222: 77}))  # ['1', 2, '3', 12]   //如果某个key不存在，则忽略。

# print("4.4 替换元素首字母大写且其余小写".center(100, "-"))
# print(List_PO.replaceElemCaptain(['adam', 'LISA', 'barT']))  # ['Adam', 'Lisa', 'Bart']

"""[删除]"""

# print("5.1 删除元素左右空格".center(100, "-"))
# print(List_PO.stripElem(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']
#
# print("5.2 清除原列表元素中的特殊字符（\n\t\r\xa0等）".center(100, "-"))
# print(List_PO.listClearSpecialChar(['0\n编号', '1\n既往史', 444, '2\n既\r往    史\t\n逻\xa0辑', 'abc']))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
# print(List_PO.listClearSpecialChar(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70']))  # ['CHF64.90', 'CHF58.40', 'CHF48.70']
#
# print("5.3 删除列表中指定的（或模糊的）元素".center(100, "-"))
# print(List_PO.listBatchDel(['0', "错误", '1', 123, "错误"], "错误"))  # ['0', '1', 123]  // 删除“错误”元素
# print(List_PO.listBatchDel(['0', "错误", '1', 22, "错误内容"], "错误", "-like"))  # ['0', '1', 22]  //关键字vague表示模糊删除，删除包含“错误”的元素。
# print(List_PO.listBatchDel(['首页', '', '', '', '', '', '', '', '建档耗时统计', '档案更新监控'], ""))  # ['首页', '建档耗时统计', '档案更新监控']
#
# print("5.4 删除列表中重复的元素".center(100, "-"))
# print(List_PO.delRepeatElem([2, "a", 1, "\n", "\n", 13, "", "test", 6, 2, "", "", 1, "a"]))  # [13, 'test', 6]
# #
# # print("5.5 列表元素去重".center(100, "-"))
# print(List_PO.deduplicationElem([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]
# #
# #
# print("6 获取重复的元素数量".center(100, "-"))
# print(List_PO.getRepeatElemCount([2, 1, 13, 6, 2, 1]))  # [(2, 2), (1, 2), (13, 1), (6, 1)]
# print(List_PO.getRepeatElemCount(['a', 'b', 'c', 'a']))  # [('a', 2), ('b', 1), ('c', 1)]
#
#
# print("7 随机获取列表元素".center(100, "-"))
# print(List_PO.getRandomElem(['111', 222, [5, 6, '888'], {"a": 1, 2: "test"}]))
#
#
# print("8 对齐列表的键值对格式".center(100, "-"))
# list11 = List_PO.alignKeyValue(
#     ['1234567890,john', '123456,666', '123,baibai', '600065,', '600064,234j2po4j2oi34'], ",")
# for i in range(len(list11)):
#     print(list11[i])
# # # # 1234567890: john
# # # # 123456    : 666
# # # # 123       : baibai
# # # # 600065    :
# # # # 600064    : 234jpo4j2oi34

# 将整数转化成数字列表
print(list(map(int, str(12345))))  # [1, 2, 3, 4, 5]
print([int(x) for x in str(12345)])  # [1, 2, 3, 4, 5]

# 递归展开列表
from iteration_utilities import deepflatten
l = [[1,2,3],[4,[5],[6,7]],[8,[9,[10]]]]
print(list(deepflatten(l, depth=3)))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print([i for sublist in [[1,2,3],[3]] for i in sublist])  # [1, 2, 3, 3]
