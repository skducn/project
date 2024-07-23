# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2024-7-23
# Description: redis
#****************************************************************

import redis

pool0 = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.Redis(connection_pool=pool0)

# todo 字符串
# 获取字符串的值
print(r.get("idcard")) # b'310089'


# todo 集合
# 获取set中row的数量
print(r.scard("s_family")) # 2

# 判断set中是否存在age
print(r.sismember("s_family",'age'))  # True

# todo 哈希
print(r.hget("h_1", 'name'))  # b'jinhao'


# 将db0中h_1移动到db3
# r.move('h_1', 3)

# print(r.get('h_1'))

# r.select(4)
# r.set("idcard", '1000')


r.rename('idd','xxx') # 呃.改名
r.expire('xxx',111110) # 让数据111110秒后过期
r.ttl('xxx') # 看剩余过期时间 不存在返回-1
