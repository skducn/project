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

import os,sys,requests,xlwt,MySQLdb,datetime,redis,smtplib
reload(sys)
sys.setdefaultencoding('utf8')
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlutils.copy import copy
from InterfaceExcel import *

connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curWeb = connWeb.cursor()
connApp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, use_unicode=True)
curApp = connApp.cursor()
connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True)
curGame = connGame.cursor()


# [Testcase]
# print "\nI251_N7 " + ">" * 150
# # 7,三藏爆款_发布爆款接口
# # 前提条件:用户必须先通过资质认证
# curWeb.execute('select username from t_user where id=10001473')
# tbl7_1 = curWeb.fetchone()
# connWeb.commit()
# tbl7_2 = Icommon3("5",str(tbl7_1[0]))
# Icase("I251_N3_C1","RtnOK","10001473",'"10001473","4","xlq1473","1234567890123456","http://sit2.88uka.com/000/000/004/350.jpg,http://sit2.88uka.com/000/000/004/482.jpg,http://sit2.88uka.com/000/000/004/771.jpg",%s,%s' %( tbl7_1[0],tbl7_2)) # 3,资质认证_保存个人认证接口
# Icase("I251_N7_C1","RtnOK","10001473",'"4","冼丽琼1473爆款1","http://sit2.88uka.com/000/000/005/939.jpg","www.baidu.com","100","0","0","1","1","10"')

# print "\nI251_N8 " + ">" * 150
# # 8,三藏爆款_爆款修改接口
# # 前提条件:用户存在未删除的爆款商品
# 检查用户是否存在未删除的爆款商品,如存在,则获取商品ID供修改使用;如不存在,则发布一个爆款商品
# curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status in (0,1)')
# tbl8_1 = curWeb.fetchone()
# connWeb.commit()
# if (tbl8_1[0] > 0):
#     curWeb.execute('select id from t_explosion_product where userId=10001482 order by id desc limit 1')
#     tbl8_2 = curWeb.fetchone()
#     connWeb.commit()
# else:
#     Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款要修改","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
#     curWeb.execute('select id from t_explosion_product where userId=10001482 order by id desc limit 1')
#     tbl8_2 = curWeb.fetchone()
#     connWeb.commit()
# Icase("I251_N8_C1","RtnOK","10001482",'%s,"13","冼丽琼1482爆款修改了","http://sit2.88uka.com/000/000/005/939.jpg","www.baidu.com","100","0","0","1","1","10","0"' % str(tbl8_2[0]))

# print "\nI251_N9 " + ">" * 150
# # 9,三藏爆款_我的爆款列表接口
# Icase("I251_N9_C1","RtnOK","10001473",'"13","0","20"')

# print "\nI251_N10 " + ">" * 150
# # 10,三藏爆款_我的爆款历史列表接口
# # 前提条件:用户存在下架的爆款商品
# # 检查用户上架的爆款是否已有3款,若已满3款,则获取其中一款商品进行下架;否则发布一款爆款并进行下架
# curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
# tbl10_1 = curWeb.fetchone()
# connWeb.commit()
# if (tbl10_1[0] == 3):
#     curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
#     tbl10_2 = curWeb.fetchone()
#     connWeb.commit()
#     Icase("I251_N12_C1","RtnOK","10001482",'"13",%s,"1"' % tbl10_2[0]) # 12,三藏爆款_上/下架爆款接口
# else:
#     Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款要下架2","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
#     curWeb.execute('select id from t_explosion_product where userId=10001482 order by id desc limit 1')
#     tbl10_2 = curWeb.fetchone()
#     connWeb.commit()
#     Icase("I251_N12_C1","RtnOK","10001482",'"13",%s,"1"' % tbl10_2[0]) # 12,三藏爆款_上/下架爆款接口
# Icase("I251_N10_C1","RtnOK","10001482",'"13","0","20"')

# print "\nI251_N11 " + ">" * 150
# # 11,三藏爆款_爆款详情接口
# # 前提条件:用户存在爆款商品
# Icase("I251_N11_C1","RtnOK","10001482",'"13","1"')
#
# print "\nI251_N12 " + ">" * 150
# # 12,三藏爆款_上/下架爆款接口
# # 上架商品前提条件:用户已上架的爆款商品少于3款
# # 下架商品前提条件:用户存在已上架的爆款商品
# Icase("I251_N12_C1","RtnOK","10001482",'"13","2","1"')

# print "\nI251_N13 " + ">" * 150
# # 13,三藏爆款_删除爆款接口
# # 前提条件:用户存在爆款商品
# Icase("I251_N13_C1","RtnOK","10001482",'"13","3"')

# print "\nI251_N14 " + ">" * 150
# # 14,三藏爆款_爆款支付接口
# # 前提条件:商家存在上架商品,用户账户余额大于商品支付金额,用户已设置支付密码
# curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
# tbl14_1 = curWeb.fetchone()
# connWeb.commit()
# if (tbl14_1[0] > 0):
#     curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
#     tbl14_2 = curWeb.fetchone()
#     connWeb.commit()
# else:
#     Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
#     curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
#     tbl14_2 = curWeb.fetchone()
#     connWeb.commit()
# Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1"' % tbl14_2[0])

# print "\nI251_N15 " + ">" * 150
# # 15,销售订单_销售订单列表接口
# Icase("I251_N15_C1","RtnOK","10001482",'"13","0","0","20"')

# print "\nI251_N16 " + ">" * 150
# # 16,销售订单_确认发货接口
# Icase("I251_N16_C1","RtnOK","10001482",'"13","2016082400029"')

# print "\nI251_N19 " + ">" * 150
# # 19,我的订单_确认收货接口
# Icase("I251_N19_C1","RtnOK","10001473",'"2016082400029",')

# print "\nI251_N23 " + ">" * 150
# 23,我的订单_订单点评接口
# Icase("I251_N23_C1","RtnOK","10001473",'"2016082400030","冼丽琼说好就是好111111111111111","http://sit2.88uka.com/000/000/004/350.jpg"')
# sleep(10)
# Icase("I251_N23_C2","RtnOK","10001473",'"2016082400029","","http://sit2.88uka.com/000/000/004/350.jpg"')
# sleep(10)
# Icase("I251_N23_C3","RtnOK","10001473",'"2016082400030","11111111111111111冼丽琼说好就是好",""')
# Icase("I251_N23_C4","RtnParamErr","10001473",'"","冼丽琼说好就是好","http://sit2.88uka.com/000/000/004/350.jpg"')

# print "\nI251_N24 " + ">" * 150
# # 24,我的订单_找店小二列表接口
# Icase("I251_N24_C1","RtnOK","10001482",'"13",')
# Icase("I251_N24_C2","RtnParamErr","10001482",'"",')

# print "\nI251_N25 " + ">" * 150
# # 25,红包群_我的红包群_我的店铺_我的店小二列表
# Icase("I251_N25_C1","RtnOK","10001482",'"13","0","1"')
# Icase("I251_N25_C1","RtnOK","10001482",'"13","","1"')
# Icase("I251_N25_C1","RtnOK","10001482",'"13","0",""')
# Icase("I251_N25_C1","RtnParamErr","10001482",'"","0","1"')

# print "\nI251_N26 " + ">" * 150
# 26,红包群_我的红包群_我的店铺_我的店小二_添加店小二
# Icase("I251_N26_C1","RtnOK","10001482",'"13","10001472"')
# Icase("I251_N26_C2","RtnOK","10001482",'"13","10001578,10001582"')
# Icase("I251_N26_C3","RtnOK","10001482",'"13",""') #成员ID不传时没有做判断,之后添加判断
# Icase("I251_N26_C4","RtnParamErr","10001482",'"","10001578,10001582"')


# print "\nI251_N27 " + ">" * 150
# # 27,红包群_我的红包群_我的店铺_我的店小二_删除店小二
# Icase("I251_N27_C1","RtnOK","10001482",'"13","10001472"')
# Icase("I251_N27_C2","RtnParamErr","10001482",'"","10001472"')
# Icase("I251_N27_C3","RtnParamErr","10001482",'"13",""')

# print "\nI251_N28 " + ">" * 150
# # 28,红包群_我的红包群_我的店铺_我的店小二_修改店小二名
# Icase("I251_N28_C1","RtnOK","10001482",'"13","10001577","1577店小二"')
# Icase("I251_N28_C2","RtnOK","10001482",'"13","10001577","","http://sit2.88uka.com/000/000/004/350.jpg"')
# Icase("I251_N28_C3","RtnParamErr","10001482",'"","10001577","","http://sit2.88uka.com/000/000/004/350.jpg"')
# Icase("I251_N28_C4","RtnParamErr","10001482",'"13","","","http://sit2.88uka.com/000/000/004/350.jpg"')
# Icase("I251_N28_C5","RtnParamErr","10001482",'"13","10001577","",""')

# print "\nI251_N29 " + ">" * 150
# # 29,红包群_我的红包群_我的店铺_我的店小二_店小二详情
# Icase("I251_N29_C1","RtnOK","10001482",'"13","10001577"')
# Icase("I251_N29_C2","RtnParamErr","10001482",'"","10001577"')
# Icase("I251_N29_C3","RtnParamErr","10001482",'"13",""')

# print "\nI251_N30 " + ">" * 150
# # 30,红包群_我的红包群_我的店铺_我的店小二_开启/关闭店小二
# Icase("I251_N30_C1","RtnOK","10001482",'"13","10001492","0"')
# Icase("I251_N30_C2","RtnParamErr","10001482",'"","10001492","0"')
# Icase("I251_N30_C3","RtnParamErr","10001482",'"13","","0"')
# Icase("I251_N30_C4","RtnParamErr","10001482",'"13","10001492",""')

# print "\nI251_N37 " + ">" * 150
# # 37,红包群首页_我是店小二的红包群列表接口
# Icase("I251_N37_C1","RtnOK","10001482",'')

# print "\nI251_N38 " + ">" * 150
# # 38,红包群首页_红包群列表接口
# Icase("I251_N38_C1","RtnOK","10001482",'"10001482","0","20"')
# Icase("I251_N38_C2","RtnParamErr","10001482",'"","0","20"')
# Icase("I251_N38_C3","RtnOK","10001482",'"10001482","","20"')
# Icase("I251_N38_C4","RtnSysErr","10001482",'"10001482","0",""')

# print "\nI251_N39 " + ">" * 150
# # 39,红包群_更多红包群列表接口
# Icase("I251_N39_C1","RtnOK","10001482",'"10001482","0","20","年糕","0","3101000000"')
# Icase("I251_N39_C2","RtnOK","10001482",'"","0","20","年糕","0","3101000000"') #userId空
# Icase("I251_N39_C3","RtnOK","10001482",'"10001482","","20","年糕","","3101000000"') #startIndex空
# Icase("I251_N39_C4","RtnSysErr","10001482",'"10001482","0","","年糕","","3101000000"') #pageSize空
# Icase("I251_N39_C5","RtnOK","10001482",'"10001482","0","20","","","3101000000"') #likeName空
# Icase("I251_N39_C6","RtnOK","10001482",'"10001482","0","20","年糕","","3101000000"') #industryId空
# Icase("I251_N39_C7","RtnParamErr","10001482",'"10001482","0","20","年糕","0",""') #cityId空
