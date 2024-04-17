# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-3-14
# Description:  InfluxDB HTTP API 时序数据库
# pip3 install influxdb-client
# 参考：https://blog.csdn.net/weixin_45589713/article/details/136059049

# 参考【腾讯文档】jmeter实战案例 中 influxDB ,API token来自于这里。
# https://docs.qq.com/doc/DYnRKRUZyZkdHZWVi
# *****************************************************************


import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Q4aC1JEgSenXFin9o-HMRl5Rj3-NGQCRT-nqZda0CA0fuJW2U57CEl4vmdUsraDTOq_UvxZUxGev8cvDuPGOdQ=="
org = "testTeam"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

from influxdb import InfluxDBClient
client2 = InfluxDBClient(host='localhost', port=8086, token=token)
client2.switch_database(database="jmeter")

result = client2.query('select * from jmeter')
print(result)


# # 写入数据
# bucket = "jinhao"
#
# write_api = client.write_api(write_options=SYNCHRONOUS)
#
# for value in range(5):
#     point = (
#         Point("measurement1")
#             .tag("tagname1", "tagvalue1")
#             .field("field1", value)
#     )
#     write_api.write(bucket=bucket, org="testTeam", record=point)
#     time.sleep(1)  # separate points by 1 second
#
#
# # 查询数据
#
# query_api = client.query_api()
#
# query = """from(bucket: "jinhao")
#  |> range(start: -10m)
#  |> filter(fn: (r) => r._measurement == "measurement1")"""
# tables = query_api.query(query, org="testTeam")
#
# for table in tables:
#   for record in table.records:
#     print(record)
#
# # 结果：
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 50, 480051, tzinfo=tzutc()), '_value': 0, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 51, 805028, tzinfo=tzutc()), '_value': 1, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 52, 834429, tzinfo=tzutc()), '_value': 2, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 53, 858986, tzinfo=tzutc()), '_value': 3, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 54, 878475, tzinfo=tzutc()), '_value': 4, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}