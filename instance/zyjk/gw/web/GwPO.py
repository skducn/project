# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-25
# Description:
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from PO.WebPO import *
Web_PO = WebPO("chrome")

from PO.ListPO import *
List_PO = ListPO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

import ddddocr

class GwPO():

    def clsApp(self, varApp):

        '''
        关闭应用程序
        :param varApp:
        :return:
         # clsApp("chrome.exe")
        '''

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()


    def login(self, varUrl, varUser, varPass):
        # 登录
        Web_PO.openURL(varUrl)
        Web_PO.setTextByX("//input[@placeholder='请输入用户名']", varUser)
        Web_PO.setTextByX("//input[@placeholder='输入密码']", varPass)
        Web_PO.clkByX("//button[@type='button']", 1)
        # for i in range(10):
        #     code = Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")
        #     Base64_PO.base64ToImg(code)
        #     ocr = ddddocr.DdddOcr()
        #     f = open("test.gif", mode='rb')
        #     img = f.read()
        #     varCode = ocr.classification(img)
        #     # print(varCode)
        #     Web_PO.setTextByX("//input[@placeholder='输入图形验证码']", varCode)
        #     Web_PO.clkByX("//button[@type='button']", 1)
        #     if Web_PO.isBooleanByX("//button[@type='button']") == False:
        #         break

    def getDecode(self, varKey, varSm2Data):

        # 在线sm2解密数据
        d = {}
        Web_PO.opnLabel("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.swhLabel(1)
        # 解密秘钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[1]/textarea", "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[2]/textarea", varSm2Data)
        Web_PO.clkByX("/html/body/div/form/div[2]/div[2]/input[2]", 2)
        s_result = Web_PO.getAttrValueByX("/html/body/div/form/div[3]/textarea", "value")
        d_result = eval(s_result)
        d[varKey] = d_result
        Web_PO.cls()
        Web_PO.swhLabel(0)
        return d

    def getMenu2Url(self):

        # 获取菜单连接

        # 统计ur数量
        c = Web_PO.getCount("ul")
        varLabelCount = c-3

        # 获取二级菜单名
        Web_PO.clsDisplayByTagName("ul", varLabelCount)  # 展开所有二级菜单（去掉display：none）
        l_menu2 = Web_PO.getTextListByX("//ul/div/a/li/span[2]")
        # print(l_menu2)  # ['健康档案概况', '个人健康档案', '家庭健康档案', ...

        # 获取二级菜单链接
        l_menu2Url = Web_PO.getAttrValueListByX("//a", "href")
        # print(l_menu2Url) # ['http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex', 'http://192.168.0.203:30080/#/phs/HealthRecord/Personal', ...

        # 生成字典{菜单：URL}
        d_menuUrl = dict(zip(l_menu2, l_menu2Url))
        # print(d_menuUrl)  # {'健康档案概况': 'http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex',...

        return d_menuUrl

    def menu1(self, varMenu1):

        '''格式化一级菜单'''

        l_menu = Web_PO.getTextListByX("//li")
        # 去掉''
        l_menu = [i for i in l_menu if i != '']  # ['首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu = (dict(enumerate(l_menu, start=1)))
        # print(d_menu)  # {1: '首页', 2: '基本公卫', 3: '三高共管六病同防', 4: '系统配置', 5: '社区管理', 6: '报表', 7: '更多菜单'}

        # 序列化反转
        d_menu = {v: k for k, v in d_menu.items()}
        print(d_menu)  # {'首页': 1, '基本公卫': 2, '三高共管六病同防': 3, '系统配置': 4, '社区管理': 5, '报表': 6, '更多菜单': 7}

        if varMenu1 == '更多菜单':
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li["+ (str(d_menu[varMenu1]))+ "]")
        else:
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li["+ (str(d_menu[varMenu1]))+ "]")
                         # /html/body/div[1]/div/div[1]/div[2]/ul/li[2]
                         # /html/body/div[1]/div/div[2]/div[2]/ul/li[3]
                         # /html/body/div[1]/div/div[2]/div[2]/ul/li[4]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[1]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[1]
        # return d_menu

    def menu2(self, d_menu1, varMenuName):

        '''格式化二级菜单'''
        # ['健康档案管理', '', '', '', '', '', '儿童健康管理', '', '', '', '', '孕产妇管理', '', '', '', '', '老年人健康管理', '', '', '', '', '', '肺结核患者管理', '', '', '', '', '残疾人健康管理', '', '', '', '', '严重精神障碍健康管理', '', '', '', '', '健康教育', '', '高血压管理', '', '', '', '糖尿病管理', '', '', '', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']

        Web_PO.clkByX('//*[@id="topmenu-container"]/li[' + str(d_menu1[varMenuName]) + ']', 2)

        # 获取二级菜单
        l_menu2 = Web_PO.getTextListByX("//li")

        # 去掉''
        l_menu2 = [i for i in l_menu2 if i != '']
        # print(l_menu2)  # ['健康档案管理', '儿童健康管理', '孕产妇管理', '老年人健康管理', '肺结核患者管理', '残疾人健康管理', '严重精神障碍健康管理', '健康教育', '高血压管理', '糖尿病管理', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu2 = (dict(enumerate(l_menu2, start=1)))
        # print(d_menu2)  # {1: '健康档案管理', 2: '儿童健康管理', 3: '孕产妇管理', 4: '老年人健康管理', 5: '肺结核患者管理', 6: '残疾人健康管理', 7: '严重精神障碍健康管理', 8: '健康教育', 9: '高血压管理', 10: '糖尿病管理', 11: '首页', 12: '基本公卫', 13: '三高共管六病同防', 14: '系统配置', 15: '社区管理', 16: '报表', 17: '更多菜单'}

        # 序列化反转
        d_menu2 = {v: k for k, v in d_menu2.items()}
        # print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}

        return d_menu2

        # return d_menu2[varMenuName]

    def menu3(self, d_menu2, varMenu2Name, varMenu3Name):

        '''格式化三级菜单'''
        # ['健康档案管理', '', '', '', '', '', '儿童健康管理', '', '', '', '', '孕产妇管理', '', '', '', '', '老年人健康管理', '', '', '', '', '', '肺结核患者管理', '', '', '', '', '残疾人健康管理', '', '', '', '', '严重精神障碍健康管理', '', '', '', '', '健康教育', '', '高血压管理\n高血压专项\n高血压随访\n高血压报病', '高血压专项', '高血压随访', '高血压报病', '糖尿病管理', '', '', '', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']
        # 定位 '高血压管理\n高血压专项\n高血压随访\n高血压报病'

        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(d_menu2[varMenu2Name]) + ']/li', 2)

        # 获取三级菜单
        l_menu3 = Web_PO.getTexts("//li")

        # 去掉''
        l_menu3 = [i for i in l_menu3 if i != '']
        # print(l_menu3)  # ['健康档案管理', '儿童健康管理', '孕产妇管理', '老年人健康管理', '肺结核患者管理', '残疾人健康管理', '严重精神障碍健康管理', '健康教育', '高血压管理\n高血压专项\n高血压随访\n高血压报病', '高血压专项', '高血压随访', '高血压报病', '糖尿病管理', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu3 = (dict(enumerate(l_menu3, start=1)))
        # print(d_menu3)  # {1: '健康档案管理', 2: '儿童健康管理', 3: '孕产妇管理', 4: '老年人健康管理', 5: '肺结核患者管理', 6: '残疾人健康管理', 7: '严重精神障碍健康管理', 8: '健康教育', 9: '高血压管理\n高血压专项\n高血压随访\n高血压报病', 10: '高血压专项', 11: '高血压随访', 12: '高血压报病', 13: '糖尿病管理', 14: '首页', 15: '基本公卫', 16: '三高共管六病同防', 17: '系统配置', 18: '社区管理', 19: '报表', 20: '更多菜单'}

        # 序列化反转
        d_menu3 = {v: k for k, v in d_menu3.items()}
        # print(d_menu3)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理\n高血压专项\n高血压随访\n高血压报病': 9, '高血压专项': 10, '高血压随访': 11, '高血压报病': 12, '糖尿病管理': 13, '首页': 14, '基本公卫': 15, '三高共管六病同防': 16, '系统配置': 17, '社区管理': 18, '报表': 19, '更多菜单': 20}

        for k, v in d_menu3.items():
            if varMenu2Name + "\n" in k:
                list1 = k.split("\n")  # ['高血压管理', '高血压专项', '高血压随访', '高血压报病']
                for i in range(len(list1)):
                    if list1[i] == varMenu3Name:
                        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(d_menu2[varMenu2Name]) + ']/li/ul/div[' + str(i) + ']/a', 2)
                        break
                break

    def newMedicalInstitution(self, hospital, hospitalCode, hospitalReg, hospitalLevel, hospitalPerson, hospitalAddress, hospitalPhone, hospitalIntro):

        # 新增医疗机构
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[1]/button', 1)
        Web_PO.setText("//input[@placeholder='请输入医院名称']", hospital)
        Web_PO.setText("//input[@placeholder='请输入医院代码']", hospitalCode)
        Web_PO.setText("//input[@placeholder='请输入医院登记号']", hospitalReg)
        Web_PO.jsReadonly("//input[@placeholder='请输入级别']")
        Web_PO.setText("//input[@placeholder='请输入级别']", hospitalLevel)
        Web_PO.setText("//input[@placeholder='请输入医院负责人姓名']", hospitalPerson)
        Web_PO.setText("//input[@placeholder='请输入医院详细地址']", hospitalAddress)
        Web_PO.setText("//input[@placeholder='请输入医院联系电话']", hospitalPhone)
        Web_PO.setText("//textarea[@placeholder='请输入医院介绍']", hospitalIntro)
        Web_PO.clk('/html/body/div[4]/div/div/div[3]/div/button[1]', 1)

    def editMedicalInstitution(self, oldHospital, hospital, hospitalCode, hospitalReg, hospitalLevel, hospitalPerson, hospitalAddress, hospitalPhone, hospitalIntro):

        # 编辑医疗机构
        # 获取列表中指定医院所在的行，点击次行的'编辑'
        varTr = self.getHospitalTR(oldHospital)
        if varTr == None:
            print("warning, 未找到医院名称")
            return None
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(varTr) + ']/td[8]/div/button[1]', 1)

        Web_PO.setText("//input[@placeholder='请输入医院名称']", hospital)
        Web_PO.setText("//input[@placeholder='请输入医院代码']", hospitalCode)
        Web_PO.setText("//input[@placeholder='请输入医院登记号']", hospitalReg)
        Web_PO.jsReadonly("//input[@placeholder='请输入级别']")
        Web_PO.setText("//input[@placeholder='请输入级别']", hospitalLevel)
        Web_PO.setText("//input[@placeholder='请输入医院负责人姓名']", hospitalPerson)
        Web_PO.setText("//input[@placeholder='请输入医院详细地址']", hospitalAddress)
        Web_PO.setText("//input[@placeholder='请输入医院联系电话']", hospitalPhone)
        Web_PO.setText("//textarea[@placeholder='请输入医院介绍']", hospitalIntro)
        Web_PO.clk('/html/body/div[4]/div/div/div[3]/div/button[1]', 1)

    def getHospitalTR(self, varHospital):

        '''获取行'''

        l_1 = Web_PO.getTexts("//tr")
        # 序列化成字典
        d_1 = (dict(enumerate(l_1, start=0)))
        # 序列化反转
        d_1 = {v: k for k, v in d_1.items()}
        for k, v in d_1.items():
            if varHospital + "\n" in k:
                return v

    def editOffice(self, hospital, d_officeCode):

        # 科室维护
        # 获取列表中指定医院所在的行，点击次行的'科室维护'

        varTr = self.getHospitalTR(hospital)
        if varTr == None:
            print("warning, 未找到医院名称")
            return None
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(varTr) + ']/td[8]/div/button[2]', 1)

        # 获取所有科室
        if Web_PO.isElement("//input"):
            l_office_Code = Web_PO.getValuesByAttr("//input", "value")
            # print(l_office_Code)  # ['骨科', '000', '儿科', '9876']
            d_officeCode_old = List_PO.list2dictBySerial(l_office_Code)
            print(d_officeCode_old)  # {'骨科': '000', '儿科': '9876'}

            # 删除所有科室
            for i in range(len(d_officeCode_old)):
                Web_PO.clk('/html/body/div[5]/div/div/div[2]/form/div[' + str(2) + ']/div[3]/i', 1)

        # 新增科室
        for index, (k, v) in enumerate(d_officeCode.items()):
            Web_PO.clk('/html/body/div[5]/div/div/div[2]/form/div[1]/div[2]/i', 1)
            Web_PO.setText("/html/body/div[5]/div/div/div[2]/form/div[" + str(index+2) + "]/div[1]/div/div/div/input", k)
            Web_PO.setText("/html/body/div[5]/div/div/div[2]/form/div[" + str(index+2) + "]/div[2]/div/div/div/input", v)
        # 保存
        Web_PO.clk('/html/body/div[5]/div/div/div[3]/div/button[1]', 1)

    def personalHealthRecord(self, varIdCard):

        # 个人健康档案
        # 查询（通过身份证查找唯一记录）,并点击姓名
        # personalHealthRecord('110101196001193209')

        # 输入身份证
        Web_PO.setTextByX("/html/body/div[1]/div/div[3]/section/div/div/div[1]/form/div[1]/div[3]/div/div/input", varIdCard)
        # 点击查询
        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/button[1]", 2)
        # 点击姓名
        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div/div[2]/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/span" ,2)

        # l_result = Web_PO.getTextListByX("//td/div")
        # l_result = [i for i in l_result if i != '']
        # print(l_result)  # ['37068500200200014', '6月26日测试', '60\n高\n脂', '女',...

    def yjzx(self, varDisease, varProject):

        # 已建专项

        l_disease = Web_PO.getTextListByX("//button/span")
        # print(l_disease)
        for i in range(len(l_disease)):
            if l_disease[i] == varDisease:
                Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/button[" + str(i+1) + "]", 2)
                if varDisease == '高血压专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血压患者管理卡
                        print(self.hypertensionPatientCard())
                if varDisease == '糖尿病专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血压患者管理卡
                        print(self.diabetesPatientCard())
                if varDisease == '高血脂专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血脂患者管理卡
                        print(self.hyperlipidemiaPatientCard())
                break



    def hypertensionPatientCard(self):

        # 高血压患者管理卡

        # 获取字段名
        l_div = Web_PO.getTextListByX("//div[@class='table_line']/div")
        # print(l_div)  # ['管理卡号', '信息来源\n健康档案\n首诊测压\n普查\n门诊就诊\n其他', '', '档案编号'...
        l_div.remove('吸烟情况\n吸烟状况\n戒烟开始日期\n开始吸烟年龄\n岁')
        l_div.remove("未服药血压\nmmHg\nmmHg")
        # print(l_div)  # ['管理卡号', '信息来源\n健康档案\n首诊测压\n普查\n门诊就诊\n其他', '', '档案编号'...

        # 获取radio或checkbox状态
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"

        d_radio = {}
        d_radio1 = {}
        l_2 = []
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_div[i] = l_div[i].replace('饮酒情况\n饮酒频率\n从不\n偶尔\n经常\n每天\n开始饮酒年龄\n岁\n是否饮酒过量\n是\n否','饮酒频率\n从不\n偶尔\n经常\n每天\n是\n否')
                l_div[i] = l_div[i].replace('体育锻炼\n锻炼频率\n每天\n每周一次以上\n偶尔\n不运动','锻炼频率\n每天\n每周一次以上\n偶尔\n不运动')
                l_div[i] = l_div[i].replace('有\n无\n职业暴露危险因素','职业病危害因素接触史\n有\n无')
                l_div[i] = l_div[i].replace('有危害因素的具体职业\n从事职业时长\n年\n防护措施\n无\n有','防护措施\n无\n有')
                l_1 = l_div[i].split("\n")
                l_2.append(l_1.pop(0))
                # print(l_1)  # ['健康档案', '首诊测压', '普查', '门诊就诊', '其他']

                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                    # l_2.append(l_1[i].split("\n")[0])
                # print(l_2)
                d_box = dict(zip(l_1, l_bool))
                d_radio[l_div[ele_n]] = d_box

        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_radio1 = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print(d_radio1)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        l_fields = ['管理卡号','其他情况说明','档案编号', '姓名', '性别', '出生日期', '联系电话',
                    '身份证号码', '居住地址', '身高(cm)', '体重(kg)', '吸烟状况', '戒烟开始日期', '开始吸烟年龄',
                    '开始饮酒年龄', '职业暴露危险因素', '有危害因素的具体职业', '从事职业时长',
                    '毫米汞柱起','毫米汞柱始','确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        l_input = Web_PO.getAttrValueListByX("//div/div/div/input", 'value')
        # print(l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(8))
        l_input.insert(8, ll)

        d_other = dict(zip(l_fields, l_input))
        # print(d_other)  # {'管理卡号': '135', '其他情况说明': '', ...

        d_other.update(d_radio1)
        return d_other

    def diabetesPatientCard(self):

        # 糖尿病患者管理卡

        # 1，获取所有字段名和checkbox值
        l_trtd = Web_PO.getTextListByX("//tr/td")
        l_trtd = [i for i in l_trtd if i != '']
        # print(l_trtd)

        # 2.1，获取非checkbox字段
        ll = []
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                ll.append(l_trtd[ele_before_n])
        l_noCheckboxfield = [i for i in l_trtd if "\n" not in i]
        for i in range(len(ll)):
            l_noCheckboxfield.remove(ll[i])
        # print(l_noCheckboxfield)  # ['档案编号', '姓名', '性别', '出生日期', '身份证号', '职业', '居住地址', '身高(cm)', '体重(kg)', '确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        # 2.2，获取非checkbox值
        l_noCheckboxValue = Web_PO.getAttrValueListByX("//div/div/div/input", 'value')
        # print(l_noCheckboxValue)  # ['37068500200200014', '6月26日测试', '女', '1960-01-19'
        # 将居住地址6个值（索引5）组成列表
        l_tmp = []
        for i in range(6):
            l_tmp.append(l_noCheckboxValue.pop(5))
        l_noCheckboxValue.insert(5, l_tmp)
        # 2.3，合成非checkbox字典
        d_noCheckbox = dict(zip(l_noCheckboxfield, l_noCheckboxValue))
        # print(d_noCheckbox)  # {'档案编号': '543912fd978b4634bae81a7b556b95cb', '姓名': '6月26日测试', '性别': '女', '出生日期': '1960-01-19', '身份证号': '110101196001193209', '居住地址': ['山东省', '烟台市', '招远市', '泉山街道', '魁星东社区居民委员会', '1'], '身高(cm)': '145', '体重(kg)': '67', '其他特殊类型糖尿病说明': '', '确诊日期': '2024-06-13', '终止管理日期': '1900-01-01', '终止管理原因': '', '建卡时间': '2024-06-28', '建卡医生': '卫健委', '建卡医疗机构': '招远市卫健局'}

        # 3.1，获取checkbox值(# el-radio__input is-checked)
        l_checkbox = Web_PO.isBooleanAttrValueListByX("//div/label/span[1]", 'class',
                                                      'el-radio__input is-disabled is-checked')
        # print(l_checkbox)  # ['False', 'True', 'False', 'False', ...
        # 3.2，合成checkbox字典
        d_checkbox = {}
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                l_1 = l_trtd[i].split("\n")
                # print(l_1)  # ['健康档案', '社区门诊', '流行病学调查', '其他']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_checkbox.pop(0))
                l_all = dict(zip(l_1, l_bool))
                d_checkbox[l_trtd[ele_before_n]] = l_all
        # print(d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 4，按页面字段名顺序输出
        d_result = {}
        l_trtd1 = [i for i in l_trtd if "\n" not in i and i != '']
        for i in range(len(l_trtd1)):
            for k, v in d_noCheckbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
        return d_result

    def hyperlipidemiaPatientCard(self):

        # 高血脂患者管理卡

        # 1，获取所有字段名和checkbox值
        l_trtd = Web_PO.getTextListByX("//tr/td")
        l_trtd = [i for i in l_trtd if i != '']
        # print(l_trtd)

        # 2.1，获取非checkbox字段
        ll = []
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                ll.append(l_trtd[ele_before_n])
        l_noCheckboxfield = [i for i in l_trtd if "\n" not in i]
        for i in range(len(ll)):
            l_noCheckboxfield.remove(ll[i])
        # print(l_noCheckboxfield)  # ['档案编号', '姓名', '性别', '出生日期', '身份证号', '职业', '居住地址', '身高(cm)', '体重(kg)', '确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        # 2.2，获取非checkbox值
        l_noCheckboxValue = Web_PO.getAttrValueListByX("//div/div/div/input", 'value')
        # print(l_noCheckboxValue)  # ['37068500200200014', '6月26日测试', '女', '1960-01-19'
        # 将居住地址6个值（索引5）组成列表
        l_tmp = []
        for i in range(6):
            l_tmp.append(l_noCheckboxValue.pop(6))
        l_noCheckboxValue.insert(6, l_tmp)
        # 2.3，合成非checkbox字典
        d_noCheckbox = dict(zip(l_noCheckboxfield, l_noCheckboxValue))
        # print(d_noCheckbox)  # {'档案编号': '543912fd978b4634bae81a7b556b95cb', '姓名': '6月26日测试', '性别': '女', '出生日期': '1960-01-19', '身份证号': '110101196001193209', '居住地址': ['山东省', '烟台市', '招远市', '泉山街道', '魁星东社区居民委员会', '1'], '身高(cm)': '145', '体重(kg)': '67', '其他特殊类型糖尿病说明': '', '确诊日期': '2024-06-13', '终止管理日期': '1900-01-01', '终止管理原因': '', '建卡时间': '2024-06-28', '建卡医生': '卫健委', '建卡医疗机构': '招远市卫健局'}

        # 3.1，获取checkbox值(# el-radio__input is-checked)
        l_checkbox = Web_PO.isBooleanAttrValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-checked')
        # print(l_checkbox)  # ['False', 'True', 'False', 'False', ...
        # 3.2，合成checkbox字典
        d_checkbox = {}
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                l_1 = l_trtd[i].split("\n")
                # print(l_1)  # ['健康档案', '社区门诊', '流行病学调查', '其他']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_checkbox.pop(0))
                l_all = dict(zip(l_1, l_bool))
                d_checkbox[l_trtd[ele_before_n]] = l_all
        # print(d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 4，按页面字段名顺序输出
        d_result = {}
        l_trtd1 = [i for i in l_trtd if "\n" not in i and i != '']
        for i in range(len(l_trtd1)):
            for k,v in d_noCheckbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
        return d_result

    def runUser(self, *varUsername):

        l_username = Web_PO.getTextListByX("//tr/td[1]/div")
        # print(l_username) # ['零跑', '测试', '黎明', '李永波', '胡军', '张建民', '舒雅有', '赵爽', '陈平安']

        if len(varUsername) == 1 and varUsername[0] != 'all':
            for i in range(len(l_username)):
                if l_username[i] == varUsername[0]:
                    # print(l_username[i])
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                    self.residentHealthRecord(l_username[i])
        elif len(varUsername) > 1:
            print(varUsername)
            for i in range(len(l_username)):
                for j in range(len(varUsername)):
                    if l_username[i] == varUsername[j]:
                        # print(l_username[i])
                        Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                        self.residentHealthRecord(l_username[i])
                        # 关闭当前标签
                        l_a = Web_PO.getAttrValueListByX("//a",'href')
                        # print(l_a)
                        for i in range(len(l_a)):
                            if "http://192.168.0.203:30080/#/phs/personalAddOrUpdate/addOrUpdate" in l_a[i]:
                                Web_PO.clkByX('/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/a[' + str(i + 1) + ']/span', 2)
        elif len(varUsername) == 1 and varUsername[0] == 'all':
            print(l_username)
            for i in range(len(l_username)):
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                self.residentHealthRecord(l_username[i])
                # 关闭当前标签
                l_a = Web_PO.getAttrValueListByX("//a", 'href')
                for i in range(len(l_a)):
                    if "http://192.168.0.203:30080/#/phs/personalAddOrUpdate/addOrUpdate" in l_a[i]:
                        Web_PO.clkByX(
                            '/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/a[' + str(i + 1) + ']/span', 2)


    def _residentHealthRecord(self, l_div, i, varDisease, varDiseaseName, varDiseaseTime):

        #  _residentHealthRecord(self, l_div, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
        if l_div[i] == varDisease:
            ele_n = l_div.index(l_div[i])
            ele_after_n = ele_n + 1
            a = len(l_div[ele_after_n].split("\n"))
            # print(a)
            if a == 1:
                l_div[ele_after_n] = varDiseaseName
                ele_n = l_div.index(l_div[ele_after_n])
                ele_after_n = ele_n + 1
                l_div.insert(ele_after_n, varDiseaseTime)
            else:
                l_ = l_div[ele_after_n].split("\n")
                # print(l_)  # ['手术名称', '手术名称', '手术名称']
                if len(l_) > 1:
                    l_div[ele_after_n] = varDiseaseName + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, varDiseaseTime + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(len(l_) - 1):
                        l_div.insert(ele_after_n + j, varDiseaseName + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, varDiseaseTime + str(j + 2))

    def residentHealthRecord(self, varUsername):

        # 居民健康档案

        # 1.1 获取字段
        l_div = Web_PO.getTextListByX("//div[@class='table_line']/div")
        # print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        l_div.remove('现住址必填')
        l_div.remove('城镇职工基本医疗保险')
        l_div.remove('城镇居民基本医疗保险')
        l_div.remove('贫困救助')
        l_div.remove('关联户主')

        # 修改
        for i in range(len(l_div)):
            if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
                l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
            if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
                l_div[i] = '医疗费用支付方式1\n城镇职工基本医疗保险'

        # 插入
        l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '更新内容':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))

        # print('1.2 清洗l_div => ', l_div)


        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 生成d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}


        # 3 生成noCheckbox字段
        l_fields = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueListByX("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_fields.insert(l_fields.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueListByX("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_fields.insert(l_fields.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_fields[i - 5] + '恶性肿瘤备注'
                l_fields.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_fields[i - 5])
                    l_div.insert(ele_n + 1, l_fields[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_fields => ', l_fields)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_noCheckbox = dict(zip(l_fields, l_input))
        # print(100, d_noCheckbox)  # {'管理卡号': '135', '其他情况说明': '', ...
        d_noCheckbox.update(d_checkbox)
        # print('混合结果 =>', d_noCheckbox)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_noCheckbox.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result


