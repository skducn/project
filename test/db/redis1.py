# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2016-6-13
# Description: redis缓存数据库  下载：http://download.redis.io/releases/
#****************************************************************
# 一般来说，mongodb 或者 mysql来做持久层，redis做缓存
# redis-py 提供两个类 Redis 和 StrictRedis 用于实现Redis的命令，StrictRedis用于实现大部分官方的命令，
# 并使用官方的语法和命令，Redis是StrictRedis的子类，用于向后兼容旧版本的redis-py。
# redis配置文件redis.conf的详细说明 http://blog.csdn.net/vv_demon/article/details/7676384
# 【python】redis基本命令和基本用法详解 http://www.cnblogs.com/wangtp/p/5636872.html
# redis单机安装以及简单redis集群搭建  https://www.cnblogs.com/mirakel/p/7251053.html

import redis, base64, hashlib
from time import sleep

# 每个redis实例都有独立的连接池
# r = redis.Redis(host='192.168.31.177', port=6379, db=0, password="123456")
# r.set('foo','Bar')
# print(r.get("foo"))

# redis实例共享连接池
# redis-py使用connection_pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。
# 可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
pool = redis.ConnectionPool(host='192.168.31.177', port=6379, db=0, password="123456")
r = redis.Redis(connection_pool=pool)
# r.set('foo','Bar')
# print(r.get("foo"))

# set(name, value, ex=None, px=None, nx=False, xx=False)
# ex，过期时间（秒）
# px，过期时间（毫秒）
# nx，如果设置为True，则只有name不存在时，当前set操作才执行（新增）
# xx，如果设置为True，则只有name存在时，当前set操作才执行（修改）
r.set('foo','123', ex=3)
print(r.get("foo"))  # b'123'
sleep(8)
print(r.get("foo"))  # None
print(r.set('foo', 'Bar', nx=True))  # None，已经存在
print(r.set('foo', 'Bar123', xx=True))   # 编辑


# # 获取redis信息
# info = connRedis.info()
# for key in info:
#     print "%s : %s" % (key, info[key])
#
# # 获取数据库大小
# print '\ndbsize: %s' % connRedis.dbsize()
#
# # 查看连接
# print "ping %s" % connRedis.ping()
#
# sleep(1212)
#
# # 返回key的set的基数 ,结果80个
# print connRedis167.scard("randomRed:34:3855")
#
# # 判断key中member元素是否存在,返回 true 或 false
# print connRedis167.sismember("randomRed:34:3855","68:1")
# sum=0
# for i in connRedis167.smembers("randomRed:34:3855"):
#     sum = sum +int(i.split(":",1)[1])
# print sum

# *******************************************************************************************************************************
# 【python】redis基本命令和基本用法详解
# 1、redis连接
# redis-py提供两个类Redis和StrictRedis用于实现Redis的命令，StrictRedis用于实现大部分官方的命令，
# 并使用官方的语法和命令，Redis是StrictRedis的子类，用于向后兼容旧版本的redis-py。
# import redis 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
# r = redis.Redis(host='192.168.19.130', port=6379) host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
# r.set('foo', 'Bar') key是"foo" value是"bar" 将键值对存入redis缓存
# print r.get('foo') Bar 取出键foo对应的值

# *******************************************************************************************************************************
# 2、连接池
# redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。
# 默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
# import redis 通过python操作redis缓存
# pool = redis.ConnectionPool(host='192.168.19.130', port=6379) host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
# r = redis.Redis(connection_pool=pool)
# r.set('foo', 'Bar') key是"foo" value是"bar" 将键值对存入redis缓存
# print r.get('foo') Bar 取出键foo对应的值


# *******************************************************************************************************************************
# 3、redis基本命令_string
#
# set(name, value, ex=None, px=None, nx=False, xx=False)
# 在Redis中设置值，默认，不存在则创建，存在则修改
# 参数：
# ex，过期时间（秒）
# px，过期时间（毫秒）
# nx，如果设置为True，则只有name不存在时，当前set操作才执行
# xx，如果设置为True，则只有name存在时，当前set操作才执行
#
# 8 mset(*args, **kwargs)
# 批量设置值
# 如：
# mset(k1='v1', k2='v2')
# 或
# mget({'k1': 'v1', 'k2': 'v2'})
# r.mset(k1="v1",k2="v2") 这里k1 和k2 不能带引号 一次设置对个键值对
# print r.mget("k1","k2")    # ['v1', 'v2'] 一次取出多个键对应的值
# print r.mget("k1")   # ['v1']  # 批量获取

# 10 getset(name, value)
# 设置新值并获取原来的值
# print(r.getset("foo1","bar_NEW"))    # Bar ， 设置的新值是"bar_NEW" 设置前的值是Bar

# 11 getrange(key, start, end)
# 获取子序列（根据字节获取，非字符）
# 参数：
# name，Redis 的 name
# start，起始位置（字节）
# end，结束位置（字节）
# 如： "武沛齐" ，0-3表示 "武"
# r.set("foo1","武沛齐") 汉字
# print(r.getrange("foo1",0,2)) 取索引号是0-2 前3位的字节 武 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
# print(r.getrange("foo1",0,-1)) 取所有的字节 武沛齐 切片操作
# r.set("foo1","bar_new") 字母
# print(r.getrange("foo1",0,2)) 取索引号是0-2 前3位的字节 bar 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
# print(r.getrange("foo1",0,-1)) 取所有的字节 bar_new 切片操作

# 12 setrange(name, offset, value)
# 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
# 参数：
# offset，字符串的索引，字节（一个汉字三个字节）
# value，要设置的值
# r.setrange("foo1",1,"aaa")
# print(r.get("foo1")) baaanew 原始值是bar_new 从索引号是1开始替换成aaa 变成 baaanew
# bar_new
#
#
# 13 setbit(name, offset, value)
# 对name对应值的二进制表示的位进行操作
# 参数：
# name，redis的name
# offset，位的索引（将值变换成二进制后再进行索引）
# value，值只能是 1 或 0
#
# 注：如果在Redis中有一个对应： n1 = "foo"，
# 那么字符串foo的二进制表示为：01100110 01101111 01101111
# 所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，
# 那么最终二进制则变成 01100111 01101111 01101111，即："goo"
#
# 扩展，转换二进制表示：
# source = "陈思维"
# source = "foo"
# for i in source:
# num = ord(i)
# print bin(num).replace('b','')
# 特别的，如果source是汉字 "陈思维"怎么办？
# 答：对于utf-8，每一个汉字占 3 个字节，那么 "陈思维" 则有 9个字节
# 对于汉字，for循环时候会按照 字节 迭代，那么在迭代时，将每一个字节转换 十进制数，然后再将十进制数转换成二进制
# 11100110 10101101 10100110 11100110 10110010 10011011 11101001 10111101 10010000
# -------------------------- ----------------------------- -----------------------------
# 陈思维

# 13 应用场景 ：统计uv
# 注：如果在Redis中有一个对应： n1 = "foo"，
# 那么字符串foo的二进制表示为：01100110 01101111 01101111
# 所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，
# 那么最终二进制则变成 01100111 01101111 01101111，即："goo"
# r.set("foo","foo1") foo1的二进制表示为：01100110 01101111 01101111 00110001
# 这里f对应的ascii值是102 折算二进制是 01100110 （64+32+4+2）
# 这里o对应的ascii值是111 折算二进制是 01101111 （64+32+8+4+2+1）
# 这里数字1对应的ascii值是49 折算二进制是 00110001 （32+16+1）
# r.setbit("foo",7,1) 将第7位设置为1，
# print(r.get("foo")) goo1
# 那么最终二进制则变成 01100111 01101111 01101111 00000001
# print(ord("f")) 102 将字符f的ascii对应的值打印出来
# print(ord("o")) 111 将字符o的ascii对应的值打印出来
# print(chr(103)) g 将ascii数字103对应的字符打印出来
# print(ord("1")) 49 将数字1的ascii对应的值打印出来


# 14 getbit(name, offset)
# 获取name对应的值的二进制表示中的某位的值 （0或1）
# print(r.getbit("foo1",0)) 0 foo1对应的二进制 4个字节 32位 第0位是0还是1
#
# 15 bitcount(key, start=None, end=None)
# 获取name对应的值的二进制表示中 1 的个数
# 参数：
# key，Redis的name
# start 字节起始位置
# end，字节结束位置
# print(r.get("foo")) goo1 01100111
# print(r.bitcount("foo",0,1)) 11 表示前2个字节中，1出现的个数
#
# 16 bitop(operation, dest, *keys)
# 获取多个值，并将值做位运算，将最后的结果保存至新的name对应的值
#
# 参数：
# operation,AND（并） 、 OR（或） 、 NOT（非） 、 XOR（异或）
# dest, 新的Redis的name
# *keys,要查找的Redis的name
#
# 如：
# bitop("AND", 'new_name', 'n1', 'n2', 'n3')
# 获取Redis中n1,n2,n3对应的值，然后讲所有的值做位运算（求并集），然后将结果保存 new_name 对应的值中
# r.set("foo","1") 0110001
# r.set("foo1","2") 0110010
# print(r.mget("foo","foo1")) ['goo1', 'baaanew']
# print(r.bitop("AND","new","foo","foo1")) "new" 0 0110000
# print(r.mget("foo","foo1","new"))
#
# source = "12"
# for i in source:
# num = ord(i)
# print(num) 打印每个字母字符或者汉字字符对应的ascii码值 f-102-0b100111-01100111
# print(bin(num)) 打印每个10进制ascii码值转换成二进制的值 0b1100110（0b表示二进制）
# print bin(num).replace('b','') 将二进制0b1100110替换成01100110


# 17 strlen(name)
# 返回name对应值的字节长度（一个汉字3个字节）
# print(r.strlen("foo")) 4 'goo1'的长度是4
#
# 18 incr(self, name, amount=1)
# 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
# 参数：
# name,Redis的name
# amount,自增数（必须是整数）
# 注：同incrby
# r.set("foo",123)
# print r.mget("foo","foo1","foo2","k1","k2") ['123', '2', 'bar', 'v1', 'v2']
# r.incr("foo",amount=1)
# print r.mget("foo","foo1","foo2","k1","k2") ['124', '2', 'bar', 'v1', 'v2']


# 18 incr(self, name, amount=1)
# 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
# 参数：
# name,Redis的name
# amount,自增数（必须是整数）
# 注：同incrby
# r.set("foo",123)
# print r.mget("foo","foo1","foo2","k1","k2") ['123', '2', 'bar', 'v1', 'v2']
# r.incr("foo",amount=1)
# print r.mget("foo","foo1","foo2","k1","k2") ['124', '2', 'bar', 'v1', 'v2']
#
# 19 incrbyfloat(self, name, amount=1.0)
# 自增 name对应的值，当name不存在时，则创建name＝amount，否则，则自增。
# 参数：
# name,Redis的name
# amount,自增数（浮点型）
# r.set("foo1","123.0")
# print r.mget("foo","foo1","foo2","k1","k2") ['124', '123.0', 'bar', 'v1', 'v2']
# r.incrbyfloat("foo1",amount=2.0)
# r.incrbyfloat("foo3",amount=3.0)
# print r.mget("foo","foo1","foo2","foo3","k1","k2") ['124', '125', 'bar', '-3', 'v1', 'v2']


# 20 decr(self, name, amount=1)
# 自减 name对应的值，当name不存在时，则创建name＝amount，否则，则自减。
# 参数：
# name,Redis的name
# amount,自减数（整数)
# r.decr("foo4",amount=3) 递减3
# r.decr("foo1",amount=1) 递减1
# print r.mget("foo","foo1","foo2","foo3","foo4","k1","k2")
# ['goo1', '121', 'bar', '15', '-18', 'v1', 'v2']

#
# 21 append(key, value)
# 在redis name对应的值后面追加内容
# 参数：
# key, redis的name
# value, 要追加的字符串
# r.append("foo","abc") 在foo对应的值goo1后面追加字符串abc
# print r.mget("foo","foo1","foo2","foo3","foo4","k1","k2")
# ['goo1abc', '121', 'bar', '15', '-18', 'v1', 'v2']
#

# *******************************************************************************************************************************
# 4 redis基本命令_hash

# 1 单个增加--修改(单个取出)--没有就新增，有的话就修改
# hset(name, key, value)
# name对应的hash中设置一个键值对（不存在，则创建；否则，修改）
# 参数：
# name，redis的name
# key，name对应的hash中的key
# value，name对应的hash中的value
# 注：
# hsetnx(name, key, value),当name对应的hash中不存在当前key时则创建（相当于添加）
# r.hset("foo_hash1","k1","v1")
# print(r.mget("foo","foo1","foo2","foo3","foo4","k1","k2"))
# ['goo1abcabc', '121', 'bar', '15', '-18', 'v1', 'v2'] 取字符串
# print(r.hget("foo_hash1","k1")) v1 单个取hash的key
# print(r.hmget("foo_hash1","k1")) ['v1'] 批量取hash的key
#
# r.hsetnx("foo_hash1","k2","v2") 只能新建
# print(r.hget("foo_hash1","k2")) v2
# print(r.hmget("foo_hash1","k2")) ['v2']
#
#
# 2 批量增加（取出）
# hmset(name, mapping)
# 在name对应的hash中批量设置键值对
# 参数：
# name，redis的name
# mapping，字典，如：{'k1':'v1', 'k2': 'v2'}
# 如：
# r.hmset('xx', {'k1':'v1', 'k2': 'v2'})
# r.hmset("foo_hash2",{"k2":"v2","k3":"v3"})
# print(r.hget("foo_hash2","k2")) v2
# 单个取出"foo_hash2"的key-k2对应的value
# print(r.hmget("foo_hash2","k2","k3")) ['v2', 'v3']
# 批量取出"foo_hash2"的key-k2 k3对应的value --方式1
# print(r.hmget("foo_hash2",["k2","k3"])) ['v2', 'v3']
# 批量取出"foo_hash2"的key-k2 k3对应的value --方式2
#
# hget(name,key)
# 在name对应的hash中获取根据key获取value
# hmget(name, keys, *args)
# 在name对应的hash中获取多个key的值
# 参数：
# name，reids对应的name
# keys，要获取key集合，如：['k1', 'k2', 'k3']
# *args，要获取的key，如：k1,k2,k3
# 如：
# r.hmget('xx', ['k1', 'k2'])
# 或
# print r.hmget('xx', 'k1', 'k2')
#
# 3 取出所有的键值对
# hgetall(name)
# 获取name对应hash的所有键值
# print(r.hgetall("foo_hash1"))
# {'k2': 'v2', 'k1': 'v1'}
#
# 4 得到所有键值对的格式 hash长度
# hlen(name)
# 获取name对应的hash中键值对的个数
# print(r.hlen("foo_hash1")) 2
#
# 5 得到所有的keys（类似字典的取所有keys）
# hkeys(name)
# 获取name对应的hash中所有的key的值
# print(r.hkeys("foo_hash1")) ['k1', 'k2'] 取出所有的keys
#
# 6 得到所有的value（类似字典的取所有value）
# hvals(name)
# 获取name对应的hash中所有的value的值
# print(r.hvals("foo_hash1")) ['v1', 'v2'] 取出所有的values
#
# 7 判断成员是否存在（类似字典的in）
# hexists(name, key)
# 检查name对应的hash是否存在当前传入的key
# print(r.hexists("foo_hash1","k3")) False 不存在
# print(r.hexists("foo_hash1","k1")) True 存在
#
# 8 删除键值对
# hdel(name,*keys)
# 将name对应的hash中指定key的键值对删除
# print(r.hgetall("foo_hash1")) {'k2': 'v2', 'k1': 'v1'}
# r.hset("foo_hash1","k2","v3") 修改已有的key k2
# r.hset("foo_hash1","k1","v1") 新增键值对 k1
# r.hdel("foo_hash1","k1") 删除一个键值对
# print(r.hgetall("foo_hash1")) {'k2': 'v3'}
#
# 9 自增自减整数(将key对应的value--整数 自增1或者2，或者别的整数 负数就是自减)
# hincrby(name, key, amount=1)
# 自增name对应的hash中的指定key的值，不存在则创建key=amount
# 参数：
# name，redis中的name
# key， hash对应的key
# amount，自增数（整数）
# r.hset("foo_hash1","k3",123)
# r.hincrby("foo_hash1","k3",amount=-1)
# print(r.hgetall("foo_hash1")) {'k3': '122', 'k2': 'v3', 'k1': 'v1'}
# r.hincrby("foo_hash1","k4",amount=1) 不存在的话，value默认就是1
# print(r.hgetall("foo_hash1")) {'k3': '122', 'k2': 'v3', 'k1': 'v1', 'k4': '4'}
#
# 10 自增自减浮点数(将key对应的value--浮点数 自增1.0或者2.0，或者别的浮点数 负数就是自减)
# hincrbyfloat(name, key, amount=1.0)
# 自增name对应的hash中的指定key的值，不存在则创建key=amount
# 参数：
# name，redis中的name
# key， hash对应的key
# amount，自增数（浮点数）
# 自增name对应的hash中的指定key的值，不存在则创建key=amount
# r.hset("foo_hash1","k5","1.0")
# r.hincrbyfloat("foo_hash1","k5",amount=-1.0) 已经存在，递减-1.0
# print(r.hgetall("foo_hash1"))
# r.hincrbyfloat("foo_hash1","k6",amount=-1.0) 不存在，value初始值是-1.0 每次递减1.0
# print(r.hgetall("foo_hash1")) {'k3': '122', 'k2': 'v3', 'k1': 'v1', 'k6': '-6', 'k5': '0', 'k4': '4'}
#
# 11 取值查看--分片读取
# hscan(name, cursor=0, match=None, count=None)
# 增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，从而放置内存被撑爆
# 参数：
# name，redis的name
# cursor，游标（基于游标分批取获取数据）
# match，匹配指定key，默认None 表示所有的key
# count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
# 如：
# 第一次：cursor1, data1 = r.hscan('xx', cursor=0, match=None, count=None)
# 第二次：cursor2, data1 = r.hscan('xx', cursor=cursor1, match=None, count=None)
# ...
# 直到返回值cursor的值为0时，表示数据已经通过分片获取完毕
# print(r.hscan("foo_hash1"))
# (0L, {'k3': '122', 'k2': 'v3', 'k1': 'v1', 'k6': '-6', 'k5': '0', 'k4': '4'})
#
# 12 hscan_iter(name, match=None, count=None)
# 利用yield封装hscan创建生成器，实现分批去redis中获取数据
# 参数：
# match，匹配指定key，默认None 表示所有的key
# count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
# 如：
# for item in r.hscan_iter('xx'):
# print item
# print(r.hscan_iter("foo_hash1")) <generator object hscan_iter at 0x027B2C88> 生成器内存地址
# for item in r.hscan_iter('foo_hash1'):
# print item
# ('k3', '122')
# ('k2', 'v3')
# ('k1', 'v1')
# ('k6', '-6')
# ('k5', '0')
# ('k4', '4')

# *******************************************************************************************************************************
# 5 redis基本命令_list
# import redis 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库
#
# pool = redis.ConnectionPool(host='192.168.19.130', port=6379)
#
# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
#
# r = redis.Redis(connection_pool=pool) 创建实例
#
# 1 增加（类似于list的append，只是这里是从左边新增加）--没有就新建
# lpush(name,values)
# 在name对应的list中添加元素，每个新的元素都添加到列表的最左边
# 如：
# r.lpush('oo', 11,22,33)
# 保存顺序为: 33,22,11
# 扩展：
# rpush(name, values) 表示从右向左操作
# r.lpush("foo_list1",11,22) 从列表的左边，先添加11，后添加22
# print(r.lrange("foo_list1",0,20))
# ['22', '11', '22', '11', '22', '11', '22', '11', '22', '11', '22', '11', '22', '11', '22', '11', '22', '11']
# 切片取出值，范围是索引号0-20
# print(r.llen("foo_list1")) 18 长度是18
#
# 2 增加（从右边增加）--没有就新建
# r.rpush("foo_list1",2,3,4) 在列表的右边，依次添加2,3,4
# print(r.lrange("foo_list1",0,-1))
# ['22', '11', '22', '11', '22', '11', '22', '11', '22', '11', '22',
# '11', '22', '11', '22', '11', '22', '11', '2', '3', '4']
# 切片取出值，范围是索引号0-最后一个元素
# print(r.llen("foo_list1")) 21 列表长度是21
#
# 3 往已经有的name的列表的左边添加元素，没有的话无法创建
# lpushx(name,value)
# 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
# 更多：
# rpushx(name, value) 表示从右向左操作
# r.lpushx("foo_list2",1) 这里"foo_list2"不存在
# print(r.lrange("foo_list2",0,-1)) []
# print(r.llen("foo_list2")) 0
#
# r.lpushx("foo_list1",1) 这里"foo_list1"之前已经存在，往列表最左边添加一个元素，一次只能添加一个
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['1', '22', '11', '22', '11', '22', '11', '22', '11', '22',
# '11', '22', '11', '22', '11', '22', '11', '22', '11', '2', '3', '4']
# print(r.llen("foo_list1")) 22 列表长度是22
#
# 4 往已经有的name的列表的右边添加元素，没有的话无法创建
# r.rpushx("foo_list1",1) 这里"foo_list1"之前已经存在，往列表最右边添加一个元素，一次只能添加一个
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['1', '22', '11', '22', '11', '22', '11', '22', '11', '22',
# '11', '22', '11', '22', '11', '22', '11', '22', '11', '2', '3', '4','1']
# print(r.llen("foo_list1")) 23 列表长度是23
#
# 5 新增（固定索引号位置插入元素）
# linsert(name, where, refvalue, value))
# 在name对应的列表的某一个值前或后插入一个新值
# 参数：
# name，redis的name
# where，BEFORE或AFTER
# refvalue，标杆值，即：在它前后插入数据
# value，要插入的数据
# r.linsert("foo_list1","before","22","33") 往列表中左边第一个出现的元素"22"前插入元素"33"
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['1', '33', '22', '11', '22', '11', '22', '11', '22',
# '11', '22', '11', '22', '11', '22', '11', '22', '11', '22', '11', '2', '3', '4', '1']
# print(r.llen("foo_list1")) 24 列表长度是24
#
# 6 修改（指定索引号进行修改）
# r.lset(name, index, value)
# 对name对应的list中的某一个索引位置重新赋值
# 参数：
# name，redis的name
# index，list的索引位置
# value，要设置的值
# r.lset("foo_list1",4,44) 把索引号是4的元素修改成44
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# print(r.llen("foo_list1")) 24 列表长度是24
#
# 7 删除（指定值进行删除）
# r.lrem(name, value, num)
# 在name对应的list中删除指定的值
# 参数：
# name，redis的name
# value，要删除的值
# num， num=0，删除列表中所有的指定值；
# num=2,从前到后，删除2个； num=1,从前到后，删除左边第1个
# num=-2,从后向前，删除2个
# r.lrem("foo_list1","2",1) 将列表中左边第一次出现的"2"删除
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['1', '33', '22', '11', '44', '11', '22', '11', '22', '11', '22', '11',
# '22', '11', '22', '11', '22', '11', '22', '11', '3', '4', '1']
# print(r.llen("foo_list1")) 23 列表长度是23
#
# r.lrem("foo_list1","11",0) 将列表中所有的"11"删除
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['1', '33', '22', '44', '22', '22', '22', '22', '22', '22', '22', '3', '4', '1']
# print(r.llen("foo_list1")) 14 列表长度是14
#
# 8 删除并返回
# lpop(name)
# 在name对应的列表的左侧获取第一个元素并在列表中移除，返回值则是第一个元素
# 更多：
# rpop(name) 表示从右向左操作
# print(r.lpop("foo_list1")) 删除最左边的22，并且返回删除的值22
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['44', '22', '22', '22', '22', '22', '22', '22', '3', '4', '1']
# print(r.llen("foo_list1")) 11 列表长度是11
#
# print(r.rpop("foo_list1")) 删除最右边的1，并且返回删除的值1
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素
# ['44', '22', '22', '22', '22', '22', '22', '22', '3', '4']
# print(r.llen("foo_list1")) 10 列表长度是10
#
# 9 删除索引之外的值
# ltrim(name, start, end)
# 在name对应的列表中移除没有在start-end索引之间的值
# 参数：
# name，redis的name
# start，索引的起始位置
# end，索引结束位置
# r.ltrim("foo_list1",0,8) 删除索引号是0-8之外的元素，值保留索引号是0-8的元素
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# ['44', '22', '22', '22', '22', '22', '22', '22', '3']
#
# 10 取值（根据索引号取值）
# lindex(name, index)
# 在name对应的列表中根据索引获取列表元素
# print(r.lindex("foo_list1",0)) 44 取出索引号是0的值
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# ['44', '22', '22', '22', '22', '22', '22', '22', '3', '4']
#
# 11 移动 元素从一个列表移动到另外一个列表
# rpoplpush(src, dst)
# 从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边
# 参数：
# src，要取数据的列表的name
# dst，要添加数据的列表的name
# r.rpoplpush("foo_list1","foo_list2")
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# ['44', '22', '22', '22', '22', '22', '22']
# print(r.lrange("foo_list2",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# ['22', '3']
#
# 12 移动 元素从一个列表移动到另外一个列表 可以设置超时
# brpoplpush(src, dst, timeout=0)
# 从一个列表的右侧移除一个元素并将其添加到另一个列表的左侧
# 参数：
# src，取出并要移除元素的列表对应的name
# dst，要插入元素的列表对应的name
# timeout，当src对应的列表中没有数据时，阻塞等待其有数据的超时时间（秒），0 表示永远阻塞
# r.brpoplpush("foo_list2","foo_list1",timeout=2)
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# ['22', '3', '44', '22', '22', '22', '22', '22', '22']
# print(r.lrange("foo_list2",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# []
#
# 13 一次移除多个列表
# blpop(keys, timeout)
# 将多个列表排列，按照从左到右去pop对应列表的元素
# 参数：
# keys，redis的name的集合
# timeout，超时时间，当元素所有列表的元素获取完之后，阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞
# 更多：
# r.brpop(keys, timeout)，从右向左获取数据
# r.blpop("foo_list1",timeout=2)
# print(r.lrange("foo_list1",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
# ['22', '3', '44', '22', '22', '22', '22', '22', '22']
# print(r.lrange("foo_list2",0,-1)) 切片取出值，范围是索引号0-最后一个元素（这里是包含最后一个元素的，是左闭右闭）
#
# 14 自定义增量迭代
# 由于redis类库中没有提供对列表元素的增量迭代，如果想要循环name对应的列表的所有元素，那么就需要：
# 1、获取name对应的所有列表
# 2、循环列表
# 但是，如果列表非常大，那么就有可能在第一步时就将程序的内容撑爆，所有有必要自定义一个增量迭代的功能：
# def list_iter(name):
# """
# 自定义redis列表增量迭代
# :param name: redis中的name，即：迭代name对应的列表
# :return: yield 返回 列表元素
# """
# list_count = r.llen(name)
# for index in xrange(list_count):
# yield r.lindex(name, index)
#
# 使用
# for item in list_iter('foo_list1'): ['3', '44', '22', '22', '22'] 遍历这个列表
# print item
#
# # *******************************************************************************************************************************
# # 6 redis基本命令_set
#
# Set操作，Set集合就是不允许重复的列表
#
# 1 新增
# sadd(name,values)
# name对应的集合中添加元素
# r.sadd("foo_set1",33,44,55,66) 往集合中添加一个元素 11
# print(r.smembers("foo_set1")) set(['11']) 获取集合中所有的成员
# print(r.scard("foo_set1")) 1 集合的长度是1
#
# r.sadd("foo_set2",66,77) 往集合中添加2个元素 22,33
# print(r.smembers("foo_set2")) set(['22',"33"]) 获取集合中所有的成员
# print(r.scard("foo_set2")) 2 集合的长度是2
#
# 2 获取元素个数 类似于len
# scard(name)
# 获取name对应的集合中元素个数
#
# 3 获取集合中所有的成员
# smembers(name)
# 获取name对应的集合的所有成员
#
# 3-1 获取集合中所有的成员--元组形式
# sscan(name, cursor=0, match=None, count=None)
# print(r.sscan("foo_set1")) (0L, ['11', '22', '33', '55'])
#
# 3-2 获取集合中所有的成员--迭代器的方式
# sscan_iter(name, match=None, count=None)
# 同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大
# for i in r.sscan_iter("foo_set1"):
# print(i)
#
# 4 差集
# sdiff(keys, *args)
# 在第一个name对应的集合中且不在其他name对应的集合的元素集合
# print(r.sdiff("foo_set1","foo_set2")) set(['11']) 在集合foo_set1但是不在集合foo_set2中
# print(r.smembers("foo_set1")) set(['22',"11"]) 获取集合中所有的成员
# print(r.smembers("foo_set2")) set(['22',"33"]) 获取集合中所有的成员
#
# 5 差集--差集存在一个新的集合中
# sdiffstore(dest, keys, *args)
# 获取第一个name对应的集合中且不在其他name对应的集合，再将其新加入到dest对应的集合中
# r.sdiffstore("foo_set3","foo_set1","foo_set2")
# print(r.smembers("foo_set1")) set(['22',"11"]) 获取集合1中所有的成员
# print(r.smembers("foo_set2")) set(['22',"33"]) 获取集合2中所有的成员
# print(r.smembers("foo_set3")) set(['11']) 获取集合3中所有的成员
#
# 6 交集
# sinter(keys, *args)
# 获取多一个name对应集合的交集
# print(r.sinter("foo_set1","foo_set2")) set(['22']) 取2个集合的交集
# print(r.smembers("foo_set1")) set(['22',"11"]) 获取集合1中所有的成员
# print(r.smembers("foo_set2")) set(['22',"33"]) 获取集合2中所有的成员
#
# 7 交集--交集存在一个新的集合中
# sinterstore(dest, keys, *args)
# 获取多一个name对应集合的并集，再将其加入到dest对应的集合中
# r.sinterstore("foo_set3","foo_set1","foo_set2")
# print(r.smembers("foo_set1")) set(['22',"11"]) 获取集合1中所有的成员
# print(r.smembers("foo_set2")) set(['22',"33"]) 获取集合2中所有的成员
# print(r.smembers("foo_set3")) set(['22']) 获取集合3中所有的成员
#
# 7-1 并集
# sunion(keys, *args)
# 获取多个name对应的集合的并集
# print(r.sunion("foo_set1","foo_set2")) set(['11', '22', '33', '77', '55', '66'])
# print(r.smembers("foo_set1")) set(['11', '33', '22', '55']) 获取集合1中所有的成员
# print(r.smembers("foo_set2")) set(['33', '77', '66', '22']) 获取集合2中所有的成员
#
# 7-2 并集--并集存在一个新的集合
# sunionstore(dest,keys, *args)
# 获取多一个name对应的集合的并集，并将结果保存到dest对应的集合中
# r.sunionstore("foo_bingji","foo_set1","foo_set2")
# print(r.smembers("foo_set1")) set(['11', '33', '22', '55']) 获取集合1中所有的成员
# print(r.smembers("foo_set2")) set(['33', '77', '66', '22']) 获取集合2中所有的成员
# print(r.smembers("foo_bingji")) set(['11', '22', '33', '77', '55', '66'])
#
# 8 判断是否是集合的成员 类似in
# sismember(name, value)
# 检查value是否是name对应的集合的成员
# print(r.sismember("foo_set1",11)) True 11是集合的成员
# print(r.sismember("foo_set1","11")) True
# print(r.sismember("foo_set1",23)) False 23不是集合的成员
#
# 9 移动
# smove(src, dst, value)
# 将某个成员从一个集合中移动到另外一个集合
# r.smove("foo_set1","foo_set4",11)
# print(r.smembers("foo_set1")) set(['22',"11"]) 获取集合1中所有的成员
# print(r.smembers("foo_set4")) set(['22',"33"]) 获取集合4中所有的成员
#
# 10 删除--随机删除并且返回被删除值
# spop(name)
# 从集合移除一个成员，并将其返回,说明一下，集合是无序的，所有是随机删除的
# print(r.smembers("foo_set1")) set(['11', '22', '33', '44', '55', '66']) 获取集合1中所有的成员
# print(r.spop("foo_set1")) 44 （这个删除的值是随机删除的，集合是无序的）
# print(r.smembers("foo_set1")) set(['11', '33', '66', '22', '55']) 获取集合1中所有的成员
#
# 11 删除--指定值删除
# srem(name, values)
# 在name对应的集合中删除某些值
# print(r.smembers("foo_set1")) set(['11', '33', '66', '22', '55'])
# r.srem("foo_set1",66) 从集合中删除指定值 66
# print(r.smembers("foo_set1")) set(['11', '33', '22', '55'])
#
# 12 随机获取多个集合的元素
# srandmember(name, numbers)
# 从name对应的集合中随机获取 numbers 个元素
# print(r.srandmember("foo_set1",3)) ['33', '55', '66'] 随机获取3个元素
# print(r.smembers("foo_set1")) set(['11', '33', '66', '22', '55'])
#
# # *******************************************************************************************************************************
# # 07 redis基本命令_有序set
# Set操作，Set集合就是不允许重复的列表，本身是无序的
# 有序集合，在集合的基础上，为每元素排序；元素的排序需要根据另外一个值来进行比较，
# 所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。
#
#
# 1 新增
# zadd(name, *args, **kwargs)
# 在name对应的有序集合中添加元素
# 如：
# zadd('zz', 'n1', 1, 'n2', 2)
# 或
# zadd('zz', n1=11, n2=22)
# r.zadd("foo_zset1",n3=11,n4=22)
# r.zadd("foo_zset2",n3=11,n4=23)
# print(r.zcard("foo_zset1")) 2 长度是2 2个元素
# print(r.zrange("foo_zset1",0,-1)) ['n1', 'n2'] 获取有序集合中所有元素
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n1', 11.0), ('n2', 22.0)] 获取有序集合中所有元素和分数
#
# 2 获取有序集合元素个数 类似于len
# zcard(name)
# 获取name对应的有序集合元素的数量
#
# 3 获取有序集合的所有元素
# r.zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)
# 按照索引范围获取name对应的有序集合的元素
# 参数：
# name，redis的name
# start，有序集合索引起始位置（非分数）
# end，有序集合索引结束位置（非分数）
# desc，排序规则，默认按照分数从小到大排序
# withscores，是否获取元素的分数，默认只获取元素的值
# score_cast_func，对分数进行数据转换的函数
# 更多：
# 从大到小排序
# zrevrange(name, start, end, withscores=False, score_cast_func=float)
# 按照分数范围获取name对应的有序集合的元素
# zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float)
# 从大到小排序
# zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float)
#
# 3-1 从大到小排序
# zrevrange(name, start, end, withscores=False, score_cast_func=float)
# print(r.zrevrange("foo_zset1",0,-1)) ['n2', 'n1'] 只获取元素，不显示分数
# print(r.zrevrange("foo_zset1",0,-1,withscores=True)) [('n2', 22.0), ('n1', 11.0)]
# 获取有序集合中所有元素和分数,安装分数倒序
#
# 3-2 按照分数范围获取name对应的有序集合的元素
# zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float)
# print(r.zrangebyscore("foo_zset1",15,25)) ['n2']
# print(r.zrangebyscore("foo_zset1",12,22, withscores=True)) [('n2', 22.0)]
# 在分数是12-22之间（左闭右闭），取出符合条件的元素
#
# 3-3 从大到小排序
# zrevrangebyscore(name, max, min, start=None, num=None, withscores=False, score_cast_func=float)
# print(r.zrevrangebyscore("foo_zset1",22,11,withscores=True)) [('n2', 22.0), ('n1', 11.0)]
# 在分数是22-11之间（左闭右闭），取出符合条件的元素 按照分数倒序
#
# 3-4 获取所有元素--默认按照分数顺序排序
# zscan(name, cursor=0, match=None, count=None, score_cast_func=float)
# print(r.zscan("foo_zset1")) (0L, [('n3', 11.0), ('n4', 22.0), ('n2', 30.0)])
#
# 3-5 获取所有元素--迭代器
# zscan_iter(name, match=None, count=None,score_cast_func=float)
# for i in r.zscan_iter("foo_zset1"): 遍历迭代器
# print(i)
# ('n3', 11.0)
# ('n4', 22.0)
# ('n2', 30.0)
#
# 4 zcount(name, min, max)
# 获取name对应的有序集合中分数 在 [min,max] 之间的个数
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n1', 11.0), ('n2', 22.0)]
# print(r.zcount("foo_zset1",11,22)) 2
#
# 5 自增
# zincrby(name, value, amount)
# 自增name对应的有序集合的 name 对应的分数
# r.zincrby("foo_zset1","n2",amount=2) 每次将n2的分数自增2
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n1', 11.0), ('n2', 30.0)]
#
# 6 获取值的索引号
# zrank(name, value)
# 获取某个值在 name对应的有序集合中的排行（从 0 开始）
# 更多：
# zrevrank(name, value)，从大到小排序
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n1', 11.0), ('n2', 30.0)]
# print(r.zrank("foo_zset1","n1")) 0 n1的索引号是0 这里按照分数顺序（从小到大）
# print(r.zrank("foo_zset1","n2")) 1 n2的索引号是1
#
# print(r.zrevrank("foo_zset1","n1")) 1 n1的索引号是1 这里安照分数倒序（从大到小）
#
# 7 删除--指定值删除
# zrem(name, values)
# 删除name对应的有序集合中值是values的成员
# 如：zrem('zz', ['s1', 's2'])
# print(r.zrange("foo_zset1",0,-1,withscores=True))
# r.zrem("foo_zset2","n3") 删除有序集合中的元素n1 删除单个
# print(r.zrange("foo_zset1",0,-1,withscores=True))
#
# 8 删除--根据排行范围删除，按照索引号来删除
# zremrangebyrank(name, min, max)
# 根据排行范围删除
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n3', 11.0), ('n4', 22.0), ('n2', 30.0)]
# r.zremrangebyrank("foo_zset1",0,1) 删除有序集合中的索引号是0,1的元素
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n2', 30.0)]
#
# 9 删除--根据分数范围删除
# zremrangebyscore(name, min, max)
# 根据分数范围删除
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n3', 11.0), ('n4', 22.0), ('n2', 30.0)]
# r.zremrangebyscore("foo_zset1",11,22) 删除有序集合中的分数是11-22的元素
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n2', 30.0)]
#
# 10 获取值对应的分数
# zscore(name, value)
# 获取name对应有序集合中 value 对应的分数
# print(r.zrange("foo_zset1",0,-1,withscores=True)) [('n3', 11.0), ('n4', 22.0), ('n2', 30.0)]
# print(r.zscore("foo_zset1","n3")) 11.0 获取元素n3对应的分数11.0
#
#
#
# # *******************************************************************************************************************************
# 08 其他常用操作
# 1 删除
# delete(*names)
# 根据删除redis中的任意数据类型（string、hash、list、set、有序set）
#
# 1-1删除string
# r.set('foo', 'Bar')
# print(r.strlen("foo")) 3 3ge 字节
# print(r.getrange("foo",0,-1)) Bar
# r.delete("foo") 删除字符串类型的foo
# print(r.get("foo")) None
# print(r.getrange("foo",0,-1))
# print(r.strlen("foo")) 0 0个字节
#
# 1-2 删除hash
# r.hset("foo_hash4","k1","v1")
# print(r.hscan("foo_hash4")) (0L, {'k1': 'v1'})
# r.delete("foo_hash4") 删除hash类型的键值对
# print(r.hscan("foo_hash4")) (0L, {})
#
# 2 检查名字是否存在
# exists(name)
# 检测redis的name是否存在
# print(r.exists("foo_hash4")) True 存在就是True
# print(r.exists("foo_hash5")) False 不存在就是False
#
# 2-1
# r.lpush("foo_list5",11,22)
# print(r.lrange("foo_list5",0,-1)) ['22', '11', '22', '11']
# print(r.exists("foo_list5")) True 存在就是True
# print(r.exists("foo_list6")) False 不存在就是False
#
# 3 模糊匹配
# keys(pattern='*')
# 根据模型获取redis的name
# 更多：
# KEYS * 匹配数据库中所有 key 。
# KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
# KEYS h*llo 匹配 hllo 和 heeeeello 等。
# KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo
# print(r.keys("foo*"))
# ['foo_hash1', 'foo_bingji', 'foo_list1', 'foo_list2', 'foo3', 'foo_set2', 'foo_hash4', 'foo_zset2',
# 'foo2', 'foo4', 'foo_set1', 'foo_zset1', 'foo_hash2', 'foo1', 'foo_list5', 'foo_set3']
#
# 4 设置超时时间
# expire(name ,time)
# 为某个redis的某个name设置超时时间
# r.lpush("foo_list5",11,22)
# r.expire("foo_list5",time=10)
# print(r.lrange("foo_list5",0,-1))
#
# 5 重命名
# rename(src, dst)
# 对redis的name重命名为
# r.rename("foo_list6","foo_list5")
# print(r.lrange("foo_list5",0,-1)) ['22', '11']
# print(r.lrange("foo_list6",0,-1)) []
#
# 6 随机获取name
# randomkey()
# 随机获取一个redis的name（不删除）
# print(r.keys("foo*"))
# ['foo_set1', 'foo3', 'foo_set2', 'foo_zset2', 'foo4', 'foo_zset1', 'foo_list5', 'foo2',
# 'foo_hash2', 'foo1', 'foo_set3', 'foo_hash1', 'foo_hash4', 'foo_list2', 'foo_bingji']
# print(r.randomkey()) foo_hash2 随机获取一个name
#
# 7 获取类型
# type(name)
# 获取name对应值的类型
# print(r.type("foo_hash2")) hash
# print(r.type("foo_set1")) set
# print(r.type("foo3")) string
#
# 8 查看所有元素
# scan(cursor=0, match=None, count=None)
# print(r.hscan("foo_hash2")) (0L, {'k3': 'v3', 'k2': 'v2'})
# print(r.sscan("foo_set3")) (0L, ['22'])
# print(r.zscan("foo_zset2")) (0L, [('n4', 23.0)])
# print(r.getrange("foo1",0,-1)) 121 --字符串
# print(r.lrange("foo_list5",0,-1)) ['22', '11'] --列表
#
# 9 查看所有元素--迭代器
# scan_iter(match=None, count=None)
# for i in r.hscan_iter("foo_hash2"):--遍历
# print(i)
# ('k3', 'v3')
# ('k2', 'v2')
#
# for i in r.sscan_iter("foo_set3"):
# print(i) 22
#
# for i in r.zscan_iter("foo_zset2"):
# print(i) ('n4', 23.0)
#




# *******************************************************************************************************************************
# redis
# redis连接实例是线程安全的，可以直接将redis连接实例设置为一个全局变量，直接使用。如果需要另一个Redis实例（or Redis数据库）时，就需要重新创建redis连接实例来获取一个新的连接。同理，python的redis没有实现select命令。
# >>> import redis
# >>> r = redis.Redis(host='localhost',port=6379,db=0)
# >>> r.set('guo','shuai')
# True
# >>> r.get('guo')
# 'shuai'
# >>> r['guo']
# 'shuai'
# >>> r.keys()
# ['guo']
# >>> r.dbsize()         #当前数据库包含多少条数据
# 1L
# >>> r.delete('guo')
# 1
# >>> r.save()               #执行“检查点”操作，将数据写回磁盘。保存时阻塞
# True
# >>> r.get('guo');
# >>> r.flushdb()        #清空r中的所有数据
# True


# *******************************************************************************************************************************
# pipeline操作
# 管道（pipeline）是redis在提供单个请求中缓冲多条服务器命令的基类的子类。它通过减少服务器-客户端之间反复的TCP数据库包，从而大大提高了执行批量命令的功能。
# # 创建一个管道
# p = connRedis167.pipeline()
# p.set('hello', 'redis')
# p.sadd('faz', 'baz')
# p.incr('num')
# p.execute()
# # [True, 1, 1]
# connRedis167.get('hello')
# # 'redis'
# 管道的命令可以写在一起，如：
# p.set('hello','redis').sadd('faz','baz').incr('num').execute()
# 默认的情况下，管道里执行的命令可以保证执行的原子性，执行pipe = r.pipeline(transaction=False)可以禁用这一特性。

# 如：
# redis-py默认在执行每次请求都会创建（连接池申请连接）和断开（归还连接池）一次连接操作，
# 如果想要在一次请求中指定多个命令，则可以使用pipline实现一次请求指定多个命令，并且默认情况下一次pipline 是原子性操作。
# import redis
# pool = redis.ConnectionPool(host='192.168.19.130', port=6379)
# r = redis.Redis(connection_pool=pool)
# pipe = r.pipeline(transaction=False)
# pipe = r.pipeline(transaction=True)
# r.set('name', 'jack')
# r.set('role', 'sb')
#
# pipe.execute()
#
# print(r.get("name")) jack
# print(r.get("role")) sb



# *******************************************************************************************************************************
# 应用场景 – 页面点击数
# 《Redis Cookbook》对这个经典场景进行详细描述。假定我们对一系列页面需要记录点击次数。例如论坛的每个帖子都要记录点击次数，而点击次数比回帖的次数的多得多。如果使用关系数据库来存储点击，可能存在大量的行级锁争用。所以，点击数的增加使用redis的INCR命令最好不过了。
# 当redis服务器启动时，可以从关系数据库读入点击数的初始值（1237这个页面被访问了34634次）
# >>> r.set("visit:1237:totals",34634)
# True
# 每当有一个页面点击，则使用INCR增加点击数即可。
#
# >>> r.incr("visit:1237:totals")
# 34635
# >>> r.incr("visit:1237:totals")
# 34636
# 页面载入的时候则可直接获取这个值
# >>> r.get ("visit:1237:totals")
# '34636'


# *******************************************************************************************************************************
# 使用hash类型保存多样化对象
# 当有大量类型文档的对象，文档的内容都不一样时，（即“表”没有固定的列），可以使用hash来表达。
#
# >>> r.hset('users:jdoe',  'name', "John Doe")
# 1L
# >>> r.hset('users:jdoe', 'email', 'John@test.com')
# 1L
# >>> r.hset('users:jdoe',  'phone', '1555313940')
# 1L
# >>> r.hincrby('users:jdoe', 'visits', 1)
# 1L
# >>> r.hgetall('users:jdoe')
# {'phone': '1555313940', 'name': 'John Doe', 'visits': '1', 'email': 'John@test.com'}
# >>> r.hkeys('users:jdoe')
# ['name', 'email', 'phone', 'visits']



# *******************************************************************************************************************************
# # 应用场景 – 社交圈子数据
# # 在社交网站中，每一个圈子(circle)都有自己的用户群。通过圈子可以找到有共同特征（比如某一体育活动、游戏、电影等爱好者）的人。当一个用户加入一个或几个圈子后，系统可以向这个用户推荐圈子中的人。
# # 我们定义这样两个圈子,并加入一些圈子成员。
# >>> r.sadd('circle:game:lol','user:debugo')
# >>> r.sadd('circle:game:lol','user:leo')
# >>> r.sadd('circle:game:lol','user:Guo')
# >>> r.sadd('circle:soccer:InterMilan','user:Guo')
# >>> r.sadd('circle:soccer:InterMilan','user:Levis')
# >>> r.sadd('circle:soccer:InterMilan','user:leo')
# #获得某一圈子的成员
# >>> r.smembers('circle:game:lol')
# set(['user:Guo', 'user:debugo', 'user:leo'])
# redis> smembers circle:jdoe:family
# 可以使用集合运算来得到几个圈子的共同成员：
# >>> r.sinter('circle:game:lol', 'circle:soccer:InterMilan')
# set(['user:Guo', 'user:leo'])
# >>> r.sunion('circle:game:lol', 'circle:soccer:InterMilan')
# set(['user:Levis', 'user:Guo', 'user:debugo', 'user:leo'])



# *******************************************************************************************************************************
# 应用场景 – 实时用户统计
# Counting Online Users with Redis介绍了这个方法。当我们需要在页面上显示当前的在线用户时，就可以使用Redis来完成了。首先获得当前时间（以Unix timestamps方式）除以60，可以基于这个值创建一个key。然后添加用户到这个集合中。当超过你设定的最大的超时时间，则将这个集合设为过期；而当需要查询当前在线用户的时候，则将最后N分钟的集合交集在一起即可。由于redis连接对象是线程安全的，所以可以直接使用一个全局变量来表示。
#
# import time
# from redis import Redis
# from datetime import datetime
# ONLINE_LAST_MINUTES = 5
# redis = Redis()
#
# def mark_online(user_id):         #将一个用户标记为online
#     now = int(time.time())        #当前的UNIX时间戳
#     expires = now + (app.config['ONLINE_LAST_MINUTES'] * 60) + 10    #过期的UNIX时间戳
#     all_users_key = 'online-users/%d' % (now // 60)        #集合名，包含分钟信息
#     user_key = 'user-activity/%s' % user_id
#     p = redis.pipeline()
#     p.sadd(all_users_key, user_id)                         #将用户id插入到包含分钟信息的集合中
#     p.set(user_key, now)                                   #记录用户的标记时间
#     p.expireat(all_users_key, expires)                     #设定集合的过期时间为UNIX的时间戳
#     p.expireat(user_key, expires)
#     p.execute()
#
# def get_user_last_activity(user_id):        #获得用户的最后活跃时间
#     last_active = redis.get('user-activity/%s' % user_id)  #如果获取不到，则返回None
#     if last_active is None:
#         return None
#     return datetime.utcfromtimestamp(int(last_active))
#
# def get_online_users():                     #获得当前online用户的列表
#     current = int(time.time()) // 60
#     minutes = xrange(app.config['ONLINE_LAST_MINUTES'])
#     return redis.sunion(['online-users/%d' % (current - x)        #取ONLINE_LAST_MINUTES分钟对应集合的交集
#                          for x in minutes])
