# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# *********************************************************************

'''
todo：【转换】
1.1 列表转字典1（将相邻两元素组成键值对，如遇重复key则取后面的key值）list2dictBySerial(["a", "1", "b", "2"]))  # {'a': '1', 'b': '2'}
1.2 列表转字典2（键值对格式的字符串，如遇重复key则取后面的key值）list2dictByKeyValue(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
1.3 列表转字典3（元组内2个值，如遇重复key则取后面的key值）list2dictByTuple([(1, 'a'), ('b', 2), ((1, 2), 'c')]))  # {1: 'a', 'b': 2, (1, 2): 'c'}
1.4 两个列表转字典，lists2dict([1, 2], ['a', 'b']))  # {1: 'a', 2: 'b'}
1.5 列表转字符串 list2str(['h', 'e', 'l', 'l', 'o']))  # hello

todo：【变换】
2.1 互转列表中数字字符串与数字 listNumericStrInterchange([123]))  # ['123']
2.2 连接列表中字符 listJointStr(["a", "b", "c", "d"], 4))  # ['abcd']
2.3 连接两列表元素 listsJointBySameType([1, [111], "a", 0.01], [2, [222], "b", 0.07 , 66]))  # [3, [111, 222], 'ab', 0.08]
2.4 设置列表元素索引号 listSetIndex(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')] ， listSetIndex(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]
2.5 分解成N个数组 listSplitArray([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)   # [array([1, 2, 3, 4, 5]), array([6, 7, 8, 9])]
2.6 分解成N个列表 listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
2.7 分解列表成区间 listSplit([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 1))  # [4, 5, '测试', 6]   只处理第一个参数
2.8 键值对齐列表 listAlignByStrPartition([], ",")
2.9 随机获取列表元素 getRandomValue()

todo：【比较】
3.1 比较获取两列表中不同元素 listsGetDiff(['张三', '王五', '老二'], ['张三', '老二', '王七']))  # (['王五'], ['王七'])
3.2 比较获取两列表中相同元素 listsGetSame(['张三', '李四', '王五', '老二'], ['张三', '李四', '老二', '王七']))  # ['张三', '李四', '老二']
3.3 比较两列表获取在list1中的哪些元素不在list2中 listsGetNotContainList2(['张三', '李四', '王五', '老二', 'test'], ['张三', '李四', '老二', '王七']))  # ['王五', 'test'] //返回list1中的哪些元素不在list2中，并以列表方式返回
3.4 比较获取两列表相同元素的索引号 listsGetIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))  # [1, 3]

todo：【替换】
4.1 一对多替换原列表中元素 listBatchReplaceByOne2More(["1", 2, "3", ":"], 2, ""))  # ['1', '', '3', ':']
4.2 多对1替换原列表中元素 listBatchReplaceByMore2One(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
4.3 多对多替换原列表中元素 listBatchReplaceByMore2More(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]

todo：【清除】
5.1 清除列表中字符串元素左右空格 listStrip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']
5.2 清除原列表元素中的特殊字符（\n\t\r\xa0等）listClearSpecialChar(['0\n编号', '1\n既往史', 444, '2\n既\r往    史\t\n逻\xa0辑', 'abc'], "abc", ":"))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
5.3 删除列表中指定的（或模糊的）元素 listBatchDel(['0', "错误", '1', 222, "错误"], "错误", "-like"))  # ['0', '1', 222]
5.4 删除列表中重复的所有元素 delRepeatAll([2, "a", 1, "\n", "\n", 13, "", "test", 6, 2, "", "", 1, "a"]))  # [13, 'test', 6]
5.5 删除列表中重复的元素（去重）delRepeat([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]

6 统计列表中字符重复的次数 getRepeatCount()

'''

import numpy
from random import choice
from collections import Counter

from PO.CharPO import *
Char_PO = CharPO()
from PO.StrPO import *
Str_PO = StrPO()


class ListPO():

    def __init__(self):
        pass

    '''[转换]'''

    # 1.1 列表转字典1（将相邻两元素组成键值对，如遇重复key则取后面的key值）
    def list2dictBySerial(self, varList):
        dict4 = {}
        if len(varList) < 2:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")
        elif len(varList) % 2 == 0:
            for i in range(0, len(varList), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4
        else:
            for i in range(0, len(varList[:-1]), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4

    # 1.2 列表转字典2（键值对格式的字符串，如遇重复key则取后面的key值）
    def list2dictByStrPartition(self, varList, varSign=":"):
        # print(List_PO.list2dictByKeyValue(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
        # print(List_PO.list2dictByKeyValue(['a,3', 'b,4'], ","))  # {'a': '3', 'b': '4'}
        # print(List_PO.list2dictByKeyValue(['a:1', 'b:2', 'a:133']))  # {'a': '133', 'b': '2'}  //转换后如果有重复的key，则后面的key替代前面的key
        # print(List_PO.list2dictByKeyValue(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //不符合键值对格式的字符串被删除
        dict3 = {}
        try:
            for item in varList:
                if varSign in item:
                    keys = item.split(varSign)
                    dict3.update({keys[0]: keys[1]})
            return (dict3)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    # 1.3 列表转字典3（元组内2个值，如遇重复key则取后面的key值）
    def list2dictByTuple(self, varList):
        # 列表 转 字典，列表中keys部分要符合字典要求，如只能是 数字、字符、元组
        # 如：[(7, 'xidada'), ('age', 64), ((1, 2), 444)] => {7: 'xidada', 'age': 64, (1, 2): 444}
        # print(List_PO.list2dictByTuple([(1, 'a'), ('b', 2), ((1, 2), 444)]))  # {1: 'a', 'b': 2, (1, 2): 444}
        # print(List_PO.list2dictByTuple([(1, 'a'), ('b', 2), (1, 444)]))  # {1: 444, 'b': 2}   //转换后如果有重复的key，则后面的key替代前面的key
        try:
            return dict(varList)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 1.4 两列表转字典
    def lists2dict(self, varList1, varList2):
        # print(List_PO.lists2dict([1, 2, 3], ['haha', 'skducn', 'yoyo']))  # {1: 'haha', 2: 'skducn', 3: 'yoyo'}
        # py3.x中
        try:
            return (dict(map(lambda x, y: [x, y], varList1, varList2)))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")
        # # py2.x中
        # return (dict(zip(varList1, varList2)))

    # 1.5, 列表转字符串
    def list2str(self, varList=None):
        # print(List_PO.list2str(['h', 'e', 'l', 'l', 'o']))  # hello
        # print(List_PO.list2str([1, 3, 5, 7, 8, 20]))  # 1357820
        # print(List_PO.list2str([1, 3, "test", "12", "中国", 20]))  # 13test12中国20
        # print(List_PO.list2str([100]))  # 100
        # print(List_PO.list2str([100, [1, 2, 3]]))  # 100[1, 2, 3]   //列表中嵌列表
        # print(List_PO.list2str([100, (1, 2, 3)]))  # 100(1, 2, 3)   //列表中嵌元组
        # print(List_PO.list2str([100, 200, [1, 2, 3], {'a': 1, "b": 2}, 500]))  # 100200[1, 2, 3]{'a': 1, 'b': 2}500  //列表中嵌字典
        # print(List_PO.list2str())  # None   //无参数返回None
        try:
            result = ''.join(varList)
            return (result)
        except:
            try:
                varList = list(map(str, varList))
                result = ''.join(varList)
                return(result)
            except:
                print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    '''[变换]'''

    # 2.1 互转列表中数字字符串与数字
    def listNumericStrInterchange(self, varList, varMode="str"):
        # 忽略非数字字符的转换
        # print(List_PO.listNumericStrInterchange([123]))  # ['123']
        # print(List_PO.listNumericStrInterchange([123], "str"))  # ['123']
        # print(List_PO.listNumericStrInterchange(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
        # print(List_PO.listNumericStrInterchange(['123'], "numeric"))  # [123]
        # print(List_PO.listNumericStrInterchange(["a", "123", "555"], "numeric"))  # ['a', 123, 555]
        # print(List_PO.listNumericStrInterchange([1, 3, '13', "一", 20], "numeric"))  # [1, 3, 13, '一', 20]
        # print(List_PO.listNumericStrInterchange(["a", "0.123", "123.00", "56.0", "555.455678"], "numeric"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
        new_numbers = []
        if varMode == "digit":
            for i in range(len(varList)):
                if Char_PO.isComplex((varList[i])):
                    if str(varList[i]).isdigit():
                         new_numbers.append(int(varList[i]))
                    else:
                        new_numbers.append(float(varList[i]))
                else:
                    new_numbers.append(varList[i])
            return new_numbers
        else:
            return [str(i) for i in varList]

    # 2.2 连接列表中字符
    def listJointStr(self, varList, varNum):
        # 列表元素必须是字符串，不支持数字或内嵌子列表。
        # print(List_PO.listJointStr(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素链接在一起组成一个元素
        # print(List_PO.listJointStr(["a", "b", "c"], 4))  # ['abc']
        # print(List_PO.listJointStr(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']
        # print(List_PO.listJointStr(["www.", "baidu.", "com"], len(["www.", "baidu.", "com"])))  # ['www.baidu.com']
        # print(List_PO.listJointStr(["a", "b", 123, "d", "e", "f"], 4))  # None  //元素必须是字符串，否则返回None
        # print(List_PO.listJointStr(["a", "b", "c", ["a", "b", "c"]], 4))  # None
        list1 = []
        str1 = ""
        addition_number = 0
        i = 1
        try:
            while addition_number < len(varList):
                while i <= varNum:
                    if addition_number > len(varList) - 1:
                        break
                    else:
                        str1 = str1 + varList[addition_number]
                        addition_number += 1
                    i += 1
                list1.append(str1)
                str1 = ""
                i = 1
            return list1
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.3 连接两列表元素
    def listsJointBySameType(self, varList1, varList2):
        # 注意：连接的2个元素类型必须一致，否则返回None
        try:
            return [i + j for i, j in zip(varList1, varList2)]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.4 设置列表元素索引号
    def listSetIndex(self, varList , varStart=0):
        # 默认编号从0开始，或指定从N开始
        # 如：['Spring', 'Summer', 'Fall', 'Winter'] = > [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'),(3, 'Winter')]
        try:
            return (list(enumerate(varList, start=varStart)))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.5 分解成N个数组
    def listSplitArray(self, varList, varNum):
        try:
            return numpy.array_split(varList, varNum)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.6 分解成N个列表
    def listSplitSubList(self, varList, varNum):
        # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'],2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
        # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
        # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'],5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。
        try:
            list_of_groups = zip(*(iter(varList),) * varNum)
            end_list = [list(i) for i in list_of_groups]
            count = len(varList) % varNum
            end_list.append(varList[-count:]) if count != 0 else end_list
            return end_list

            # 方法2：通过切片可以一次append添加多个元素，如 list.append(varList[0:2]),即一条命令可以添加2个元素
            # l_valueAll = []
            # for i in range(0, len(varList), varNum):
            #     l_valueAll.append(varList[i:i+varNum])
            # return (l_valueAll)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.7 分解列表成区间。
    def listSplit(self, varList, varElement, varMode):
        # 如：[1,2,3,'测试',4,5,6] ，获取测试之前的元素，或获取测试之后的元素。
        if varMode == 1:
            list3 = []
            a = ""
            for i in varList:
                if i == varElement:
                    a = 1
                if a == 1:
                    list3.append(i)
            list3.pop(0)
            return (list3)
        elif varMode == 0:
            # 将列表中某个元素之前的元素组成一个新的列表， 如 [1,2,3,'审核信息',4,5,6] 变为 [1,2,3]
            list4 = []
            for i in varList:
                if varElement == i:
                    break
                list4.append(i)
            return (list4)

    # 2.8 键值对齐列表
    def listAlignByStrPartition(self, varList, varSplit):
        l1 = []
        l2 = []
        try:
            for i in range(len(varList)):
                varCount = varList[i].count(varSplit)
                if varCount == 1:
                    l1.append(str(varList[i]).split(varSplit)[0])  # key
                    l2.append(str(varList[i]).split(varSplit)[1])  # value
                elif varCount > 1:
                    for j in range(0, len(str(varList[i]).split(varSplit)) - 1, 2):
                        l1.append(str(varList[i]).split(varSplit)[j].replace(varSplit, ""))  # key
                        l2.append(str(varList[i]).split(varSplit)[j + 1].replace(varSplit, ""))  # value
                else:
                    l1.append(str(varList[i]).replace("(", "（").replace(")", "）").replace(varSplit, ""))  # key
                    l2.append("")  # value

            # print(l1)
            # print(l2)
            # 排版
            count = 0
            for i in range(len(l1)):
                if len(l1[i]) > count:
                    count = len(l1[i])
            for i in range(len(l1)):
                if Str_PO.isChinese(l1[i]):
                    # 全部是汉字
                    if count != len(l1[i]):
                        l1[i] = l1[i] + "  " * (count - len(l1[i])) + ":"
                    else:
                        l1[i] = l1[i] + ":"
                elif Str_PO.isContainChinese(l1[i]):
                    # 部分是汉字 ? 未处理 同上
                    l1[i] = l1[i] + "  " * (count - len(l1[i])) + ":"
                else:
                    # 全部是非汉字
                    l1[i] = l1[i] + " " * (count - len(l1[i])) + ":"
            # print(l1)
            # print(l2)
            c = [i + j for i, j in zip(l1, l2)]
            return (c)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.9 随机获取列表元素
    def getRandomValue(self, varList):
        try:
            return (choice(varList))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    '''[比较]'''

    # 3.1 比较获取两列表中不同元素
    def listsGetDiff(self, varList1, varList2):
        a = [x for x in varList1 if x in varList2]  # 两个列表中都存在
        return [y for y in (varList1) if y not in a], [y for y in (varList2) if y not in a]  # 两个列表中的不同元素

    # 3.2 比较获取两列表中相同元素
    def listsGetSame(self, varList1, varList2):
        return [x for x in varList1 if x in varList2]  # 两个列表中都存在

    # 3.3 比较两列表获取在list1中的哪些元素不在list2中
    def listsGetNotContainList2(self, varList1, varList2):
        return [x for x in varList1 if x not in varList2]

    # 3.4 比较获取两列表相同元素的索引号
    def listsGetIndex(self, varList1, varList2):
        error_index = []
        if len(varList1) == len(varList2):
            for i in range(0, len(varList1)):
                # 两个列表对应元素相同，则直接过
                if varList1[i] == varList2[i]:
                    pass
                else:
                    # 两个列表对应元素不同，则输出对应的索引
                    error_index.append(i)
            if error_index == []:
                return None
            else:
                return (error_index)
        else:
            return ("error, 两列表元素数量不一致")


    '''[替换]'''

    # 4.1 1 对多替换原列表中元素
    def listBatchReplaceByOne2More(self, varList, varSource, varDest):
        try:
            return [varDest if i == varSource else i for i in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 4.2 多对1替换原列表中元素
    def listBatchReplaceByMore2One(self, varList, varSourceList, varDest):
        # 多对一，多个元素被一个元素替换），影响原列表。
        # print(List_PO.listReplaceElements(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
        try:
            return [varDest if i in varSourceList else i for i in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 4.3 多对多替换原列表中元素
    def listBatchReplaceByMore2More(self, varList, varDict):
        try:
            return [varDict[i] if i in varDict else i for i in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    '''[删除]'''

    # 5.1 清除列表中字符串元素左右空格
    def listStrip(self, varList):
        try:
            return [n.strip() for n in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 5.1 清除原列表元素特殊字符\n\t\r\xa0等
    def listClearSpecialChar(self, varList):
        try:
            return ([''.join([i.strip() for i in str(a).strip()]) for a in varList])
            # return ([''.join([i.strip() for i in str(a).strip().replace(varSource, varDest)]) for a in varList])
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 5.3 删除列表中指定的（或模糊的）元素
    def listBatchDel(self, varList, varPartElement, varMode="-accurate"):
        tmpList = []
        try:
            for i in range(len(varList)):
                if varMode == "-accurate":
                    if varPartElement != varList[i]:
                        tmpList.append(varList[i])
                else:
                    if type(varPartElement) != type(varList[i]):
                        tmpList.append(varList[i])
                    elif varPartElement not in varList[i]:
                        tmpList.append(varList[i])
            return tmpList
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 5.4 删除列表中重复的所有元素
    def delRepeatAll(self, varList):
        return [item for item in varList if varList.count(item) == 1]


    # 5.5 删除列表中重复的元素
    def delRepeat(self, varList):
        return sorted(set(varList), key=varList.index)
        # 列表去重,并从小到大排列
        # def duplicateRemovalBySort(self, varList):
        #     return list(set(varList))


    # 6 统计列表中字符重复的次数
    def getRepeatCount(self, varList):
        counter = Counter()
        counter.update(varList)
        return (counter.most_common())


if __name__ == "__main__":

    List_PO = ListPO()

    '''[转换]'''

    # print("1.1 列表转字典1（将相邻两元素组成键值对，如遇重复key则取后面的key值）".center(100, "-"))
    # print(List_PO.list2dictBySerial(["a", "1", 100, 2]))  # {'a': '1', 100: 2}
    # print(List_PO.list2dictBySerial(["a", "1", "a", "2"]))  # {'a': '2'}   //如遇到重复key，则取后面的key值
    # print(List_PO.list2dictBySerial(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //如果元素个数是奇数，则忽略最后一个元素
    #
    # print("1.2 列表转字典2（键值对格式的字符串，如遇重复key则取后面的key值）".center(100, "-"))
    # print(List_PO.list2dictByKeyValue(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
    # print(List_PO.list2dictByKeyValue(['a,3', 'b,4'], ","))  # {'a': '3', 'b': '4'}
    # print(List_PO.list2dictByKeyValue(['a:1', 'b:2', 'a:133']))  # {'a': '133', 'b': '2'}  //转换后如果有重复的key，则后面的key替代前面的key
    # print(List_PO.list2dictByKeyValue(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //不符合键值对格式的字符串被删除
    #
    # print("1.3 列表转字典3（元组内2个值，如遇重复key则取后面的key值）".center(100, "-"))
    # print(List_PO.list2dictByTuple([(1, 'a'), ('b', 2), ((1, 2), 444)]))  # {1: 'a', 'b': 2, (1, 2): 444}
    # print(List_PO.list2dictByTuple([(1, 'a'), ('b', 2), (1, 444)]))  # {1: 444, 'b': 2}   //转换后如果有重复的key，则后面的key替代前面的key
    #
    # print("1.4，两个列表转字典".center(100, "-"))
    # print(List_PO.lists2dict([1, 2], ['skducn', 'yoyo']))  # {1: 'skducn', 2: 'yoyo'}
    #
    # # print("1.5，列表转字符串".center(100, "-"))
    # print(List_PO.list2str(['h', 'e', 'l', 'l', 'o']))  # hello
    # print(List_PO.list2str([1, 3, 5, 7, 8, 20]))  # 1357820
    # print(List_PO.list2str([1, 3, "test", "12", "中国", 20]))  # 13test12中国20
    # print(List_PO.list2str([100]))  # 100
    # print(List_PO.list2str([100, [1, 2, 3]]))  # 100[1, 2, 3]   //列表中嵌列表
    # print(List_PO.list2str([100, (1, 2, 3)]))  # 100(1, 2, 3)   //列表中嵌元组
    # print(List_PO.list2str([100, 200, [1, 2, 3], {'a': 1, "b": 2}, 500]))  # 100200[1, 2, 3]{'a': 1, 'b': 2}500  //列表中嵌字典
    # print(List_PO.list2str(213123213))  # None   //错误参数返回None
    # print(List_PO.list2str())  # None   //无参数返回None


    '''[变换]'''

    # print("2.1 互转列表中数字字符串与数字".center(100, "-"))
    # print(List_PO.listNumericStrInterchange([123]))  # ['123']
    # print(List_PO.listNumericStrInterchange([123], "str"))  # ['123']
    # print(List_PO.listNumericStrInterchange(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
    # print(List_PO.listNumericStrInterchange(['123'], "numeric"))  # [123]
    # print(List_PO.listNumericStrInterchange(["a", "123", "555"], "numeric"))  # ['a', 123, 555]
    # print(List_PO.listNumericStrInterchange([1, 3, '13', "一", 20], "numeric"))  # [1, 3, 13, '一', 20]
    # print(List_PO.listNumericStrInterchange(["a", "0.123", "123.00", "56.0", "555.455678"], "numeric"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
    #
    # print("2.2 连接列表中字符".center(100, "-"))
    # print(List_PO.listJointStr(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素链接在一起组成一个元素
    # print(List_PO.listJointStr(["a", "b", "c"], 4))  # ['abc']
    # print(List_PO.listJointStr(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']
    # print(List_PO.listJointStr(["www.", "baidu.", "com"], len(["www.", "baidu.", "com"])))  # ['www.baidu.com']
    # # print(List_PO.listJointStr(["a", "b", 123, "d", "e", "f"], 4))  # None  //元素必须是字符串，否则返回None
    # # print(List_PO.listJointStr(["a", "b", "c", ["a", "b", "c"]], 4))  # None
    #
    # print("2.3 连接两列表元素".center(100, "-"))
    # list1 = [1, [111], "a", 0.01]
    # list2 = [2, [222], "b", 0.07 ,66]
    # list3 = [-25, [222], "b", -0.07]
    # list4 = [2, [222], "b", "111"]
    # print(List_PO.listsJointBySameType([1, [111], "a", 0.01], [2, [222], "b", 0.07 , 66]))  # [3, [111, 222], 'ab', 0.08]  //多余的元素被忽略
    # print(List_PO.listsJointBySameType(list1, list3))  # [-24, [111, 222], 'ab', -0.060000000000000005]   //注意浮点数负数计算出现问题，未知
    # print(List_PO.listsJointBySameType(list1, list4))  # None
    #
    # print("2.4 设置列表元素索引号".center(100, "-"))
    # print(List_PO.listSetIndex(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]  //默认编号从0开始
    # print(List_PO.listSetIndex(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]    //指定编号从2开始
    # for i, j in enumerate(['Spring', 'Summer', 'Fall', 'Winter'], start=1):
    #     print(i, j)
    # # 1 Spring
    # # 2 Summer
    # # 3 Fall
    # # 4 Winter
    #

    # print("2.5 分解成N个数组".center(100, "-"))
    # varArr = List_PO.listSplitArray([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)  # //将列表拆成2个数组
    # print(varArr)  # [array([1, 2, 3, 4, 5]), array([6, 7, 8, 9])]
    # print(varArr[1][2])  # 8  //定位数组元素
    # print(len(varArr))  # 2
    # for i in range(len(varArr)):
    #     print(varArr[i])
    # # [1 2 3 4 5]
    # # [6 7 8 9]
    #
    # print("2.6 分解成N个列表".center(100, "-"))
    # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
    # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
    # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。

    # print("2.7 分解列表成区间".center(100, "-"))
    # print(List_PO.listSplit([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 0))  # [1,2,3]
    # print(List_PO.listSplit([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 1))  # [4, 5, '测试', 6]   只处理第一个参数
    # print(List_PO.listSplit([1, 2, 3, '测试', 4, 5, 6], '测试', 1))  # [4,5,6]

    # print("2.8 键值对齐列表".center(100, "-"))
    # list11 = List_PO.listAlignByStrPartition(
    #     ['1234567890,john', '123456,666', '123,baibai', '600065,', '600064,234j2po4j2oi34'], ",")
    # for i in range(len(list11)):
    #     print(list11[i])
    # # # 1234567890: john
    # # # 123456: 666
    # # # 123: baibai
    # # # 600065:
    # # # 600064: 234jpo4j2oi34

    # print("2.9 随机获取列表元素".center(100, "-"))
    # print(List_PO.getRandomValue(['111', 222, [5, 6, '888'], {"a": 1, 2: "test"}]))


    '''[比较]'''

    # print("3.1 比较获取两列表中不同元素".center(100, "-"))
    # print(List_PO.listsGetDiff(['张三', '王五', '老二'], ['张三', '老二', '王七']))  # (['王五'], ['王七'])
    # print(List_PO.listsGetDiff(['张三', '12', '33'], ['张三', '12']))  # (['33'], [])
    #
    # print("3.2 比较获取两列表中相同元素".center(100, "-"))
    # print(List_PO.listsGetSame(['张三', '李四', '王五', '老二'], ['张三', '李四', '老二', '王七']))  # ['张三', '李四', '老二']
    #
    # print("3.3 比较两列表获取在list1中的哪些元素不在list2中".center(100, "-"))
    # print(List_PO.listsGetNotContainList2(['张三', '李四', '王五', '老二', 'test'], ['张三', '李四', '老二', '王七']))  # ['王五', 'test'] //返回list1中的哪些元素不在list2中，并以列表方式返回
    #
    # print("3.4 比较获取两列表相同元素的索引号".center(100, "-"))
    # print(List_PO.listsGetIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))  # [1, 3]


    '''[替换]'''

    # print("4.1 1对多替换原列表中元素".center(100, "-"))
    # print(List_PO.listBatchReplaceByOne2More(["1", 2, "3", ":"], "2", ""))  # ['1', 2, '3', ':']   //没有变化，因为原列表中是数字2，要被替换的是字符串2
    # print(List_PO.listBatchReplaceByOne2More(["1", 2, "3", ":"], "3", 88))  # ['1', 2, 88, ':']
    # print(List_PO.listBatchReplaceByOne(["1", 2, "3", 2, 2, 2], 2, "j"))  # ['1', 'j', '3', 'j', 'j', 'j']  //把所有2替换成j

    # print("4.2 多对1替换原列表中元素".center(100, "-"))
    # print(List_PO.listBatchReplaceByMore2One(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
    # print(List_PO.listBatchReplaceByMore2One(["1", 2, "3", ":"], [":", "2"], 7))  # ['1', 2, '3', 7]  //原列表中没有找到“2”所以不做替换。
    #
    # print("4.3 多对多替换原列表中元素".center(100, "-"))
    # print(List_PO.listBatchReplaceByMore2More(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
    # print(List_PO.listBatchReplaceByMore2More(["1", 2, "3", ":"], {":": 12, 1222: 77}))  # ['1', 2, '3', 12]   //如果某个key不存在，则忽略。


    '''[删除]'''

    # print("5.1 清除列表中字符串元素左右空格".center(100, "-"))
    # print(List_PO.listStrip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']

    # print("5.2 清除原列表元素中的特殊字符（\n\t\r\xa0等）".center(100, "-"))
    # print(List_PO.listClearSpecialChar(['0\n编号', '1\n既往史', 444, '2\n既\r往    史\t\n逻\xa0辑', 'abc']))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
    # print(List_PO.listClearSpecialChar(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70']))  # ['CHF64.90', 'CHF58.40', 'CHF48.70']
    #    
    # print("5.3 删除列表中指定的（或模糊的）元素".center(100, "-"))
    # print(List_PO.listBatchDel(['0', "错误", '1', 123, "错误"], "错误"))  # ['0', '1', 123]  // 删除“错误”元素
    # print(List_PO.listBatchDel(['0', "错误", '1', 22, "错误内容"], "错误", "-like"))  # ['0', '1', 22]  //关键字vague表示模糊删除，删除包含“错误”的元素。
    # print(List_PO.listBatchDel(['首页', '', '', '', '', '', '', '', '建档耗时统计', '档案更新监控'], ""))  # ['首页', '建档耗时统计', '档案更新监控']
    #
    print("5.4 删除列表中重复的所有元素".center(100, "-"))
    print(List_PO.delRepeatAll([2, "a", 1, "\n", "\n", 13, "", "test", 6, 2, "", "", 1, "a"]))  # [13, 'test', 6]

    print("5.5 删除列表中重复的元素".center(100, "-"))
    print(List_PO.delRepeat([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]


    print("6 统计列表中字符重复的次数".center(100, "-"))
    print(List_PO.getRepeatCount([2, 1, 13, 6, 2, 1]))  # [(2, 2), (1, 2), (13, 1), (6, 1)]
    print(List_PO.getRepeatCount(['a', 'b', 'c', 'a']))  # [('a', 2), ('b', 1), ('c', 1)]
