# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 接口驱动

#****************************************************************
# 使用说明:
# 1,Icase() 中参数规则及说明,
# 参数1 = 接口 + 序号 + 用例序号 , 如"I251_N6_C1" 表示 i251接口文档中序号为6的测试用例1
# 参数2 = 测试返回类型 ,
# 参数3 ~ 参数N = 依据接口实际的参数数量传递 (注意:参数3-参数N 外层需加上单引号 ' )

import os,sys,requests,xlwt,xlrd,MySQLdb,datetime,redis,smtplib
reload(sys)
sys.setdefaultencoding('utf8')
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlutils.copy import copy
from InterfaceExcel import Icase,Icommon3

connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curWeb = connWeb.cursor()
connApp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, use_unicode=True)
curApp = connApp.cursor()
connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True)
curGame = connGame.cursor()


# # [Testcase]
# print "\nI250_N6 " + ">" * 150
# # 6,我_设置_提现密码_获取设置提现密码验证码  2=提现验证码 ,4=设置提现密码 ,5=资质认证验证码
# Icase("I250_N6_C1","RtnOK","10001588",'"10001588"')
# print "\nI251_N3 " + ">" * 150
# # 3,资质认证_保存个人认证接口  关联表：t_person_certification插入一条未审核记录
# Icase("I251_N3_C1","RtnOK","10001588",'"10001588","118","pp","431222199206290017","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C2","RtnParamErr","10001588",'"","118","pp","431222199206290017","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C3","RtnSysErr","10001588",'"10001588","","pp","431222199206290017","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C4","RtnParamErr","10001588",'"10001588","118","","431222199206290017","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C5","RtnParamErr","10001588",'"10001588","118","DFDF","","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C6","RtnParamErr","10001588",'"10001588","118","DFDF","431222199206290017","","17000000020", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C7","RtnParamErr","10001588",'"10001588","118","DFDF","431222199206290017","5","", %s' % Icommon3("5","17000000020"))
# Icase("I251_N3_C8","RtnParamErr","10001588",'"10001588","118","DFDF","431222199206290017","5","17000000020", ""')
# #修改个人认证
# Icase("I251_N3_C9","RtnOK","10001588",'"10001588","118","司徒浩南","431222199206290017X","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
# curWeb.execute('delete from ukardweb.t_person_certification where userId=10001588')
# connWeb.commit()


# # # # 3,资质认证_修改个人认证接口  关联表：t_person_certification
# curWeb.execute('select id from ukardweb.t_person_certification where userId=10001588')
# tbl3= curWeb.fetchone()
# connWeb.commit()
# Icase("I251_N3_C1","RtnOK","10001588",'"10001588","118","pp","431222199206290017X","5,6,7","17000000020",%s,%s' % (tbl3[0],Icommon3("5","17000000020")))
# # # curWeb.execute('delete from ukardweb.t_person_certification where userId=10001588')
# # # connWeb.commit()

## print "\nI251_N5 " + ">" * 150
##资质认证_保存、修改店铺认证接口  关联表：实体店表t_entity_store_certification   网店表：t_web_store_certification
##需要验证一下一个群只允许存在一个网店或者实体店
# Icase("I251_N5_C1","RtnParamErr","10001588",'"","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
# Icase("I251_N5_C2","RtnParamErr","10001588",'"10001588","","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
# Icase("I251_N5_C3","RtnParamErr","10001588",'"10001588","118","","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
# Icase("I251_N5_C4","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
# Icase("I251_N5_C5","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","3","17000000020", %s,"0"' % Icommon3("5","17000000020"))
# Icase("I251_N5_C6","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","", %s,"0"' % Icommon3("5","17000000020"))
# Icase("I251_N5_C7","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020","","0"')
# Icase("I251_N5_C8","RtnOK","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000023", %s,"0"' % Icommon3("5","17000000023"))
# # 修改资质认证
# curWeb.execute('select id from ukardweb.t_entity_store_certification where groupId=118')
# tbl3= curWeb.fetchone()
# Icase("I251_N5_C9","RtnOK","10001588",'"10001588","118","4","动量","好方d法店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com", %s,"1","17000000023", %s,"0"' % (tbl3[0],Icommon3("5","17000000023")))
# curWeb.execute('delete from ukardweb.t_entity_store_certification  where groupId=118')
# connWeb.commit()


#资质认证_资质认证首页
# print "\nI251_N1 " + ">" * 150
# Icase("I251_N1_C1","RtnOK","10001588",'"118"')
# Icase("I251_N1_C2","RtnOK","",'"118"')
# Icase("I251_N1_C3","RtnParamErr","10001588",'""')


# #城市列表接口
# print "\nI251_N2 " + ">" * 150
# Icase("I251_N2_C1","RtnOK","10001588",'"1100000000"')
# Icase("I251_N2_C2","RtnOK","",'"1100000000"')
# Icase("I251_N2_C3","RtnOK","",'""')


##资质认证_个人认证信息查询接口
# print "\nI251_N4 " + ">" * 150
# Icase("I251_N4_C1","RtnOK","10001588",'"10001588","118"')
# Icase("I251_N4_C2","RtnParamErr","10001588",'"","118"')
# Icase("I251_N4_C3","RtnParamErr","10001588",'"10001588",""')

#资质认证_商户认证信息查询接口
# print "\nI251_N6 " + ">" * 150
# Icase("I251_N6_C1","RtnOK","10001588",'"10001588","118","1"')
# Icase("I251_N6_C1","RtnParamErr","10001588",'"","118","1"')
# Icase("I251_N6_C1","RtnParamErr","10001588",'"10001588","","1"')
# Icase("I251_N6_C1","RtnParamErr","10001588",'"10001588","",""')



#三藏爆款_发布爆款接口 关联表：t_explosion_product
# print "\nI251_N7 " + ">" * 150
# Icase("I251_N7_C1","RtnOK","10001588",'"118","sdfsd","5","www.baidjfu.com","1","0","0","0","0","0"')
# Icase("I251_N7_C1","RtnParamErr","10001588",'"","sdfsd","5","www.baidjfu.com","1","0","0","0","0","0"')
#？？？？？
Icase("I251_N7_C1","RtnParamErr","10001588",'"118","","","www.baidjfu.com","","0","0","","0","0"')


#三藏爆款_爆款修改接口  #关联表：t_explosion_product
# print "\nI251_N8 " + ">" * 150
# curWeb.execute('select id from ukardweb.t_explosion_product where groupId=118')
# tbl3= curWeb.fetchone()
# Icase("I251_N8_C1","RtnOK","10001588",'%s,"118","sdfsd1","5","www.baidu.com","1","0","0","0","0","0","0"' % (tbl3[0]))
# curWeb.execute('delete from ukardweb.t_explosion_product  where groupId=118')
# connWeb.commit()

# Icase("I251_N3_C1","RtnOK","10001588",'"10001588","118","pp","431222199206290017X","5,6,7","17000000020",%s,%s' % (tbl3[0],Icommon3("5","17000000020")))
#三藏爆款_我的爆款列表接口
# print "\nI251_N9 " + ">" * 150
# Icase("I251_N9_C1","RtnOK",'"118","0","20"')


#三藏爆款_我的爆款历史列表接口
# print "\nI251_N10 " + ">" * 150
# Icase("I251_N10_C1","RtnOK",'"118","0","20"')


#三藏爆款_爆款详情接口
# print "\nI251_N11 " + ">" * 150
# Icase("I251_N11_C1","RtnOK",'"118","4"')


#三藏爆款_上/下架爆款接口
# print "\nI251_N12 " + ">" * 150
# Icase("I251_N12_C1","RtnOK",'"118","4","0"')

#三藏爆款_删除爆款接口
# print "\nI251_N13 " + ">" * 150
# Icase("I251_N13_C1","RtnOK",'"4"')


#三藏爆款_爆款支付接口  需要增加一个群Id
# print "\nI251_N14 " + ">" * 150
# Icase("I251_N14_C1","RtnOK","10001588",'"10001588","4","118","3","111111"')


#销售订单_销售订单列表接口
# print "\nI251_N15 " + ">" * 150
# Icase("I251_N15_C1","RtnOK","10001588",'"118","0","0","20"')

#销售订单_确认发货接口
# print "\nI251_N16 " + ">" * 150
# Icase("I251_N16_C1","RtnOK","10001588",'"118","2016082300022"')


# #销售订单_确认退款接口
# print "\nI251_N17 " + ">" * 150
# Icase("I251_N17_C1","RtnOK","10001588",'"118","2016082300022"')


##我的订单_订单列表接口
# print "\nI251_N18 " + ">" * 150
# Icase("I251_N18_C1","RtnOK","10001588",'"0","0","20"')



##我的订单_确认收货接口
# print "\nI251_N19 " + ">" * 150
# Icase("I251_N19_C1","RtnOK","10001588",'"4"')


##我的订单_申请退款接口
# print "\nI251_N20 " + ">" * 150
# Icase("I251_N20_C1","RtnOK","10001588",'"2016082300022"')

##我的订单_订单列表接口
# print "\nI251_N21 " + ">" * 150
# Icase("I251_N21_C1","RtnOK","10001588",'"2016082300022"')

##我的订单_订单列表接口
# print "\nI251_N22 " + ">" * 150
# Icase("I251_N22_C1","RtnOK","10001588",'"2016082300022"')



