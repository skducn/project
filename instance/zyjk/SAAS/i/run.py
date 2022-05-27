# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : saas高血压接口自动化
# 接口文档：http://192.168.0.238:8001/swagger-ui.html
# web页：
# pip3 install jsonpath for cmd
# pip3 install pymysql for cmd
# pip3 install mysqlclient  (MySQLdb) for cmd
# css样式（外链） https://blog.csdn.net/qq_38316655/article/details/104663077
# css样式（内嵌） https://www.cnpython.com/qa/91356
# *****************************************************************
import sys,platform
sys.path.append("../../../../")

import json, jsonpath
from PO.TimePO import *
Time_PO = TimePO()
import reflection
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from MysqlPO import *
from PO.NetPO import *
Net_PO = NetPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.SysPO import *
Sys_PO = SysPO()
xlsName = localReadConfig.get_system("xlsName")
rptName = localReadConfig.get_system("rptName")
xlsSheetName = localReadConfig.get_system("xlsSheetName")

if localReadConfig.get_env("switchENV") == "test":
    db_ip = localReadConfig.get_test("db_ip")
    db_username = localReadConfig.get_test("db_username")
    db_password = localReadConfig.get_test("db_password")
    db_port = localReadConfig.get_test("db_port")
    db_database = localReadConfig.get_test("db_database")
    testTable = localReadConfig.get_test("testTable")
else:
    db_ip = localReadConfig.get_dev("db_ip")
    db_username = localReadConfig.get_dev("db_username")
    db_password = localReadConfig.get_dev("db_password")
    db_port = localReadConfig.get_dev("db_port")
    db_database = localReadConfig.get_dev("db_database")
    testTable = localReadConfig.get_test("testTable")

Mysql_PO = MysqlPO(db_ip, db_username, db_password, db_database, db_port)

from DictPO import *
Dict_PO = DictPO()
from DataPO import *
Data_PO = DataPO()
from HtmlPO import *
Html_PO = HtmlPO()
import pandas as pd


class Run:

    def __init__(self):

        # 全局字典
        self.d_tmp = {}

        # 导入数据库表
        Mysql_PO.xlsx2db(xlsName, testTable, sheet_name=xlsSheetName)

        # 执行exec非N的用例
        self.df = pd.read_sql_query("select * from %s where exec is null" % (testTable), Mysql_PO.getMysqldbEngine())

        # 初始化数据，清空字段值（i返回值，i结果，s结果）
        Mysql_PO.execQuery("update %s set i返回值=null" % (testTable))
        Mysql_PO.execQuery("update %s set i结果=null" % (testTable))
        Mysql_PO.execQuery("update %s set s结果=null" % (testTable))


    def result(self, indexs, iName, iPath, iMethod, iParam, responseCheck, selectSql, selectSqlCheck, fileCheck, g_var):

        ''' 1转义参数，2解析接口，3检查值 '''
        # 参数：数据库表序号，名称，路径，方法，参数，i检查返回值，s表值，s检查表值, f检查文件位置，全局变量

        if iName in "初始化全局变量":
            if g_var != None:
                # 转义全局变量
                if "{{" in g_var:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in g_var:
                            g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
                d_var = dict(eval(g_var))
                print(d_var)
                for k, v in d_var.items():
                    # 其他封装函数返回内容转字符串，如str(Data_PO.autoNum(3))
                    if "str(" in str(v):
                        d_var[k] = eval(d_var[k])
                    if "select" in v and "from" in v :
                        sql_value = Mysql_PO.execQuery(v)
                        d_var[k]= sql_value[0][0]
                # sys.exit(0)


            else:
                d_var = {}
        else:
            # 1.1 转义路径
            if "{{" in iPath:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in iPath:
                        iPath = str(iPath).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # 1.2 转义参数
            if iParam != None:
                if "{{" in iParam:
                    for k in self.d_tmp :
                        if "{{" + k + "}}" in iParam:
                            iParam = str(iParam).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # 1.3 转义全局变量
            if g_var != None:
                if "{{" in g_var:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in g_var:
                            # g_var = str(g_var).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')
                            g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
                d_var = dict(eval(g_var))
                for k, v in d_var.items():
                    if "str(" in str(v):
                        d_var[k] = eval(d_var[k])
            else:
                d_var = {}
            # 1.4 转义i检查返回值
            if responseCheck != None:
                if "{{" in responseCheck:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in responseCheck:
                            responseCheck = str(responseCheck).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')
            # 1.5 转义s表值
            if selectSql != None:
                if "{{" in selectSql:
                    for k in self.d_tmp:
                        if "{{" + k + "}}" in selectSql:
                            selectSql = str(selectSql).replace("{{" + k + "}}", str(self.d_tmp[k]))
                try:
                    # 加入全局变量
                    d_sql = json.loads(selectSql)
                    for k, v in d_sql.items():
                        sql_value = Mysql_PO.execQuery(v)
                        self.d_tmp[k] = sql_value[0][0]
                except Exception as e:
                    # print(e.__traceback__)
                    Sys_PO.outMsg2("error", str(sys._getframe(0).f_lineno), "[s表值]格式有误！", "")
                    os._exit(0)

            # 当前变量
            print("curr_var => " + str(d_var))

            # 2解析接口 （返回值）
            res, d_var = reflection.run([iName, iPath, iMethod, iParam, d_var])
            # 用于downFile情况
            if res == None:
                d_res = None
            else:
                d_res = json.loads(res)


            # 3, i检查返回值 iCheckResponse（如 $.code=200）
            try:
                if d_res != None:
                    varSign = ""
                    d_responseCheck = json.loads(responseCheck)
                    if len(d_responseCheck) == 1:
                        for k, v in d_responseCheck.items():
                            iResValue = jsonpath.jsonpath(d_res, expr=k)
                            if v == iResValue[0]:
                                # print("\n<font color='blue'>responseCheck => " + str(k) + " = " + str(v) + " </font>")
                                self.setDb(indexs, "Ok", None, None)
                            else:
                                # self.setDb(indexs, "Fail", None)
                                self.setDb(indexs,  '{"' + str(k) + '":' + str(iResValue[0]) + "}", None, None)
                                # assert v == iResValue[0], "预期值: " + str(v) + "，实测值: " + str(iResValue[0])
                    else:
                        for k, v in d_responseCheck.items():
                            iResValue = jsonpath.jsonpath(d_res, expr=k)
                            # print(iResValue)
                            if iResValue != False:   # 如果key不存在
                                if v != iResValue[0]:
                                    self.setDb(indexs,  '{"' + str(k) + '":' + str(iResValue[0]) + "}", None, None)
                                    # print("\n<font color='red'>responseCheck => " + str(k) + " != " + str(v) + " </font>")
                                    varSign = "error"
                            else:
                                self.setDb(indexs, '没找到 "' + str(k) + '"', None, None)
                                varSign = "error"
                        if varSign != "error":
                            self.setDb(indexs,  "Ok", None, None)
            except Exception as e:
                # print(e.__traceback__)
                Color_PO.consoleColor("31", "31", "[ERROR], [i检查返回值]列格式有误！", "")
                self.setDb(indexs, 'err,[i检查返回值]列格式有误！', None, None)


            # s检查表值
            try:
                dict1 = {}
                varSign = ""
                if selectSqlCheck != None:
                    d_selectSqlCheck = json.loads(selectSqlCheck)
                    if len(d_selectSqlCheck) == 1:
                        for k, v in d_selectSqlCheck.items():
                            if self.d_tmp[k] == v:
                                # print("\n<font color='green'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                                self.setDb(indexs, None, "Ok", None)
                            else:
                                # print("\n<font color='red'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                                # self.setDb(indexs, None, "Fail", None)
                                self.setDb(indexs, None, '{"' + str(k) + '": ' + str(self.d_tmp[k]) + '}', None)
                    else:
                        for k, v in d_selectSqlCheck.items():
                            if self.d_tmp[k] != v:
                                dict1[k] = self.d_tmp[k]
                                varSign = "error"
                        if varSign == "error":
                            # print(dict1)
                            self.setDb(indexs, None, json.dumps(dict1), None)
                        else:
                            self.setDb(indexs, None, "Ok", None)
            except Exception as e:
                # print(e.__traceback__)
                Color_PO.consoleColor("31", "31", "[ERROR], [s检查表值]列格式有误！", "")
                self.setDb(indexs, None, 'err,[s检查表值]列格式有误！')

            # f检查文件位置
            if fileCheck != None:
                # /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/SAAS/i/data/sfb.xlsx
                # D:\\51\\python\\project\\PO\\FilePO\\test.txt

                if (os.path.isfile(fileCheck)):
                    self.setDb(indexs, None, None, "Ok")
                else:
                    self.setDb(indexs, None, None, "Fail")

        # 全局变量
        self.d_tmp = dict(self.d_tmp, **d_var)  # 合并字典，如key重复，则前面字典key值被后面字典所替换
        print("global_var => " + str(self.d_tmp))
        # print("\n<font color='purple'>globalVar => " + str(self.d_tmp) + "</font>")


    def setDb(self, id, iResult, sResult, fResult):

        ''' 写入数据库 '''
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy

        if iResult != None:
            self.df.update(pd.Series(iResult, index=[id], name='i结果'))

        if sResult != None:
            self.df.update(pd.Series(sResult, index=[id], name='s结果'))

        if fResult != None:
            self.df.update(pd.Series(fResult, index=[id], name='f结果'))


if __name__ == '__main__':

    run = Run()

    # 遍历所有用例

    for indexs in run.df.index:
        r = run.df.loc[indexs].values[0:-1]
        print("\n" + str(r[0]) + ", " + str(r[3]) + " - " + str(r[4]) + " _" *50)

        # 参数：数据库表序号，名称，路径，方法，参数，i检查返回值，s表值，s检查表值, f检查文件位置, 全局变量
        run.result(indexs, r[4], r[5], r[6], r[7], r[10], r[12], r[13], r[15], r[17])
        # pd.set_option('display.max_columns', None)  //显示所有列
        # run.df.loc[indexs]['i返回值'] = ""   # 不写入，因为内容过多表里可能报错

    run.df.to_sql(testTable, con=Mysql_PO.getMysqldbEngine(), if_exists='replace', index=False)

    # 生成report.html
    df = pd.read_sql(sql="select id, 类型,模块,名称,路径,方法,参数,i检查返回值,i结果,s表值,s检查表值,s结果,f检查文件位置,f结果,全局变量 from %s" % (testTable), con=Mysql_PO.getPymysqlEngine())
    pd.set_option('colheader_justify', 'center')  # 对其方式居中
    html = '''<html><head><title>接口自动化报告</title></head>
    <body><b><caption>招远疫情防控接口自动化报告''' + str(Time_PO.getDate()) + '''</caption></b><br><br>{table}</body></html>'''
    style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
    rptName = "report/" + str(rptName) + str(Time_PO.getDate()) + ".html"
    with open(rptName, 'w') as f:
        f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        # f.write(html.format(table=df.to_html(classes="mystyle", col_space=50)))

    # df.to_html(htmlFile,col_space=100,na_rep="0")

    # 优化report.html
    html_text = BeautifulSoup(open(rptName), features='html.parser')
    # 去掉None、修改颜色
    # 绿色 = 00E400，黄色 = FFFF00，橙色 = FF7E00，红色 = FF0000，粉色 = 99004C，褐色 =7E0023,'c6efce = 淡绿', '006100 = 深绿'，'ffffff=白色', '000000=黑色'，'ffeb9c'= 橙色
    html_text = str(html_text).replace("<td>None</td>", "<td></td>").replace(">i结果</th>", 'bgcolor="#ffeb9c">i结果</th>').replace(">s结果</th>", 'bgcolor="#ffeb9c">s结果</th>').\
        replace("<td>Ok</td>", '<td bgcolor="#c6efce">Ok</td>').replace("<td>Fail</td>", '<td bgcolor="#ff0000">Fail</td>')

    # 另存为report.html
    tf = open(rptName, 'w', encoding='utf-8')
    tf.write(str(html_text))
    tf.close()

    if platform.system() == 'Darwin':
        os.system("open ./" + rptName)
    if platform.system() == 'Windows':
        os.system("start ./" + rptName)
    # #
    # # # Net_PO.sendEmail("令狐冲", 'skducn@163.com', "h.jin@zy-healthtech.com",
    # # #                  "招远疫情防控接口自动化报告" + str(Time_PO.getDate_minus()),
    # # #                  "你好，\n\n以下是本次自动化接口测试结果，请查阅。\n\n\n\n这是一封自动生成的email，请勿回复，如有打扰请谅解。\n测试组\nBest Regards",
    # # #                  rptName,
    # # #                  "","", "")