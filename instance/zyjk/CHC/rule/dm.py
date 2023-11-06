# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# ***************************************************************u**


# import pyodbc
# conn = pyodbc.connect('DRIVER={DMODBC};SERVER=192.168.0.234;DATABASE=PHUSERS;UID=PHUSERS;PWD=Zy_123456789')
#
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM SYS_DRUG')
# result = cursor.fetchall()
# for row in result:
#     print(row)
#
# cursor.close()
# conn.close()

import dmPython
try :
    # 输入相关配置信息
    conn = dmPython.connect(user='PHUSERS', password='Zy_123456789', server='192.168.0.234', port=5236)
    # 连接数据库
    curses = conn.cursor()
    #连接成功提示
    print("连接成功")
except:
    #失败提示
    print("失败")

