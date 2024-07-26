# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-3-14
# Description:  InfluxDB HTTP API 时序数据库
# pip3 install influxdb-client
# 参考：https://blog.csdn.net/weixin_45589713/article/details/136059049
# https://www.cnblogs.com/aimoboshu/p/17037326.html
# https://influxdb-client.readthedocs.io/en/latest/api.html#queryapi


# 参考【腾讯文档】jmeter实战案例 中 influxDB ,API token来自于这里。
# https://docs.qq.com/doc/DYnRKRUZyZkdHZWVi

# url = "http://localhost:8086"
# username: linghuchong
# password:jinhao123
# org:testTeam
# bucket:jinhao
# token = "Q4aC1JEgSenXFin9o-HMRl5Rj3-NGQCRT-nqZda0CA0fuJW2U57CEl4vmdUsraDTOq_UvxZUxGev8cvDuPGOdQ=="
# *****************************************************************

import influxdb_client, os, time
import requests
import pandas as pd

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WriteOptions
url = "http://localhost:8086"
token = "Q4aC1JEgSenXFin9o-HMRl5Rj3-NGQCRT-nqZda0CA0fuJW2U57CEl4vmdUsraDTOq_UvxZUxGev8cvDuPGOdQ=="
org = "testTeam"
bucket = "jinhao"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


# 写入数据
# 点数据集插入数据（ok）
# # # mydb是数据库，measurement1表名，tagname1是标签名，tagvalue1是标签值，field1是字段名，value是字段值
# write_api = client.write_api(write_options=SYNCHRONOUS)
# for value in range(5):
#     point = (
#         Point("m3")
#             .tag("tagname1", "tagvalue1")
#             .field("field1", value)
#     )
#     write_api.write(bucket=bucket, org="testTeam", record=point)
#     time.sleep(1)  # separate points by 1 second


# 数据帧插入数据(测试未通过)

data = {
    "time": ["2022-01-01T00:00:00Z", "2022-01-02T00:00:00Z"],
    "measurement": ["measurement-name", "measurement-name"],
    "tag-key": ["tag-value", "tag-value"],
    "field-key": ["field-value", "field-value"]
}

df = pd.DataFrame(data)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
write_api.write(bucket=bucket, record=df, data_frame_measurement_name="m4")



# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------


#
# # # # 查询数据(ok)
# # # # 参考：https://influxdb-client.readthedocs.io/en/latest/api.html#queryapi
# query_api = client.query_api()
# query = """from(bucket: "test2") |> range(start: -1000m) |> filter(fn: (r) => r._measurement == "m1")"""
# tables = query_api.query(query, org="testTeam")
# for table in tables:
#   for record in table.records:
#     print(record)
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 7, 25, 13, 9, 33, 710974, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 7, 26, 5, 49, 33, 710974, tzinfo=tzutc()), '_time': datetime.datetime(2024, 7, 26, 5, 33, 59, 343398, tzinfo=tzutc()), '_value': 1.2, '_field': 'field1', '_measurement': 'm1', 'host': 'host1', 'location': 'us-midwest'}
# # FluxRecord() table: 1, {'result': '_result', 'table': 1, '_start': datetime.datetime(2024, 7, 25, 13, 9, 33, 710974, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 7, 26, 5, 49, 33, 710974, tzinfo=tzutc()), '_time': datetime.datetime(2024, 7, 26, 5, 38, 46, 202816, tzinfo=tzutc()), '_value': 2.4, '_field': 'field1', '_measurement': 'm1', 'host': 'host2', 'location': 'us-midwest'}


# 关闭客户端连接
client.close()
