# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Data       : 2024-1-18
# Description: Mongo 对象层
# pip3.9 install pymongo -U
# jar包  https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/
# 参考：http://www.51testing.com/html/85/n-7794185.html
# 使用方法 参考：https://www.moonapi.com/news/2512.html
# 增删改查 https://www.runoob.com/python3/python-mongodb.html
# 怎么操作MongoDB http://www.codebaoku.com/it-python/it-python-235296.html

# 符号	含义	示例
# $lt	小于	{'age': {'$lt': 20}}
# $gt	大于	{'age': {'$gt': 20}}
# $lte	小于等于	{'age': {'$lte': 20}}
# $gte	大于等于	{'age': {'$gte': 20}}
# $ne	不等于	{'age': {'$ne': 20}}
# $in	在范围内	{'age': {'$in': [20, 23]}}
# $nin	不在范围内	{'age': {'$nin': [20, 23]}}

# 符号	含义	示例	示例含义
# $regex	匹配正则表达式	{'name': {'$regex': '^M.*'}}	name以M开头
# $exists	属性是否存在	{'name': {'$exists': True}}	name属性存在
# $type	类型判断	{'age': {'$type': 'int'}}	age的类型为int
# $mod	数字模操作	{'age': {'$mod': [5, 0]}}	年龄模5余0
# $text	文本查询	{'$text': {'$search': 'Mike'}}	text类型的属性中包含Mike字符串
# $where	高级条件查询	{'$where': 'obj.fans_count == obj.follows_count'}	自身粉丝数等于关注数

# 错误：AttributeError: module 'httpcore' has no attribute 'NetworkBackend'
# pip install dnspython==2.3.0
# 参考：https://www.saoniuhuo.com/question/detail-2755168.html

# show dbs  # 查看所有数据库列表
#     # admin   40.00 KiB
#     # config  60.00 KiB
#     # local   40.00 KiB
#     # test     8.00 KiB
# db.getName()
# use test  # 切换test数据库，没有则新建
# db  # test  查看当前数据库
# db.version()  # 7.0.5
# db.stats()
# db.getMongo()  # mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.1

# show collections  # dog  //查看当前数据库下所有集合
# db.createCollection('dog')  # { ok: 1 }
# db.dog.insertOne({dogNum: 'A-1001', dogName: '麦兜', dogAge: 3, dogKind: '边牧'})
# db.dog.find()  # 查看dog集合中信息


# ***************************************************************

from pymongo import MongoClient

class MongoPO:

    def __init__(self, varHostPort):

        self.client = MongoClient('mongodb://' + varHostPort)
        # self.client = MongoClient('mongodb://username:password@192.168.146.192:27017/')

    def getCollection(self, varDb):

        # 获取当前数据库的所有集合名
        # 获取所有数据库名
        self.l_db = self.client.list_database_names()
        # print(self.l_db)  # ['admin', 'config', 'local', 'test']
        try :
            if varDb not in self.l_db:
                raise (NameError, "没有数据库信息")
            else:
                db = self.client[varDb]  # 获取数据库
                return db.list_collection_names()
        except:
            return []

    def getRecord(self, varDb, varCollection):

        # 获取数据库
        db = self.client[varDb]
        col = db[varCollection]
        return col

    def close(self):

        # 关闭连接
        self.client.close()


if __name__ == "__main__":

    Mongo_PO = MongoPO("127.0.0.1:27017")


    # 获取test库中的集合
    l_collection = Mongo_PO.getCollection("test")
    # print(l_collection)  # ['cat', 'dog']


    col = Mongo_PO.getRecord("test", "dog")

    # todo 查询第一条记录 find_one
    # d_one = col.find_one()
    # # print(d_one)  # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
    # print(d_one['_id'])  # 65a89cc692c79cad7b3cafb2

    # # todo 查询集合中所有数据 find
    # o_b = col.find()
    # for d_one in o_b:
    #     print(d_one, d_one['dogName'])
    # #     # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
    # #     # {'_id': ObjectId('65a89ce392c79cad7b3cafb3'), 'dogNum': 'A-1002', 'dogName': '泡泡', 'dogAge': 5, 'dogKind': '柯基'}
    # #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb4'), 'dogNum': 'A-1003', 'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}
    # #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪', 'dogAge': 8, 'dogKind': '秋田'}
    #
    # # todo 查询指定字段的数据
    # 不要输出的字段为0，否则为1
    # 注意：除了 _id，不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然。如：0，0，1 或 1，0，1 都是错误的。
    # o_c = col.find({}, {'_id':0, 'dogNum':0})
    # for d in o_c:
    #     print(d)
    #     # {'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
    #     # {'dogName': '泡泡', 'dogAge': 5, 'dogKind': '柯基'}
    #     # {'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}
    #     # {'dogName': '闪闪', 'dogAge': 8, 'dogKind': '秋田'}

    # todo 根据指定条件查询
    # o_c = col.find({'dogAge':3})
    # for d in o_c:
    #     print(d)  # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}

    # todo 高级查询
    # # dogAge值大于3的数据
    # o_c = col.find({'dogAge': {"$gt":3} })
    # for d in o_c:
    #     print(d)
    #     # {'_id': ObjectId('65a89ce392c79cad7b3cafb3'), 'dogNum': 'A-1002', 'dogName': '泡泡', 'dogAge': 5, 'dogKind': '柯基'}
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪', 'dogAge': 8, 'dogKind': '秋田'}
    #     # {'_id': ObjectId('65a8aae3fd2a653d0ac0d1fc'), 'dogNum': 'A-1005', 'dogName': '皮皮', 'dogAge': 14, 'dogKind': '萨摩耶犬'}
    #     # {'_id': ObjectId('65a8b347399fcb727ee8f554'), 'dogNum': 'A-1006', 'dogName': '大白', 'dogAge': 5, 'dogKind': '啸天犬'}
    #     # {'_id': ObjectId('65a8b347399fcb727ee8f555'), 'dogNum': 'A-1007', 'dogName': '小白', 'dogAge': 6, 'dogKind': '藏獒'}

    # todo 使用正则表达式查询
    # # dogName中第一个是"大"的
    # o_c = col.find({'dogName': {"$regex": "^大"}})
    # for d in o_c:
    #     print(d)
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb4'), 'dogNum': 'A-1003', 'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}
    #     # {'_id': ObjectId('65a8b347399fcb727ee8f554'), 'dogNum': 'A-1006', 'dogName': '大白', 'dogAge': 5, 'dogKind': '啸天犬'}




    # todo 插入一个文档（记录）insert_one
    # 如果我们在插入文档时没有指定 _id，MongoDB 会为每个文档添加一个唯一的 id。
    # InsertOneResult = col.insert_one({'dogNum': 'A-1005', 'dogName': '皮皮', 'dogAge': 14, 'dogKind': '萨摩耶犬'})
    # print(InsertOneResult) <pymongo.results.InsertOneResult object at 0x10a34b288>
    # 返回 _id 字段
    # print("_id:", InsertOneResult.inserted_id)  # 65a8aae3fd2a653d0ac0d1fc

    # todo 插入多个文档（记录）insert_many
    # InsertOneResult = col.insert_many([{'dogNum': 'A-1006', 'dogName': '大白', 'dogAge': 5, 'dogKind': '啸天犬'},
    #                                    {'dogNum': 'A-1007', 'dogName': '小白', 'dogAge': 6, 'dogKind': '藏獒'}])
    # print(InsertOneResult)  # InsertManyResult([ObjectId('65a8b347399fcb727ee8f554'), ObjectId('65a8b347399fcb727ee8f555')], acknowledged=True)
    # print(InsertOneResult.inserted_ids)  # [ObjectId('65a8b347399fcb727ee8f554'), ObjectId('65a8b347399fcb727ee8f555')]

    # o_b = col.find()
    # for d_one in o_b:
    #     print(d_one)
        # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
        # {'_id': ObjectId('65a89ce392c79cad7b3cafb3'), 'dogNum': 'A-1002', 'dogName': '泡泡', 'dogAge': 5, 'dogKind': '柯基'}
        # {'_id': ObjectId('65a89d3992c79cad7b3cafb4'), 'dogNum': 'A-1003', 'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}
        # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪', 'dogAge': 8, 'dogKind': '秋田'}
        # {'_id': ObjectId('65a8aae3fd2a653d0ac0d1fc'), 'dogNum': 'A-1005', 'dogName': '皮皮', 'dogAge': 14, 'dogKind': '萨摩耶犬'}
        # {'_id': ObjectId('65a8b347399fcb727ee8f554'), 'dogNum': 'A-1006', 'dogName': '大白', 'dogAge': 5, 'dogKind': '啸天犬'}
        # {'_id': ObjectId('65a8b347399fcb727ee8f555'), 'dogNum': 'A-1007', 'dogName': '小白', 'dogAge': 6, 'dogKind': '藏獒'}


    # todo 更新一个文档 update_one
    # # 将 dogName字段 "闪闪" 改为 "闪闪123"
    # # 注意：如匹配到多条记录，则只更新第一条数据
    # col.update_one({"dogName": "闪闪"}, {"$set": {"dogName": "闪闪123"}})
    # o_c = col.find({'dogNum': "A-1004"})
    # for d in o_c:
    #     print(d)  # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪123', 'dogAge': 8, 'dogKind': '秋田'}

    # todo 更新多个文档 update_many
    # x = col.update_many({"dogAge": 5}, {"$set": {"dogAge": 54}})
    # print(x.modified_count)  # 2   //修改了2个文档
    # o_c = col.find()
    # for d in o_c:
    #     print(d)
    #     # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
    #     # {'_id': ObjectId('65a89ce392c79cad7b3cafb3'), 'dogNum': 'A-1002', 'dogName': '泡泡', 'dogAge': 54, 'dogKind': '柯基'}
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb4'), 'dogNum': 'A-1003', 'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪123', 'dogAge': 8, 'dogKind': '秋田'}
    #     # {'_id': ObjectId('65a8aae3fd2a653d0ac0d1fc'), 'dogNum': 'A-1005', 'dogName': '皮皮', 'dogAge': 14, 'dogKind': '萨摩耶犬'}
    #     # {'_id': ObjectId('65a8b347399fcb727ee8f554'), 'dogNum': 'A-1006', 'dogName': '大白', 'dogAge': 54, 'dogKind': '啸天犬'}
    #     # {'_id': ObjectId('65a8b347399fcb727ee8f555'), 'dogNum': 'A-1007', 'dogName': '小白', 'dogAge': 6, 'dogKind': '藏獒'}


    # todo 删除一个文档 delete_one
    # col.delete_one({"dogName": "小白"})

    # todo 删除多个文档 delete_many
    # # 删除dogName中最后一个中文是"白"的数据 ， 即删除了 大白，小白
    # e = col.delete_many({"dogName": {"$regex": "白$"}})
    # print(e.deleted_count)  # 2
    # o_c = col.find()
    # for d in o_c:
    #     print(d)

    # todo 删除所有文档 delete_many
    # e = col.delete_many({}})
    # print(e.deleted_count)

    # todo 删除集合 drop
    # 如果删除成功 drop() 返回 true，如果删除失败(集合不存在)则返回 false。
    # col.drop()




    # todo 排序 sort
    # # 1 为升序，-1 为降序，默认为升序
    # o_c = col.find().sort("dogAge")
    # for d in o_c:
    #     print(d)
    #
    # o_c = col.find().sort("dogAge", -1)
    # for d in o_c:
    #     print(d)
    #     # {'_id': ObjectId('65a89ce392c79cad7b3cafb3'), 'dogNum': 'A-1002', 'dogName': '泡泡', 'dogAge': 54, 'dogKind': '柯基'}
    #     # {'_id': ObjectId('65a8aae3fd2a653d0ac0d1fc'), 'dogNum': 'A-1005', 'dogName': '皮皮', 'dogAge': 14, 'dogKind': '萨摩耶犬'}
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪123', 'dogAge': 8, 'dogKind': '秋田'}
    #     # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb4'), 'dogNum': 'A-1003', 'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}
    #
    # print("/n")

    # todo 偏移 skip
    # # 比如偏移2，就忽略前两个元素，得到第三个及以后的元素：
    # o_c = col.find().sort("dogAge", -1).skip(2)
    # for d in o_c:
    #     print(d)
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb5'), 'dogNum': 'A-1004', 'dogName': '闪闪123', 'dogAge': 8, 'dogKind': '秋田'}
    #     # {'_id': ObjectId('65a89cc692c79cad7b3cafb2'), 'dogNum': 'A-1001', 'dogName': '麦兜', 'dogAge': 3, 'dogKind': '边牧'}
    #     # {'_id': ObjectId('65a89d3992c79cad7b3cafb4'), 'dogNum': 'A-1003', 'dogName': '大牙', 'dogAge': 2, 'dogKind': '边牧'}

    # 注意：在数据库数量非常庞大的时候，如千万、亿级别，最好不要使用大的偏移量来查询数据，因为这样很可能导致内存溢出。此时可以使用类似如下操作来查询：
    # from bson.objectid import ObjectId
    # col.find({'_id': {'$gt': ObjectId('593278c815c2602678bb2b8d')}})


    # todo 限定 limit
    # 返回指定条数记录
    # # 对输出结果限制数量，只显示1条（有3条结果，但实际第一条）
    # o_c = col.find({'dogAge': {"$gt": 3}}).limit(1)
    # for d in o_c:
    #     print(d)  # {'_id': ObjectId('65a89ce392c79cad7b3cafb3'), 'dogNum': 'A-1002', 'dogName': '泡泡', 'dogAge': 5, 'dogKind': '柯基'}


    Mongo_PO.close()




