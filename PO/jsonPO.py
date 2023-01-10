# coding: utf-8
# ****************************************************************
# Author        : John
# Date          : 2020-5-12
# Description   : json对象层
# jsonpath官网语法 https://https://goessner.net/

# todo:数据结构
# json 文件中存储的数据结构为“列表” 或 “字典”。
# todo: 安装
# pip3 install jsonpath-rw
# 下载包：https://pypi.python.org/pypi/jsonpath-rw
# todo: 线上json文档(可用于测试)
# https://www.lagou.com/lbs/getAllCitySearchLabels.json
# https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=__all__&utm_source=toutiao&widen=1&tadrequire=true
# from script.json1 import jsonDumpsDefault

# todo: json对象比较,输出差异部分
# pip3 install deepdiff
# ****************************************************************

# '''
# 1.1 将JSON格式序列化内容保存到文件  json2file()
# 1.2 将变量保存到json文件  var2file()
# 1.3 json格式的文件内容保存到excel  file2xlsx()
#
# 2.1 用jsonpath_expr表达式从文件中提取json值  getValueFromFileByExpr()  如： stu_info[*].name
# 2.2 用jsonpath_expr表达式从变量中提取json值 getValueFromVarByExpr()
# 2.3 用jsonpath从文件中提取json值  getValueFromFileByJsonpath()
# 2.4 用jsonpath从变量中提取json值  getValueFromVarByJsonpath()  如：$.token
#
# 3. 比较2个json对象，输出差异部分
#
# '''


from jsonpath_rw import parse
from deepdiff import DeepDiff

from PO.DataPO import *

Data_PO = DataPO()


class JsonPO:
    def json2file(self, varUrl, varData, varFile):

        """
        1.1 将JSON格式序列化内容保存到文件
        """

        res = requests.get(
            url=varUrl,
            headers={"user-agent": Data_PO.getUserAgent()},
            proxies={"url": Data_PO.getIpAgent()},
        )
        d_res = json.loads(res.text)
        data = d_res[varData]
        for i in range(len(data)):
            data_dict = data[i]
            with open(varFile, "a+") as f:
                json.dump(data_dict, f, ensure_ascii=False)
                f.write("\n")

    def var2file(self, var, varFile):

        """
        1.2 将变量保存到json文件
        """

        with open(varFile, "w") as f_obj:
            json.dump(var, f_obj)

    def file2xlsx(self, varFile, xlsxFile):

        """
        1.3 json格式的文件内容保存到excel
        file2xlsx(''api.json',"api.xlsx")
        """

        df = pd.read_json(varFile, lines=True, encoding="gbk")
        df.to_excel(xlsxFile)

    def getValueFromFileByExpr(self, varFile, varParse):

        """
        # 2.1 从文件中解析json中的值 用jsonpath_expr表达式从文件中提取json值
        """

        with open(varFile, "r", encoding="utf-8") as f_obj:
            varData = json.load(f_obj)
        jsonpath_expr = parse(varParse)
        male = jsonpath_expr.find(varData)
        return [match.value for match in male]

    def getValueFromVarByExpr(self, varData, varParse):

        """
        # 2.2 从变量中解析json中的值 用jsonpath_expr表达式从变量中提取json值
        """

        jsonpath_expr = parse(varParse)
        male = jsonpath_expr.find(varData)
        return [match.value for match in male]

    def getValueFromFileByJsonpath(self, varJsonFile, varParse):
        """
        # 2.3 用jsonpath从文件中提取json值
        :param varJsonFile:
        :param varParse:
        :return:
        """
        with open(varJsonFile, "r", encoding="utf-8") as f_obj:
            varData = json.load(f_obj)
        if isinstance(varData, str):
            dict = json.loads(varData)  # 字符串转字典
            return jsonpath.jsonpath(dict, expr=varParse)
        else:
            return jsonpath.jsonpath(varData, expr=varParse)

    def getValueFromVarByJsonpath(self, varData, varParse):
        """
        # 2.4 用jsonpath从变量中提取json值
        :param varData:
        :param varParse:
        :return:
        """
        if isinstance(varData, str):
            dict = json.loads(varData)  # 字符串转字典
            return jsonpath.jsonpath(dict, expr=varParse)
        else:
            return jsonpath.jsonpath(varData, expr=varParse)


if __name__ == "__main__":

    Json_PO = JsonPO()

    # print("1.1 将JSON格式序列化内容保存到文件".center(100, "-"))
    # Json_PO.json2file('https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=__all__&utm_source=toutiao&widen=1&tadrequire=true', "data", "data/api.json")

    varDictJson = {
        "error_code": 10,
        "stu_info": [
            {
                "id": 309,
                "name": "小白",
                "sex": "男",
                "age": 28,
            },
            {"id": 310, "name": "小黑", "sex": "男", "age": 28, "addr": "河南省济源市北海大道32号"},
        ],
    }

    # print("1.2 将变量写入json文件".center(100, "-"))
    # Json_PO.var2file(varDictJson, "data/var.json")

    # print("1.3 jsonfile 写入excel文件".center(100, "-"))
    # Json_PO.file2xlsx('data/api.json', "data/api.xlsx")
    # Json_PO.file2xlsx('data/var.json', "data/var.xlsx")

    # print("2.1 用jsonpath_expr表达式从文件中提取json值".center(100, "-"))
    print(
        Json_PO.getValueFromFileByExpr("data/dict.json", "stu_info[*].name")
    )  # ['小白', '小黑']
    print(
        Json_PO.getValueFromFileByExpr("data/dict.json", "stu_info[0].name")
    )  # ['小白']
    #
    # # print("2.2 用jsonpath_expr表达式从变量中提取json值".center(100, "-"))
    print(Json_PO.getValueFromVarByExpr(varDictJson, "stu_info[*].name")[1])  # 小黑
    print(Json_PO.getValueFromVarByExpr(varDictJson, "stu_info[1].name"))  # ['小黑']
    # print(Json_PO.getValueFromVarByExpr(varDictJson, "stu_info[2].name"))  # []
    # print(Json_PO.getValueFromVarByExpr(varDictJson, "error_code"))  # [10]
    #
    # # print("2.3 用jsonpath从文件中提取json值".center(100, "-"))
    # varStrJson = {"status": 200, "msg": "success", "token": "e351b73b1c6145ceab2a02d7bc8395e7"}
    # Json_PO.var2file(varStrJson, "JsonPO/dict1.json")  # "12345678"
    print(
        Json_PO.getValueFromFileByJsonpath("data/dict1.json", "$.token")
    )  # ['e351b73b1c6145ceab2a02d7bc8395e7']
    #
    # # print("2.4 用jsonpath从变量中提取json值".center(100, "-"))
    varStrJson = {
        "status": 200,
        "msg": "success",
        "token": "e351b73b1c6145ceab2a02d7bc8395e7",
    }
    print(
        Json_PO.getValueFromVarByJsonpath(varStrJson, "$.token")
    )  # ['e351b73b1c6145ceab2a02d7bc8395e7']
    #
    # d = {
    #     "error_code": 0,
    #     "stu_info": [
    #         {
    #             "id": 2059,
    #             "name": "小白",
    #             "sex": "男",
    #             "age": 28,
    #             "addr": "河南省济源市北海大道32号",
    #             "grade": "天蝎座",
    #             "phone": "18378309272",
    #             "gold": 10896,
    #             "info": {
    #                 "card": 434345432,
    #                 "bank_name": '中国银行'
    #             }
    #
    #         },
    #         {
    #             "id": 2067,
    #             "name": "小黑",
    #             "sex": "男",
    #             "age": 28,
    #             "addr": "河南省济源市北海大道32号",
    #             "grade": "天蝎座",
    #             "phone": "12345678915",
    #             "gold": 100
    #         }
    #     ]
    # }
    #
    # print(Json_PO.getValueFromVarByJsonpath(d, '$.stu_info[*].name'))  # ['小白', '小黑']   //stu_info下的所有name
    # print(Json_PO.getValueFromVarByJsonpath(d, '$.stu_info[0].name'))  # ['小白']
    # print(Json_PO.getValueFromVarByJsonpath(d, '$.stu_info[1].name'))  # ['小黑']
    # print(Json_PO.getValueFromVarByJsonpath(d, '$..name'))  # ['小白', '小黑']   //所有的name
    # print(Json_PO.getValueFromVarByJsonpath(d, '$..bank_name'))  # ['中国银行']
    # print(Json_PO.getValueFromVarByJsonpath(d, '$..name123'))  # False  //没有找到返回False
    #
    # x = {
    #     "store": {
    #     "book": [
    #       { "category": "reference",
    #         "author": "Nigel Rees",
    #         "title": "Sayings of the Century",
    #         "price": 8.95
    #       },
    #       { "category": "fiction",
    #         "author": "Evelyn Waugh",
    #         "title": "Sword of Honour",
    #         "price": 12.99
    #       },
    #       { "category": "fiction",
    #         "author": "Herman Melville",
    #         "title": "Moby Dick",
    #         "isbn": "0-553-21311-3",
    #         "price": 8.99
    #       },
    #       { "category": "fiction",
    #         "author": "J. R. R. Tolkien",
    #         "title": "The Lord of the Rings",
    #         "isbn": "0-395-19395-8",
    #         "price": 22.99
    #       }
    #     ],
    #     "bicycle": {
    #       "color": "red",
    #       "price": 19.95
    #     }
    #   }
    # }
    #
    # print(Json_PO.getValueFromVarByJsonpath(x, '$.store.book[*].author')) # ['Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien']
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..author'))  # ['Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien']
    # print(Json_PO.getValueFromVarByJsonpath(x, '$.store.*'))
    # print(Json_PO.getValueFromVarByJsonpath(x, '$.store..price'))  # [8.95, 12.99, 8.99, 22.99, 19.95]
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[2]'))  # [{'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}]
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[(@.length-1)]'))  # [{'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[-1:]'))  # 同上
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[:2]'))  # [{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Evelyn Waugh', 'title': 'Sword of Honour', 'price': 12.99}]
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[0,1]'))  # 同上
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[?(@.isbn)]'))  # [{'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}, {'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}]
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..book[?(@.price<10)]'))  # [{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}]
    # print(Json_PO.getValueFromVarByJsonpath(x, '$..*'))
    #

    print("3. 比较2个json对象，输出差异部分".center(100, "-"))

    v1 = {
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
                "info": {"card": 434345432, "bank_name": "中国银行"},
            }
        ],
    }

    v2 = {
        "error_code": 1,
        "stu_info": [
            {
                "id": 2059,
                "addr": "河南省济源市北海大道32号",
                "name": "小白",
                "sex": "男",
                "age": 28,
                "grade": "天蝎座",
                "phone": "18378309272",
                "gold": 10896,
                "info": {"card": 434345432000, "bank_name": "中国银行"},
            }
        ],
    }

    x = DeepDiff(v1, v2)
    print(
        x
    )  # {'values_changed': {"root['error_code']": {'new_value': 1, 'old_value': 0}, "root['stu_info'][0]['info']['card']": {'new_value': 434345432000, 'old_value': 434345432}}}
    print(
        x["values_changed"]
    )  # {"root['error_code']": {'new_value': 1, 'old_value': 0}, "root['stu_info'][0]['info']['card']": {'new_value': 434345432000, 'old_value': 434345432}}

    print("3.2 比较2个json对象，对指定位置元素的差异检查".center(100, "-"))
    x = DeepDiff(v1, v2, exclude_paths=["root['stu_info'][0]['info']"])
    print(
        x
    )  # {'values_changed': {"root['error_code']": {'new_value': 1, 'old_value': 0}}}
    print(
        x["values_changed"]
    )  # {"root['error_code']": {'new_value': 1, 'old_value': 0}}

    v1 = {"node1": 1, "node2": 2, "_node": 123}

    v2 = {"node1": 17, "node2": 28, "_node": 888}
    print("3.3 比较2个json对象，利用正则表达式定义要忽略的模糊层次规则".center(100, "-"))
    x = DeepDiff(v1, v2, exclude_regex_paths=[r"root\['node\d'\]"])
    print(
        x
    )  # {'values_changed': {"root['_node']": {'new_value': 888, 'old_value': 123}}}
    print(
        x["values_changed"]
    )  # {"root['_node']": {'new_value': 888, 'old_value': 123}}

    v1 = {"level1": 0.998}
    v2 = {"level1": 0.999}
    print("3.3 比较2个json对象，限制针对浮点数的检查精度".center(100, "-"))
    x = DeepDiff(v1, v2, significant_digits=2)
    print(x)  # {}

    x = DeepDiff(v1, v2)
    print(
        x
    )  # {'values_changed': {"root['level1']": {'new_value': 0.999, 'old_value': 0.998}}}

    print("3.4 比较2个json对象，忽略对指定类型数据的比较检查".center(100, "-"))
    from datetime import datetime, timedelta

    v1 = {"x": datetime.strptime("2022-08-07", "%Y-%m-%d"), "y": timedelta(seconds=100)}

    v2 = {
        "x": datetime.strptime("2032-03-17", "%Y-%m-%d"),
        "y": timedelta(seconds=12200),
    }

    x = DeepDiff(v1, v2, exclude_types=[datetime, timedelta])
    print(x)  # {}
