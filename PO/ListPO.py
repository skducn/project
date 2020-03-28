# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# http://172.21.200.150/article-2123-3.html
# *********************************************************************

import numpy
from PO.CharPO import *
Char_PO = CharPO()
import re


class ListPO():

    def __init__(self):
        pass

    # 1,一个列表拆分成多个数组
    def list2Array(self, varList, varArrayNum):
        return numpy.array_split(varList, varArrayNum)

    # 2,一个列表拆分成多个子列表
    def list2SubList(self, varList, varGroupNum):
        list_of_groups = zip(*(iter(varList),) * varGroupNum)
        end_list = [list(i) for i in list_of_groups]
        count = len(varList) % varGroupNum
        end_list.append(varList[-count:]) if count != 0 else end_list
        return end_list

    # 3,列表合并字符串元素
    def list2MergeChar(self, varList, varMergeNums):
        # print(list_PO.list2MergeChar(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']
        list1 = []
        str1 = ""
        addition_number = 0
        i = 1
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

    # 4,替换列表内容（自动去掉特殊符号如 \t \r \n）
    def listReplace(self, varList, varSource, varDest):
        return ([''.join([i.strip() for i in a.strip().replace(varSource, varDest)]) for a in varList])
        # return ([' '.join([i.strip() for i in a.strip().split(varSplit)]) for a in varList])

    # 5，键值对齐
    def alignmentKey(self, l_src, varSplit):
        l1 = []
        l2 = []
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
        # print(c)

        return(c)
        # for i in range(len(c)):
        #     print(c[i])

    # 6，列表转字典 (列表形式符合字典要求key:value)
    def listColon2Dict(self, varList):
        # 注意：元素如不包含冒号，则忽略此元素
        dict3 = {}
        for item in varList:
            if ":" in item:
                keys = item.split(':')
                dict3.update({keys[0]: keys[1]})
        return (dict3)

    # 7，列表转字典 (列表中相邻两元素组成键值对队)
    def listElement2Dict(self, varList):
        # 列表中相邻两元素组成键值对队， 转字典
        # 注意：列表元素如遇奇数，则忽略最后1个元素 ， 元素必须大于2个。
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

    # 8，两列表合成一个字典
    def twoList2Dict(self, varList1, varList2):
        # py3.x中
        return (dict(map(lambda x, y: [x, y], varList1, varList2)))  # {{1: 'haha', 2: 'skducn', 3: 'yoyo'}
        # # py2.x中
        # return (dict(zip(l1, l2)))


if __name__ == "__main__":
    list_PO = ListPO()

    # 1,一个列表拆分成3个数组
    varArr = list_PO.list2Array([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    print(varArr)  # [array([1, 2, 3]), array([4, 5, 6]), array([7, 8, 9])]
    print(varArr[1][2])  # 6  //定位到元素
    print(len(varArr))  # 3
    for i in range(len(varArr)):
        print(varArr[i])
    # [1 2 3]
    # [4 5 6]
    # [7 8 9]

    # 2,一个列表拆分成多个子列表
    print(list_PO.list2SubList(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]
    print(list_PO.list2SubList(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
    print(list_PO.list2SubList(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]

    # 3,列表合并字符串元素
    print(list_PO.list2MergeChar(["a", "b", "c", "d", "e", "f"], 4))

    # 4,替换列表内容（自动去掉特殊符号如 \t \r \n）
    print(list_PO.listReplace(['0\n编号 规则', '1\n既往史记录 逻辑 错误', '2\n既往史\t\n逻辑错误'], "\n", ":"))   #  ['0:编号规则', '1:既往史记录逻辑错误', '2:既往史:逻辑错误']
    print(list_PO.listReplace(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70'], "\t", ""))  # ['CHF64.90', 'CHF58.40', 'CHF48.70']

    # 5,键值对齐
    print(list_PO.alignmentKey(['1234567890:john', '123456:测试', '123:baibai', '600065:', '600064:234j2po4j2oi34'], ":"))

    # 6,列表转字典（a:b格式）
    print(list_PO.listColon2Dict(['a:123', 'b:456', 'c:789']))  # {'a': '123', 'b': '456', 'c': '789'}
    print(list_PO.listColon2Dict(['a:123', '123b456', 'c:555']))  # {'a': '123', 'c': '555'}

    # 7，列表转字典 (列表中相邻两元素组成键值对队)
    print(list_PO.listElement2Dict(["a", "123", "b", "345", "c", "777"]))  # {'a': '123', 'b': '345', 'c': '777'}
    print(list_PO.listElement2Dict(["a", "123", "b", "345", "c", "777", "d"]))  # {'a': '123', 'b': '345', 'c': '777'}
    print(list_PO.listElement2Dict(["a"]))  # None

    # 8，两列表合成一个字典
    print(list_PO.twoList2Dict([1, 2, 3], ['haha', 'skducn', 'yoyo']))







