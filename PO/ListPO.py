# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# *********************************************************************

'''
1.1，列表（字典格式）转字典，如：['a:1', 'b:4'] => {"a":1, "b":4}
1.2，列表（列表中相邻两元素组成键值队）转字典，如：[a,1,b,2] => {"a":1, "b":2}
1.3，两列表转字典，如：[1, 2, 3], ['haha', 'skducn', 'yoyo'] => {1: 'haha', 2: 'skducn', 3: 'yoyo'}
1.4, 列表转字符串

2.1，列表之字符与数字互转
2.2，列表内元素合并（列表元素必须是字符串，不支持数字或内嵌子列表。）
2.3，两列表元素相加（相加的2个元素类型必须一致，否则忽略）
2.4，列表元素生成对应编号，组成元组，如：['Spring', 'Summer', 'Fall', 'Winter'] => [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
2.5，列表字符串元素去除左右空格，如：['   glass','apple   ','  greenleaf  ']  => ['glass', 'apple', 'greenleaf']

3.1，列表拆成多个数组
3.2，列表拆成多个子列表

4.1，列表替换单个元素，影响原列表。
4.2，列表替换批量元素（多对一，多个元素被一个元素替换），影响原列表。
4.3，列表替换多个元素（多对多，多个元素各自被替代，字典格式），影响原列表。
4.4，列表替换单个元素，并过滤掉特殊符号（如 \t \r \n），影响原列表。？

5.1，列表替换单个元素，并删除某个元素，且原列表不变。
5.2，列表删除元素（包含模糊元素），且原列表不变。

6，键值对齐
7，随机获取list中的值


'''

import numpy
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


    # 1.1，列表转字典（列表中相邻两元素组成键值队）
    def list2dictBySerial(self, varList):
        # 注意：列表元素如遇奇数，则忽略最后1个元素，元素必须大于2个。
        # print(List_PO.list2dictBySerial(["a", "1", "b", "2"]))  # {'a': '1', 'b': '2'}
        # print(List_PO.list2dictBySerial(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //因为元素个数是奇数，因此最后一个元素被忽略
        # print(List_PO.list2dictBySerial(["a"]))  # None
        dict4 = {}
        if len(varList) < 2:
            return None
        elif len(varList) % 2 == 0:
            for i in range(0, len(varList), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4
        else:
            for i in range(0, len(varList[:-1]), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4

    # 1.2，列表转字典（字典格式的字符串）
    def list2dictByStr(self, varList):
        # 注意：如不符合字典格式（key:value）的字符串，则忽略此元素
        # print(List_PO.list2dictByStr(['a:1', 'b:2', 'c:3']))  # {'a': '1', 'b': '2', 'c': '3'}
        # print(List_PO.list2dictByStr(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //列表中字符串元素不符合字典格式的被过滤。
        dict3 = {}
        try:
            for item in varList:
                if ":" in item:
                    keys = item.split(':')
                    dict3.update({keys[0]: keys[1]})
            return (dict3)
        except:
            return None

    # 1.3，列表转字典（元组格式）
    def list2dictByTuple(self, varList):
        # 列表 转 字典，列表中keys部分要符合字典要求，如只能是 数字、字符、元组
        # 如：[(7, 'xidada'), ('age', 64), ((1, 2), 444)] => {7: 'xidada', 'age': 64, (1, 2): 444}
        try:
            return dict(varList)
        except:
            return None

    # 1.4，两列表转字典
    def lists2dict(self, varList1, varList2):
        # print(List_PO.lists2dict([1, 2, 3], ['haha', 'skducn', 'yoyo']))  # {1: 'haha', 2: 'skducn', 3: 'yoyo'}
        # py3.x中
        try:
            return (dict(map(lambda x, y: [x, y], varList1, varList2)))
        except:
            return None
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
                return None



    # 2.1，列表之字符与数字互转
    def listConvertElement(self, varList, varMode="str"):
        # print(List_PO.listConvertElement([123], "str"))  # ['123']
        # print(List_PO.listConvertElement(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
        # print(List_PO.listConvertElement([1, 3, '13', "一二", 20], "str"))  # ['1', '3', '13', '一二', '20']
        # print(List_PO.listConvertElement(['123'], "digit"))  # [123]
        # print(List_PO.listConvertElement(["a", "123", "555"], "digit"))  # ['a', 123, 555]
        # print(List_PO.listConvertElement([1, 3, '13', "一二", 20], "digit"))  # [1, 3, 13, '一二', 20]
        # print(List_PO.listConvertElement(["a", "0.123", "123.00", "56.0", "555.455678"], "digit"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
        new_numbers = []
        if varMode == "digit":
            for i in range(len(varList)):
                if Char_PO.isNumbersType((varList[i])):
                    if str(varList[i]).isdigit():
                         new_numbers.append(int(varList[i]))
                    else:
                        new_numbers.append(float(varList[i]))
                else:
                    new_numbers.append(varList[i])
            return new_numbers
        else:
            return [str(i) for i in varList]

    # 2.2，列表内元素合并
    def listJointElement(self, varList, varNum):
        # 列表元素必须是字符串，不支持数字或内嵌子列表。
        # print(List_PO.listJointElement(["a", "b", "c"], 4))  # ['abc']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
        # print(List_PO.listJointElement(["a", "b", "c", "d"], 4))  # ['abcd']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
        # print(List_PO.listJointElement(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
        # print(List_PO.listJointElement(["a", "b", 123, "d", "e", "f"], 4))  # None  //列表元素必须是字符串，否则返回None
        # print(List_PO.listJointElement(["www.", "baidu.", "com"], len(["www.", "baidu.", "com"])))  # ['www.baidu.com']
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
            return None

    # 2.3，两列表元素相加
    def listAddElement(self, varList1, varList2):
        # 相加的2个元素类型必须一致，否则返回None
        try:
            return [i + j for i, j in zip(varList1, varList2)]
        except:
            return None

    # 2.4，列表元素生成对应编号并组成元组
    def listSignNoElement(self, varList , varStart=0):
        # 默认编号从0开始，或指定从N开始
        # 如：['Spring', 'Summer', 'Fall', 'Winter'] = > [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'),(3, 'Winter')]
        try:
            return (list(enumerate(varList, start=varStart)))
        except:
            return None

    # 2.5，列表字符串元素去除左右空格
    def listStrip(self, varList):
        try:
            return [n.strip() for n in varList]
        except:
            return None





    # 3.1，列表拆成多个数组
    def listSplitArray(self, varList, varNum):
        try:
            return numpy.array_split(varList, varNum)
        except:
            return None

    # 3.2，列表拆成多个子列表
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
        except:
            return None



    # 4.1，列表替换单个元素（影响原列表）。
    def listReplaceElement(self, varList, varSource, varDest):
        try:
            return [varDest if i == varSource else i for i in varList]
        except:
            return None

    # 4.2，列表替换批量元素（多对一，多个元素被一个元素替换，影响原列表。）
    def listReplaceLotElement(self, varList, varSourceList, varDest):
        # 多对一，多个元素被一个元素替换），影响原列表。
        # print(List_PO.listReplaceElements(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
        try:
            return [varDest if i in varSourceList else i for i in varList]
        except:
            return None

    # 4.3，列表替换多个元素（多对多，多个元素各自被替代，字典格式，影响原列表。）
    def listReplaceElements(self, varList, varDict):
        try:
            return [varDict[i] if i in varDict else i for i in varList]
        except:
            return None

    # 4.4，列表替换单个元素，并过滤掉特殊符号（如 \t \r \n），影响原列表。
    # 问题：数字被转成字符？？
    def listReplaceSmart(self, varList, varSource, varDest):
        # 注意：只适用于字符串内容，如列表中元素是数字类型的，则转换成字符串，如 123 转为 “123”
        try:
            return ([''.join([i.strip() for i in str(a).strip().replace(varSource, varDest)]) for a in varList])
        except:
            return None

    # 5.1，列表替换单个元素，并删除指定元素，原列表不变。
    def listReplaceDelElement(self, varList, varSource, varDest, varDelElement):
        # print(List_PO.listReplaceDelElement(["1", 2, "3", ":"], ":", "", ""))  # ['1', '2', '3']   //将 ：替换成空，再删除空元素。
        try:
            tmplist1 = ([''.join([i for i in str(a).replace(varSource, varDest)]) for a in varList])
            tmplist2 = []
            for i in range(len(tmplist1)):
                if tmplist1[i] != varDelElement:
                    tmplist2.append(tmplist1[i])
            return tmplist2
        except:
            return None

    # 5.2，列表删除元素（包含模糊元素），且原列表不变。
    def listDelElement(self, varList, varPartElement, varMode="accurate"):
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
            return None

    # 6，键值对齐
    def listKeyValueAlign(self, varList, varSplit):

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
                        l1.append(str(varList[i]).split(varSplit)[j].replace(":", ""))  # key
                        l2.append(str(varList[i]).split(varSplit)[j + 1].replace(":", ""))  # value
                else:
                    l1.append(str(varList[i]).replace("(", "（").replace(")", "）").replace(":", ""))  # key
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
            return None

    # 7，随机获取list中的值
    def listRandomValue(self, varList):
        try:
            return (choice(varList))
        except:
            return None




if __name__ == "__main__":

    List_PO = ListPO()

    print(dir(list))

    print("1.1，列表转字典（列表中相邻两元素组成键值队）".center(100, "-"))
    print(List_PO.list2dictBySerial(["a", "1", "b", "2"]))  # {'a': '1', 'b': '2'}
    print(List_PO.list2dictBySerial(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //因为元素个数是奇数，因此最后一个元素被忽略
    print(List_PO.list2dictBySerial(["a"]))  # None

    print(" 1.2，列表转字典（字典格式的字符串）".center(100, "-"))
    print(List_PO.list2dictByStr(['a:1', 'b:2', 'c:3']))  # {'a': '1', 'b': '2', 'c': '3'}
    print(List_PO.list2dictByStr(['a:1', '123b456', 'c:3']))  # {'a': '1', 'c': '3'}   //列表中字符串元素不符合字典格式的被过滤。

    print("1.3，列表转字典（元组）".center(100, "-"))
    print(List_PO.list2dictByTuple([(7, 'xidada'), ('age', 64), ((1, 2), 444)]))  # {7: 'xidada', 'age': 64, (1, 2): 444}

    print("1.4，两列表转字典".center(100, "-"))
    print(List_PO.lists2dict([1, 2, 3], ['haha', 'skducn', 'yoyo']))  # {1: 'haha', 2: 'skducn', 3: 'yoyo'}

    print("1.5，列表转字符串".center(100, "-"))
    print(List_PO.list2str(['h', 'e', 'l', 'l', 'o']))  # hello
    print(List_PO.list2str([1, 3, 5, 7, 8, 20]))  # 1357820
    print(List_PO.list2str([1, 3, "test", "12", "中国", 20]))  # 13test12中国20
    print(List_PO.list2str([100]))  # 100
    print(List_PO.list2str([100, [1, 2, 3]]))  # 100[1, 2, 3]   //列表中嵌列表
    print(List_PO.list2str([100, (1, 2, 3)]))  # 100(1, 2, 3)   //列表中嵌元组
    print(List_PO.list2str([100, 200, [1, 2, 3], {'a': 1, "b": 2}, 500]))  # 100200[1, 2, 3]{'a': 1, 'b': 2}500  //列表中嵌字典
    print(List_PO.list2str(213123213))  # None   //错误参数返回None
    print(List_PO.list2str())  # None   //无参数返回None



    print("2.1，列表之字符与数字互转".center(100, "-"))
    print(List_PO.listConvertElement([123], "str"))  # ['123']
    print(List_PO.listConvertElement(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
    print(List_PO.listConvertElement([1, 3, '13', "一二", 20], "str"))  # ['1', '3', '13', '一二', '20']
    print(List_PO.listConvertElement(['123'], "digit"))  # [123]
    print(List_PO.listConvertElement(["a", "123", "555"], "digit"))  # ['a', 123, 555]
    print(List_PO.listConvertElement([1, 3, '13', "一", 20], "digit"))  # [1, 3, 13, '一', 20]
    print(List_PO.listConvertElement(["a", "0.123", "123.00", "56.0", "555.455678"],"digit"))  # ['a', 0.123, 123.0, 56.0, 555.455678]

    print("2.2，列表内元素合并".center(100, "-"))
    print(List_PO.listJointElement(["a", "b", "c"], 4))  # ['abc']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
    print(List_PO.listJointElement(["a", "b", "c", "d"], 4))  # ['abcd']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
    print(List_PO.listJointElement(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
    print(List_PO.listJointElement(["www.", "baidu.", "com"], len(["www.", "baidu.", "com"])))  # ['www.baidu.com']
    print(List_PO.listJointElement(["a", "b", 123, "d", "e", "f"], 4))  # None  //列表元素必须是字符串，否则返回None
    print(List_PO.listJointElement(["a", "b", "c", ["a", "b", "c"]], 4))  # None

    print("2.3，两列表元素相加".center(100, "-"))
    list1 = ['张洪瑞', '张华卿', '张洪瑞', '张凯旋', [111], 11]
    list2 = ['平诊', '急诊', '急诊', '急诊', [123], 22]
    list3 = ['平诊', '急诊', '急诊', '急诊', [5], "66"]
    print(List_PO.listAddElement(list1, list2))  # ['张洪瑞平诊', '张华卿急诊', '张洪瑞急诊', '张凯旋急诊', [111, 123], 33]
    print(List_PO.listAddElement(list1, list3))  # None  //字符串66不能与数字11相加。

    print("2.4，列表元素生成对应编号并组成元组".center(100, "-"))
    print(List_PO.listSignNoElement(['Spring', 'Summer', 'Fall', 'Winter']))  #  [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]  //默认编号从0开始
    print(List_PO.listSignNoElement(['Spring', 'Summer', 'Fall', 'Winter'], 2))  #  [(2, 'Spring'), (3, 'Summer'), (4, 'Fall'), (5, 'Winter')]    //指定编号从2开始
    for i, j in enumerate(['Spring', 'Summer', 'Fall', 'Winter'],start=1):
        print(i, j)
    # 1 Spring
    # 2 Summer
    # 3 Fall
    # 4 Winter

    print("2.5，列表字符串元素去除左右空格".center(100, "-"))
    print(List_PO.listStrip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']



    print("3.1，列表拆成多个数组".center(100, "-"))
    varArr = List_PO.listSplitArray([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    print(varArr)  # [array([1, 2, 3]), array([4, 5, 6]), array([7, 8, 9])]
    print(varArr[1][2])  # 6  //定位数组元素
    print(len(varArr))  # 3
    for i in range(len(varArr)):
        print(varArr[i])
    # [1 2 3]
    # [4 5 6]
    # [7 8 9]

    print("3.2，列表拆成多个子列表".center(100, "-"))
    print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
    print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
    print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。



    print("4.1，列表替换单个元素，影响原列表。".center(100, "-"))
    print(List_PO.listReplaceElement(["1", 2, "3", ":"], "2", ""))  # ['1', 2, '3', ':']   //没有变化，因为2是数字，不是字符串
    print(List_PO.listReplaceElement(["1", 2, "3", ":"], 2, ""))  # ['1', '', '3', ':']
    print(List_PO.listReplaceElement(['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误'], "\n", ":"))   #  ['0:编号 规则', '1:既往史记录 逻辑 错误', '2:既往史\t:逻辑错误']
    print(List_PO.listReplaceElement(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  #['\nCHF\xa0\r\n\r\n  64.90', '\nCHF\xa0\r\n58.40', '\nCHF\xa0\r48.70']

    print("4.2，列表替换批量元素（多对一，多个元素被一个元素替换），影响原列表。".center(100, "-"))
    print(List_PO.listReplaceLotElement(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]

    print("4.3，列表替换多个元素（多对多，多个元素各自被替代，字典格式），影响原列表。".center(100, "-"))
    print(List_PO.listReplaceElements(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
    print(List_PO.listReplaceElements(["1", 2, "3", ":"], {":": 12, 1222: 77}))  # ['1', 2, '3', 12]   //如果某个key不存在，则忽略。
    print(List_PO.listReplaceElements(["1", 2, "3", ":"], ""))   # None

    print("4.4，列表替换单个元素，并过滤掉特殊符号，影响原列表。".center(100, "-"))
    print(List_PO.listReplaceSmart(['0\n编号', '1\n既往史', 444, '2\n既往史\t\n逻辑', 'abc'], "abc", ":"))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
    print(List_PO.listReplaceSmart(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  # ['CHF64.90', 'CHF58.40', 'CHF48.70']



    print("5.1，列表替换单个元素，并删除某个元素，且原列表不变。".center(100, "-"))
    print(List_PO.listReplaceDelElement(["1", 2, "3", ":"], ":", "?", "3"))   # ['1', '2', '?']   //将 ：替换成?，再删除元素“3”

    print("5.2，列表删除元素（包含模糊元素），且原列表不变。".center(100, "-"))
    list1 = ['0\n编号 规则', "错误", '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误', 'abc', "错误"]
    print(List_PO.listDelElement(list1, "错误"))  # ['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误', 'abc']  // 删除“错误”元素
    print(List_PO.listDelElement(list1, "错误", "vague"))  # ['0\n编号 规则', 'abc']  //关键字vague表示模糊删除，删除包含“错误”的元素。
    print(list1)  # 原值不变



    print("6，键值对齐".center(100, "-"))
    list11 = List_PO.listKeyValueAlign(['1234567890:john', '123456:666', '123:baibai', '600065:', '600064:234j2po4j2oi34'], ":")
    for i in range(len(list11)):
        print(list11[i])


    print("7，随机获取list中的值".center(100, "-"))
    print(List_PO.listRandomValue(['111',222,[5,6,'888'],{"a":1, 2:"test"}]))