# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.5
# Date       : 2017-10-25
# Description: 电科党员学习教育平台, 用户转移，测试岗位是否存在。

'''业务场景：带岗位的用户被转移后的岗位测试
逻辑及流程：将A部门用户转移到B部门，用户原有的岗位应被取消，同时B部门赋予用户新的岗位，再将用户再转移回A部门时，同样用户岗位应被取消。'''

# 测试条件
# 1、测试环境，admin登录
# 2、组织架构：软信齐聚测试支部01 中成员 "金枝青" ，且具有'审核管理员'岗位。
# 3、岗位：软信齐聚测试支部02  中有 '普通管理员工'岗位。
# 4、以上组织架构、岗位必须存在，且脚本中对以上信息进行写死。

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Dangjian.Config.config import *
Level_PO = LevelPO(driver)

class WebTransferUser(unittest.TestCase):

    '''登录'''

    Level_PO.openURL(1200, 900, u"http://10.111.3.5:88/dangjian1.5/web/app_test.php/DJsecurity/security/login", 3)
    Level_PO.inputID(u"_username", u"admin")
    Level_PO.inputID(u"_password", u"123456")
    Level_PO.inputID(u"_captcha", Level_PO.getCode(u"test.jpg", 2060, 850, 2187, 900))  # 获取并输入验证码
    Level_PO.clickTAGNAME(u'button', 2)
    # 多次遍历获取并输入验证码
    for i in range(10):
        if Level_PO.isElementId(u"_captcha"):
            Level_PO.inputID(u"_username", u"admin")
            Level_PO.inputID(u"_password", u"123456")
            Level_PO.inputID(u"_captcha", Level_PO.getCode(u"test1.jpg", 2060, 792, 2187, 849))
            Level_PO.clickTAGNAME(u'button', 2)
        else:
            break
    Level_PO.setMaximize()

    ''' 软信奇聚测试支部01 (转移前）'''

    Level_PO.clickLINKTEXT(u'用户及权限管理', 2)
    Level_PO.clickLINKTEXT(u'架构及用户管理', 6)
    Level_PO.clickXPATH(u"//span[@id='treeDemo_2_switch']", 2)
    Level_PO.clickLINKTEXT(u'软信奇聚测试支部01', 2)
    Level_PO.printXpathText(u"//span[@id='companyName']")
    Level_PO.printXpathText(u"//table[@id='company_user_list']")
    y = Level_PO.getXpathText(u"//table[@id='company_user_list']")

    if u'金枝青 13516109050' in y:
        print u"end, no岗位"
    elif u'没有找到符合条件的数据' in y:
        print u"end"
    else:
        print u"\n//转移前，金枝青的岗位是'审核管理员'\n"
        Level_PO.clickXPATH(u"//a[@onclick='transfer(12201)']", 4)
        Level_PO.clickXPATH(u"//span[@id='companyTree_9_span']", 2)
        Level_PO.clickXPATH(u"//button[@onclick='transferUser()']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-default cetc-popup-confirm-btn']", 2)


        print u"~~~~~~~~~~~~~~~~~~~~ 01 转移后 02 ~~~~~~~~~~~~~~~~~~~~~"

        Level_PO.clickLINKTEXT(u'软信奇聚测试支部02', 4)
        Level_PO.printXpathText(u"//span[@id='companyName']")
        Level_PO.printXpathText(u"//table[@id='company_user_list']")
        z = Level_PO.getXpathText(u"//table[@id='company_user_list']")

        if u'金枝青 13516109050' in z:
            print u"\n//转移后，无岗位\n"
        else:
            print u"\n//errorrrrrrrrrr，转移失败\n"


        print u"~~~~~~~~~~~~~~~~~~~~ 02 给金枝青赋予新的岗位'普通管理员工' ~~~~~~~~~~~~~~~~~~~~~"

        Level_PO.clickLINKTEXT(u'岗位管理', 2)
        Level_PO.clickXPATH(u"//span[@id='companyTree_2_switch']", 2)
        Level_PO.clickLINKTEXT(u'软信奇聚测试支部02', 2)
        Level_PO.clickXPATH(u"//a[@data-target='#positionEdit_modal' and @onclick='setGlobalRoleId(67)']", 2)
        Level_PO.clickXPATH(u"//a[@onclick='addUser(67)']", 2)
        Level_PO.clickXPATH(u"//input[@value='12201']", 2)
        Level_PO.clickXPATH(u"//button[@onclick='position_add_user_submit()']", 2)
        Level_PO.clickXPATH(u"//div[@class='col-md-9']/div[1]/div[7]/div[1]/div[1]/div[3]/button[1]", 2)

        Level_PO.clickLINKTEXT(u'架构及用户管理', 6)
        Level_PO.clickXPATH(u"//span[@id='treeDemo_2_switch']", 2)
        Level_PO.clickXPATH(u"//span[@id='treeDemo_9_span']", 2)
        Level_PO.printXpathText(u"//span[@id='companyName']")
        Level_PO.printXpathText(u"//table[@id='company_user_list']")

        print u"\n//金枝青的新岗位是'普通管理员工'\n"

        # 再转移回 '软信齐聚测试支部01'， 检查用户的权限，应该没有权限
        print u"~~~~~~~~~~~~~~~~~~~~ 02 再转移回 01 ~~~~~~~~~~~~~~~~~~~~~"

        Level_PO.clickXPATH(u"//a[@onclick='transfer(12201)']", 4)
        Level_PO.clickXPATH(u"//span[@id='companyTree_7_span']", 2)
        Level_PO.clickXPATH(u"//button[@onclick='transferUser()']", 2)
        Level_PO.clickXPATH(u"//button[@class='btn btn-default cetc-popup-confirm-btn']", 2)
        Level_PO.clickLINKTEXT(u'软信奇聚测试支部01', 4)
        Level_PO.printXpathText(u"//span[@id='companyName']")
        Level_PO.printXpathText(u"//table[@id='company_user_list']")
        z = Level_PO.getXpathText(u"//table[@id='company_user_list']")

        if u'金枝青 13516109050' in z:
            print u"\n//金枝青 无岗位\n"
        else:
            print u"\n//errorrrrrrrrrr，再转移回失败\n"

        print u"~~~~~~~~~~~~~~~~~~~~ 还原 ~~~~~~~~~~~~~~~~~~~~~"

        # 给 '软信齐聚测试支部01' 中的用户添加 '审核管理者' 权限。
        Level_PO.clickLINKTEXT(u'岗位管理', 2)
        Level_PO.clickXPATH(u"//span[@id='companyTree_2_switch']", 2)
        Level_PO.clickLINKTEXT(u'软信奇聚测试支部01', 2)
        Level_PO.clickXPATH(u"//a[@data-target='#positionEdit_modal' and @onclick='setGlobalRoleId(66)']", 2)
        Level_PO.clickXPATH(u"//a[@onclick='addUser(66)']", 2)
        Level_PO.clickXPATH(u"//input[@value='12201']", 2)
        Level_PO.clickXPATH(u"//button[@onclick='position_add_user_submit()']", 2)
        Level_PO.clickXPATH(u"//div[@class='col-md-9']/div[1]/div[7]/div[1]/div[1]/div[3]/button[1]", 2)

        # 显示结果
        Level_PO.clickLINKTEXT(u'架构及用户管理', 6)
        Level_PO.clickXPATH(u"//span[@id='treeDemo_2_switch']", 2)
        Level_PO.clickLINKTEXT(u'软信奇聚测试支部01', 2)

        Level_PO.printXpathText(u"//span[@id='companyName']")
        Level_PO.printXpathText(u"//table[@id='company_user_list']")
        print u"\n//已恢复 金枝青的岗位'审核管理员'"

        print u"\npass "

        Level_PO.close_driver()


if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(WebTransferUser)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试




