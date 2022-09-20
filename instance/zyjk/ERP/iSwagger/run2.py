# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : saas高血压接口自动化
# 接口文档：http://192.168.0.238:8801/doc.html
# web页：
# pip3 install jsonpath
# pip3 install pymysql
# pip3 install mysqlclient  (MySQLdb)
# css样式（外链） https://blog.csdn.net/qq_38316655/article/details/104663077
# css样式（内嵌） https://www.cnpython.com/qa/91356
# 展开
# 展开当前代码块ctrl =
# 彻底展开当前代码块ctrl alt =
# 展开所有代码块ctrl shift +
# 折叠
# 折叠当前代码块ctrl -
# 彻底折叠当前代码块ctrl alt -
# 折叠所有代码块ctrl shift -
# 参考：pandas之read_sql_query-params设置， https://zhuanlan.zhihu.com/p/281422144
# 参考：颜色对照表，https://bbs.bianzhirensheng.com/color01.html
# 参考 Python 通过Request上传(form-data Multipart)\下载文件, http://www.manongjc.com/detail/23-edxwzduohhtlzhf.html
# *****************************************************************
import sys, platform, json, jsonpath
import reflection
import readConfig as readConfig
import pandas as pd

import urllib3
urllib3.disable_warnings()


# sys.path.append("../../../")
sys.path.append("./")

from PO.TimePO import *
Time_PO = TimePO()

from PO.NetPO import *
Net_PO = NetPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.DictPO import *
Dict_PO = DictPO()

from PO.DataPO import *
Data_PO = DataPO()

from PO.HtmlPO import *
Html_PO = HtmlPO()

from ProjectI import *
project_I = ProjectI()



localReadConfig = readConfig.ReadConfig()

cf_default_project = localReadConfig.get_default("project")
cf_default_iCheck = localReadConfig.get_default("iCheck")
cf_switch_openRpt = localReadConfig.get_switch("openRpt")
cf_switch_sendEmail = localReadConfig.get_switch("sendEmail")
cf_default_xlsName = localReadConfig.get_default("xlsName")
cf_default_rptName = localReadConfig.get_default("rptName")
cf_default_rptTitle = localReadConfig.get_default("rptTitle")
cf_default_caseSheet = localReadConfig.get_default("caseSheet")


# 拉取swagger上项目接口
cf_switch_updateProject = localReadConfig.get_switch("updateProject")
if cf_switch_updateProject == "on":
    cf_switch_pullProject = localReadConfig.get_switch("pullProject")
    cf_switch_pullProject = json.loads(cf_switch_pullProject)
    Sys_PO.killPid('EXCEL.EXE')
    for k, v in cf_switch_pullProject.items():
        if v == "on":
            project_I.getI(k, cf_default_xlsName)
            print("[update], 拉取" + k)


cf_email_addresser = localReadConfig.get_email("addresser")
cf_email_to = localReadConfig.get_email("to")
cf_email_cc = localReadConfig.get_email("cc")
if cf_email_cc != 'None':
    print(cf_email_cc.split(","))
else:
    cf_email_cc = None
# ConfigParser的value如果包含\r\n的话都会被当成普通字符处理（自动转义成\\r\\n），只有编译器在编译时才会对\r\n等进行转义，只需 str.replace("\\n", "\n")即可。
cf_email_content = localReadConfig.get_email("content")
cf_email_content = cf_email_content.replace("\\n", "\n")
cf_email_head = localReadConfig.get_email("head")
cf_email_head = cf_email_head.replace("\\n", "\n")
cf_email_foot = localReadConfig.get_email("foot")
cf_email_foot = cf_email_foot.replace("\\n", "\n")
cf_email_content_html = localReadConfig.get_email("content_html")
cf_email_head_html = localReadConfig.get_email("head_html")
cf_email_foot_html = localReadConfig.get_email("foot_html")

if localReadConfig.get_default("env") == "test":
    cf_test_db_ip = localReadConfig.get_test("db_ip")
    cf_test_db_username = localReadConfig.get_test("db_username")
    cf_test_db_password = localReadConfig.get_test("db_password")
    cf_test_db_port = localReadConfig.get_test("db_port")
    cf_test_db_database = localReadConfig.get_test("db_database")
    cf_test_db_table = localReadConfig.get_test("db_table")
else:
    cf_dev_db_ip = localReadConfig.get_dev("db_ip")
    cf_dev_db_username = localReadConfig.get_dev("db_username")
    cf_dev_db_password = localReadConfig.get_dev("db_password")
    cf_dev_db_port = localReadConfig.get_dev("db_port")
    cf_dev_db_database = localReadConfig.get_dev("db_database")
    cf_dev_db_table = localReadConfig.get_test("db_table")


from PO.MysqlPO import *
Mysql_PO = MysqlPO(cf_test_db_ip, cf_test_db_username, cf_test_db_password, cf_test_db_database, cf_test_db_port)

from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO(cf_default_xlsName)

# excel导入数据库表
Mysql_PO.xlsx2db(cf_default_xlsName, cf_test_db_table, sheet_name=cf_default_caseSheet, index=True)
# 数据库index与excel编号一致
Mysql_PO.execQuery('update %s set `index` = `index` + 2' % (cf_test_db_table))

# 获取表格字段列表
l_m = Mysql_PO.getTableField(cf_test_db_table)
# print(l_m)
# ['index', '执行', '类型', '模块', '接口名称', '用例名称', '路径', '方法', '方式', 'query参数', 'body参数', 'i检查接口返回值', 'i结果', 'db检查表值', 'db结果', 'f检查文件', 'f结果', '全局变量', '备注']

# 获取列表的索引号
def getIndex(l_m, varText):
    for i in range(len(l_m)):
        if l_m[i] == varText:
            return i
    print("error，列表中没有找到" + str(varText))
    sys.exit(0)


class Run:

    def __init__(self):

        # 全局字典
        self.d_tmp = {}

        # 执行用例
        self.df = pd.read_sql_query("select * from %s where %s is null " % (cf_test_db_table, l_m[getIndex(l_m, '执行')]), Mysql_PO.getMysqldbEngine())


    def _escape(self, var):

        # 转义
        if "{{" in var:
            for k in self.d_tmp:
                if "{{" + k + "}}" in var:
                    var = str(var).replace("{{" + k + "}}", str(self.d_tmp[k]))
        d_var = dict(eval(var))
        # print(d_var)
        for k, v in d_var.items():
            # 其他封装函数返回内容转字符串，如str(Data_PO.autoNum(3))
            if "str(" in str(v):
                d_var[k] = eval(d_var[k])

            if "select" in str(v) and "from" in str(v):
                sql_value = Mysql_PO.execQuery(str(v))
                d_var[k] = sql_value[0][0]
        return d_var

    def _escape2(self, var):

        if "{{" in var:
            for k in self.d_tmp:
                if "{{" + k + "}}" in var:
                    var = str(var).replace("{{" + k + "}}", str(self.d_tmp[k]))
        return var


    def result(self, indexs, iName, iPath, iMethod, iConsumes, iQueryParam, iParam, iCheck, dbCheck, fCheck, g_var):

        # 字段：数据库表里数据索引, 4用例名称，5路径，6方法，7方式，8query参数，9body参数，10i检查接口返回值，11db检查表值, 12f检查文件, 13全局变量
        # run.result(indexs, r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13])

        d_var = {}


        if iName == "登录" and iParam != None:

            header = {"content-type": "application/x-www-form-urlencoded"}
            # print(iParam)
            # print(type(iParam))
            # print(json.loads(iParam))
            r = requests.post("http://192.168.0.65/logincheck.php", headers=header, data=json.loads(iParam), verify=False)
            a = r.cookies.get_dict()
            r = requests.get("http://192.168.0.65/general/appbuilder/web/business/product/crm", headers={"Cookie": "PHPSESSID=" + a["PHPSESSID"]}, verify=False)
            # print(r.url)
            d = {}
            # print(str(r.url).split("token=")[1])
            d["token"] = str(r.url).split("token=")[1]
            iParam = d
            iMethod = "header"


            # 7, 解析接口，获取返回值
            res, d_var = reflection.run([iName, iPath, iMethod, iConsumes, iQueryParam, iParam, d_var])

        elif iName == "设置全局变量":
            if g_var != None:
                d_var = self._escape(g_var)

            else:
                d_var = {}
        else:
            # 转义
            if iName == "设置请求头" and iParam != None:
                iParam = self._escape(iParam)
                iMethod = "header"
            else:
                if iQueryParam != None:
                    iQueryParam = self._escape2(iQueryParam)

                if iParam != None:
                    iParam = self._escape2(iParam)

                if iCheck == None:
                    iCheck = self._escape2(cf_default_iCheck)
                else:
                    iCheck = self._escape2(iCheck)

                if g_var != None:
                    d_var = self._escape(g_var)


            # 6, 输出当前变量
            if d_var != {}:
                print("d_var => " + str(d_var))
                # Color_PO.consoleColor("31", "33", "d_var => " + str(d_var), "")

            # 7, 解析接口，获取返回值
            res, d_var = reflection.run([iName, iPath, iMethod, iConsumes, iQueryParam, iParam, d_var])

            # 用于downFile情况
            if res == None:
                d_res = None
            else:
                d_res = json.loads(res)


            # 8, i检查接口返回值 iCheck（如 $.code=200）
            try:
                if d_res != None:
                    varSign = ""
                    dict1 = {}
                    d_iCheck = json.loads(iCheck)
                    # print(d_res)
                    # print(d_iCheck)  # {'$.code': 200}
                    if len(d_iCheck) == 1:
                        for k, v in d_iCheck.items():
                            iResValue = jsonpath.jsonpath(d_res, expr=k)
                            # print(iResValue)
                            # print(v)
                            if v == iResValue[0]:
                                self.setDb("iCheck", indexs, "Ok", "")
                            else:
                                dict1[k] = iResValue[0]
                                # print("111")
                                # print(dict1)
                                # print(type(dict1))
                                # print(str(json.dumps(dict1)))
                                self.setDb("iCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                                Color_PO.consoleColor("31", "31", "[Fail], " + str(iCheck) + " 不存在或格式错误！", "")
                    else:
                        for k, v in d_iCheck.items():
                            iResValue = jsonpath.jsonpath(d_res, expr=k)
                            if iResValue != False:   # 如果key不存在
                                if v != iResValue[0]:
                                    dict1[k] = iResValue[0]
                                    # print(str(json.dumps(dict1, ensure_ascii=False)))
                                    self.setDb("iCheck", indexs, "Fail", 'd_res => ' + str(json.dumps(dict1, ensure_ascii=False)) + ", 没找到 " + str(iCheck))
                                    varSign = "error"
                            else:
                                self.setDb("iCheck", indexs, "Fail", 'd_res => ' + str(d_res) + ', 没找到 "' + str(k) + '"')
                                Color_PO.consoleColor("31", "31", "[Fail], 没找到 " + str(k), "")
                                varSign = "error"
                        if varSign != "error":
                            self.setDb("iCheck", indexs, "Ok", "")
                        else:
                            Color_PO.consoleColor("31", "31", "[Fail], " + str(d_iCheck) + " 格式错误或与返回参数不一致！", "")

            except Exception as e:
                # print(e.__traceback__)
                Color_PO.consoleColor("31", "31", "[Error], [Exception]" + iCheck + "无法匹配！", "")
                self.setDb("iCheck", indexs, "Error", "[Exception], d_res => " + str(d_res))

            # 9, db检查表值
            try:
                dict1 = {}
                varSign = ""
                if dbCheck != None:
                    if "{{" in dbCheck:
                        for k in self.d_tmp:
                            if "{{" + k + "}}" in dbCheck:
                                dbCheck = str(dbCheck).replace("{{" + k + "}}", str(self.d_tmp[k]))
                    d_dbCheck = json.loads(dbCheck)

                    if len(d_dbCheck) == 1:
                        # 一个字典
                        for k, v in d_dbCheck.items():
                            if "select" in str(v) and "from" in str(v):
                                sql_value = Mysql_PO.execQuery(v)
                                if self.d_tmp[k] == sql_value[0][0]:
                                    self.setDb("dbCheck", indexs, "Ok", "")
                                else:
                                    dict1[k] = self.d_tmp[k]
                                    self.setDb("dbCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                                    Color_PO.consoleColor("31", "31", "[Fail], " + str(dbCheck) + " 不存在或错误！", "")
                            elif self.d_tmp[k] == v:
                                self.setDb("dbCheck", indexs, "Ok", "")
                            else:
                                dict1[k] = self.d_tmp[k]
                                self.setDb("dbCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                                Color_PO.consoleColor("31", "31", "[Fail], " + str(dbCheck) + " 不存在或错误！", "")
                    else:
                        # 多个字典
                        for k, v in d_dbCheck.items():
                            if "select" in str(v) and "from" in str(v):
                                sql_value = Mysql_PO.execQuery(v)
                                if self.d_tmp[k] != sql_value[0][0]:
                                    dict1[k] = self.d_tmp[k]
                                    varSign = "error"
                            elif self.d_tmp[k] != v:
                                dict1[k] = self.d_tmp[k]
                                varSign = "error"
                        if varSign == "error":
                            self.setDb("dbCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                            Color_PO.consoleColor("31", "31", "[Fail], " + str(dbCheck) + " 不存在或错误！", "")
                        else:
                            self.setDb("dbCheck", indexs, "Ok", "")
            except Exception as e:
                # print(e.__traceback__)
                Color_PO.consoleColor("31", "31", "[Fail], " + dbCheck + " 不存在或错误！", "")
                self.setDb("dbCheck", indexs, "Fail", "不存在或错误！")

            # f检查文件位置
            if fCheck != None:
                # /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/SAAS/i/data/sfb.xlsx
                # D:\\51\\python\\project\\PO\\FilePO\\test.txt
                if (os.path.isfile(fCheck)):
                    self.setDb("fCheck", indexs, "Ok", "")
                else:
                    self.setDb("fCheck", indexs, "Fail", "[Fail], 不存在或错误！")
                    Color_PO.consoleColor("31", "31", "[Fail], 不存在或错误！", "")

        # 全局变量
        if d_var != {}:
            # print(d_var)
            self.d_tmp = dict(self.d_tmp, **d_var)  # 合并字典，如key重复，则前面字典key值被后面字典所替换
            # print("g_var => " + str(self.d_tmp))
            Color_PO.consoleColor("31", "33", "g_var => " + str(self.d_tmp), "")
            # print("<font color='purple'>globalVar => " + str(self.d_tmp) + "</font>")
            self.setDb("g_var", indexs, "", str(json.dumps(d_var, ensure_ascii=False)))

        # header
        # if (iName == "设置请求头" or iName == "登录") and iParam != None :
        #     self.setDb("header", indexs, "", str(json.dumps(iParam, ensure_ascii=False)))

    def setDb(self, varCheck, id, varStatus, varMemo):

        ''' 写入数据库 '''
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

        # 'i结果'
        if varCheck == "iCheck":
            if varStatus == "Ok":
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[getIndex(l_m, "i结果")]))
            else:
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[getIndex(l_m, "i结果")]))
                self.df.update(pd.Series(varMemo, index=[id], name=l_m[getIndex(l_m, "备注")]))
        elif varCheck == "dbCheck":
            if varStatus == "Ok":
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[getIndex(l_m, "db结果")]))
            else:
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[getIndex(l_m, "db结果")]))
                self.df.update(pd.Series(varMemo, index=[id], name=l_m[getIndex(l_m, "备注")]))
        elif varCheck == "fCheck":
            if varStatus == "Ok":
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[getIndex(l_m, "f结果")]))
            else:
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[getIndex(l_m, "f结果")]))
                self.df.update(pd.Series(varMemo, index=[id], name=l_m[getIndex(l_m, "备注")]))
        elif varCheck == "header":
            self.df.update(pd.Series(varMemo, index=[id], name=l_m[getIndex(l_m, "备注")]))
        elif varCheck == "g_var":
            self.df.update(pd.Series(varMemo, index=[id], name=l_m[getIndex(l_m, "全局变量")]))


if __name__ == '__main__':

    run = Run()

    # 遍历用例
    for index in run.df.index:
        r = run.df.loc[index].values[0:]
        # print(r)
        Color_PO.consoleColor("31", "36", "\n" + str(r[0]) + ", " + str(r[4]) + " - " + str(r[5]) + " - " + str(r[6]) + " _" * 50, "")


        l_paths_method_consumes = []

        if r[3] == None:
            r3 = cf_default_project
        else:
            r3 = r[3]

        if r[6] == "设置全局变量" or r[6] == "设置请求头" or r[6] == "登录":
            run.result(index, r[6], "", "", "",  r[7], r[8], r[9], r[11], r[13], r[15])  # 读取数据库里的内容

        elif r[4] == None or r[5] == None:
            # 模块、接口名称
            Color_PO.consoleColor("31", "31", "[warning], 缺少模块或接口名称，程序已中断！", "")
            sys.exit()
        else:
            list1 = Openpyxl_PO.getColValueByCol([1, 2, 3, 4, 5], [], r3)
            for i in range(len(list1[0])):
                if list1[0][i] == r[4] and list1[1][i] == r[5]:
                    l_paths_method_consumes.append(list1[2][i])
                    l_paths_method_consumes.append(list1[3][i])
                    l_paths_method_consumes.append(list1[4][i])
                    break

            # 字段：index, 5用例名称，6路径，7方法，8方式，9query参数，10body参数，11i检查接口返回值，13db检查表值, 15f检查文件, 17全局变量
            if l_paths_method_consumes != []:
                # print(index, r[6], l_paths_method_consumes[0], l_paths_method_consumes[1], l_paths_method_consumes[2],  r[7], r[8], r[9], r[11], r[13], r[15])
                run.result(index, r[6], l_paths_method_consumes[0], l_paths_method_consumes[1], l_paths_method_consumes[2],  r[7], r[8], r[9], r[11], r[13], r[15])  # 读取数据库里的内容
            else:
                Color_PO.consoleColor("31", "31", "[warning], 模块或接口名称不匹配，程序已中断！", "")
                # print("[warning], excel表格的第" + str(index) + "模块或接口名称有错误，程序中断！")
                sys.exit()

        # pd.set_option('display.max_columns', None)  //显示所有列
        # run.df.loc[indexs]['i返回值'] = ""   # 不写入，因为内容过多表里可能报错

    run.df.to_sql(cf_test_db_table, con=Mysql_PO.getMysqldbEngine(), if_exists='replace', index=False)

    # 生成report.html
    # ['0编号', '1执行', '2类型', '3模块', '4名称', '5路径', '6方法', '7query参数'，'8body参数', '9担当者', '10i检查接口返回值', '11i结果', '12db检查表值', '13db结果', '14f检查文件', '15f结果', '16全局变量'，'17备注']
    # df = pd.read_sql(sql="select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s from %s" % (l_m[0], l_m[2], l_m[3], l_m[4], l_m[7], l_m[9], l_m[10], l_m[11], l_m[12], l_m[14], l_m[15], l_m[16], cf_test_db_table), con=Mysql_PO.getPymysqlEngine())
    # df = pd.read_sql(sql="select %s,%s,%s,%s,%s,%s,%s,%s from %s" % (l_m[0], l_m[2], l_m[3], l_m[4], l_m[11], l_m[13], l_m[15], l_m[17], cf_test_db_table), con=Mysql_PO.getPymysqlEngine())

    # ['编号', '1类型', '2模块', ‘3接口名称’，'4用例名称',  '10i结果',  '11db结果',  '12f结果', '16备注']
    df = pd.read_sql(sql="select `%s`,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s from %s" % (l_m[0], l_m[2], l_m[3], l_m[4], l_m[5], l_m[6], l_m[10], l_m[12], l_m[14], l_m[15], l_m[16], cf_test_db_table), con=Mysql_PO.getPymysqlEngine())

    pd.set_option('colheader_justify', 'center')  # 对其方式居中
    html = '''<html><head><title>''' + str(cf_default_rptTitle) + '''</title></head>
    <body><b><caption>''' + str(cf_default_rptTitle) + '''_''' + str(Time_PO.getDate()) + '''</caption></b><br><br>{table}</body></html>'''
    style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
    rptNameDate = "report/" + str(cf_default_rptName) + str(Time_PO.getDate()) + ".html"
    with open(rptNameDate, 'w') as f:
        f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        # f.write(html.format(table=df.to_html(classes="mystyle", col_space=50)))

    # df.to_html(htmlFile,col_space=100,na_rep="0")

    # 优化report.html, 去掉None、修改颜色
    html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
    html_text = str(html_text).replace("<td>None</td>", "<td></td>"). \
        replace(">" + str(l_m[0]) + "</th>", 'bgcolor="#90d7ec">' + str(l_m[0]) + '</th>'). \
        replace(">" + l_m[1] + "</th>", 'bgcolor="#90d7ec">' + l_m[1] + '</th>'). \
        replace(">" + l_m[2] + "</th>", 'bgcolor="#90d7ec">' + l_m[2] + '</th>'). \
        replace(">" + l_m[3] + "</th>", 'bgcolor="#90d7ec">' + l_m[3] + '</th>'). \
        replace(">" + l_m[4] + "</th>", 'bgcolor="#90d7ec">' + l_m[4] + '</th>'). \
        replace(">" + l_m[5] + "</th>", 'bgcolor="#90d7ec">' + l_m[5] + '</th>'). \
        replace(">" + l_m[6] + "</th>", 'bgcolor="#90d7ec">' + l_m[6] + '</th>'). \
        replace(">" + l_m[7] + "</th>", 'bgcolor="#90d7ec">' + l_m[7] + '</th>'). \
        replace(">" + l_m[8] + "</th>", 'bgcolor="#90d7ec">' + l_m[8] + '</th>'). \
        replace(">" + l_m[9] + "</th>", 'bgcolor="#90d7ec">' + l_m[9] + '</th>'). \
        replace(">" + l_m[10] + "</th>", 'bgcolor="#50b7c1">' + l_m[10] + '</th>'). \
        replace(">" + l_m[11] + "</th>", 'bgcolor="#90d7ec">' + l_m[11] + '</th>'). \
        replace(">" + l_m[12] + "</th>", 'bgcolor="#50b7c1">' + l_m[12] + '</th>'). \
        replace(">" + l_m[13] + "</th>", 'bgcolor="#90d7ec">' + l_m[13] + '</th>'). \
        replace(">" + l_m[14] + "</th>", 'bgcolor="#50b7c1">' + l_m[14] + '</th>'). \
        replace(">" + l_m[15] + "</th>", 'bgcolor="#90d7ec">' + l_m[15] + '</th>'). \
        replace(">" + l_m[16] + "</th>", 'bgcolor="#90d7ec">' + l_m[16] + '</th>'). \
        replace("<td>Ok</td>", '<td bgcolor="#00ae9d">Ok</td>'). \
        replace("<td>Fail</td>", '<td bgcolor="#f69c9f">Fail</td>'). \
        replace("<td>Error</td>", '<td bgcolor="#ed1941">Error</td>'). \
        replace("<td>反向</td>", '<td><font color="red">反向</font></td>')

    # 另存为report.html
    tf = open(rptNameDate, 'w', encoding='utf-8')
    tf.write(str(html_text))
    tf.close()


    # 判断是否打开报告
    if cf_switch_openRpt == "on":
        Sys_PO.openFile(rptNameDate)


    # 判断是否发邮件
    if cf_switch_sendEmail == "on":
        # 邮件正文是报告和附件报告
        Net_PO.sendEmail(cf_email_addresser, cf_email_to.split(","), cf_email_cc, str(cf_default_rptTitle) + str(Time_PO.getDate()),
                     "htmlFile", cf_email_head_html, "./report/" + str(cf_default_rptName) + str(Time_PO.getDate()) + ".html", cf_email_foot_html,
                     "./report/" + str(cf_default_rptName) + str(Time_PO.getDate()) + ".html"
                     )