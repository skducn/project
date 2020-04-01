# coding: utf-8
#****************************************************************
# Author     : John
# Version    : V 2.5.1
# Date       : 2016-8.18
# Description: 三藏红包 2.5.1 app接口文档 1-32
#****************************************************************

import sys,requests,redis,MySQLdb,random,datetime,time
import smtplib,pytesseract
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep

# 1,资质认证_资质认证首页
# 2,城市列表接口
# 3,资质认证_保存、修改个人认证接口
# 4,资质认证_个人认证信息查询接口"
# 5,资质认证_保存、修改店铺认证接口
# 6,资质认证_商户认证信息查询接口


def Icommon3(param1,param2):
    # Icommon3 ,获取验证码接口
    # 参数: type=1 获取登录验证码 , 2 提现验证码 , 4=设置提现密码  ;mobileNum=手机号
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
    querystring = {"type":param1,"mobileNum":param2}
    headers = {'cache-control': "no-cache"}
    requests.request("GET", varUrl, headers=headers, params=querystring)
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    ########################################################################
    #"Icommon3,获取验证码接口"
    if param1=="1":
        varVerifyCode = r.get("app_login_" + str(param2))
        print param2 +" 验证码: " + varVerifyCode
        return varVerifyCode
    elif param1 =="4":
        varVerifyCode = r.get("app_withdrawCode_" + str(param2))
        print param2 +" 验证码: " + varVerifyCode
        return varVerifyCode
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


def I251_1(varnum,varuserId,param1,testcase):
    # 参数: gorupId
    varInterfaceName = "I251_1,资质认证_资质认证首页"
    varUrl = "http://192.168.2.176:9999/WebBusi/certification/2.5/getCertificationList.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,groupId=param1)

def I251_2(varnum,varuserId,param1,testcase):
    # 参数: parentId =省市编码，获得省份列表传空
    varInterfaceName = "I251_2,城市列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/certification/2.5/getDictRegion.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,parentId=param1)

def I25_3(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,testcase):
    # 参数: userId ,groupId ,userName ,cardNo ,picUrl,phone,id,mobileCode
    varInterfaceName = "I251_3,资质认证_保存、修改个人认证接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/certification/2.5/savePersonCertificationInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,userName=param3,cardNo=param4,picUrl=param5,phone=param6,id=param7,mobileCode=param8)

def I25_4(varnum,varuserId,param1,param2,testcase):
    # 参数: userId,groupId
    varInterfaceName = "I251_4,资质认证_个人认证信息查询接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/certification/2.5/getPersonCertificationInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2)

def I25_5(varnum,varuserId,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,testcase):
    # 参数: userId,groupId,certificationId,companyName,storeName,province,city,area,address,coordGps,coordBd,phone,businessTime,storeType,picUrl,webPlatform,storeLink,id,type,mobileCode
    varInterfaceName = "I251_5,资质认证_保存、修改店铺认证接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/certification/2.5/saveStoreCertificationInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=p1,groupId=p2,certificationId=p3,companyName=p4,storeName=p5,province=p6,city=p7,area=p8,address=p9,coordGps=p10,coordBd=p11,phone=p12,businessTime=p13,storeType=p14,picUrl=p15,webPlatform=p16,storeLink=p17,id=p18,type=p19,mobileCode=p20)

def I25_6(varnum,varuserId,p1,p2,p3,testcase):
    # 参数: userId,groupId,type
    varInterfaceName = "I251_6,资质认证_商户认证信息查询接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/certification/2.5/getStoreCertificationInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=p1,groupId=p2,type=p3)

def I25_7(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: verifyUserId = 验证用户ID, phone = 手机号, curPwd=当前密码 ,mobileCode= 验证码
    varInterfaceName = "I25_7,我_设置_提现密码_保存提现密码接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/withdraw/2.5/save_withdraw_pwd.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,phone=param2,curPwd=param3,mobileCode=param4)
def I25_8(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: verifyUserId = 验证用户ID, oldPwd = 原始密码, curPwd=当前密码
    varInterfaceName = "I25_8,我_设置_提现密码_修改提现密码接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/withdraw/2.5/update_withdraw_pwd.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,oldPwd=param2,curPwd=param3)

def I25_9(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId = 用户ID, groupId= 群ID, startIndex=分页开始位置 ,pageSize=每页显示条数
    varInterfaceName = "I25_9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupSta/2.2/user_redAdvert_statistics.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,startIndex=param3,pageSize=param4)
def I25_10(varnum,varuserId,param1,param2,testcase):
    # 参数: userId , templateType=模版类型
    varInterfaceName = "I25_10,红包模板_红包类型列表"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/getRedPacketTypeList.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,templateType=param2)
def I25_11(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId = 用户ID, templateType= 模板, startIndex=分页开始位置 ,pageSize=每页显示条数
    varInterfaceName = "I25_11,红包模板_红包模板列表"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/getTemplateList.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,templateType=param2,startIndex=param3,pageSize=param4)

def I25_12(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,testcase):
    # 参数: userId = 用户ID, templateType= 模板, title=标题,brandContent=品牌,extensionSub=推广内容,extensionUrl=推广链接,videoUrl=视频链接,picFlag=添加图文标记,picUrls=图片链接（逗号表达式）,
    # templateId=模板id（没有修改，不需要传递）
    varInterfaceName = "I25_12,红包模板_保存红包模板"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/saveTemplateInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,templateType=param2,title=param3,brandContent=param4,extensionSub=param5,extensionUrl=param6,videoUrl=param7,picFlag=param8,picUrls=param9,templateId=param10)

def I25_13(varnum,varuserId,param1,param2,testcase):
    # 参数: userId = 用户ID, templateId = 模版ID
    varInterfaceName = "I25_13,红包模板_删除红包模板"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/delTemplateInfo.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,templateId=param2)
def I25_14(varnum,varuserId,param1,param2,param3,param4,param5,param6,testcase):
    # 参数: userID = 用户ID, groupId= 群ID, startIndex=分页开始位置 ,pageSize=每页显示条数 ,acceptId=收件人ID ,isGroup=是否为群主(0:否,1:是)
    varInterfaceName = "I25_14,首页_红包群_我的红包群私信详情接口(新增返回值)"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivate/2.2/user_private_detail.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,startIndex=param3,pagesize=param4,acceptId=param5,isGroup=param6)
def I25_15(varnum,varuserId,param1,param2,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName = "I25_15,首页_红包群_我的红包群_领私信转账接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_lead_transfer.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,redId=param2)
def I25_16(varnum,varuserId,param1,param2,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    ########################################################################
    varInterfaceName = "I25_16,首页_红包群_我的红包群_转账详情接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_transfer_detail.do"


    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,redId=param2)
def I25_17(varnum,varuserId,param1,param2,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    varInterfaceName =  "I25_17,私首页_红包群_我的红包群_重新发送私信转账接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_transfer_resend.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,redId=param2)
def I25_18(varnum,varuserId,param1,param2,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    varInterfaceName =  "I25_18,首页_红包群_我的红包群_私信转账退回接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_transfer_return.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,redId=param2)
def I25_19(varnum,varuserId,param1,param2,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    varInterfaceName =  "I25_19,首页_红包群_我的红包群_领私信红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_lead_red.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,redId=param2)
def I25_20(varnum,varuserId,param1,param2,testcase):
    # 参数: verifyUserId = 验权用户ID ,redId =红包ID
    varInterfaceName =  "I25_20,首页_红包群_我的红包群_私信红包详情接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_red_detail.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,redId=param2)
def I25_21(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    # 参数: groupId = 群id, cityId=城市ID, brandContent= 标题 , redNumber = 红包个数 ,redAmount=红包单个金额(单位:元),
    # payType=支付类型(1 微信，2 支付宝，3 余额),payPwd=支付密码（可选）, payType=3时，(必选),templateId=模板ID（可选）,userId = 用户ID
    varInterfaceName =  "I25_21,红包群_我的红包群_发普通红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,groupId=param1,cityId=param2,brandContent=param3,redNumber=param4,amount=param5,payType=param6,payPwd=param7,templateId=param8,userId=param9)
def I25_22(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    varInterfaceName =  "I25_22,红包群_我的红包群_发普通红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed_auth.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4,labelId=param5)
def I25_23(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    varInterfaceName =  "I25_23,红包群_我的红包群_取消发普通红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/cancel_send_commonRed.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4)
def I25_24(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    # 参数: groupId = 群id, cityId=城市ID, brandContent= 标题 , redNumber = 红包个数 ,amount=红包总金额(单位:元),
    # payType=支付类型(1 微信，2 支付宝，3 余额),payPwd=支付密码（可选）, payType=3时，(必选),templateId=模板ID（可选）
    varInterfaceName =  "I25_24,红包群_我的红包群_发拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuckRed.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,groupId=param1,cityId=param2,brandContent=param3,redNumber=param4,amount=param5,payType=param6,payPwd=param7,templateId=param8,userId=param9)
def I25_25000(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    # 参数: userId , groupId , batchId ,channelId   ,labelId=标签ID,多个以逗号分隔
    varInterfaceName =  "I25_25,红包群_我的红包群_发拼手气红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuck_auth.do"

    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4,labelId=param5)
def I25_26(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId , groupId , batchId ,channelId
    varInterfaceName = "I25_26,红包群_我的红包群_取消发拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/cancel_fightLuckRed.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4)

def I25_38000(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,testcase):
    varInterfaceName =  "I25_38,首页_发红包_私信红包_发送私信红包接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_red.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,payType=param2,amount=param3,acceptId=param4,groupId=param5,content=param6,payPwd=param7,templateId=param8)
def I25_39000(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,testcase):
    # 参数: userId=用户Id , payType=支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , amount=红包金额 ,acceptId=收红包用户ID ,
    # groupId=群ID ,content=信息内容(可选) ,payPwd=支付密码(可选,支付类型3、5必传)    ########################################################################
    varInterfaceName =  "I25_39,首页_发红包_私信红包_发送私信转账接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_transfer.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,payType=param2,amount=param3,acceptId=param4,groupId=param5,content=param6,payPwd=param7)

#如果是新用户没有模版就需要调用保存模版接口
def I25_120000(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,testcase):
    # 参数: userId = 用户ID, templateType= 模板, title=标题,brandContent=品牌,extensionSub=推广内容,extensionUrl=推广链接,videoUrl=视频链接,picFlag=添加图文标记,picUrls=图片链接（逗号表达式）,
    # templateId=模板id（没有修改，不需要传递）
    varInterfaceName = "I25_12,红包模板_保存红包模板"
    varUrl = "http://192.168.2.176:9999/payment/template/2.5/saveTemplateInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,templateType=param2,title=param3,brandContent=param4,extensionSub=param5,extensionUrl=param6,videoUrl=param7,picFlag=param8,picUrls=param9,templateId=param10)
#发普通红包接口
def I25_21000(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    # 参数: groupId = 群id, cityId=城市ID, brandContent= 标题 , redNumber = 红包个数 ,redAmount=红包单个金额(单位:元),
    # payType=支付类型(1 微信，2 支付宝，3 余额),payPwd=支付密码（可选）, payType=3时，(必选),templateId=模板ID（可选）,userId = 用户ID
    varInterfaceName =  "I25_21,红包群_我的红包群_发普通红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,groupId=param1,cityId=param2,brandContent=param3,redNumber=param4,amount=param5,payType=param6,payPwd=param7,templateId=param8,userId=param9)
#发普通红包设置标签接口
def I25_22000(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    ########################################################################
    varInterfaceName =  "I25_22,红包群_我的红包群_发普通红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payCommonRed/2.5/send_commonRed_auth.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"groupId":param2,"batchId":param3
        ,"channelId":param4,"labelId":param5}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']==True:

                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
#发拼手气红包接口
def I25_24000(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    # 参数: groupId = 群id, cityId=城市ID, brandContent= 标题 , redNumber = 红包个数 ,amount=红包总金额(单位:元),
    # payType=支付类型(1 微信，2 支付宝，3 余额),payPwd=支付密码（可选）, payType=3时，(必选),templateId=模板ID（可选）
    varInterfaceName =  "I25_24,红包群_我的红包群_发拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuckRed.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,groupId=param1,cityId=param2,brandContent=param3,redNumber=param4,amount=param5,payType=param6,payPwd=param7,templateId=param8,userId=param9)
#发拼手气红包设置标签接口
def I25_25(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:
    ########################################################################
    varInterfaceName ="I25_25,红包群_我的红包群_发拼手气红包设置标签接口"
    varUrl = "http://192.168.2.176:9999/payment/payFightLuckRed/2.5/send_fightLuck_auth.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "groupId": param2,
                   "batchId": param3, "channelId": param4, "labelId": param5}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK" :
            if response.json()['success']==True:

                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr" :
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr" :
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnDeviceErr":
            if response.json()['errorcode'] == 100003 and response.json()['success'] == False:
                print "[OK,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnDeviceErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"

def I25_27(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0,password="dlhy123456")
    varverifyCode = r.hget("app:verify:"+varuserId,"code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，messageId = 消息ID，groupId = 群Id，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName =  "I25_27,红包群_我关注的红包群_抢普通红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robCommonRed/2.5/rob_commonRed.do"
    querystring = {"verifyUserId":varuserId,"verifyCode":varverifyCode,"userId":param1,"messageId":param2,"groupId":param3
        ,"batchId":param4,"channelId":param5}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum=="RtnOK":
            if response.json()['success']==True:
                print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnSysErr":
            if response.json()['errorcode']==100001 and response.json()['success']== False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum=="RtnParamErr":
            if response.json()['errorcode']==100002 and response.json()['success']== False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception,data:
        print Exception,":",data,"\n"
def I25_28(varnum, varuserId, param1, param2, param3, param4, param5, testcase):
    r = redis.StrictRedis(host='192.168.2.176', port=6379, db=0, password="dlhy123456")
    varverifyCode = r.hget("app:verify:" + varuserId, "code")
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，messageId = 消息ID，groupId = 群Id，batchId = 批次ID，channelId = 批次ID
    ########################################################################
    varInterfaceName = "I25_28,红包群_我关注的红包群_抢拼手气红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robFightLuckRed/2.5/rob_fightLuck_Red.do"
    querystring = {"verifyUserId": varuserId, "verifyCode": varverifyCode, "userId": param1, "messageId": param2,
                   "groupId": param3, "batchId": param4, "channelId": param5}
    ########################################################################
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", varUrl, headers=headers, params=querystring)
    try:
        if varnum == "RtnOK":
            if response.json()['success'] == True:print "[OK,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content
                sendemail(varInterfaceName,"[errorrrrrrrrrr,RtnOK]," + varInterfaceName + " => " + testcase + " => " + response.content)
        if varnum == "RtnSysErr":
            if response.json()['errorcode'] == 100001 and response.json()['success'] == False:
                print "[OK,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnSysErr]," + varInterfaceName + " => " + testcase + " => " + response.content
        if varnum == "RtnParamErr":
            if response.json()['errorcode'] == 100002 and response.json()['success'] == False:
                print "[OK,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content
            else:
                print "[errorrrrrrrrrr,RtnParamErr]," + varInterfaceName + " => " + testcase + " => " + response.content

    except Exception, data:
        print Exception, ":", data, "\n"
def I25_29(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，messageId = 消息ID，groupId = 群Id，batchId = 批次ID，channelId = 批次ID
    varInterfaceName = "I25_29,红包群_我关注的红包群_抢广告红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/rob_advertRed.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,messageId=param2,groupId=param3,batchId=param4,channelId=param5)
def I25_30(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数:userId = 用户Id，groupId = 群ID，batchId = 批次ID，channelId = 批次ID
    varInterfaceName = "I25_30,红包群_我关注的红包群_领取广告红包消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/redGroup_robRed_receive.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4)
def I25_31(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId = 用户Id，groupId = 群ID，batchId = 批次ID，channelId = 批次ID
    varInterfaceName = "I25_31,红包群_我关注的红包群_抢广告红包回调接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/redGroup_robRed_callback.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4)
def I25_32(varnum,varuserId,param1,param2,testcase):
    # 参数: userId = 用户Id，channelId = 批次ID
    varInterfaceName = "I25_32,红包群_我关注的红包群_查看是否还有可抢红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robFightLuckRed/2.5/is_red.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,channelId=param2)
def I25_33(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11,testcase):
    # 参数:
    # userId = 用户Id(必填)
    # amount = 红包总金额（元）(必填)
    # count＝红包数量(必填)
    # payType ＝ 支付类型
    # door =   1首页进入 2红包再发一次
    # type ＝ 资金类型
    # cityId ＝ 城市编码
    # groupId ＝ 群id(必填)
    # templateId ＝ 模板id(必填)
    ########################################################################
    varInterfaceName =  "I25_33,发红包_广告红包发送接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeGetOrderNew.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,amount=param2,count=param3,payType=param4,door=param5,type=param6,cityId=param7,groupId=param8,templateId=param9,payPwd=param10,redPoolId=param11)

def I25_34(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: userId = 用户Id，redPoolId = 红包批次id，payOrderId = 订单编号
    ########################################################################
    varInterfaceName = "I25_34，发红包_微信支付用户回调接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeOrderReturnNew.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,redPoolId=param2,payOrderId=param3)
def I25_35(varnum,varuserId,param1,param2,param3,param4, param5, param6, param7, param8, param9, param10,param11,param12, testcase):
    # 参数: userId = 用户Id，amount = 红包总金额，count = 红包数量，payType = 支付类型，door = 入口标记，
    # type = 资金类型，cityId = 城市编码，groupId = 群id，templateId = 模板id，qrFlag = 是否是二维码充值，redPoolId = 批次id，payPwd = 支付密码
    varInterfaceName = "I25_35,发红包_红包充值接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/advertApprentice.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,amount=param2,count=param3,payType=param4,door=param5,type=param6,cityId=param7,groupId=param8,templateId=param9,qrFlag=param10,redPoolId=param11,payPwd=param12)
def I25_36(varnum, varuserId, param1, param2, param3, param4, testcase):
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，callBackType = 回收类型，redPoolId = 批次号，redType = 红包类型
    varInterfaceName = "I25_36,红包列表_红包放入红包池、余额回收接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/redpackCallBack.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, callBackType=param2, redPoolId=param3,redType=param4)
def I25_37(varnum, varuserId, param1, param2, param3, testcase):
    varInterfaceName = "I25_37,我的_个人信息接口（新增返回值）"
    varUrl = "http://192.168.2.176:9999/WebBusi/personalHomePage/2.2/homePage_info.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, visitUserId=param2,isGroup=param3)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，visitUserId = 访问人id，isGroup = 是否群主，1是，0否
def I25_38(varnum, varuserId, param1, param2, param3, param4, param5, param6, param7, param8, testcase):
    varInterfaceName = "I25_38,首页_发红包_私信红包_发送私信红包接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_red.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, payType=param2, amount=param3,acceptId=param4, groupId=param5,
             content=param6, payPwd=param7, templateId=param8)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，payType = 支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡)，amount = 红包金额，
    # acceptId = 红包金额，groupId=群ID，content=信息内容(可选)，payPwd=付密码(可选,支付类型3、5必传)，templateId =模板ID(可选)
def I25_39(varnum, varuserId, param1, param2, param3, param4, param5, param6, param7, testcase):
    varInterfaceName = "I25_39,首页_发红包_私信红包_发送私信转帐接口"
    varUrl = "http://192.168.2.176:9999/payment/privateOrder/2.5/save_user_private_transfer.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase, userId=param1, payType=param2, amount=param3,
             acceptId=param4, groupId=param5,content=param6, payPwd=param7)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，payType = 支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡)，amount = 红包金额，
    # acceptId = 红包金额，groupId=群ID，content=信息内容(可选)，payPwd=付密码(可选,支付类型3、5必传)
def I25_40(varnum, varuserId, param1, param2, param3, param4, param5, param6, param7,param8,param9, testcase):
    varInterfaceName = "I25_40,分享红包_获取分享链接接口"
    varUrl = "http://192.168.2.176:9999/payment/share/1.0/get_share_url.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase,userId=param1,shareType=param2,platform=param3,
             amount=param4,tranId=param5,channel=param6,channelId=param7,lvl=param8,labelIds=param9)
    # 参数:verifyUserId = 验证用户ID,userId = 用户Id，shareType = 分享类型，20app分享,25红包分享，platform = 分享渠道，1：新浪微博 2：腾讯微博 3：微信好友 4：微信朋友圈 5：短信 6：qq好友 7：qq空间，
    # amount = 金额，tranId=批次id，channel=渠道类型1外平台,2红包池，3红包群,4二维码，channelId=渠道id，lvl=层次id，1一级，2二级,id，labelIds=红包群标签，逗号表达式
def I25_41(varnum, varuserId, param1, testcase):
    # 参数: redId  红包ID
    varInterfaceName = "I25_41,首页_红包群_我的红包群_私信红包领取信息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_lead_info.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase,redId=param1)
def I25_42(varnum, varuserId, param1, testcase):
    varInterfaceName = "I25_42红包群_我的红包群_新成员数量接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redGroupInfo/2.5/get_newMember_number.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase,groupId=param1)
def I25_43(varnum, varuserId, testcase):
    varInterfaceName = "I25_43,批处理_分享至红包池_同城红包生成批处理接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redPacketBuilder/2.5/saveRedPoolRedPacketBuilder2_5.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase)
def I25_44(varnum, varuserId, testcase):
    varInterfaceName = "I25_44,批处理_广告红包分成_同城红包生成批处理接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/redPacketBuilder/2.2/city_redPacket.do"
    Idefault(varnum, varuserId, varInterfaceName, varUrl, testcase)




print  "\n====================== 2.5.1版本_APP接口测试 ======================"
print "1,================================================================================================="
I251_1("RtnOK","10001679","213","C1-1无参数")
