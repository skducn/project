# coding: utf-8
#****************************************************************
# Author     : John
# Version    : 1.0.0
# Date       : 2016-5-27
# Description: TSZ alltable
#****************************************************************
import os,sys,unittest,MySQLdb,tempfile,shutil,platform,string,datetime,re,SendKeys
# import xlwt,xlrd,chardet,random,webbrowser,win32api,win32con,win32gui,
# import HTMLTestRunner,smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# from appium import webdriver
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
# sleepfrom xlwt.Style import *
# from xlrd import open_workbook
# from xlutils.copy import copy
# from PIL import Image

HeaduserID="10001679"   #13816109050

conn= MySQLdb.connect(host='192.168.2.176', user='ukaapp', passwd='ukaapp', db='ukardweb', port=3306, use_unicode=True)
cur = conn.cursor()
conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
# [1 渠道推广红包渠道记录表]
# id,userId=10001679,extensionRedPoolId=渠道推广红包池Id,channel=1外平台2抢红包3红包群4二维码,
# channelRedNumber=红包总数,channelRedNoLeadNumber=未领红包总数，channelRedSumAmout=红包总金额,channelRedAmout=红包单个金额,
# source=推广来源（1微信2支付宝3余额），cityId，redType=红包类型（21推广红包22推广短信红包26推广体验金红包），createTime,updateTime,
# redState=红包状态（1正常2回收3审核退回）
cur.execute('select * from t_extension_channel order by id desc limit 1')
data1 = cur.fetchone()
if data1[1]<>10001679:print "Err,1,t_extension_channel_redPool [last 1 is "+str(data1[1])+" ,not 10001679]"
else:print "Ok,1,t_extension_channel_redPool [last 1 is 10001679]"

# [2 渠道推广红包主表]
#   id,userId=10001679,redNumber=红包总数量',redLeadNumber=已领红包总数量',redNoLeadNumber=未领红包总数量',redGenerateNumber=已生成红包个数',
#   redType=红包类型(21:推广红包，22：推广短信红包，26：推广体验金红包)',
#   redState=红包状态 0:未分享,1:已分享,2:已过期,4:新建记录,5:未成功充值',
#   redSumAmount=红包总金额',extensionSub='推广内容',createTime,updateTime,cityId,source= '推广来源，1 微信，2 支付宝，3 余额',
#   transFee= '交易总费率',extensionUrl='渠道推广红包的推广链接',auditStatus='审核状态(0:审核通过,1:审核不过)',
#   refundAmount='退款金额',brandContent='品牌/商户名称',downloadCount='未登录用户点击下载数',openCount='红包打开次数',linkOpenCount= '图片链接打开次数',
#   type='0正常充值,1体验金,2大咖',surplusAmount= '剩余金额',
cur.execute('select * from t_extension_channel_redPool order by id desc limit 1')
data2 = cur.fetchone()
if data2[1]<>10001679:print "Err,2,t_extension_channel_redPool [last 1 is "+str(data2[1])+" ,not 10001679]"
else:print "Ok,2,t_extension_channel_redPool [last 1 is 10001679]"

# [3 红包池-外部红包池(主表)]
  # id,redAmount='红包金额',redType='红包类型  社交好友:16,体验金社交好友：27',
  # redNumber='红包总数量',redLeadNumber='已领红包总数量',redNoLeadNumber='未领红包总数量',
  # userid=10001679,tranid= '交易id',redState='红包状态 0.未激活1,已激活2.已过期3无效  4回收  5 :未分享  6: 未分享已过期',
  # payOutAmount='补贴金额 ', payInAmount='溢出金额 ',busiId='商户id',storeId='门店id',storeCityId='门店所属城市',createTime,updateTime,busiName='商户名称',storeName='门店名称',
  # tranAmount='交易金额',extensionId='推广红包ID',extensionType='推广红包类型(0:消费推广红包,1:用户推广红包)',
  # downloadCount='未登录用户点击下载数',openCount='红包打开次数',linkOpenCount='图片链接打开次数',
  # channelId ='渠道ID',batchId='批次ID',
cur.execute('select * from t_external_redPool order by id desc limit 1')
data3 = cur.fetchone()
if data3[6]<>10001679:print "Err,3,t_external_redPool [last 1 is "+str(data3[6])+" ,not 10001679]"
else:print "Ok,3,t_external_redPool [last 1 is 10001679]"

# [4 红包池-外部红包明细表]
#   id,redPoolId='红包池id',userId ='发红包者',redType='红包类型',belongId='红包所属人',storeId='门店id',busiId='商户id',storeCityId='门店所属城市',
#   redState='红包状态 1.未领2.占用3.已领4.平台回收,5.推广红包审核未通过',
#   amount='红包金额',createTime,updateTime
#   belongNam='领取人第三方名称',belongThumb='领取人第三方头像',
#   extensionId='推广红包ID',extensionType= '推广红包类型(0:消费推广红包,1:用户推广红包)',
#   experienceAmount='体验金',actualAmount='实际领到金额',channelId='渠道ID',batchId='批次ID',
#   channelType='渠道类型(1：外平台,3：红包群,4:二维码)',belongOpenId='领取人第三方标识ID',isLeadEnd'是否领完(0:未领完,1:领完)',
cur.execute('select * from t_external_redDetail  order by id desc limit 0,1')
data4 = cur.fetchone()
if data4[2]<>10001679:print "Err,4,t_external_redDetail [last 1 is "+str(data4[2])+" ,not 10001679]"
else:print "Ok,4,t_external_redDetail [last 1 is 10001679]"

# [5 红包池-内部红包池(主表)]
#   id,redAmount='红包金额',redType='红包类型  app好友:11  同城好友:14',
#   redNumber='红包总数量', redLeadNumber='已领红包总数量',redNoLeadNumber='未领红包总数量',
#   userid = '用户ID',tranid = '交易id',
#   redState ='红包状态 0.未激活1,已激活2.已过期3无效  4回收  5 :未分享  6: 未分享已过期',
#   payOutAmount ='补贴金额 ', payInAmount= '溢出金额 ', busiId='商户id',storeId = '门店id',storeCityId ='门店所属城市',createTime,updateTime
#   appRedPoolId ='APP好友红包池ID（只有同城红包池用到）',busiName= '商户名称',storeName= '门店名称',extensionId='推广红包ID',
#   extensionType= '推广红包类型(0:消费推广红包,1:用户推广红包)',channelId = '渠道ID',batchId = '批次ID',
cur.execute('select * from t_internal_redPool order by id desc limit 0,1')
data5 = cur.fetchone()
if data5[6]<>10001679:print "Err,5,t_internal_redPool [last 1 is "+str(data5[6])+" ,not 10001679]"

# [6 红包池-内部红包明细表]
#   id,redPoolId= '红包池id',userId = '发红包者',redType= '红包类型',belongId = '红包所属人',storeId =  '门店id',busiId = '商户id',storeCityId = '门店所属城市',
#   redState = '红包状态 1.未领2.占用3.已领4.平台回收,5.推广红包审核未通过',amount='红包金额',createTime,
#   appRedPoolId= 'APP好友红包池ID（只有同城红包池用到）',updateTimeextensionId= '推广红包ID',extensionType= '推广红包类型(0:消费推广红包,1:用户推广红包)',
#   channelId='渠道ID',batchId='批次ID',
cur.execute('select * from t_internal_redDetail order by id desc limit 0,1')
data6 = cur.fetchone()
if data6[2]<>10001679:print "Err,6,t_internal_redDetail [发红包: "+str(data6[2])+" ,红包接受转发:"+str(data6[4])+"]"

# [7 推广分成表,分享奖励红包]
#   id,userId='发红包者',userOpenId='发送人第三方ID',belongId='红包所属人',batchId = '批次ID ',channelId = '渠道ID', redId = '红包ID',
#   redAmount ='红包金额', redType= '红包类型',redState= '红包状态(1:激活状态,3:已领状态,4:审核不通过)',
#   belongOpenId = '领取人第三方标识ID',channel ='渠道 1 微信，2 qq，3 微博',createTime ,updateTime,belongName = '领取人名称',belongThumb = '领取人头像',
cur.execute('select * from t_extension_fallinto order by id desc limit 0,1')
data7 = cur.fetchone()
if data7[1]<>10001679:print "Err,7,t_extension_fallinto [发红包: "+str(data7[1])+" ,红包接受转发:"+str(data7[3])+"]"

# [8 第三方用户信息表]
#   id,userId = '用户id',belongName='第三方昵称',belongThumb = '第三方头像',
#   channel = '渠道，1 微信，2 qq，3 微博',isValid= '绑定标记，0 未绑定，1 已绑定',openid,token ,createTime
cur.execute('select userId from t_user_thirdInfo order by id desc limit 0,1') # 获取最后第二条的userId
data8 = cur.fetchone()
if data8[0]<>10001679:print "Err,8,t_user_thirdInfo [last 1 is "+str(data8[0])+" ,not 10001679]"
cur.execute('select userId from t_user_thirdInfo order by id desc limit 1,1') # 获取最后第一条的userId
data8 = cur.fetchone()
if data8[0]<>10001679:print "Err,8,t_user_thirdInfo [last 2 is "+str(data8[0])+" ,not 10001679]"

# [9 运营-审核消息任务表]
#   id,m_type= '消息类型',m_status= '0等待执行 1执行成功 2执行失败 其他json错误', m_content= '消息内容',oper_time = '操作时间',
#   m_from= '来源',ver = '版本',busi_id= '业务编号',result = '回执结果',from_id = '来源编号', msg_id = '信息标识',
#   phone = '用户手机号',verify_code = '动态验证码',
cur.execute('select verify_code from ta_message where phone="13816109050" order by id desc limit 1')
data9 = cur.fetchone()
print "Ok,9,ta_message,13816109050's verifycode is ["+str(data9[0])+"]"

# [10 用户管理-提现表]
#   id,user_id = '用户id',amount =  '提现金额',
#   charge = '手续费',w_state = '0 提现中 1 提现成功 2  提现失败 3 付款中',check_state = '0 提交审核 1 审核成功 2  审核失败 ', bank_num = '银行卡号',
#   card_id = '我的默认银行卡id',bank_name = '银行名称',account_name = '银行卡账户名',is_valid = '是否有效',create_time= '创建时间',audit_remark= '审核备注',
#   audit_name= '审核人姓名',audit_time ='审核时间',audit = '审核人id',payer_name = '付款人名字',pay_time = '付款时间',payer = '付款人id',pay_remark = '付款失败原因',
#   moneyType = '交易类型  26推广审核退回 27体验金推广发红 28大咖推广发红包 29大咖充值  30体验金审核退回  31 新用户体验金充值 32新用户体验金过期 33大咖充值过期',
#   pay_type = '交易类型（0.pos 1.微信 2.支付宝）',pay_order_id = 'app支付订单号',pay_id = '第三方支付id',time_end = '支付完成时间',object_id = '业务主键',
cur.execute('select user_id from t_user_withdraw order by id desc limit 0,1;')
data10 = cur.fetchone()
if data10[0]<>10001679:print "Err,10,t_user_withdraw [last 1 is "+str(data10[0])+" ,not 10001679]"


conn.commit()
cur.close()
conn.close()