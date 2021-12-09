# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2021-11-15
# Description   : 招远防疫 epidemic 接口自动化
# pip3 install flask_bootstrap
# *****************************************************************
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import pymysql
app = Flask(__name__)
bootstrap = Bootstrap(app)
from PO.MysqlPO import *

Mysql_PO = MysqlPO("192.168.0.234", "root", "123456", "epd", 3306)  # 测试

@app.route('/')
def index():


    Mysql_PO.cur.execute('select * from test1')
    l_result = Mysql_PO.cur.fetchall()
    print(l_result)

    # conn = pymysql.connect(host='192.168.0.243', user='root', password='123456', db='epd', charset='utf8')
    # cur = conn.cursor()
    # sql = "SELECT * FROM user"
    # cur.execute(sql)
    # u = cur.fetchall()
    # conn.close()
    return render_template('index.html', u=l_result)
if __name__ == '__main__':
    app.run()


