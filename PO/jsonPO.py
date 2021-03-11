# coding: utf-8
#****************************************************************
# Author        : John
# Date          : 2020-5-12
# Description   : 使用json 模块操作文件
# json 文件中存储的数据结构为“列表” 或 “字典”。
# 安装： pip3 install jsonpath-rw
# 官网： 1.4.0 https://pypi.python.org/pypi/jsonpath-rw
# jsonpath官网 https://goessner.net/articles/JsonPath/
# 网上一个json文档，https://www.lagou.com/lbs/getAllCitySearchLabels.json
#****************************************************************

'''
1 将字符串、列表、字典保存在json文件中
2 获取json文件中的值
3 获取json字典中属性值或批量重复属性的值 by jsonpathrw , 如： stu_info[*].name
4 获取json字典中属性值或批量重复属性的值 by jsonpath， 如：$.token
'''

import json, sys, jsonpath
from jsonpath_rw import parse

class JsonPO():

    # 1，将字符串、列表、字典保存在json文件中
    def saveFile(self, varJsonFile, varListDict):
        with open(varJsonFile, 'w') as f_obj:
            json.dump(varListDict, f_obj)

    # 2，获取json文件中的值
    def getValue(self, varJsonFile):
        # json.load(f_obj) 从json文件读取数据到内存中
        try:
            with open(varJsonFile, 'r') as f_obj:
                numbers = json.load(f_obj)
            return (numbers)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    # 3，获取json字典中属性值或批量重复属性的值 by jsonpathrw
    def getValueByJsonpathrw(self, varData, varParse):
        jsonpath_expr = parse(varParse)
        male = jsonpath_expr.find(varData)
        return [match.value for match in male]

    # 4，获取json字典中属性值或批量重复属性的值 by jsonpath
    def getValueByJsonpath(self, varData, varParse):
        try:
            if isinstance(varData, str):
                dict = json.loads(varData)  # 字符串转字典
                return jsonpath.jsonpath(dict, expr=varParse)
            else:
                return jsonpath.jsonpath(varData, expr=varParse)
        except:
            return None


if __name__ == '__main__':

    Json_PO = JsonPO()

    print("1 将字符串、列表、字典保存在json文件中".center(100, "-"))
    Json_PO.saveFile("JsonPO/list.json", [1, 2, 3, 4, 5, 6, 7])  # [1, 2, 3, 4, 5, 6, 7]
    Json_PO.saveFile("JsonPO/dict.json", {1: "a", 2: "b"})  # {"1": "a", "2": "b"}
    Json_PO.saveFile("JsonPO/str.json", "12345678")  # "12345678"
    Json_PO.saveFile("JsonPO/list2.json", (3, 4, 5))   # [3, 4, 5]   //注意：元组以列表形式保存。


    print("2，获取json文件中的值".center(100, "-"))
    print(Json_PO.getValue("JsonPO/list.json"))  # [1, 2, 3, 4, 5, 6, 7]  //列表
    print(Json_PO.getValue("JsonPO/dict.json"))  # {"1": "a", "2": "b"}  //字典
    print(Json_PO.getValue("JsonPO/str.json"))  # 12345678 //字符串
    print(Json_PO.getValue("JsonPO/list2.json"))   # [3, 4, 5]  //列表


    print("3，获取json字典中值".center(100, "-"))
    varDictJson = {
        "error_code": 10,
        "stu_info": [
            {
                "id": 309,
                "name": "小白",
                "sex": "男",
                "age": 28,

            },
            {
                "id": 310,
                "name": "小黑",
                "sex": "男",
                "age": 28,
                "addr": "河南省济源市北海大道32号"

            }
        ]
    }

    print(Json_PO.getValueByJsonpathrw(varDictJson, "stu_info[*].name"))  # ['小白', '小黑']
    print(Json_PO.getValueByJsonpathrw(varDictJson, "stu_info[*].name")[1])  # 小黑
    print(Json_PO.getValueByJsonpathrw(varDictJson, "stu_info[1].name"))  # ['小黑']
    print(Json_PO.getValueByJsonpathrw(varDictJson, "stu_info[2].name"))  # []
    print(Json_PO.getValueByJsonpathrw(varDictJson, "error_code"))  # [10]


    varStrJson = {"status": 200, "msg": "success", "token": "e351b73b1c6145ceab2a02d7bc8395e7"}
    print(Json_PO.getValueByJsonpath(varStrJson, '$.token'))  # ['e351b73b1c6145ceab2a02d7bc8395e7']

    d = {
        "error_code": 0,
        "stu_info": [
            {
                "id": 2059,
                "name": "小白",
                "sex": "男",
                "age": 28,
                "addr": "河南省济源市北海大道32号",
                "grade": "天蝎座",
                "phone": "18378309272",
                "gold": 10896,
                "info": {
                    "card": 434345432,
                    "bank_name": '中国银行'
                }

            },
            {
                "id": 2067,
                "name": "小黑",
                "sex": "男",
                "age": 28,
                "addr": "河南省济源市北海大道32号",
                "grade": "天蝎座",
                "phone": "12345678915",
                "gold": 100
            }
        ]
    }

    print(Json_PO.getValueByJsonpath(d, '$.stu_info[*].name'))  # ['小白', '小黑']   //stu_info下的所有name
    print(Json_PO.getValueByJsonpath(d, '$.stu_info[0].name'))  # ['小白']
    print(Json_PO.getValueByJsonpath(d, '$.stu_info[1].name'))  # ['小黑']
    print(Json_PO.getValueByJsonpath(d, '$..name'))  # ['小白', '小黑']   //所有的name
    print(Json_PO.getValueByJsonpath(d, '$..bank_name'))  # ['中国银行']
    print(Json_PO.getValueByJsonpath(d, '$..name123'))  # False  //没有找到返回False

    x = {
        "store": {
        "book": [
          { "category": "reference",
            "author": "Nigel Rees",
            "title": "Sayings of the Century",
            "price": 8.95
          },
          { "category": "fiction",
            "author": "Evelyn Waugh",
            "title": "Sword of Honour",
            "price": 12.99
          },
          { "category": "fiction",
            "author": "Herman Melville",
            "title": "Moby Dick",
            "isbn": "0-553-21311-3",
            "price": 8.99
          },
          { "category": "fiction",
            "author": "J. R. R. Tolkien",
            "title": "The Lord of the Rings",
            "isbn": "0-395-19395-8",
            "price": 22.99
          }
        ],
        "bicycle": {
          "color": "red",
          "price": 19.95
        }
      }
    }

    print(Json_PO.getValueByJsonpath(x, '$.store.book[*].author')) # ['Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien']
    print(Json_PO.getValueByJsonpath(x, '$..author'))  # ['Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien']
    print(Json_PO.getValueByJsonpath(x, '$.store.*'))
    print(Json_PO.getValueByJsonpath(x, '$.store..price'))  # [8.95, 12.99, 8.99, 22.99, 19.95]
    print(Json_PO.getValueByJsonpath(x, '$..book[2]'))  # [{'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}]
    print(Json_PO.getValueByJsonpath(x, '$..book[(@.length-1)]'))  # [{'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
    print(Json_PO.getValueByJsonpath(x, '$..book[-1:]'))  # 同上
    print(Json_PO.getValueByJsonpath(x, '$..book[:2]'))  # [{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Evelyn Waugh', 'title': 'Sword of Honour', 'price': 12.99}]
    print(Json_PO.getValueByJsonpath(x, '$..book[0,1]'))  # 同上
    print(Json_PO.getValueByJsonpath(x, '$..book[?(@.isbn)]'))  # [{'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}, {'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
    print(Json_PO.getValueByJsonpath(x, '$..book[?(@.price<10)]'))  # [{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}]
    print(Json_PO.getValueByJsonpath(x, '$..*'))

