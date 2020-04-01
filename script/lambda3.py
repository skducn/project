# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-12-19
# Description: 输入编号，返回相应内容
# ********************************************************************************************************************

g = lambda x : x+2
info = [g(x) for x in range(1,10)]
print(info)



#
# msgCtrl = "1 : pause\n2 : stop\n3 : restart\nother to quit\n"
#
# ctrlMap = {
#     '1': lambda: doPause(),
#     '2': lambda: doStop(),
#     '3': lambda: doRestart()}
# def doPause():
#     print('do pause')
# def doStop():
#     print('do stop')
# def doRestart():
#     print('do restart')
#
# if __name__ == '__main__':
#     print(msgCtrl)
#     cmdCtrl = input('Input : ')
#     if cmdCtrl  in ctrlMap:
#         ctrlMap[cmdCtrl]()