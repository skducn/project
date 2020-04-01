# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-4-27
# Description: 首营 交换设置
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PageObject.ShouyingPO import *
varERROR = u"错误，缺少参数，预期参数" + str(len(sys.argv)) + u"个。\n"

if len(sys.argv) != 3:
    print u"功能：首营交换设置(企业首营资料 + 品种首营资料)\n" \
           u"语法：" + str(sys.argv[0]).split(".")[0] + u" 企业账号 (* = 选择所有 ， ? = 手工输入)\n" \
           u"例子：" + str(sys.argv[0]).split(".")[0] + u" 14516109051 all|? \n" \
           u"注释：依据手机号对应的企业类型，默认勾选所有企业首营资料及品种首营资料 \n"
else:

    from Public.webdriver import *
    Level_PO = LevelPO(Webdriver())
    Shouying_PO = ShouyingPO(Level_PO)

    # main =============================================================================================================

    try:
        Database_PO.cur.execute('select enterprise_id from tt_enterprise_user where phone_number="%s" order by enterprise_user_id desc limit 1' % (sys.argv[1]))
        t0 = Database_PO.cur.fetchone()
        Database_PO.cur.execute('select type from tt_enterprise where enterprise_id="%s" order by enterprise_id desc limit 1' % (t0[0]))
        t1 = Database_PO.cur.fetchone()
        varCompanyType = t1[0]
    except:
        printColor('\033[1;31;47m', 'printRed', u"很抱歉，企业账号" + sys.argv[1] + u"不存在。")
        os._exit(0)  # 会直接将python程序终止，之后的所有代码都不会继续执行。

    if sys.argv[2] == "all" :
        # 交换设置'
        try:
            Level_PO.openURL(varURLfront, 1)
            Shouying_PO.login(sys.argv[1], "q123456")
        except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));

        # 选择交换设置资料
        Level_PO.clickLinktext(u"首营管理", 2)
        Level_PO.clickLinktext(u"交换设置", 2)
        Level_PO.clearXpathsCheckbox(u"//input[@type='checkbox']")  # 初始化复选框
        if varCompanyType == 1:
            Shouying_PO.setExchange_enterprise()
        if varCompanyType == 2 or varCompanyType == 6:
            Shouying_PO.setExchange_operate()
        if varCompanyType == 3:
            Shouying_PO.setExchange_public()
        if varCompanyType == 4:
            Shouying_PO.setExchange_private()
        if varCompanyType == 5:
            Shouying_PO.setExchange_clinic()
    else:
        # 企业首营资料（手工输入编号）
        printColor('\033[1;31;47m', 'printSkyBlue', u"规则：企业/品种首营资料（名称）的勾选，多个编号之间用英文逗号分隔，如1,4,8 ，* 表示全选\n")
        printColor('\033[1;31;47m', 'printGreen', u"【企业首营品种可选编号如下】")
        if varCompanyType == 1:  # 勾选8个
            printColor('\033[1;31;47m', 'printGreen', u"1 = 营业执照")
            printColor('\033[1;31;47m', 'printGreen', u"2 = GMP药品生产质量管理规范认证证书")
            printColor('\033[1;31;47m', 'printGreen', u"3 = 全国工业产品生产许可证")
            printColor('\033[1;31;47m', 'printGreen', u"4 = 药品生产许可证")
            printColor('\033[1;31;47m', 'printGreen', u"5 = 化妆品生产")
            printColor('\033[1;31;47m', 'printGreen', u"6 = 食品生产许可证")
            printColor('\033[1;31;47m', 'printGreen', u"7 = 消毒产品生产")
            printColor('\033[1;31;47m', 'printGreen', u"8 = 医疗器械生产")
        elif varCompanyType == 2 or varCompanyType == 6:  # 勾选5个  经营企业 或 零售企业
            printColor('\033[1;31;47m', 'printGreen', u"1 = 营业执照。")
            # printColor('\033[1;31;47m', 'printGreen', u"2 = 药品经营许可证。")
            # printColor('\033[1;31;47m', 'printGreen', u"3 = GSP药品经营质量管理规范认证证书。")
            # printColor('\033[1;31;47m', 'printGreen', u"4 = 食品经营许可证。")
            # printColor('\033[1;31;47m', 'printGreen', u"5 = 医疗器械经营。")
        elif varCompanyType == 3:   # 公立
            printColor('\033[1;31;47m', 'printGreen', u"1 = 医疗机构执业许可证。")
        elif varCompanyType == 4:   # 私立
            printColor('\033[1;31;47m', 'printGreen', u"1 = 营业执照。")
            # printColor('\033[1;31;47m', 'printGreen', u"2 = 医疗机构执业许可证。")
        elif varCompanyType == 5:  # 诊所
            printColor('\033[1;31;47m', 'printGreen', u"1 = 营业执照。")
            printColor('\033[1;31;47m', 'printGreen', u"2 = 医疗机构执业许可证。")
        try:
            varEnterprise = raw_input(unicode('\n请输入企业首营资料所需对应的编号：','utf-8').encode('gbk'))
        except:
            os._exit(0)

        # 品种首营资料（手工输入编号）
        printColor('\033[1;31;47m', 'printYellow', u"【品种首营品种可选编号如下】")
        printColor('\033[1;31;47m', 'printYellow', u"1 = 批准文号。")
        printColor('\033[1;31;47m', 'printYellow', u"2 = 药品质量标准。")
        printColor('\033[1;31;47m', 'printYellow', u"3 = 药品生产批件、药品注册证。")
        printColor('\033[1;31;47m', 'printYellow', u"4 = 药品检验报告书（省检或厂检）。")
        printColor('\033[1;31;47m', 'printYellow', u"5 = 药品包装盒、说明书备案。")
        printColor('\033[1;31;47m', 'printYellow', u"6 = 药品包装、标签、说明书实样和变更包装、标签、说明书材料。")
        printColor('\033[1;31;47m', 'printYellow', u"7 = 产品说明书。")
        printColor('\033[1;31;47m', 'printYellow', u"8 = 执行标准。")
        printColor('\033[1;31;47m', 'printYellow', u"9 = 疾控中心检测报告。")
        printColor('\033[1;31;47m', 'printYellow', u"10 = 生产许可证 （QS或SC证书）。")
        printColor('\033[1;31;47m', 'printYellow', u"11 = 包装盒说明书实物或复印件。")
        printColor('\033[1;31;47m', 'printYellow', u"12 = 化妆品网上备案打印件。")
        printColor('\033[1;31;47m', 'printYellow', u"13 = 第三方检测报告。")
        printColor('\033[1;31;47m', 'printYellow', u"14 = 卫生安全评价报告。")
        printColor('\033[1;31;47m', 'printYellow', u"15 = 备案凭证。")
        printColor('\033[1;31;47m', 'printYellow', u"16 = 消毒产品卫生许可证书。")
        printColor('\033[1;31;47m', 'printYellow', u"17 = 医疗器械质量检验监督中心检验报告或一类厂检。")
        printColor('\033[1;31;47m', 'printYellow', u"18 = 器械证书。")
        try:
            varProduct = raw_input(unicode('\n请输入品种首营资料所需对应的编号：', 'utf-8').encode('gbk'))
        except:
            os._exit(0)

        # 交换设置'
        try:
            Level_PO.openURL(varURLfront, 1)
            Shouying_PO.login(sys.argv[1], "q123456")
        except:printColor('\033[1;31;47m', 'printRed', "errorrrrrrrrrr, " + str(sys._getframe().f_lineno) + " row from " + str(__file__));

        ''' 选择交换设置资料 '''
        Level_PO.clickLinktext(u"首营管理", 2)
        Level_PO.clickLinktext(u"交换设置", 2)
        Level_PO.clearXpathsCheckbox(u"//input[@type='checkbox']")  # 初始化复选框
        print "\n"
        if varCompanyType == 1:  # 勾选8个
            if "all" in varEnterprise:
                    Shouying_PO.setExchange_enterprise()
            else:
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False and "1" in varEnterprise:
                    Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_gmp']") == False and "2" in varEnterprise:
                    Level_PO.clickId("standardClassEId_gmp", 2)  # GMP药品生产质量管理规范认证证书
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、GMP药品生产质量管理规范认证证书。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_industry_product_licence']") == False and "3" in varEnterprise:
                    Level_PO.clickId("standardClassEId_industry_product_licence", 2)  # 全国工业产品生产许可证
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，3、全国工业产品生产许可证。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_produce_authorize']") == False and "4" in varEnterprise:
                    Level_PO.clickId("standardClassEId_produce_authorize", 2)  # 药品生产许可证
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，4、药品生产许可证。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_cosmetics_licence']") == False and "5" in varEnterprise:
                    Level_PO.clickId("standardClassEId_cosmetics_licence", 2)  # 化妆品生产
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，5、化妆品生产。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_food_produce_authorize']") == False and "6" in varEnterprise:
                    Level_PO.clickId("standardClassEId_food_produce_authorize", 2)  # 食品生产许可证
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，6、食品生产许可证。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_disinfect_license']") == False and "7" in varEnterprise:
                    Level_PO.clickId("standardClassEId_disinfect_license", 2)  # 消毒产品生产
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，7、消毒产品生产。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_instrument_licence']") == False and "8" in varEnterprise:
                    Level_PO.clickId("standardClassEId_medical_instrument_licence", 2)  # 医疗器械生产
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，8、医疗器械生产。")
        elif varCompanyType == 2 or varCompanyType ==6:  # 勾选5个  经营企业 或 零售企业
            if "all" in varEnterprise:
                Shouying_PO.setExchange_operate()
            else:
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False and "1" in varEnterprise:
                    Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
                # if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_sale_authorize']") == False and "2" in varEnterprise:
                #     Level_PO.clickId("standardClassEId_sale_authorize", 2)  # 药品经营许可证
                #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、药品经营许可证。")
                # if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_gsp']") == False  and "3" in varEnterprise:
                #     Level_PO.clickId("standardClassEId_gsp", 2)  # GSP药品经营质量管理规范认证证书
                #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，3、GSP药品经营质量管理规范认证证书。")
                # if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_food_business']") == False  and "4" in varEnterprise:
                #     Level_PO.clickId("standardClassEId_food_business", 2)  # 食品经营许可证
                #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，4、食品经营许可证。")
                # if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_instrument_business_licence']") == False and "5" in varEnterprise:
                #     Level_PO.clickId("standardClassEId_medical_instrument_business_licence", 2)  # 医疗器械经营
                #     printColor('\033[1;31;47m', 'printGreen', u"已勾选，5、医疗器械经营。")
        elif varCompanyType == 3:   # 公立
            if "all" in varEnterprise:
                Shouying_PO.setExchange_public()
            else:
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_practice_license']") == False and "1" in varEnterprise:
                    Level_PO.clickId("standardClassEId_medical_practice_license", 2)  # 医疗机构执业许可证
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、医疗机构执业许可证。")
        elif varCompanyType == 4:   # 私立
            if "all" in varEnterprise:
                Shouying_PO.setExchange_private()
            else:
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False and "1" in varEnterprise:
                    Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_practice_license']") == False and "2" in varEnterprise:
                    Level_PO.clickId("standardClassEId_medical_practice_license", 2)  # 医疗机构执业许可证
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、医疗机构执业许可证。")
        elif varCompanyType == 5:  # 诊所
            if "all" in varEnterprise:
                Shouying_PO.setExchange_clinic()
            else:
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_business_licence']") == False and "1" in varEnterprise:
                    Level_PO.clickId("standardClassEId_business_licence", 2)  # 营业执照
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，1、营业执照。")
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassEId_medical_practice_license']") == False and "2" in varEnterprise:
                    Level_PO.clickId("standardClassEId_medical_practice_license", 2)  # 医疗机构执业许可证
                    printColor('\033[1;31;47m', 'printGreen', u"已勾选，2、医疗机构执业许可证。")

    # 品种交换

    # 选择所有的品种
    if sys.argv[2] == "all" or "all" in varProduct :
        Level_PO.clickXpath("//form[@id='exchangeSettingForm']/div/div[2]/div/div[2]/table/thead/tr/th[3]/div/input", 2)  # 全选
        printColor('\033[1;31;47m', 'printYellow', u"已全选，品种首营资料。")
    else:
        for i in range(len(varProduct.split(","))):
            if varProduct.split(",")[i] == "1":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_authenticationCode']") == False:
                    Level_PO.clickId("standardClassPId_authenticationCode", 2)  # 批准文号
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，1、批准文号。")
            if varProduct.split(",")[i] == "2":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_qualityStandard']") == False:
                    Level_PO.clickId("standardClassPId_qualityStandard", 2)  # 药品质量标准
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，2、药品质量标准。")
            if varProduct.split(",")[i] == "3":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_registration']") == False:
                    Level_PO.clickId("standardClassPId_registration", 2)  # 药品生产批件、药品注册证
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，3、药品生产批件、药品注册证。")
            if varProduct.split(",")[i] == "4":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_inspectionReport']") == False:
                    Level_PO.clickId("standardClassPId_inspectionReport", 2)  # 药品检验报告书（省检或厂检）
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，4、药品检验报告书（省检或厂检）。")
            if varProduct.split(",")[i] == "5":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_record']") == False:
                    Level_PO.clickId("standardClassPId_record", 2)  # 药品包装盒、说明书备案
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，5、药品包装盒、说明书备案。")
            if varProduct.split(",")[i] == "6":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_packageLabelInstruction']") == False:
                    Level_PO.clickId("standardClassPId_packageLabelInstruction", 2)  # 药品包装、标签、说明书实样和变更包装、标签、说明书材料
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，6、药品包装、标签、说明书实样和变更包装、标签、说明书材料。")
            if varProduct.split(",")[i] == "7":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_instruction']") == False:
                    Level_PO.clickId("standardClassPId_instruction", 2)  # 产品说明书
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，7、产品说明书。")
            if varProduct.split(",")[i] == "8":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_executeStandard']") == False:
                    Level_PO.clickId("standardClassPId_executeStandard", 2)  # 执行标准
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，8、执行标准。")
            if varProduct.split(",")[i] == "9":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_detectReport']") == False:
                    Level_PO.clickId("standardClassPId_detectReport", 2)  # 疾控中心检测报告
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，9、疾控中心检测报告。")
            if varProduct.split(",")[i] == "10":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_productLicense']") == False:
                    Level_PO.clickId("standardClassPId_productLicense", 2)  # 生产许可证 （QS或SC证书）
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，10、生产许可证 （QS或SC证书）。")
            if varProduct.split(",")[i] == "11":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_packBoxManual']") == False:
                    Level_PO.clickId("standardClassPId_packBoxManual", 2)  # 包装盒说明书实物或复印件
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，11、包装盒说明书实物或复印件。")
            if varProduct.split(",")[i] == "12":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_cosmeticsBackup']") == False:
                    Level_PO.clickId("standardClassPId_cosmeticsBackup", 2)  # 化妆品网上备案打印件
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，12、化妆品网上备案打印件。")
            if varProduct.split(",")[i] == "13":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_thirdRartyDetectReport']") == False:
                    Level_PO.clickId("standardClassPId_thirdRartyDetectReport", 2)  # 第三方检测报告
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，13、第三方检测报告。")
            if varProduct.split(",")[i] == "14":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_healthSafetyAssessmentReport']") == False:
                    Level_PO.clickId("standardClassPId_healthSafetyAssessmentReport", 2)  # 卫生安全评价报告
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，14、卫生安全评价报告。")
            if varProduct.split(",")[i] == "15":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_recordCertificate']") == False:
                    Level_PO.clickId("standardClassPId_recordCertificate", 2)  # 备案凭证
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，15、备案凭证。")
            if varProduct.split(",")[i] == "16":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_disinfectProductEquatur']") == False:
                    Level_PO.clickId("standardClassPId_disinfectProductEquatur", 2)  # 消毒产品卫生许可证书
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，16、消毒产品卫生许可证书。")
            if varProduct.split(",")[i] == "17":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_factoryInspection']") == False:
                    Level_PO.clickId("standardClassPId_factoryInspection", 2)  # 医疗器械质量检验监督中心检验报告或一类厂检
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，17、医疗器械质量检验监督中心检验报告或一类厂检。")
            if varProduct.split(",")[i] == "18":
                if Level_PO.isXpathCheckbox(u"//input[@id='standardClassPId_instrumentCert']") == False:
                    Level_PO.clickId("standardClassPId_instrumentCert", 2)  # 器械证书
                    printColor('\033[1;31;47m', 'printYellow', u"已勾选，18、器械证书。")
    Level_PO.clickXpath("//button[@type='submit']", 2)
    x = int(sys.argv[1]) + 1
    printColor('\033[1;31;47m', 'printGreen', u"5、恭喜您，首营交换设置已完成。下一步发起首营：python faqishouying.py " + sys.argv[1] +  u" " + str(x))

    Level_PO.close_driver()

