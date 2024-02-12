# coding: utf-8
#****************************************************************
# Author     : John
# Date       : 2016-6-13
# Description: redis 实现分布式锁
#  python + redis 实现分布式锁 https://zhuanlan.zhihu.com/p/628951850
# 下载：http://download.redis.io/releases/
#****************************************************************
# 一般来说，mongodb 或者 mysql来做持久层，redis做缓存
# redis-py 提供两个类 Redis 和 StrictRedis 用于实现Redis的命令，StrictRedis用于实现大部分官方的命令，
# 并使用官方的语法和命令，Redis是StrictRedis的子类，用于向后兼容旧版本的redis-py。
# redis配置文件redis.conf的详细说明 http://blog.csdn.net/vv_demon/article/details/7676384
# 【python】redis基本命令和基本用法详解 http://www.cnblogs.com/wangtp/p/5636872.html
# redis单机安装以及简单redis集群搭建  https://www.cnblogs.com/mirakel/p/7251053.html



import time
import uuid
import redis
from threading import Thread

# redis 存字符串返回的是byte, 指定 decode_responses=True 可以解决
pool = redis.ConnectionPool(host="127.0.0.1", port=6379, socket_connect_timeout=3, decode_responses=True)
redis_cli = redis.Redis(connection_pool=pool)


# 加锁
def acquire_lock(lock_name, acquire_timeout=4, lock_timeout=7):
    """
    param lock_name: 锁名称
    param acquire_timeout: 客户端获取锁的超时时间
    param lock_timeout: 锁过期时间, 超过这个时间锁自动释放
    """
    identifier = str(uuid.uuid4())
    end_time = time.time() + acquire_timeout   # 客户端获取锁的结束时间
    while time.time() <= end_time:
        # setnx(key, value) 只有 key 不存在情况下将 key 设置为 value 返回 True
        # 若 key 存在则不做任何动作,返回 False
        if redis_cli.setnx(lock_name, identifier):
            redis_cli.expire(lock_name, lock_timeout)   # 设置锁的过期时间，防止线程获取锁后崩溃导致死锁
            return identifier   # 返回锁唯一标识
        elif redis_cli.ttl(lock_name) == -1:   # 当锁未被设置过期时间时，重新设置其过期时间
            redis_cli.expire(lock_name, lock_timeout)
        time.sleep(0.001)
    return False   # 获取超时返回 False


# 释放锁
def release_lock(lock_name, identifier):
    """
    param lock_name:   锁名称
    param identifier:  锁标识
    """
    # 解锁操作需要在一个 redis 事务中进行，python 中 redis 事务通过 pipeline 封装实现
    with redis_cli.pipeline() as pipe:
        while True:
            try:
                # 使用 WATCH 监听锁，如果删除过程中锁自动失效又被其他客户端拿到，即锁标识被其他客户端修改
                # 此时设置了 WATCH 事务就不会再执行，这样就不会出现删除了其他客户端锁的情况
                pipe.watch(lock_name)
                id = pipe.get(lock_name)
                if id and id == identifier:   # 判断解锁与加锁线程是否一致
                    pipe.multi()
                    pipe.delete(lock_name)   # 标识相同，在事务中删除锁
                    pipe.execute()    # 执行EXEC命令后自动执行UNWATCH
                    return True
                pipe.unwatch()
                break
            except redis.WatchError:
                pass
        return False


def exec_test(thread_name):
    identifier = acquire_lock('jaye')
    if identifier:   # 如果获取到锁,则执行业务逻辑
        print(f'{thread_name} 获取 redis 分布式锁成功！')
        time.sleep(3)   # 模拟业务耗时
        res = release_lock('jaye', identifier)   # 处理完之后释放锁
        print(f'{thread_name} 释放状态: {res}')
    else:
        print(f'{thread_name} 获取 redis 分布式锁失败, 其他线程正在使用')



if __name__ == '__main__':
    for i in range(10):
        t_name = f'thread_{i}'
        t = Thread(target=exec_test, args=(t_name,))
        t.start()