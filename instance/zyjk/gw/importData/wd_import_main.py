# coding=utf-8
# *****************************************************************
# Author     : John
# Created on : 2024-3-11
# Description: 万达导入公卫字段比对自动化
# 【腾讯文档】万达导入公卫字段比对自动化
# https://docs.qq.com/sheet/DYnlJdlpKZFRkRkhx?tab=9e0apl
# *****************************************************************

from Wd_import_PO import *
wd_import_PO = Wd_import_PO()


# todo 1, 导入比对数据
# wd_import_PO.excel2db(Configparser_PO.FILE("case"), Configparser_PO.FILE("sheetName"))

# # todo 2，执行
wd_import_PO.run()


