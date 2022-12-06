# -*- coding: utf-8 -*-
#***************************************************************
# Author     : John
# Data       : 2022-12-06
# Description: Mongo 对象层
# pip3.9 install pymongo
# 参考：http://www.51testing.com/html/85/n-7794185.html
#***************************************************************

import pymongo


class MongoPO():

    def __init__(self, varHost, varDB, varPort):


        self.varHost = varHost
        self.varDB = varDB
        self.varPort = varPort

    def __GetConnect(self):

        '''连接数据库'''

        if not self.varDB:
            raise (NameError, "没有设置数据库信息")
        self.client = pymongo.MongoClient(host=self.varHost, port=int(self.varPort))

        # 获取数据库
        self.db = self.client[self.varDB]

        # 获取集合collection
        myset = self.db['集合名字']

        # 插入数据
        # myset.insert(dict)





if __name__ == '__main__':


    Mongo_PO = MongoPO("host", 27017)
    # t_userNo = Mongo_PO.execQuery('select id from sys_user_detail where userNo="%s"' % ("16766667777"))
