# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-7-19
# Description: ERP 对象库
# *****************************************************************


import string, numpy
from string import digits
from PO.HtmlPO import *
from PO.ListPO import *
from PO.TimePO import *
from PO.ColorPO import *
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.FilePO import *
from PO.StrPO import *
from PO.WebPO import *
from PO.ListPO import *

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ErpPO():

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        self.Char_PO = CharPO()
        self.List_PO = ListPO()

        self.oaURL = "http://192.168.0.65"



    def loginOA(self):

        '''登录oa'''

        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(self.oaURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        self.Web_PO.inputId("name", "liuting")
        # self.Web_PO.inputId("password", "")
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    def getToken(self):

        '''获取token'''

        url = self.oaURL + "/logincheck.php"
        header = {"content-type": "application/x-www-form-urlencoded"}
        d_iParam = {'USERNAME': "niuxuebin"}
        r = requests.post(url, headers=header, data=d_iParam, verify=False)
        a = r.cookies.get_dict()
        url = self.oaURL + "/general/appbuilder/web/business/product/crm"
        r = requests.get(url, headers={"Cookie": "PHPSESSID=" + a["PHPSESSID"]}, verify=False)
        token = str(r.url).split("token=")[1]
        # print(token)
        return token

    def clickMemuOA(self, varMemuName, varSubName):

        '''左侧菜单选择模块及浮层模块（无标题）'''

        sleep(2)
        x = self.Web_PO.getXpathsText("//div")
        list1 = []
        for i in x:
            if "快捷菜单" in i:
                list1.append(i)
                break
        list2 = []
        for i in range(len(str(list1[0]).split("\n"))):
            if Str_PO.isContainChinese(str(list1[0]).split("\n")[i]) == True:
                list2.append(str(list1[0]).split("\n")[i])
        # print(list2)
        for j in range(len(list2)):
            if list2[j] == varMemuName:
                self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j + 1) + "]", 2)
                x = self.Web_PO.getXpathsText("//li")
                list3 = []
                list4 = []
                for i in x:
                    if varMemuName in i:
                        list3.append(i)
                        break
                # print(list3)
                for i in range(len(str(list3[0]).split("\n"))):
                    if str(list3[0]).split("\n")[i] != varMemuName and Str_PO.isContainChinese(
                            str(list3[0]).split("\n")[i]) == True:
                        list4.append(str(list3[0]).split("\n")[i])
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath(
                            "//ul[@id='first_menu']/li[" + str(j + 1) + "]/div[2]/ul/li[" + str(k + 1) + "]/a", 2)

    def clickMemuERP(self, menu1, menu2):

        '''盛蕴ERP管理平台 之菜单树'''

        l_menu1 = self.Web_PO.getXpathsText("//li")
        l_menu1_tmp = self.List_PO.delRepeatElem(l_menu1)
        for i in range(len(l_menu1_tmp)):
            if menu1 in l_menu1_tmp[i]:
                self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/div', 2)
                l_menu2_a = self.Web_PO.getXpathsText('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a')
                # print(l_menu2_a)  # ['拜访分析报表', '会议分析表', '投入产出分析表', '协访分析表', '重点客户投入有效性分析', '开发计划总揽']
                for j in range(len(l_menu2_a)):
                    if menu2 == l_menu2_a[j]:
                        self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a[' + str(j + 1) + ']', 2)

        # self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[2]/div/div[1]/input', "1234测试")



    def _helpingAnalysis(self, res_visitAnalysis, tbl_report, tblField, iResField, sql, d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}

        # visitAnalysis( '拜访分析报表', "计划拜访人次", "plannedVisitsNumber", "sql", {"endTime": "2022-06-30  23:59:59", "startTime": "2022-06-01", "uid": 0})
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2
        Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)
        # print(tblField)

        if iResField != None and sql == None:
            pass

        elif iResField != None and "%s" in sql:

            # 遍历所有人的字段值
            s = 0
            for i in range(len(res_visitAnalysis['data']['detail'])):


                if tbl_report == "协访分析":
                    sql_value = Mysql_PO.execQuery(sql % (res_visitAnalysis['data']['detail'][i]['uid'], d_tbl_param["startTime"], d_tbl_param["endTime"]))

                    if len(sql_value) == 0:
                        sql_value = 0
                    else:
                        if sql_value[0][0] == None:
                            sql_value = 0
                        else:
                            sql_value = sql_value[0][0]

                    # 接口和sql比对
                    s = s + sql_value
                    Openpyxl_PO.setCellValue(currRow, 1, res_visitAnalysis['data']['detail'][i]['userName'], varSheet)  # 第1列区域

                if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value), varSheet)  # 指标值
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

                currRow = currRow + 1
                d[iResField] = s

            Openpyxl_PO.save()


        else:
            # 各比率的计算

            for i in range(len(res_visitAnalysis['data']['detail'])):
                if res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0 :
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp1 = Data_PO.newRound(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] / res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100)
                    if tmp1 == int(res_visitAnalysis['data']['detail'][i][iResField]):
                        Openpyxl_PO.setCellValue(currRow, currCol, str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                        # Openpyxl_PO.setCellValue(currRow, 1, "ok", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                currRow = currRow + 1
            Openpyxl_PO.save()

        # 合计
        Openpyxl_PO.setCellValue(currRow, 1, "总计", varSheet)


        if iResField in d:
            if d[iResField] == res_visitAnalysis['data']['total'][iResField]:
                Openpyxl_PO.setCellValue(currRow, currCol, str(res_visitAnalysis['data']['total'][iResField]), varSheet)
            else:
                Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算1)/" + str(res_visitAnalysis['data']['total'][iResField]), varSheet)
                Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色


        else:
            if sql != None:
                if res_visitAnalysis['data']['total'][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['total'][sql.split("/")[0]] == 0:
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp = Data_PO.newRound(res_visitAnalysis['data']['total'][sql.split("/")[0]] / res_visitAnalysis['data']['total'][sql.split("/")[1]] * 100)
                    # print(tmp)
                    if tmp == int(res_visitAnalysis['data']['total'][iResField]):
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%(计算)/" + str(int(res_visitAnalysis['data']['total'][iResField])) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

        Openpyxl_PO.save()

    def helpingAnalysis_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        # 1，获取协访分析表接口数据

        # 获取token
        token = self.getToken()

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            if l_getRowValue_case[i][0] != "N":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                d_tbl_param = Str_PO.str2dict(l_getRowValue_case[i][2])  # 参数2字典
                varNowTime = str(Time_PO.getDateTime())
                varTitle = "erp_" + tbl_report + "(" + str(l_getRowValue_case[i][4]) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域经理"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        r = requests.post(iUrl + l_getRowValue_i[j][2],
                                          headers={"content-type": "application/json", "token": token,
                                                   "traceId": "123"},
                                          json=d_tbl_param, verify=False)
                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res_visitAnalysis = json.loads(str1)
                        l_getRowValue = (Openpyxl_PO.getRowValue(tbl_report))
                        varSign1 = 1
                        break

                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)

                for j in range(1, len(l_getRowValue)):
                    if l_getRowValue[j][0] != "N":
                        self._helpingAnalysis(res_visitAnalysis, tbl_report, l_getRowValue[j][1], l_getRowValue[j][2],
                                              l_getRowValue[j][3], d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO)

        return varTitle

    def getBrowserData_helpingAnalysis(self, varSheet, Openpyxl_PO):

        # 获取浏览器页面数据

        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "协访分析表")
        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")
        l_fieldValue = self.List_PO.sliceList(l_fieldValueArea, '区域经理', 0)
        l_area = self.List_PO.sliceList(l_fieldValueArea, '区域经理', 1)
        l_area.insert(0, '区域经理')
        l_area.append('总计')

        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValue)):
            list3 = str(l_fieldValue[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

        # 5, 将区域经理插入表格
        Openpyxl_PO.insertCols(1, 1, varSheet)
        Openpyxl_PO.setColValue({"A": l_area}, varSheet)

        self.Web_PO.close()

    def getResult(self, varSheet, Openpyxl_PO):

        # 对新表生成结果状态

        r = Openpyxl_PO.getRowCol(varSheet)[0]
        c = Openpyxl_PO.getRowCol(varSheet)[1]

        varSign = 0
        list11 = []
        for i in range(r):
            for j in range(c):
                if "/" in Openpyxl_PO.getCellValue(i + 1, j + 1, varSheet):
                    varSign = 1
            if varSign == 1:
                list11.append("error")
            else:
                list11.append("ok")
            varSign = 0

        Openpyxl_PO.insertCols(1, 1, varSheet)
        Openpyxl_PO.setColValue({"A": list11}, varSheet)
        Openpyxl_PO.setCellValue(1, 1, "结果", varSheet)

    def db2html(self, Mysql_PO, varTitle):

        # 生成report.html
        # varNowTime = str(Time_PO.getDateTime())
        # varTitle = "erp_" + tbl_report + "(" + str(l_getRowValue_case[i][4]) + ")_" + db_ip + "_" + varNowTime
        df = pd.read_sql(sql="select * from `12345`", con=Mysql_PO.getPymysqlEngine())
        pd.set_option('colheader_justify', 'center')  # 对其方式居中
        html = '''<html><head><title>''' + varTitle + '''</title></head>
        <body><b><caption>''' + varTitle + '''</caption></b><br><br>{table}</body></html>'''
        style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
        rptNameDate = "report/" + varTitle + ".html"
        with open(rptNameDate, 'w') as f:
            f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        from bs4 import BeautifulSoup
        # 优化report.html, 去掉None、修改颜色
        html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
        html_text = str(html_text).replace("<td>None</td>", "<td></td>").replace("<td>error</td>",'<td bgcolor="#ed1941">error</td>'). \
            replace("<td>ok</td>", '<td bgcolor="#00ae9d">ok</td>')
        # 另存为report.html
        tf = open(rptNameDate, 'w', encoding='utf-8')
        tf.write(str(html_text))
        tf.close()
        Sys_PO.openFile(rptNameDate)
