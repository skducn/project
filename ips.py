# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-4-27
# Description: # 快代理 - 免费代理 - 国内高匿代理
# 快代理 https://www.kuaidaili.com/free/inha/1/
# *****************************************************************

# http://122.4.44.101:9999
# http://121.233.207.219:9999
# http://175.42.122.164:9999
# http://175.43.57.47:9999
# http://219.151.157.130:3128
# http://114.239.2.151:9999
# http://180.120.209.130:8888
# http://183.166.163.192:9999
# http://113.120.62.237:9999
# http://120.83.96.49:9999
# http://182.46.122.112:9999
# http://163.204.247.194:9999
# http://150.255.8.206:9999
# http://49.86.182.169:9999
# http://49.86.176.213:9999

import requests,json
from PO.DataPO import *
Data_PO = DataPO()

# print(Data_PO.getIpAgent())
proxies = {"url": Data_PO.getIpAgent()}
# proxies = {"url": "http://183.166.163.192:9999"}
# print(proxies)

print(Data_PO.getUserAgent())
# headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
headers = {'user-agent': Data_PO.getUserAgent()}  # {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15'}
# print(headers)

response = requests.get(url="https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&_signature=_02B4Z6wo00d01fvn0YwAAIDCSxY9RVtwNlH7wtUAAB6A2JVj2nlWEjSOc-lM3cuw3CMwjgeCaE3YOlaB8m9h1KXkLks00Mx0nTEqpVhbWkT4F6PcW6NjNqpMl6ecsp8crnX41QHPcvftP6C323"
                        ,headers=headers
                        ,proxies=proxies)

# print(response.text)
print(response.text.encode("utf-8").decode("unicode_escape"))
print("---------------")
response_json = json.loads(response.text)
print(response_json)
print(response_json["data"])

data = response_json["data"]
for i in range(len(data)):
    data_dict = data[i]
    print(data_dict)
    with open("doutiao.json", "w") as f:
        json.dump(data_dict, f, ensure_ascii=False)
        f.write("\n")


import pandas as pd
df= pd.read_json("doutiao.json",lines=True,encoding="gbk")
print(df["abstract"])
print(df)
df.to_excel("2.xlsx")