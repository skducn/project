# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2022-7-19
# Description: # Whoosh：Python 的轻量级搜索工具
# 参考：http://www.51testing.com/html/60/n-7792260.html
# 默认使用 Okapi BM25F排序算法，也支持其他排序算法
# 相比于其他搜索引擎，Whoosh会创建更小的index文件；
# Whoosh中的index文件编码必须是unicode;
# Whoosh可以储存任意的Python对象。
# Whoosh的官方介绍网站为：https://whoosh.readthedocs.io/en/latest/intro.html
# 搜索的两个重要的方面为mapping和query，也就是索引的构建以及查询，背后是复杂的索引储存、query解析以及排序算法等
# 它能够提供全文检索，这依赖于排序算法，比如BM25，也依赖于我们怎样储存字段。
# pip3 install jieba,whoosh
# *****************************************************************


import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json


def x(var):


    # 1,创建schema, stored为True表示能够被检索
    schema = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),dynasty=ID(stored=True),poet=ID(stored=True),content=TEXT(stored=True, analyzer=ChineseAnalyzer()))

    # 2,解析poem.csv文件
    # with open('poem.csv', 'r', encoding='utf-8') as f:
    with open('poem.csv', 'r') as f:
        texts = [_.strip().split(',') for _ in f.readlines() if len(_.strip().split(',')) == 4]

    # 3,存储schema信息至indexdir目录
    indexdir = 'indexdir/'
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)

    # 4,按照schema定义信息，增加需要建立索引的文档
    writer = ix.writer()
    print(texts)
    # print(texts[0][0])


    for i in range(1, len(texts)):
        title2, dynasty2, poet2, content2 = texts[i]
        # writer.add_document(title=title2, dynasty=dynasty2, poet=poet2, content=content2)
        tt = {texts[0][0]: title2, texts[0][1]: dynasty2, texts[0][2]: poet2, texts[0][3]: content2}
        writer.add_document(**tt)
    writer.commit()

    # 5,创建一个检索器
    searcher = ix.searcher()
    # 检索content中出现'明月'的文档
    results = searcher.find("content", var)
    # results = searcher.find("dynasty", var)
    print('一共发现%d份文档。' % len(results))
    # for i in range(min(10, len(results))):
    for i in range(len(results)):
        # print(json.dumps(results[i].fields(), ensure_ascii=False))
        print(results[i].fields())


# x("唐代")
x("寞红")