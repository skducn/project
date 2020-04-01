# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 电科智药，发起品种首营
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../")))  # 将上级目录添加到环境变量中
from PageObject.color import *


def shouyingAudit(varPhoneFromManager, auditStatus):
    # 企业发起者（发起方：美国经营有效公司）
    Level_PO.openURL(1200, 900, varURLfront, 3)
    Level_PO.setMaximize()
    '登录 '
    Shouying_PO.login(varPhoneFromManager, "q123456")
    '首营管理'
    Level_PO.clickLinktext(u"首营管理", 2)
    Level_PO.clickLinktext(u"企业首营管理", 2)
    Level_PO.clickLinktext(u"查看企业资料", 2)
    if auditStatus == u"审核通过":
        # 审核通过且确认
        Level_PO.clickXpathsConfirm("//a[@ng-click='accept(r)']", "//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)
        Level_PO.clickXpath("//button[@ng-click='finish()']", 2)  # 提交下一位审核人
        Level_PO.clickXpath("//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)  # 确认

    elif auditStatus == u"审核拒绝":
        # 审核拒绝且确认
        for a in driver.find_elements_by_xpath("//a[@ng-click='showRejectModal(r)']"):
            a.click()
            sleep(2)
            driver.find_element_by_xpath("//textarea[@ng-model='reason']").send_keys("1")
            driver.find_element_by_xpath("//button[@ng-click='reject()']").click()
            sleep(2)
    # Level_PO.clickXpath("//button[@data-target='#needMoreModal']", 2)  # 缺少资料
def shouyingToRetry(varPhone):
    # 企业接受方 重新签发
    Level_PO.openURL(1200, 900, varURLfront, 3)
    Level_PO.setMaximize()
    '登录 '
    Shouying_PO.login(varPhone, "q123456")
    '首营管理'
    Level_PO.clickLinktext(u"首营管理", 2)
    Level_PO.clickLinktext(u"企业首营管理", 2)
    Level_PO.clickLinktext(u"查看企业资料", 2)
    Level_PO.clickLinktext(u"发出企业资料", 2)
    # 重新签发且确认
    Level_PO.clickXpathsConfirm("//a[@ng-click='reSend(r)']", "//div[@id='alertDialog']/div/div/div[2]/button", 2)
    # 删除且确认
    # Level_PO.clickXpathsConfirm("//a[@ng-click='delete($index)", "//div[@id='confirmDialog']/div/div/div[2]/button[2]", 2)

    # Level_PO.clickXpath("//button[@data-target='#sendMoreModal']", 2)  # 补发资料


varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"
varFORMAT = u"功能：发起品种首营\n\n" \
            u"语法：" + str(sys.argv[0]).split(".")[0] + u" 发起方 接收方 品种名称 \n"
varDEMO = u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 14516109052 登山用品\n"\


if len(sys.argv) != 4:
    printColor('\033[1;31;47m', 'printGreen', u"脚本版本: 1.2.1 2018-6-5\n")
    printColor('\033[1;31;47m', 'printYellow', varFORMAT)
    printColor('\033[1;31;47m', 'printYellow', varDEMO)
else:
    from config.config import *
    from PageObject.ShouyingPO import *
    from Public.PageObject.ThirdPO import *
    from Public.PageObject.DatabasePO import *
    Level_PO = LevelPO(driver)
    Shouying_PO = ShouyingPO(Level_PO)
    Third_PO = ThirdPO()
    Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetc_sy')
    # 发起方用户名
    Database_PO.cur.execute('select link_man,enterprise_id from tt_enterprise where link_phone="%s" order by enterprise_id desc limit 1' % (sys.argv[1]))
    sendName = Database_PO.cur.fetchone()

    # 接受方用户名
    Database_PO.cur.execute('select link_man,enterprise_id from tt_enterprise where link_phone="%s" order by enterprise_id desc limit 1' % (sys.argv[2]))
    receiveName = Database_PO.cur.fetchone()

    # 发起方普通管理员用户名
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (sendName[1]))
    sendManager = Database_PO.cur.fetchone()

    # 接收方普通管理员用户名
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (receiveName[1]))
    receiveManager = Database_PO.cur.fetchone()

    # main =============================================================================================================
    printColor('\033[1;31;47m', 'printSkyBlue', u"发起品种首营（1我方发起、2对方普管拒绝、3我方再次发起、4对方普管接收、5对方企管接收、6首营统计）")


    # 4、对方普管接收
    printColor('\033[1;31;47m', 'printYellow', u"\n[4/6]，对方普管（" + receiveManager[0] + u"，" + receiveManager[1] + u"）同意品种交换。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(receiveManager[1], "q123456")
    Shouying_PO.productToAudit(sys.argv[2], sys.argv[3], u"pass")

    # 5、对方企管接收
    printColor('\033[1;31;47m', 'printYellow', u"\n[5/6]，对方（" + receiveName[0] + u"，" + sys.argv[2] + u"）同意品种交换。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[2], "q123456")
    Shouying_PO.productToAudit(sys.argv[2], sys.argv[3], u"pass")

    # 6、我方首营统计
    printColor('\033[1;31;47m', 'printYellow', u"\n[6/6]，我方（" + sys.argv[1] + u"）首页首营统计信息。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[1], u"q123456")
    Shouying_PO.statisticsShouying(1)
    # 6、对方首营统计
    printColor('\033[1;31;47m', 'printYellow', u"\n[6/6]，对方（" + sys.argv[2] + u"）首页首营统计信息。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.statisticsShouying(0)

    printColor('\033[1;31;47m', 'printSkyBlue', u"\n品种首营交换已完成")

    Level_PO.close_driver()
