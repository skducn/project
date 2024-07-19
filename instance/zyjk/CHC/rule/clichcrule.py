# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-10-20
# Description: 社区健康规则自动化 cli脚本
#【腾讯文档】社区健康规则自动化 https://docs.qq.com/sheet/DYkZUY0ZNaHRPdkRk?scene=ecc60f85696bdecefee4fce04Rykr1&tab=j7ir8j
# 社区健康管理中心 http://192.168.0.243:8010/login#/login
# 健康档案接口文档 http://192.168.0.243:8014/doc.html
# Swagger http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST

# todo Alfred中输入 "clichcrule 健康评估 1 "，执行以下脚本
# todo Alfred中输入 "clichcrule 健康评估 1-10 "，执行以下脚本
# todo Alfred中输入 "clichcrule 健康评估 error "，执行以下脚本
# conda activate py308
# cd /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CHC/rule
# python clichcrule.py -t a_jiankangpinggu -i 1 -l off

# clichcrule.sh（未测试）
# python clichcrule.py -t $1 -i $2 -l $(3:-off)
# clichcrule.sh a_jiankangpinggu 1 on
# clichcrule.sh a_jiankangpinggu 1-4 on
# clichcrule.sh a_jiankangpinggu error on
#***************************************************************

import sys
sys.path.append('../../../../')
from ChcrulePO import *
import threading
import argparse, ast

# print(sys.argv[2])
# sys.exit(0)

# 步骤1
r = ChcrulePO(sys.argv[1])

# 步骤2, 默认off
if len(sys.argv) == 3 :
    Configparser_PO.write('SWITCH', 'printsql', 'off')
else:
    if sys.argv[3] == "on":
        Configparser_PO.write('SWITCH', 'printsql', 'on')
    else:
        Configparser_PO.write('SWITCH', 'printsql', 'off')

# 步骤3
try:
    if sys.argv[2] == "error":
        r.runResult("error")
    elif sys.argv[2] == "ok":
        r.runResult("ok")
    elif sys.argv[2] == "all":
        r.runResult("all")
    else:
        if "-" in (sys.argv[2]):
            start = int((sys.argv[2]).split("-")[0])
            end = int((sys.argv[2]).split("-")[1])
            if start < end:
                for i in range(start, end+1):
                    r.run(i)
            else:
                for i in range(end, start+1):
                    r.run(i)
        else:
            r.run(sys.argv[2])

except:
    sys.exit(0)


# ***************************************************************
# 以下使用 "argparse" 实现：

# parser = argparse.ArgumentParser(usage="程序用途描述", description='帮助文档的描述', epilog="额外说明")
# parser.add_argument('--table', '-t', help='sheetName，必要参数', required=True)
# parser.add_argument('--id', '-i', help='id行号，必要参数', required=True)
# parser.add_argument('--log', '-l', help='步骤日志，非必要参数')
# args = parser.parse_args()

# 步骤1
# r = Chc_rule_PO(args.table)

# 步骤2
# if args.log == "on":
#     Configparser_PO.write('SWITCH', 'printsql', 'on')
# else:
#     Configparser_PO.write('SWITCH', 'printsql', 'off')


# 步骤3， 1 ｜ 1-N
# if args.id == "error":
#     r.runResult("error")
# elif args.id == "ok":
#     r.runResult("ok")
# elif args.id == "all":
#     r.runResult("all")
# else:
#     if "-" in (args.id):
#         start = int((args.id).split("-")[0])
#         end = int((args.id).split("-")[1])
#         if start < end:
#             for i in range(start, end+1):
#                 r.runRow(i)
#         else:
#             for i in range(end, start+1):
#                 r.runRow(i)
#     else:
#         r.runRow(args.id)



