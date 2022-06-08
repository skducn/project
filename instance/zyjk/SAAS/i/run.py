# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : saas高血压接口自动化
# 接口文档：http://192.168.0.238:8001/swagger-ui.html
# web页：
# pip3 install jsonpath
# pip3 install pymysql
# pip3 install mysqlclient  (MySQLdb)
# css样式（外链） https://blog.csdn.net/qq_38316655/article/details/104663077
# css样式（内嵌） https://www.cnpython.com/qa/91356
# *****************************************************************
import sys, platform, json, jsonpath
import reflection
import readConfig as readConfig
import pandas as pd

# sys.path.append("../../../")

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

localReadConfig = readConfig.ReadConfig()
xlsName = localReadConfig.get_system("xlsName")
rptName = localReadConfig.get_system("rptName")
rptTitle = localReadConfig.get_system("rptTitle")
xlsSheetName = localReadConfig.get_system("xlsSheetName")
varAddresser = localReadConfig.get_email("varAddresser")
varTo = localReadConfig.get_email("varTo")
varCc = localReadConfig.get_email("varCc")
if varCc != 'None':
    print(varCc.split(","))
else:
    varCc = None
# ConfigParser的value如果包含\r\n的话都会被当成普通字符处理（自动转义成\\r\\n），只有编译器在编译时才会对\r\n等进行转义，只需 str.replace("\\n", "\n")即可。
varContent = localReadConfig.get_email("varContent")
varContent = varContent.replace("\\n", "\n")
varHead = localReadConfig.get_email("varHead")
varHead = varHead.replace("\\n", "\n")
varFoot = localReadConfig.get_email("varFoot")
varFoot = varFoot.replace("\\n", "\n")
varContent_html = localReadConfig.get_email("varContent_html")
varHead_html = localReadConfig.get_email("varHead_html")
varFoot_html = localReadConfig.get_email("varFoot_html")

if localReadConfig.get_env("switchENV") == "test":
    db_ip = localReadConfig.get_test("db_ip")
    db_username = localReadConfig.get_test("db_username")
    db_password = localReadConfig.get_test("db_password")
    db_port = localReadConfig.get_test("db_port")
    db_database = localReadConfig.get_test("db_database")
    db_table = localReadConfig.get_test("db_table")
else:
    db_ip = localReadConfig.get_dev("db_ip")
    db_username = localReadConfig.get_dev("db_username")
    db_password = localReadConfig.get_dev("db_password")
    db_port = localReadConfig.get_dev("db_port")
    db_database = localReadConfig.get_dev("db_database")
    db_table = localReadConfig.get_test("db_table")

from PO.MysqlPO import *
Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)

# excel导入数据库表
Mysql_PO.xlsx2db(xlsName, db_table, sheet_name=xlsSheetName)
# 获取表格字段列表
l_m = Mysql_PO.getTableField(db_table)
# print(l_m)

class Run:

    def __init__(self):

        # 全局字典
        self.d_tmp = {}


        # 执行用例
        # 参考：https://zhuanlan.zhihu.com/p/281422144
        self.df = pd.read_sql_query("select * from %s where %s is null " % (db_table, l_m[1]), Mysql_PO.getMysqldbEngine())


        # # 初始化数据，清空字段值（i返回值，i结果，s结果）
        # Mysql_PO.execQuery("update %s set i返回值=null" % (db_table))
        # Mysql_PO.execQuery("update %s set i结果=null" % (db_table))
        # Mysql_PO.execQuery("update %s set s结果=null" % (db_table))


    def result(self, indexs, iName, iPath, iMethod, iParam, iCheck, dbCheck, fCheck, g_var):

        # 参数：数据库表里数据索引，名称，路径，方法，参数，i检查接口返回值，s检查db表值, f检查文件, 全局变量
        # 1, 初始化设置全局变量
        if iName == "设置全局变量":
            if g_var != None:
                # 转义全局变量
                if "{{" in g_var:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in g_var:
                            g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
                d_var = dict(eval(g_var))
                # print(d_var)
                for k, v in d_var.items():
                    # 其他封装函数返回内容转字符串，如str(Data_PO.autoNum(3))
                    if "str(" in str(v):
                        d_var[k] = eval(d_var[k])
                    if "select" in v and "from" in v :
                        sql_value = Mysql_PO.execQuery(v)
                        d_var[k] = sql_value[0][0]
            else:
                d_var = {}
        elif iName == "设置请求头":
            if g_var != None:
                # 转义全局变量
                if "{{" in g_var:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in g_var:
                            g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
                d_var = dict(eval(g_var))
                # print(d_var)
                for k, v in d_var.items():
                    # 其他封装函数返回内容转字符串，如str(Data_PO.autoNum(3))
                    if "str(" in str(v):
                        d_var[k] = eval(d_var[k])
                    if "select" in v and "from" in v :
                        sql_value = Mysql_PO.execQuery(v)
                        d_var[k] = sql_value[0][0]
                reflection.run([iName, iPath, iMethod, iParam, d_var])
            else:
                d_var = {}


        else:
            # 2, 转义路径
            if "{{" in iPath:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in iPath:
                        iPath = str(iPath).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # 3, 转义参数
            if iParam != None:
                if "{{" in iParam:
                    for k in self.d_tmp :
                        if "{{" + k + "}}" in iParam:
                            iParam = str(iParam).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # 4, 转义全局变量
            if g_var != None:
                if "{{" in g_var:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in g_var:
                            g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
                d_var = dict(eval(g_var))
                for k, v in d_var.items():
                    if "str(" in str(v):
                        d_var[k] = eval(d_var[k])
                    if "select" in v and "from" in v :
                        sql_value = Mysql_PO.execQuery(v)
                        d_var[k] = sql_value[0][0]
            else:
                d_var = {}
            # 5, 转义i检查接口返回值
            if iCheck != None:
                if "{{" in iCheck:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in iCheck:
                            iCheck = str(iCheck).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')


            # 6, 输出当前变量
            print("curr_var => " + str(d_var))

            # 7, 解析接口，获取返回值
            res, d_var = reflection.run([iName, iPath, iMethod, iParam, d_var])
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
                    if len(d_iCheck) == 1:
                        for k, v in d_iCheck.items():
                            iResValue = jsonpath.jsonpath(d_res, expr=k)
                            if v == iResValue[0]:
                                self.setDb("iCheck", indexs, "Ok", "")
                            else:
                                dict1[k] = iResValue[0]
                                # print(str(json.dumps(dict1)))
                                self.setDb("iCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                                Color_PO.consoleColor("31", "31", "[ERROR], " + str(iCheck) + " 不存在或格式错误！", "")
                    else:
                        for k, v in d_iCheck.items():
                            iResValue = jsonpath.jsonpath(d_res, expr=k)
                            if iResValue != False:   # 如果key不存在
                                if v != iResValue[0]:
                                    dict1[k] = iResValue[0]

                                    self.setDb("iCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                                    varSign = "error"
                            else:
                                self.setDb("iCheck", indexs, "Fail", '没找到 "' + str(k) + '"')
                                Color_PO.consoleColor("31", "31", "[ERROR], 没找到" + str(k), "")
                                varSign = "error"
                        if varSign != "error":
                            self.setDb("iCheck", indexs, "Ok", "")
                        else:
                            Color_PO.consoleColor("31", "31", "[ERROR], " + str(iCheck) + " 不存在或格式错误！", "")

            except Exception as e:
                # print(e.__traceback__)
                Color_PO.consoleColor("31", "31", "[ERROR], " + iCheck + "不存在或错误！", "")
                self.setDb("iCheck", indexs, "Fail", "不存在或错误！")

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
                                    Color_PO.consoleColor("31", "31", "[ERROR], " + str(dbCheck) + " 不存在或错误！", "")
                            elif self.d_tmp[k] == v:
                                self.setDb("dbCheck", indexs, "Ok", "")
                            else:
                                dict1[k] = self.d_tmp[k]
                                self.setDb("dbCheck", indexs, "Fail", str(json.dumps(dict1, ensure_ascii=False)))
                                Color_PO.consoleColor("31", "31", "[ERROR], " + str(dbCheck) + " 不存在或错误！", "")
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
                            Color_PO.consoleColor("31", "31", "[ERROR], " + str(dbCheck) + " 不存在或错误！", "")
                        else:
                            self.setDb("dbCheck", indexs, "Ok", "")
            except Exception as e:
                # print(e.__traceback__)
                Color_PO.consoleColor("31", "31", "[ERROR], " + dbCheck + " 不存在或错误！", "")
                self.setDb("dbCheck", indexs, "Fail", "不存在或错误！")

            # f检查文件位置
            if fCheck != None:
                # /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/SAAS/i/data/sfb.xlsx
                # D:\\51\\python\\project\\PO\\FilePO\\test.txt
                if (os.path.isfile(fCheck)):
                    self.setDb("fCheck", indexs, "Ok", "")
                else:
                    self.setDb("fCheck", indexs, "Fail", "[ERROR], 不存在或错误！")
                    Color_PO.consoleColor("31", "31", "[ERROR], 不存在或错误！", "")

        # 全局变量
        self.d_tmp = dict(self.d_tmp, **d_var)  # 合并字典，如key重复，则前面字典key值被后面字典所替换
        print("global_var => " + str(self.d_tmp))
        # print("<font color='purple'>globalVar => " + str(self.d_tmp) + "</font>")


    def setDb(self, varCheck, id, varStatus, varMemo):

        ''' 写入数据库 '''
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

        # 'i结果'
        if varCheck == "iCheck":
            if varStatus == "Ok":
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[10]))
            else:
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[10]))
                self.df.update(pd.Series(varMemo, index=[id], name=l_m[16]))  # '错误写入备注'
        elif varCheck == "dbCheck":
            if varStatus == "Ok":
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[12]))
            else:
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[12]))
                self.df.update(pd.Series(varMemo, index=[id], name=l_m[16]))  # '错误写入备注'
        elif varCheck == "fCheck":
            if varStatus == "Ok":
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[14]))
            else:
                self.df.update(pd.Series(varStatus, index=[id], name=l_m[14]))
                self.df.update(pd.Series(varMemo, index=[id], name=l_m[16]))  # '错误写入备注'


if __name__ == '__main__':

    run = Run()

    # 遍历用例
    for indexs in run.df.index:
        r = run.df.loc[indexs].values[0:]
        Color_PO.consoleColor("31", "36", "\n" + str(r[0]) + ", " + str(r[3]) + " - " + str(r[4]) + " _" * 50, "")

        # 参数：数据库表里数据索引，名称，路径，方法，参数，i检查接口返回值，db检查表值, f检查文件, 全局变量
        run.result(indexs, r[4], r[5], r[6], r[7], r[9], r[11], r[13], r[15])
        # pd.set_option('display.max_columns', None)  //显示所有列
        # run.df.loc[indexs]['i返回值'] = ""   # 不写入，因为内容过多表里可能报错

    run.df.to_sql(db_table, con=Mysql_PO.getMysqldbEngine(), if_exists='replace', index=False)

    # 生成report.html
    # ['0编号', '1执行', '2类型', '3模块', '4名称', '5路径', '6方法', '7参数', '8担当者', '9i检查接口返回值', '10i结果', '11db检查表值', '12db结果', '13f检查文件', '14f结果', '15全局变量'，'16备注']
    df = pd.read_sql(sql="select %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s from %s" % (l_m[0], l_m[2], l_m[3], l_m[4], l_m[7], l_m[9], l_m[10], l_m[11], l_m[12], l_m[14], l_m[15], l_m[16], db_table), con=Mysql_PO.getPymysqlEngine())

    pd.set_option('colheader_justify', 'center')  # 对其方式居中
    html = '''<html><head><title>''' + str(rptTitle) + '''</title></head>
    <body><b><caption>''' + str(rptTitle) + ''' ( ''' + str(Time_PO.getDate()) + ''' )</caption></b><br><br>{table}</body></html>'''
    style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
    rptNameDate = "report/" + str(rptName) + str(Time_PO.getDate()) + ".html"
    with open(rptNameDate, 'w') as f:
        f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        # f.write(html.format(table=df.to_html(classes="mystyle", col_space=50)))

    # df.to_html(htmlFile,col_space=100,na_rep="0")

    # 优化report.html
    # 去掉None、修改颜色
    # https://bbs.bianzhirensheng.com/color01.html
    html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
    html_text = str(html_text).replace("<td>None</td>", "<td></td>"). \
        replace(">" + l_m[0] + "</th>", 'bgcolor="#90d7ec">' + l_m[0] + '</th>'). \
        replace(">" + l_m[1] + "</th>", 'bgcolor="#90d7ec">' + l_m[1] + '</th>'). \
        replace(">" + l_m[2] + "</th>", 'bgcolor="#90d7ec">' + l_m[2] + '</th>'). \
        replace(">" + l_m[3] + "</th>", 'bgcolor="#90d7ec">' + l_m[3] + '</th>'). \
        replace(">" + l_m[4] + "</th>", 'bgcolor="#90d7ec">' + l_m[4] + '</th>'). \
        replace(">" + l_m[5] + "</th>", 'bgcolor="#90d7ec">' + l_m[5] + '</th>'). \
        replace(">" + l_m[6] + "</th>", 'bgcolor="#90d7ec">' + l_m[6] + '</th>'). \
        replace(">" + l_m[7] + "</th>", 'bgcolor="#90d7ec">' + l_m[7] + '</th>'). \
        replace(">" + l_m[8] + "</th>", 'bgcolor="#90d7ec">' + l_m[8] + '</th>'). \
        replace(">" + l_m[9] + "</th>", 'bgcolor="#90d7ec">' + l_m[9] + '</th>'). \
        replace(">" + l_m[10] + "</th>", 'bgcolor="#90d7ec">' + l_m[10] + '</th>'). \
        replace(">" + l_m[11] + "</th>", 'bgcolor="#90d7ec">' + l_m[11] + '</th>'). \
        replace(">" + l_m[12] + "</th>", 'bgcolor="#90d7ec">' + l_m[12] + '</th>'). \
        replace(">" + l_m[13] + "</th>", 'bgcolor="#90d7ec">' + l_m[13] + '</th>'). \
        replace(">" + l_m[14] + "</th>", 'bgcolor="#90d7ec">' + l_m[14] + '</th>'). \
        replace(">" + l_m[15] + "</th>", 'bgcolor="#90d7ec">' + l_m[15] + '</th>'). \
        replace(">" + l_m[16] + "</th>", 'bgcolor="#90d7ec">' + l_m[16] + '</th>'). \
        replace("<td>Ok</td>", '<td bgcolor="#c6efce">Ok</td>'). \
        replace("<td>Fail</td>", '<td bgcolor="#f69c9f">Fail</td>'). \
        replace("<td>异常</td>", '<td><font color="red">异常</font></td>')

    # 另存为report.html
    tf = open(rptNameDate, 'w', encoding='utf-8')
    tf.write(str(html_text))
    tf.close()

    if platform.system() == 'Darwin':
        os.system("open ./" + rptNameDate)
    if platform.system() == 'Windows':
        os.system("start ./" + rptNameDate)

    # 邮件正文是文本
    # Net_PO.sendEmail(varAddresser, varTo.split(","), varCc, str(rptTitle) + str(Time_PO.getDate()),
    #                  "plain", varHead, varContent, varFoot,
    #                  "./report/" + str(rptName) + str(Time_PO.getDate()) + ".html"
    #                  )

    # 邮件正文是html
    Net_PO.sendEmail(varAddresser, varTo.split(","), varCc, str(rptTitle) + str(Time_PO.getDate()),
                     "htmlFile", varHead_html, "./report/" + str(rptName) + str(Time_PO.getDate()) + ".html", varFoot_html,
                     "./report/" + str(rptName) + str(Time_PO.getDate()) + ".html"
                     )