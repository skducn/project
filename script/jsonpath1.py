# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-19
# Description   : jsonpath for python3
# *****************************************************************
# jsonpath官网 https://goessner.net/articles/JsonPath/
# 线上的一个json文档用于测试，https://www.lagou.com/lbs/getAllCitySearchLabels.json


import json, jsonpath

jsonstr = '{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}'
dict = json.loads(jsonstr)

# 获取根节点下的token节点的值
names = jsonpath.jsonpath(dict, expr='$.token')
print(names)  # ['e351b73b1c6145ceab2a02d7bc8395e7']
