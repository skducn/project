# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# 接口文档：http://192.168.0.237:8001/swagger-ui.html
# web页：http://192.168.0.243:8002/admin/notice/index  （测试243， 开发237）
# pip3 install jsonpath for cmd
# pip3 install pymysql for cmd
# pip3 install mysqlclient  (MySQLdb) for cmd
# css样式（外链） https://blog.csdn.net/qq_38316655/article/details/104663077
# css样式（内嵌） https://www.cnpython.com/qa/91356
# *****************************************************************
import sys
sys.path.append("../../../../")

import json, jsonpath
from PO.TimePO import *
Time_PO = TimePO()
import reflection
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from MysqlPO import *

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
        # Mysql_PO.xlsx2db("testcase2.xlsx", "testcase2", sheet_name="case")
        Mysql_PO.xlsx2db(xlsName, testTable, sheet_name=xlsSheetName)

        # 执行exec非N的用例
        self.df = pd.read_sql_query("select * from %s where exec is null" % (testTable), Mysql_PO.getMysqldbEngine())

        # 初始化数据，清空字段值（i返回值，i结果，s结果）
        Mysql_PO.execQuery("update %s set i返回值=null" % (testTable))
        Mysql_PO.execQuery("update %s set i结果=null" % (testTable))
        Mysql_PO.execQuery("update %s set s结果=null" % (testTable))


    def result(self, indexs, iName, iPath, iMethod, iParam, responseCheck, selectSql, selectSqlCheck, g_var):

        ''' 1替换参数，2解析接口，3检查值 '''

        # 1.1替换路径
        if "{{" in iPath:
            for k in self.d_tmp:
                if "{{" + k + "}}" in iPath:
                    iPath = str(iPath).replace("{{" + k + "}}", str(self.d_tmp[k]))
        # 1.2替换参数
        if iParam != None:
            if "{{" in iParam:
                for k in self.d_tmp :
                    if "{{" + k + "}}" in iParam:
                        iParam = str(iParam).replace("{{" + k + "}}", str(self.d_tmp[k]))

        # 1.3替换全局变量
        if g_var != None:
            if "{{" in g_var:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in g_var:
                        # g_var = str(g_var).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')
                        g_var = str(g_var).replace("{{" + k + "}}", str(self.d_tmp[k]))
            # d_var = json.loads(g_var)
            d_var = dict(eval(g_var))
            for k, v in d_var.items():
                if "str(" in str(v):
                    d_var[k] = eval(d_var[k])
        else:
            d_var ={}

        # 1.4替换检查返回值
        if responseCheck != None:
            if "{{" in responseCheck:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in responseCheck:
                        responseCheck = str(responseCheck).replace("{{" + k + "}}", '"' + str(self.d_tmp[k]) + '"')

        print("curr_var => " + str(d_var))

        # 2解析接口 （返回值）
        res, d_var = reflection.run([iName, iPath, iMethod, iParam, d_var])
        # 用于downFile情况
        if res == None:
            d_res = None
        else:
            d_res = json.loads(res)


        # 3i检查返回值 iCheckResponse（如 $.code=200）
        try:
            if d_res != None:
                varSign = ""
                d_responseCheck = json.loads(responseCheck)
                if len(d_responseCheck) == 1:
                    for k, v in d_responseCheck.items():
                        iResValue = jsonpath.jsonpath(d_res, expr=k)

                        if v == iResValue[0]:
                            # print("\n<font color='blue'>responseCheck => " + str(k) + " = " + str(v) + " </font>")
                            self.setDb(indexs, "Ok", None)
                        else:
                            self.setDb(indexs,  "预期值: " + str(v) + "，实测值: " + str(iResValue[0]), None)
                            # assert v == iResValue[0], "预期值: " + str(v) + "，实测值: " + iResValue
                else:
                    for k, v in d_responseCheck.items():
                        iResValue = jsonpath.jsonpath(d_res, expr=k)
                        if v == iResValue[0]:
                            pass
                            # print("\n<font color='blue'>responseCheck => " + str(k) + " = " + str(v) + " </font>")
                        else:
                            # print("\n<font color='red'>responseCheck => " + str(k) + " != " + str(v) + " </font>")
                            varSign = "error"
                    if varSign == "error":
                        self.setDb(indexs,  "预期值: " + str(v) + "，实测值: " + str(iResValue[0]), None)
                        # assert v == iResValue[0], "预期值: " + str(v) + "，实测值: " + iResValue
                    else:
                        self.setDb(indexs,  "Ok", None)

        except Exception as e:
            print(e.__traceback__)
            assert 1 == 0, "【i检查返回值】列有误，请检查参数或变量是否引用正确！"


        # s表值
        if selectSql != None:
            if "{{" in selectSql:
                for k in self.d_tmp:
                    if "{{" + k + "}}" in selectSql:
                        selectSql = str(selectSql).replace("{{" + k + "}}", str(self.d_tmp[k]))
            try:
                # 转全局变量
                d_sql = json.loads(selectSql)
                for k, v in d_sql.items():
                    sql_value = Mysql_PO.execQuery(v)
                    self.d_tmp[k] = sql_value[0][0]
                    # print("\n<font color='green'>selectSql => " + str(k) + " = " + str(sql_value[0][0]) + " </font>")
            except Exception as e:
                print(e.__traceback__)
                assert 1 == 0, "【s表值】有误，请检查参数或变量是否引用正确！"

        # s检查表值
        try:
            varSign = ""
            if selectSqlCheck != None:
                d_selectSqlCheck = json.loads(selectSqlCheck)
                if len(d_selectSqlCheck) == 1:
                    for k, v in d_selectSqlCheck.items():
                        if self.d_tmp[k] == v:
                            # print("\n<font color='green'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                            self.setDb(indexs, None, "Ok")
                        else:
                            # print("\n<font color='red'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                            self.setDb(indexs, None, "Fail")
                else:
                    for k, v in d_selectSqlCheck.items():
                        if self.d_tmp[k] == v:
                            pass
                            # print("\n<font color='green'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                        else:
                            # print("\n<font color='red'>selectSqlCheck => " + str(k) + " = " + str(v) + " </font>")
                            varSign = "error"
                    if varSign == "error":
                        self.setDb(indexs, None, "Fail")
                    else:
                        self.setDb(indexs, None, "Ok")
        except Exception as e:
            print(e.__traceback__)
            assert 1 == 0, "【s检查表值】列有误，请检查参数或变量是否引用正确！"
        # f检查文件位置


        # 当前变量
        # print("\ncurrVar => " + str(d_var))

        # 全局变量
        self.d_tmp = dict(self.d_tmp, **d_var)  # 合并字典，如key重复，则前面字典key值被后面字典所替换
        print("global_var => " + str(self.d_tmp))

        # print("\n<font color='purple'>globalVar => " + str(self.d_tmp) + "</font>")



    def setDb(self, id, iResult, sResult):

        ''' 写入数据库 '''

        if iResult != None:
            self.df.loc[id]['i结果'] = iResult

        if sResult != None:
            self.df.loc[id]['s结果'] = sResult



if __name__ == '__main__':

    run = Run()

    # 遍历所有用例
    for indexs in run.df.index:
        # print(run.df.loc[indexs].values[0:-1])
        r = run.df.loc[indexs].values[0:-1]

        # 参数：数据库表序号，名称，路径，方法，参数，i检查返回值，s表值，s检查表值,全局变量
        # print("- -" *100)
        print(str(indexs) + ", " + str(r[3]) + "_" *100)
        run.result(indexs, r[3], r[4], r[5], r[6], r[9], r[11], r[12], r[16])

        run.df.loc[indexs]['i返回值'] = ""   # 不写入，因为内容过多表里可能报错
        run.df.to_sql(testTable, con=Mysql_PO.getMysqldbEngine(), if_exists='replace', index=False)

    # 生成report.html
    df = pd.read_sql(sql="select 类型,模块,名称,参数,i结果,s表值,s检查表值,s结果,全局变量 from %s" % (testTable), con=Mysql_PO.getPymysqlEngine())
    pd.set_option('colheader_justify', 'center')  # 对其方式居中
    html = '''<html><head><title>接口自动化报告</title></head>    
    <body><b><caption>招远疫情防控接口自动化报告''' + str(Time_PO.getDate_divide()) + '''</caption></b><br><br>{table}</body></html>'''
    style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
    rptName = "report/" + str(rptName) + str(Time_PO.getDatetime()) + ".html"
    with open(rptName, 'w') as f:
        f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100)))
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


