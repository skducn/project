# coding: utf-8
#****************************************************************
# Author     : John
# Version    : V 2.5.0
# Date       : 2016-7
# Description: 三藏红包 2.5.0 app接口文档 1-44
#****************************************************************
# 使用说明:
# 1,Icase() 中参数规则及说明,
# 参数1 = 接口 + 序号 + 用例序号 , 如"I251_N6_C1" 表示 i251接口文档中序号为6的测试用例1
# 参数2 = 测试返回类型 ,
# 参数3 ~ 参数N = 依据接口实际的参数数量传递 (注意:参数3-参数N 外层需加上单引号 ' )


import os,sys,requests,xlwt,xlrd,MySQLdb,datetime,redis,smtplib,time
import datetime #导入日期时间模块

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


def I22_19(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    # 参数: userID = 用户ID ,acceptId=收件人ID, groupId= 群ID, content=信息内容 ,isGroup=是否为群主(0:否,1:是)
    varInterfaceName =  "I22_19,保存用户私信内容接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivate/2.2/save_user_private_info.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,acceptId=param2,groupId=param3,content=param4,isGroup=param5)
def sendemail(varTitle,varContent):
    # 邮箱配置
    sender = '<jinhao@mo-win.com.cn>'
    receiver = 'jinhao@mo-win.com.cn'
    msg = MIMEText(varContent,'text','utf-8')
    msg['Subject'] = varTitle  # u'三藏红包gameTAble'
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com')
        smtp.login('jinhao@mo-win.com.cn','Jinhao123')
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(e)
def Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,**query):
     r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
     varverifyCode = r.hget("app:verify:"+varuserId,"code")
     query1={}
     query1["verifyUserId"]= varuserId
     query1["verifyCode"]=varverifyCode
     for x in query:
        query1[x] =  str(query[x])
     headers = {'cache-control': "no-cache"}
     response = requests.request("GET", varUrl, headers=headers, params=query1)
     try:
        if varnum=="RtnNullOK" :  #如:{"data":null,"errorstr":"","errorcode":0,"success":true}
            if response.json()['success']==True:print "[OK,RtnNullOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnNullOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
        if varnum=="RtnOK" : #如:{"data":149,"errorstr":"","errorcode":0,"success":true}
            if response.json()['success']==True and len(str(response.json()['data']))>0:print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
        if varnum=="RtnNoDATAOK" : # 如:{"data":[],"errorstr":"","errorcode":0,"success":true}
            if response.json()['success'] == True and response.json()['data'] == []:print "[OK,RtnNoDATAOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnNoDATAOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else: print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnDeviceErr" :
            if response.json()['errorcode']==100003 and response.json()['success']== False:print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
                sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
     except Exception,data:
        print Exception,":",data,"\n"


# [Testcase]
# i15 -I39错误 ,I38 ,I19

# Icase("I250_N1_C1","RtnOK","10001679",'')
# Icase("I250_N2_C1","RtnOK","10001679",'"13816109050","3101000000","1","0",u"令狐冲","","","",Icommon3("1","13816109050"),"C2-1,手机号,城市ID,下载渠道,渠道(手机),第三方昵称,第三方头像,token,微信唯一标识别(空),验证码"')
#
# # 3 我_设置_点击授权，找回红包_第三方绑定接口(微信标识无法获取?)
# # I25_3("I250_N10_C","RtnOK","10001679",'"10001679","0","John","","","3101000000","")
#
# Icase("I250_N4_C1","RtnOK","10001679",'"10001679",')
# Icase("I250_N4_C2","RtnDeviceErr","10001679",'"",')
# Icase("I250_N4_C3","RtnDeviceErr","10001679",'"123456789",')

# Icase("I250_N5_C1","RtnOK","10001679",'')

# Icase("I250_N6_C1","RtnOK","10001679",'"10001679","13816109050","1"')
# Icase("I250_N6_C2","RtnOK","10001679",'"10001679","13816109050","2"')
# Icase("I250_N6_C3","RtnOK","10001679",'"10001679","13816109050","4"')
# Icase("I250_N6_C4","RtnParamErr","10001679",'"10001679","13816109050",""')

# Icase("I250_N7_C1","RtnOK","10001679",'"10001679","13816109050","123456",%s' % Icommon3("4","13816109050"))
# Icase("I250_N7_C2","RtnParamErr","10001679",'"10001679","13816109050","123456","0000"')
# Icase("I250_N7_C3","RtnParamErr","10001679",'"10001679","13816109050","123456000",%s' % Icommon3("4","13816109050"))
# Icase("I250_N7_C4","RtnParamErr","10001679",'"10001679","13816109050","123456",""')
# Icase("I250_N7_C5","RtnParamErr","10001679",'"10001679","13816109050","",%s' % Icommon3("4","13816109050"))

# 8,我_设置_提现密码_修改提现密码接口
# Icase("I250_N8_C1","RtnNullOK","10001679",'"10001679","123456","111111"')
# Icase("I250_N8_C2","RtnNullOK","10001679",'"10001679","111111","111111"')
# Icase("I250_N8_C3","RtnParamErr","10001679",'"10001679","666666","111111"')
# Icase("I250_N8_C4","RtnParamErr","10001679",'"10001679","","111111"')
# Icase("I250_N8_C5","RtnParamErr","10001679",'"10001679","666666",""')
# Icase("I250_N8_C6","RtnParamErr","10001679",'"10001679","",""')

# # 9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)
# Icase("I250_N9_C1","RtnOK","10001679",'"10001679","213","1","1"')
# # 10,红包模板_红包类型列表, 类型1=广告红包炸弹 ; 2=好评红包 ; 3=普通群红包 ; 4=普通群红包 ; 5=私信红包
# Icase("I250_N10_C1","RtnOK","10001679",'"10001679","1"')
# Icase("I250_N10_C2","RtnOK","10001679",'"10001679","2"')
# Icase("I250_N10_C3","RtnOK","10001679",'"10001679","3"')
# Icase("I250_N10_C4","RtnOK","10001679",'"10001679","4"')
# Icase("I250_N10_C5","RtnOK","10001679",'"10001679","5"')
# Icase("I250_N10_C6","RtnNoDATAOK","10001679",'"10001679","6"')

# # 11,红包模板_红包模板列表
# Icase("I250_N11_C1","RtnOK","10001679",'"10001679","1","1","1"')
# Icase("I250_N11_C2","RtnOK","10001679",'"10001679","2","1","1"',)
# Icase("I250_N11_C3","RtnOK","10001679",'"10001679","3","1","1"',)
# Icase("I250_N11_C4","RtnOK","10001679",'"10001679","4","1","1"',)
# Icase("I250_N11_C5","RtnOK","10001679",'"10001679","5","1","1"',)
# Icase("I250_N11_C6","RtnParamErr","10001679",'"10001679","66","1","1"')

# 12,	红包模板_保存红包模板 ,1-5 分别对应 t_sys_config 表里5个类型
# Icase("I250_N12_C1","RtnOK","10001679",'"10001679","1","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com",""')
# Icase("I250_N12_C2","RtnOK","10001679",'"10001679","2","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com",""')
# Icase("I250_N12_C3","RtnOK","10001679",'"10001679","3","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com",""')
# Icase("I250_N12_C4","RtnOK","10001679",'"10001679","4","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com",""')
# Icase("I250_N12_C5","RtnOK","10001679",'"10001679","5","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com",""')
# Icase("I250_N12_C6","RtnParamErr","10001679",'"10001679","166","title1","pinpai","neirong","www.baidu.com","vedio.com","166","http://pic.com",""')


# # 13,红包模板_删除红包模板
# Icase("I250_N13_C1","RtnNullOK","10001679",'"10001679","1"')
# Icase("I250_N13_C2","RtnNullOK","10001679",'"10001679","2"')
# Icase("I250_N13_C3","RtnNullOK","10001679",'"10001679","3"')
# Icase("I250_N13_C4","RtnNullOK","10001679",'"10001679","4"')
# Icase("I250_N13_C5","RtnNullOK","10001679",'"10001679","5"')

# # 14 首页_红包群_我的红包群私信详情接口(新增返回值) ,依赖于I22_19群主与群成员各自互相发送1条私信消息
# I22_19("RtnOK","10002084",'"10002084","10002290","610","10002084_保存用户私信内容接口发送的消息","1","C19-1,用户ID ,收件人ID, 群ID, 信息内容 ,是否为群主(0:否,1:是)")
# I22_19("RtnOK","10002290","10002290","10002084","815","10002290_保存用户私信内容接口发送的消息","1","C19-2,用户ID ,收件人ID, 群ID, 信息内容 ,是否为群主(0:否,1:是)")
# Icase("I250_N14_C1","RtnOK","10002084",'"10002290","610","0","20","10002084","1"')
# Icase("I250_N14_C2","RtnOK","10002290",'"10002084","610","0","20","10002290","0"')
# Icase("I250_N14_C3","RtnOK","10002290",'"10002084","815","","20","10002290","1"')
# Icase("I250_N14_C4","RtnSysErr","10002290",'"10002084","815","0","","10002290","1"') #每页显示条数为空时,取默认参数每页20条
# Icase("I250_N14_C5","RtnSysErr","10002290",'"10002084","815","","","10002290","1"',) #每页显示条数为空时,取默认参数每页20条
# Icase("I250_N14_C6","RtnParamErr","10002084",'"","610","0","20","10002290","1"')
# Icase("I250_N14_C7","RtnParamErr","10002084",'"10002084","","0","20","10002290","1"')
# Icase("I250_N14_C8","RtnParamErr","10002084",'"10002084","","0","20","","1"')
# Icase("I250_N14_C9","RtnParamErr","10002084",'"10002084","","0","20","10002290",""')
# Icase("I250_N14_C10","RtnParamErr","10002084",'"00002084","610","0","20","10002290","1"')
# Icase("I250_N14_C11","RtnParamErr","10002084",'"10002084","000","0","20","10002290","1"')
# Icase("I250_N14_C12","RtnParamErr","10002084",'"10002084","610","-1","20","10002290","1"')
# Icase("I250_N14_C13","RtnParamErr","10002084",'"10002084","610","0.1","20","10002290","1"')
# Icase("I250_N14_C14","RtnParamErr","10002084",'"10002084","610","0","-1","10002290","1"')
# Icase("I250_N14_C15","RtnParamErr","10002084",'"10002084","610","0","0.5","10002290","1"')
# Icase("I250_N14_C16","RtnParamErr","10002084",'"10002084","610","0","20","00002290","1"')
# Icase("I250_N14_C17","RtnParamErr","10002084",'"10002084","610","0","20","10002290","0"')
# Icase("I250_N14_C18","RtnParamErr","10002084",'"10002084","610","0","20","10002290","2"')

# #15首页_红包群_我的红包群_领私信转账接口(依赖Icase)
# 39首页_发红包_私信红包_发送私信转帐接口(间隔10s)
# # "C39-1,用户ID ,支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , 红包金额, 收红包用户ID ,群ID ,信息内容(可选) ,支付密码(可选,支付类型3、5必传)"
# Icase("I250_N39_C1","RtnOK","10002084",'"10002084","3","1","10002290","610","10002084给10002290发送私信转账1元","000000"')
# print "   ...waiting 12s"
# sleep(12)
# Icase("I250_N15_C1","RtnOK","10002290",'"10002290","3"')
# Icase("I250_N15_C2","RtnDeviceErr","10002290",'"","3"')
# Icase("I250_N15_C3","RtnParamErr","10002290",'"10002290",""')
# Icase("I250_N15_C4","RtnDeviceErr","10002290",'"",""')
# Icase("I250_N15_C5","RtnDeviceErr","10002290",'"00002290","3"')
# Icase("I250_N15_C6","RtnDeviceErr","10002290",'"0.01","3"')
# Icase("I250_N15_C7","RtnDeviceErr","10002290",'"-1","3"')
# Icase("I250_N15_C8","RtnParamErr","10002290",'"10002290","0.1"')
# Icase("I250_N15_C9","RtnParamErr","10002290",'"10002290","0"')
# Icase("I250_N15_C10","RtnParamErr","10002290",'"10002290","-1"')


# #16首页_红包群_我的红包群_转账详情接口
# Icase("I250_N16_C1","RtnOK","10002084",'"10002084","3"')
# Icase("I250_N16_C2","RtnOK","10002290",'"10002290","3"')
# Icase("I250_N16_C3","RtnDeviceErr","10002290",'"","3"')
# Icase("I250_N16_C4","RtnParamErr","10002290",'"10002290",""')
# Icase("I250_N16_C5","RtnDeviceErr","10002290",'"",""')
# Icase("I250_N16_C6","RtnDeviceErr","10002290",'"00002290","3"')
# Icase("I250_N16_C7","RtnDeviceErr","10002290",'"0.01","3"')
# Icase("I250_N16_C8","RtnDeviceErr","10002290",'"-1","3"')
# Icase("I250_N16_C9","RtnParamErr","10002290",'"10002290","0.1"')
# Icase("I250_N16_C10","RtnParamErr","10002290",'"10002290","0"')
# Icase("I250_N16_C11","RtnParamErr","10002290",'"10002290","-1"')

# # #17首页_红包群_我的红包群_重新发送私信转账接口(依赖于Icase)
# # 39首页_发红包_私信红包_发送私信转帐接口
# Icase("I250_N39_C1","RtnOK","10002084",'"10002084","3","1","10002290","610","10002084给10002290发送私信转账1元","000000"')
# print "   ...waiting 12s"
# sleep(12)
# curWeb.execute('select id from t_user_private_red where userId=10002084 and belongId=10002290 order by id desc limit 1')
# tbl17 = curWeb.fetchone()
# connWeb.commit()
# Icase("I250_N17_C1","RtnOK","10002084",'"10002084",%s' % str(tbl17[0]))  # 转账信息已过期??
# Icase("I250_N17_C2","RtnDeviceErr","10002084",'"","6"')
# Icase("I250_N17_C3","RtnParamErr","10002084",'"10002084",""')
# Icase("I250_N17_C4","RtnDeviceErr","10002084",'"",""')
# Icase("I250_N17_C5","RtnDeviceErr","10002084",'"00002084","30"')
# Icase("I250_N17_C6","RtnDeviceErr","10002084",'"0.01","6"')
# Icase("I250_N17_C7","RtnDeviceErr","10002084",'"-1","6"')
# Icase("I250_N17_C8","RtnParamErr","10002084",'"10002084","0.1"')
# Icase("I250_N17_C9","RtnParamErr","10002084",'"10002084","0"')
# Icase("I250_N17_C10","RtnParamErr","10002084",'"10002084","-1"')
#
# #18首页_红包群_我的红包群_私信转账退回接口 (依赖Icase)
# Icase("I250_N39_C1","RtnOK","10002084",'"10002084","5","1","10002290","610","10002084给10002290发送私信转账1元","000000"')
# curWeb.execute('select id from t_user_private_red where userId=10002084 and belongId=10002290 order by id desc limit 1')
# tbl18 = curWeb.fetchone()
# connWeb.commit()
# Icase("I250_N18_C1","RtnOK","10002290",'"10002290",%s' % tbl18[0])  #红包信息不匹配 ???
# Icase("I250_N18_C2","RtnDeviceErr","10002290",'"",%s' % tbl18[0])
# Icase("I250_N18_C3","RtnParamErr","10002290",'"10002290",""')
# Icase("I250_N18_C4","RtnDeviceErr","10002290",'"",""')
# Icase("I250_N18_C5","RtnDeviceErr","10002290",'"00002290",%s' % tbl18[0])
# Icase("I250_N18_C6","RtnDeviceErr","10002290",'"0.01",%s' % tbl18[0])
# Icase("I250_N18_C7","RtnDeviceErr","10002290",'"-1",%s' % tbl18[0])
# Icase("I250_N18_C8","RtnParamErr","10002290",'"10002290","0.1"')
# Icase("I250_N18_C9","RtnParamErr","10002290",'"10002290","0"')
# Icase("I250_N18_C10","RtnParamErr","10002290",'"10002290","-1"')


# # #19首页_红包群_我的红包群_领私信红包接口(依赖Icase)
# # # #38首页_发红包_私信红包_发送私信红包接口
# # ,"C38-1,用户ID ,支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , 红包金额, 收红包用户ID ,群ID ,信息内容(可选) ,支付密码(可选,支付类型3、5必传) ,模板(可选)"
# Icase("I250_N38_C1","RtnOK","10002084",'"10002084","3","1","10002290","610","10002084给10002290发送私信红包10","000000",""')
# Icase("I250_N19_C1","RtnOK","10002290",'"10002290","2"')
# Icase("I250_N19_C2","RtnDeviceErr","10002290",'"","2"')
# Icase("I250_N19_C3","RtnParamErr","10002290",'"10002290",""')
# Icase("I250_N19_C4","RtnDeviceErr","10002290",'"",""')
# Icase("I250_N19_C5","RtnDeviceErr","10002290",'"00002290","2"')
# Icase("I250_N19_C6","RtnDeviceErr","10002290",'"0.01","2"')
# Icase("I250_N19_C7","RtnDeviceErr","10002290",'"-1","2"')
# Icase("I250_N19_C8","RtnParamErr","10002290",'"10002290","0.1"')
# Icase("I250_N19_C9","RtnParamErr","10002290",'"10002290","0"')
# Icase("I250_N19_C10","RtnParamErr","10002290",'"10002290","-1"')


# # #20首页_红包群_我的红包群_私信红包详情接口
# Icase("I250_N20_C1","RtnOK","10002084",'"10002084","2"')
# Icase("I250_N20_C2","RtnOK","10002290",'"10002290","2"')
# Icase("I250_N20_C3","RtnDeviceErr","10002290",'"","2"')
# Icase("I250_N20_C4","RtnParamErr","10002290",'"10002290",""')
# Icase("I250_N20_C5","RtnDeviceErr","10002290",'"",""')
# Icase("I250_N20_C6","RtnDeviceErr","10002290",'"00002290","2"')
# Icase("I250_N20_C7","RtnDeviceErr","10002290",'"0.01","2"')
# Icase("I250_N20_C8","RtnDeviceErr","10002290",'"-1","2"')
# Icase("I250_N20_C9","RtnParamErr","10002290",'"10002290","0.1"')
# Icase("I250_N20_C10","RtnParamErr","10002290",'"10002290","0"')
# Icase("I250_N20_C11","RtnParamErr","10002290",'"10002290","-1"')

# # 21,红包群_我的红包群_发普通红包接口
# # 注意事项: 连续发普通红包需间隔10s
# # 前置条件: 10002084账号要有余额 , 默认设置100元, t_redgroup_baseinfo,groupAccount=10000(100元) ; redis同步修改为10000.
curWeb.execute('update t_redgroup_baseinfo set groupAccount=10000 where userId=10002084')
connWeb.commit()
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10002084","groupAccount",10000)
sleep(2)
# 红包金额10元
Icase("I250_N21_C1","RtnOK","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084"') #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
print "   ...waiting 13s"
sleep(13)

# 红包金额5.234元
Icase("I250_N21_C2","RtnOK","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","5.237","4","000000","","10002084"') #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
print "   ...waiting 13s"
sleep(13)

# 红包金额 0.03元
Icase("I250_N21_C3","RtnOK","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","0.03","4","000000","","10002084"') #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
# 检查扣费情况
curWeb.execute('select groupAccount from t_redgroup_baseinfo where userId=10002084')
tbl21 = curWeb.fetchone()
connWeb.commit()
if tbl21[0]==8474:print "  => [Ok,C21-1,t_redgroup_baseinfo,扣费计算正确]"
else:print "  => [errorrrrrrrrrr,C21-1,t_redgroup_baseinfo,扣费计算错误,预期:8474,实测:" + str(tbl21[0]) + "]"
Icase("I250_N21_C4","RtnParamErr","10002084",'"","3101000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084"')
Icase("I250_N21_C5","RtnParamErr","10002084",'"610","","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084"')
sleep(13)
Icase("I250_N21_C6","RtnOK","10002084",'"610","3101000000","","1","10","4","000000","","10002084"')
Icase("I250_N21_C7","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","","10","4","000000","","10002084"') #bug
Icase("I250_N21_C8","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","","4","000000","","10002084"')
Icase("I250_N21_C9","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","","000000","","10002084"')
Icase("I250_N21_C10","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","","10002084"')
Icase("I250_N21_C11","RtnDeviceErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","",""')
Icase("I250_N21_C12","RtnParamErr","10002084",'"000","3101000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084"')
sleep(10)
Icase("I250_N21_C13","RtnOK","10002084",'"610","0000000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084"') #城市ID不做判断,对系统没影响
Icase("I250_N21_C14","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","0","10","4","000000","","10002084"')
Icase("I250_N21_C15","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","-1","10","4","000000","","10002084"')
# Icase("I250_N11_C","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","0.01","10","4","000000","","10002084","C21-14,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #bug
Icase("I250_N21_C16","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","-1","4","000000","","10002084"')
Icase("I250_N21_C17","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","0","4","000000","","10002084"')
Icase("I250_N21_C18","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","0.001","4","000000","","10002084"')
Icase("I250_N21_C19","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","0.025","4","000000","","10002084"')
Icase("I250_N21_C20","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","0","000000","","10002084",')
Icase("I250_N21_C21","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","5","000000","","10002084",')
Icase("I250_N21_C22","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","-1","000000","","10002084"')
Icase("I250_N21_C23","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","0.1","000000","","10002084"')
Icase("I250_N21_C24","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","0","10002084"')
Icase("I250_N21_C25","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","-1","10002084"')
Icase("I250_N21_C26","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","0.1","10002084"')
Icase("I250_N21_C27","RtnParamErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","0000000","10002084"')
Icase("I250_N21_C28","RtnDeviceErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","",""')
Icase("I250_N21_C29","RtnDeviceErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","","000"')
Icase("I250_N21_C30","RtnDeviceErr","10002084",'"610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","","-1"')

print "22,================================================================================================="
# #22红包群_我的红包群_发普通红包设置标签接口(依赖于21)
# 业务逻辑: 红包群中发送普通红包,点击塞进红包后,选择标签发送红包,标签ID为0 表示所有群成员可见 , 多个标签ID以逗号分隔表示发送到多个标签下
# 前置条件: 红包群中存在标签(ID), select id from t_redgroup_label where groupId=610 (2182,2183)
# 动态参数: 接口21 返回值 batchId=批次ID, channelId=渠道ID
# 数据库: 表 t_redgroup_message , t_redgroup_message_auth新增一条记录; t_redgroup_memberinfo中对应标签下的非黑名单群成员的isMessage + 1
# t_redgroup_message ,type类型说明: 0文字消息,1红包炸弹消息,2分享消息,3抢到红包消息,4分享奖励消息,5广告红包抢完消息,6第一次加入消息,7图片消息,8:普通红包消息,9:拼手气红包消息,10:广告红包消息,11:抢到普通红包消息,12:抢到拼手气红包消息,13：抢到广告红包消息,14:普通红包抢完消息,15：拼手气红包抢完消息
# 检查标签ID=0 时情况
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I250_N21_C1","RtnOK","10002084",'"610","3101000000",varAutoMessage,"1","10","4","000000","","10002084"')
curWeb.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curWeb.fetchone()
connWeb.commit()
Icase("I250_N22_C1","RtnOK","10002084",'"10002084","610",tbl3[1],tbl3[0],"0"')
# 检查数据库记录是否生成
curWeb.execute('select count(id),id from t_redgroup_message where groupId=610 and type=8 and channelId=%s and batchId=%s order by id desc' %(tbl3[0],tbl3[1]))
tbl4 = curWeb.fetchone()
if tbl4[0] == 1 :print "OK,Icase,t_redgroup_message,生成一条记录"
else: print "Error,Icase,t_redgroup_message,未生成新记录!"
curWeb.execute('select count(id) from t_redgroup_messamge_auth where groupId=610 and messageId=%s'%(tbl4[1]))
tbl5 = curWeb.fetchone()
if tbl5[0] == 1 :print "OK,Icase,t_redgroup_messamge_auth,生成一条记录"
else: print "Error,Icase,t_redgroup_messamge_auth,未生成新记录!"

# 检查1个标签ID情况
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I250_N21_C1","RtnOK","10002084",'"610","3101000000",varAutoMessage,"1","10","4","000000","","10002084"')
curWeb.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curWeb.fetchone()
Icase("I250_N22_C1","RtnOK","10002084",'"10002084","610",tbl3[1],tbl3[0],"2182"')
print "   ...waiting 13s"
sleep(13)

# 检查多个标签ID情况
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I250_N21_C1","RtnOK","10002084",'"610","3101000000",varAutoMessage,"1","10","4","000000","","10002084"')
curWeb.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curWeb.fetchone()
Icase("I250_N22_C2","RtnOK","10002084",'"10002084","610",tbl3[1],tbl3[0],"2182,2183"')
Icase("I250_N12_C3","RtnDeviceErr","10002084","","610","3412","4505","2611"'')
Icase("I250_N22_C4","RtnParamErr","10002084",'"10002084","","3412","4505","2611"')
Icase("I250_N22_C5","RtnParamErr","10002084",'"10002084","610","","4505","2611"')
Icase("I250_N22_C6","RtnParamErr","10002084",'"10002084","610","3412","","2611"')
Icase("I250_N22_C7","RtnParamErr","10002084",'"10002084","610","3412","","2611"')
Icase("I250_N22_C8","RtnDeviceErr","10002084","0002084","610","3412","4505","2611"'')
Icase("I250_N22_C9","RtnParamErr","10002084",'"10002084","000","3412","4505","2611"')
Icase("I250_N22_C10","RtnParamErr","10002084",'"10002084","610","00","4505","2611"')
Icase("I250_N22_C11","RtnParamErr","10002084",'"10002084","610","3412","00","2611"')
Icase("I250_N22_C12","RtnParamErr","10002084",'"10002084","610","3412","4505","01"')

# print "23,================================================================================================="
# # #23红包群_我的红包群_取消发普通红包接口
# # # 检查1个标签ID情况
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
Icase("I250_N21_C1","RtnOK","10002084",'"610","3101000000",varAutoMessage,"1","10","4","000000","","10002084"')
curWeb.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl23 = curWeb.fetchone()
connWeb.commit()
Icase("I250_N23_C1","RtnOK","10002084",'"10002084","610",%s,%s' % (tbl23[1],tbl23[0]))
Icase("I250_N23_C2","RtnDeviceErr","10002084",'"","610","3419","4512"')
Icase("I250_N23_C3","RtnParamErr","10002084",'"10002084","","3419","4512"')
Icase("I250_N23_C4","RtnParamErr","10002084",'"10002084","610","","4512"')
Icase("I250_N23_C5","RtnParamErr","10002084",'"10002084","610","3419",""')
Icase("I250_N23_C6","RtnDeviceErr","10002084","0002084","610","3419","4512"'')
Icase("I250_N23_C7","RtnParamErr","10002084",'"10002084","000","3419","4512"')
Icase("I250_N23_C8","RtnParamErr","10002084",'"10002084","610","00","4512"')
Icase("I250_N23_C9","RtnParamErr","10002084",'"10002084","610","3419","00"')

# print "24,================================================================================================="
# # #24红包群_我的红包群_发拼手气红包接口
Icase("I250_N24_C1","RtnOK","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084"')
Icase("I250_N24_C2","RtnParamErr","10002084",'"","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084",')
Icase("I250_N24_C3","RtnParamErr","10002084",'"610","","10002084发送拼手气红包1元","1","10","4","000000","","10002084",')
sleep(10)
Icase("I250_N24_C4","RtnOK","10002084",'"610","3101000000","","1","10","4","000000","","10002084"')
Icase("I250_N24_C5","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","","10","4","000000","","10002084"')
Icase("I250_N24_C6","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","","4","000000","","10002084"')
Icase("I250_N24_C7","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","","000000","","10002084"')
Icase("I250_N24_C8","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","","","10002084"')
Icase("I250_N24_C9","RtnDeviceErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","",""')
Icase("I250_N24_C10","RtnParamErr","10002084",'"000","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084"')
sleep(10)
Icase("I250_N24_C11","RtnOK","10002084",'"610","0000000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084"')
Icase("I250_N24_C12","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","0","10","4","000000","","10002084"')
Icase("I250_N24_C13","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","-1","10","4","000000","","10002084"')
# Icase("I250_N11_C","RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","0.01","10","4","000000","","10002084","C24-14,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #bug
Icase("I250_N24_C14","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","-1","4","000000","","10002084"')
Icase("I250_N24_C15","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","0","4","000000","","10002084"')
Icase("I250_N24_C16","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","0.001","4","000000","","10002084"')
Icase("I250_N24_C17","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","0.025","4","000000","","10002084"')
Icase("I250_N24_C18","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","0","000000","","10002084"')
Icase("I250_N24_C19","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","5","000000","","10002084"')
Icase("I250_N24_C20","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","-1","000000","","10002084"')
Icase("I250_N24_C21","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","0.1","000000","","10002084"')
Icase("I250_N24_C22","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","","0","10002084"')
Icase("I250_N24_C23","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","","-1","10002084"')
Icase("I250_N24_C24","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","","0.1","10002084"')
Icase("I250_N24_C25","RtnParamErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","","0000000","10002084"')
Icase("I250_N24_C26","RtnDeviceErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","",""')
Icase("I250_N24_C27","RtnDeviceErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","","000"')
Icase("I250_N24_C28","RtnDeviceErr","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","","-1"')

# print "25,================================================================================================="
# # # #25红包群_我的红包群_发拼手气红包设置标签接口(依赖24)
# # 业务逻辑:红包群中发送拼手气红包,点击塞钱进红包后选择标签发送红包,标签ID为0时代表所有群成员可见,多个标签ID以逗号分隔代表发送到多个标签下
# # 前提条件:红包群中存在标签,红包群的标签ID: SELECT id FROM t_redgroup_label WHERE groupId=610
# # 动态参数:接口24的返回值"batchId":批次ID,"channelId":渠道ID
# # 影响数据库:表t_redgroup_message,表t_redgroup_messamge_auth中各插入一条数据 ,表t_redgroup_memberinfo中对应标签下的非黑名单群成员的isMessage+1

Icase("I250_N24_C1","RtnOK","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084"')
curWeb.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl25 = curWeb.fetchone()
Icase("I250_N25_C1","RtnOK","10002084",'"10002084","610",%s,%s,"0"' % (tbl25[1],tbl25[0]))
# Icase("I250_N10_C","RtnOK","10002084",'"10002084","610","3426","4518","2611","C25-2,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
# Icase("I250_N10_C","RtnOK","10002084",'"10002084","610","3427","4519","2611,2382","C25-3,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
Icase("I250_N25_C2","RtnDeviceErr","10002084",'"","610","3412","4505","2611"')
Icase("I250_N25_C3","RtnParamErr","10002084",'"10002084","","3412","4505","2611"')
Icase("I250_N25_C4","RtnParamErr","10002084",'"10002084","610","","4505","2611"')
Icase("I250_N25_C5","RtnParamErr","10002084",'"10002084","610","3412","","2611"')
Icase("I250_N25_C6","RtnParamErr","10002084",'"10002084","610","3412","","2611"')
Icase("I250_N25_C7","RtnDeviceErr","10002084","0002084","610","3412","4505","2611"'')
Icase("I250_N25_C8","RtnParamErr","10002084",'"10002084","000","3412","4505","2611"')
Icase("I250_N25_C9","RtnParamErr","10002084",'"10002084","610","00","4505","2611"')
Icase("I250_N25_C10","RtnParamErr","10002084",'"10002084","610","3412","00","2611"')
Icase("I250_N25_C11","RtnParamErr","10002084",'"10002084","610","3412","4505","01"')

# print "26,================================================================================================="
# # #26红包群_我的红包群_取消发拼手气红包接口

Icase("I250_N24_C1","RtnOK","10002084",'"610","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084"')
curWeb.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl26 = curWeb.fetchone()
Icase("I250_N26_C1","RtnOK","10002084",'"10002084","610",%s,%s' % (tbl26[1],tbl26[0]))
Icase("I250_N26_C2","RtnDeviceErr","10002084",'"","610",%s,%s' % (tbl26[1],tbl26[0]))
Icase("I250_N26_C3","RtnParamErr","10002084",'"10002084","",%s,%s' % (tbl26[1],tbl26[0]))
Icase("I250_N26_C4","RtnParamErr","10002084",'"10002084","610","","4522"')
Icase("I250_N26_C5","RtnParamErr","10002084",'"10002084","610","3431",""')
Icase("I250_N26_C6","RtnDeviceErr","10002084",'"0002084","610","3431","4522"')
Icase("I250_N26_C7","RtnParamErr","10002084",'"10002084","000","3431","4522"')
Icase("I250_N26_C8","RtnParamErr","10002084",'"10002084","610","0.1","4522"')
Icase("I250_N26_C9","RtnParamErr","10002084",'"10002084","610","3431","00"')
#
#
##发普通红包接口
Icase("I250_N21_C1","RtnOK","10001588",'"118","3101000000","红包标题","5","0.5","4","111111","","10001588"')
##发普通红包设置标签接口
curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data1 = curWeb.fetchone()
curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data2 = curWeb.fetchone()
connWeb.commit()
Icase("I250_N22_C1","RtnOK","10001588",'"10001588","118",data1[0],data2[0],"0"')

##发拼手气红包接口
Icase("I250_N24_C1","RtnOK","10001588",'"118","3101000000","红包标题","5","2.5","4","111111","","10001588"')

##发拼手气红包设置标签接口
curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
tbl26 = curWeb.fetchone()
curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
tbl26 = curWeb.fetchone()
connWeb.commit()
sleep(10)  #########################################整体后需要放开#############################################################
Icase("I250_N25_C1","RtnOK","10001588",'"10001588","118",%s,%s,"0"' % (tbl26[0],tbl26[0]))
#
# print "27,================================================================================================="
# #27红包群_我关注的红包群_抢普通红包接口
curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32  ORDER BY id DESC LIMIT 0,1')
tbl27_1 = curWeb.fetchone()
curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
tbl27_2 = curWeb.fetchone()
curWeb.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(tbl27_1[0]))
tbl27_3 = curWeb.fetchone()
connWeb.commit()

Icase("I250_N27_C1","RtnOK","10001801",'"10001801",data3,"118",%s,%s' % (tbl27_1[0],tbl27_2[0]))

curWeb.execute('SELECT count(id),id from ukardweb.t_external_redDetail WHERE belongId=10001801 and redState=3 and redType=32 and batchId=%s' %(data1[0]))
tbl27_4 = curWeb.fetchone()
connWeb.commit()
if tbl27_4[0]==1:print "  => [Ok,t_external_redDetail数据库记录新增1条成功并且10001801领取成功,C27-1]"
else:print "  => [errorrrrrrrrrr,t_external_redDetail数据库记录新增1条失败且领取失败,C27-1]"
Icase("I250_N27_C2","RtnParamErr","10001801",'"",tbl27_3[0],"118",tbl27_1[0],tbl27_2[0], "C27-2,userId(空),messageId,groupId,batchId,channelId")
Icase("I250_N27_C3","RtnParamErr","10001801",'"10001801","","118",tbl27_1[0],tbl27_2[0], "C27-3,userId,messageId（空),groupId,batchId,channelId")
Icase("I250_N27_C4","RtnParamErr","10001801",'"10001801",tbl27_3[0],"118",'',tbl27_2[0], "C27-4,userId,messageId,groupId,batchId(空),channelId")
Icase("I250_N27_C5","RtnParamErr","10001801",'"10001801",tbl27_3[0],"118",tbl27_1[0],'', "C27-5,userId,messageId,groupId,batchId,channelId(空)")
Icase("I250_N27_C6","RtnDeviceErr","",'"",%s,"118",%s,%stbl27_3[0],"118",tbl27_1[0],tbl27_2[0], "C27-6,userId（空）,messageId,groupId,batchId,channelId(空)")
#黑名单用户
Icase("I250_N27_C7","RtnOK","10001813",'"10001813",%s,%s,%s,"118"' % (tbl27_3[0],tbl27_1[0],tbl27_2[0]))
# print "28,================================================================================================="
# # 28红包群_我关注的红包群_抢拼手气红包接口
# #调用一下
# Icase("I250_N10_C","RtnOK","10001588","118","3101000000","红包标题","5","2.5","4","111111","","10001588", "C24-1,userId,groupId,cityId,brandContent,redNumber,amount,payType")
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
# data2 = curWeb.fetchone()
# conn.commit()
# sleep(10)  #########################################整体后需要放开#############################################################
# Icase("I250_N10_C","RtnOK","10001588","10001588","118",data1,data2,"0","C25-1,userId,groupId,batchId,channelId,labelId")
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
# data2 = curWeb.fetchone()
# curWeb.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
# data3 = curWeb.fetchone()
# Icase("I250_N10_C","RtnOK","10001801","10001801",data3,"118",data1,data2, "C28-1,userId,messageId,groupId,batchId,channelId")
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT count(id),id from ukardweb.t_external_redDetail WHERE belongId=10001801 and redState=3 and redType=33 and batchId=%s' %(data1[0]))
# data4 = curWeb.fetchone()
# if data4[0]==1:print "  => [Ok,t_external_redDetail数据库记录新增1条成功并且10001801领取成功,C28-1]"
# else:print "  => [errorrrrrrrrrr,t_external_redDetail数据库记录新增1条失败且领取失败,C28-1]"
# Icase("I250_N11_C","RtnParamErr","10001801","",data3,"118",data1,data2, "C28-2,userId(空),messageId,groupId,batchId,channelId")
# Icase("I250_N11_C","RtnParamErr","10001801","10001801","","118",data1,data2, "C28-3,userId,messageId（空),groupId,batchId,channelId")
# Icase("I250_N11_C","RtnParamErr","10001801","10001801",data3,"118",'',data2, "C28-4,userId,messageId,groupId,batchId(空),channelId")
# Icase("I250_N11_C","RtnParamErr","10001801","10001801",data3,"118",data1,'', "C28-5,userId,messageId,groupId,batchId,channelId(空)")
# Icase("I250_N12_C1","RtnDeviceErr","","",data3,"118",data1,data2, "C28-6,userId（空）,messageId,groupId,batchId,channelId(空)")
# #黑名单用户
# Icase("I250_N10_C","RtnOK","10001813","10001813",data3,"118",data1,data2, "C28-7,userId,messageId,groupId,batchId,channelId")
#
# print "29,================================================================================================="
# ##新用户没有模版就需要调用一下，老用户有模版就不需要
# Icase("I250_N10_C","RtnOK","10001588","10001588","1","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com",""',"C12-1,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
# #33发红包_广告红包发送接口,#连续执行会提示重复提交
# Icase("I250_N10_C","RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
#
# #29红包群_我关注的红包群_抢广告红包接口
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
# data2 = curWeb.fetchone()
# Icase("I250_N10_C","RtnOK", "10001877", "10001877","123", "118", data1, data2,"C29-1,userId,messageId,groupId,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "","123", "118", data1, data2,"C29-2,userId(空),messageId(groupId,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","123", "", data1, data2,"C29-3,userId,messageId,groupId（空）,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","123", "118", "", data2,"C29-4,userId,messageId,groupId,batchId(空),channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","123", "118", data1, "","C29-5,userId,messageId,groupId,batchId,channelId（空）,")
# print "30,================================================================================================="
# #30红包群_我关注的红包群_领取广告红包消息接口
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
# data2 = curWeb.fetchone()
# Icase("I250_N10_C","RtnOK", "10001877", "10001877","118", data1, data2,"C30-1,userId,groupId,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "","118", data1, data2,"C30-2,userId,groupId,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","", data1, data2,"C30-3,userId,groupId（空）,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","119", "", data2,"C30-4,userId,groupId,batchId(空),channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","119", data1, "","C30-5,userId,groupId,batchId,channelId(空),")
# print "31,================================================================================================="
# #31红包群_我关注的红包群_抢广告红包回调接口
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
# data2 = curWeb.fetchone()
# Icase("I250_N10_C","RtnOK", "10001877", "10001877","118",data1[0],data2[0],"C31-1,userId,groupId,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "","118",data1[0],data2[0],"C31-2,userId（空）,groupId,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","",data1[0],data2[0],"C31-3,userId,groupId（空）,batchId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","",data1[0],data2[0],"C31-4,userId,groupId,batchId（空）,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","118","",data2[0],"C31-5,userId,groupId,batchId（空）,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","118",data1[0],"" ,"C31-6,userId,groupId,batchId,channelId（空）,")
# print "32,================================================================================================="
# #32红包群_我关注的红包群_查看是否还有可抢红包接口
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
# data2 = curWeb.fetchone()
# Icase("I250_N10_C","RtnOK", "10001877", "10001877",data2[0],"C32-1,userId,channelId,")
# Icase("I250_N11_C","RtnParamErr", "10001877", "10001877","","C32-2,userId,channelId(空),")
#
# print "33,================================================================================================="
# #33发红包_广告红包发送接口
# Icase("I250_N10_C","RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
# #连续执行会提示重复提交
# sleep(5)
# Icase("I250_N11_C","RtnParamErr","10001588","10001588","1","100000","0.01","1","0","3101000000","0","31","111111","0","C33-2,userId,amount,count(错误),payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
# sleep(5)
# Icase("I250_N12_C1","RtnDeviceErr","10001588","","1","1","0.01","1","0","3101000000","0","31","111111","0","C33-3,userId（空）,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
# sleep(5)
# Icase("I250_N11_C","RtnParamErr","10001588","10001588","","1","3","1","0","3101000000","0","31","111111","0","C33-4,userId,amount（空）,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
# sleep(5)
# Icase("I250_N11_C","RtnParamErr","10001588","10001588","1","-1","3","1","0","3101000000","0","31","111111","0","C33-5,userId,amount,count（负数）,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
# sleep(5)
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "2", "3", "100", "3101000000", "0", "31", "111111", "0","C33-6,userId,amount,count,payType（错不在数据类型范围内）,door,cityId,groupId,templateId,payPwd,redPoolId,")
# sleep(5)
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "", "111111", "0","C33-7,userId,amount,count,payType,door,cityId,groupId,templateId（空）,payPwd,redPoolId,")
# sleep(5)
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31", "", "0","C33-8,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（空）,redPoolId,")
# sleep(5)
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31", "", "0","C33-9,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（错）,redPoolId,")
# sleep(5)
# Icase("I250_N10_C","RtnOK", "10001588", "10001588", "1", "2", "3", "2", "0", "3101000000", "0", "31", "111111", "3452","C33-10,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（错）,redPoolId,")
#
# print "34,================================================================================================="
# #34发红包_微信支付用户回调接口  ##################该接口正常业务无法正常测试####################
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT pay_order_id  from ukardweb.t_user_withdraw WHERE user_id=10001588 and object_id=%s' %(data1[0]))
# data2 = curWeb.fetchone()
# #首先要发红包微信支付
# sleep(10)
# Icase("I250_N10_C","RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId")
#
# # Icase("I250_N11_C","RtnParamErr", "10001588", "10001588",data1[0],data2[0],"C34-1,userId,redPoolId,payOrderId")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","","","C34-2,userId,redPoolId,payOrderId(空)")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","",data2[0],"C34-3,userId,redPoolId(空),payOrderId")
# print "35,================================================================================================="
# #35发红包_红包充值接口
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# conn.commit()
# Icase("I250_N10_C","RtnOK", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-1,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# # #本人应无法给别人红包充值已修复
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", "3680", "111111","C35-2,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# Icase("I250_N11_C","RtnParamErr", "10001588", "", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-3,userId（空）,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId（别人的红包批次）,payPwd,")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-4,userId,amount（空）,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "-1", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-5,userId,amount,count（负数）,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-6,userId,amount,count,payType（空）,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", "", "111111","C35-7,userId,amount,count,payType（空）,door,cityId,groupId,templateId,qrFlag,redPoolId（空）,payPwd,")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "","C35-8,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd(错),")
# print "36,================================================================================================="
# #36红包列表_红包放入红包池、余额回收接口
# #先生成一个广告红包做铺垫怕影响到别的接口
# sleep(10)
# Icase("I250_N10_C","RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,推广来源,红包总金额,渠道推广图片ID,userid,品牌商户名称,红包总数量,door")
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# #回收余额需要先修改红包主表updateTime
# curWeb.execute('UPDATE t_extension_channel_redPool set updateTime=ADDDATE(NOW(),2) WHERE id=%s'%(data1[0]))
# conn.commit()
# #激活同城红包
# I25_44("I250_N10_C","RtnOK", "10001588","C44-1")
# #放入红包池目前不用测试了，下个版本没有了
# Icase("I250_N10_C","RtnOK", "10001588", "10001588","2",data1[0],"34","C36-1,userId,callBackType,redPoolId,redType")
# Icase("I250_N11_C","RtnParamErr", "10001588", "","2",data1[0],"34","C36-2,userId(空),callBackType,redPoolId,redType")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","",data1[0],"34","C36-2,userId,callBackType（空）,redPoolId,redType")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","9",data1[0],"34","C36-2,userId,callBackType（不在回收范围内的类型）,redPoolId,redType")
# ########别人的批次的ID问题以修复
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","2","3485","34","C36-2,userId,callBackType,redPoolId（别人的批次ID）,redType")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","2","","34","C36-2,userId,callBackType,redPoolId(空),redType")
# Icase("I250_N10_C","RtnOK", "10001588", "10001588","2",data1[0],"33","C36-2,userId,callBackType,redPoolId,redType（不匹配用户批次的类型）")
# print "37,================================================================================================="
# #37我的_个人信息接口（新增返回值）
# Icase("I250_N10_C","RtnOK", "10001588", "10001588","10001877","1","C37-1,userId,visitUserId,isGroup")
# Icase("I250_N10_C","RtnOK", "10001588", "10001588","10001877","0","C37-2,userId,visitUserId,isGroup")
# Icase("I250_N11_C","RtnParamErr", "10001588", "","10001877","0","C37-3,userId（空）,visitUserId,isGroup")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","","0","C37-4,userId,visitUserId（空）,isGroup")
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588","10001877","","C37-5,userId,visitUserId,isGroup（空）")
# print "38,================================================================================================="
# #38首页_发红包_私信红包_发送私信红包接口
# Icase("I250_N10_C","RtnOK", "10001588", "10001588", "3", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-1,userId,payType,amount,""acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N12_C1","RtnDeviceErr", "10001588", "", "3", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-2,userId（空）,payType,amount,""acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-3,userId,payType（空）,amount,""acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-4,userId,payType,amount（空）,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "-1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-5,userId,payType,amount（负数）,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "118", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-6,userId,payType,amount,acceptId（不是群成员）,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-7,userId,payType,amount,acceptId,groupId（空）,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "119", "10001588给10001588发送私信红包1", "111111", "",
#        "C38-8,userId,payType,amount,acceptId,groupId（不匹配的群ID）,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "119", "10001588给10001588发送私信红包1", "", "",
#        "C38-9,userId,payType,amount,acceptId,groupId,content,payPwd(空),templateId ")
# print "39,================================================================================================="
# #39发送私信转帐接口
# Icase("I250_N10_C","RtnOK","10001588","10001588","3","1","10001877","118","10001588给10001877发送私信转账1元","111111",
#        "C39-1,userId,payType,amount,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N12_C1","RtnDeviceErr", "10001588", "", "3", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
#        "C39-1,userId（空）,payType,amount,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
#        "C39-1,userId,payType（空）,amount,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
#        "C39-1,userId,payType,amount（空）,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "-1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
#        "C39-1,userId,payType,amount（负数）,acceptId,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "1", "10001588", "118", "10001588给10001588发送私信转账1元", "111111",
#        "C39-1,userId,payType,amount,acceptId（不是群成员的成员）,groupId,content,payPwd,templateId ")
#
# Icase("I250_N11_C","RtnParamErr", "10001588", "10001588", "3", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "",
#        "C39-1,userId,payType,amount,acceptId,groupId,content,payPwd（错误）,templateId ")
# print "40,================================================================================================="
# #40分享红包_获取分享链接接口
# sleep(10)
# Icase("I250_N10_C","RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
# conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
# curWeb = conn.cursor()
# curWeb.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
# data1 = curWeb.fetchone()
# curWeb.execute('SELECT pay_order_id  from ukardweb.t_user_withdraw WHERE user_id=10001588 and object_id=%s' %(data1[0]))
# data2 = curWeb.fetchone()
# conn.commit()
# Icase("I250_N10_C","RtnOK", "10001588", "10001588", "20", "7", "1", data1[0],"2" ,data2[0], "1","0",
#        "C40-1,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds")
#
# Icase("I250_N10_C","RtnOK", "10001588", "10001588", "25", "7", "1", data1[0], "2", data2[0], "1", "0",
#        "C40-2,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", data2[0], "1", "0",
#        "C40-3,userId,shareType（不在范围内的类型）,platform,amount,tranId,channel,channelId,lvl,labelIds")
#
#
# Icase("RtnParamErr1", "10001588", "10001588", "60", "70", "1", data1[0], "2", data2[0], "1", "0",
#        "C40-4,userId,shareType,platform（不在分享渠道内）,amount,tranId,channel,channelId,lvl,labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "", data1[0], "2", data2[0], "1", "0",
#        "C40-5,userId,shareType,platform,amount（空）,tranId,channel,channelId,lvl,labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "-1", data1[0], "2", data2[0], "1", "0",
#        "C40-6,userId,shareType,platform,amount（负数）,tranId,channel,channelId,lvl,labelIds")
#
# Icase("I250_N10_C","RtnOK", "10001588", "10001588", "20", "7", "1", "3547", "2", data2[0], "1", "0",
#        "C40-4,userId,shareType,platform,amount,tranId（不是自己的批次）,channel,channelId,lvl,labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "", data2[0], "1", "0",
#        "C40-7,userId,shareType,platform,amount,tranId,channel（空）,channelId,lvl,labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "1", "0",
#        "C40-8,userId,shareType,platform,amount,tranId,channel,channelId(不是自己的渠道ID),lvl,labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "3", "0",
#        "C40-9,userId,shareType,platform,amount,tranId,channel,channelId,lvl(超过层级范围),labelIds")
#
# Icase("I250_N12_C1","RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "3", "",
#        "C40-10,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds（空）")
# print "41,================================================================================================="
# # 41,首页_红包群_我的红包群_私信红包领取信息接口
# Icase("I250_N10_C","RtnOK","10002084","2","C41-1,redId")
# print "42,================================================================================================="
# # 42,红包群_我的红包群_新成员数量接口
# Icase("I250_N10_C","RtnOK","10001679","213","C42-1,groupId")
# print "43,================================================================================================="
# #43,批处理_分享至红包池_同城红包生成批处理接口
# Icase("I250_N10_C","RtnOK","10001679","C43-1")
# print "44,================================================================================================="
# # 44,批处理_广告红包分成_同城红包生成批处理接口
# Icase("I250_N10_C","RtnOK","10001588","C44-1")