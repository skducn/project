# coding: utf-8
# *******************************************************************
# Author     : John
# Date       : 2019-1-29
# Description: dir函数 common - dir1.py
# dir()函数可以查看对象内所有属于及方法
# *******************************************************************

def gerInternalFunc(varType, param):
    object = dir(varType)
    count = 0
    for i in range(len(object)):
        if param == '':
            if '__' not in object[i]:
                print(object[i])
                count += 1
        elif param == '__':
            if '__' in object[i]:
                print(object[i])
                count += 1
        elif param == 'all':
            print(object[i])
            count += 1
    print(str(type(varType)) + '内置函数：' + str(count) + '/' + str(len(object)))

# 列表内置函数清单
# gerInternalFunc([],'all')  # 返回所有内置函数
# gerInternalFunc([],'__') # 返回带__XX__的内置函数
# gerInternalFunc([],'')  # 返回不带__XX__的内置函数

# 字符串内置函数清单
# gerInternalFunc('','')

# 字典内置函数清单
gerInternalFunc({},'all')

# 元组内置函数清单
# gerInternalFunc((),'')
