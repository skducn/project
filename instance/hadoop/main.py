# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-2-26
# Description: python3 调用HDFS集群API
# pip install pyhdfs -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# https://www.cnblogs.com/hziwei/p/12801867.html
# https://blog.csdn.net/agurt80004/article/details/101136785
# pyhdfs.HdfsClient(hosts: Union[str, Iterable[str]] = 'localhost',
# randomize_hosts: bool = True,
# user_name: Optional[str] = None,
# timeout: float = 20,
# max_tries: int = 2,
# retry_delay: float = 5,
# requests_session: Optional[requests.sessions.Session] = None,
# requests_kwargs: Optional[Dict[str, Any]] = None)
# 参数：
# hosts（list 或str）– NameNode HTTP host：port字符串的列表，可以list是逗号分隔的字符串。如果未指定，则端口默认为50070。请注意，在Hadoop 3中，默认的NameNode HTTP端口已更改为9870。旧版本的默认值50070保持向后兼容。
# randomize_hosts（bool）–默认情况下，随机选择主机。
# user_name –以什么Hadoop用户身份运行。默认为HADOOP_USER_NAME环境变量（如果存在），否则为getpass.getuser()。
# timeout（float）–等待一个NameNode持续多长时间（以秒为单位）。在某些情况下，备用NameNode可能无响应（例如，加载fsimage或检查点），因此我们不想对其进行阻止。
# max_tries（int）–对每个NameNode重试请求的次数。如果NN1处于待机状态，而NN2处于活动状态，则我们可能首先联系NN1，然后在联系NN2时观察到故障转移到NN1。在这种情况下，我们要针对NN1重试。
# retry_delay（float）–再次经历NameNodes之前要等待的时间（以秒为单位）
# requests_session –一个requests.Session高级用法的对象。如果不存在，则此类将使用默认请求行为，即每个HTTP请求进行新会话。呼叫者负责关闭会话。
# request_kwargs – **kwargs传递给请求的附加项

# todo 注意事项
# 使用pyhdfs连接hdfs，连接时需要修改本机hosts文件中的IP地址与主机名的映射，不然会报错。
# for win：C:\WINDOWS\system32\drivers\etc\hosts  //添加hadoop集群主机的映射关系
# for mac: /etc/hosts
# 例如 添加一下主机映射：
# 192.168.1.202 hadoop102
# *****************************************************************

import pyhdfs

fs = pyhdfs.HdfsClient(hosts='192.168.1.202:9870', user_name='root')

# 返回可用的namenode节点
print(fs.get_active_namenode())  # 192.168.1.202:9870

# 返回用户的根目录
print(fs.get_home_directory())  # /user/root

# 返回指定目录下所有文件
print(fs.listdir("/"))  # ['input', 'tmp', 'wcoutput', 'wcoutput3', 'wcoutput4', 'wcoutput5', 'wcoutput6']


# 本地上传到hadoop
# fs.copy_from_local("/Users/linghuchong/Downloads/qq.txt", "/input/q2.txt")

# 从hadoop下载到本地
# fs.copy_to_local("/input/q2.txt", "/Users/linghuchong/Downloads/qq123.txt")

# 判断hadoop上目录或文件是否存在
print(fs.exists("/input/q2.txt"))  # True
print(fs.exists("/input/"))  # True
print(fs.exists("/input/121212.txt"))  # False

# 返回目录下所有目录、路径、文件名
print(list(fs.walk('/input')))  # [('/input', [], ['1.txt', 'jdk-8u401-linux-x64.tar.gz', 'q2.txt', 'test.txt', 'word.txt'])]

# 删除hadoop上目录、文件
# fs.delete("/mp4", recursive=True)  # 删除目录  recursive=True
# fs.delete("/mp4/3.mp4  ")  # 删除文件

# 获取文件内容
r = fs.open("/input/1.txt")
print(r.read())  # b'1\n2\ntest\nhello\n'

# # 文件追加内容
# fs.append("/input/1.txt", "123\hello")
# r = fs.open("/input/1.txt")
# print(r.read())  # b'1\n2\ntest\nhello\n123\\hello'

# 查看文件大小
print(fs.get_file_checksum("/input/1.txt"))

# 查看单个路径的状态
print(fs.list_status("/input"))
# [FileStatus(accessTime=1708926152661, blockSize=134217728, childrenNum=0, fileId=16390, group='supergroup', length=33, modificationTime=1708926318321, owner='root', pathSuffix='1.txt', permission='644', replication=2, storagePolicy=0, type='FILE'), FileStatus(accessTime=1708650381134, blockSize=134217728, childrenNum=0, fileId=16511, group='supergroup', length=141600542, modificationTime=1708650392815, owner='root', pathSuffix='jdk-8u401-linux-x64.tar.gz', permission='644', replication=3, storagePolicy=0, type='FILE'), FileStatus(accessTime=1708925447875, blockSize=134217728, childrenNum=0, fileId=16512, group='supergroup', length=20, modificationTime=1708925449242, owner='root', pathSuffix='q2.txt', permission='644', replication=3, storagePolicy=0, type='FILE'), FileStatus(accessTime=1708582076676, blockSize=134217728, childrenNum=0, fileId=16388, group='supergroup', length=10, modificationTime=1708572989401, owner='root', pathSuffix='test.txt', permission='644', replication=3, storagePolicy=0, type='FILE'), FileStatus(accessTime=1708582076583, blockSize=134217728, childrenNum=0, fileId=16387, group='supergroup', length=25, modificationTime=1708572838887, owner='root', pathSuffix='word.txt', permission='644', replication=3, storagePolicy=0, type='FILE')]

# 查看单个文件状态
print(fs.list_status("/input/1.txt"))
# [FileStatus(accessTime=1708926152661, blockSize=134217728, childrenNum=0, fileId=16390, group='supergroup', length=33, modificationTime=1708926318321, owner='root', pathSuffix='', permission='644', replication=2, storagePolicy=0, type='FILE')]

