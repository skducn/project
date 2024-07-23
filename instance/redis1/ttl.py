# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2024-7-23
# Description: redis TTL  获取redis中的key的过期时间
# 重新设置过期时间600s expire key 600

# todo 获取hello的过期时间，
# 当 key 不存在时，返回 -2
# 当 key 存在但没有设置剩余生存时间时，返回 -1


# 方法1：命令行
# localhost-2:~ linghuchong$ redis-cli TTL hello
# (integer) 9636

# 方法2：命令行
# localhost-2:~ linghuchong$ redis-cli -h localhost -p 6379
# localhost:6379> ttl hello
# (integer) 9555

# 方法3：python脚本
# pool0 = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
# r = redis.Redis(connection_pool=pool0)
# # 获取TTL的值
# ttl = r.ttl("hello")
# print(ttl)
#****************************************************************

import redis

# 每个redis实例都有独立的连接池
# r = redis.Redis(host='192.168.31.177', port=6379, db=0, password="123456")
# r.set('foo','Bar')
# print(r.get("foo"))

# redis实例共享连接池
# redis-py使用connection_pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。
# 可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
pool0 = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = redis.Redis(connection_pool=pool0)

# 获取剩余时间
ttl = r.ttl("hello")
print(ttl)

# 重新设置过期时间600s
r.expire("hello", 600)
ttl = r.ttl("hello")
print(ttl)



pool3 = redis.ConnectionPool(host='127.0.0.1', port=6379, db=3)
r = redis.Redis(connection_pool=pool3)
# r.set('home1','44')
# print(r.get('home1'))  # b'44'

print(r.dbsize())  # 2 , db3中有2个keys
r.flushdb()  # 清空数据库db3中所有的key
print(r.dbsize())  # 0


