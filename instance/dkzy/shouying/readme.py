# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-6-6
# Description: 首营 各脚本说明
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PageObject.ShouyingPO import *

printColor('\033[1;32;47m', 'printSkyBlue', u"首营脚本: 2.0.1 2018-7-6\n")

printColor('\033[1;31;47m', 'printGreen', "1、注册账号（1 = 生产企业，2 = 经营企业，3 = 公立医院，4 = 私立医院，5 = 诊所，6 = 零售药店）")
print u"   register 15016109051 1     //注册生产企业\n"

printColor('\033[1;31;47m', 'printGreen', "2、资料认证 ")
print u"   authenticate 14616109051\n"

printColor('\033[1;31;47m', 'printGreen', "3、审核认证（pass = 通过，refuse = 拒绝） ")
print u"   approve 14616109053 pass|refuse \n"

printColor('\033[1;31;47m', 'printGreen', "4、新增及设置普管（new = 新增，remove = 移出）")
print u"   setManager 14616109053 new ?     //随机生成一个普管"
print u"   setManager 14616109053 remove 13816109052      //移出13816109052普管\n"

printColor('\033[1;31;47m', 'printGreen', "5、企业及品种首营交换设置（ all = 全选， ? = 手工输入）")
print u"   setExchange 14616109053 all|? \n"

printColor('\033[1;31;47m', 'printGreen', "6、发起企业首营（上游企业对下游企业发起首营交换）")
print u"   faqishouying 14616109051 14616109053      //14616109051对14616109053发起企业首营\n"

printColor('\033[1;31;47m', 'printGreen', "7、新增产品（生产企业新增或经营企业代为新增，1 = 药品，2 = 中药饮片，3 = 化妆品，4 = 食品，5 = 日用品，6 = 消毒产品，7 = 保健食品，8 = 医疗器械）")
print u"   addProduct 14616109051 ? 3 面膜     //生产企业新增面膜产品，"
print u"   addProduct 14616109051 14616109052 1 阿司匹林     //经营企业代为新增阿司匹林产品\n"

printColor('\033[1;31;47m', 'printGreen', "8、审核产品（管理员13816109050审核产品，pass = 通过，refuse = 拒绝）")
print u"   productApprove 面膜 pass|refuse     //审核面膜产品\n"

printColor('\033[1;31;47m', 'printGreen', "9、药检单（新建药检单、发送药检单、接收/拒绝药检单、继续发送给下游企业[经营、公立、私立、诊所、零售药房]）,pass = 通过，refuse = 拒绝")
print u"   drugList 15016109051 15016109052 15016109053 维生素 pass|refuse     \n"

printColor('\033[1;31;47m', 'printGreen', "10、发起品种首营（上游企业给下游企业发起品种首营）")
print u"   faqiProduct 15016109051 15016109052 维生素 \n"

printColor('\033[1;31;47m', 'printGreen', "11、特药出入库（上游企业给下游企业发起品种首营）")
print u"   stockInOut 15016109051 15016109052 15016109053 消毒产品\n"

printColor('\033[1;31;47m', 'printGreen', "12、特殊药品流向登记")
print u"   drugFlowRegister 15016109052 \n"


