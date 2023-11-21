# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-11-18
# Description: # api（json）转 excel
# *****************************************************************

# 将json文档转换成excel
import pandas as pd
df = pd.read_json("api.json", lines=True, encoding="gbk")
# print(df["abstract"])
df.to_excel("api.xlsx")