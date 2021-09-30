# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# *********************************************************************

'''
1.1，列表转字典（相邻两元素组成键值对，重复key后替代）list2dictBySerial(["a", "1", "b", "2"]))  # {'a': '1', 'b': '2'}
1.2，列表转字典（键值对格式的字符串，重复key后替代））list2dictByStrPartition(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
1.3，列表转字典（元组内2个值，重复key后替）list2dictByTuple([(1, 'a'), ('b', 2), ((1, 2), 'c')]))  # {1: 'a', 'b': 2, (1, 2): 'c'}
1.4，两个列表转字典，lists2dict([1, 2], ['a', 'b']))  # {1: 'a', 2: 'b'}
1.5，列表转字符串 list2str()

2.1，数字与数字字符串互转（默认转数字字符）str2Digit2str([123]))  # ['123']
2.2，列表中字符串元素连接 listJointStr(["a", "b", "c", "d"], 4))  # ['abcd']
2.3，两个列表对应序列号相同类型元素相加 listsAddBySameType([1, [111], "a", 0.01], [2, [222], "b", 0.07 , 66]))  # [3, [111, 222], 'ab', 0.08]
2.4，listSerialNumber(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
listSerialNumber(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]
2.5，去除列表字符串元素左右空格，listStrip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']

3.1，列表拆成N个数组（列表）listSplitArray([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)  # //将列表拆成2个数组
3.2，列表拆成N个元素组成的多个子列表 listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]

4.1，列表一对一替换，影响原列表。 listReplace(["1", 2, "3", ":"], 2, ""))  # ['1', '', '3', ':']
4.2，列表多对一替换（多对一，多个元素被一个元素替换），影响原列表。listReplaceByList(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
4.3，列表多对多替换（多对多，多个元素各自被替代，字典格式），影响原列表。listReplaceByDict(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
4.4，列表一对一替换，并过滤掉特殊符号（如 \t \r \n），影响原列表。listReplaceSmart

5.1，列表一对一替换，并删除某个元素，且原列表不变。listReplaceDel(["1", 2, "3", ":"], ":", "3", "3"))   # ['1', '2']
5.2，列表删除元素（包含模糊元素），且原列表不变。listDel(['0', "错误", '1', '2', "错误"], "错误"))  # ['0', '1', '2']

6，键值对齐 listAlignByStrPartition([], ",")

7，随机获取list中的值 getRandomValue()

8.1，比较两列表，返回两列表中不同元素 compare2listsGetDiff()
8.2，比较两列表，返回两列表中相同元素 compare2listsGetSame(）
8.3，比较两列表，返回list1中的哪些元素不在list2中 compare2ListsGetNotContainList2()
8.4, 比较两列表，返回对应元素不同的索引号 compare2ListsGetIndex()

9，截取列表中区间元素 interceptSection()

10, 删除重复的元素 delRepeat()

11.1 去重，从小到大排序 duplicateRemovalBySort()
11.2 去重 duplicateRemoval()
'''

import numpy,sys
from random import choice

from PO.CharPO import *
Char_PO = CharPO()
from PO.StrPO import *
Str_PO = StrPO()
from PO.CharPO import *
Char_PO = CharPO()

class ListPO():

    def __init__(self):
        pass


    # 1.1，列表转字典（相邻两元素组成键值对，重复key后替代）
    def list2dictBySerial(self, varList):
        # 注意：列表元素如遇奇数，则忽略最后1个元素。
        # print(List_PO.list2dictBySerial(["a", "1", "b", "2"]))  # {'a': '1', 'b': '2'}
        # print(List_PO.list2dictBySerial(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //因为元素个数是奇数，因此最后一个元素被忽略
        # print(List_PO.list2dictBySerial(["a"]))  # None
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

    # 1.2，列表转字典（某种符号相隔格式的字符串，重复key后替代）
    def list2dictByStrPartition(self, varList, varSign=":"):
        # print(List_PO.list2dictByStrPartition(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
        # print(List_PO.list2dictByStrPartition(['a,3', 'b,4'], ","))  # {'a': '3', 'b': '4'}
        # print(List_PO.list2dictByStrPartition(['a:1', 'b:2', 'a:133']))  # {'a': '133', 'b': '2'}  //转换后如果有重复的key，则后面的key替代前面的key
        # print(List_PO.list2dictByStrPartition(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //不符合键值对格式的字符串被删除
        dict3 = {}
        try:
            for item in varList:
                if varSign in item:
                    keys = item.split(varSign)
                    dict3.update({keys[0]: keys[1]})
            return (dict3)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    # 1.3，列表转字典（元组格式）
    def list2dictByTuple(self, varList):
        # 列表 转 字典，列表中keys部分要符合字典要求，如只能是 数字、字符、元组
        # 如：[(7, 'xidada'), ('age', 64), ((1, 2), 444)] => {7: 'xidada', 'age': 64, (1, 2): 444}
        try:
            return dict(varList)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 1.4，两列表转字典
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
        # print(List_PO.list2str(213123213))  # None   //错误参数返回None
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



    # 2.1，列表之字符与数字互转
    def str2Digit2str(self, varList, varMode="str"):
        # print(List_PO.str2Digit2str([123]))  # ['123']
        # print(List_PO.str2Digit2str([123], "str"))  # ['123']
        # print(List_PO.str2Digit2str(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
        # print(List_PO.str2Digit2str(['123'], "digit"))  # [123]
        # print(List_PO.str2Digit2str(["a", "123", "555"], "digit"))  # ['a', 123, 555]
        # print(List_PO.str2Digit2str([1, 3, '13', "一", 20], "digit"))  # [1, 3, 13, '一', 20]
        # print(List_PO.str2Digit2str(["a", "0.123", "123.00", "56.0", "555.455678"], "digit"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
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

    # 2.2，列表中字符串元素连接
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

    # 2.3，两个列表对应序列号相同类型元素相加
    def listsAddBySameType(self, varList1, varList2):
        # 相加的2个元素类型必须一致，否则返回None
        try:
            return [i + j for i, j in zip(varList1, varList2)]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.4，列表元素生成对应编号并组成元组
    def listSerialNumber(self, varList , varStart=0):
        # 默认编号从0开始，或指定从N开始
        # 如：['Spring', 'Summer', 'Fall', 'Winter'] = > [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'),(3, 'Winter')]
        try:
            return (list(enumerate(varList, start=varStart)))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 2.5，列表字符串元素去除左右空格
    def listStrip(self, varList):
        try:
            return [n.strip() for n in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")





    # 3.1，列表拆成N个数组（列表）
    def listSplitArray(self, varList, varNum):
        try:
            return numpy.array_split(varList, varNum)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 3.2，列表拆成N个元素组成的多个子列表
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



    # 4.1，列表一对一替换（影响原列表）。
    def listReplace(self, varList, varSource, varDest):
        try:
            return [varDest if i == varSource else i for i in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 4.2，列表多对一替换（多对一，多个元素被一个元素替换，列表格式，影响原列表。）
    def listReplaceByList(self, varList, varSourceList, varDest):
        # 多对一，多个元素被一个元素替换），影响原列表。
        # print(List_PO.listReplaceElements(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
        try:
            return [varDest if i in varSourceList else i for i in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 4.3，列表多对多替换（多对多，多个元素各自被替代，字典格式，影响原列表。）
    def listReplaceByDict(self, varList, varDict):
        try:
            return [varDict[i] if i in varDict else i for i in varList]
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 4.4，列表替换单个元素，并过滤掉特殊符号（如 \t \r \n），影响原列表。
    # 问题：数字被转成字符？？
    def listReplaceSmart(self, varList, varSource, varDest):
        # 注意：只适用于字符串内容，如列表中元素是数字类型的，则转换成字符串，如 123 转为 “123”
        try:
            return ([''.join([i.strip() for i in str(a).strip().replace(varSource, varDest)]) for a in varList])
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 5.1，列表替换单个元素，并删除指定元素，原列表不变。
    def listReplaceDel(self, varList, varSource, varDest, varDelElement):
        # print(List_PO.listReplaceDelElement(["1", 2, "3", ":"], ":", "", ""))  # ['1', '2', '3']   //将 ：替换成空，再删除空元素。
        try:
            tmplist1 = ([''.join([i for i in str(a).replace(varSource, varDest)]) for a in varList])
            tmplist2 = []
            for i in range(len(tmplist1)):
                if tmplist1[i] != varDelElement:
                    tmplist2.append(tmplist1[i])
            return tmplist2
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 5.2，列表删除元素（包含模糊元素），且原列表不变。
    def listDel(self, varList, varPartElement, varMode="accurate"):
        # print(List_PO.listDelElement(list1,"错误"))  # ['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误', 'abc']  // 精准删除，删除“错误”元素
        # print(List_PO.listDelElement(list1, "错误", "vague"))  # ['0\n编号 规则', 'abc']  //模糊删除，删除包含“错误”的元素。
        # print(list1)  # 原值不变
        tmpList = []
        try:
            for i in range(len(varList)):
                if varMode == "accurate":
                    if varPartElement != varList[i]:
                        tmpList.append(varList[i])
                else:
                    if varPartElement not in varList[i]:
                        tmpList.append(varList[i])
            return tmpList
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    # 6，键值对齐
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

    # 7，随机获取list中的值
    def getRandomValue(self, varList):
        try:
            return (choice(varList))
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")


    # 8.1，比较两列表，返回两列表中不同元素
    def compare2listsGetDiff(self, varList1, varList2):
        a = [x for x in varList1 if x in varList2]  # 两个列表中都存在
        return [y for y in (varList1) if y not in a], [y for y in (varList2) if y not in a]  # 两个列表中的不同元素
    # 8.2，比较两列表，返回两列表中相同元素
    def compare2listsGetSame(self ,varList1, varList2):
        return [x for x in varList1 if x in varList2]  # 两个列表中都存在
    # 8.3，比较两列表，返回list1中的哪些元素不在list2中
    def compare2ListsGetNotContainList2(self, varList1, varList2):
        return [x for x in varList1 if x not in varList2]
    # 8.4, 比较两列表，返回对应元素不同的索引号
    def compare2ListsGetIndex(self, varList1, varList2):
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


    # 9，截取列表中区间元素作为新列表元素。
    def interceptSection(self, varList, varElement, varMode):
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


    # 10，删除列表中重复的项目
    def delRepeat(self, varList):
        return [item for item in varList if varList.count(item) == 1]



    # 11.1 列表去重,并从小到大排列
    def duplicateRemovalBySort(self, varList):
        return list(set(varList))
    # 11.2 列表去重(保持原位)
    def duplicateRemoval(self, varList):
        return sorted(set(varList), key=varList.index)


if __name__ == "__main__":

    List_PO = ListPO()

    # print(dir(list))
    #
    # print("1.1，列表转字典（相邻两元素组成键值对，重复key后替代）".center(100, "-"))
    # print(List_PO.list2dictBySerial(["a", "1", 100, 2]))  # {'a': '1', 100: 2}
    # print(List_PO.list2dictBySerial(["a", "1", "a", "2"]))  # {'a': '2'}   //转换后如果有重复的key，则后面的key替代前面的key
    # print(List_PO.list2dictBySerial(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //如果元素个数是奇数，则忽略最后一个元素
    #
    # print(" 1.2，列表转字典（某种符号相隔格式的字符串，重复key后替代）".center(100, "-"))
    # print(List_PO.list2dictByStrPartition(['a:1', 'b:2']))  # {'a': '1', 'b': '2'}
    # print(List_PO.list2dictByStrPartition(['a,3', 'b,4'], ","))  # {'a': '3', 'b': '4'}
    # print(List_PO.list2dictByStrPartition(['a:1', 'b:2', 'a:133']))  # {'a': '133', 'b': '2'}  //转换后如果有重复的key，则后面的key替代前面的key
    # print(List_PO.list2dictByStrPartition(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //不符合键值对格式的字符串被删除
    #
    # print("1.3，列表转字典（元组内2个值，重复key后替）".center(100, "-"))
    # print(List_PO.list2dictByTuple([(1, 'a'), ('b', 2), ((1, 2), 444)]))  # {1: 'a', 'b': 2, (1, 2): 444}
    # print(List_PO.list2dictByTuple([(1, 'a'), ('b', 2), (1, 444)]))  # {1: 444, 'b': 2}   //转换后如果有重复的key，则后面的key替代前面的key
    #
    # print("1.4，两个列表转字典".center(100, "-"))
    # print(List_PO.lists2dict([1, 2], ['skducn', 'yoyo']))  # {1: 'skducn', 2: 'yoyo'}
    #
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
    #
    #
    #
    # print("2.1，列表中数字与数字字符串互转（默认转数字字符）".center(100, "-"))
    # print(List_PO.str2Digit2str([123]))  # ['123']
    # print(List_PO.str2Digit2str([123], "str"))  # ['123']
    # print(List_PO.str2Digit2str(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
    # print(List_PO.str2Digit2str(['123'], "digit"))  # [123]
    # print(List_PO.str2Digit2str(["a", "123", "555"], "digit"))  # ['a', 123, 555]
    # print(List_PO.str2Digit2str([1, 3, '13', "一", 20], "digit"))  # [1, 3, 13, '一', 20]
    # print(List_PO.str2Digit2str(["a", "0.123", "123.00", "56.0", "555.455678"], "digit"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
    #
    # print("2.2，列表中字符串元素连接".center(100, "-"))
    # print(List_PO.listJointStr(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素链接在一起组成一个元素
    # print(List_PO.listJointStr(["a", "b", "c"], 4))  # ['abc']
    # print(List_PO.listJointStr(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']
    # print(List_PO.listJointStr(["www.", "baidu.", "com"], len(["www.", "baidu.", "com"])))  # ['www.baidu.com']
    # # print(List_PO.listJointStr(["a", "b", 123, "d", "e", "f"], 4))  # None  //元素必须是字符串，否则返回None
    # # print(List_PO.listJointStr(["a", "b", "c", ["a", "b", "c"]], 4))  # None
    #
    # print("2.3，两个列表对应序列号相同类型元素相加".center(100, "-"))
    # list1 = [1, [111], "a", 0.01]
    # list2 = [2, [222], "b", 0.07 ,66]
    # list3 = [-25, [222], "b", -0.07]
    # list4 = [2, [222], "b", "111"]
    # print(List_PO.listsAddBySameType([1, [111], "a", 0.01], [2, [222], "b", 0.07 , 66]))  # [3, [111, 222], 'ab', 0.08]  //多余的元素被忽略
    # print(List_PO.listsAddBySameType(list1, list3))  # [-24, [111, 222], 'ab', -0.060000000000000005]   //注意浮点数负数计算出现问题，未知
    # print(List_PO.listsAddBySameType(list1, list4))  # None
    #
    # print("2.4，为列表元素生成对应序号".center(100, "-"))
    # print(List_PO.listSerialNumber(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]  //默认编号从0开始
    # print(List_PO.listSerialNumber(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]    //指定编号从2开始
    # for i, j in enumerate(['Spring', 'Summer', 'Fall', 'Winter'], start=1):
    #     print(i, j)
    # # 1 Spring
    # # 2 Summer
    # # 3 Fall
    # # 4 Winter
    #
    # print("2.5，去除列表字符串元素左右空格".center(100, "-"))
    # print(List_PO.listStrip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']
    #
    #
    #
    # print("3.1，列表拆成N个数组（列表）".center(100, "-"))
    # varArr = List_PO.listSplitArray([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)  # //将列表拆成2个数组
    # print(varArr)  # [array([1, 2, 3, 4, 5]), array([6, 7, 8, 9])]
    # print(varArr[1][2])  # 8  //定位数组元素
    # print(len(varArr))  # 2
    # for i in range(len(varArr)):
    #     print(varArr[i])
    # # [1 2 3 4 5]
    # # [6 7 8 9]
    #
    # print("3.2，列表拆成N个元素组成的多个子列表".center(100, "-"))
    # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
    # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
    # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。
    #
    #
    #
    # print("4.1，列表一对一替换，影响原列表。".center(100, "-"))
    # print(List_PO.listReplace(["1", 2, "3", ":"], "2", ""))  # ['1', 2, '3', ':']   //没有变化，因为2是数字，不是字符串
    # print(List_PO.listReplace(["1", 2, "3", 2], 2, ""))  # ['1', '', '3', '']
    # print(List_PO.listReplace(['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误'], "\n", ":"))   #  ['0:编号 规则', '1:既往史记录 逻辑 错误', '2:既往史\t:逻辑错误']
    # print(List_PO.listReplace(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40', '\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  #['\nCHF\xa0\r\n\r\n  64.90', '\nCHF\xa0\r\n58.40', '\nCHF\xa0\r48.70']
    #
    # print("4.2，列表多对一替换（多对一，多个元素被一个元素替换，列表格式），影响原列表。".center(100, "-"))
    # print(List_PO.listReplaceByList(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
    #
    # print("4.3，列表多对多替换（多对多，多个元素各自被替代，字典格式），影响原列表。".center(100, "-"))
    # print(List_PO.listReplaceByDict(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
    # print(List_PO.listReplaceByDict(["1", 2, "3", ":"], {":": 12, 1222: 77}))  # ['1', 2, '3', 12]   //如果某个key不存在，则忽略。
    # # print(List_PO.listReplaceByDict(["1", 2, "3", ":"], ""))   # None
    #
    # print("4.4，列表一对一替换，并过滤掉特殊符号，影响原列表。".center(100, "-"))
    # print(List_PO.listReplaceSmart(['0\n编号', '1\n既往史', 444, '2\n既往史\t\n逻辑', 'abc'], "abc", ":"))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
    # print(List_PO.listReplaceSmart(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  # ['CHF64.90', 'CHF58.40', 'CHF48.70']
    #
    #
    #
    # print("5.1，列表一对一替换，并删除某个元素，且原列表不变。".center(100, "-"))
    # print(List_PO.listReplaceDel(["1", 2, "3", ":"], ":", "?", "3"))   # ['1', '2', '?']   //将 ：替换成?，再删除元素“3”
    # print(List_PO.listReplaceDel(["1", 2, "3", ":"], ":", "3", "3"))   # ['1', '2']
    # print(List_PO.listReplaceDel(["1", 2, "3", ":"], ":", "3", ""))   # ['1', '2', '3', '3']
    #
    # print("5.2，列表删除元素（包含模糊元素），且原列表不变。".center(100, "-"))
    # print(List_PO.listDel(['0', "错误", '1', '2', "错误"], "错误"))  # ['0', '1', '2']   // 删除“错误”元素
    # print(List_PO.listDel(['0', "错误", '1', '2', "错误内容"], "错误", "vague"))  # ['0', '1', '2']  //关键字vague表示模糊删除，删除包含“错误”的元素。
    # print(List_PO.listDel(['首页', '', '', '', '', '', '', '', '建档耗时统计', '档案更新监控'], ""))  # ['首页', '建档耗时统计', '档案更新监控']
    #
    #
    #
    # print("6，键值对齐".center(100, "-"))
    # list11 = List_PO.listAlignByStrPartition(['1234567890,john', '123456,666', '123,baibai', '600065,', '600064,234j2po4j2oi34'], ",")
    # for i in range(len(list11)):
    #     print(list11[i])
    # # 1234567890: john
    # # 123456: 666
    # # 123: baibai
    # # 600065:
    # # 600064: 234jpo4j2oi34



    # print("7，随机获取list中的值".center(100, "-"))
    # print(List_PO.getRandomValue(['111', 222, [5, 6, '888'], {"a": 1, 2: "test"}]))


    # print("8.1，比较两列表，返回两列表中不同元素".center(100, "-"))
    # print(List_PO.compare2listsGetDiff(['张三', '王五', '老二'], ['张三', '老二', '王七']))  # (['王五'], ['王七'])
    # print(List_PO.compare2listsGetDiff(['张三', '12', '33'], ['张三', '12']))  # (['33'], [])
    # x = List_PO.compare2listsGetDiff(['张三', '12', '33'], ['张三', '12', '33'])
    # if x[0] == [] and x[0] == []:
    #     print("ok")
    # else:
    #     print("error")
    #
    # print("8.2，比较两列表，返回两列表中相同元素".center(100, "-"))
    # print(List_PO.compare2listsGetSame(['张三', '李四', '王五', '老二'], ['张三', '李四', '老二', '王七']))  # ['张三', '李四', '老二']
    #
    # print("8.3，比较两列表，返回list1中的哪些元素不在list2中".center(100, "-"))
    # print(List_PO.compare2ListsGetNotContainList2(['张三', '李四', '王五', '老二', 'test'], ['张三', '李四', '老二', '王七']))  # ['王五', 'test'] //返回list1中的哪些元素不在list2中，并以列表方式返回
    #
    # print("8.4, 比较两列表，返回对应元素不同的索引号".center(100, "-"))
    # print(List_PO.compare2ListsGetIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))


    # print("9，截取列表中区间元素".center(100, "-"))
    # print(List_PO.interceptSection([1, 2, 3, '测试', 4, 5, 6], '测试', 0))  # [1,2,3]
    # print(List_PO.interceptSection([1, 2, 3, '测试', 4, 5, 6], '测试', 1))  # [4,5,6]
    #
    # print("10，删除列表中重复的元素".center(100, "-"))
    # print(List_PO.delRepeat([2, 1, 13, 6, 2, 1]))  # [13, 6]



    # print("11.1，列表去重，元素从小到大排列".center(100, "-"))
    # print(List_PO.duplicateRemovalBySort([2, 1, 13, 6, 2, 1]))  # [1, 2, 13, 6]
    # print("11.2，列表去重（保持原位）".center(100, "-"))
    # print(List_PO.duplicateRemoval([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]


