# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# http://172.21.200.150/article-2123-3.html
# 关于列表复制，如 将a列表复制成b列表，应该是 a = list(b)
# 而 a = b 则是引用，只是创建了一个新的标签b，然后将其指向a所指向的列表。
# 因为 list()是列表构造函数。它会在传入的数列基础上新建一个列表。数列不一定是列表，它可以是任何类型的数列。
# *********************************************************************

import numpy
from PO.CharPO import *
Char_PO = CharPO()
import re


class ListPO():

    def __init__(self):
        pass

    # 1,一个列表拆分成多个数组
    def listSplitArray(self, varList, varArrayNum):
        try:
            return numpy.array_split(varList, varArrayNum)
        except:
            return None

    # 2,一个列表拆分成多个子列表
    def listSplitSubList(self, varList, varGroupNum):
        # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'],2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
        # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
        # print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'],5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。
        try:
            list_of_groups = zip(*(iter(varList),) * varGroupNum)
            end_list = [list(i) for i in list_of_groups]
            count = len(varList) % varGroupNum
            end_list.append(varList[-count:]) if count != 0 else end_list
            return end_list
        except:
            return None

    # 3,列表元素合并 ？
    # 问题：元素不能是数字 ，待解决？
    def listJointElement(self, varList, varMergeNums):
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
                while i <= varMergeNums:
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

    # 4,列表内容替换 ?
    # 问题：列表中数字元素会改为字符串元素，待解决？
    def listReplace(self, varList, varSource, varDest):
        try:
            return ([''.join([i for i in str(a).replace(varSource, varDest)]) for a in varList])
        except:
            return None

    # 5,列表内容替换（自动去掉特殊符号如 \t \r \n）
    def listReplaceSmart(self, varList, varSource, varDest):
        # 注意：只适用于字符串内容，如列表中元素是数字类型的，则转换成字符串，如 123 转为 “123”
        try:
            return ([''.join([i.strip() for i in str(a).strip().replace(varSource, varDest)]) for a in varList])
            # return ([' '.join([i.strip() for i in a.strip().split(varSplit)]) for a in varList])
        except:
            return None

    # 6，列表元素替换并删除
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

    # 7，删除列表中包含关键字的元素
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

    # 8，键值对齐
    def listKeyValueAlign(self, l_src, varSplit):
        # list1 = List_PO.listKeyValueAlign(
        #     ['1234567890:john', '123456:测试', '123:baibai', '600065:', '600064:234j2po4j2oi34'], ":")
        # for i in range(len(list1)):
        #     print(list1[i])
        #
        # list1 = List_PO.listKeyValueAlign(
        #     ['1234567890,john', '123456,测试', '123,baibai', '600065', '600064,234j2po4j2oi34'], ",")
        # for i in range(len(list1)):
        #     print(list1[i])

        # 1234567890: john
        # 123456    : 测试
        # 123       : baibai
        # 600065    :
        # 600064    : 234j
        l1 = []
        l2 = []
        try:
            for i in range(len(l_src)):
                varCount = l_src[i].count(varSplit)
                if varCount == 1 :
                    l1.append(str(l_src[i]).split(varSplit)[0])  # key
                    l2.append(str(l_src[i]).split(varSplit)[1])  # value
                elif varCount > 1:
                    for j in range(0, len(str(l_src[i]).split(varSplit))-1, 2):
                        l1.append(str(l_src[i]).split(varSplit)[j].replace(":", ""))  # key
                        l2.append(str(l_src[i]).split(varSplit)[j + 1].replace(":", ""))  # value
                else:
                    l1.append(str(l_src[i]).replace("(", "（").replace(")", "）").replace(":", ""))  # key
                    l2.append("")  # value

            # print(l1)
            # print(l2)
            # 排版
            count = 0
            for i in range(len(l1)):
                if len(l1[i]) > count:
                    count = len(l1[i])
            for i in range(len(l1)):
                if Char_PO.isChinese(l1[i]):
                    # 全部是汉字
                    if count != len(l1[i]):
                        l1[i] = l1[i] + "  " * (count - len(l1[i])) + ":"
                    else:
                        l1[i] = l1[i] + ":"
                elif Char_PO.isContainChinese(l1[i]):
                    # 部分是汉字 ? 未处理 同上
                    l1[i] = l1[i] + "  " * (count - len(l1[i])) + ":"
                else:
                    # 全部是非汉字
                    l1[i] = l1[i] + " " * (count - len(l1[i])) + ":"
            # print(l1)
            # print(l2)
            c = [i + j for i, j in zip(l1, l2)]
            return(c)
        except:
            return None

    # 9，列表转字典 (列表形式符合字典要求key:value)
    def listKeyValue2dict(self, varList):
        # 注意：元素如不包含冒号，则忽略此元素
        # print(List_PO.listKeyValue2dict(['a:123', 'b:456', 'c:789']))  # {'a': '123', 'b': '456', 'c': '789'}
        # print(List_PO.listKeyValue2dict(['a:123', '123b456', 'c:555']))  # {'a': '123', 'c': '555'}   //不符合条件的列表值被过滤。
        dict3 = {}
        try:
            for item in varList:
                if ":" in item:
                    keys = item.split(':')
                    dict3.update({keys[0]: keys[1]})
            return (dict3)
        except:
            return None

    # 10，列表 转 字典 (一个列表相邻两元素组成键值对队)
    def list2dict(self, varList):
        # 一个列表相邻两元素组成键值对队
        # 注意：列表元素如遇奇数，则忽略最后1个元素，元素必须大于2个。
        # print(List_PO.list2dict(["a", "123", "b", "345", "c", "777"]))  # {'a': '123', 'b': '345', 'c': '777'}
        # print(List_PO.list2dict(["a", "123", "b", "345", "c", "777", "d"]))  # {'a': '123', 'b': '345', 'c': '777'}  //最后多余的列表值被忽略
        # print(List_PO.list2dict(["a"]))  # None
        dict4 = {}
        if len(varList) < 2 :
            return None
        elif len(varList) % 2 == 0:
            for i in range(0, len(varList), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4
        else:
            for i in range(0, len(varList[:-1]), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4

    # 11，两列表合成一个字典
    def listMergeDict(self, varList1, varList2):
        # print(List_PO.listMergeDict([1, 2, 3], ['haha', 'skducn', 'yoyo']))  # {1: 'haha', 2: 'skducn', 3: 'yoyo'}
        # py3.x中
        return (dict(map(lambda x, y: [x, y], varList1, varList2)))
        # # py2.x中
        # return (dict(zip(varList1, varList2)))

    # 12，列表中，字符元素转数字，数字元素转字符
    def list2partValue(self, varList, varMode="str"):
        # print(List_PO.list2partValue([123], "str"))  # ['123']
        # print(List_PO.list2partValue(["a", 123.56, 0.12], "str"))  # ['a', '123.56', '0.12']
        # print(List_PO.list2partValue([1, 3, '13', "一二", 20], "str"))  # ['1', '3', '13', '一二', '20']
        # print(List_PO.list2partValue(['123'], "digit"))  # [123]
        # print(List_PO.list2partValue(["a", "123", "555"], "digit"))  # ['a', 123, 555]
        # print(List_PO.list2partValue([1, 3, '13', "一二", 20], "digit"))  # [1, 3, 13, '一二', 20]
        # print(List_PO.list2partValue(["a", "0.123", "123.00", "56.0", "555.455678"], "digit"))  # ['a', 0.123, 123.0, 56.0, 555.455678]
        new_numbers = []
        if varMode == "digit":
            for i in range(len(varList)):
                if self.is_number(varList[i]):
                    if str(varList[i]).isdigit():
                         new_numbers.append(int(varList[i]))
                    else:
                        new_numbers.append(float(varList[i]))
                else:
                    new_numbers.append(varList[i])
            return new_numbers
        else:
            return [str(i) for i in varList]

    # 13, 列表 转 字符串
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

    # 判断字符串中元素类型
    def is_number(self, s):
        # 字符串中元素是数字（浮点数），long类型 或 complex的 则返回True，否则返回False
        # 注意：python2中有long类型， python3中没有long类型，只有int类型
        # print(List_PO.is_number("100"))  # True
        # print(List_PO.is_number("12.3456"))  # True
        # print(List_PO.is_number("abd123"))  # False
        try:
            complex(s)
        except ValueError:
            return False
        return True


if __name__ == "__main__":

    List_PO = ListPO()

    print("1，一个列表拆分成3个数组".center(100, "-"))
    varArr = List_PO.listSplitArray([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    print(varArr)  # [array([1, 2, 3]), array([4, 5, 6]), array([7, 8, 9])]
    print(varArr[1][2])  # 6  //定位数组元素
    print(len(varArr))  # 3
    for i in range(len(varArr)):
        print(varArr[i])
    # [1 2 3]
    # [4 5 6]
    # [7 8 9]


    print("2，一个列表拆分成多个子列表".center(100, "-"))
    print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
    print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
    print(List_PO.listSplitSubList(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。


    print("3，列表中相邻部分元素合并(列表必须是字符串)".center(100, "-"))
    print(List_PO.listJointElement(["a", "b", "c"], 4))  # ['abc']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
    print(List_PO.listJointElement(["a", "b", "c", "d"], 4))  # ['abcd']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
    print(List_PO.listJointElement(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']  //列表中每4个元素合并在一起，最后不足4个元素则合并在一起
    print(List_PO.listJointElement(["a", "b", 123, "d", "e", "f"], 4))  # None  //列表元素必须是字符串，否则返回None
    print(List_PO.listJointElement(["www.", "baidu.", "com"], len(["www.", "baidu.", "com"])))  # ['www.baidu.com']


    print("4，替换列表元素".center(100, "-"))
    print(List_PO.listReplace(["1", 2, "3", ":"], ":", ""))  # ['1', '2', '3', ''] ？2变成字符串？
    print(List_PO.listReplace(['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误'], "\n", ":"))   #  ['0:编号 规则', '1:既往史记录 逻辑 错误', '2:既往史\t:逻辑错误']
    print(List_PO.listReplace(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  #['\nCHF\xa0\r\n\r\n  64.90', '\nCHF\xa0\r\n58.40', '\nCHF\xa0\r48.70']


    print("5，替换列表元素（自动去掉特殊符号如 \t \r \n）".center(100, "-"))
    print(List_PO.listReplaceSmart(['0\n编号', '1\n既往史', 444, '2\n既往史\t\n逻辑', 'abc'], "abc", ":"))   #  ['0编号规则', '1既往史记录逻辑错误', '444', '2既往史逻辑错误', ':']
    print(List_PO.listReplaceSmart(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  # ['CHF64.90', 'CHF58.40', 'CHF48.70']


    print("6，列表内容替换并删除".center(100, "-"))
    print(List_PO.listReplaceDelElement(["1", 2, "3", ":"], ":", "", ""))   # ['1', '2', '3']   //将 ：替换成空，再删除空元素。


    print("7，删除列表中包含关键字的元素".center(100, "-"))
    list1 = ['0\n编号 规则', "错误", '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误', 'abc', "错误"]
    print(List_PO.listDelElement(list1, "错误"))  # ['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误', 'abc']  // 精准删除，删除“错误”元素
    print(List_PO.listDelElement(list1, "错误", "vague"))  # ['0\n编号 规则', 'abc']  //模糊删除，删除包含“错误”的元素。
    print(list1)  # 原值不变


    print("8，键值对齐".center(100, "-"))
    list1 = List_PO.listKeyValueAlign(['1234567890:john', '123456:测试', '123:baibai', '600065:', '600064:234j2po4j2oi34'],":")
    for i in range(len(list1)):
        print(list1[i])

    list1 = List_PO.listKeyValueAlign(['1234567890,john', '123456,测试', '123,baibai', '600065', '600064,234j2po4j2oi34'],",")
    for i in range(len(list1)):
        print(list1[i])


    print("9，列表 转 字典（['key:value', 'key2:valur']格式）".center(100, "-"))
    print(List_PO.listKeyValue2dict(['a:123', 'b:456', 'c:789']))  # {'a': '123', 'b': '456', 'c': '789'}
    print(List_PO.listKeyValue2dict(['a:123', '123b456', 'c:555']))  # {'a': '123', 'c': '555'}   //不符合条件的列表值被过滤。


    print("10，列表 转 字典 (一个列表相邻两元素组成键值对队)".center(100, "-"))
    print(List_PO.list2dict(["a", "123", "b", "345", "c", "777"]))  # {'a': '123', 'b': '345', 'c': '777'}
    print(List_PO.list2dict(["a", "123", "b", "345", "c", "777", "d"]))  # {'a': '123', 'b': '345', 'c': '777'}  //最后多余的列表值被忽略
    print(List_PO.list2dict(["a"]))  # None


    print("11，两列表合成一个字典".center(100, "-"))
    print(List_PO.listMergeDict([1, 2, 3], ['haha', 'skducn', 'yoyo']))  # {1: 'haha', 2: 'skducn', 3: 'yoyo'}


    print("12，将列表元素是数字类型的字符串转数字".center(100, "-"))
    print(List_PO.list2partValue([123], "str"))  # ['123']
    print(List_PO.list2partValue(["a", 123.56, 0.12], "str"))    # ['a', '123.56', '0.12']
    print(List_PO.list2partValue([1, 3, '13', "一二", 20], "str"))    # ['1', '3', '13', '一二', '20']
    print(List_PO.list2partValue(['123'], "digit"))    # [123]
    print(List_PO.list2partValue(["a", "123", "555"], "digit"))    # ['a', 123, 555]
    print(List_PO.list2partValue([1, 3, '13', "一二", 20], "digit"))    # [1, 3, 13, '一二', 20]
    print(List_PO.list2partValue(["a", "0.123","123.00", "56.0", "555.455678"], "digit"))    # ['a', 0.123, 123.0, 56.0, 555.455678]


    print("13，列表转字符串".center(100, "-"))
    print(List_PO.list2str(['h', 'e', 'l', 'l', 'o']))  # hello
    print(List_PO.list2str([1, 3, 5, 7, 8, 20]))   # 1357820
    print(List_PO.list2str([1, 3, "test", "12", "中国", 20]))   # 13test12中国20
    print(List_PO.list2str([100]))   # 100
    print(List_PO.list2str([100, [1, 2, 3]]))   # 100[1, 2, 3]   //列表中嵌列表
    print(List_PO.list2str([100, (1, 2, 3)]))   # 100(1, 2, 3)   //列表中嵌元组
    print(List_PO.list2str([100, 200, [1, 2, 3], {'a': 1, "b": 2}, 500]))   # 100200[1, 2, 3]{'a': 1, 'b': 2}500  //列表中嵌字典
    print(List_PO.list2str(213123213))   # None   //错误参数返回None
    print(List_PO.list2str())   # None   //无参数返回None