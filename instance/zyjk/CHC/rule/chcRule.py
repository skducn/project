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
#  python chcRule.py -s 3
# ./chcRule.sh 4-10    //执行第4到第10行记录
# ./chcRule.sh 4    //执行第4行记录
#***************************************************************

import sys
sys.path.append('../../../../')

from ChcRulePO2 import *
import threading
import argparse,ast

parser = argparse.ArgumentParser(usage="程序用途描述", description='帮助文档的描述', epilog="额外说明")
parser.add_argument('--seq', '-s', help='seq 属性，必要参数')
args = parser.parse_args()
r = ChcRulePO2("健康评估")

if "-" in (args.seq):
    start = int((args.seq).split("-")[0])
    end = int((args.seq).split("-")[1])
    if start < end :
        for i in range(start, end+1):
            r.run(i)
    else:
        for i in range(end, start+1):
            r.run(i)
else:
    r.run(args.seq)

# if args.testRule == "None":
#     r.run(int(args.seq), type(ast.literal_eval('None')))
# else:
#     r.run(int(args.seq), args.testRule)

# if __name__ == '__main__':
#     try:
#         # r = ChcRulePO({"sheetName":  "健康评估", "colTitle": ["测试结果", "测试规则", "评估规则编码"]})
#         r.run(args.result, args.testRule)
#         # test_for_sys(args.year, args.name, args.body)  # 此处调参即可
#     except Exception as e:
#         print("error")

# r.run(3, None)  # r1
# r.run(4, None)  # r6
# r.run(20, None)  # r4
# r.run(25, None)  # r3
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "健康干预", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "干预规则编码", "命中次数"]})
# r.run(3, None)  # r2
# r.run(20, None)  # r11, 命中2
# r.run(35, None)  # r5, 命中2
# r.run(44, None)  # r2, 命中2
# r.run(50, None)  # r8
# r.run(87, None)  # r7
# r.run("ERROR", "GW")
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "健康干预中医体质辨识", "colTitle": ["测试结果", "测试规则", "干预规则编码", "干预规则"]})
# r.run(2, None)  # r12

# r = ChcRulePO({"sheetName": "儿童健康干预", "colTitle": ["测试结果", "测试规则", "干预规则编码"]})
# r.run(2, None)  # r1
# r.run("ERROR", None)

# r = ChcRulePO({"sheetName": "已患和高风险疾病评估", "colTitle": ["测试结果", "测试规则", "疾病评估规则编码", "健康评估规则库编码"]})
# r.run(2, None)  # r9
# r.run(3, None)  # r10
# r.run("ERROR", "GW")
# r.run(None, "GW")
# r.run("ERROR", None)

# r.open('儿童健康干预')
