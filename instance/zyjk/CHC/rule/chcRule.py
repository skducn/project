# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-10-20
# Description: 社区健康管理中心规则自动化cmd脚本
#【腾讯文档】健康评估规则表自动化 https://docs.qq.com/sheet/DYkZUY0ZNaHRPdkRk?tab=sf3rdj
# 社区健康管理中心登录 http://192.168.0.243:8010/login#/login
# 健康档案接口文档 http://192.168.0.243:8014/doc.html
# Swagger http://192.168.0.243:8012/swagger-ui/index.html#/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# nacos  http://192.168.0.223:8848/nacos/#/serviceDetail?name=chc-auth&groupName=DEFAULT_GROUP
# open /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CHC/rule/健康评估规则表自动化1.xlsx

# conda activate py308
# cd /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CHC/rule
# python chcRule.py -t $1 -i $2 -l $(3:-off)
# chcRule.sh jkpg 1 on
# chcRule.sh jkpg 1-4 on
# chcRule.sh jkpg error
#***************************************************************

import sys
sys.path.append('../../../../')

from Sql_chcPO import *
import threading
import argparse, ast


parser = argparse.ArgumentParser(usage="程序用途描述", description='帮助文档的描述', epilog="额外说明")
parser.add_argument('--table', '-t', help='数据库表表名，必要参数', required=True)
parser.add_argument('--id', '-i', help='id，必要参数', required=True)
parser.add_argument('--log', '-l', help='日志，非必要参数')
args = parser.parse_args()

# todo -s jkpg
try:
    d = {'jkpg': '健康评估', 'jkgy': '健康干预',  'zytzbs': '中医体质辨识', 'etjkgy': '儿童健康干预', 'jbpg': '疾病评估'}
    r = Sql_chcPO(d[args.table])  # # r = Sql_chcPO("健康评估")
except:
    sys.exit(0)

# todo 参数-p on｜off(默认值)
if args.log == "on":
    Configparser_PO.write('SWITCH', 'printsql', 'on')
else:
    Configparser_PO.write('SWITCH', 'printsql', 'off')


# todo 参数-n 1 ｜ 1-N
if args.id == "error":
    r.runResult("error")
elif args.id == "ok":
    r.runResult("ok")
elif args.id == "all":
    r.runResult("all")
else:
    if "-" in (args.id):
        start = int((args.id).split("-")[0])
        end = int((args.id).split("-")[1])
        if start < end:
            for i in range(start, end+1):
                r.run(i)
        else:
            for i in range(end, start+1):
                r.run(i)
    else:
        r.run(args.id)


