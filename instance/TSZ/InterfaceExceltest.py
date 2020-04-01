# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 接口自动化测试用例
#****************************************************************
# 使用说明:
# 接口调用使用方法: Icase("参数1","参数2","参数3",'"**参数4"')
# 例子:Icase("I251_N28_C1","RtnOK","10001482",'"13","10001577","1577店小二"')
# 参数1 = 接口坐标定位,由三部分组成 "excel工作表_序号_用例编号" , 如"I251_N6_C1" 对应excel中工作表I251序号为6的测试用例1 .
# 参数2 = 测试返回类型
# 参数3 = userID
# **参数4 = 开发接口文档的请求参数列表 (注意:各参数用逗号分隔,且最外层有单引号 ' ,如 '"userid","groupId","memberId"')
# 如果接口的正确返回值是 {"data":null,"errorstr":"","errorcode":0,"success":true} ,请使用 "RtnNullOK" 作为测试返回类型,否则用 RtnOK.
# 如果接口的正确返回值是 {"data":[],"errorstr":"","errorcode":0,"success":true} ,请使用 "RtnNoDATAOK" 作为测试返回类型,否则用 RtnOK.

import os,sys,requests,xlwt,xlrd,MySQLdb,redis,smtplib
reload(sys)
sys.setdefaultencoding('utf8')
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
from xlutils.copy import copy
from InterfaceExcel import *

connWeb= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curWeb = connWeb.cursor()
curWeb.execute('SET NAMES utf8;')
connApp= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardapp', port=3306, use_unicode=True)
curApp = connApp.cursor()
curApp.execute('SET NAMES utf8;')
connGame= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='game', port=3306, use_unicode=True)
curGame = connGame.cursor()
curGame.execute('SET NAMES utf8;')

# [Testcase]
# 1,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1,资质认证_资质认证首页()
print "\nI251_N1 " + ">" * 150
Icase("I251_N1_C1","RtnOK","10001679",'"213",')
Icase("I251_N1_C2","RtnParamErr","",'"118",')
Icase("I251_N1_C3","RtnParamErr","10001588",'"",')

# 2,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 2,城市列表接口
print "\nI251_N2 " + ">" * 150
Icase("I251_N2_C1","RtnOK","10001588",'"1100000000",')
Icase("I251_N2_C2","RtnOK","",'"1100000000"')
Icase("I251_N2_C3","RtnOK","",'""')

# 3,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 3,资质认证_保存个人认证接口 (调用 Icommon3)
print "\nI251_N3 " + ">" * 150
# 关联表：t_person_certification插入一条未审核记录
Icase("I251_N3_C1","RtnOK","10001588",'"10001588","118","pp","431222199206290017","5,6,7","17000000020", %s,"",""' % Icommon3("5","17000000020"))
Icase("I251_N3_C2","RtnParamErr","10001588",'"","118","pp","431222199206290017","5,6,7","17000000020", %s,"",""' % Icommon3("5","17000000020"))
Icase("I251_N3_C3","RtnParamErr","10001588",'"10001588","118","","431222199206290017","5,6,7","17000000020", %s,"",""' % Icommon3("5","17000000020"))
Icase("I251_N3_C4","RtnParamErr","10001588",'"10001588","118","DFDF","","5,6,7","17000000020", %s,"",""' % Icommon3("5","17000000020"))
Icase("I251_N3_C5","RtnParamErr","10001588",'"10001588","118","DFDF","431222199206290017","","17000000020", %s,"",""' % Icommon3("5","17000000020"))
Icase("I251_N3_C6","RtnParamErr","10001588",'"10001588","118","DFDF","431222199206290017","5","", %s,"",""' % Icommon3("5","17000000020"))
Icase("I251_N3_C7","RtnParamErr","10001588",'"10001588","118","DFDF","431222199206290017","5","17000000020", "","",""')
Icase("I251_N3_C8","RtnSysErr","10001588",'"10001588","118","pp","431222199206290017","5,6,7","17000000020", %s,"100","100"' % Icommon3("5","17000000020"))
# 修改个人认证
curWeb.execute('select id from ukardweb.t_person_certification where userId=10001588')
tbl3= curWeb.fetchone()
connWeb.commit()
Icase("I251_N3_C9","RtnOK","10001588",'"10001588","118","pp1","431222199206290017X","5,6,8","17000000020",%s,"",""' % (Icommon3("5","17000000020")))
Icase("I251_N3_C10","RtnParamErr","10001588",'"10001588","118","pp1","431222199206290017X","5,6,8","17000000021",%s,"",""' % (Icommon3("5","17000000020")))
Icase("I251_N3_C11","RtnParamErr","10001588",'"","118","pp1","431222199206290017X","5,6,8","17000000020",%s,"",""' % (Icommon3("5","17000000020")))

# 4,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 4,资质认证_个人认证信息查询接口 (依赖 I251_N3_C1)
print "\nI251_N4 " + ">" * 150
Icase("I251_N4_C1","RtnOK","10001588",'"10001588","118"')
Icase("I251_N4_C2","RtnParamErr","10001588",'"","118"')
Icase("I251_N4_C3","RtnParamErr","10001588",'"10001588",""')
# 销毁测试数据
curWeb.execute('delete from t_person_certification where userId=10001588')
connWeb.commit()

# 5,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 5,资质认证_保存、修改店铺认证接口(依赖于Icommon3) ???
# 关联表：实体店表t_entity_store_certification   网店表：t_web_store_certification
# 需要验证一下一个群只允许存在一个网店或者实体店
#（调用个人认证接口）
print "\nI251_N5 " + ">" * 150
Icase("I251_N3_C1","RtnOK","10001588",'"10001588","118","pp","431222199206290017","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
curWeb.execute('select id from ukardweb.t_person_certification where userId=10001588')
tbl5= curWeb.fetchone()
connWeb.commit()
curWeb.execute('delete from ukardweb.t_entity_store_certification where groupId=118')
connWeb.commit()
Icase("I251_N5_C1","RtnNullOK","10001588",'"10001588","118",%s,"动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"",""' % (tbl5[0],Icommon3("5","17000000020")))
curWeb.execute('select count(id) from ukardweb.t_entity_store_certification where groupId=118')
tbl6= curWeb.fetchone()
connWeb.commit()
assertEqual(tbl6[0],1,"","[errorrrrrrrrrr , t_entity_store_certification,保存商户认证失败!]")
# 验证没有个人认证没有用户ID是无法创建商户认证的  还需要张金修改后在测试
curWeb.execute('delete from ukardweb.t_person_certification where userId=10001588')
connWeb.commit()
Icase("I251_N5_C2","RtnSysErr","10001588",'"10001588","118","14","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % (Icommon3("5","17000000020")))
# 还原个人认证
Icase("I251_N3_C1","RtnOK","10001588",'"10001588","118","pp","431222199206290017","5,6,7","17000000020", %s' % Icommon3("5","17000000020"))
Icase("I251_N5_C3","RtnParamErr","10001588",'"","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
Icase("I251_N5_C4","RtnParamErr","10001588",'"10001588","","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
Icase("I251_N5_C5","RtnParamErr","10001588",'"10001588","118","","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
Icase("I251_N5_C6","RtnSysErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","","0","www.abidu.com","0","1","17000000020", %s,"0"' % Icommon3("5","17000000020"))
Icase("I251_N5_C7","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","3","17000000020", %s,"0"' % Icommon3("5","17000000020"))
Icase("I251_N5_C8","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","", %s,"0"' % Icommon3("5","17000000020"))
Icase("I251_N5_C9","RtnParamErr","10001588",'"10001588","118","4","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com","0","1","17000000020","","0"')
# 修改商户资质认证
curWeb.execute('select id from ukardweb.t_person_certification where userId=10001588')
tbl7= curWeb.fetchone()
connWeb.commit()
curWeb.execute('select id from ukardweb.t_entity_store_certification where groupId=118 ')
tbl8= curWeb.fetchone()
connWeb.commit()
Icase("I251_N5_C10","RtnNullOK","10001588",'"10001588","118",%s,"动量","好方d法店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000000020","09:00","其他","5","0","www.abidu.com", %s,"1","17000000020", %s,"0"' % (tbl7[0],tbl8[0],Icommon3("5","17000000020")))

# 6,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 6,资质认证_商户认证信息查询接口 (依赖于I251_N5_C1)
print "\nI251_N6 " + ">" * 150
Icase("I251_N6_C1","RtnNullOK","10001588",'"10001588","118","1"')
Icase("I251_N6_C1","RtnParamErr","10001588",'"","118","1"')
Icase("I251_N6_C1","RtnParamErr","10001588",'"10001588","","1"')
Icase("I251_N6_C1","RtnParamErr","10001588",'"10001588","",""')

# 7,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 7,三藏爆款_发布爆款接口
# 关联表：t_explosion_product
# 备注：如果爆款超过三件就会提示，
print "\nI251_N7 " + ">" * 150
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118')
connWeb.commit()
Icase("I251_N7_C1","RtnNullOK","10001588",'"118","adidas商品1","商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"')
Icase("I251_N7_C2","RtnNullOK","10001588",'"118","adidas商品2","商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"')
Icase("I251_N7_C3","RtnNullOK","10001588",'"118","adidas商品3","商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"')
Icase("I251_N7_C4","RtnParamErr","10001588",'"118","adidas商品4","商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"')
curWeb.execute('select count(id) from t_explosion_product where userid=10001588 and groupId=118 and status=0')
tbl7 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl7[0],3,"","[errorrrrrrrrrr , t_explosion_product,爆款不是3件!]")
Icase("I251_N7_C2","RtnParamErr","10001588",'"","adidas商品","商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"')
Icase("I251_N7_C3","RtnParamErr","10001588",'"118","","","www.baidjfu.com","","0","0","","0","0","10001588"')
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118')
connWeb.commit()

# 8,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 8,三藏爆款_爆款修改接口(调用 I251_N7_C1)
# 业务逻辑:
# 前置条件: 上线及删除的爆款无法修改
# 关联表：t_explosion_product
print "\nI251_N8 " + ">" * 150
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
# 上架的爆款应无法修改,最后一个参数status=0
Icase("I251_N7_C1","RtnNullOK","10001588",'"118","adidas商品1","商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"')
curWeb.execute('select id from t_explosion_product where userId=10001588 and groupId=118 order by id desc')
tbl8= curWeb.fetchone()
connWeb.commit()
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N8_C1","RtnParamErr","10001588",'%s,"118",%s,"商品图片100","www.baidu.com100","100","1","70","1","1","20","0","10001588"' % (tbl8[0],varTimeStamp))
curWeb.execute('select count(id) from t_explosion_product where productContent="%s" and productPic="商品图片100" '
               'and videoUrl="www.baidu.com100" and productAmount=10000 and isFree=1 and postageAmount=7000 and isPraiseRed=1 '
               'and praiseRedType=1 and praiseRedAmount="2000.0"' % varTimeStamp)
tbl8 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl8[0],1,"[errorrrrrrrrrr , t_explosion_product,不能修改上架的爆款]","")
# 删除的爆款应无法修改,最后一个参数status=2
Icase("I251_N7_C1","RtnNullOK","10001588",'"118","adidas商品1","商品图片","www.baidjfu.com","1","0","0","0","0","2","10001588"')
curWeb.execute('select id from t_explosion_product where userId=10001588 and groupId=118 order by id desc')
tbl8= curWeb.fetchone()
connWeb.commit()
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N8_C1","RtnParamErr","10001588",'%s,"118",%s,"商品图片100","www.baidu.com100","100","1","70","1","1","20","0","10001588"' % (tbl8[0],varTimeStamp))
curWeb.execute('select count(id) from t_explosion_product where productContent="%s" and productPic="商品图片100" '
               'and videoUrl="www.baidu.com100" and productAmount=10000 and isFree=1 and postageAmount=7000 and isPraiseRed=1 '
               'and praiseRedType=1 and praiseRedAmount="2000.0"' % varTimeStamp)
tbl8 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl8[0],1,"[errorrrrrrrrrr , t_explosion_product,不能修改删除的爆款]","")
# 下架的爆款可以修改,最后一个参数status=1
Icase("I251_N7_C1","RtnNullOK","10001588",'"118","adidas商品1","商品图片","www.baidjfu.com","1","0","0","0","0","1","10001588"')
curWeb.execute('select id from t_explosion_product where userId=10001588 order by id desc limit 1')
tbl10_2 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N12_C1","RtnNullOK","10001588",'"118",%s,"1"' % tbl10_2[0]) # 12,三藏爆款_上/下架爆款接口
curWeb.execute('select id from t_explosion_product where userId=10001588 and groupId=118 order by id desc  limit 0,1')
tbl8= curWeb.fetchone()
connWeb.commit()
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N8_C2","RtnNullOK","10001588",'%s,"118",%s,"商品图片","www.baidu.com100","1","1","1","1","1","0.01","1","10001588"' % (tbl8[0],varTimeStamp))
curWeb.execute('select count(id) from t_explosion_product where productContent="%s" and status=1' % varTimeStamp)
tbl8 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl8[0],1,"","[errorrrrrrrrrr , t_explosion_product,下架的爆款修改失败!]")
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118')
connWeb.commit()

# 9,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 9,三藏爆款_我的爆款列表接口
print "\nI251_N9 " + ">" * 150
Icase("I251_N9_C1","RtnOK","10001473",'"13","0","20"')

# 10,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 10,三藏爆款_我的爆款历史列表接口(调用 I251_N7_C1,I251_N7_C12)
# 前提条件:爆款历史列表中只记录下架的商品,上架一个商品
print "\nI251_N10 " + ">" * 150
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s"' % varTimeStamp)
tbl10 = curWeb.fetchone()
connWeb.commit()
# 下架一个商品
Icase("I251_N12_C1","RtnNullOK","10001588",'"118",%s,"1"' % tbl10[0]) # 12,三藏爆款_下架爆款接口
# 检查爆款历史列表记录
Icase("I251_N10_C1","RtnOK","10001588",'"118","0","20"')
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118')
connWeb.commit()

# 11,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 11,三藏爆款_爆款详情接口(调用 I251_N7_C1)
# 前提条件:用户存在爆款商品
print "\nI251_N11 " + ">" * 150
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s"' % varTimeStamp)
tbl11 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N11_C1","RtnOK","10001588",'"118",%s' % tbl11[0])
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118')
connWeb.commit()

# 12,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 12,三藏爆款_上/下架爆款接口(调用 I251_N7_C1)
# 业务逻辑:先发布一个上架商品,然后下架,再上架检查
print "\nI251_N12 " + ">" * 150
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl12 = curWeb.fetchone()
connWeb.commit()
# 下架处理
Icase("I251_N12_C1","RtnNullOK","10001588",'"118",%s,"1"' % tbl12[0])
curWeb.execute('select id,count(id) from t_explosion_product where productContent="%s" and status=1' % varTimeStamp)
tbl12 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl12[1],1,"","[errorrrrrrrrrr , t_explosion_product,下架的爆款修改失败!]")
# 上架处理
Icase("I251_N12_C1","RtnNullOK","10001588",'"118",%s,"0"' % tbl12[0])
curWeb.execute('select count(id) from t_explosion_product where productContent="%s" and status=0' % varTimeStamp)
tbl12 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl12[0],1,"","[errorrrrrrrrrr , t_explosion_product,下架的爆款修改失败!]")

# 13,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 13,三藏爆款_删除爆款接口(调用 I251_N7_C1)(金浩自写)
print "\nI251_N13 " + ">" * 150
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0","10001588"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl13 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N13_C1","RtnNullOK","10001588",'"10001588","118",%s,' % str(tbl13[0]))
curWeb.execute('select count(id) from t_explosion_product where productContent="%s" and status=2' % varTimeStamp)
tbl13 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl13[0],1,"","[errorrrrrrrrrr , t_explosion_product,删除爆款失败!]")

# 14,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 14,三藏爆款_爆款支付接口(调用 I251_N7_C1)(金浩写)
print "\nI251_N14 " + ">" * 150
# 前提条件:商家存在上架商品,用户账户余额大于商品支付金额,用户已设置支付密码
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
# curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
curWeb.execute('select id from t_explosion_product where userId=10002135 and status = 0 order by id desc limit 1')
tbl14 = curWeb.fetchone()
connWeb.commit()

Icase("I251_N14_C1","RtnOK","10001588",'"10001588",%s,"118","3","111111","1"' % tbl14[0])
Icase("I251_N14_C2","RtnParamErr","10001588",'"",%s,"118","3","111111","1"'% (tbl14[0]))
Icase("I251_N14_C3","RtnParamErr","10001588",'"10001588",%s,"","3","111111","1"'% (tbl14[0]))
Icase("I251_N14_C4","RtnParamErr","10001588",'"10001588",%s,"","3","","1"'% (tbl14[0]))

# 15,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 15,销售订单_销售订单列表接口
print "\nI251_N15 " + ">" * 150
Icase("I251_N15_C1","RtnOK","10001482",'"13","0","0","20"')

# 16,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 16,销售订单_确认发货接口(调用 I251_N7_C1,I251_N14_C1)
# 关联表: t_order
print "\nI251_N16 " + ">" * 150
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl14 = curWeb.fetchone()
connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001588",'"10001588",%s,"118","3","111111","1"' % tbl14[0])
curWeb.execute('select id from t_order where groupId=118 and orderState=1 order by id desc limit 1')
tbl16= curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001588",'"118",%s' % (tbl16[0]))
Icase("I251_N16_C2","RtnParamErr","10001588",'"",%s' % (tbl16[0]))
Icase("I251_N16_C3","RtnParamErr","10001588",'"118",""')

# 17,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 17,销售订单_确认退款接口(调用 I251_N7_C1,I251_N14_C1)
print "\nI251_N17 " + ">" * 150
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl14 = curWeb.fetchone()
connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001588",'"10001588",%s,"118","3","111111","1"' % tbl14[0])
curWeb.execute('select id from ukardweb.t_order where groupId=118 and orderState=1 order by id desc limit 1')
tbl18= curWeb.fetchone()
connWeb.commit()
Icase("I251_N17_C1","RtnNullOK","10001588",'"118",%s' %(tbl18[0]))
Icase("I251_N17_C2","RtnParamErr","10001588",'"",%s' %(tbl18[0]))
Icase("I251_N17_C3","RtnParamErr","10001588",'"118",""')

# 18,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 18,我的订单_订单列表接口
print "\nI251_N18 " + ">" * 150
Icase("I251_N18_C1","RtnOK","10001588",'"0","0","20"')
Icase("I251_N18_C2","RtnOK","10001588",'"","0","20"')
Icase("I251_N18_C3","RtnSysErr","10001588",'"","",""')
Icase("I251_N18_C4","RtnOK","",'"0","0","20"')

# 19,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 19,我的订单_确认收货接口(调用 I251_N7_C1,I251_N14_C1,I251_N16_C1)
print "\nI251_N19 " + ">" * 150
# 支付一个爆款
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl14 = curWeb.fetchone()
connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001588",'"10001588",%s,"118","3","111111","1"' % tbl14[0])
print "waiting 10s"
sleep(10)
# 确认发货
curWeb.execute('select id from t_order where groupId=118 and orderState=1 order by id desc limit 1')
tbl19= curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001588",'"118",%s' % (tbl19[0]))
# 确认收货
curWeb.execute('select id from t_order where groupId=118 and orderState=2 limit 1')
tbl19= curWeb.fetchone()
Icase("I251_N19_C1","RtnNullOK","10001588",'%s,' % (tbl19[0]))
Icase("I251_N19_C2","RtnParamErr","10001588",'""')

# 20,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 20,我的订单_申请退款接口 (调用 I251_N7_C1,I251_N14_C1)
print "\nI251_N20 " + ">" * 150
# 先支付一笔
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl14 = curWeb.fetchone()
connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001588",'"10001588",%s,"118","3","111111","1"' % tbl14[0])
sleep(10)
# 申请退款
curWeb.execute('select id from t_order where groupId=118 and orderState=1 ORDER BY id DESC limit 1')
tbl20= curWeb.fetchone()
connWeb.commit()
Icase("I251_N20_C1","RtnNullOK","10001588",'%s,' % (tbl20[0]))
Icase("I251_N20_C2","RtnParamErr","10001588",'""')

# 21,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 21,我的订单_取消退款接口
print "\nI251_N21 " + ">" * 150
curWeb.execute('select id from t_order where groupId=118 and orderState=4 ORDER BY id DESC limit 1')
tbl21= curWeb.fetchone()
Icase("I251_N21_C1","RtnNullOK","10001588",'%s,' % (tbl21[0]))
Icase("I251_N21_C2","RtnParamErr","10001588",'""')

# 22,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 22,我的订单_删除订单接口(依赖于 I251_N19_C1)
print "\nI251_N22 " + ">" * 150
Icase("I251_N22_C1","RtnNullOK","10001588",'"2016082400102",')
curWeb.execute('select count(id) from t_order where id=%s and isUserDel=1' % tbl19[0])
tbl22= curWeb.fetchone()
connWeb.commit()
assertEqual(tbl22[0],0,"","[errorrrrrrrrrr , t_order,删除订单失败!]")
Icase("I251_N22_C3","RtnParamErr","10001588",'"",')

# 23,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 23,我的订单_订单点评接口 (调用 I251_N19_C1,I251_N14_C1,I251_N7_C1,I251_N16_C1)
print "\nI251_N23 " + ">" * 150
# 前提条件:用户存在已确认收货,但是未进行点评的订单
# 检查用户是否有未已确认收货,但是未进行点评的订单,若有,则点评订单,若没有,则购买商品,确认收货后进行点评订单
curWeb.execute('update t_explosion_product set status=2 where userId=10001588 and groupId=118 ')
connWeb.commit()
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N7_C1","RtnNullOK","10001588",'"118",%s,"商品图片","www.baidjfu.com","1","0","0","0","0","0"' % (varTimeStamp))
curWeb.execute('select id from t_explosion_product where productContent="%s" ' % varTimeStamp)
tbl14 = curWeb.fetchone()
connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001588",'"10001588",%s,"118","3","111111","1"' % tbl14[0])
sleep(10)
# 确认发货
curWeb.execute('select id from t_order where groupId=118 and orderState=1 order by id desc limit 1')
tbl19= curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001588",'"118",%s' % (tbl19[0]))
# 确认收货
curWeb.execute('select id from t_order where groupId=118 and orderState=2 limit 1')
tbl19= curWeb.fetchone()
Icase("I251_N19_C1","RtnNullOK","10001588",'%s,' % (tbl19[0]))
Icase("I251_N23_C1","RtnNullOK","10001588",'%s,"点评点评","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl19[0]))
Icase("I251_N23_C4","RtnParamErr","10001588",'"","冼丽琼说好就是好","http://sit2.88uka.com/000/000/004/350.jpg"')

# 24,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 24,我的订单_点评详情接口(依赖 I251_N23_C1)
print "\nI251_N24 " + ">" * 150
Icase("I251_N24_C1","RtnOK","10001588",'%s,' % (tbl19[0]))
Icase("I251_N24_C2","RtnSysErr","10001588",'"1212121212121212",')
Icase("I251_N24_C3","RtnParamErr","10001588",'')

# 25,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 25,我的订单_找店小二列表接口 (调用 I251_N27_C1,I24_N50_C1)
print "\nI251_N25 " + ">" * 150
# 前提条件:店铺存在店小二
curWeb.execute('select groupId,count(id) from t_redgroup_memberinfo where memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1 order by userId desc limit 1')
tbl25_1 = curWeb.fetchone()
connWeb.commit()
if (tbl25_1[1] > 0):
    Icase("I251_N25_C1","RtnOK","10001473",'%s,' % (tbl25_1[0]))
else:
    curWeb.execute('select userId,count(id) from t_redgroup_memberinfo where memberState = 0 and groupId = 13 and isBlack = 0 and isWaiter = 0')
    tbl27_1 = curWeb.fetchone()
    connWeb.commit()
    if (tbl27_1[1] > 0): Icase("I251_N27_C1","RtnNullOK","10001482",'"13",%s' % (tbl27_1[0]))
    else:
        curWeb.execute('select userId from t_redgroup_memberinfo where groupId <> 13 order by userId desc limit 1')
        tbl27_2 = curWeb.fetchone()
        connWeb.commit()
        Icase("I24_N50_C1", "RtnOK", str(tbl27_2[0]), '%s,"13","10001482"' % (tbl27_2[0])) # 红包群_加入红包群接口（新增返回值）
        Icase("I251_N27_C2","RtnNullOK","10001482",'"13",%s' % (tbl27_2[0]))

    Icase("I251_N25_C1","RtnOK","10001473",'"13",')
Icase("I251_N25_C2","RtnParamErr","10001473",'"",')

# 26,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 26,红包群_我的红包群_我的店铺_我的店小二列表
print "\nI251_N26 " + ">" * 150
Icase("I251_N26_C1","RtnOK","10001493",'"24","0","1"')
Icase("I251_N26_C1","RtnOK","10001493",'"24","","1"')
Icase("I251_N26_C1","RtnOK","10001493",'"24","0",""')
Icase("I251_N26_C1","RtnParamErr","10001493",'"","0","1"')

# 27,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 27,红包群_我的红包群_我的店铺_我的店小二_添加店小二(调用 I24_N50_C1,I251_N27_C1)
print "\nI251_N27 " + ">" * 150
# 前提条件:店铺存在未被设为店小二的群成员
curWeb.execute('select userId,count(id) from t_redgroup_memberinfo where memberState = 0 and groupId = 13 and isBlack = 0 and isWaiter = 0')
tbl27_1 = curWeb.fetchone()
connWeb.commit()
if (tbl27_1[1] > 0):
    Icase("I251_N27_C1","RtnNullOK","10001482",'"13",%s' % (tbl27_1[0]))
    tbl27userId = tbl27_1[0]
else:
    curWeb.execute('select userId from t_redgroup_memberinfo where groupId <> 13 order by userId desc limit 1')
    tbl27_2 = curWeb.fetchone()
    connWeb.commit()
    Icase("I24_N50_C1", "RtnOK", str(tbl27_2[0]), '%s,"13","10001482"' % (tbl27_2[0])) # 红包群_加入红包群接口（新增返回值）
    Icase("I251_N27_C2","RtnNullOK","10001482",'"13",%s' % (tbl27_2[0]))
    tbl27userId = tbl27_2[0]
Icase("I251_N27_C3","RtnParamErr","10001482",'"13",""')
Icase("I251_N27_C4","RtnParamErr","10001482",'"","10001578,10001582"')

# 28,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 28,红包群_我的红包群_我的店铺_我的店小二_删除店小二(依赖 I251_N27_C1)
print "\nI251_N28 " + ">" * 150
# 前提条件:店铺存在店小二
Icase("I251_N28_C1","RtnNullOK","10001482",'"13",%s' % (tbl27userId))
Icase("I251_N28_C2","RtnParamErr","10001482",'"","10001472"')
Icase("I251_N28_C3","RtnParamErr","10001482",'"13",""')

# 29,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 29,红包群_我的红包群_我的店铺_我的店小二_修改店小二名
print "\nI251_N29 " + ">" * 150
# 前提条件:店铺存在店小二
curWeb.execute('select userId,count(id) from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1')
tbl29_1 = curWeb.fetchone()
connWeb.commit()
curWeb.execute('select userId from t_redgroup_memberinfo where groupId <> 13 order by userId desc limit 1')
tbl29_2 = curWeb.fetchone()
connWeb.commit()
Icase("I24_N50_C1", "RtnOK", str(tbl29_2[0]), '%s,"13","10001482"' % (tbl29_2[0])) # 红包群_加入红包群接口（新增返回值）
Icase("I251_N27_C2","RtnNullOK","10001482",'"13",%s' % (tbl29_2[0]))
import datetime
varTimeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I251_N29_C1", "RtnNullOK", "10001482", '"13",%s,%s,"http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl29_2[0],varTimeStamp))
curWeb.execute('select count(id) from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and remarks="%s" ' % varTimeStamp)
tbl29_3 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl29_3[0],1,"","[errorrrrrrrrrr , t_redgroup_memberinfo,修改店小二名错误!]")
tbl29userId = tbl29_2[0]
Icase("I251_N29_C3","RtnParamErr","10001482",'"","10001577","","http://sit2.88uka.com/000/000/004/350.jpg"')
Icase("I251_N29_C4","RtnParamErr","10001482",'"13","","","http://sit2.88uka.com/000/000/004/350.jpg"')
Icase("I251_N29_C5","RtnParamErr","10001482",'"13","10001577","",""')

# 30,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 30,红包群_我的红包群_我的店铺_我的店小二_店小二详情(依赖 I251_N29_C1)
print "\nI251_N30 " + ">" * 150
# 前提条件:店铺存在店小二
Icase("I251_N30_C1", "RtnOK", "10001482", '"13",%s' % (tbl29userId))
Icase("I251_N30_C2","RtnParamErr","10001482",'"","10001577"')
Icase("I251_N30_C3","RtnParamErr","10001482",'"13",""')

# 31,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 31,红包群_我的红包群_我的店铺_我的店小二_开启/关闭店小二
print "\nI251_N31 " + ">" * 150
# 前提条件:店铺存在店小二
# 关联表字段:t_redgroup_memberinfo ,isWaiter
# 关闭店小二后,检查表字段值
Icase("I251_N31_C1", "RtnOK", "10001482", '"13",%s,"0"' % tbl29userId)
curWeb.execute('select count(id) from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 0 and remarks="%s" ' % varTimeStamp)
tbl31 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl31[0],1,"","[errorrrrrrrrrr , t_redgroup_memberinfo,关闭店小二错误!]")
# 打开店小二后,检查表字段值
Icase("I251_N31_C1", "RtnOK", "10001482", '"13",%s,"1"' % tbl29userId)
curWeb.execute('select count(id) from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and remarks="%s" ' % varTimeStamp)
tbl31 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl31[0],1,"","[errorrrrrrrrrr , t_redgroup_memberinfo,打开店小二错误!]")
Icase("I251_N31_C2","RtnParamErr","10001482",'"","10001492","0"')
Icase("I251_N31_C3","RtnParamErr","10001482",'"13","","0"')
Icase("I251_N31_C4","RtnParamErr","10001482",'"13","10001492",""')

# 32,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 32,红包群_我的红包群_我的店铺_我的店小二_查看店小二聊天记录_聊天用户列表
print "\nI251_N32 " + ">" * 150
curWeb.execute(
    'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1 order by userId limit 1')
tbl32_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N32_C1","RtnOK","10001482",'"13",%s' % tbl32_1[0])

# 33,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 33,红包群_我的红包群_我的店铺_我的店小二_查看店小二聊天记录_用户聊天记录
print "\nI251_N33 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0  and isWaiter = 0 order by userId desc limit 1')
tbl72_1 = curWeb.fetchone()
connWeb.commit()
curWeb.execute(
  'select count(userId) from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1')
tbl72_2 = curWeb.fetchone()
connWeb.commit()
if (tbl72_2[0] > 0):
    curWeb.execute(
        'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1 order by userId limit 1')
    tbl72_3 = curWeb.fetchone()
    connWeb.commit()
    Icase("I251_N72_C1","RtnNullOK",str(tbl72_3[0]),'"13",%s,"我是店小二","1","0"' % (tbl72_1[0]))
    Icase("I251_N33_C1", "RtnOK", "10001482", '"13",%s,%s,"0"' % (tbl72_3[0],tbl72_1[0]))
else:
    curWeb.execute(
        'select id from t_user where id not in (select distinct(userId) from t_redgroup_memberinfo where groupId = 13) order by id desc limit 1')
    tbl33_1 = curWeb.fetchone()
    connWeb.commit()
    Icase("I24_N50_C1", "RtnOK", str(tbl33_1[0]), '%s,"13","10001482"' % (tbl33_1[0])) # 红包群_加入红包群接口（新增返回值）
    Icase("I251_N27_C1","RtnOK","10001482",'"13",%s' % (tbl33_1[0])) # 添加为店小二
    Icase("I251_N72_C1","RtnNullOK",str(tbl33_1[0]),'"13",%s,"我是新的店小二","1","0"' % (tbl72_1[0]))
    Icase("I251_N33_C1", "RtnOK", "10001482", '"13",%s,%s,"0"' % (tbl33_1[0],tbl72_1[0]))

# 34,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 34,红包群_我关注的红包群_私信_私信小二列表
print "\nI251_N34 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl34_1 = curWeb.fetchone()
connWeb.commit()
print str(tbl34_1[0])
Icase("I251_N34_C1", "RtnOK", str(tbl34_1[0]), '"13","10001482","0"')

# 35,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 35,红包群_我的红包群_三藏爆款_用户点评列表
print "\nI251_N35 " + ">" * 150
# 前提条件:店铺存在点评订单
curWeb.execute('select count(id),isPraise from t_review where groupId = 13 group by (isPraise)')
tbl35_1 = curWeb.fetchall()
connWeb.commit()
for i in tbl35_1:
    if (i[0] > 0) :
        isPraise = i[1]
        Icase("I251_N35_C1","RtnOK","10001482",'"13",%s' % isPraise)

# 36,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 36,红包群_我的红包群_三藏爆款_用户点评_审核点评
print "\nI251_N36 " + ">" * 150
# 前提条件:店铺存在未审核点评的订单
curWeb.execute('select count(id) from t_review where groupId = 13 and isPraise = 0')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
if (tbl36_1[0] > 0):
    curWeb.execute('select id from t_review where groupId = 13 and isPraise = 0 order by id desc limit 1')
    tbl36_2 = curWeb.fetchone()
    connWeb.commit()
    Icase("I251_N36_C1","RtnOK","10001482",'"13",%s,"1"' % (tbl36_2[0]))
else:
    curWeb.execute('select count(id) from t_order where userId=10001473 and orderState = 3 and isReview = 0')
    tbl23_1 = curWeb.fetchone()
    connWeb.commit()
    if (tbl23_1[0] > 0):
        curWeb.execute('select id from t_order where userId=10001473 and orderState = 3 and isReview = 0 order by id desc limit 1')
        tbl23_2 = curWeb.fetchone()
        connWeb.commit()
        Icase("I251_N23_C1","RtnNullOK","10001473",'%s,"点评点评","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl23_2[0]))#我的订单_订单点评接口
        curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
        tbl36_2 = curWeb.fetchone()
        connWeb.commit()
        Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_2[0]))
    else:
        curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
        tbl14_1 = curWeb.fetchone()
        connWeb.commit()
        if (tbl14_1[0] > 0):
            curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
            tbl14_2 = curWeb.fetchone()
            connWeb.commit()
        else:
            Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
            curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
            tbl14_2 = curWeb.fetchone()
            connWeb.commit()
        print "waiting 13s"
        sleep(13)
        Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1"' % tbl14_2[0])# 14,三藏爆款_爆款支付接口
        sleep(10)
        curWeb.execute(
            'select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
        tbl16_1 = curWeb.fetchone()
        connWeb.commit()
        Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % (tbl16_1[0])) # 16,销售订单_确认发货接口
        sleep(10)
        curWeb.execute(
            'select id from t_order where userId=10001473 and orderState = 2 order by id desc limit 1')
        tbl19_1 = curWeb.fetchone()
        connWeb.commit()
        Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % (tbl19_1[0])) # 19,我的订单_确认收货接口
        sleep(10)
        Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评点评","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl19_1[0]))#我的订单_订单点评接口
        curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
        tbl36_2 = curWeb.fetchone()
        connWeb.commit()
        Icase("I251_N36_C1", "RtnNullOK", "10001482", '"13",%s,"2"' % (tbl36_2[0]))

# 37,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 37,红包群_我的红包群_三藏爆款_用户点评_发点评炸弹预览
print "\nI251_N37 " + ">" * 150
# 前提条件:店铺存在好评的订单
curWeb.execute('select count(id) from t_review where groupId = 13 and isPraise = 1')
tbl37_1 = curWeb.fetchone()
connWeb.commit()
if (tbl37_1[0] > 0):
    curWeb.execute('select id from t_review where groupId = 13 and isPraise = 1  order by id desc limit 1')
    tbl37_2 = curWeb.fetchone()
    connWeb.commit()
    Icase("I251_N37_C1","RtnOK","10001482",'"13",%s' % (tbl37_2))

# 38,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 38,红包群首页_我是店小二的红包群列表接口
print "\nI251_N38 " + ">" * 150
Icase("I251_N38_C1","RtnOK","10001482",'')

# 39,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 39,红包群首页_红包群列表接口
print "\nI251_N39 " + ">" * 150
Icase("I251_N39_C1","RtnOK","10001482",'"10001482","0","20"')
Icase("I251_N39_C2","RtnParamErr","10001482",'"","0","20"')
Icase("I251_N39_C3","RtnOK","10001482",'"10001482","","20"')
Icase("I251_N39_C4","RtnSysErr","10001482",'"10001482","0",""')

# 40,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 40,红包群_更多红包群列表接口
print "\nI251_N40 " + ">" * 150
Icase("I251_N40_C1","RtnOK","10001482",'"10001482","0","20","年糕","0","3101000000"')
Icase("I251_N40_C2","RtnOK","10001482",'"","0","20","年糕","0","3101000000"') #userId空
Icase("I251_N40_C3","RtnOK","10001482",'"10001482","","20","年糕","","3101000000"') #startIndex空
Icase("I251_N40_C4","RtnSysErr","10001482",'"10001482","0","","年糕","","3101000000"') #pageSize空
Icase("I251_N40_C5","RtnOK","10001482",'"10001482","0","20","","","3101000000"') #likeName空
Icase("I251_N40_C6","RtnOK","10001482",'"10001482","0","20","年糕","","3101000000"') #industryId空
Icase("I251_N40_C7","RtnParamErr","10001482",'"10001482","0","20","年糕","0",""') #cityId空

# 41,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 41，红包群_查看店铺信息接口
print "\nI251_N41 " + ">" * 150
# 文档cityId需要修改成city
Icase("I251_N41_C1","RtnOK","10001588",'"2","2","3100000000"')
Icase("I251_N41_C2","RtnNullOK","10001588",'"","2","3100000000"')
Icase("I251_N41_C3","RtnParamErr","10001588",'"2","","3100000000"')

# 42,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 42，红包群_我的红包群列表接口
print "\nI251_N42 " + ">" * 150
Icase("I251_N42_C1","RtnOK","10001588",'"10001588",')

# 43,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 43, 红包群_我的红包群明细接口
print "\nI251_N43 " + ">" * 150
#文档新增加了两个参数
Icase("I251_N43_C1","RtnOK","10001588",'"10001588","10001598","118"')
Icase("I251_N43_C2","RtnParamErr","10001588",'"10001588","","118"')
Icase("I251_N43_C3","RtnParamErr","10001588",'"10001588","10001598",""')

# 44,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 44, 红包群消息_我的红包群消息列表接口
print "\nI251_N44 " + ">" * 150
Icase("I251_N44_C1","RtnOK","10001588",'"128","10001598"')
Icase("I251_N44_C2","RtnParamErr","10001588",'"118","10001598"')
Icase("I251_N44_C3","RtnParamErr","10001588",'"","10001598"')
Icase("I251_N44_C4","RtnParamErr","10001588",'"128",""')
Icase("I251_N44_C5","RtnParamErr","10001588",'"128","10001591"')

# 45,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 45, 红包群消息_我关注的红包群消息列表接口
print "\nI251_N45 " + ">" * 150
Icase("I251_N45_C1","RtnOK","10001588",'"128","10001598"')
Icase("I251_N45_C1","RtnSysErr","10001588",'"118","10001598"')
Icase("I251_N45_C1","RtnDeviceErr","",'"118","10001598"')
Icase("I251_N45_C1","RtnParamErr","10001588",'"","10001598"')
Icase("I251_N45_C1","RtnParamErr","10001588",'"118",""')
Icase("I251_N45_C1","RtnSysErr","10001588",'"118","10001591"')

# 46,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 46,我的店铺_发抽奖红包接口
print "\nI251_N46 " + ">" * 150
# 先保存抽奖红包模板
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))

# 47,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 47，我的店铺_抽奖红包列表接口
print "\nI251_N47 " + ">" * 150
Icase("I251_N47_C1","RtnOK","10001588",'"0","20"')
Icase("I251_N47_C2","RtnSysErr","10001588",'"",""')

# 48,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 48，我的店铺_抽奖红包详情接口
print "\nI251_N48 " + ">" * 150
curWeb.execute('select max(id) from t_lottery_red where groupId=118')
tbl48= curWeb.fetchone()
Icase("I251_N48_C1","RtnOK","10001482",'"%s,"'% (tbl48[0]))
Icase("I251_N48_C2","RtnSysErr","10001482",'"",')

# 49,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 49, 我的店铺_查看获奖名单接口
print "\nI251_N49 " + ">" * 150
curWeb.execute('select max(id) from t_lottery_red where groupId=118')
tbl49= curWeb.fetchone()
Icase("I251_N49_C1","RtnOK","10001482",'"118",%s,"0","20"' % (tbl49[0]))
Icase("I251_N49_C2","RtnParamErr","10001482",'"",%s,"0","20"' % (tbl49[0]))

# 50,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 50, 我的店铺_修改获奖用户【确认/取消】发货标记接口（依赖60,46,51,52，56）
print "\nI251_N50 " + ">" * 150
# 前提条件:发布一个2分钟后开奖的抽奖红包,一个用户参与抽奖,开奖
# 发抽奖红包
Icase("I251_N60_C1","RtnOK","10001473",'"10001473","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","4"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001473 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001473",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
# 用户参与抽奖
# print varJson
Icase("I251_N52_C1","RtnOK","10001679",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
print "waiting 120s"
sleep(120)
# 开奖批处理
Icase("I251_N56_C1","RtnNullOK","10001588",'')
# 50,修改获奖用户【确认/取消】发货标记接口
Icase("I251_N50_C1","RtnNullOK","10001588",'"10001679",%s,"1"' % (varJson))
Icase("I251_N50_C2","RtnNullOK","10001588",'"10001679",%s,"0"' % (varJson))
##isSend没有判断0和1以后的
#####Icase("I251_N50_C3","RtnNullOK","10001588",'"10001679","36",""')

# 51,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 51, 首页_抽奖平台_抽奖红包列表接口
print "\nI251_N51 " + ">" * 150
# 发抽奖红包
sleep(5)
Icase("I251_N51_C1","RtnOK","10001588",'"0","0","20"')
Icase("I251_N51_C2","RtnOK","10001588",'"1","0","20"')
Icase("I251_N51_C3","RtnOK","10001588",'"3","0","20"')
Icase("I251_N51_C4","RtnSysErr","10001588",'"4","0","20"')

# 52,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 52,红包群_用户参与抽奖红包接口
print "\nI251_N52 " + ">" * 150
# 前提条件:发布一个2分钟后开奖的抽奖红包,一个用户参与抽奖
# 数据库确认: t_lottery_user表新增一条记录, t_lottery_red表 partakeNum+1
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
# print tbl46_1[0],tbl46_1[1]
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
sleep(5)
# print varJson
Icase("I251_N52_C1", "RtnOK", "10001473",'%s,'%(varJson))

# 53,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 53,我的抽奖记录_抽奖记录列表接口
print "\nI251_N53 " + ">" * 150
# 前提条件:发布一个2分钟后开奖的抽奖红包,一个用户参与抽奖
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
print tbl46_1[0],tbl46_1[1]
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
sleep(5)
print varJson
Icase("I251_N52_C1", "RtnOK", "10001473",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
Icase("I251_N53_C1", "RtnOK", "10001473",'"","0","20"') #状态(可选,默认为0. 0:进行中,1:已揭晓,2:中奖)

# 54,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 54,我的抽奖记录_投诉接口
print "\nI251_N54 " + ">" * 150
# 前提条件:用户存在1个已经揭晓的,并且已中奖的抽奖红包
# 数据库变化:t_lottery_user表 isComplain = 1,t_lottery_red表 complainNum+1
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
print tbl46_1[0],tbl46_1[1]
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
sleep(5)
Icase("I251_N52_C1", "RtnOK", "10001473",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
print "waiting 120s"
sleep(120)
Icase("I251_N56_C1", "RtnNullOK","10001482",'') #抽奖红包_开奖批处理接口
sleep(5)
Icase("I251_N54_C1", "RtnNullOK","10001473",'%s,"11111"'%(varJson))
curWeb.execute(
    'select isComplain from t_lottery_user where userId = 10001473 and isLottery = 1 and complainSub = 11111 and lotteryId = %s order by id desc limit 1' %(varJson))
tbl54_1 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl54_1[0],1,"","[errorrrrrrrrrr , t_lottery_user,我的抽奖记录_投诉接口失败!]")

# 55,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 55,我的抽奖记录_删除抽奖记录接口
print "\nI251_N55 " + ">" * 150
# 前提条件:用户存在1个已经揭晓的抽奖红包
# 数据库变化:t_lottery_user表 status = 1
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
print tbl46_1[0],tbl46_1[1]
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
sleep(5)
Icase("I251_N52_C1", "RtnOK", "10001473",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
print "waiting 120s"
sleep(120)
Icase("I251_N56_C1", "RtnNullOK","10001482",'') #抽奖红包_开奖批处理接口
sleep(5)
Icase("I251_N55_C1", "RtnNullOK","10001473",'%s,'%(varJson))
curWeb.execute(
    'select status from t_lottery_user where userId = 10001473 and lotteryId = %s order by id desc limit 1' %(varJson))
tbl55_1 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl55_1[0],1,"","[errorrrrrrrrrr , t_lottery_user,删除抽奖记录失败!]")

# 56,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 56,抽奖红包_开奖批处理接口
print "\nI251_N56 " + ">" * 150
# 前提条件:发布一个2分钟后开奖的抽奖红包,一个用户参与抽奖
# 数据库确认:t_lottery_red表 status = 2, t_lottery_user表 isLottery变化(0:进行中,1:中奖，2;没中奖)
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
print tbl46_1[0],tbl46_1[1]
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
sleep(5)
print varJson
Icase("I251_N52_C1", "RtnOK", "10001473",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
print "waiting 120s"
sleep(120)
Icase("I251_N56_C1", "RtnNullOK","10001482",'')

# 57,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 57,红包群_新用户列表_接受加入请求接口
print "\nI251_N57 " + ">" * 150
# 数据库确认:表t_redgroup_memberinfo增加一条记录(memberState=0,isAuth=0,isCheck=0),表t_redgroup_baseinfo的countNumber+1
curWeb.execute(
    'select id from t_user where id not in (select distinct(userId) from t_redgroup_memberinfo where groupId = 13) and username like "%189%"order by id desc limit 1')
tbl57_1 = curWeb.fetchone()
connWeb.commit()
Icase("I24_N50_C1", "RtnOK", str(tbl57_1[0]), '%s,"13","10001482"' % (tbl57_1[0])) # 红包群_加入红包群接口（新增返回值）
Icase("I251_N57_C1","RtnNullOK","10001482",'"13",%s'  % (tbl57_1[0]))
Icase("I251_N57_C1","RtnParamErr","10001482",'"",%s'  % (tbl57_1[0]))
Icase("I251_N57_C1","RtnParamErr","10001482",'"13",""')

# 58,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 58,红包群_获取新成员列表接口(update)
print "\nI251_N58 " + ">" * 150
# 业务逻辑:加入群ID为13的红包群,查询新成员
# 要确认有返回值:"isAuth":1  //是否通过认证(0:通过,1:未通过)
curWeb.execute(
    'select id from t_user where id not in (select distinct(userId) from t_redgroup_memberinfo where groupId = 13) and username like "%189%"order by id desc limit 1')
tbl58_1 = curWeb.fetchone()
connWeb.commit()
Icase("I24_N50_C1", "RtnOK", str(tbl58_1[0]), '%s,"13","10001482"' % (tbl58_1[0])) # 红包群_加入红包群接口（新增返回值）
varJson = Icase("I251_N58_C1", "RtnOK", "10001482", '"13","10001482","0","20"')
curWeb.execute('select count(id) from t_redgroup_memberinfo where groupId = 13 and userId = %s and isAuth = %s' %(varJson['dataList'][0]['userId'],varJson['dataList'][0]['isAuth']))
tbl58_2 = curWeb.fetchone()
connWeb.commit()
assertEqual(tbl58_2[0],1,"","[errorrrrrrrrrr , t_redgroup_memberinfo,获取新成员列表失败!]")
Icase("I251_N58_C1", "RtnParamErr", "10001482", '"","10001482","0","20"')
Icase("I251_N58_C1", "RtnParamErr", "10001482", '"13","","0","20"')

# 59,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 59,红包模板_模板列表接口(update)
print "\nI251_N59 " + ">" * 150
for i in range(1,8):
    Icase("I251_N59_C1", "RtnOK", "10001482", '"10001482",%s' % str(i))

# 60,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 60,红包模板_新增列表接口(update)
print "\nI251_N60 " + ">" * 150
# 先保存抽奖红包模板
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')

# 61,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 61,红包群_商户信息修改接口
print "\nI251_N61 " + ">" * 150
Icase("I251_N61_C1","RtnNullOK","10002412",'"2","3101000000","17000099999","00:00-23:00","停车,WIFI","http://sit2.88uka.com/000/000/004/757.jpg"')

# 62,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 62,红包群_我的红包群_三藏爆款_用户点评_发点评炸弹接口
print "\nI251_N62 " + ">" * 150
# 业务逻辑:支付一个爆款,发货,确认收货,点评,审核点评,保存好评红包模板
curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
tbl14_1 = curWeb.fetchone()
connWeb.commit()
if (tbl14_1[0] > 0):
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
else:
    Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1","备注"' % tbl14_2[0]) # 三藏爆款_爆款支付接口
curWeb.execute('select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
tbl16_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % tbl16_1[0]) # 销售订单_确认发货接口
Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % tbl16_1[0]) # 我的订单_确认收货接口
# print tbl16_1[0]
Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评好评!!!!!!!!!!!","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl16_1[0])) # 我的订单_订单点评接口
curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_1[0])) # 红包群_我的红包群_三藏爆款_用户点评_审核点评
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","2","好评","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
Icase("I251_N62_C1", "RtnOK", "10001482", '"3","1","1","10001482","13","000000",%s,%s' % ((tbl36_1[0]),varJson))

# 63,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 63,红包群_我的红包群/我是店小二的红包群_私信列表接口
print "\nI251_N63 " + ">" * 150
# 业务逻辑:加入红包群,把群成员设为店小二
curWeb.execute(
  'select id from t_user where id not in (select distinct(userId) from t_redgroup_memberinfo where groupId = 13) and username like "%189%"order by id desc limit 1')
tbl25_1 = curWeb.fetchone()
connWeb.commit()
Icase("I24_N50_C1", "RtnOK", str(tbl25_1[0]), '%s,"13","10001482"' % (tbl25_1[0])) # 红包群_加入红包群接口（新增返回值）
Icase("I251_N27_C1","RtnNullOK","10001482",'"13",%s' % (tbl25_1[0]))
Icase("I251_N63_C1","RtnOK",str(tbl25_1[0]),'%s,"13"' % (tbl25_1[0]))

# 64,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 64,私信_我的店小二_私信点赞接口
print "\nI251_N64 " + ">" * 150
# 逻辑:由于每个用户每天最多可给同1个店小二点赞3次,所以用户给店小二点赞后要删除redis点赞次数
curWeb.execute(
  'select id from t_user order by id desc limit 1')
tbl64_1 = curWeb.fetchone()
connWeb.commit()
curWeb.execute(
  'select count(userId) from t_redgroup_memberinfo where memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1')
tbl64_2 = curWeb.fetchone()
connWeb.commit()
if (tbl64_2[0] > 0):
    curWeb.execute(
        'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1 order by userId limit 1')
    tbl64_3 = curWeb.fetchone()
    connWeb.commit()
    Icase("I251_N64_C1","RtnOK",str(tbl64_1[0]),'%s,"13"' % (tbl64_3[0]))
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    r.delete("tmp:likeWaiter:13:"+str(tbl64_3[0]))
else:
    Icase("I251_N64_C1", "RtnOK", str(tbl64_1[0]), '"10001482","13"')
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    r.delete("tmp:likeWaiter:13:10001482")

# 65,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 65，私信_我的店小二_私信打赏接口
print "\nI251_N65 " + ">" * 150
# 数据库确认:t_user_withdraw增加一条记录
# 字段解释：groupId:群主的ID
curWeb.execute('SELECT COUNT(id) from  t_user_withdraw a WHERE user_id=10001926')
tbl65_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N65_C1", "RtnOK", "10001926",'"10001476","4","10001926"')
tbl65_2 =tbl65_1[0]+1
assertEqual(tbl65_1,tbl65_2,"error","")
Icase("I251_N65_C2", "RtnParamErr", "10001926",'"","4","10001926"')
# 账户余额不足的情况
Icase("I251_N65_C1", "RtnOK", "10001470",'"10001476","4","10001470"')

# 66,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 66,分享抽奖红包到红包群_回调接口
print "\nI251_N66 " + ">" * 150
# 前提条件:发布一个2分钟后开奖的抽奖红包,一个用户参与抽奖分享
# 数据库确认:t_redgroup_message和t_redgroup_messamge_auth表插入一条数据，修改t_redgroup_messamge_auth表isMessage数量
Icase("I251_N60_C1","RtnOK","10001588",'"10001588","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","118"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001588 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001588",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
Icase("I251_N52_C1", "RtnOK", "10001482",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
curWeb.execute('SELECT id from t_redgroup_baseinfo WHERE userid=10001482')
tbl66_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N66_C1", "RtnNullOK", "10001482",'%s,%s,"0"' %(tbl66_1[0],varJson)) #分享抽奖红包到红包群_回调接口
Icase("I251_N66_C2", "RtnParamErr", "10001482",'"118","110","0"')
Icase("I251_N66_C3", "RtnParamErr", "10001482",'"","110","0"')
Icase("I251_N66_C4", "RtnParamErr", "10001482",'"13","","0"')
Icase("I251_N66_C5", "RtnParamErr", "10001482",'"13","110",""')

# 67,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 67,红包群通讯录_我的红包群列表接口
print "\nI251_N67 " + ">" * 150
Icase("I251_N67_C1", "RtnOK", "10001482", '"10001482",')

# 68,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 68,发红包_广告红包发送接口
print "\nI251_N68 " + ">" * 150
# 数据库变化: t_extension_channel_redPool, t_extension_channel_redPic表, t_extension_channel表, t_extension_userdeed_count表, t_operate_audit表增加一条记录,t_user_withdraw表增加一条记录
# t_extension_channel_template表 sendTime 被修改, t_redgroup_countinfo表advertPicURL被修改, t_user表commission_residue被修改, t_redgroup_baseinfo表redCountNumber被修改
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","7","广告","品牌","推广内容","www.baidu.com","vedio.com","1","http://www.t3zang.com/000/000/060/6.png","","13"') #保存红包模板
Icase("I251_N68_C1", "RtnOK", "10001482", '"10001482","1","1","3","0","3101000000","13",%s,"000000"' % varJson)

# 69,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 69,获取用户认证过的群信息接口
print "\nI251_N69 " + ">" * 150
Icase("I251_N69_C1", "RtnOK", "10001482", '"10001482",')

# 70,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 70,私信_获取用户私信聊天头像接口
print "\nI251_N70 " + ">" * 150
Icase("I251_N70_C1", "RtnOK", "10001482", '"13",')

# 71,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 71,首页_抽奖红包TOP5列表接口
print "\nI251_N71 " + ">" * 150
# 逻辑:发一个抽奖红包,用户参与抽奖
Icase("I251_N60_C1","RtnOK","10001482",'"10001482","6","抽奖商品名称","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
curWeb.execute('select id,groupId from t_extension_channel_template where userId =10001482 and type = 6 order by id desc limit 1')
tbl46_1 = curWeb.fetchone()
connWeb.commit()
print tbl46_1[0],tbl46_1[1]
from datetime import datetime
from datetime import timedelta
now2 = datetime.now() + timedelta(minutes=+2)
varJson = Icase("I251_N46_C1", "RtnOK","10001482",'%s,%s,"1","%s"'% (tbl46_1[1],tbl46_1[0],now2.strftime('%Y-%m-%d %H:%M:%S')))
sleep(5)
Icase("I251_N52_C1", "RtnOK", "10001473",'%s,'%(varJson)) #红包群_用户参与抽奖红包接口
Icase("I251_N71_C1", "RtnOK", "10001482", '"10001482",')

# 72,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 72,私信_保存用户私信内容接口
print "\nI251_N72 " + ">" * 150
# 数据库变化: t_user_private_info表增加一条记录
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0  and isWaiter = 0 order by userId desc limit 1')
tbl72_1 = curWeb.fetchone()
connWeb.commit()
curWeb.execute(
  'select count(userId) from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1')
tbl72_2 = curWeb.fetchone()
connWeb.commit()
if (tbl72_2[0] > 0):
    curWeb.execute(
        'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 and isBlack = 0 and isWaiter = 1 and isEnabled = 1 order by userId limit 1')
    tbl72_3 = curWeb.fetchone()
    connWeb.commit()
    Icase("I251_N72_C1","RtnNullOK",str(tbl72_3[0]),'"13",%s,"我是店小二","1","0"' % (tbl72_1[0]))
else:
    Icase("I251_N72_C1", "RtnNullOK", "10001482", '"13",%s,"你是群主","1","0"' % (tbl72_1[0]))

# 73,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 73,首页_发红包_私信红包_发送私信转帐接口(update)
print "\nI251_N73 " + ">" * 150
# 数据库变化: t_user_private_red表, t_user_withdraw表, t_user_private_info表增加一条记录
# t_extension_channel_redPool表type被修改, commission_residue表commission_residue被修改
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl73_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N73_C1", "RtnOK", "10001482", '"10001482","3","1",%s,"13","10001482发送私信转账1元","000000","1"' % (tbl73_1[0]))

# 74,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 74,首页_发红包_私信红包_发送私信红包接口(update)
print "\nI251_N74 " + ">" * 150
# 数据库变化: t_user_private_red表, t_user_withdraw表, t_user_private_info表增加一条记录
# t_extension_channel_redPool表type被修改, commission_residue表commission_residue被修改
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl74_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N74_C1", "RtnOK", "10001482", '"10001482","3","1",%s,"13","10001482发送私信红包1元","000000","","1"' % (tbl74_1[0]))

# 75,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 75,首页_红包群_我的红包群_领私信红包接口(Update)
print "\nI251_N75 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl74_1 = curWeb.fetchone()
connWeb.commit()
sleep(12)
Icase("I251_N74_C1", "RtnOK", "10001482", '"10001482","3","1",%s,"13","10001482发送私信红包1元","000000","","1"' % (tbl74_1[0]))
curWeb.execute(
  'select id,belongId from t_user_private_red where userId = 10001482 and redType = 29 and isValid = 1 order by id desc limit 1')
tbl75_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N75_C1", "RtnOK", str(tbl75_1[1]), '%s,%s,"1"' % (tbl75_1[1],tbl75_1[0]))

# 76,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 76,首页_爆款销售冠军列表接口
print "\nI251_N76 " + ">" * 150
Icase("I251_N76_C1", "RtnNullOK","10001482", '"10001482",')

# 77,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 77,私信_领点评红包炸弹接口
print "\nI251_N77 " + ">" * 150
# 业务逻辑:支付一个爆款,发货,确认收货,点评,审核点评,保存好评红包模板，发送好评红包,私信领取点评红包
curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
tbl14_1 = curWeb.fetchone()
connWeb.commit()
if (tbl14_1[0] > 0):
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
else:
    Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1","备注"' % tbl14_2[0]) # 三藏爆款_爆款支付接口
sleep(10)
curWeb.execute('select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
tbl16_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % tbl16_1[0]) # 销售订单_确认发货接口
Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % tbl16_1[0]) # 我的订单_确认收货接口
Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评好评!!!!!!!!!!!","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl16_1[0])) # 我的订单_订单点评接口
curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_1[0])) # 红包群_我的红包群_三藏爆款_用户点评_审核点评
sleep(10)
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","2","好评","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
Icase("I251_N62_C1", "RtnOK", "10001482", '"3","1","1","10001482","13","000000",%s,%s' % ((tbl36_1[0]),varJson))
curWeb.execute('SELECT id from t_extension_channel_redPool WHERE userId=10001482 and redState=1  order by id desc limit 1')
tbl77_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N77_C1", "RtnOK", "10001473",'%s,' % (tbl77_1[0]))#私信_领点评红包炸弹接口
Icase("I251_N77_C2", "RtnParamErr", "10001473",'"",')
Icase("I251_N77_C3", "RtnSysErr", "10001473",'"4112",')

# 78,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 78,红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
print "\nI251_N78 " + ">" * 150
# 业务逻辑:支付一个爆款,发货,确认收货,点评,审核点评,保存好评红包模板，发送好评红包,分享至红包群
curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
tbl14_1 = curWeb.fetchone()
connWeb.commit()
if (tbl14_1[0] > 0):
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
else:
    Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1","备注"' % tbl14_2[0]) # 三藏爆款_爆款支付接口
curWeb.execute('select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
tbl16_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % tbl16_1[0]) # 销售订单_确认发货接口
Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % tbl16_1[0]) # 我的订单_确认收货接口
Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评好评!!!!!!!!!!!","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl16_1[0])) # 我的订单_订单点评接口
curWeb.execute('select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_1[0])) # 红包群_我的红包群_三藏爆款_用户点评_审核点评
sleep(10)
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","2","好评","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
Icase("I251_N62_C1", "RtnOK", "10001482", '"3","1","1","10001482","13","000000",%s,%s' % ((tbl36_1[0]),varJson))
curWeb.execute('SELECT id from t_extension_channel_redPool WHERE userId=10001482 and redState=1  order by id desc limit 1')
tbl78_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N78_C1", "RtnNullOK", "10001473",'%s,"4","0"' % (tbl78_1[0])) #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
Icase("I251_N78_C2", "RtnParamErr", "10001473",'"6","13","0"')
Icase("I251_N78_C3", "RtnParamErr", "10001482",'"","13","0"')

# 79,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 79,红包群_我的红包群_三藏爆款_用户点评_分享点评红包炸弹回调接口
print "\nI251_N79 " + ">" * 150
# 业务逻辑:支付一个爆款,发货,确认收货,点评,审核点评,保存好评红包模板，发送好评红包,分享至红包群，点击完成回调
curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
tbl14_1 = curWeb.fetchone()
connWeb.commit()
if (tbl14_1[0] > 0):
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
else:
    Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1","备注"' % tbl14_2[0]) # 三藏爆款_爆款支付接口
sleep(10)
curWeb.execute('select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
tbl16_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % tbl16_1[0]) # 销售订单_确认发货接口
Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % tbl16_1[0]) # 我的订单_确认收货接口
Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评好评!!!!!!!!!!!","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl16_1[0])) # 我的订单_订单点评接口
curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_1[0])) # 红包群_我的红包群_三藏爆款_用户点评_审核点评
sleep(10)
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","2","好评","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
Icase("I251_N62_C1", "RtnOK", "10001482", '"3","1","1","10001482","13","000000",%s,%s' % ((tbl36_1[0]),varJson))
curWeb.execute('SELECT id from t_extension_channel_redPool WHERE userId=10001482 and redState=1  order by id desc limit 1')
tbl79_1 = curWeb.fetchone()
connWeb.commit()
print  tbl79_1[0]
Icase("I251_N77_C1", "RtnOK", "10001473",'%s,' % (tbl79_1[0]))#私信_领点评红包炸弹接口
Icase("I251_N78_C1", "RtnNullOK", "10001473",'%s,"4","0"' % (tbl79_1[0])) #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
Icase("I251_N79_C1", "RtnNullOK", "10001473",'%s,"13"' % (tbl79_1[0]))  #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
Icase("I251_N79_C2", "RtnParamErr", "10001473",'"","13"')
Icase("I251_N79_C3", "RtnParamErr", "10001473",'"3955","13"')
Icase("I251_N79_C4", "RtnParamErr", "10001473",'"3955",""')
Icase("I251_N79_C5", "RtnParamErr", "10001473",'"3955","189"')

# 80,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 80,首页_发出红包总个数接口
print "\nI251_N80 " + ">" * 150
Icase("I251_N80_C1", "RtnNullOK", "10001473",'')

# 81,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 81,首页_红包群_抢点评红包接口
print "\nI251_N81 " + ">" * 150
# 业务逻辑:支付一个爆款,发货,确认收货,点评,审核点评,保存好评红包模板，发送好评红包,分享至红包群，点击完成回调,抢点评红包
curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
tbl14_1 = curWeb.fetchone()
connWeb.commit()
if (tbl14_1[0] > 0):
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
else:
    Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1","备注"' % tbl14_2[0]) # 三藏爆款_爆款支付接口
sleep(10)
curWeb.execute('select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
tbl16_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % tbl16_1[0]) # 销售订单_确认发货接口
Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % tbl16_1[0]) # 我的订单_确认收货接口
Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评好评!!!!!!!!!!!","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl16_1[0])) # 我的订单_订单点评接口
curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_1[0])) # 红包群_我的红包群_三藏爆款_用户点评_审核点评
sleep(10)
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","2","好评","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
Icase("I251_N62_C1", "RtnOK", "10001482", '"3","1","1","10001482","13","000000",%s,%s' % ((tbl36_1[0]),varJson))
curWeb.execute('SELECT id from t_extension_channel_redPool WHERE userId=10001482 and redState=1  order by id desc limit 1')
tbl79_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N77_C1", "RtnOK", "10001473",'%s,' % (tbl79_1[0]))#私信_领点评红包炸弹接口
Icase("I251_N78_C1", "RtnNullOK", "10001473",'%s,"4","0"' % (tbl79_1[0])) #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
Icase("I251_N79_C1", "RtnNullOK", "10001473",'%s,"13"' % (tbl79_1[0]))  #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
curWeb.execute('SELECT channelId,groupId,id from t_redgroup_message WHERE batchId=%s  order by id desc limit 1' % (tbl79_1[0]))
tbl81_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N81_C1", "RtnOK", "10001588",'%s,%s,%s,%s' % (tbl79_1[0],tbl81_1[0],tbl81_1[1],tbl81_1[2]))  #首页_红包群_抢点评红包接口
Icase("I251_N81_C2", "RtnParamErr", "10001588",'"","5539","13","95568"')
Icase("I251_N81_C3", "RtnParamErr", "10001588",'"4469","","13","95568"')
Icase("I251_N81_C4", "RtnParamErr", "10001588",'"4469","5539","13",""')

# 82,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 82,首页_红包群_抢点评红包回调接口
print "\nI251_N82 " + ">" * 150
# 业务逻辑:支付一个爆款,发货,确认收货,点评,审核点评,保存好评红包模板，发送好评红包,分享至红包群，点击完成回调,抢点评红包,抢红包回调
curWeb.execute('select COUNT(id) from t_explosion_product where userId=10001482 and status = 0')
tbl14_1 = curWeb.fetchone()
connWeb.commit()
if (tbl14_1[0] > 0):
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
else:
    Icase("I251_N7_C1","RtnOK","10001482",'"13","冼丽琼1482爆款发布","http://www.t3zang.com/000/000/060/6.png","www.baidu.com","500","0","0","1","1","50"') # 7,三藏爆款_发布爆款接口
    curWeb.execute('select id from t_explosion_product where userId=10001482 and status = 0 order by id desc limit 1')
    tbl14_2 = curWeb.fetchone()
    connWeb.commit()
print "waiting 13s"
sleep(13)
Icase("I251_N14_C1","RtnOK","10001473",'"10001473",%s,"13","3","000000","1","备注"' % tbl14_2[0]) # 三藏爆款_爆款支付接口
sleep(10)
curWeb.execute('select id from t_order where userId=10001473 and orderState = 1 order by id desc limit 1')
tbl16_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N16_C1","RtnNullOK","10001482",'"13",%s' % tbl16_1[0]) # 销售订单_确认发货接口
Icase("I251_N19_C1","RtnNullOK","10001473",'%s,' % tbl16_1[0]) # 我的订单_确认收货接口
Icase("I251_N23_C1", "RtnNullOK", "10001473", '%s,"点评好评!!!!!!!!!!!","http://sit2.88uka.com/000/000/004/350.jpg"' % (tbl16_1[0])) # 我的订单_订单点评接口
curWeb.execute(
            'select id from t_review where userId=10001473 and  groupId = 13 and isPraise = 0 order by id desc limit 1')
tbl36_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N36_C1", "RtnOK", "10001482", '"13",%s,"1"' % (tbl36_1[0])) # 红包群_我的红包群_三藏爆款_用户点评_审核点评
sleep(10)
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","2","好评","品牌","推广内容","www.baidu.com","vedio.com","1","http://pic.com","","13"')
Icase("I251_N62_C1", "RtnOK", "10001482", '"3","1","1","10001482","13","000000",%s,%s' % ((tbl36_1[0]),varJson))
curWeb.execute('SELECT id from t_extension_channel_redPool WHERE userId=10001482 and redState=1  order by id desc limit 1')
tbl79_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N77_C1", "RtnOK", "10001473",'%s,' % (tbl79_1[0]))#私信_领点评红包炸弹接口
Icase("I251_N78_C1", "RtnNullOK", "10001473",'%s,"4","0"' % (tbl79_1[0])) #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
Icase("I251_N79_C1", "RtnNullOK", "10001473",'%s,"13"' % (tbl79_1[0]))  #红包群_我的红包群_三藏爆款_用户点评_分享点评红包至红包群权限接口
curWeb.execute('SELECT channelId,groupId,id from t_redgroup_message WHERE batchId=%s  order by id desc limit 1' % (tbl79_1[0]))
tbl81_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N81_C1", "RtnOK", "10001588",'%s,%s,%s,%s' % (tbl79_1[0],tbl81_1[0],tbl81_1[1],tbl81_1[2]))  #首页_红包群_抢点评红包接口
Icase("I251_N82_C1", "RtnOK", "10001588",'%s,%s,%s' % (tbl79_1[0],tbl81_1[0],tbl81_1[1]))  #首页_红包群_抢点评红包回调接口
# 检查红包是否被领取
curWeb.execute('SELECT count(id) from t_external_redDetail WHERE batchId=%s and redState=3 order by id desc limit 1' % (tbl79_1[0]))
tbl81_2 = curWeb.fetchone()
assertEqual(tbl81_2[0], 1, "", "[errorrrrrrrrrr , t_external_redDetail,点评红包被领取失败!]")
Icase("I251_N82_C2", "RtnOK", "10001588",'"4469","5539","13"')  #（领过的情况）
Icase("I251_N82_C3", "RtnParamErr", "10001588",'"","5539","13"')
Icase("I251_N82_C4", "RtnParamErr", "10001588",'"4469","","13"')
Icase("I251_N82_C5", "RtnParamErr", "10001588",'"4469","5539",""')

# 83,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 83,游戏_玩家TOP排名接口
print "\nI251_N83 " + ">" * 150
Icase("I251_N83_C1", "RtnOK","10001588",'')

# 84,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 84,个人钱包_最近的私信转账
print "\nI251_N84 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl73_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N73_C1", "RtnOK", "10001482", '"10001482","3","1",%s,"13","10001482发送私信转账1元","000000","1"' % (tbl73_1[0])) #发送私信转账
Icase("I251_N84_C1", "RtnOK","10001482", '"10001482",')
#
# 85,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 85,个人钱包_私信联系人列表
sleep(10)
print "\nI251_N85 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl73_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N73_C1", "RtnOK", "10001482", '"10001482","3","1",%s,"13","10001482发送私信转账1元","000000","1"' % (tbl73_1[0])) #发送私信转账
Icase("I251_N85_C1", "RtnOK","10001482", '"10001482","0","20"')

# 86,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 86,个人钱包_个人钱包详情接口（update）
print "\nI251_N86 " + ">" * 150
Icase("I251_N86_C1", "RtnOK","10001482", '"10001482",')

# 87,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 87,个人钱包_最近付款群接口
print "\nI251_N87 " + ">" * 150
curWeb.execute(
  'select groupId from t_redgroup_memberinfo where userId = 10001482 and memberState = 0 and isBlack = 0 and isAuth = 0 order by groupId desc limit 1')
tbl89_1 = curWeb.fetchone()
connWeb.commit()
print tbl89_1[0]
Icase("I251_N89_C1", "RtnOK", "10001482",'"10001482","1",%s,"3","000000"' % tbl89_1[0])
Icase("I251_N87_C1", "RtnOK","10001482", '"10001482",')

# 88,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 88,个人钱包_最近联系已商户认证的群列表接口
print "\nI251_N88 " + ">" * 150
Icase("I251_N88_C1", "RtnOK", "10001588",'"10001588","0","20"')
Icase("I251_N88_C2", "RtnParamErr", "10001588",'"","0","20"')

# 89,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 89,个人钱包_转账接口
print "\nI251_N89 " + ">" * 150
# 业务逻辑：本人给我关注的群付款
curWeb.execute('SELECT COUNT(id) from  t_user_withdraw a WHERE user_id=10001588')
tbl89_1 = curWeb.fetchone()
curWeb.execute('SELECT commission_residue from t_user WHERE id =10001588')
tbl89_3 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N89_C1", "RtnOK", "10001588",'"10001588","1","213","3","111111"')
# 验证t_user_withdraw付款记录是否插入
tbl89_2 =tbl89_1[0]+1
assertEqual(tbl89_1,tbl89_2,"error","")
# 验证付款记录是否扣款
tbl89_4 =tbl89_3[0]-100
assertEqual(tbl89_3, tbl89_4, "[error,付款验证失败!]","")
Icase("I251_N89_C2", "RtnParamErr", "10001588",'"","1","213","3","111111"')
Icase("I251_N89_C3", "RtnParamErr", "10001588",'"10001588","-1","213","3","111111"')
Icase("I251_N89_C4", "RtnParamErr", "10001588",'"10001588","1","","3","111111"')
Icase("I251_N89_C5", "RtnParamErr", "10001588",'"10001588","1","213","9","111111"')
Icase("I251_N89_C6", "RtnParamErr", "10001588",'"10001588","1","213","9","11111"')

# 90,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 90,红包群_修改红包群信息接口
print "\nI251_N90 " + ">" * 150
Icase("I251_N90_C1", "RtnOK", "10001588",'"10001588","118","0","品牌内容","http://sit2.88uka.com/000/000/004/350.jpg"')
Icase("I251_N90_C2", "RtnParamErr", "10001588",'"","118","0","品牌内容","http://sit2.88uka.com/000/000/004/350.jpg"')
Icase("I251_N90_C3", "RtnParamErr", "10001588",'"10001588","213","0","品牌内容","http://sit2.88uka.com/000/000/004/350.jpg"')
Icase("I251_N90_C4", "RtnParamErr", "10001588",'"10001588","","0","品牌内容","http://sit2.88uka.com/000/000/004/350.jpg"')
Icase("I251_N90_C5", "RtnParamErr", "10001588",'"10001588","118","9","品牌内容","http://sit2.88uka.com/000/000/004/350.jpg"')

# 91,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 91,个人钱包_个人余额转群账户接口
print "\nI251_N91 " + ">" * 150
curWeb.execute('select id from t_redgroup_baseinfo where userId = 10001482 order by id desc limit 1')
tbl91_1 = curWeb.fetchone()
connWeb.commit()
print tbl91_1[0]
Icase("I251_N91_C1", "RtnNullOK", "10001482",'"10001482",%s,"1"' % tbl91_1[0])

# 92,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 92,个人钱包_群账户转群账户接口
print "\nI251_N92 " + ">" * 150
# 前提条件:用户存在多个红包群
Icase("I251_N92_C1", "RtnNullOK", "10001491",'"10001491","22","1","939"')

# 93,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 93,土豪榜_个人土豪列表接口
print "\nI251_N93 " + ">" * 150
Icase("I251_N93_C1", "RtnOK", "10001588",'"0","20"')
Icase("I251_N93_C2", "RtnSysErr", "10001588",'"",""')

# 94,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 94,土豪榜_商户土豪列表接口
print "\nI251_N94 " + ">" * 150
Icase("I251_N94_C1", "RtnOK", "10001588",'"0","20"')
Icase("I251_N94_C2", "RtnSysErr", "10001588",'"",""')

# 95,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 95,豪榜_获得个人土豪统计信息接口
print "\nI251_N95 " + ">" * 150
Icase("I251_N95_C1", "RtnOK", "10001482",'"10001482","1"')

# 96,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 96,土豪榜_获得分享链接接口（update）
print "\nI251_N96 " + ">" * 150
varJson1 = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","7","广告","品牌","推广内容","www.baidu.com","vedio.com","1","http://www.t3zang.com/000/000/060/6.png","","13"') #保存红包模板
varJson2 = Icase("I251_N68_C1", "RtnOK", "10001482", '"10001482","1","1","3","0","3101000000","13",%s,"000000"' % varJson1)
curWeb.execute(
  'select extensionRedPoolId from t_extension_channel where userId = 10001482 and groupId = 13 and redState = 1 order by id desc limit 1')
tbl97_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N96_C1", "RtnOK", "10001482",'"10001482","25","3","1",%s,"1",%s,"1","0","标题标题标题标题标题标题标题！!","13"' % (tbl97_1[0],varJson2['channelId']))

# 97,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 97,红包群_图文收费提醒接口
# 条件:1个红包群同一人数阶梯内只提醒一次
print "\nI251_N97 " + ">" * 150
Icase("I251_N97_C1", "RtnOK", "10001473",'"10001473","4"')

# 98,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 98,个人_个人主页接口
print "\nI251_N98 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_memberinfo where memberState = 0 and groupId = 13 order by id desc limit 1')
tbl98_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N98_C1", "RtnOK", "10001482",'"10001482","1",%s' % tbl98_1[0])

# 99,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 99,充值_二维码充值修改使用模板接口
print "\nI251_N99 " + ">" * 150
# 业务逻辑：新增二维码红包模版，发送二维码红包，二维码充值修改使用模板接口
varJson = Icase("I251_N60_C1","RtnOK","10001482",'"10001482","7","广告","品牌","推广内容","www.baidu.com","vedio.com","1","http://www.t3zang.com/000/000/060/6.png","","13"') #保存红包模板
Icase("I251_N68_C1", "RtnOK", "10001482", '"10001482","1","1","3","0","3101000000","13",%s,"000000"' % varJson)
curWeb.execute('SELECT id from  t_extension_channel_redPool WHERE redType=40 and redState=1 and userId=10001482 ORDER BY id DESC LIMIT 1')
tbl99_1 = curWeb.fetchone()
print tbl99_1[0]
curWeb.execute('SELECT id FROM t_extension_channel_template WHERE userId=10001482 ORDER BY id DESC LIMIT 1')
tbl99_2 = curWeb.fetchone()
curWeb.execute('SELECT templateId FROM t_extension_channel_redPool WHERE userId=10001482 ORDER BY id DESC LIMIT 1')
tbl99_3 = curWeb.fetchone()
Icase("I251_N99_C1", "RtnOK", "10001482",'"10001482",%s,%s'%(tbl99_1[0],tbl99_2[0]))
# 验证t_extension_channel_redPool模板id是否替换
assertEqual(varJson,tbl99_3[0],"","[error,模板templateId替换失败!]")
Icase("I251_N99_C2", "RtnParamErr", "10001482",'"","",""')
Icase("I251_N99_C3", "RtnParamErr", "10001482",'"10001482","",""')
Icase("I251_N99_C4", "RtnParamErr", "10001482",'"10001482","4620",""')

# 100,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 100, 第三方绑定手机号接口  (该接口只能跑一次绑定成功后无法再次使用)
# print "\nI251_N100 " + ">" * 150
# 业务逻辑：第三方登录获取验证码，第三方绑定手机号
# Icase("I250_N6_C1", "RtnOK", "10002407",'"10002407","17000000299","6"')#I250_我_设置_提现密码_获取设置提现密码验证码
# Icase("I251_N100_C1", "RtnOK", "10002407",'"17000000299","3101000000",%s'% Icommon3("6","17000000299"))
# Icase("I251_N100_C2", "RtnParamErr", "10002407",'"17000000299","3101000000","5655"')
# Icase("I251_N100_C3", "RtnDeviceErr", "10002407",'"","3101000000","5655"')
# Icase("I251_N100_C4", "RtnDeviceErr", "10002407",'"17000000299","","5655"')
#
# # 101,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 101, 创建商户群接口--------不适合自动化需要更改数据，和系统后台审核————————————
# print "\nI251_N101 " + ">" * 150
# # 业务逻辑：新建商户（新建群状态为-1），个人认证，商户认证，后台商户审核通过修改新建商户t_redgroup_baseinfo的groupState的状态
# Icase("I251_N101_C1", "RtnOK", "10002414",'"10002414","3101000000","4"')
# #个人认证填写商户id
# Icase("I251_N3_C1","RtnOK","10002414",'"10002414","980","aa","431222199206290017","5,6,7","17000999997", %s,"4","3101000000"' % Icommon3("5","17000999997"))
# #商户认证填写新建商户的群ID
# Icase("I251_N5_C1","RtnNullOK","10002413",'"10002413","978","144","动量","好店","3101000000","长沙f市","芙蓉路","详细地址","0","1","17000099998","09:00","其他","5","0","www.abidu.com","0","1","17000099998", %s,"3","3101000000"' % Icommon3("5","17000099998"))

# # 102,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 102,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)
# print "\nI251_N102 " + ">" * 150
Icase("I251_N102_C1", "RtnOK", "10001588",'"10001588","0","20","1"')
Icase("I251_N102_C2", "RtnParamErr", "10001588",'"","0","20","1"')
Icase("I251_N102_C3", "RtnSysErr", "10001588",'"10001588","","",""')
#
# 103,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 103,首页_发红包炸弹_设置广告内容问号接口
print "\nI251_N103 " + ">" * 150
varJson=Icase("I251_N103_C1", "RtnOK", "10001588",'"7"')
varJson1='http://payment.rrzsh.com/WebBusi/h5tsz/appDesc/adRedDesc7.html'
assertEqual(varJson,varJson1,"","[error,广告内容问号验证失败!]")
Icase("I251_N103_C2", "RtnParamErr", "10001588",'"9"')

# 104,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 104,我_购物订单_我的订单红点接口
print "\nI251_N104 " + ">" * 150
Icase("I251_N104_C1", "RtnOK", "10001486", '"10001486",')

# 105,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 105,红包群_我的红包群_三藏爆款_销售订单红点接口
print "\nI251_N105 " + ">" * 150
Icase("I251_N105_C1", "RtnOK", "10001493", '"24",')

# 106,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 106,查看用户是否发过红包接口
print "\nI251_N106 " + ">" * 150
Icase("I251_N106_C1", "RtnOK", "10001493", '"10001493",')

# 107,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 107,发私信红包_选择分享群成员接口
print "\nI251_N107 " + ">" * 150
varJson = Icase("I251_N74_C1", "RtnOK", "10001482", '"10001482","3","0.01","","0","10001482发送私信红包0.01元","000000","","1"')
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 13 and memberState = 0 order by userId desc limit 1')
tbl107_1 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N107_C1", "RtnNullOK", "10001482", '"10001482","13",%s,%s' % (tbl107_1[0],varJson['id']))

# 108,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 108,店铺信息_修改商铺信息接口
print "\nI251_N108 " + ">" * 150
curWeb.execute(
  'select userId from t_redgroup_baseinfo where id = (select groupId from t_entity_store_certification where auditState = 2 order by id desc limit 1)')
tbl108_1 = curWeb.fetchone()
connWeb.commit()
curWeb.execute(
  'select groupId from t_entity_store_certification where auditState = 2 order by id desc limit 1')
tbl108_2 = curWeb.fetchone()
connWeb.commit()
Icase("I251_N108_C1", "RtnNullOK", str(tbl108_1[0]),'"停车","15618377966","9:00-23:00",%s,"2","http://www.t3zang.com/000/000/060/6.png"' % (tbl108_2[0]))

# 109,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 109,群账户_群账户充值接口
print "\nI251_N109 " + ">" * 150
Icase("I251_N109_C1", "RtnNullOK", "10001493", '"10001493","0.01","3","965","000000"')

# 110,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nI251_N110 " + ">" * 150
# 110,群账户_群账户转个人账户接口
Icase("I251_N110_C1", "RtnNullOK", "10001493", '"10001493","0.01","24"')

# 111,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nI251_N111 " + ">" * 150
# 111,获取红包群状态信息接口
Icase("I251_N111_C1", "RtnOK", "10001493", '"10001493","24"')

# 112,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nI251_N112 " + ">" * 150
# 112,获取红包群状态信息接口
curWeb.execute(
  'select userId from t_redgroup_memberinfo where groupId = 24 and memberState = 0 and isBlack = 0 order by userId desc limit 1')
tbl112_1 = curWeb.fetchone()
connWeb.commit()
print tbl112_1
Icase("I251_N112_C1", "RtnOK", "10001493", '"10001493",%s' % tbl112_1[0])

# 113,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print "\nI251_N113 " + ">" * 150
# 113,红包群_我关注的红包群_群置顶接口
Icase("I251_N113_C1", "RtnOK", "10001588", '"118",')


