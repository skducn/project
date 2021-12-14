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
1.1 将url内容写入json文件 url2jsonfile()
1.2 将变量（字符串、列表、字典）写入json文件  setJsonFile()
1.3 将json文件写入excel jsonfile2xlsx()

2.1 用jsonpath_expr表达式从文件中提取json值  getValueFromFileByExpr()  如： stu_info[*].name
2.2 用jsonpath_expr表达式从变量中提取json值 getValueFromVarByExpr()
2.3 用jsonpath从文件中提取json值  getValueFromFileByJsonpath()
2.4 用jsonpath从变量中提取json值  getValueFromVarByJsonpath()  如：$.token


'''


from jsonpath_rw import parse
from PO.DataPO import *
Data_PO = DataPO()
from PO.MysqlPO import *
Mysql_PO = MysqlPO("192.168.0.234", "root", "123456", "epd", 3306)   # 测试


class JsonPO():

    def url2jsonfile(self, varApi, jsonFile):
        '''
        1.1 在线api（json内容）写入json文件
        :param api:
        :return:
        url2jsonfile('https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=__all__&utm_source=toutiao&widen=1&tadrequire=true','api.json')
        '''

        try:
            res = requests.get(url=varApi, headers={'user-agent': Data_PO.getUserAgent()}, proxies={"url": Data_PO.getIpAgent()})
            d_res = json.loads(res.text)
            data = d_res["data"]
            for i in range(len(data)):
                data_dict = data[i]
                with open(jsonFile, "a+") as f:
                    json.dump(data_dict, f, ensure_ascii=False)
                    f.write("\n")

            # # 将json文档转换成excel
            # df = pd.read_json("./JsonPO/api.json", lines=True, encoding="gbk")
            # df.to_excel("./JsonPO/api.xlsx")
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")

    def var2jsonfile(self, var, jsonFile):
        '''
        1.2 变量（字符串、列表、字典）写入json文件
        :param varJsonFile:
        :param varListDict:
        :return:
        '''

        try:
            with open(jsonFile, 'w') as f_obj:
                json.dump(var, f_obj)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    def jsonfile2xlsx(self, jsonFile, xlsxFile):
        '''
        1.3 jsonfile 写入excel
        :param api:
        :return:
        jsonfile2xlsx(''api.json',"api.xlsx")
        '''

        try:
            df = pd.read_json(jsonFile, lines=True, encoding="gbk")
            df.to_excel(xlsxFile)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")



    def getValueFromFileByExpr(self, varJsonFile, varParse):
        '''
        # 2.1 用jsonpath_expr表达式从文件中提取json值
        :param varJsonFile:
        :param varParse:
        :return:
        '''

        try:
            with open(varJsonFile, 'r', encoding='utf-8') as f_obj:
                varData = json.load(f_obj)
            jsonpath_expr = parse(varParse)
            male = jsonpath_expr.find(varData)
            return [match.value for match in male]
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    def getValueFromVarByExpr(self, varData, varParse):
        '''
        # 2.2 用jsonpath_expr表达式从变量中提取json值
        :param varData:
        :param varParse:
        :return:
        '''

        try:
            jsonpath_expr = parse(varParse)
            male = jsonpath_expr.find(varData)
            return [match.value for match in male]
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    def getValueFromFileByJsonpath(self, varJsonFile, varParse):
        '''
        # 2.3 用jsonpath从文件中提取json值
        :param varJsonFile:
        :param varParse:
        :return:
        '''
        try:
            with open(varJsonFile, 'r', encoding='utf-8') as f_obj:
                varData = json.load(f_obj)
            if isinstance(varData, str):
                dict = json.loads(varData)  # 字符串转字典
                return jsonpath.jsonpath(dict, expr=varParse)
            else:
                return jsonpath.jsonpath(varData, expr=varParse)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )

    def getValueFromVarByJsonpath(self, varData, varParse):
        '''
        # 2.4 用jsonpath从变量中提取json值
        :param varData:
        :param varParse:
        :return:
        '''
        try:
            if isinstance(varData, str):
                dict = json.loads(varData)  # 字符串转字典
                return jsonpath.jsonpath(dict, expr=varParse)
            else:
                return jsonpath.jsonpath(varData, expr=varParse)
        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )



if __name__ == '__main__':

    Json_PO = JsonPO()

    # print("1.1 将api在线json内容保存到变量".center(100, "-"))
    Json_PO.url2jsonfile('https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=__all__&utm_source=toutiao&widen=1&tadrequire=true', "JsonPO/api.json")


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

    # print("1.2 将变量（字符串、列表、字典）写入json文件".center(100, "-"))
    # Json_PO.var2jsonfile(varDictJson, "JsonPO/dict.json")  # "12345678"

    # print("1.3 jsonfile 写入excel文件".center(100, "-"))
    # Json_PO.jsonfile2xlsx('JsonPO/api.json', "JsonPO/api.xlsx")


    # # print("2.1 用jsonpath_expr表达式从文件中提取json值".center(100, "-"))
    # print(Json_PO.getValueFromFileByExpr("./JsonPO/dict.json", "stu_info[*].name"))  # ['小白', '小黑']
    #
    # # print("2.2 用jsonpath_expr表达式从变量中提取json值".center(100, "-"))
    # print(Json_PO.getValueFromVarByExpr(varDictJson, "stu_info[*].name")[1])  # 小黑
    # print(Json_PO.getValueFromVarByExpr(varDictJson, "stu_info[1].name"))  # ['小黑']
    # print(Json_PO.getValueFromVarByExpr(varDictJson, "stu_info[2].name"))  # []
    # print(Json_PO.getValueFromVarByExpr(varDictJson, "error_code"))  # [10]
    #
    # # print("2.3 用jsonpath从文件中提取json值".center(100, "-"))
    # varStrJson = {"status": 200, "msg": "success", "token": "e351b73b1c6145ceab2a02d7bc8395e7"}
    # Json_PO.var2jsonfile(varStrJson, "JsonPO/dict.json")  # "12345678"

    # print(Json_PO.getValueFromFileByJsonpath("./JsonPO/dict1.json", '$.token'))  # ['e351b73b1c6145ceab2a02d7bc8395e7']
    #
    # # print("2.4 用jsonpath从变量中提取json值".center(100, "-"))
    # varStrJson = {"status": 200, "msg": "success", "token": "e351b73b1c6145ceab2a02d7bc8395e7"}
    # print(Json_PO.getValueFromVarByJsonpath(varStrJson, '$.token'))  # ['e351b73b1c6145ceab2a02d7bc8395e7']
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
