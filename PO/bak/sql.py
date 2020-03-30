# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2017-11-16
# Description: 用于 python命令行 搜索关键字，返回对应的表、行数、记录信息1111
# *******************************************************************************************************************************

import sys, os, platform
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# from Public.PageObject.DatabasePO import *
from PO import DatabasePO,cmdColor

'''数据库信息'''
# object = [['10.111.3.4', 3306, 'cetc', '20121221', 'cetc_sy', 'testsy']]

object = [['140.143.94.177', 3306, 'cetc', '20121221', 'cetc_sy', 'presy'],
          ['10.111.3.4', 3306, 'cetc', '20121221', 'cetc_sy', 'testsy']
          ]

def printColor(macColor, winColor, varContent):
    if platform.system() == 'Darwin':
        print(macColor) + varContent + '\033[0m'
    if platform.system() == 'Windows':
        (eval(winColor))(varContent.encode('gb2312') + "\n")

# *******************************************************************************************************************************
varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"
varFORMAT = u"语法：sql -command 数据库.表[*|%|#] [关键字*|%|#] [条件1-2]\n\n"\
u"通配符 *|%|#中  * 表示所有 , % 前缀符 , # 忽略符\n"
varDEMO = u"例子: \n" \
u"  sql -sk|-sf|-sk hjk.* char 66600%  // 搜索所有的表 , 字符类型 注意：mac机上,星号两侧有单引号 ，如 ‘*’\n"\
u"  sql -sk|-sf|-sk hjk.tt_store char 666001   // 搜索tt_store指定的表, 类型包括 int,char,tinyint,smallint,timestamp,varchar,double,datetime \n"\
u"  sql -sk|-sf|-sk hjk.tt_% datetime 2018-05-28%   // 搜索tt_开头的表，日期类型\n"\
u"  sql -sk|-sf|-sk hjk.#tt_store 666001  // 搜索忽略tt_store表\n"\
u"  sql -sk|-sf|-sk hjk.#tt_% 666001  // 搜索忽略tt_开头的表\n"\
u"  sql -sk|-sf|-sk hjk.#tt_qa,tt_picture 666001  // 搜索忽略指定的2张表（表之间用逗号分隔），注意：mac机上，#号两侧有单引号，如 '#tt_qa,tt_picture'\n"\
u" \n" \
u"  sql -ss hjk.tt_store *    // 显示tt_store表所有（字段、类型、备注）结构\n"\
u"  sql -ss hjk.tt_store name  //显示tt_store表中某个字段的类型、备注\n"\
u"  sql -ss hjk.tt_store store_id,org_id,name  //显示tt_store表中多个字段的类型、备注 （字段之间用逗号分隔）\n"\
u"  sql -ss hjk.* name  //显示所有表中带name字段的类型、备注\n"\
u"  sql -ss hjk.* store_id,name  //显示所有表中多个字段的类型、备注\n"\
u"  sql -ss hjk.tt_s% store_id,name  //显示tt_s开头表中多个字段的类型、备注\n"\
u"  sql -ss hjk.tt_s% *  //显示tt_s开头表中所有字段的类型、备注\n"\
u"  sql -sw hjk.tt_store status store_id=1  //搜索1个条件返回1个字段列表\n"\
u"  sql -sw hjk.tt_store * store_id=1  //搜索1个条件返回所有字段列表\n"\
u"  sql -sw hjk.tt_store status user_name=666001,store_id=1 //搜索2个条件返回1字段列表(条件中逗号分隔表示and)\n"\
u"  sql -sw hjk.tt_store status,user type_name=666001!store_id=1 //搜索2个条件返回2个字段列表(条件中感叹号分隔表示or，字段间用逗号分隔，最多5个字段)\n"\
u" \n" \
u"  sql -sc hjk.tt_store // 统计表记录数\n" \
u"  sql -scw hjk.tt_store user_name=666001\n" \
u"  sql -uw hjk.tt_store is_need_approve=1 store_id=1  //依据1个条件更新1个字段值\n"\
u"  sql -uw hjk.tt_store is_need_approve=1 store_id=1,user_name=666001  //以及2个条件更新1个字段值(条件中逗号分隔表示and)\n"\
u"  sql -uw hjk.tt_store is_need_approve=1 store_id=1!user_name=666001  //以及2个条件更新1个字段值(条件中感叹号分隔表示or)\n"\

varParam = u"-command 使用说明：\n"\
u"  -sk 搜索关键字，显示记录 (select keyword)\n" \
u"  -sf 搜索关键字，显示带字段的记录 (select field)\n" \
u"  -sl 搜索关键字，显示带DDL的记录 (select list)\n" \
u"  -ss 搜索表结构 (select structure)\n" \
u"  -sc 返回统计表记录数 (select count)\n" \
u"  -scw 返回统计表记录数带1个条件(select count where)\n" \
u"  -sw  搜索1个或2个条件后返回1个或2个值\n" \
u"  -uw 搜索1个或2个条件后更新1个值\n" \

for i in range(0, len(object)):
    try:
        if object[i][5] == str(sys.argv[2]).split(".")[0]:
            Database_PO = DatabasePO(object[i][0], object[i][1], object[i][2], object[i][3], object[i][4])
            try:
                # 搜索关键字
                if sys.argv[1] == "-sk":
                    Database_PO.selectKeyword(str(sys.argv[2]).split(".")[1], sys.argv[3], sys.argv[4])

                # 搜索带字段的关键字 （方法如 -sk）
                if sys.argv[1] == "-sf":
                    Database_PO.selectField(str(sys.argv[2]).split(".")[1], sys.argv[3], sys.argv[4])

                # 搜索带DDL字段的关键字（方法如 -sk）
                if sys.argv[1] == "-sl":
                    Database_PO.selectDDL(str(sys.argv[2]).split(".")[1], sys.argv[3], sys.argv[4])

                # 搜索表结构
                if sys.argv[1] == "-ss":
                    Database_PO.selectStructure(str(sys.argv[2]).split(".")[1], sys.argv[3])

                # 搜索带条件后返回结果
                if sys.argv[1] == "-sw":
                    for i in range(0, len(object) - 1):
                        try:
                            if object[i][4] == str(sys.argv[2]).split(".")[0]:
                                Database_PO = DatabasePO(object[i][0], object[i][1], object[i][2], object[i][3],object[i][4])
                                Database_PO.selectW(str(sys.argv[2]).split(".")[1], sys.argv[3], sys.argv[4])
                        except:
                            if len(sys.argv) != 5:
                                printColor('\033[1;31;47m', 'printRed', u"错误，缺少参数数量，请检查参数，如 sql -sw 数据库.表 字段[,字段2,字段3] 条件=值[,条件2=值]")
                            elif u"=" not in sys.argv[4]:
                                printColor('\033[1;31;47m', 'printRed', u"错误，条件格式错误，如：字段=值")
                            else:
                                printColor('\033[1;31;47m', 'printRed', u"错误，某个字段不存在或条件格式错误！")

                # 搜索1个条件返回统计数量
                if sys.argv[1] == "-scw":
                    for i in range(0, len(object) - 1):
                        try:
                            if object[i][4] == str(sys.argv[2]).split(".")[0]:
                                Database_PO = DatabasePO(object[i][0], object[i][1], object[i][2], object[i][3],object[i][4])
                                print(Database_PO.rtnCountW(str(sys.argv[2]).split(".")[1], sys.argv[3]))
                        except:
                            if len(sys.argv) != 4:
                                printColor('\033[1;31;47m', 'printRed', u"错误，参数数量与预期数量（3）不一致。\n")
                                print(varFORMAT)
                                print(varDEMO)

                # 搜索表统计表数量
                if sys.argv[1] == "-sc":
                    for i in range(0, len(object)-1):
                        try:
                            if object[i][4] == str(sys.argv[2]).split(".")[0]:
                                Database_PO = DatabasePO(object[i][0], object[i][1], object[i][2], object[i][3],object[i][4])
                                print(Database_PO.rtnCount(str(sys.argv[2]).split(".")[1]))
                        except:
                            if len(sys.argv) != 3:
                                printColor('\033[1;31;47m', 'printRed', u"错误，参数数量与预期数量（2）不一致。\n")
                                print(varFORMAT)
                                print(varDEMO)

                # 更新字段值
                if sys.argv[1] == "-uw":
                    for i in range(0, len(object)-1):
                        try:
                            if object[i][4] == str(sys.argv[2]).split(".")[0]:
                                Database_PO = DatabasePO(object[i][0], object[i][1], object[i][2], object[i][3],object[i][4])
                                Database_PO.updateW(str(sys.argv[2]).split(".")[1], sys.argv[3], sys.argv[4])
                        except:
                            if len(sys.argv) != 5:
                                printColor('\033[1;31;47m', 'printRed', u"错误，参数数量与预期数量（4）不一致。\n")
                                print(varFORMAT)
                                print(varDEMO)

            except:
                if len(sys.argv) != 5:
                    printColor('\033[1;31;47m', 'printRed', varERROR)
                    printColor('\033[1;31;47m', 'printYellow', varFORMAT)

    except:
        if len(sys.argv) == 1:
            printColor('\033[1;31;47m', 'printGreen', u"Version: 1.3.0 2018-5-29\n")
            printColor('\033[1;31;47m', 'printYellow', varFORMAT)
            print(varParam)
            print(varDEMO)
        break
