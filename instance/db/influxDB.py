# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-3-14
# Description:  InfluxDB HTTP API 时序数据库
# pip3 install influxdb-client
# 参考：https://blog.csdn.net/weixin_45589713/article/details/136059049
# https://influxdb-client.readthedocs.io/en/latest/api.html#queryapi
# https://www.cnblogs.com/aimoboshu/p/17037326.html


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

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
token = "Q4aC1JEgSenXFin9o-HMRl5Rj3-NGQCRT-nqZda0CA0fuJW2U57CEl4vmdUsraDTOq_UvxZUxGev8cvDuPGOdQ=="
org = "testTeam"
url = "http://localhost:8086"
bucket = "mydb"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# 写入数据ok
# # mydb是数据库，measurement1表名，tagname1是标签名，tagvalue1是标签值，field1是字段名，value是字段值
# write_api = client.write_api(write_options=SYNCHRONOUS)
# for value in range(5):
#     point = (
#         Point("measurement1")
#             .tag("tagname1", "tagvalue1")
#             .field("field1", value)
#     )
#     write_api.write(bucket=bucket, org="testTeam", record=point)
#     time.sleep(1)  # separate points by 1 second

# 在influxdb中查看数据ok
# > select * from measurement1
# name: measurement1
# time                field1 tagname1
# ----                ------ --------
# 1721899962326868000 0      tagvalue1
# 1721899963387882000 1      tagvalue1
# 1721899964410089000 2      tagvalue1
# 1721899965433381000 3      tagvalue1
# 1721899966452422000 4      tagvalue1
# >

# -------------------------------------------------------------------------------------

# 获取数据ok
# 构建请求 URL
url = f"{url}/query"
# 查询参数
params = {
  'q': 'SHOW MEASUREMENTS',  # 示例查询，列出所有的测量
  'db': bucket
}
# 发送 GET 请求
response = requests.get(url, params=params)
# 检查响应并输出结果
if response.status_code == 200:
  query_result = response.json()
  print(query_result)  # {'results': [{'statement_id': 0, 'series': [{'name': 'measurements', 'columns': ['name'], 'values': [['cpu'], ['cpu_load_short'], ['measurement1'], ['temperature']]}]}]}
else:
  print("Error: ", response.content)

# -------------------------------------------------------------------------------------

#
# from influxdb import InfluxDBClient
# client2 = InfluxDBClient(host='localhost', port=8086, token=token)
# client2.switch_database(database="mydb")
#
# result = client2.query('select * from mydb')
# print(result)



# with InfluxDBClient(url="http://localhost:8086", token=token, org="testTeam") as client:
#
#   # Query: using Table structure
#   tables = client.query_api().query('from(bucket:"mydb") |> range(start: -10m)')
#
#   # Serialize to values
#   output = tables.to_values(columns=['location', '_time', '_value'])
#   print(output)


#
# # # 查询数据
# # # 参考：https://influxdb-client.readthedocs.io/en/latest/api.html#queryapi
query_api = client.query_api()

query = """from(bucket: "mydb") |> range(start: -10m) |> filter(fn: (r) => r._measurement == "jmeter")"""
tables = query_api.query(query, org="testTeam")

for table in tables:
  for record in table.records:
    print(record)




# # 结果：
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 50, 480051, tzinfo=tzutc()), '_value': 0, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 51, 805028, tzinfo=tzutc()), '_value': 1, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 52, 834429, tzinfo=tzutc()), '_value': 2, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 53, 858986, tzinfo=tzutc()), '_value': 3, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
# # FluxRecord() table: 0, {'result': '_result', 'table': 0, '_start': datetime.datetime(2024, 3, 14, 2, 1, 55, 900818, tzinfo=tzutc()), '_stop': datetime.datetime(2024, 3, 14, 2, 11, 55, 900818, tzinfo=tzutc()), '_time': datetime.datetime(2024, 3, 14, 2, 11, 54, 878475, tzinfo=tzutc()), '_value': 4, '_field': 'field1', '_measurement': 'measurement1', 'tagname1': 'tagvalue1'}
