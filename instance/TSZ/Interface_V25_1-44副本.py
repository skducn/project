# coding: utf-8
#****************************************************************
# Author     : John
# Version    : V 2.5.0
# Date       : 2016-7
# Description: 三藏红包 2.5.0 app接口文档 1-44
#****************************************************************

import sys,requests,redis,MySQLdb,random,datetime,time
import smtplib,pytesseract
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf-8')
from time import sleep

# 1,首页_发红包炸弹_设置广告内容问号接口
# 2,APP登录接口
# 3,我_设置_点击授权，找回红包_第三方绑定接口
# 4,首页_发红包_私信红包_获取用户私信初始金额接口
# 5,首页_发红包_私信红包_私信内容列表接口
# 6,我_设置_提现密码_获取设置提现密码验证码
# 7,我_设置_提现密码_保存提现密码接口
# 8,我_设置_提现密码_修改提现密码接口
# 9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)
# 10,红包模板_红包类型列表
# 11,红包模板_红包模板列表
# 12,红包模板_保存红包模板
# 13,红包模板_删除红包模板
# 14,首页_红包群_我的红包群私信详情接口(新增返回值)
# 15,首页_红包群_我的红包群_领私信转账接口
# 16,首页_红包群_我的红包群_转账详情接口
# 17,私首页_红包群_我的红包群_重新发送私信转账接口
# 18,首页_红包群_我的红包群_私信转账退回接口
# 19,首页_红包群_我的红包群_领私信红包接口
# 20,首页_红包群_我的红包群_私信红包详情接口
# 21,红包群_我的红包群_发普通红包接口
# 22,红包群_我的红包群_发普通红包设置标签接口
# 23,红包群_我的红包群_取消发普通红包接口
# 24,红包群_我的红包群_发拼手气红包接口
# 25,红包群_我的红包群_发拼手气红包设置标签接口
# 26,红包群_我的红包群_取消发拼手气红包接口
# 27,发红包_广告红包发送接口
# 28,发红包_微信支付用户回调接口
# 29,发红包_红包充值接口
# 30,红包列表_红包放入红包池、余额回收接口
# 31,发红包_微信支付用户回调接口
# 32,发红包_红包充值接口
# 33,红包列表_红包放入红包池、余额回收接口
# 34,我的_个人信息接口（新增返回值）
# 35,首页_发红包_私信红包_发送私信红包接口
# 36,首页_发红包_私信红包_发送私信转帐接口
# 37,我的_个人信息接口（新增返回值）
# 38,首页_发红包_私信红包_发送私信红包接口
# 39,首页_发红包_私信红包_发送私信转帐接口
# 40,分享红包_获取分享链接接口
# 41,首页_红包群_我的红包群_私信红包领取信息接口
# 42,红包群_我的红包群_新成员数量接口
# 43,批处理_分享至红包池_同城红包生成批处理接口
# 44,批处理_广告红包分成_同城红包生成批处理接口

def I22_19(varnum,varuserId,param1,param2,param3,param4,param5,testcase):
    # 参数: userID = 用户ID ,acceptId=收件人ID, groupId= 群ID, content=信息内容 ,isGroup=是否为群主(0:否,1:是)
    varInterfaceName =  "I22_19,保存用户私信内容接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivate/2.2/save_user_private_info.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,acceptId=param2,groupId=param3,content=param4,isGroup=param5)
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

def I25(casePrefix,caseStatus,varuserId,**caseParam):
    # 参数: phone = 手机号, cityId=城市ID, channelId= 下载渠道 , channel = 渠道(0手机/1微信/2QQ/3微博),nickName=第三方昵称(可选),
    # headPic=第三方头像(可选),token=第三方token(可选),unionId=微信唯一标识(可选,微信时必传) ,password =验证码
    caseParam={}
    # query1["verifyUserId"]= varuserId
    # query1["verifyCode"]=varverifyCode
    for x in caseParam:
       caseParam[x] =  str(caseParam[x])

    varInterfaceName = "I25_2,APP登录接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.5/login.do"
    Idefault(caseStatus,varuserId,varInterfaceName,varUrl,casePrefix,phone=param1,cityId=param2,channelId=param3,channel=param4,nickName=param5,headPic=param6,token=param7,unionId=param8,password=param9)


def I25_1(varnum,varuserId,testcase):
    varInterfaceName = "I25_1,首页_发红包炸弹_设置广告内容问号接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/appDesc/2.5/get_ad_red_url.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase)
def I25_2(varnum,varuserId,param1,param2,param3,param4,param5,param6,param7,param8,param9,testcase):
    # 参数: phone = 手机号, cityId=城市ID, channelId= 下载渠道 , channel = 渠道(0手机/1微信/2QQ/3微博),nickName=第三方昵称(可选),
    # headPic=第三方头像(可选),token=第三方token(可选),unionId=微信唯一标识(可选,微信时必传) ,password =验证码
    varInterfaceName = "I25_2,APP登录接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.5/login.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,phone=param1,cityId=param2,channelId=param3,channel=param4,nickName=param5,headPic=param6,token=param7,unionId=param8,password=param9)

def I25_3(varnum,varuserId,param1,param2,param3,param4,param5,param6,testcase):
    # 参数: userId = 用户ID, channel = 渠道(0手机/1微信/2QQ/3微博), labelName = 绑定第三方名称 , belongThumb=绑定第三方头像(可选) , openId=第三方标识(微信传 unionId)
    varInterfaceName = "I25_3,我_设置_点击授权，找回红包_第三方绑定接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.5/bindUserThirdInfo.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,channel=param2,labelName=param3,belongThumb=param4,openId=param5,cityId=param6)
def I25_4(varnum,varuserId,param1,testcase):
    # 参数: verifyUserId = 验权用户ID
    varInterfaceName = "I25_4,首页_发红包_私信红包_获取用户私信初始金额接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_init_amount.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1)
def I25_5(varnum,varuserId,testcase):
    varInterfaceName = "I25_5,首页_发红包_私信红包_私信内容列表接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/userPrivateRed/2.5/user_private_content_list.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase)
def I25_6(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: verifyUserId = 验证用户ID, mobileNum = 手机号, type=类型(1：动态密码 2：提现验证码 4:设置提现密码)
    varInterfaceName = "I25_6,我_设置_提现密码_获取设置提现密码验证码"
    varUrl = "http://192.168.2.176:9999/WebBusi/personal/2.1/send_mobile_code.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,verifyUserId=param1,mobileNum=param2,type=param3)
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
    varInterfaceName ="I25,红包群_我的红包群_发拼手气红包设置标签接口"
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
    varInterfaceName =  "I27,红包群_我关注的红包群_抢普通红包接口"
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
    varInterfaceName = "I28,红包群_我关注的红包群_抢拼手气红包接口"
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
    varInterfaceName = "I29,红包群_我关注的红包群_抢广告红包接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/rob_advertRed.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,messageId=param2,groupId=param3,batchId=param4,channelId=param5)
def I25_30(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数:userId = 用户Id，groupId = 群ID，batchId = 批次ID，channelId = 批次ID
    varInterfaceName = "I30,红包群_我关注的红包群_领取广告红包消息接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/redGroup_robRed_receive.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4)
def I25_31(varnum,varuserId,param1,param2,param3,param4,testcase):
    # 参数: userId = 用户Id，groupId = 群ID，batchId = 批次ID，channelId = 批次ID
    varInterfaceName = "31,红包群_我关注的红包群_抢广告红包回调接口"
    varUrl = "http://192.168.2.176:9999/WebBusi/robAdvertRed/2.5/redGroup_robRed_callback.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,groupId=param2,batchId=param3,channelId=param4)
def I25_32(varnum,varuserId,param1,param2,testcase):
    # 参数: userId = 用户Id，channelId = 批次ID
    varInterfaceName = "32,红包群_我关注的红包群_查看是否还有可抢红包接口"
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
    varInterfaceName =  "I33,发红包_广告红包发送接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeGetOrderNew.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,amount=param2,count=param3,payType=param4,door=param5,type=param6,cityId=param7,groupId=param8,templateId=param9,payPwd=param10,redPoolId=param11)
def I25_34(varnum,varuserId,param1,param2,param3,testcase):
    # 参数: userId = 用户Id，redPoolId = 红包批次id，payOrderId = 订单编号
    ########################################################################
    varInterfaceName = "34，发红包_微信支付用户回调接口"
    varUrl = "http://192.168.2.176:9999/payment/order/1.0/apprenticeOrderReturnNew.do"
    Idefault(varnum,varuserId,varInterfaceName,varUrl,testcase,userId=param1,redPoolId=param2,payOrderId=param3)
def I25_35(varnum,varuserId,param1,param2,param3,param4, param5, param6, param7, param8, param9, param10,param11,param12, testcase):
    # 参数: userId = 用户Id，amount = 红包总金额，count = 红包数量，payType = 支付类型，door = 入口标记，
    # type = 资金类型，cityId = 城市编码，groupId = 群id，templateId = 模板id，qrFlag = 是否是二维码充值，redPoolId = 批次id，payPwd = 支付密码
    varInterfaceName = "35,发红包_红包充值接口"
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

print  "\n====================== 2.5.0版本_APP接口测试 ======================"
print "1,================================================================================================="
# 1 首页_发红包炸弹_设置广告内容问号接口
I25_1("RtnOK","10001679","C1-1无参数")
print "2,================================================================================================="
# 2,APP登录接口(只测手机号) 先调用获取验证码接口
I25_2("RtnOK","10001679","13816109050","3101000000","1","0",u"令狐冲","","","",Icommon3("1","13816109050"),"C2-1,手机号,城市ID,下载渠道,渠道(手机),第三方昵称,第三方头像,token,微信唯一标识别(空),验证码")
# print "3,================================================================================================="
# 3 我_设置_点击授权，找回红包_第三方绑定接口(微信标识无法获取?)
# I25_3("RtnOK","10001679","10001679","0","John","","","3101000000","")
print "4,================================================================================================="
# 4,首页_发红包_私信红包_获取用户私信初始金额接口
I25_4("RtnOK","10001679","10001679","C4-1,用户ID")
I25_4("RtnDeviceErr","10001679","","C4-2,用户ID(空)")
I25_4("RtnDeviceErr","10001679","123456789","C4-3,用户ID(错)")
print "5,================================================================================================="
# 5,首页_发红包_私信红包_私信内容列表接口
I25_5("RtnOK","10001679","C5-1无参数")
print "6,================================================================================================="
# 6,我_设置_提现密码_获取设置提现密码验证码  2=提现验证码 ,4=设置提现密码
I25_6("RtnOK","10001679","10001679","13816109050","1","C6-1,用户ID,手机号,类型")
I25_6("RtnOK","10001679","10001679","13816109050","2","C6-2,用户ID,手机号,类型")
I25_6("RtnOK","10001679","10001679","13816109050","4","C6-3,用户ID,手机号,类型")
I25_6("RtnParamErr","10001679","10001679","13816109050","","C6-4,用户ID,手机号,类型(空)")
print "7,================================================================================================="
# 7,我_设置_提现密码_保存提现密码接口
xx=Icommon3("4","13816109050")
I25_7("RtnOK","10001679","10001679","13816109050","123456",xx,"C7-1,用户ID,手机号,当前密码,验证码")
I25_7("RtnParamErr","10001679","10001679","13816109050","123456","0000","C7-2,用户ID,手机号,当前密码,验证码(错)")
I25_7("RtnParamErr","10001679","10001679","13816109050","123456000",xx,"C7-3,用户ID,手机号,当前密码(错),验证码")
I25_7("RtnParamErr","10001679","10001679","13816109050","123456","","C7-4,用户ID,手机号,当前密码,验证码(空)")
I25_7("RtnParamErr","10001679","10001679","13816109050","",xx,"C7-5,用户ID,手机号,当前密码(空),验证码")
print "8,================================================================================================="
# 8,我_设置_提现密码_修改提现密码接口
I25_8("RtnNullOK","10001679","10001679","123456","111111","C8-1,用户ID,原密码,当前密码")
I25_8("RtnNullOK","10001679","10001679","111111","111111","C8-2,用户ID,原密码,当前密码")
I25_8("RtnParamErr","10001679","10001679","666666","111111","C8-3,用户ID,原密码(错),当前密码")
I25_8("RtnParamErr","10001679","10001679","","111111","C8-4,用户ID,原密码(空),当前密码")
I25_8("RtnParamErr","10001679","10001679","666666","","C8-5,用户ID,原密码,当前密码(空)")
I25_8("RtnParamErr","10001679","10001679","","","C8-6,用户ID,原密码(空),当前密码(空)")
print "9,================================================================================================="
# 9,发出的红包广告_用户发的红包广告统计信息接口(新增返回值)
I25_9("RtnOK","10001679","10001679","213","1","1","C9-1,用户ID,群ID,分页开始位置,每页显示条数")
print "10,================================================================================================="
# 10,红包模板_红包类型列表, 类型1=广告红包炸弹 ; 2=好评红包 ; 3=普通群红包 ; 4=普通群红包 ; 5=私信红包
I25_10("RtnOK","10001679","10001679","1","C10-1,用户id,模版类型1")
I25_10("RtnOK","10001679","10001679","2","C10-2,用户id,模版类型2")
I25_10("RtnOK","10001679","10001679","3","C10-3,用户id,模版类型3")
I25_10("RtnOK","10001679","10001679","4","C10-4,用户id,模版类型4")
I25_10("RtnOK","10001679","10001679","5","C10-5,用户id,模版类型5")
I25_10("RtnNoDATAOK","10001679","10001679","6","C10-6,用户id,模版类型(错)")
print "11,================================================================================================="
# 11,红包模板_红包模板列表
I25_11("RtnOK","10001679","10001679","1","1","1","C11-1,用户id,模版类型1,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","2","1","1","C11-2,用户id,模版类型2,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","3","1","1","C11-3,用户id,模版类型3,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","4","1","1","C11-4,用户id,模版类型4,分页开始位置,每页显示条数")
I25_11("RtnOK","10001679","10001679","5","1","1","C11-5,用户id,模版类型5,分页开始位置,每页显示条数")
I25_11("RtnParamErr","10001679","10001679","66","1","1","C11-6,用户id,模版类型(错),分页开始位置,每页显示条数")
print "12,================================================================================================="
# 12,	红包模板_保存红包模板 ,1-5 分别对应 t_sys_config 表里5个类型
I25_12("RtnOK","10001679","10001679","1","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-1,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","2","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-2,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","3","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-3,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","4","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-4,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnOK","10001679","10001679","5","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-5,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
I25_12("RtnParamErr","10001679","10001679","166","title1","pinpai","neirong","www.baidu.com","vedio.com","166","http://pic.com","","C12-6,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")
print "13,================================================================================================="
# 13,红包模板_删除红包模板
I25_13("RtnNullOK","10001679","10001679","1","C13-1,用户ID,模版ID")
I25_13("RtnNullOK","10001679","10001679","2","C13-1,用户ID,模版ID")
I25_13("RtnNullOK","10001679","10001679","3","C13-1,用户ID,模版ID")
I25_13("RtnNullOK","10001679","10001679","4","C13-1,用户ID,模版ID")
I25_13("RtnNullOK","10001679","10001679","5","C13-1,用户ID,模版ID")
print "14,================================================================================================="
# 14 首页_红包群_我的红包群私信详情接口(新增返回值) ,依赖于I22_19群主与群成员各自互相发送1条私信消息
I22_19("RtnOK","10002084","10002084","10002290","610","10002084_保存用户私信内容接口发送的消息","1","C19-1,用户ID ,收件人ID, 群ID, 信息内容 ,是否为群主(0:否,1:是)")
I22_19("RtnOK","10002290","10002290","10002084","815","10002290_保存用户私信内容接口发送的消息","1","C19-2,用户ID ,收件人ID, 群ID, 信息内容 ,是否为群主(0:否,1:是)")
I25_14("RtnOK","10002084","10002290","610","0","20","10002084","1","C14-1,用户ID,群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)") #acceptId为当前登录的人
I25_14("RtnOK","10002290","10002084","610","0","20","10002290","0","C14-2,用户ID,群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)") #acceptId为当前登录的人
I25_14("RtnOK","10002290","10002084","815","","20","10002290","1","C14-3,用户ID,群ID,分页开始位置(空),每页显示条数,收件人ID,是否为群主(0:否,1:是)")
# I25_14("RtnSysErr","10002290","10002084","815","0","","10002290","1","C14-4,用户ID,群ID,分页开始位置,每页显示条数(空),收件人ID,是否为群主(0:否,1:是)") #每页显示条数为空时,取默认参数每页20条
# I25_14("RtnSysErr","10002290","10002084","815","","","10002290","1","C14-5,用户ID,群ID,分页开始位置(空),每页显示条数(空),收件人ID,是否为群主(0:否,1:是)") #每页显示条数为空时,取默认参数每页20条
I25_14("RtnParamErr","10002084","","610","0","20","10002290","1","C14-6,用户ID(空),群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","","0","20","10002290","1","C14-7,用户ID,群ID(空),分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","","0","20","","1","C14-8,用户ID,群ID,分页开始位置,每页显示条数,收件人ID(空),是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","","0","20","10002290","","C14-9,用户ID,群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)(空)")
I25_14("RtnParamErr","10002084","00002084","610","0","20","10002290","1","C14-10,用户ID(错),群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","000","0","20","10002290","1","C14-11,用户ID,群ID(错),分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","610","-1","20","10002290","1","C14-12,用户ID,群ID,分页开始位置(错),每页显示条数,收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","610","0.1","20","10002290","1","C14-13,用户ID,群ID,分页开始位置(错),每页显示条数,收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","610","0","-1","10002290","1","C14-14,用户ID,群ID,分页开始位置,每页显示条数(错),收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","610","0","0.5","10002290","1","C14-15,用户ID,群ID,分页开始位置,每页显示条数(错),收件人ID,是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","610","0","20","00002290","1","C14-16,用户ID,群ID,分页开始位置,每页显示条数,收件人ID(错),是否为群主(0:否,1:是)")
I25_14("RtnParamErr","10002084","10002084","610","0","20","10002290","0","C14-17,用户ID,群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)(错)")
I25_14("RtnParamErr","10002084","10002084","610","0","20","10002290","2","C14-18,用户ID,群ID,分页开始位置,每页显示条数,收件人ID,是否为群主(0:否,1:是)(错)")
print "15,================================================================================================="
#15首页_红包群_我的红包群_领私信转账接口(依赖I25_39)
# 39首页_发红包_私信红包_发送私信转帐接口(间隔10s)
print "   ...waiting 12s"
sleep(12)
I25_39("RtnOK","10002084","10002084","3","1","10002290","610","10002084给10002290发送私信转账1元","000000","C39-1,用户ID ,支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , 红包金额, 收红包用户ID ,群ID ,信息内容(可选) ,支付密码(可选,支付类型3、5必传)")
print "   ...waiting 12s"
sleep(12)
I25_15("RtnOK","10002290","10002290","3","C15-1,验权用户ID ,红包ID")
I25_15("RtnDeviceErr","10002290","","3","C15-2,验权用户ID(空) ,红包ID")
I25_15("RtnParamErr","10002290","10002290","","C15-3,验权用户ID ,红包ID(空)")
I25_15("RtnDeviceErr","10002290","","","C15-4,验权用户ID(空) ,红包ID(空)")
I25_15("RtnDeviceErr","10002290","00002290","3","C15-5,验权用户ID(错) ,红包ID")
I25_15("RtnDeviceErr","10002290","0.01","3","C15-6,验权用户ID(错) ,红包ID")
I25_15("RtnDeviceErr","10002290","-1","3","C15-7,验权用户ID(错) ,红包ID")
I25_15("RtnParamErr","10002290","10002290","0.1","C15-8,验权用户ID ,红包ID(错)")
I25_15("RtnParamErr","10002290","10002290","0","C15-9,验权用户ID ,红包ID(错)")
I25_15("RtnParamErr","10002290","10002290","-1","C15-10,验权用户ID ,红包ID(错)")
print "16,================================================================================================="
#16首页_红包群_我的红包群_转账详情接口
I25_16("RtnOK","10002084","10002084","3","C16-1,验权用户ID ,红包ID")
I25_16("RtnOK","10002290","10002290","3","C16-2,验权用户ID ,红包ID")
I25_16("RtnDeviceErr","10002290","","3","C16-3,验权用户ID(空) ,红包ID")
I25_16("RtnParamErr","10002290","10002290","","C16-4,验权用户ID ,红包ID(空)")
I25_16("RtnDeviceErr","10002290","","","C16-5,验权用户ID(空) ,红包ID(空)")
I25_16("RtnDeviceErr","10002290","00002290","3","C16-6,验权用户ID(错) ,红包ID")
I25_16("RtnDeviceErr","10002290","0.01","3","C16-7,验权用户ID(错) ,红包ID")
I25_16("RtnDeviceErr","10002290","-1","3","C16-8,验权用户ID(错) ,红包ID")
I25_16("RtnParamErr","10002290","10002290","0.1","C16-9,验权用户ID ,红包ID(错)")
I25_16("RtnParamErr","10002290","10002290","0","C16-10,验权用户ID ,红包ID(错)")
I25_16("RtnParamErr","10002290","10002290","-1","C16-11,验权用户ID ,红包ID(错)")
print "17,================================================================================================="
# # #17首页_红包群_我的红包群_重新发送私信转账接口(依赖于I25_39)
# # 39首页_发红包_私信红包_发送私信转帐接口
I25_39("RtnOK","10002084","10002084","3","1","10002290","610","10002084给10002290发送私信转账1元","000000","C39-1,用户ID ,支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , 红包金额, 收红包用户ID ,群ID ,信息内容(可选) ,支付密码(可选,支付类型3、5必传)")
print "   ...waiting 12s"
sleep(12)
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_user_private_red where userId=10002084 and belongId=10002290 order by id desc limit 1')
tbl0 = curT.fetchone()
I25_17("RtnOK","10002084","10002084",str(tbl0[0]),"C17-1,验权用户ID ,红包ID")
I25_17("RtnDeviceErr","10002084","","6","C17-2,验权用户ID(空) ,红包ID")
I25_17("RtnParamErr","10002084","10002084","","C17-3,验权用户ID ,红包ID(空)")
I25_17("RtnDeviceErr","10002084","","","C17-4,验权用户ID(空) ,红包ID(空)")
I25_17("RtnDeviceErr","10002084","00002084","30","C17-5,验权用户ID(错) ,红包ID")
I25_17("RtnDeviceErr","10002084","0.01","6","C17-6,验权用户ID(错) ,红包ID")
I25_17("RtnDeviceErr","10002084","-1","6","C17-7,验权用户ID(错) ,红包ID")
I25_17("RtnParamErr","10002084","10002084","0.1","C17-8,验权用户ID ,红包ID(错)")
I25_17("RtnParamErr","10002084","10002084","0","C17-9,验权用户ID ,红包ID(错)")
I25_17("RtnParamErr","10002084","10002084","-1","C17-10,验权用户ID ,红包ID(错)")
print "18,================================================================================================="
#18首页_红包群_我的红包群_私信转账退回接口 (依赖I25_39)
print "   ...waiting 20s"
sleep(20)
I25_39("RtnOK","10002084","10002084","5","1","10002290","610","10002084给10002290发送私信转账1元","000000","C39-1,用户ID ,支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , 红包金额, 收红包用户ID ,群ID ,信息内容(可选) ,支付密码(可选,支付类型3、5必传)")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('select id from t_user_private_red where userId=10002084 and belongId=10002290 order by id desc limit 1')
tbl0 = curT.fetchone()
I25_18("RtnOK","10002290","10002290",str(tbl0[0]),"C18-1,验权用户ID ,红包ID")
I25_18("RtnDeviceErr","10002290","",tbl0[0],"C18-2,验权用户ID(空) ,红包ID")
I25_18("RtnParamErr","10002290","10002290","","C18-3,验权用户ID ,红包ID(空)")
I25_18("RtnDeviceErr","10002290","","","C18-4,验权用户ID(空) ,红包ID(空)")
I25_18("RtnDeviceErr","10002290","00002290",tbl0[0],"C18-5,验权用户ID(错) ,红包ID")
I25_18("RtnDeviceErr","10002290","0.01",tbl0[0],"C18-6,验权用户ID(错) ,红包ID")
I25_18("RtnDeviceErr","10002290","-1",tbl0[0],"C18-7,验权用户ID(错) ,红包ID")
I25_18("RtnParamErr","10002290","10002290","0.1","C18-8,验权用户ID ,红包ID(错)")
I25_18("RtnParamErr","10002290","10002290","0","C18-9,验权用户ID ,红包ID(错)")
I25_18("RtnParamErr","10002290","10002290","-1","C18-10,验权用户ID ,红包ID(错)")
print "19,================================================================================================="
# #19首页_红包群_我的红包群_领私信红包接口(依赖I25_38)
# # #38首页_发红包_私信红包_发送私信红包接口
I25_38("RtnOK","10002084","10002084","3","1","10002290","610","10002084给10002290发送私信红包10","000000","","C38-1,用户ID ,支付类型(1 微信，2 支付宝，3 余额 ,4,群账户, 5三藏卡) , 红包金额, 收红包用户ID ,群ID ,信息内容(可选) ,支付密码(可选,支付类型3、5必传) ,模板(可选)")
I25_19("RtnOK","10002290","10002290","2","C19-1,验权用户ID ,红包ID")
I25_19("RtnDeviceErr","10002290","","2","C19-2,验权用户ID(空) ,红包ID")
I25_19("RtnParamErr","10002290","10002290","","C19-3,验权用户ID ,红包ID(空)")
I25_19("RtnDeviceErr","10002290","","","C19-4,验权用户ID(空) ,红包ID(空)")
I25_19("RtnDeviceErr","10002290","00002290","2","C19-5,验权用户ID(错) ,红包ID")
I25_19("RtnDeviceErr","10002290","0.01","2","C19-6,验权用户ID(错) ,红包ID")
I25_19("RtnDeviceErr","10002290","-1","2","C19-7,验权用户ID(错) ,红包ID")
I25_19("RtnParamErr","10002290","10002290","0.1","C19-8,验权用户ID ,红包ID(错)")
I25_19("RtnParamErr","10002290","10002290","0","C19-9,验权用户ID ,红包ID(错)")
I25_19("RtnParamErr","10002290","10002290","-1","C19-10,验权用户ID ,红包ID(错)")
print "20,================================================================================================="
# #20首页_红包群_我的红包群_私信红包详情接口
I25_20("RtnOK","10002084","10002084","2","C20-1,验权用户ID ,红包ID")
I25_20("RtnOK","10002290","10002290","2","C20-2,验权用户ID ,红包ID")
I25_20("RtnDeviceErr","10002290","","2","C20-3,验权用户ID(空) ,红包ID")
I25_20("RtnParamErr","10002290","10002290","","C20-4,验权用户ID ,红包ID(空)")
I25_20("RtnDeviceErr","10002290","","","C20-5,验权用户ID(空) ,红包ID(空)")
I25_20("RtnDeviceErr","10002290","00002290","2","C20-6,验权用户ID(错) ,红包ID")
I25_20("RtnDeviceErr","10002290","0.01","2","C20-7,验权用户ID(错) ,红包ID")
I25_20("RtnDeviceErr","10002290","-1","2","C20-8,验权用户ID(错) ,红包ID")
I25_20("RtnParamErr","10002290","10002290","0.1","C20-9,验权用户ID ,红包ID(错)")
I25_20("RtnParamErr","10002290","10002290","0","C20-10,验权用户ID ,红包ID(错)")
I25_20("RtnParamErr","10002290","10002290","-1","C20-11,验权用户ID ,红包ID(错)")
print "21,================================================================================================="
# 21,红包群_我的红包群_发普通红包接口
# 注意事项: 连续发普通红包需间隔10s
# 前置条件: 10002084账号要有余额 , 默认设置100元, t_redgroup_baseinfo,groupAccount=10000(100元) ; redis同步修改为10000.
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('update t_redgroup_baseinfo set groupAccount=10000 where userId=10002084')
conn.commit()
r2 = redis.StrictRedis(host='192.168.2.176', port=6380, db=0,password="dlhy123456")
r2.hset("t_redgroup_baseinfo:10002084","groupAccount",10000)
sleep(2)
# 红包金额10元
I25_21("RtnOK","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
sleep(13)
print "   ...waiting 13s"
# 红包金额5.234元
I25_21("RtnOK","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","5.237","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
sleep(13)
print "   ...waiting 13s"
# 红包金额 0.03元
I25_21("RtnOK","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","0.03","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
# 检查扣费情况
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select groupAccount from t_redgroup_baseinfo where userId=10002084')
tbl3 = curT.fetchone()
if tbl3[0]==8474:print "  => [Ok,C21-1,t_redgroup_baseinfo,扣费计算正确]"
else:print "  => [errorrrrrrrrrr,C21-1,t_redgroup_baseinfo,扣费计算错误,预期:8474,实测:" + str(tbl3[0]) + "]"
I25_21("RtnParamErr","10002084","","3101000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084","C21-2,群Id(空) ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084","C21-3,群Id ,城市ID(空) , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
sleep(13)
I25_21("RtnOK","10002084","610","3101000000","","1","10","4","000000","","10002084","C21-4,群Id ,城市ID , 标题(空), 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","","10","4","000000","","10002084","C21-5,群Id ,城市ID , 标题, 红包个数(空) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #bug
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","","4","000000","","10002084","C21-6,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(空) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","","000000","","10002084","C21-7,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(空) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","","10002084","C21-8,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnDeviceErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","","","C21-9,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","000","3101000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084","C21-10,群Id(错) ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
sleep(10)
I25_21("RtnOK","10002084","610","0000000000","10002084给10002290发送普通红包1元","1","10","4","000000","","10002084","C21-11,群Id ,城市ID(错) , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #城市ID不做判断,对系统没影响
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","0","10","4","000000","","10002084","C21-12,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","-1","10","4","000000","","10002084","C21-13,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
# I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","0.01","10","4","000000","","10002084","C21-14,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #bug
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","-1","4","000000","","10002084","C21-15,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","0","4","000000","","10002084","C21-16,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","0.001","4","000000","","10002084","C21-17,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","0.025","4","000000","","10002084","C21-18,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","0","000000","","10002084","C21-19,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","5","000000","","10002084","C21-20,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","-1","000000","","10002084","C21-21,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","0.1","000000","","10002084","C21-22,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","0","10002084","C21-23,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","-1","10002084","C21-24,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","0.1","10002084","C21-25,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnParamErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","","0000000","10002084","C21-26,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnDeviceErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","","","C21-27,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnDeviceErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","","000","C21-28,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_21("RtnDeviceErr","10002084","610","3101000000","10002084给10002290发送普通红包1元","1","1","4","000000","","-1","C21-29,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
print "22,================================================================================================="
# #22红包群_我的红包群_发普通红包设置标签接口(依赖于21)
# 业务逻辑: 红包群中发送普通红包,点击塞进红包后,选择标签发送红包,标签ID为0 表示所有群成员可见 , 多个标签ID以逗号分隔表示发送到多个标签下
# 前置条件: 红包群中存在标签(ID), select id from t_redgroup_label where groupId=610 (2182,2183)
# 动态参数: 接口21 返回值 batchId=批次ID, channelId=渠道ID
# 数据库: 表 t_redgroup_message , t_redgroup_message_auth新增一条记录; t_redgroup_memberinfo中对应标签下的非黑名单群成员的isMessage + 1
# t_redgroup_message ,type类型说明: 0文字消息,1红包炸弹消息,2分享消息,3抢到红包消息,4分享奖励消息,5广告红包抢完消息,6第一次加入消息,7图片消息,8:普通红包消息,9:拼手气红包消息,10:广告红包消息,11:抢到普通红包消息,12:抢到拼手气红包消息,13：抢到广告红包消息,14:普通红包抢完消息,15：拼手气红包抢完消息
# 检查标签ID=0 时情况
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
print "   ...waiting 13s"
sleep(13)
I25_21("RtnOK","10002084","610","3101000000",varAutoMessage,"1","10","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curT.fetchone()
I25_22("RtnOK","10002084","10002084","610",tbl3[1],tbl3[0],"0","C22-1,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
# 检查数据库记录是否生成
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select count(id),id from t_redgroup_message where groupId=610 and type=8 and channelId=%s and batchId=%s order by id desc' %(tbl3[0],tbl3[1]))
tbl4 = curT.fetchone()
if tbl4[0] == 1 :print "OK,I25_22,t_redgroup_message,生成一条记录"
else: print "Error,I25_22,t_redgroup_message,未生成新记录!"
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select count(id) from t_redgroup_messamge_auth where groupId=610 and messageId=%s'%(tbl4[1]))
tbl5 = curT.fetchone()
if tbl5[0] == 1 :print "OK,I25_22,t_redgroup_messamge_auth,生成一条记录"
else: print "Error,I25_22,t_redgroup_messamge_auth,未生成新记录!"
# 检查1个标签ID情况
print "   ...waiting 13s"
sleep(13)
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
I25_21("RtnOK","10002084","610","3101000000",varAutoMessage,"1","10","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curT.fetchone()
I25_22("RtnOK","10002084","10002084","610",tbl3[1],tbl3[0],"2182","C22-2,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
# 检查多个标签ID情况
print "   ...waiting 13s"
sleep(13)
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
I25_21("RtnOK","10002084","610","3101000000",varAutoMessage,"1","10","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curT.fetchone()
I25_22("RtnOK","10002084","10002084","610",tbl3[1],tbl3[0],"2182,2183","C22-2,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnDeviceErr","10002084","","610","3412","4505","2611","C22-4,用户ID(空) ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","","3412","4505","2611","C22-5,用户ID ,群ID(空), 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","610","","4505","2611","C22-6,用户ID ,群ID, 批次ID(空), 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","610","3412","","2611","C22-7,用户ID ,群ID, 批次ID, 渠道ID(空) ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","610","3412","","2611","C22-8,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔(空)")
I25_22("RtnDeviceErr","10002084","0002084","610","3412","4505","2611","C22-9,用户ID(错) ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","000","3412","4505","2611","C22-10,用户ID ,群ID(错), 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","610","00","4505","2611","C22-11,用户ID ,群ID, 批次ID(错), 渠道ID ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","610","3412","00","2611","C22-12,用户ID ,群ID, 批次ID, 渠道ID(错) ,标签ID,多个以逗号分隔")
I25_22("RtnParamErr","10002084","10002084","610","3412","4505","01","C22-13,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔(错)")
print "23,================================================================================================="
# #23红包群_我的红包群_取消发普通红包接口
# # 检查1个标签ID情况
print "   ...waiting 13s"
sleep(13)
varAutoMessage=u"10002084给10002290发送普通红包10元%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
I25_21("RtnOK","10002084","610","3101000000",varAutoMessage,"1","10","4","000000","","10002084","C21-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信 2 支付宝 3 余额 4红包群) ,支付密码（可选）payType=3时必选 ,模板ID（可选）,用户ID") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curT.fetchone()
I25_23("RtnOK","10002084","10002084","610",tbl3[1],tbl3[0],"C23-1,用户ID ,群ID, 批次ID, 渠道ID")
I25_23("RtnDeviceErr","10002084","","610","3419","4512","C23-2,用户ID(空) ,群ID, 批次ID, 渠道ID")
I25_23("RtnParamErr","10002084","10002084","","3419","4512","C23-3,用户ID ,群ID(空), 批次ID, 渠道ID")
I25_23("RtnParamErr","10002084","10002084","610","","4512","C23-4,用户ID ,群ID, 批次ID(空), 渠道ID")
I25_23("RtnParamErr","10002084","10002084","610","3419","","C23-5,用户ID ,群ID, 批次ID, 渠道ID(空)")
I25_23("RtnDeviceErr","10002084","0002084","610","3419","4512","C23-6,用户ID(错) ,群ID, 批次ID, 渠道ID")
I25_23("RtnParamErr","10002084","10002084","000","3419","4512","C23-7,用户ID ,群ID(错), 批次ID, 渠道ID")
I25_23("RtnParamErr","10002084","10002084","610","00","4512","C23-8,用户ID ,群ID, 批次ID(错), 渠道ID")
I25_23("RtnParamErr","10002084","10002084","610","3419","00","C23-9,用户ID ,群ID, 批次ID, 渠道ID(错)")
print "24,================================================================================================="
# #24红包群_我的红包群_发拼手气红包接口
I25_24("RtnOK","10002084","610","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
I25_24("RtnParamErr","10002084","","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-2,群Id(空) ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-3,群Id ,城市ID(空) , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
sleep(10)
I25_24("RtnOK","10002084","610","3101000000","","1","10","4","000000","","10002084","C24-4,群Id ,城市ID , 标题(空), 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","","10","4","000000","","10002084","C24-5,群Id ,城市ID , 标题, 红包个数(空) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #bug
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","","4","000000","","10002084","C24-6,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(空) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","","000000","","10002084","C24-7,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(空) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","","","10002084","C24-8,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnDeviceErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","","","C24-9,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","000","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-10,群Id(错) ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
sleep(10)
I25_24("RtnOK","10002084","610","0000000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-11,群Id ,城市ID(错) , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #城市ID不做判断,对系统没影响
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","0","10","4","000000","","10002084","C24-12,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","-1","10","4","000000","","10002084","C24-13,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
# I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","0.01","10","4","000000","","10002084","C24-14,群Id ,城市ID , 标题, 红包个数(错) ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #bug
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","-1","4","000000","","10002084","C24-15,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","0","4","000000","","10002084","C24-16,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","0.001","4","000000","","10002084","C24-17,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","0.025","4","000000","","10002084","C24-18,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元)(错) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","0","000000","","10002084","C24-19,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","5","000000","","10002084","C24-20,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","-1","000000","","10002084","C24-21,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","0.1","000000","","10002084","C24-22,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额)(错) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","","0","10002084","C24-23,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","","-1","10002084","C24-24,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","","0.1","10002084","C24-25,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnParamErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","","0000000","10002084","C24-26,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(错), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnDeviceErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","","","C24-27,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnDeviceErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","","000","C24-28,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
I25_24("RtnDeviceErr","10002084","610","3101000000","10002084发送拼手气红包1元","1","1","4","000000","","-1","C24-29,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）(空), payType=3时，必选 ,模板ID（可选）")
print "25,================================================================================================="
# # #25红包群_我的红包群_发拼手气红包设置标签接口(依赖24)
# 业务逻辑:红包群中发送拼手气红包,点击塞钱进红包后选择标签发送红包,标签ID为0时代表所有群成员可见,多个标签ID以逗号分隔代表发送到多个标签下
# 前提条件:红包群中存在标签,红包群的标签ID: SELECT id FROM t_redgroup_label WHERE groupId=610
# 动态参数:接口24的返回值"batchId":批次ID,"channelId":渠道ID
# 影响数据库:表t_redgroup_message,表t_redgroup_messamge_auth中各插入一条数据 ,表t_redgroup_memberinfo中对应标签下的非黑名单群成员的isMessage+1
print "   ...waiting 13s"
sleep(13)
I25_24("RtnOK","10002084","610","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curT.fetchone()
I25_25("RtnOK","10002084","10002084","610",tbl3[1],tbl3[0],"0","C25-1,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
# I25_25("RtnOK","10002084","10002084","610","3426","4518","2611","C25-2,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
# I25_25("RtnOK","10002084","10002084","610","3427","4519","2611,2382","C25-3,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnDeviceErr","10002084","","610","3412","4505","2611","C25-4,用户ID(空) ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","","3412","4505","2611","C25-5,用户ID ,群ID(空), 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","610","","4505","2611","C25-6,用户ID ,群ID, 批次ID(空), 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","610","3412","","2611","C25-7,用户ID ,群ID, 批次ID, 渠道ID(空) ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","610","3412","","2611","C25-8,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔(空)")
I25_25("RtnDeviceErr","10002084","0002084","610","3412","4505","2611","C25-9,用户ID(错) ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","000","3412","4505","2611","C25-10,用户ID ,群ID(错), 批次ID, 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","610","00","4505","2611","C25-11,用户ID ,群ID, 批次ID(错), 渠道ID ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","610","3412","00","2611","C25-12,用户ID ,群ID, 批次ID, 渠道ID(错) ,标签ID,多个以逗号分隔")
I25_25("RtnParamErr","10002084","10002084","610","3412","4505","01","C25-13,用户ID ,群ID, 批次ID, 渠道ID ,标签ID,多个以逗号分隔(错)")
print "26,================================================================================================="
# #26红包群_我的红包群_取消发拼手气红包接口
print "   ...waiting 13s"
sleep(13)
I25_24("RtnOK","10002084","610","3101000000","10002084发送拼手气红包1元","1","10","4","000000","","10002084","C24-1,群Id ,城市ID , 标题, 红包个数 ,红包单个金额(单位:元) ,支付类型(1 微信，2 支付宝，3 余额) ,支付密码（可选）, payType=3时，必选 ,模板ID（可选）") #支付类型为4表示使用群账户余额,接口文档上模板ID后少了参数userId
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
curT = conn.cursor()
curT.execute('select id,extensionRedPoolId from t_extension_channel where userId=10002084 and groupId=610 order by id desc limit 1')
tbl3 = curT.fetchone()
I25_26("RtnOK","10002084","10002084","610",tbl3[1],tbl3[0],"C26-1,用户ID ,群ID, 批次ID, 渠道ID")
I25_26("RtnDeviceErr","10002084","","610",tbl3[1],tbl3[0],"C26-2,用户ID(空) ,群ID, 批次ID, 渠道ID")
I25_26("RtnParamErr","10002084","10002084","",tbl3[1],tbl3[0],"C26-3,用户ID ,群ID(空), 批次ID, 渠道ID")
I25_26("RtnParamErr","10002084","10002084","610","","4522","C26-4,用户ID ,群ID, 批次ID(空), 渠道ID")
I25_26("RtnParamErr","10002084","10002084","610","3431","","C26-5,用户ID ,群ID, 批次ID, 渠道ID(空)")
I25_26("RtnDeviceErr","10002084","0002084","610","3431","4522","C26-6,用户ID(错) ,群ID, 批次ID, 渠道ID")
I25_26("RtnParamErr","10002084","10002084","000","3431","4522","C26-7,用户ID ,群ID(错), 批次ID, 渠道ID")
I25_26("RtnParamErr","10002084","10002084","610","0.1","4522","C26-8,用户ID ,群ID, 批次ID(错), 渠道ID")
I25_26("RtnParamErr","10002084","10002084","610","3431","00","C26-9,用户ID ,群ID, 批次ID, 渠道ID(错)")





print "21,================================================================================================="
##发普通红包接口
I25_21("RtnOK","10001588","118","3101000000","红包标题","5","0.5","4","111111","","10001588","C21-1,userId,payType,cityId,payPwd,groupId,redNumber,amount,brandContent,templateId")
##发普通红包设置标签接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
conn.commit()
I25_22("RtnOK","10001588","10001588","118",data1[0],data2[0],"0","C22-1,userId,groupId,batchId,channelId,labelId")
##发拼手气红包接口
I25_24("RtnOK","10001588","118","3101000000","红包标题","5","2.5","4","111111","","10001588", "C24-1,userId,groupId,cityId,brandContent,redNumber,amount,payType")

##发拼手气红包设置标签接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
conn.commit()
sleep(10)  #########################################整体后需要放开#############################################################
I25_25("RtnOK","10001588","10001588","118",data1[0],data2[0],"0","C25-1,userId,groupId,batchId,channelId,labelId")

print "27,================================================================================================="
#27红包群_我关注的红包群_抢普通红包接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=32 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
conn.commit()
I25_27("RtnOK","10001801","10001801",data3,"118",data1,data2, "C27-1,userId,messageId,groupId,batchId,channelId")
conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True) #sit2
curT = conn.cursor()
curT.execute('SELECT count(id),id from ukardweb.t_external_redDetail WHERE belongId=10001801 and redState=3 and redType=32 and batchId=%s' %(data1[0]))
data4 = curT.fetchone()
if data4[0]==1:print "  => [Ok,t_external_redDetail数据库记录新增1条成功并且10001801领取成功,C27-1]"
else:print "  => [errorrrrrrrrrr,t_external_redDetail数据库记录新增1条失败且领取失败,C27-1]"
I25_27("RtnParamErr","10001801","",data3,"118",data1,data2, "C27-2,userId(空),messageId,groupId,batchId,channelId")
I25_27("RtnParamErr","10001801","10001801","","118",data1,data2, "C27-3,userId,messageId（空),groupId,batchId,channelId")
I25_27("RtnParamErr","10001801","10001801",data3,"118",'',data2, "C27-4,userId,messageId,groupId,batchId(空),channelId")
I25_27("RtnParamErr","10001801","10001801",data3,"118",data1,'', "C27-5,userId,messageId,groupId,batchId,channelId(空)")
I25_27("RtnDeviceErr","","",data3,"118",data1,data2, "C27-6,userId（空）,messageId,groupId,batchId,channelId(空)")
#黑名单用户
I25_27("RtnOK","10001813","10001813",data3,"118",data1,data2, "C27-7,userId,messageId,groupId,batchId,channelId")
print "28,================================================================================================="
# 28红包群_我关注的红包群_抢拼手气红包接口
#调用一下
I25_24("RtnOK","10001588","118","3101000000","红包标题","5","2.5","4","111111","","10001588", "C24-1,userId,groupId,cityId,brandContent,redNumber,amount,payType")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
conn.commit()
sleep(10)  #########################################整体后需要放开#############################################################
I25_25("RtnOK","10001588","10001588","118",data1,data2,"0","C25-1,userId,groupId,batchId,channelId,labelId")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=33  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=33 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
I25_28("RtnOK","10001801","10001801",data3,"118",data1,data2, "C28-1,userId,messageId,groupId,batchId,channelId")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT count(id),id from ukardweb.t_external_redDetail WHERE belongId=10001801 and redState=3 and redType=33 and batchId=%s' %(data1[0]))
data4 = curT.fetchone()
if data4[0]==1:print "  => [Ok,t_external_redDetail数据库记录新增1条成功并且10001801领取成功,C28-1]"
else:print "  => [errorrrrrrrrrr,t_external_redDetail数据库记录新增1条失败且领取失败,C28-1]"
I25_28("RtnParamErr","10001801","",data3,"118",data1,data2, "C28-2,userId(空),messageId,groupId,batchId,channelId")
I25_28("RtnParamErr","10001801","10001801","","118",data1,data2, "C28-3,userId,messageId（空),groupId,batchId,channelId")
I25_28("RtnParamErr","10001801","10001801",data3,"118",'',data2, "C28-4,userId,messageId,groupId,batchId(空),channelId")
I25_28("RtnParamErr","10001801","10001801",data3,"118",data1,'', "C28-5,userId,messageId,groupId,batchId,channelId(空)")
I25_28("RtnDeviceErr","","",data3,"118",data1,data2, "C28-6,userId（空）,messageId,groupId,batchId,channelId(空)")
#黑名单用户
I25_28("RtnOK","10001813","10001813",data3,"118",data1,data2, "C28-7,userId,messageId,groupId,batchId,channelId")

##新用户没有模版就需要调用一下，老用户有模版就不需要
# #I25_12("RtnOK","10001588","10001588","1","title1","pinpai","neirong","www.baidu.com","vedio.com","1","http://pic.com","","C12-1,用户id,模版类型,标题,品牌,推广内容,推广链接,视频链接,添加图文标记,图片链接,模版Id")

#33发红包_广告红包发送接口
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
#连续执行会提示重复提交
sleep(5)
I25_33("RtnParamErr","10001588","10001588","1","100000","0.01","1","0","3101000000","0","31","111111","0","C33-2,userId,amount,count(错误),payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnDeviceErr","10001588","","1","1","0.01","1","0","3101000000","0","31","111111","0","C33-3,userId（空）,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr","10001588","10001588","","1","3","1","0","3101000000","0","31","111111","0","C33-4,userId,amount（空）,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr","10001588","10001588","1","-1","3","1","0","3101000000","0","31","111111","0","C33-5,userId,amount,count（负数）,payType,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "2", "3", "100", "3101000000", "0", "31", "111111", "0","C33-6,userId,amount,count,payType（错不在数据类型范围内）,door,cityId,groupId,templateId,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "", "111111", "0","C33-7,userId,amount,count,payType,door,cityId,groupId,templateId（空）,payPwd,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31", "", "0","C33-8,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（空）,redPoolId,")
sleep(5)
I25_33("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31", "", "0","C33-9,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（错）,redPoolId,")
sleep(5)
I25_33("RtnOK", "10001588", "10001588", "1", "2", "3", "2", "0", "3101000000", "0", "31", "111111", "3452","C33-10,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd（错）,redPoolId,")

print "29,================================================================================================="
#29红包群_我关注的红包群_抢广告红包接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
I25_29("RtnOK", "10001877", "10001877","123", "118", data1, data2,"C29-1,userId,messageId,groupId,batchId,channelId,")
I25_29("RtnParamErr", "10001877", "","123", "118", data1, data2,"C29-2,userId(空),messageId(groupId,batchId,channelId,")
I25_29("RtnParamErr", "10001877", "10001877","123", "", data1, data2,"C29-3,userId,messageId,groupId（空）,batchId,channelId,")
I25_29("RtnParamErr", "10001877", "10001877","123", "118", "", data2,"C29-4,userId,messageId,groupId,batchId(空),channelId,")
I25_29("RtnParamErr", "10001877", "10001877","123", "118", data1, "","C29-5,userId,messageId,groupId,batchId,channelId（空）,")
print "30,================================================================================================="
#30红包群_我关注的红包群_领取广告红包消息接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_redgroup_message WHERE batchId=%s' %(data1[0]))
data3 = curT.fetchone()
I25_30("RtnOK", "10001877", "10001877","118", data1, data2,"C30-1,userId,groupId,batchId,channelId,")
I25_30("RtnParamErr", "10001877", "","118", data1, data2,"C30-2,userId,groupId,batchId,channelId,")
I25_30("RtnParamErr", "10001877", "10001877","", data1, data2,"C30-3,userId,groupId（空）,batchId,channelId,")
I25_30("RtnParamErr", "10001877", "10001877","119", "", data2,"C30-4,userId,groupId,batchId(空),channelId,")
I25_30("RtnParamErr", "10001877", "10001877","119", data1, "","C30-5,userId,groupId,batchId,channelId(空),")
print "31,================================================================================================="
#31红包群_我关注的红包群_抢广告红包回调接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
I25_31("RtnOK", "10001877", "10001877","118",data1[0],data2[0],"C31-1,userId,groupId,batchId,channelId,")
I25_31("RtnParamErr", "10001877", "","118",data1[0],data2[0],"C31-2,userId（空）,groupId,batchId,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","",data1[0],data2[0],"C31-3,userId,groupId（空）,batchId,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","",data1[0],data2[0],"C31-4,userId,groupId,batchId（空）,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","118","",data2[0],"C31-5,userId,groupId,batchId（空）,channelId,")
I25_31("RtnParamErr", "10001877", "10001877","118",data1[0],"" ,"C31-6,userId,groupId,batchId,channelId（空）,")
print "32,================================================================================================="
#32红包群_我关注的红包群_查看是否还有可抢红包接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT.execute('SELECT id from ukardweb.t_extension_channel WHERE  userId=10001588 and redType=34 ORDER BY id DESC LIMIT 0,1')
data2 = curT.fetchone()
I25_32("RtnOK", "10001877", "10001877",data2[0],"C32-1,userId,channelId,")
I25_32("RtnParamErr", "10001877", "10001877","","C32-2,userId,channelId(空),")
print "34,================================================================================================="
#34发红包_微信支付用户回调接口  ##################该接口正常业务无法正常测试####################
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT pay_order_id  from ukardweb.t_user_withdraw WHERE user_id=10001588 and object_id=%s' %(data1[0]))
data2 = curT.fetchone()
#首先要发红包微信支付
sleep(10)
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,cityId,groupId,templateId,payPwd,redPoolId")

# I25_34("RtnParamErr", "10001588", "10001588",data1[0],data2[0],"C34-1,userId,redPoolId,payOrderId")
I25_34("RtnParamErr", "10001588", "10001588","","","C34-2,userId,redPoolId,payOrderId(空)")
I25_34("RtnParamErr", "10001588", "10001588","",data2[0],"C34-3,userId,redPoolId(空),payOrderId")
print "35,================================================================================================="
#35发红包_红包充值接口
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=32  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
conn.commit()
I25_35("RtnOK", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-1,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
# #本人应无法给别人红包充值已修复
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", "3680", "111111","C35-2,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-3,userId（空）,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId（别人的红包批次）,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-4,userId,amount（空）,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "-1", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-5,userId,amount,count（负数）,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "", "1", "0", "3101000000", "0", "31","0", data1[0], "111111","C35-6,userId,amount,count,payType（空）,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", "", "111111","C35-7,userId,amount,count,payType（空）,door,cityId,groupId,templateId,qrFlag,redPoolId（空）,payPwd,")
I25_35("RtnParamErr", "10001588", "10001588", "1", "2", "3", "1", "0", "3101000000", "0", "31","0", data1[0], "","C35-8,userId,amount,count,payType,door,cityId,groupId,templateId,qrFlag,redPoolId,payPwd(错),")
print "36,================================================================================================="
#36红包列表_红包放入红包池、余额回收接口
#先生成一个广告红包做铺垫怕影响到别的接口
sleep(10)
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,推广来源,红包总金额,渠道推广图片ID,userid,品牌商户名称,红包总数量,door")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
#回收余额需要先修改红包主表updateTime
curT.execute('UPDATE t_extension_channel_redPool set updateTime=ADDDATE(NOW(),2) WHERE id=%s'%(data1[0]))
conn.commit()
#激活同城红包
I25_44("RtnOK", "10001588","C44-1")
#放入红包池目前不用测试了，下个版本没有了
I25_36("RtnOK", "10001588", "10001588","2",data1[0],"34","C36-1,userId,callBackType,redPoolId,redType")
I25_36("RtnParamErr", "10001588", "","2",data1[0],"34","C36-2,userId(空),callBackType,redPoolId,redType")
I25_36("RtnParamErr", "10001588", "10001588","",data1[0],"34","C36-2,userId,callBackType（空）,redPoolId,redType")
I25_36("RtnParamErr", "10001588", "10001588","9",data1[0],"34","C36-2,userId,callBackType（不在回收范围内的类型）,redPoolId,redType")
########别人的批次的ID问题以修复
I25_36("RtnParamErr", "10001588", "10001588","2","3485","34","C36-2,userId,callBackType,redPoolId（别人的批次ID）,redType")
I25_36("RtnParamErr", "10001588", "10001588","2","","34","C36-2,userId,callBackType,redPoolId(空),redType")
I25_36("RtnOK", "10001588", "10001588","2",data1[0],"33","C36-2,userId,callBackType,redPoolId,redType（不匹配用户批次的类型）")
print "37,================================================================================================="
#37我的_个人信息接口（新增返回值）
I25_37("RtnOK", "10001588", "10001588","10001877","1","C37-1,userId,visitUserId,isGroup")
I25_37("RtnOK", "10001588", "10001588","10001877","0","C37-2,userId,visitUserId,isGroup")
I25_37("RtnParamErr", "10001588", "","10001877","0","C37-3,userId（空）,visitUserId,isGroup")
I25_37("RtnParamErr", "10001588", "10001588","","0","C37-4,userId,visitUserId（空）,isGroup")
I25_37("RtnParamErr", "10001588", "10001588","10001877","","C37-5,userId,visitUserId,isGroup（空）")
print "38,================================================================================================="
#38首页_发红包_私信红包_发送私信红包接口
I25_38("RtnOK", "10001588", "10001588", "3", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-1,userId,payType,amount,""acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnDeviceErr", "10001588", "", "3", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-2,userId（空）,payType,amount,""acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "", "1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-3,userId,payType（空）,amount,""acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-4,userId,payType,amount（空）,acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "-1", "10001877", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-5,userId,payType,amount（负数）,acceptId,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "118", "10001588给10001588发送私信红包1", "111111", "",
       "C38-6,userId,payType,amount,acceptId（不是群成员）,groupId,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "", "10001588给10001588发送私信红包1", "111111", "",
       "C38-7,userId,payType,amount,acceptId,groupId（空）,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "119", "10001588给10001588发送私信红包1", "111111", "",
       "C38-8,userId,payType,amount,acceptId,groupId（不匹配的群ID）,content,payPwd,templateId ")

I25_38("RtnParamErr", "10001588", "10001588", "3", "1", "10002084", "119", "10001588给10001588发送私信红包1", "", "",
       "C38-9,userId,payType,amount,acceptId,groupId,content,payPwd(空),templateId ")
print "39,================================================================================================="
#39发送私信转帐接口
I25_39("RtnOK","10001588","10001588","3","1","10001877","118","10001588给10001877发送私信转账1元","111111",
       "C39-1,userId,payType,amount,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnDeviceErr", "10001588", "", "3", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId（空）,payType,amount,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId,payType（空）,amount,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId,payType,amount（空）,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "-1", "10001877", "118", "10001588给10001877发送私信转账1元", "111111",
       "C39-1,userId,payType,amount（负数）,acceptId,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "1", "10001588", "118", "10001588给10001588发送私信转账1元", "111111",
       "C39-1,userId,payType,amount,acceptId（不是群成员的成员）,groupId,content,payPwd,templateId ")

I25_39("RtnParamErr", "10001588", "10001588", "3", "1", "10001877", "118", "10001588给10001877发送私信转账1元", "",
       "C39-1,userId,payType,amount,acceptId,groupId,content,payPwd（错误）,templateId ")
print "40,================================================================================================="
#40分享红包_获取分享链接接口
sleep(10)
I25_33("RtnOK","10001588","10001588","1","2","3","1","0","3101000000","0","31","111111","0","C33-1,userId,amount,count,payType,door,""cityId,groupId,templateId,payPwd,redPoolId,")
conn = MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)  # sit2
curT = conn.cursor()
curT.execute('SELECT id from ukardweb.t_extension_channel_redPool WHERE  userId=10001588 and redType=34  ORDER BY id DESC LIMIT 0,1')
data1 = curT.fetchone()
curT.execute('SELECT pay_order_id  from ukardweb.t_user_withdraw WHERE user_id=10001588 and object_id=%s' %(data1[0]))
data2 = curT.fetchone()
conn.commit()
I25_40("RtnOK", "10001588", "10001588", "20", "7", "1", data1[0],"2" ,data2[0], "1","0",
       "C40-1,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnOK", "10001588", "10001588", "25", "7", "1", data1[0], "2", data2[0], "1", "0",
       "C40-2,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", data2[0], "1", "0",
       "C40-3,userId,shareType（不在范围内的类型）,platform,amount,tranId,channel,channelId,lvl,labelIds")


I25_40("RtnParamErr1", "10001588", "10001588", "60", "70", "1", data1[0], "2", data2[0], "1", "0",
       "C40-4,userId,shareType,platform（不在分享渠道内）,amount,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "", data1[0], "2", data2[0], "1", "0",
       "C40-5,userId,shareType,platform,amount（空）,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "-1", data1[0], "2", data2[0], "1", "0",
       "C40-6,userId,shareType,platform,amount（负数）,tranId,channel,channelId,lvl,labelIds")

I25_40("RtnOK", "10001588", "10001588", "20", "7", "1", "3547", "2", data2[0], "1", "0",
       "C40-4,userId,shareType,platform,amount,tranId（不是自己的批次）,channel,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "", data2[0], "1", "0",
       "C40-7,userId,shareType,platform,amount,tranId,channel（空）,channelId,lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "1", "0",
       "C40-8,userId,shareType,platform,amount,tranId,channel,channelId(不是自己的渠道ID),lvl,labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "3", "0",
       "C40-9,userId,shareType,platform,amount,tranId,channel,channelId,lvl(超过层级范围),labelIds")

I25_40("RtnSysErr", "10001588", "10001588", "60", "7", "1", data1[0], "2", "4618", "3", "",
       "C40-10,userId,shareType,platform,amount,tranId,channel,channelId,lvl,labelIds（空）")
print "41,================================================================================================="
# 41,首页_红包群_我的红包群_私信红包领取信息接口
I25_41("RtnParamErr","10001679","213","C41-1,redId")
print "42,================================================================================================="
# 42,红包群_我的红包群_新成员数量接口
I25_42("RtnOK","10001679","213","C42-1,groupId")
print "43,================================================================================================="
#43,批处理_分享至红包池_同城红包生成批处理接口
I25_43("RtnOK","10001679","C43-1")
print "44,================================================================================================="
# 44,批处理_广告红包分成_同城红包生成批处理接口
I25_44("RtnOK","10001588","C44-1")