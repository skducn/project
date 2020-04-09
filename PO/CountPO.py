# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-9
# Description   : 计算模块

# *********************************************************************
import round

class CountPO():

    def __init__(self):
        pass


    def purge(self):
        # 清空缓存中的正则表达式
        re.purge()

if __name__ == "__main__":

    Re_PO = RePO()

    print(Re_PO.subBlank("JGood is a handsome boy, he is cool, clever, and so on...", ""))   # 去掉字符串中的空格 JGoodisahandsomeboy,heiscool,clever,andsoon...
    print(Re_PO.split_list("JGood is a handsome boy, he is cool, clever, and so on...", r'\W+', 0)) # ['JGood', 'is', 'a', 'handsome', 'boy', 'he', 'is', 'cool', 'clever', 'and', 'so', 'on', '']
    print(Re_PO.split_list("JGood is a handsome boy, he is cool, clever, and so on...", r'(\W+)', 0))
    x = (Re_PO.split_list("0etrerta3B9", '[a-z]+', 0))  # ['0', '3', '9']
    print(Re_PO.findall_list("JGood is a handsome boy, he is cool, clever, and so on...", r'\w*oo\w*'))  # 匹配所有包含'oo'的单词 ， ['JGood', 'cool']
