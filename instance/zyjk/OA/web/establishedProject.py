# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-3-31
# Description: 项目立项
# 测试环境：192.168.0.233
#***************************************************************

import os, sys
# sys.path.append("../../../../")
from instance.zyjk.OA.PageObject.OaPO import *
Oa_PO = OaPO()
List_PO = ListPO()
Time_PO = TimePO()
Net_PO = NetPO()
Data_PO = DataPO()
File_PO = FilePO()
Char_PO = CharPO()


# 项目立项
varNo = Oa_PO.flowScheme("项目基础信息", ["刘霞", "saas11", "2020-02-12", "2020-02-15", "董兰强"])
Oa_PO.flowScheme("需求分析", ["董兰强",  "刘霞", "2020-3-20", "需求分析文档", "2020-2-21", "董兰强", varNo])
Oa_PO.flowScheme("产品调研", ["董兰强", "刘霞", "2020-5-21", "产品调研文档", "2020-2-21", "董兰强", varNo])
Oa_PO.flowScheme("竞品分析", ["董兰强", "刘霞", "2020-6-21", "竞品分析文档", "2020-2-21", "董兰强", varNo])
Oa_PO.flowScheme("产品设计", ["董兰强", "刘霞", "2020-7-21", "产品设计文档", "2020-2-21", "王磊", varNo])
Oa_PO.flowScheme("研发", ["王磊", "江伟健", "2020-8-20", "研发文档", "2020-2-21", "王磊", varNo])
Oa_PO.flowScheme("测试", ["王磊", "金浩", "2020-9-20", "测试文档",  "2020-2-21", "王磊", varNo])
Oa_PO.flowScheme("实施", ["王磊", "刘耀", "2020-10-20", "实施文档", "2020-2-21",  "王磊", varNo])
Oa_PO.flowScheme("交付", ["王磊", "夏晴", "2020-11-20", "交付文档",  "2020-2-21", "李晨曦", varNo])



