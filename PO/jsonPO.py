# coding: utf-8
#****************************************************************
# Author        : John
# Date          : 2020-5-12
# Description   : 使用json 模块操作文件
# json 文件中存储的数据结构为 列表 或 字典。
#****************************************************************

import json,sys

class JsonPO():


    # 1，将列表或字典保存在json文件中
    def setByJson(self, varJsonFile, varListDict):
        with open(varJsonFile, 'w') as f_obj:
            json.dump(varListDict, f_obj)

    # 2，获取json文件中的值
    def getByJson(self, varJsonFile):
        # json.load(f_obj) 从json文件读取数据到内存中
        try:
            with open(varJsonFile, 'r') as f_obj:
                numbers = json.load(f_obj)
            return (numbers)

        except:
            print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) +" row" )


if __name__ == '__main__':

    Json_PO = JsonPO()

    print("1，将列表或字典保存在json文件中".center(100, "-"))
    Json_PO.setByJson("jsonPO_list.json", [1, 2, 3, 4, 5, 6, 7])
    Json_PO.setByJson("jsonPO_dict.json", {1: "a", 2: "b"})
    Json_PO.setByJson("jsonPO_tuple.json", "12345678")
    Json_PO.setByJson("jsonPO_str.json", (3, 4, 5))


    print("2，获取json文件中的值".center(100, "-"))
    print(Json_PO.getByJson("jsonPO_list1.json"))  # [1, 2, 3, 4, 5, 6, 7]  //列表
    print(Json_PO.getByJson("jsonPO_dict.json"))  # {"1": "a", "2": "b"}  //字典
    print(Json_PO.getByJson("jsonPO_tuple.json"))  # 12345678 //字符串
    print(Json_PO.getByJson("jsonPO_str.json"))   # [3, 4, 5]  //元组转列表





