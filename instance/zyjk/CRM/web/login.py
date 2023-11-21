# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-12-18
# Description: CRM/OA 智能办公
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# *****************************************************************

from instance.zyjk.CRM.PageObject.PimPO import *
Pim_PO = PimPO()
from PO.sqlserverPO import *
sqlserver_PO = SqlServerPO("192.168.0.195", "DBuser", "qwer#@!", "bmlpimpro")  # PIM 测试环境

# 登录
Pim_PO.login(user_drugstore)
sleep(3)

# # 切换目录
Pim_PO.leftMenu("门诊配发药")
Level_PO.clickLinkstext("门诊配发药管理", 2)

# c1,门诊配发药管理，检查门诊配发药窗口数量与待发数量是否一致，且已发数量默认第二天重置为0。
# 备注，门诊配发药窗口数来自 门诊收费 （小寒提供门诊收费数量，未处理）
# 默认第二天已发数量为0（未处理）
varWinSum = Level_PO.getXpathsNums("//div[@类与实例='el-table__fixed-body-wrapper']/table/tbody/tr")
# print("门诊配发药窗口数统计：" + str(varWinSum))
l_sum = Level_PO.getXpathsText("//div[@类与实例='printWrap clearfix']/span/span")
# print("待发数：" + str(l_sum[0]) + " , 已发数：" + str(l_sum[1]))
if int(varWinSum) != int(l_sum[0]):
    print("[errorrrrrrrrrrr] c1,门诊配发药管理，检查门诊配发药窗口数量与待发数量不一致！")
    print("门诊配发药窗口数统计：" + str(varWinSum) + " , 待发数：" + str(l_sum[0]) + " , 已发数：" + str(l_sum[1]))
elif int(l_sum[1]) != 0 :
    print("[errorrrrrrrrrrr] c1,门诊配发药管理，已发数量不为0！")
    print("待发数：" + str(l_sum[0]) + " , 已发数：" + str(l_sum[1]))
else:
    print("[ok] c1,门诊配发药管理，检查门诊配发药窗口数量与待发数量一致，且已发数量默认第二天重置为0。")

# c2, 门诊配发药管理，检查每个处方号是否有可用配发药数量（number - previewnumber + 规则*后数量）
# 检查药品单价、数量、金额、总计。
varEmpty = varCount = varSum = varMoney = varTotal = 0
l_recipeId = Level_PO.getXpathsText("//div[@类与实例='el-table__body-wrapper is-scrolling-left']/table/tbody/tr/td[4]/div")
# print(l_recipeId)
for i in range(len(l_recipeId)):
    l_drugIdSpec = sqlserver_PO.ExecQuery('select drugId,spec,recipeId,price number from t_ph_outpatient_dispensing_detail where recipeId=%s ' % (l_recipeId[i]))
    print(l_drugIdSpec)   # 记录数列表
    for j in range(len(l_drugIdSpec)):
        # print(l_drugIdSpec[j][0])  # drugId
        # print(l_drugIdSpec[j][1])  # 50mg/片*24/瓶
        l_drugCount = sqlserver_PO.ExecQuery('select number,previewNumber from t_ph_outpatient_drug_info where drugId=%s ' % (l_drugIdSpec[j][0]))
        if "*" in str(l_drugIdSpec[j][1]):
            x = str(l_drugIdSpec[j][1]).split("*")
            x = x[1].split("/")
            varEmpty = int(x[0])
            varCount = int(l_drugCount[0][0]) - int(l_drugCount[0][1]) + varEmpty
            print(str(l_drugCount[0][0]) + " - " + str(l_drugCount[0][1]) + " + " + str(varEmpty))
        else:
            varCount = int(l_drugCount[0][0]) - int(l_drugCount[0][1]) + 1
            print(str(l_drugCount[0][0]) + " - " + str(l_drugCount[0][1]) + " + 1")
        # print(varCount)
        varSum = varCount + varSum  # 某一个处方号下可配发药数量合计
        varMoney = int(l_drugIdSpec[j][3]) * int(l_drugIdSpec[j][4])  # 金额 = 单价 * 处方药品数量
        varTotal = varTotal + varMoney
    print("处方号：" + str(l_drugIdSpec[0][2]) + " => 可配发药数量合计：" + str(varSum) + " ， 金额：" + str(varMoney) + " , 总计：" + str(varTotal))
    varSum = 0





# # Pim_PO.modelMenu("医保")
# # Level_PO.clickXpath("//div[@aria-label='医保类型']/div[2]/button[3]/span", 2)  # 医保类型3  ? bug 无法点击文字
# Pim_PO.modelMenu("批量配发药")
# Pim_PO.modelMenu("\ue6f1 配发药")
# Pim_PO.modelMenu("叫号")
# Pim_PO.modelMenu("刷新")
# Pim_PO.modelMenu("挂起")
# # Pim_PO.modelMenu("暂停")  # 点击暂定后，设置和菜单的元素位置发生变化，则无法定位。
# Pim_PO.modelMenu("设置")
# Level_PO.clickXpath("//div[@aria-label='显示列设置']/div[3]/div/div/button[1]", 2)  # 确定
# Pim_PO.modelMenu("菜单")
# Level_PO.clickLinktext("配发药统计", 2)

