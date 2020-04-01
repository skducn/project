# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author        : John
# Date          : 2016-11-8
# Description   : 场景鹿1.0接口测试用例
# reference     : CJLinterfaceDriver.py , CJLinterfaceParam.py
# 接口调用: Icase("参1","参2","参3", '"**参数4"')
# 参1 = 坐标定位,由三部分组成 "excel工作表_序号_用例编号" , 如"I251_N6_C1" 对应excel中工作表I251序号为6的测试用例1 .
# 参2 = 返回类型（如：RtnOK（正确返回），RtnSysErr（错误100001），RtnParamErr（错误100002），RtnDeviceErr（错误100003））
# 参3 = userID
# **参4 = 接口文档的请求参数列表 (各参数用逗号分隔,且最外层是单引号。)
#   情况1，有多个参数，写法如 '"userid","groupId","memberId"'
#   情况2，无参数，写法如 ''
#   情况3，只有1个参数则最后加上逗号，写法如 '"userid", '
# 例子:Icase("I251_N28_C1", "RtnOK", "10001482", '"13","10001577","1577店小二"')
# ********************************************************************************************************************************
from CJLinterfaceParam import *
from CJLinterfaceDriver import *
# *******************************************************************************************************************************


# [Testcase]
# 6,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 6,登录_获取验证码接口
print "\nCJL1_N6 " + ">" * 150
Icase("CJL1_N6_C1", "RtnOK", "123456789", '"%s","1"' %(myPhone))

# 7,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 7,登录接口 （依赖接口6）
print "\nCJL1_N7 " + ">" * 150
Icase("CJL1_N7_C1", "RtnOK", getCJLverifyCode(myPhone), '"%s","0","%s","%s","0","0"' % (myPhone, cityID, getCJLverifyCode(myPhone)))
redisCheckuser = connRedis167.exists("login:app:user:" + myPhone)
if redisCheckuser: redisTmpuserid = connRedis167.hget("login:app:user:" + myPhone, "userId")
else: redisTmpuserid = connRedis167.hget("login:tmpuser:" + myPhone, "userId")

# 8,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 8,用户信息修改接口（依赖接口7）
print "\nCJL1_N8 " + ">" * 150
Icase("CJL1_N8_C1", "RtnOK", redisTmpuserid, '"1","%s","%s","%s","%s"' % (headPic, nickName, sign, cityID))
# 检查 t_user_setting(用户设置表), 新增1条记录
curPersonal.execute('select isAddAuth,openDisturb,isAcceptNotice,isShowDetail,openSound,openVibration,openStealth,isValid from t_user_setting where id=%s order by id desc limit 1' % (getCJLuserID(myPhone)))
tbl8 = curPersonal.fetchall()
connPersonal.commit()
var8 = "t_user_setting , id = " + str(getCJLuserID(myPhone)) + "isAddAuth = 1 , openDisturb = 0 , isAcceptNotice = 1 , isShowDetail = 1 , openSound = 1 , openVibration = 1 , openStealth = 0 , isValid = 1]"
assertEqual(str(tbl8[0]), "(1, 0, 1, 1, 1, 1, 0, 1)", "[OK , " + var8, "[errorrrrrrrrrr , " + var8)
print "\nuserId = " + str(getCJLuserID(myPhone))
# tmp8 = curPersonal.execute('select id from t_user_setting where id=%s order by id desc limit 1' % (getCJLuserID(myPhone)))
# connPersonal.commit()
# var8 = "t_user_setting , 新增一条记录]"
# assertEqual(tmp8, 1, "[OK , " + var8, "[errorrrrrrrrrr , " + var8)


# 34,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 34,我的_扫码加好友接口
print "\nCJL1_N34 " + ">" * 150
# 影响表(t_user_friends , t_user_friends_apply），重复新增好友不报错
# 新增2条记录（主动邀请，被邀请）
varcontent = "加我好友吧？"
Icase("CJL1_N34_C1", "RtnOK", getCJLuserID(myPhone), '"%s","0","%s","%s"' % (friendID1, varcontent, cityID))
sleep(4)
# 检查 t_user_friends, 新增2条邀请与被邀请记录。(friendID1 是需验证用户，因此检查 status=0、isFriend=0)
tmp1 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=0 and isfrom=1 and isFriend=0 order by id desc limit 1' % (getCJLuserID(myPhone), friendID1))
tmp2 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=0 and isfrom=0 and isFriend=0 order by id desc limit 1' % (friendID1, getCJLuserID(myPhone)))
sleep(2)
var1 = "t_user_friends , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID1) + " , status = 0 , isfrom = 1 , isFriend = 0]  # 新增"
var2 = "t_user_friends , userId = " + str(friendID1) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , status = 0 , isfrom = 0 , isFriend = 0]  # 新增"
assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)
assertEqual(tmp2, 1, "[OK , " + var2, "[errorrrrrrrrrr , " + var2)
# 检查 t_user_friends_apply ,新增1条申请消息。
curPersonal.execute('select id,userId,acceptId,channel,status,isValid from t_user_friends_apply where userId = %s and acceptId = %s and content = "%s" order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, varcontent))
tbl34 = curPersonal.fetchall()
connPersonal.commit()
var34 = "t_user_friends_apply , id = " + str(tbl34[0][0]) + " , userId = " + str(tbl34[0][1])+ " , acceptId = " + str(tbl34[0][2])+ " , channel = " + str(tbl34[0][3]) + " , status = " + str(tbl34[0][4]) + " , isValid = "+ str(tbl34[0][5]) + "] # 新增"
assertEqual(str(tbl34[0]), "("+str(tbl34[0][0])+"L, "+getCJLuserID(myPhone)+"L, "+friendID1+"L, 0, 0, 1)", "[OK , " + var34, "[errorrrrrrrrrr , " + var34)

# 新增4个好友(friendID2-friendID5都是免验证用户，因此检查 status=1、isFriend=1))
Icase("CJL1_N34_C2", "RtnOK", getCJLuserID(myPhone), '"%s","1","%s","%s"' %(friendID2, varcontent, cityID))
sleep(4)
tmp1 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 1 and isfrom=1  and isFriend=1 order by id desc limit 1' % (getCJLuserID(myPhone), friendID2))
tmp2 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 1 and isfrom=0  and isFriend=1 order by id desc limit 1' % (friendID2, getCJLuserID(myPhone)))
connPersonal.commit()
var1 = "t_user_friends , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID2) + " , status = 1 , channel = 1 , isfrom = 1 , isFriend = 1]  # 新增"
var2 = "t_user_friends , userId = " + str(friendID2) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , status = 1 , channel = 1 , isfrom = 0 , isFriend = 1]  # 新增"
assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)
assertEqual(tmp2, 1, "[OK , " + var2, "[errorrrrrrrrrr , " + var2)

Icase("CJL1_N34_C3", "RtnOK", getCJLuserID(myPhone), '"%s","2","%s","%s"' %(friendID3, varcontent, cityID))
sleep(4)
tmp1 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 2 and isfrom=1  and isFriend=1 order by id desc limit 1' % (getCJLuserID(myPhone), friendID3))
tmp2 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 2 and isfrom=0  and isFriend=1 order by id desc limit 1' % (friendID3, getCJLuserID(myPhone)))
connPersonal.commit()
var1 = "t_user_friends , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID3) + " , status = 1 , channel = 2 , isfrom = 1 , isFriend = 1]  # 新增"
var2 = "t_user_friends , userId = " + str(friendID3) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , status = 1 , channel = 2 , isfrom = 0 , isFriend = 1]  # 新增"
assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)
assertEqual(tmp2, 1, "[OK , " + var2, "[errorrrrrrrrrr , " + var2)

Icase("CJL1_N34_C4", "RtnOK", getCJLuserID(myPhone), '"%s","3","%s","%s"' %(friendID4, varcontent, cityID))
sleep(4)
tmp1 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 3 and isfrom=1  and isFriend=1 order by id desc limit 1' % (getCJLuserID(myPhone), friendID4))
tmp2 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 3 and isfrom=0  and isFriend=1 order by id desc limit 1' % (friendID4, getCJLuserID(myPhone)))
connPersonal.commit()
var1 = "t_user_friends , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID4) + " , status = 1 , channel = 3 , isfrom = 1 , isFriend = 1]  # 新增"
var2 = "t_user_friends , userId = " + str(friendID4) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , status = 1 , channel = 3 , isfrom = 0 , isFriend = 1]  # 新增"
assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)
assertEqual(tmp2, 1, "[OK , " + var2, "[errorrrrrrrrrr , " + var2)

Icase("CJL1_N34_C5", "RtnOK", getCJLuserID(myPhone), '"%s","4","%s","%s"' %(friendID5, varcontent, cityID))
tmp1 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 4 and isfrom=1  and isFriend=1 order by id desc limit 1' % (getCJLuserID(myPhone), friendID5))
tmp2 = curPersonal.execute('select id from t_user_friends where userId = %s and friendUserId = %s and status=1 and channel= 4 and isfrom=0  and isFriend=1 order by id desc limit 1' % (friendID5, getCJLuserID(myPhone)))
connPersonal.commit()
var1 = "t_user_friends , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID5) + " , status = 1 , channel = 4 , isfrom = 1 , isFriend = 1]  # 新增"
var2 = "t_user_friends , userId = " + str(friendID5) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , status = 1 , channel = 4 , isfrom = 0 , isFriend = 1]  # 新增"
assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)
assertEqual(tmp2, 1, "[OK , " + var2, "[errorrrrrrrrrr , " + var2)

# 84,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 84，好友_同意好友申请接口
print "\nCJL1_N84 " + ">" * 150
Icase("CJL1_N84_C1", "RtnOK", getCJLverifyCode(myPhone), '"%s","%s"' % (friendID1, getCJLuserID(myPhone)))
sleep(4)
# 检查 t_user_friends, status=1 ，isfriend=1
curPersonal.execute('select id,userId,friendUserId,status,isFriend from t_user_friends where userId = %s and friendUserId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1))
tbl84 = curPersonal.fetchall()
connPersonal.commit()
var84 = "t_user_friends , id = " + str(tbl84[0][0]) + " , userId = " + str(tbl84[0][1]) + " , friendUserId = " + str(tbl84[0][2]) + " , status = " + str(tbl84[0][3]) + " , isFriend = " + str(tbl84[0][4]) + "] # 修改"
assertEqual(str(tbl84[0]), "("+str(tbl84[0][0])+"L, "+getCJLuserID(myPhone)+"L, "+friendID1+"L, 1, 1)", "[OK , " + var84, "[errorrrrrrrrrr , " + var84)

# 40,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 40，私聊_通讯录_新建标签接口
# 此接口完成了2件事：1、t_user_label表当前用户新增一个标签；2、t_user_label_memberinfo表当前用户的好友friend1加入标签
print "\nCJL1_N40 " + ">" * 150
# 单标签名
varlabelName401 = "fourZeroOne" + randomDigits(4)
labelID1 = Icase("CJL1_N40_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' % (varlabelName401, friendID1))  # 新增标签（标签名称唯一）
# 检查 t_user_label, 新增1条记录
tmp401 = curPersonal.execute('select id from t_user_label where userId=%s and id=%s and userNumber=1 order by id desc limit 1' % (getCJLuserID(myPhone), int(labelID1)))
var401 = "t_user_label , id = " + str(labelID1) + " , userId = " + str(getCJLuserID(myPhone)) + " , userNumber = 1]  # 新增"
assertEqual(tmp401, 1, "[OK , " + var401, "[errorrrrrrrrrr , " + var401)
connPersonal.commit()
# 检查 t_user_label_memberinfo, 新增1条记录
tmp402 = curPersonal.execute('select id from t_user_label_memberinfo where userId=%s and friendUserId=%s and labelId=%s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, int(labelID1)))
var402 = "t_user_label_memberinfo , id = " + str(labelID1) + " , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID1) + " , labelId = " + str(labelID1) + "]  # 新增"
assertEqual(tmp402, 1, "[OK , " + var402, "[errorrrrrrrrrr , " + var402)
connPersonal.commit()

print "\nlabelID1 = " + str(labelID1)

# 61,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 61,私聊_通讯录_修改标签成员接口 (依赖 接口34、40)
# 业务场景：成员必须是当前用户的好友，其次标签是当前用户的标签。
print "\nCJL1_N61 " + ">" * 150

# 修改+新增，修改原标签名，并将1个朋友添加到此标签下为成员标签 (不能重复添加)
# 1,t_user_label，将当前用户原{labelId1}的标签名改为{varlabelName611},且userNumber+1
# 2,t_user_label_memberinfo，新增friend2为当前用户的标签成员，
varlabelName611 = "sixOneOne" + randomDigits(4)  # 标签名
Icase("CJL1_N61_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' %(str(labelID1), friendID2, varlabelName611))

# 检查 t_user_label 的 userNumber=2 、 labelName={varlabelName611}
curPersonal.execute('select userId,labelName,userNumber from t_user_label where id=%s order by id desc limit 1' % (int(labelID1)))
tbl611 = curPersonal.fetchall()
connPersonal.commit()
var611 = "t_user_label , id = " + str(labelID1) + " , userId = " + str(getCJLuserID(myPhone)) + " , labelName = " + varlabelName611 + " , userNumber = " + str(tbl611[0][2]) + "]  # 修改"
tmp611 = long(str(getCJLuserID(myPhone))), unicode(varlabelName611), long(str(tbl611[0][2]))
assertEqual(list(tbl611[0]), list(tmp611), "[OK , " + var611, "[errorrrrrrrrrr , " + var611)

# 检查 t_user_label_memberinfo , 新增1条记录
curPersonal.execute('select id,userId,friendUserId,labelId from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID2, int(labelID1)))
tbl612 = curPersonal.fetchall()
connPersonal.commit()
var612 = "t_user_label_memberinfo , id = " + str(tbl612[0][0]) + " , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID2) + " , labelId = " + str(labelID1) + "]  # 新增"
tmp612 = long(str(tbl612[0][0])), long(str(getCJLuserID(myPhone))), long(str(friendID2)), long(str(labelID1))
assertEqual(list(tbl612[0]), list(tmp612), "[OK , " + var612, "[errorrrrrrrrrr , " + var612)

# 将2个朋友添加到标签下，且标签名不修改(varlabelName611)
x = friendID3 + "," + friendID4
Icase("CJL1_N61_C2", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' %(str(labelID1), x, varlabelName611))  # 新建
#
# # 检查 t_user_label  的 userNumber=4 与 labelName={varlabelName611}
# curPersonal.execute('select id from t_user_label where userId=%s and id=%s and userNumber=3 and labelName = "%s" order by id desc limit 1' % (getCJLuserID(myPhone),int(labelID2), varlabelName401))
# varN61C2_4 = "t_user_label , id = " + str(labelID2) + " , userId = " + str(getCJLuserID(myPhone)) + " , userNumber = 3 , labelName = " + varlabelName401 + "]  # 修改"
# assertEqual(N61C2_4, 1, "[OK , " + varN61C2_4, "[errorrrrrrrrrr , " + varN61C2_4)
# connPersonal.commit()

# 检查 t_user_label 的 userNumber+4 、 labelName={varlabelName611}
curPersonal.execute('select userNumber from t_user_label where id=%s order by id desc limit 1' % (int(labelID1)))
tbl613 = curPersonal.fetchall()
connPersonal.commit()
var613 = "t_user_label , id = " + str(labelID1) + " , userId = " + str(getCJLuserID(myPhone)) + " , labelName = " + varlabelName611 + " , userNumber = " + str(tbl613[0][0]) + "]  # 修改"
assertEqual(tbl613[0][0], 4, "[OK , " + var613, "[errorrrrrrrrrr , " + var613)

# 检查 t_user_label_memberinfo , 新增2条记录
N61C2_2 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID3, int(labelID1)))
N61C2_3 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID4, int(labelID1)))
varN61C2_2 = "t_user_label_memberinfo , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID3) + " , labelId = " + str(labelID1) + "]  # 新增2"
assertEqual(N61C2_2, 1, "[OK , " + varN61C2_2, "[errorrrrrrrrrr , " + varN61C2_2)
varN61C2_3 = "t_user_label_memberinfo , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID4) + " , labelId = " + str(labelID1) + "]  # 新增3"
assertEqual(N61C2_3, 1, "[OK , " + varN61C2_3, "[errorrrrrrrrrr , " + varN61C2_3)
connPersonal.commit()

# 42,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 私聊_通讯录_删除标签接口
# 删除当前用户的标签及所有的用户标签成员
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID1))
sleep(4)

# 检查 t_user_label, 删除所有标签
N42C1 = curPersonal.execute('select id from t_user_label where userId=%s and id=%s order by id desc limit 1' % (getCJLuserID(myPhone), labelID1))
varN42C1 = "t_user_label , userId = " + str(getCJLuserID(myPhone)) + "]  # 已删除"
assertEqual(N42C1, 0, "[OK , " + varN42C1, "[errorrrrrrrrrr , " + varN42C1)
connPersonal.commit()
# 检查 t_user_label_memberinfo
N42C1 = curPersonal.execute('select id from t_user_label_memberinfo where userId=%s and labelId=%s order by id desc limit 1' % (getCJLuserID(myPhone), labelID1))
varN42C1 = "t_user_label_memberinfo , userId = " + str(getCJLuserID(myPhone)) + "]  # 已删除"
assertEqual(N42C1, 0, "[OK , " + varN42C1, "[errorrrrrrrrrr , " + varN42C1)
connPersonal.commit()


# 62,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 62,私聊_通讯录_修改单个用户标签接口
# 业务场景：单个用户必须是当前用户的好友，标签是当前用户的标签。
# 涉及表 t_user_friends , t_user_label_memberinfo
print "\nCJL1_N62 " + ">" * 150
varlabelName621 = "思考" + randomDigits(4)
varlabelName622 = "名誉" + randomDigits(4)
varlabelNames = varlabelName621 + "," + varlabelName622  # 多个标签名

# 1-4，新增2个标签（t_user_label），新增2条 用户标签成员（t_user_label_memberinfo），（标签名不能重复）
Icase("CJL1_N62_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s",""' % (friendID1, varlabelNames))    # 新建多标签,多个用户标签成员
sleep(4)
# 检查 t_user_label ,2条记录
tmp1 = curPersonal.execute('select id from t_user_label where userId = %s and labelName = "%s" and userNumber=1 order by id desc limit 1' % (getCJLuserID(myPhone), varlabelName621))
if tmp1 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    labelID1 = tbl62[0]
else:labelID1 = 0
var1 = "t_user_label , id = " + str(labelID1) + " , userId = " + str(getCJLuserID(myPhone)) + " , labelName = " + str(varlabelName621) + "]  # 新增"
assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)

tmp2 = curPersonal.execute('select id from t_user_label where userId = %s and labelName = "%s" and userNumber=1 order by id desc limit 1' % (getCJLuserID(myPhone), varlabelName622))
if tmp2 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    labelID2 = tbl62[0]
else:labelID2 = 0
var2 = "t_user_label , id = " + str(labelID2) + " , userId = " + str(getCJLuserID(myPhone)) + " , labelName = " + str(varlabelName622) + "]  # 新增"
assertEqual(tmp2, 1, "[OK , " + var2, "[errorrrrrrrrrr , " + var2)
# 检查 t_user_label_memberinfo，2条记录
tmp3 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId=%s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, labelID1))
if tmp3 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    id3 = tbl62[0]
else: id3 = "?"
var3 = "t_user_label_memberinfo , id = " + str(id3) + " , userId = " + str(friendID1) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , labelId = " + str(labelID1) + "]  # 新增"
assertEqual(tmp3, 1, "[OK , " + var3, "[errorrrrrrrrrr , " + var3)
tmp4 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId=%s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, labelID2))
if tmp4 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    id4 = tbl62[0]
else: id4 = "?"
var4 = "t_user_label_memberinfo , id = " + str(id4) + " , userId = " + str(friendID1) + " , friendUserId = " + str(getCJLuserID(myPhone)) + " , labelId = " + str(labelID2) + "]  # 新增"
assertEqual(tmp4, 1, "[OK , " + var4, "[errorrrrrrrrrr , " + var4)

# 2-4，新增1个标签（t_user_label），新增1条 用户标签成员（t_user_label_memberinfo），（标签名不能重复）
varlabelName = "newOne" + randomDigits(4)  # 单标签名

Icase("CJL1_N62_C2", "RtnOK", getCJLuserID(myPhone), '"%s","%s",""' % (friendID2, varlabelName))    # 新建单标签，单个用户标签成员
sleep(4)
# 检查 t_user_label
tmp1 = curPersonal.execute('select id from t_user_label where userId = %s and labelName = "%s" and userNumber=1 order by id desc limit 1' % (getCJLuserID(myPhone), varlabelName))
if tmp1 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    labelID6 = tbl62[0]
# ？检查 t_user_label_memberinfo

# 3-4，新增2条 用户标签成员（t_user_label_memberinfo），（业务上，标签id应该是当前用户创建过的标签）
varlabelName621 = "newTwo" + randomDigits(4)  # 单标签名
varlabelName622 = "newThree" + randomDigits(4)  # 单标签名

labelID3 = Icase("CJL1_N40_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' % (varlabelName621, friendID3))
sleep(4)
labelID4 = Icase("CJL1_N40_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' % (varlabelName622, friendID4))
sleep(4)
labelIDs = str(labelID3) + "," + str(labelID4)

Icase("CJL1_N62_C3", "RtnOK", getCJLuserID(myPhone), '"%s","","%s"' % (friendID1, labelIDs))    # 新建多个用户标签成员
sleep(4)
# 检查 t_user_label_memberinfo, 2条记录
tmp3 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, labelID3))
if tmp3 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    id5 = tbl62[0]
else: id5 = "?"
var3 = "t_user_label_memberinfo , id = " + str(id5) + " , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID1) + " , labelId = " + str(labelID3) + "]  # 新增"
assertEqual(tmp3, 1, "[OK , " + var3, "[errorrrrrrrrrr , " + var3)
tmp4 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, labelID4))
if tmp4 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    id6 = tbl62[0]
else: id6 = "?"
var4 = "t_user_label_memberinfo , id = " + str(id6) + " , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID1) + " , labelId = " + str(labelID4) + "]  # 新增"
assertEqual(tmp4, 1, "[OK , " + var4, "[errorrrrrrrrrr , " + var4)

varlabelName3 = "newFour" + randomDigits(4)  # 单标签名
labelID5 = Icase("CJL1_N40_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(varlabelName3, friendID5))
sleep(4)

# 4-4，新增1条 用户标签成员（t_user_label_memberinfo），（业务上，标签id应该是当前用户创建过的标签）
Icase("CJL1_N62_C4", "RtnOK", getCJLuserID(myPhone), '"%s","","%s"' %(friendID1,labelID5))    # 新建1个用户标签成员
sleep(4)
# 检查 t_user_label_memberinfo, 1条记录
tmp5 = curPersonal.execute('select id from t_user_label_memberinfo where userId = %s and friendUserId = %s and labelId = %s order by id desc limit 1' % (getCJLuserID(myPhone), friendID1, labelID5))
if tmp5 == 1:
    tbl62 = curPersonal.fetchone()
    connPersonal.commit()
    id7 = tbl62[0]
else: id7 = "?"
var5 = "t_user_label_memberinfo , id = " + str(id7) + " , userId = " + str(getCJLuserID(myPhone)) + " , friendUserId = " + str(friendID1) + " , labelId = " + str(labelID5) + "]  # 新增"
assertEqual(tmp5, 1, "[OK , " + var5, "[errorrrrrrrrrr , " + var5)

Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID1))
sleep(4)
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID2))
sleep(4)
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID4))
sleep(4)
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID5))
sleep(4)

# 1,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1,首页_创建公共场景_查询5公里内相同场景名称的接口
print "\nCJL1_N1 " + ">" * 150
Icase("CJL1_N1_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","%s"' %(lon,lat,comSceneName,cityID))
# 2,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 2,首页_创建公共场景接口
# 依赖于CJL1_N1_C1，且2个脚本中 sceneName 必须一致。
# 参数说明：
# 分类id = 100004 （学校）， 区id = 310101 （黄浦区）， 商圈id = 13658（新天地）
# 经纬度定位的地址是"天山路641号" ， 百度坐标：121.401307,31.218743 ，gps坐标：121.4013090000，31.2188120000
# mongdb验证是否创建成功，如：db.sceneDto.find({"_id":"G_10000006"})
print "\nCJL1_N2 " + ">" * 150
comID = Icase("CJL1_N2_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","%s","%s","100004","310101","13658","%s","%s","%s","%s"' %(lon,lat,gpslon,gpslat,getCJLuserID(myPhone),comSceneAddress,comSceneName,headPic,cityID))
# 验证mongdb中是否存在公共场景名和公共场景地址,输出返回值。
# 正确返回结果：[OK , mongdb , G_10000152 , sceneName = 我的公共场景1642 , address = 我的公共场景地址是1642]
(mdbcomSceneName, mdbcomSceneAddress) = getCJLsceneDto_310101_info(comID)
if mdbcomSceneName == comSceneName and mdbcomSceneAddress == comSceneAddress: print "[OK , mongdb , " + comID + " , sceneName = " + comSceneName + " , address = " + comSceneAddress + "]"
else: print "[errorrrrrrr , mongdb , " + comID + " , sceneName = " + comSceneName + " , address = " + comSceneAddress + "]"
print "\n" + comID


# 5,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 5,首页_更多场景接口
print "\nCJL1_N5 " + ">" * 150
Icase("CJL1_N5_C1", "RtnOK", getCJLuserID(myPhone), '"%s","0","20","%s"' %(comID,cityID))

# 9,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 9,我的_获取用户设置信息接口
print "\nCJL1_N9 " + ">" * 150
Icase("CJL1_N9_C1", "RtnOK", getCJLuserID(myPhone), '"1", ')

# 10,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 10,我的_设置_修改用户设置信息接口
print "\nCJL1_N10 " + ">" * 150
Icase("CJL1_N10_C1", "RtnOK", getCJLuserID(myPhone), '"0","0","8:00","12:00","0","0","0","0","0"')

# 11,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 11,我的_获取(我的个人信息/详情)接口
print "\nCJL1_N11 " + ">" * 150
Icase("CJL1_N11_C1", "RtnOK", getCJLuserID(myPhone), '')

# 12,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 12,场景_创建分场景接口
# 依赖于CJL1_N2_C1
# 分类大类：sysparam - t_dict_industry Ilevel=1的 id
# 分类小类：sysparam - t_dict_industry Ilevel=2的 id
print "\nCJL1_N12 " + ">" * 150
splitID = Icase("CJL1_N12_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","%s","100000","100001","%s"' %(getCJLuserID(myPhone),comID,splitSceneName,splitScenePic,cityID))
print "\n" + splitID
# 结果：{"data":"F_10000004","errorstr":"","errorcode":0,"success":true}


# 3,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 3,首页_场景列表接口
# 查询条件：依据查询类型而定，如 查询类型是附近，那么条件就是多少米；商圈对应的是多少米，在场人数最多对应的人数；在场美女、帅哥最多没有对应的条件。
print "\nCJL1_N3 " + ">" * 150
# ？？？
Icase("CJL1_N3_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","1","100","0","100000","0","父ID","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C2", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","1","100","1","西餐","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C3", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","1","100","2","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C4", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","1","100","3","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C5", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","1","100","4","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
#
Icase("CJL1_N3_C6", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2","田林","0","100004","0","父id","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C7", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2","田林","1","西餐","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C8", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2","田林","2","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C9", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2","田林","3","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C10", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2","田林","4","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
#
Icase("CJL1_N3_C11", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","3","310101","0","100004","0","父ID","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C12", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","3","310101","1","西餐4","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C13", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","3","310101","2","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C14", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","3","310101","3","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))
Icase("CJL1_N3_C15", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","3","310101","4","00","1","00","0","20","%s","310101"' %(lon, lat, cityID))

# 4,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 4,首页_搜索场景接口
# 场景ID需从mongdb,sceneDto,_id
print "\nCJL1_N4 " + ">" * 150
# Icase("CJL1_N4_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","1","%s","0","父ID","0","20","%s"' %(lon,lat,comSceneName,cityID))
# Icase("CJL1_N4_C2", "RtnOK", getCJLuserID(myPhone), '"%s","%s","1","%s","1","00","0","20","%s"' %(lon,lat,comSceneName,cityID))
# # CJL1_N4_C2接口需要在创建分场景后执行。
# # Icase("CJL1_N4_C2", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2","%s","0","20","%s"' %(lon,lat,splitSceneName,cityID))
# Icase("CJL1_N4_C3", "RtnOK", getCJLuserID(myPhone), '"%s","%s","3","%s","0","20","%s"' %(lon,lat,getCJLsceneDto_310100_id(getCJLuserID(myPhone)),cityID))  #场景ID号


# 13,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 13,场景_获得公共场景内容接口
print "\nCJL1_N13 " + ">" * 150
Icase("CJL1_N13_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' %(comID,getCJLuserID(myPhone),cityID))

# 14,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 14,场景_收藏公共场景接口
print "\nCJL1_N14 " + ">" * 150
Icase("CJL1_N14_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' %(comID,getCJLuserID(myPhone),cityID))

# 15,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 15,场景_查询我的场景接口
print "\nCJL1_N15 " + ">" * 150
Icase("CJL1_N15_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(getCJLuserID(myPhone),cityID))

# 16,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 16,足迹_保存足迹接口
print "\nCJL1_N16 " + ">" * 150
Icase("CJL1_N16_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' %(comID,getCJLuserID(myPhone),cityID))

# 17,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 17,足迹_退出场景保存足迹接口
print "\nCJL1_N17 " + ">" * 150
Icase("CJL1_N17_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(comID,getCJLuserID(myPhone)))

# 18,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 18,足迹_查询足迹接口
print "\nCJL1_N18 " + ">" * 150
Icase("CJL1_N18_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","1","0","1","0","20"' %(comID,getCJLuserID(myPhone)))
sleep(2)

# 21,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 21,[非]好友主页_拉入黑名单（好友主页/加入黑名单）接口
print "\nCJL1_N21 " + ">" * 150
Icase("CJL1_N21_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(friendID1))

# 19,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 19,我的_黑名单列表(我的隐私/黑名单)接口
# 先加入一个到黑名单？
print "\nCJL1_N19 " + ">" * 150
Icase("CJL1_N19_C1", "RtnOK", getCJLuserID(myPhone), '"0","1"')

# 20,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 20,我的_移除黑名单(我的隐私/黑名单)接口
# personal - t_user_friends - userID 对应的 friendUserId 10000012 , status由3变为-1 ，因此需要确保有status=3的记录。
print "\nCJL1_N20 " + ">" * 150
Icase("CJL1_N20_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(friendID1))

# 23,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 23,查看好友主页/相册_投诉好友/相册接口
# 1.好友投诉 2.相册投诉
print "\nCJL1_N23 " + ">" * 150
Icase("CJL1_N23_C1", "RtnOK", getCJLuserID(myPhone), '"我投诉内容是123","1","%s","%s"' %(friendID1, cityID))
# Icase("CJL1_N23_C2", "RtnOK", getCJLuserID(myPhone), '"我投诉内容是456","2","?"')  相册ID如何获取？

# 22,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 22,好友主页_删除好友（好友主页/删除）接口
print "\nCJL1_N22 " + ">" * 150
Icase("CJL1_N22_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(friendID1))


# 24,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 24,我的_设置_关于我们_意见反馈
# 来源（1.IOS 2.Android）
print "\nCJL1_N24 " + ">" * 150
Icase("CJL1_N24_C1", "RtnOK", getCJLuserID(myPhone), '"我的反馈是abc","1","%s"' %(cityID))
Icase("CJL1_N24_C2", "RtnOK", getCJLuserID(myPhone), '"我的反馈是def","2","%s"' %(cityID))

# 25,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 25,初始化_用户获取长连接IP接口
print "\nCJL1_N25 " + ">" * 150
Icase("CJL1_N25_C1", "RtnOK", "10000003", '')
# http://192.168.2.113:8080/sceneMsg/initAction/1.0/initHost.do
# https://cjl.dailylife365.com/sceneMsg/initAction/1.0/initHost.do

# 26 - 33 是请求json

# 87,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 87，场景_分场景_邀请好友加入场景接口
# 好友数组参数json格式.如:["1000001","1000002"])
# 用例：当前 用户 邀请  10000018 加入 自己的分场景
# 前置条件：先加好友，34接口，84接口确认，如 加10000018好友 ，并邀请10000018加入场景
print "\nCJL1_N87 " + ">" * 150
string1 = '["' + friendID2 + '"]'
print string1
Icase("CJL1_N87_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' % (splitID,str(eval(string1)).replace("'","\\\""),cityID))

# 85,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 85，我的场景_场景通知_同意邀请加入场景接口
# 依赖于 CJL1_N87_C1
# 业务逻辑：当前用户邀请 18918814232用户（10000018），18918814232用户登录后同意邀请。
# 前置条件：被邀请用户登录 18918814232账号登录，接口85同意邀请，
print "\nCJL1_N85 " + ">" * 150
myPhone19 = "17000000029"  # 被邀请用户
Icase("CJL1_N6_C1", "RtnOK", "1234567890", '"%s","1"' % (myPhone19))   # 18918814232手机号对应userid是 10000018
Icase("CJL1_N7_C1", "RtnOK", getCJLverifyCode(myPhone19), '"%s","0","%s","%s"' %(myPhone19, cityID, getCJLverifyCode(myPhone19)))
Icase("CJL1_N85_C1", "RtnOK", getCJLuserID(myPhone19), '"%s","%s"' %(splitID, cityID))



# 35,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 35,我的_我创建的场景列表接口
print "\nCJL1_N35 " + ">" * 150
Icase("CJL1_N35_C1", "RtnOK", getCJLuserID(myPhone), '"0","20","%s"' %(cityID))

# 36,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 36,我的_通讯录列表接口
print "\nCJL1_N36 " + ">" * 150
Icase("CJL1_N36_C1", "RtnOK", getCJLuserID(myPhone), '"0","20"')

# 37,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 37,我的_通讯录更新数据列表接口
print "\nCJL1_N37 " + ">" * 150
Icase("CJL1_N37_C1", "RtnOK", getCJLuserID(myPhone), '"0","2016-11-14"')

# 38,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 38,我的_我的场景足迹列表接口
print "\nCJL1_N38 " + ">" * 150
Icase("CJL1_N38_C1", "RtnOK", getCJLuserID(myPhone), '"0","20","%s"' %(cityID))

# 39,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 39，私聊_通讯录_标签列表接口
print "\nCJL1_N39 " + ">" * 150
Icase("CJL1_N39_C1", "RtnOK", getCJLuserID(myPhone), '')

# 40,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 40，私聊_通讯录_新建标签接口
# 涉及表 t_user_label
print "\nCJL1_N40 " + ">" * 150
# 新增1个标签1个用户
varlabelName = "test" + randomDigits(4)  # 单标签名
labelID5 = Icase("CJL1_N40_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(varlabelName, friendID5))  # labelID是unicode
print "\nlabelID = " + str(labelID5) + "\n"
# 检查 t_user_label, 新增1条记录
N40C1 = curPersonal.execute('select id from t_user_label where userId=%s and id=%s and userNumber=1 order by id desc limit 1' % (getCJLuserID(myPhone),int(labelID5)))
varN40C1 = "t_user_label , id = " + str(labelID5) + " , userId = " + str(getCJLuserID(myPhone)) + " , userNumber = 1]  # 新增"
assertEqual(N40C1, 1, "[OK , " + varN40C1, "[errorrrrrrrrrr , " + varN40C1)
connPersonal.commit()
sleep(3)

# 新增1个标签3个用户
labelName = "john多人" + randomDigits(4)  # 标签名不能重复，需重新生成
labelID3 = Icase("CJL1_N40_C2", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(labelName, friendID1 +","+friendID2+","+friendID3))
# 检查 t_user_label, 新增1条记录，userNumber=3
N40C2 = curPersonal.execute('select id from t_user_label where userId=%s and id=%s and userNumber=3 order by id desc limit 1' % (getCJLuserID(myPhone),int(labelID3)))
varN40C2 = "t_user_label , id = " + str(labelID3) + " , userId = " + str(getCJLuserID(myPhone)) + " , userNumber = 3]  # 新增"
assertEqual(N40C2, 1, "[OK , " + varN40C2, "[errorrrrrrrrrr , " + varN40C2)
connPersonal.commit()

# 42,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 42，私聊_通讯录_删除标签名称接口
# 依赖于 CJL1_N40_C2
# 删除1个标签3个用户记录
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(labelID3))
sleep(4)
# 检查 t_user_label, 删除1条记录
N42C1 = curPersonal.execute('select id from t_user_label where id = %s order by id desc limit 1' % (int(labelID3)))
varN42C1 = "t_user_label , id = " + str(labelID3) + " , userId = " + str(getCJLuserID(myPhone)) + "]  # 删除"
assertEqual(N42C1, 0, "[OK , " + varN42C1, "[errorrrrrrrrrr , " + varN42C1)
connPersonal.commit()
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(labelID5))

# # 41,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 41，私聊_通讯录_修改标签名称接口 (作废)
# # 依赖于CJL1_N40_C1
# print "\nCJL1_N41 " + ">" * 150
# Icase("CJL1_N41_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(labelName+"(改)",str(labelID)))
# # 检查 t_user_label, 修改1条记录
# tmp1 = curPersonal.execute('select id from t_user_label where labelName="%s" order by id desc limit 1' % (labelName + "(改)"))
# var1 = "t_user_label , id = " + str(labelID) + " , userId = " + str(getCJLuserID(myPhone)) + " , userNumber = 1 , labelName = " + labelName+"(改)" + "]  # 修改"
# assertEqual(tmp1, 1, "[OK , " + var1, "[errorrrrrrrrrr , " + var1)

# 43,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 43，场景_分场景_获取分场景详情接口
# 依赖于CJL1_N12_C1
print "\nCJL1_N43 " + ">" * 150
Icase("CJL1_N43_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(splitID,cityID))

# 44,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 44，场景_分场景_完善场景资料接口
# 备注：只有管理员才能完善资料 或场主
# 依赖于CJL1_N12_C1
print "\nCJL1_N44 " + ">" * 150
Icase("CJL1_N44_C1", "RtnOK", getCJLuserID(myPhone), '"%s","分场景地址100号","02157665511","公告1","1","1","%s"' %(splitID,cityID))
# # 去mongdb中检查isAddCheck ，加场景验证(1:任何人，2:需要验证,3:不允许任何人)
# # isVisit，场景公开(1:允许游客访问,2:不允许游客访问)
# Icase("CJL1_N44_C2", "RtnOK", getCJLuserID(myPhone), '"%s","分场景地址100号","02157665511","公告1","2","2","%s"' %(splitID,cityID))
# # 去mongdb中检查？
# Icase("CJL1_N44_C3", "RtnOK", getCJLuserID(myPhone), '"%s","分场景地址100号","02157665511","公告1","3","1","%s"' %(splitID,cityID))
# # 去mongdb中检查？

# 45,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 45，场景_分场景_编辑场景接口
# 依赖于CJL1_N12_C1
print "\nCJL1_N45 " + ">" * 150
Icase("CJL1_N45_C1", "RtnOK", getCJLuserID(myPhone), '"%s","分场景地址200号","02157665512","公告2","%s","john的分场景1","100002","%s"' %(splitID,headPic2,cityID))

# 46,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 46，场景_分场景_修改场景公开接口
# 备注：只有管理员才能完善资料
# 依赖于CJL1_N12_C1
print "\nCJL1_N46 " + ">" * 150
Icase("CJL1_N46_C1", "RtnOK", getCJLuserID(myPhone), '"%s","1","%s"' %(splitID,cityID))

# 47,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 47，文件上传接口 (调用第三方上传函数)
print "\nCJL1_N47 " + ">" * 150
x = Icase("CJL1_N47_C1", "RtnOK", getCJLuserID(myPhone), '')
mysqlURL = eval(x.replace("true","0"))['data'][0]['url']     # https://cjl.88uka.com/pic/000/000/000/079.jpg?width=1440&height=900

# 48,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 48,首页_查看好友主页_设置/修改好友备注信息接口
print "\nCJL1_N48 " + ">" * 150
Icase("CJL1_N48_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(friendID1))  # 查看好友,并获取备注名及电话
# 检查数据库？
Icase("CJL1_N48_C2", "RtnOK", getCJLuserID(myPhone), '"%s","经商天后（原备注名）","02156778612（原电话）"' %(friendID1))  # 修改好友备注名及电话
# 检查数据库？
Icase("CJL1_N48_C3", "RtnOK", getCJLuserID(myPhone), '"%s","原备注名","原电话"' %(friendID1))  # 恢复好友备注名及电话
# 检查数据库？

# 49,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 49,首页_公共场景_查看好友/非好友信息接口
print "\nCJL1_N49 " + ">" * 150
Icase("CJL1_N49_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(friendID1,cityID))

# 50,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 50,场景_分场景_是否允许成员邀请好友接口
print "\nCJL1_N50 " + ">" * 150
Icase("CJL1_N50_C1", "RtnOK", getCJLuserID(myPhone), '"%s","1","%s"' %(splitID,cityID))

# 51,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 51,场景_分场景_修改分场景背景接口
print "\nCJL1_N51 " + ">" * 150
Icase("CJL1_N51_C1", "RtnOK", getCJLuserID(myPhone), '"%s","https://cjl.dailylife365.com/pic/0000/0000/0000/0037.jpg"' %(splitID))

# 52 在后面

# 53,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 53,场景_分场景_成员列表接口
print "\nCJL1_N53 " + ">" * 150
Icase("CJL1_N53_C1", "RtnOK", getCJLuserID(myPhone), '"%s","0","20","123"' %(splitID))

# 54 - 56 在后面

# 57,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 57,场景_分场景_修改消息免打扰接口
print "\nCJL1_N57 " + ">" * 150
Icase("CJL1_N57_C1", "RtnOK", getCJLuserID(myPhone), '"%s","1"' %(splitID))
sleep(4)
Icase("CJL1_N57_C2", "RtnOK", getCJLuserID(myPhone), '"%s","0"' %(splitID))

# 58,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 58,场景_分场景_修改置顶聊天接口
print "\nCJL1_N58 " + ">" * 150
Icase("CJL1_N58_C1", "RtnOK", getCJLuserID(myPhone), '"%s","0"' %(splitID))
sleep(4)
# 检查数据库？
Icase("CJL1_N58_C2", "RtnOK", getCJLuserID(myPhone), '"%s","1"' %(splitID))
# 检查数据库？

# 59,60 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 59,场景_分场景_修改加入场景方式接口
# 59的参数：1:任何人，2:需要验证,3:不允许任何人
# splitID的场景是1000003创建的，将10000015加入到 splitID场景里
print "\nCJL1_N59 " + ">" * 150
Icase("CJL1_N59_C1", "RtnOK", getCJLuserID(myPhone), '"%s","3","%s"' %(splitID,cityID))
sleep(4)
print "\nCJL1_N60 " + ">" * 150
# 60,场景_分场景_申请加入分场景接口
# 60的参数：0 加入成功,1 已经加入过，2 认证中, 3 该场景不允许主动加入
x = Icase("CJL1_N60_C1", "RtnOK", "10000015", '"%s","%s",""' % (splitID, cityID))
sleep(4)
assertEqual(x,3,"[OK , 该场景不允许主动加入]","[errorrrrrrrrr , CJL1_N59_C1,CJL1_N60_C1该场景不允许主动加入失败]")

Icase("CJL1_N59_C2", "RtnOK", getCJLuserID(myPhone), '"%s","2","%s"' % (splitID,cityID))
sleep(4)
x = Icase("CJL1_N60_C2", "RtnOK", "10000015", '"%s","%s",""' % (splitID, cityID))
sleep(4)
assertEqual(x,2,"[Ok , 认证中]","[errorrrrrrrr , CJL1_N59_C1,CJL1_N60_C1认证中失败]")
print "\nCJL1_N65 " + ">" * 150
# 65,我的场景_场景通知_同意申请加入场景接口
Icase("CJL1_N65_C1", "RtnOK", getCJLuserID(myPhone), '"%s","10000015"' % (splitID))
print "\nCJL1_N54 " + ">" * 150
# 54,场景_分场景_删除成员接口 ?
# 删除场景成员修改成删除多个
string1 = '["10000015"]'
Icase("CJL1_N54_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' %(splitID,str(eval(string1)).replace("'", "\\\""), cityID))
# Icase("CJL1_N54_C1", "RtnOK", getCJLuserID(myPhone), '"%s","10000015"' %(splitID))

# 第一次加入分场景
Icase("CJL1_N59_C3", "RtnOK", getCJLuserID(myPhone), '"%s","1","%s"' % (splitID, cityID))
sleep(4)
x = Icase("CJL1_N60_C3", "RtnOK", "10000015", '"%s","%s",""' % (splitID, cityID))
sleep(4)
assertEqual(x,0,"[OK , 加入成功]","[errorrrrrrr , CJL1_N59_C1,CJL1_N60_C1加入失败]")

Icase("CJL1_N59_C4", "RtnOK", getCJLuserID(myPhone), '"%s","1","%s"' % (splitID, cityID))
x = Icase("CJL1_N60_C4", "RtnOK", getCJLuserID(myPhone), '"%s","%s",""' % (splitID, cityID))
assertEqual(x,1,"[Ok , 已经加入过]","[errorrrrrrr,CJL1_N59_C1,CJL1_N60_C1已经加入过失败]")

# 56,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 56,场景_分场景_增加管理员接口
# 依赖于59，60，65接口，分场景中将成员ID提升为管理员。
print "\nCJL1_N56 " + ">" * 150
string1 = '["10000015"]'
Icase("CJL1_N56_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s"' % (splitID, str(eval(string1)).replace("'", "\\\""), cityID))
sleep(4)

# 92,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 92,场景_分场景_删除管理员接口
print "\nCJL1_N92 " + ">" * 150
Icase("CJL1_N92_C1", "RtnOK", getCJLuserID(myPhone), '"%s","10000015","%s"' % (splitID, cityID))

# 55,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 55,场景_分场景_管理员列表接口
print "\nCJL1_N55 " + ">" * 150
Icase("CJL1_N55_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(splitID))

# 52,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 52,场景_分场景_删除并退出接口
# 依赖于CJL1_N60_C1,
# 业务逻辑场景中应该有成员，当场主退出时才能指任下一人。 此接口有第二个2个参数可选
print "\nCJL1_N52 " + ">" * 150
Icase("CJL1_N52_C1", "RtnOK", getCJLuserID(myPhone), '"%s","10000015","%s"' % (splitID, cityID))
sleep(4)
Icase("CJL1_N52_C2", "RtnParamErr", getCJLuserID(myPhone), '"%s","10000015","%s"' % (splitID, cityID))
# 检查mongdb，查询，db.mySceneDto.find({sceneId:splitID}),记录userId=10000003的isAdmin=0，status=0，同时userID=10000015的isAdmin=2，status=1

# 63,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 63，私聊_通讯录_获取标签下所有成员接口
# 依赖 接口62，
print "\nCJL1_N63 " + ">" * 150
Icase("CJL1_N63_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID3))
Icase("CJL1_N42_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (labelID3))

# 64,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 64，私聊_通讯录_导入场景_我加入的列表接口
print "\nCJL1_N64 " + ">" * 150
Icase("CJL1_N64_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(cityID))

# 65 在前面

# 66，私聊_发送消息接口（请求json）

# 67,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 67，首页_公共场景_查看好友_设置标签_获取用户标签列表
print "\nCJL1_N67 " + ">" * 150
Icase("CJL1_N67_C1", "RtnOK", getCJLuserID(myPhone), '')

# 68,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 68，公共场景_公共场景报错和补充接口
# 涉及数据库 t_dict_industry , 依赖于1，2，12接口
# 大类及大类名 level=1 的id，name ，如id=100000
# 小类及小类名 level=2的id，name，且 parent=100000
print "\nCJL1_N68 " + ">" * 150
Icase("CJL1_N68_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","02167887611","100000","生活服务","100002","住宅小区","公告信息","%s","%s"' %(comID, getCJLuserID(myPhone),headPic,cityID))

# 69,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 69，分享_获得分享链接接口
# 涉及t_share
# 分享平台：'1：新浪微博 2：腾讯微博 3：微信好友 4：微信朋友圈 5：短信 6：qq好友 7：qq空间'
print "\nCJL1_N69 " + ">" * 150
Icase("CJL1_N69_C1", "RtnOK", getCJLuserID(myPhone), '"%s","1","3","%s","%s"' %(getCJLuserID(myPhone), splitID, cityID))

# # 70,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 70，私信_私信首页列表接口(作废,已本地化处理)
# print "\nCJL1_N70 " + ">" * 150
# Icase("CJL1_N70_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(getCJLuserID(myPhone),cityID))

# 71,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 71，私聊_私聊详情设置接口
# 前置条件新增好友CJL1_N34_C1
print "\nCJL1_N71 " + ">" * 150
Icase("CJL1_N71_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(getCJLuserID(myPhone), friendID2))
# 实际业务中是否有非好友的用户进行私聊详情设置？
# Icase("CJL1_N71_C2", "RtnSysErr", getCJLuserID(myPhone), '"%s","%s"' %(getCJLuserID(myPhone), "10000099"))


# 72,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 72，私聊_私聊详情设置修改接口
print "\nCJL1_N72 " + ">" * 150
Icase("CJL1_N72_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","0","1"' %(getCJLuserID(myPhone), friendID2))
Icase("CJL1_N72_C2", "RtnSysErr", getCJLuserID(myPhone), '"%s","%s","0","1"' %(getCJLuserID(myPhone), friendID1))

# 73,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 73，私聊_修改私信已读标记接口
print "\nCJL1_N73 " + ">" * 150
Icase("CJL1_N73_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(getCJLuserID(myPhone),friendID2))
Icase("CJL1_N73_C2","RtnSysErr",getCJLuserID(myPhone), '"%s","%s"' %(getCJLuserID(myPhone),friendID1))

# 74,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 74，私聊_获得私信消息列表接口(作废,已本地化处理)
# print "\nCJL1_N74 " + ">" * 150
# Icase("CJL1_N74_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","2016-11-01 09:43:42"' %(getCJLuserID(myPhone),friendID1))

# 75,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 75，场景_上传场景图片接口
print "\nCJL1_N75 " + ">" * 150
Icase("CJL1_N75_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","%s","https://cjl.dailylife365.com/pic/0000/0000/0000/0038.jpg,https://cjl.dailylife365.com/pic/0000/0000/0000/0032.jpg"' %(splitID,getCJLuserID(myPhone),cityID))

# 76,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 76，场景_场景相册列表接口
print "\nCJL1_N76 " + ">" * 150
# Icase("CJL1_N76_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","0","20"' %(splitID,getCJLuserID(myPhone)))
Icase("CJL1_N76_C1", "RtnOK", getCJLuserID(myPhone), '"%s","0","20"' %(splitID))


# 77,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 77，场景_获取图片详情接口
# 从 sceneAlbumDto中获取场景的 _id=(mainID)
print "\nCJL1_N77 " + ">" * 150
Icase("CJL1_N77_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(getCJLsceneAlbumDto_id(getCJLuserID(myPhone),splitID)))

# 78,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 78，场景_图片点赞接口
print "\nCJL1_N78 " + ">" * 150
Icase("CJL1_N78_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(getCJLsceneAlbumDto_id(getCJLuserID(myPhone),splitID)))

# 79,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 79，场景_取消点赞接口
print "\nCJL1_N79 " + ">" * 150
Icase("CJL1_N79_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(getCJLsceneAlbumDto_id(getCJLuserID(myPhone),splitID)))

# 80,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 80，首页_获取搜索关键词接口
print "\nCJL1_N80 " + ">" * 150
Icase("CJL1_N80_C1", "RtnOK", getCJLuserID(myPhone), '"1","%s","%s"' %(comSceneName,cityID))
sleep(4)
Icase("CJL1_N80_C2", "RtnOK", getCJLuserID(myPhone), '"2","%s","%s"' %(splitSceneName,cityID))

# 81,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 81，我的_我的相册列表接口
print "\nCJL1_N81 " + ">" * 150
Icase("CJL1_N81_C1", "RtnOK", getCJLuserID(myPhone), '"0","20","%s"' %(cityID))

# 82,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 82，文件上传_图片修改接口
# 依赖于 CJL1_N47_C1 的返回 mysqlURL
# # 涉及表 uploadfile,确保有相同的userID及图片
print "\nCJL1_N82 " + ">" * 150
Icase("CJL1_N82_C1", "RtnOK", getCJLuserID(myPhone), '%s' %(mysqlURL))

# 83,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 83，场景_删除相册接口
print "\nCJL1_N83 " + ">" * 150
Icase("CJL1_N83_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s"' %(getCJLsceneAlbumDto_id(getCJLuserID(myPhone),splitID),splitID))

# 86,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 86，场景_分场景_修改我加入的场景昵称接口
print "\nCJL1_N86 " + ">" * 150
Icase("CJL1_N86_C1", "RtnOK", getCJLuserID(myPhone), '"%s","修改的昵称1","%s"' %(splitID,cityID))

# 87,在前面

# 88,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 88,App异常信息上传接口
print "\nCJL1_N88 " + ">" * 150
Icase("CJL1_N88_C1", "RtnOK", getCJLuserID(myPhone), '"1","2.5.0","huawei","6.0","error123","null"')

# 89,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 89,我的_我的相册_删除相册接口
# 从 sceneAlbumDto中获取场景的 _id=(mainID)
print "\nCJL1_N89 " + ">" * 150
Icase("CJL1_N89_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' %(getCJLsceneAlbumDto_id(getCJLuserID(myPhone),splitID)))

# 90,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 90,我的场景_我的场景列表接口
print "\nCJL1_N90 " + ">" * 150
Icase("CJL1_N90_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ')

# 91,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 91,私聊_新的朋友_搜索好友接口
print "\nCJL1_N91 " + ">" * 150
Icase("CJL1_N91_C1", "RtnOK", getCJLuserID(myPhone), '"%s", ' % (vardeerNumber))

# 92, 在前面

# 93,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 93,私聊_通讯录_获取在线好友列表接口
print "\nCJL1_N93 " + ">" * 150
Icase("CJL1_N93_C1", "RtnOK", getCJLuserID(myPhone), '"%s","10000015","%s"' % (splitID, cityID))

# 94,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 94,我的场景_我的场景在场人数接口
print "\nCJL1_N94 " + ">" * 150
Icase("CJL1_N94_C1", "RtnOK", getCJLuserID(myPhone), '')

# 95,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 95,私聊_私聊详情免打扰设置修改接口
print "\nCJL1_N95 " + ">" * 150
Icase("CJL1_N95_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","0"' %(getCJLuserID(myPhone), friendID2))

# 96,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 96，私聊_私聊详情置顶设置修改接口
print "\nCJL1_N96 " + ">" * 150
Icase("CJL1_N96_C1", "RtnOK", getCJLuserID(myPhone), '"%s","%s","0"' %(getCJLuserID(myPhone), friendID2))


# [场景鹿1.1接口]
# 3,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 3,获取IOS用户图标红点接口
print "\nCJL11_N3 " + ">" * 150
Icase("CJL11_N3_C1", "RtnOK", getCJLuserID(myPhone), '')

# 4,>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 4,登出接口
print "\nCJL11_N4 " + ">" * 150
Icase("CJL11_N4_C1", "RtnOK", getCJLuserID(myPhone), '')




# # mysql手工清理数据
#
# # 1、删除好友（t_user_friends）
# curPersonal.execute('delete from t_user_friends where userId=%s or friendUserId=%s' %(getCJLuserID(myPhone), getCJLuserID(myPhone)))
# connPersonal.commit()
# print "t_user_friends , 已清除数据"
#
# # 2、删除新好友申请消息（t_user_friends_apply）
# curPersonal.execute('delete from t_user_friends_apply where userId=%s ' %(getCJLuserID(myPhone)))
# connPersonal.commit()
# print "t_user_friends_apply , 已清除数据"
#
# # 3、删除用户设置表（t_user_setting）
# curPersonal.execute('delete from t_user_setting where id=%s' %(getCJLuserID(myPhone)))
# connPersonal.commit()
# print "t_user_setting , 已清除数据"
#
# # 4、删除标签及用户标签成员
# curPersonal.execute('delete from t_user_label where userId=%s' %(getCJLuserID(myPhone)))
# connPersonal.commit()
# print "t_user_label , 已清除数据"
#
# curPersonal.execute('delete from t_user_label_memberinfo where userId=%s' %(getCJLuserID(myPhone)))
# connPersonal.commit()
# print "t_user_label_memberinfo , 已清除数据"
