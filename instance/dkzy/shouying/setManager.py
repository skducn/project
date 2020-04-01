# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-5-30
# Description: 首营前台审核流程设置，添加管理员加入审核流程中。（必须要先后台审核认证通过）
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PageObject.ShouyingPO import *

varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个\n"

if len(sys.argv) != 4:
    print u"功能：首营新增普通管理员并添加到审核流程中\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 手机号 设置普通管理员状态对应编号 普通管理员手机号\n" \
           u"参数：设置普通管理员对应编号： new = 新增，remove = 移出\n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 new ? //为企业账号（14516109051）随机新增1个普通管理员账号，并将Ta移入审批人列表\n\n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 remove 15088924500 //将企业账号（14516109051）下普通管理员（15088924500）移出审批人列表"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    try:
        Level_PO.openURL(varURLfront, 1)
        Shouying_PO.login(sys.argv[1], "q123456")
    except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));os._exit(0)

    '''新增普通管理员（手机号与身份证都判重）'''
    if sys.argv[2] == "new":
        Level_PO.clickLinktext(u"账户管理", 2)
        Level_PO.clickXpath("//a[@href='/shouying/web/app.php/user/account/index']", 2)  # 点击账户管理
        randomUserName = Third_PO.randomUserName()
        randomPhone = Third_PO.randomPhone()
        randomOtherPhone1 = Third_PO.randomPhone()
        randomOtherPhone2 = Third_PO.randomPhone()
        Level_PO.clickXpath("//button[@data-target='#popup-user-add']", 2)  # 新增
        Level_PO.inputId("add_name", randomUserName)  # 姓名
        Level_PO.inputId("add_phoneNumber", randomPhone) # 手机号码
        Level_PO.inputId("add_otherLink1", randomOtherPhone1)  # 其他联系方式1
        Level_PO.inputId("add_otherLink2", randomOtherPhone2)  # 其他联系方式2
        Level_PO.inputId("add_email", str(randomPhone) + "@manager.com")  # 邮箱
        Level_PO.inputId("add_idCard", Third_PO.randomIdCard())  # 身份证号码
        Level_PO.inputId("add_password", "q123456")  # 登录密码
        Level_PO.clickXpath("//button[@onclick='doCreate();']", 2)  # 提交
        Level_PO.clickXpath("//button[@onclick='closeHindModal();']", 2)  # 确定
        printColor('\033[1;31;47m', 'printGreen', u"4、恭喜您，已新增普管：" + randomUserName + u"（" + randomPhone + u"）")

        ''' 移入审核人列表 '''
        Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[2]/a", 2)  # 首营管理
        Level_PO.clickLinktext(u"审核流程设置", 2)
        Level_PO.clickLinktext(randomUserName, 2)  # 选择刚新增的普通管理员，移到已选审批人列表内。
        Level_PO.clickXpath("//button[@type='submit']", 2)  # 保存
        list1 =[]
        list1 = Level_PO.getXpathsText("//div")
        var1 = 0
        for i in range(len(Level_PO.getXpathsText("//div"))):
            if u"审批流程修改成功" in list1[i]:
                var1 = 1
        if var1 == 1:
            printColor('\033[1;31;47m', 'printGreen', u"   恭喜您，已将 \"" + randomUserName + u"\" 移入已选审批人列表。下一步交换设置：python setExchange.py " + sys.argv[1] + u" *|?")
        else:
            printColor('\033[1;31;47m', 'printRed', u"4、很遗憾，审批流程保存错误，请检查可选审核人员列表！")
    else:
        ''' 移出审核人列表 '''
        Level_PO.clickXpath("//ul[@class='sidebar-menu tree']/li[2]/a", 2)  # 首营管理
        Level_PO.clickLinktext(u"审核流程设置", 2)
        Database_PO.cur.execute('select enterprise_user_id from tt_enterprise_user where phone_number="%s" order by enterprise_id desc limit 1' % (sys.argv[3]))
        t1 = Database_PO.cur.fetchone()
        Level_PO.clickXpath("//div[@id='approval-item-" + str(t1[0]) + "']/i", 2)
        Level_PO.clickXpath("//button[@type='submit']", 2)  # 保存
        printColor('\033[1;31;47m', 'printGreen', u"4、恭喜您，已将'" + sys.argv[3] + u"'移出审批人列表。")

    Level_PO.close_driver()