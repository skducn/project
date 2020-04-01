# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 发起首营,上游发给下游的企业
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../")))  # 将上级目录添加到环境变量中
from PageObject.color import *

varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"
varFORMAT = u"功能：发起企业首营\n\n" \
            u"语法：" + str(sys.argv[0]).split(".")[0] + u" 上游企业 下游企业 \n"
varDEMO = u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051  14516109052 \n"\


if len(sys.argv) != 3:
    printColor('\033[1;31;47m', 'printGreen', u"更新时间: 2018-6-14\n")
    printColor('\033[1;31;47m', 'printYellow', varFORMAT)
    printColor('\033[1;31;47m', 'printYellow', varDEMO)
else:
    from config.config import *
    from PageObject.ShouyingPO import *
    Level_PO = LevelPO(driver)
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    Database_PO.cur.execute('select link_man,enterprise_id from tt_enterprise where link_phone="%s" order by enterprise_id desc limit 1' % (sys.argv[1]))
    sendName = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select link_man,enterprise_id from tt_enterprise where link_phone="%s" order by enterprise_id desc limit 1' % (sys.argv[2]))
    receiveName = Database_PO.cur.fetchone()
    if not (sendName):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[1] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)
    if not (receiveName):
        Level_PO.printColor('\033[1;31;47m', 'printRed', u"很抱歉，该账号（" + sys.argv[2] + u"）不存在。")
        Level_PO.close_driver();os._exit(0)
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (sendName[1]))
    sendManager = Database_PO.cur.fetchone()
    Database_PO.cur.execute('select name,phone_number from tt_enterprise_user where enterprise_id="%s" order by enterprise_user_id desc limit 1' % (receiveName[1]))
    receiveManager = Database_PO.cur.fetchone()

    # main =============================================================================================================
    printColor('\033[1;31;47m', 'printSkyBlue', u"发起企业首营（1我方发起、2对方拒绝、3我方再次发起、4对方接收、5我方普管拒绝、6我方重新签发、7我方普管通过、8对方普管通过、9我方企管通过、10对方企管通过、11我方及对方首营统计）")


    # Level_PO.clickLinktext(u"首营管理", 2)
    # Level_PO.clickLinktext(u"企业首营管理", 2)
    # Level_PO.clickLinktext(u"签发资料", 2)
    # from selenium.webdriver.common.action_chains import ActionChains
    # Level_PO.clickXpath("//section[@id='sign']/div/div/div/div/div[1]/a/div/img", 2)  # 行政公章
    # dragger = Level_PO.driver.find_element_by_xpath("//img[@id='zhang']")
    # target = Level_PO.driver.find_element_by_xpath("//div[@id='draw']/canvas")
    # action = ActionChains(Level_PO.driver)
    # action.drag_and_drop(dragger, target).perform()  # 1.移动dragger到目标1
    # js = "var q=document.getElementById('zhang').scrollTop=500"
    # driver.execute_script(js)
    # target = driver.find_element_by_id("id_keypair")
    # Level_PO.driver.execute_script("arguments[0].scrollIntoView();", dragger)  # 拖动到可见的元素去
    # Level_PO.driver.get('http://sahitest.com/demo/dragDropMooTools.htm')
    # dragger = Level_PO.driver.find_element_by_id('dragger')  # 被拖拽元素
    # item1 = Level_PO.driver.find_element_by_xpath('//div[text()="Item 1"]')  # 目标元素1
    # item2 = Level_PO.driver.find_element_by_xpath('//div[text()="Item 2"]')  # 目标2
    # action = ActionChains(Level_PO.driver)
    # action.drag_and_drop(dragger, item2).perform()  # 1.移动dragger到目标1
    # action = ActionChains(Level_PO.driver)
    # ActionChains(Level_PO.driver).context_click(target).perform()
    # ActionChains(Level_PO.driver).click_and_hold(dragger).move_by_offset(1,1).release().perform()  # 5.与上一句相同，移动到指定坐标
    # ActionChains(Level_PO.driver).click_and_hold(dragger).move_by_offset(1,1).release().perform()  # 5.与上一句相同，移动到指定坐标
    # # 鼠标左键按下不放
    # ActionChains(Level_PO.driver).click_and_hold(element).perform()
    # # 平行移动大于解锁的长度的距离
    # action.drag_and_drop_by_offset(element, 300, 300).perform()
    # ActionChains(Level_PO.driver).drag_and_drop_by_offset(element, 0, 100).perform()
    # action.click_and_hold(element).move_by_offset(300, 300).release(2).perform(2)
    # ActionChains(Level_PO.driver).drag_and_drop(dragger, target).perform()  # 1.移动dragger到目标1
    # action.click_and_hold(element).move_by_offset(0, 550).release().perform()  # 5.与上一句相同，移动到指定坐标
    # ActionChains(Level_PO.driver).context_click(element).perform()
    # element = Level_PO.driver.find_element_by_xpath("//img[@id='zhang']")
    # target = Level_PO.driver.find_element_by_xpath("//canvas[@id='the-canvas']")
    # ActionChains(Level_PO.driver).context_click(target).perform()
    # ActionChains(Level_PO.driver).context_click().perform()
    # ActionChains(Level_PO.driver).drag_and_drop_by_offset(element, 222, 222).perform()
    # sleep(2)
    # Level_PO.clickXpath("//button[@ng-click='finish()']", 2)  # 完成签署
    # print "end "

    # # 2对方拒绝
    # printColor('\033[1;31;47m', 'printGreen', u"\n[2/11]，对方(" + receiveName[0] + u"，" + sys.argv[2] + u")拒绝企业首营交换。")
    # Level_PO.openURL(1980, 1080, varURLfront, 3)
    # Shouying_PO.login(sys.argv[2], u"q123456")
    # Shouying_PO.shouyingTo(u"refuse", u"拒绝理由是资料缺少！")
    #
    # # 3我方再次发起
    # printColor('\033[1;31;47m', 'printGreen', u"\n[3/11]，我方(" + sendName[0] + u"，" +  sys.argv[1] + u")再次发起首营交换申请。")
    # Level_PO.openURL(1980, 1080, varURLfront, 3)
    # Shouying_PO.login(sys.argv[1], u"q123456")
    # Shouying_PO.shouyingFromAgain(sys.argv[1])
    #
    # # 4对方接收
    # printColor('\033[1;31;47m', 'printGreen', u"\n[4/11]，对方(" + receiveName[0] + u"，" +  sys.argv[2] + u")接收企业首营交换。")
    # Level_PO.openURL(1980, 1080, varURLfront, 3)
    # Shouying_PO.login(sys.argv[2], u"q123456")
    # Shouying_PO.shouyingTo(u"pass", u"")
    #
    # # 5我方普管拒绝
    # printColor('\033[1;31;47m', 'printGreen', u"\n[5/11]，我方普管（" + sendManager[0] + u"，" + sendManager[1] + u"）审核拒绝。")
    # Level_PO.openURL(1980, 1080, varURLfront, 3)
    # Shouying_PO.login(sendManager[1], u"q123456")
    # Shouying_PO.normalManagerAudit(sys.argv[1], u"refuse")
    #
    # # 6我方重新签发
    # printColor('\033[1;31;47m', 'printGreen', u"\n[6/11]，对方(" + receiveName[0] + u"，" + sys.argv[2] + u")重新签发。")
    # Level_PO.openURL(1980, 1080, varURLfront, 3)
    # Shouying_PO.login(sys.argv[2], u"q123456")
    # Shouying_PO.shouyingToRetry(sys.argv[2])
    #
    # 7我方普管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[7/11]，我方普管（" + sendManager[0] + u"，" + sendManager[1] + u"）审核通过。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sendManager[1], u"q123456")
    Shouying_PO.normalManagerAudit(sys.argv[1], "pass")

    # 8对方普管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[8/11]，对方普管（" + receiveManager[0] + u"，" + receiveManager[1] + u"）审核通过。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(receiveManager[1], u"q123456")
    Shouying_PO.normalManagerAudit(sys.argv[2], "pass")

    # 9我方企管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[9/11]，我方企管(" + sendName[0] + u"，" + sys.argv[1] + u")审核通过。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[1], u"q123456")
    Shouying_PO.enterpriseManagerAudit(sys.argv[1], u"pass")

    # 10对方企管通过
    printColor('\033[1;31;47m', 'printGreen', u"\n[10/11]，对方企管(" + receiveName[0] + u"，" +  sys.argv[2] + u")审核通过。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.enterpriseManagerAudit(sys.argv[2], u"pass")

    # 11我方首营统计
    printColor('\033[1;31;47m', 'printGreen', u"\n[11/11]，我方（" + sys.argv[1] + u"）首页首营统计信息。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[1], u"q123456")
    Shouying_PO.statisticsShouying(1)
    # 对方首营统计
    printColor('\033[1;31;47m', 'printGreen', u"\n[11/11]，对方（" + sys.argv[2] + u"）首页首营统计信息。")
    Level_PO.openURL(1980, 1080, varURLfront, 3)
    Shouying_PO.login(sys.argv[2], u"q123456")
    Shouying_PO.statisticsShouying(0)

    printColor('\033[1;31;47m', 'printSkyBlue', u"\n企业首营交换已完成")

    Level_PO.close_driver()
