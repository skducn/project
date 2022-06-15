# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-11-18
# Description: # api（json）转 excel
# *****************************************************************

from PO.DataPO import *
Data_PO = DataPO()

# 解析api
response = requests.get(url="https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=__all__&utm_source=toutiao&widen=1&tadrequire=true"
                        , headers={'user-agent': Data_PO.getUserAgent()}
                        , proxies={"url": Data_PO.getIpAgent()})
# print(response.text)
# print(response.text.encode("utf-8").decode("unicode_escape"))

# 转换成json字典
response_json = json.loads(response.text)
# print(response_json)
# print(response_json["data"])
# print(response_json["data"][0]['abstract'])

# 抽取内容保存到文件
data = response_json["data"]
for i in range(len(data)):
    data_dict = data[i]
    # print(data_dict)
    with open("api.json", "w+") as f:
        json.dump(data_dict, f, ensure_ascii=False)
        f.write("\n")

# 将json文档转换成excel
import pandas as pd
df = pd.read_json("api.json", lines=True, encoding="gbk")
# print(df["abstract"])
df.to_excel("api.xlsx")