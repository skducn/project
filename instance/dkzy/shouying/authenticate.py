# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 首营企业资料认证
# usage: python authenticate.py 手机号
# http://sfz.ckd.cc/  身份证生成
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PageObject.ShouyingPO import *
varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"

if len(sys.argv) != 2:
    print u"功能：首营企业资料认证\n" \
           u"语法：python " + str(sys.argv[0]).split(".")[0] + u".py 手机号\n" \
           u"例子：python " + str(sys.argv[0]).split(".")[0] + u".py 14516109051  \n"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    try:
        Level_PO.openURL(varURLfront, 1)
        Shouying_PO.login(sys.argv[1], "q123456")
    except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));os._exit(0)

    #企业认证
    Level_PO.clickXpath("//a[@href='/shouying/web/app.php/person/editEnterpriseInfo']", 2)
    # 参数1 企业类型：varCompanyType 如生产企业，经营企业，医疗机构 - 公立医院，医疗机构 - 私立医院，医疗机构 - 诊所，零售药店
    # 参数2 证件类型：普通营业执照 ，多证合一营业执照
    # 最后的参数经营范围8个：药品,中药饮片,化妆品,食品,日用品,消毒产品,保健食品,医疗器械
    # 1，企业类型，证件类型，营业执照注册号，企业所在省份，地区，详细地址，有效期开始，有效期结束，长期有效，营业执照PIC，[组织机构代码证号码，组织机构代码证PIC]
    # 2，开户名称，开会账号，开户银行，开户所在地，开户许可证PIC
    # 3，经办人姓名，身份证号码，固定电话，身份证前，身份证后，经办授权委托书
    # 4，企业授权书PIC，行政公章PIC，质量管理部门印章PIC，经营范围
    # 5，生产企业之许可证（药品编号，药品有效期，药品PIC，GMPPIC，化妆品PIC1，化妆品有效期，化妆品PIC2，食品编号，食品有效期，食品PIC，医疗器械PIC）
    # 5，经营企业之许可证（药品编号，药品有效期，药品PIC，GSPPIC，食品编号，食品有效期，食品PIC，医疗器械PIC）
    # 6, 医疗机构公立医院之许可证（医疗机构执业许可证登记号，有效期，长期有效，医疗机构PIC）

    # 通过手机号获得企业类型和企业名称
    varCompanyName, varCompanyType = Shouying_PO.getEnterpriseTypeAndName(sys.argv[1])

    infoBusiness = Shouying_PO.authenticate(
        varCompanyType, u"多证合一营业执照", Third_PO.randomDigit(18), u"上海市", u"虹口区", u"上海虹口区大木桥路1200号", u"2018-04-18", u"2020-06-12", u"on", varJpg, Third_PO.randomDigit(15), varJpg,
        u"招商银行", Third_PO.randomDigit(16), u"招商张杨路支行", u"上海", varJpg,
        Third_PO.randomUserName(), Third_PO.randomIdCard(), u"021-58774521,0773-58774533,13816109050,13816109051", varJpg, varJpg, varJpg, varJpg, varGif, varGif,
        u"药品,中药饮片,化妆品,食品,日用品,消毒产品,保健食品,医疗器械",
        Third_PO.randomDigit(8), u"2038-04-01", varJpg, varJpg, varJpg, u"2038-04-01", varJpg, Third_PO.randomDigit(8), u"2038-04-01", varJpg, varJpg, Third_PO.randomDigit(8), u"2038-04-01", varJpg)

    if u"平台将收到纸质文件后3个工作日内完成资料审核" in infoBusiness:
        printColor('\033[1;31;47m', 'printGreen', u"2、恭喜您，企业账号（" + sys.argv[1] + u"）认证信息提交成功。下一步审核认证：python approve.py " + sys.argv[1] + u" pass|refuse")
    else:
        print infoBusiness
        print u"2、很遗憾，企业账号（" + sys.argv[1] + u"）认证信息提交错误，请检查！"

    Level_PO.close_driver()

