#-*-coding:utf-8 -*-
#****************************************************************
# Author     : John
# Date       : 2023-12-29
# Description: 上下文管理器 __enter__ , __exit__
# https://pythonjishu.com/zifazjnjqupeurz/
# 使用__enter__和__exit__魔法方法来实现一个简单的上下文管理器，用于管理数据库连接。
# 在__enter__方法中，连接数据库并返回当前对象；在__exit__方法中，断开连接。同时在query方法中可以执行一些其他操作，如查询数据库。
# 在使用 with 语句时，可以自动管理上下文，使得上下文管理器的相关操作更加简单方便。
#****************************************************************


class Database:
    def __init__(self, db_name):
        self._db_name = db_name

    def __enter__(self):
        print(f"connect to {self._db_name}")
        # 返回当前对象
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"disconnect from {self._db_name}")

    def query(self, sql):
        print(f"query: {sql}")


with Database("test") as db:
    db.query("select * from table")

# connect to test
# query: select * from table
# disconnect from test